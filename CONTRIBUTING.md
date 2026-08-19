# Contributing

Loops are markdown files. There is no build step, no package to install, and no
dependency on how the maintainers run their own systems. If you can read a loop
file, you can change one.

The only thing you need locally is Python 3.10+, and only to run the validator:

```bash
git clone https://github.com/AetherAI3/agentic-loops.git
cd agentic-loops
python tools/validate_loops.py
```

That prints `21 loops conform to PROTOCOL.md section 14.` on a clean checkout.
CI runs the same command with no install step, so a green local run is a green
PR.

## Pick your first contribution

| If you want to… | Start with… |
| --- | --- |
| Make a loop catch something it misses | [Improve an existing loop](#improve-an-existing-loop) — the best first PR |
| Report that a `RUN PROMPT` broke | [Open a run-prompt bug](https://github.com/AetherAI3/agentic-loops/issues/new?template=run-prompt-bug.yml) |
| Audit a surface nothing covers | [Add a new loop](#add-a-new-loop) |
| Fix a stale claim or a broken link | A direct PR; the validator checks links for you |

Issues labelled [`good first issue`](https://github.com/AetherAI3/agentic-loops/labels/good%20first%20issue)
are scoped so that one PR closes them.

## What a loop is

One file under `skills/` is one complete audit-and-fix system: a mission, an
execution DAG, per-node tool and failure specs, a hostile reviewer, quantitative
exit criteria, and a `RUN PROMPT` you paste into an agent. Every loop shares the
execution contract in [`PROTOCOL.md`](PROTOCOL.md) — read at minimum sections 1,
6, 10, and 12 before changing behavior.

### The contract, in short

**Naming.** `skills/LOOP-NN-kebab-slug.md`, where `NN` is the next free
two-digit id. Frontmatter `loop-id` must be `LOOP-NN` and frontmatter `name`
must be `loop-<kebab-slug>` — both derived from the filename, both enforced by
the validator, because `name` is what an agent invokes the skill by.

**Frontmatter.** Seven required keys, exactly as in
[`PROTOCOL.md` section 14](PROTOCOL.md):

```yaml
---
name: loop-<slug>
loop-id: LOOP-NN
description: <one line, under 400 characters>
domain: <the surface this audits>
risk-class: read-only | read-only→branch | branch-mutating | infra-touching
default-debate: FREE-MAD | MAD | MoE | RA-CR
model-tiers: {scan: cheap, audit: mid, verdict: reasoning}
---
```

A risk class may carry a scope note in parentheses — `branch-mutating (loops
only)` — but the class before the parenthesis has to be one of the four.
An optional `composed-of: [LOOP-NN, ...]` key declares which loops a meta-loop
orchestrates, and `coordinates-with: [LOOP-NN, ...]` declares the loops a base
loop hands findings to or defers to. The validator checks that every id either
one names exists.

**Sections.** Eleven `#` headings, in this order:

```
Mission · Trigger · Inputs · Preconditions · Execution DAG · Node Specs
Adversarial Check · Exit Criteria · Failure Routing · Approval Gates · RUN PROMPT
```

Headings may carry a parenthetical — `# Trigger (when the operator runs this)` —
but must start with the section name and stay in order, so any two loops diff
against each other cleanly.

**Portability.** A loop runs on someone else's repo with no edits beyond the
target. No absolute home paths, no `localhost` URLs, no assuming a particular
CI provider, ORM, cloud, or internal tool exists. Where a loop benefits from a
tool not everyone has, phrase it conditionally the way LOOP-13 does with code
graphs: *"if you maintain one."* The validator rejects the obvious violations;
the reviewer catches the rest.

## Safety requirements

These are not style preferences. A loop hands an autonomous agent a plan to
change someone's codebase, and every one of these exists because the alternative
is an agent that cannot be undone.

1. **Declare the least invasive risk class that can do the job.** `read-only`
   never touches code. `branch-mutating` works only on an isolated loop branch.
   `infra-touching` reads live infrastructure and proposes plans. A loop that
   exceeds its declared class is a safety bug, not a wording bug.
2. **Nothing merges to a default branch inside a loop.** Loops end at a branch,
   a findings artifact, and a human decision. PROTOCOL.md section 10 owns the
   approval classes; deviate only in your `# Approval Gates` section, explicitly.
3. **Every mutation is checkpointed and revertible.** PROTOCOL.md section 6 —
   commit per node on the loop branch, so a bad node is one revert, not an
   archaeology exercise.
4. **The adversary has to be able to fail the loop.** A reviewer persona that
   cannot produce a FAIL verdict is decoration. State what it attacks and what
   evidence it demands.
5. **`FAIL-with-artifact` beats silent success.** Exit criteria are numbers.
   "Looks good" is not an exit criterion.

## Improve an existing loop

The most useful PRs are small and motivated by a real failure:

- a bug class the loop should have caught and did not,
- an exit criterion the loop can pass while the problem is still present,
- an adversarial persona that accepts what it should attack,
- a failure that routes into the wrong class or dead-ends,
- an assumption that makes the loop unrunnable on a normal repo.

Say in the PR **what failure motivated the change**. That sentence is what a
reviewer checks the diff against, and it is the difference between a change that
can be evaluated and one that can only be agreed with.

## Add a new loop

1. Check the catalog first. Extending an existing loop beats a new one unless
   the surface is genuinely uncovered — a thin loop dilutes the catalog.
2. Open a [new-loop proposal](https://github.com/AetherAI3/agentic-loops/issues/new?template=new-loop.yml)
   and agree the domain, risk class, and adversary before writing the file. The
   DAG is cheap to change in an issue and expensive to change in review.
3. Copy the template from [`PROTOCOL.md` section 14](PROTOCOL.md) into
   `skills/LOOP-NN-your-slug.md` and fill in every section.
4. Add a row to the README catalog table. The validator fails the build if a
   loop exists that the README does not link — an unlisted loop is one nobody
   runs.
5. Run `python tools/validate_loops.py`.

## Testing your change

There is no unit test for a prompt, so the test is running it.

```bash
python tools/validate_loops.py
```

checks the mechanical contract: frontmatter keys and values, filename/`loop-id`/
`name` agreement, all eleven sections present and in order, a fenced `RUN
PROMPT`, no duplicate ids, no non-portable paths, `composed-of` references that
resolve, README catalog coverage, and every relative markdown link in the repo.

It does **not** check whether the loop works. That part is on you:

1. Point the changed `RUN PROMPT` at a real repository with a real agent.
2. Record which agent and model you used, roughly what the target looked like,
   and what the run produced.
3. Put that in the PR. Prefer a target you can talk about publicly; the shape of
   the repo matters more than its name.

If you genuinely cannot run it — a documentation fix, a link repair — say so in
the PR instead of leaving the box blank. An honest "not run, docs only" costs a
reviewer nothing. An unchecked box costs them a round trip.

## Pull requests

- Branch from `master`, one reason per PR.
- Conventional commit subjects: `feat: add LOOP-22 ...`, `fix: tighten LOOP-08
  exit criteria`, `docs: ...`.
- Fill in the PR template, including the run notes and the safety boundary.
- CI must be green. It runs one command; you can run the same one.

## License

Contributions are MIT, same as the rest of the repo.
