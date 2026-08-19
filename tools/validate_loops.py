#!/usr/bin/env python3
"""Validate every loop file against the contract in PROTOCOL.md.

A loop is a markdown file, so nothing about it is checked by a compiler. This
script is the compiler: it reads `skills/LOOP-*.md`, enforces the frontmatter
and section contract from PROTOCOL.md section 14, and cross-checks the README
catalog so a new loop cannot land undiscoverable.

Standard library only, on purpose. CI installs nothing, and a contributor can
run it against a fresh clone with no setup:

    python tools/validate_loops.py

Exit code 0 means every loop conforms. Exit code 1 prints one line per
violation, each naming the file and what the contract expects.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"

FILENAME = re.compile(r"^LOOP-(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")

REQUIRED_KEYS = (
    "name",
    "loop-id",
    "description",
    "domain",
    "risk-class",
    "default-debate",
    "model-tiers",
)

# The three risk classes from PROTOCOL.md section 6, plus the staged form used
# by loops that begin read-only and open a branch only after a gate. A class may
# carry a trailing parenthetical scope note, e.g. `branch-mutating (loops only)`.
RISK_CLASSES = ("read-only→branch", "read-only", "branch-mutating", "infra-touching")

DEBATE_PROTOCOLS = ("FREE-MAD", "MAD", "MoE", "RA-CR")

# PROTOCOL.md section 14, in order. Every loop file carries all of them as `#`
# headings; the order is part of the contract so loops stay diffable side by side.
REQUIRED_SECTIONS = (
    "Mission",
    "Trigger",
    "Inputs",
    "Preconditions",
    "Execution DAG",
    "Node Specs",
    "Adversarial Check",
    "Exit Criteria",
    "Failure Routing",
    "Approval Gates",
    "RUN PROMPT",
)

# A loop has to run on someone else's repo with no edits, so anything that only
# resolves on one machine or inside one company is a portability bug.
NON_PORTABLE = (
    (re.compile(r"/Users/[A-Za-z0-9._-]+"), "an absolute macOS home path"),
    (re.compile(r"/home/[A-Za-z0-9._-]+"), "an absolute Linux home path"),
    (re.compile(r"[A-Za-z]:\\\\?Users\\\\?"), "an absolute Windows home path"),
    (re.compile(r"https?://localhost|https?://127\.0\.0\.1"), "a localhost URL"),
)

MAX_DESCRIPTION = 400


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def fail(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def check(self, condition: bool, where: str, message: str) -> bool:
        if not condition:
            self.fail(where, message)
        return condition


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | tuple[None, str]:
    """Split `---` frontmatter from the body.

    Deliberately not YAML: the contract is a flat `key: value` block, and a
    stdlib-only parser keeps CI dependency-free. A value containing `:` (every
    `model-tiers` line does) survives because only the first colon splits.
    """
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    block, body = text[4:end], text[end + 5 :]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        data[key.strip()] = value.strip()
    return data, body


def base_risk_class(value: str) -> str | None:
    """Strip a trailing parenthetical scope note and match the base class."""
    stem = value.split("(", 1)[0].strip()
    for known in RISK_CLASSES:
        if stem == known:
            return known
    return None


def validate_loop(path: Path, report: Report) -> dict[str, str] | None:
    where = f"skills/{path.name}"
    match = FILENAME.match(path.name)
    if not report.check(
        bool(match), where, "filename must look like LOOP-NN-kebab-slug.md"
    ):
        return None
    assert match is not None
    number, slug = match.group(1), match.group(2)

    text = path.read_text(encoding="utf-8")
    front, body = parse_frontmatter(text)
    if not report.check(
        front is not None, where, "missing or unterminated `---` frontmatter block"
    ):
        return None
    assert front is not None

    for key in REQUIRED_KEYS:
        report.check(key in front, where, f"frontmatter is missing `{key}`")

    if "loop-id" in front:
        report.check(
            front["loop-id"] == f"LOOP-{number}",
            where,
            f"`loop-id: {front.get('loop-id')}` does not match the filename "
            f"(expected LOOP-{number})",
        )
    if "name" in front:
        report.check(
            front["name"] == f"loop-{slug}",
            where,
            f"`name: {front.get('name')}` does not match the filename "
            f"(expected loop-{slug}) — the skill name is how agents invoke it",
        )
    if "risk-class" in front:
        report.check(
            base_risk_class(front["risk-class"]) is not None,
            where,
            f"`risk-class: {front['risk-class']}` is not one of "
            + ", ".join(RISK_CLASSES),
        )
    if "default-debate" in front:
        report.check(
            front["default-debate"] in DEBATE_PROTOCOLS,
            where,
            f"`default-debate: {front['default-debate']}` is not one of "
            + ", ".join(DEBATE_PROTOCOLS),
        )
    if "description" in front:
        report.check(
            0 < len(front["description"]) <= MAX_DESCRIPTION,
            where,
            f"`description` must be 1-{MAX_DESCRIPTION} characters "
            f"(it is {len(front['description'])})",
        )

    headings = [
        line[2:].strip() for line in body.splitlines() if line.startswith("# ")
    ]
    cursor = 0
    for section in REQUIRED_SECTIONS:
        found = next(
            (i for i, h in enumerate(headings) if h.lower().startswith(section.lower())),
            None,
        )
        if found is None:
            report.fail(where, f"missing required `# {section}` section")
            continue
        if found < cursor:
            report.fail(
                where,
                f"`# {section}` appears out of order — PROTOCOL.md section 14 fixes "
                "the section order so loops stay diffable",
            )
        cursor = max(cursor, found)

    run_prompt = body.rsplit("# RUN PROMPT", 1)
    if len(run_prompt) == 2:
        report.check(
            "```" in run_prompt[1],
            where,
            "`# RUN PROMPT` must contain a fenced code block a user can copy verbatim",
        )

    for pattern, label in NON_PORTABLE:
        hit = pattern.search(text)
        if hit:
            report.fail(
                where,
                f"contains {label} (`{hit.group(0)}`) — a loop must run on any "
                "repo with no edits beyond the target",
            )

    return front


def validate_catalog(loops: dict[str, Path], report: Report) -> None:
    """Every loop is linked from the README, and every README link resolves."""
    readme = README.read_text(encoding="utf-8")
    linked = set(re.findall(r"\(skills/(LOOP-\d{2}-[a-z0-9-]+\.md)\)", readme))

    for path in loops.values():
        if path.name not in linked:
            report.fail(
                "README.md",
                f"{path.name} is not linked from the catalog — a loop nobody can "
                "find is a loop nobody runs",
            )
    for name in sorted(linked):
        if not (SKILLS / name).exists():
            report.fail("README.md", f"links skills/{name}, which does not exist")

    claimed = re.findall(r"\*\*(\d+) autonomous", readme)
    for number in claimed:
        if int(number) != len(loops):
            report.fail(
                "README.md",
                f"claims {number} loops; the catalog ships {len(loops)}",
            )


RELATIVE_LINK = re.compile(r"\[[^\]]*\]\((?!https?:|mailto:|#)([^)\s]+)\)")
ANCHOR_LINK = re.compile(r"\[[^\]]*\]\(#([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def slugify(heading: str) -> str:
    """GitHub's heading-anchor rule: lowercase, drop punctuation, spaces to dashes."""
    text = re.sub(r"[`*_\[\]()]", "", heading).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"\s", "-", text.strip())


def validate_relative_links(report: Report) -> None:
    """Every relative markdown link resolves to a file that exists.

    Renaming a loop is a one-line change that silently breaks the README, the
    protocol, and half the cross-references between loops. Nothing else in a
    markdown-only repo would notice.
    """
    for path in sorted(ROOT.rglob("*.md")):
        if ".github" in path.parts:
            continue
        where = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for target in RELATIVE_LINK.findall(text):
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                report.fail(where, f"links to `{target}`, which does not exist")

        # Same-page anchors. Renaming a heading silently breaks every table of
        # contents entry pointing at it, and nothing about that looks wrong in a
        # diff — the link and the heading are usually far apart in the file.
        anchors = {slugify(h) for h in HEADING.findall(text)}
        for target in ANCHOR_LINK.findall(text):
            if target.lower() not in anchors:
                report.fail(
                    where,
                    f"links to `#{target}`, but no heading in the file has that "
                    "anchor — a heading was probably renamed",
                )


def validate_composition(fronts: dict[str, dict[str, str]], report: Report) -> None:
    """`composed-of` and `coordinates-with` may only name loops that exist.

    Two different relationships, both worth checking: `composed-of` is a
    meta-loop declaring the loops it *runs*, `coordinates-with` is a loop
    declaring the ones it hands findings to. A dangling reference in either is a
    loop telling an agent to reach for something that is not there.
    """
    known = set(fronts)
    for loop_id, front in fronts.items():
        for key in ("composed-of", "coordinates-with"):
            raw = front.get(key)
            if not raw:
                continue
            referenced = re.findall(r"LOOP-\d{2}", raw)
            if not referenced:
                report.fail(loop_id, f"`{key}` is set but names no LOOP-NN ids")
            for ref in referenced:
                if ref not in known:
                    report.fail(loop_id, f"`{key}` names {ref}, which does not exist")
                if ref == loop_id:
                    report.fail(loop_id, f"`{key}` lists the loop itself")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet", action="store_true", help="print only violations, not the summary"
    )
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        # Windows consoles still default to a legacy code page, and the contract
        # messages quote risk classes and arrows verbatim. Without this a Windows
        # contributor reads mojibake instead of the rule they broke.
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except (AttributeError, OSError):  # pragma: no cover - exotic stream
            pass

    report = Report()
    paths = sorted(SKILLS.glob("LOOP-*.md"))
    if not paths:
        print(f"error: no loop files found under {SKILLS}", file=sys.stderr)
        return 1

    loops: dict[str, Path] = {}
    fronts: dict[str, dict[str, str]] = {}
    for path in paths:
        front = validate_loop(path, report)
        if front is None:
            continue
        loop_id = front.get("loop-id", path.stem)
        if loop_id in loops:
            report.fail(
                f"skills/{path.name}",
                f"duplicate loop-id {loop_id} (already used by {loops[loop_id].name})",
            )
            continue
        loops[loop_id] = path
        fronts[loop_id] = front

    validate_composition(fronts, report)
    validate_catalog(loops, report)
    validate_relative_links(report)

    if report.errors:
        print(f"{len(report.errors)} contract violation(s):\n", file=sys.stderr)
        for error in report.errors:
            print(f"  {error}", file=sys.stderr)
        print(
            "\nThe contract lives in PROTOCOL.md section 14 and CONTRIBUTING.md.",
            file=sys.stderr,
        )
        return 1

    if not args.quiet:
        print(f"{len(loops)} loops conform to PROTOCOL.md section 14.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
