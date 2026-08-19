<div align="center">

# Agentic Loops

**22 autonomous, self-contained "loop" systems that turn Claude Code (or any AI coding agent) into a full audit-and-fix pipeline — with built-in adversarial review, confidence scoring, and safe rollback.**

[![GitHub stars](https://img.shields.io/github/stars/AetherAI3/agentic-loops?style=social)](https://github.com/AetherAI3/agentic-loops/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Made by Aether AI](https://img.shields.io/badge/made%20by-Aether%20AI-6f42c1?style=flat-square)](https://github.com/AetherAI3)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-compatible-CC785C?style=flat-square)](https://claude.com/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

</div>

---

Each loop is a complete, runnable audit-and-fix system in one markdown file — a mission, an execution DAG, a hostile adversarial reviewer, and quantitative exit criteria, all sharing one contract defined in [`PROTOCOL.md`](PROTOCOL.md).

<p align="center">
  <img src="docs/loop-cards.svg" alt="LOOP-01 to LOOP-15, color-coded by risk class" width="100%">
</p>

## Table of Contents

- [Quick Start](#quick-start)
- [The Loop Catalog](#the-loop-catalog) — the 16 base loops
- [Meta-Loops — Loops That Run the Catalog](#meta-loops--loops-that-run-the-catalog) — LOOP-16 to LOOP-21
- [How It Works](#how-it-works)
- [Installing as a Claude Code Skill](#installing-as-a-claude-code-skill)
- [Suggested Cadence](#suggested-cadence)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

Pick a loop, paste its `RUN PROMPT` into your AI coding agent, done. No install required.

```
Run LOOP-01 on <your-repo> (scope: <api dir>)
```

The agent reads the loop file, reads [`PROTOCOL.md`](PROTOCOL.md) for the shared execution rules, and runs the whole audit end-to-end — handing you back a branch, a findings artifact, and nothing merged without your sign-off.

Three ways to use this repo:

1. **Copy-paste** — open any file in [`skills/`](skills/), copy the `RUN PROMPT` block at the bottom, paste it into Claude Code (or ChatGPT, Cursor, Windsurf, etc.) with your target repo.
2. **Install as a skill** — each loop's frontmatter is already skill-compatible (see [Installing as a Claude Code Skill](#installing-as-a-claude-code-skill)).
3. **Clone the whole set** — `git clone` this repo and point your agent at the `skills/` folder for the full catalog.

## The Loop Catalog

The 16 base loops, each auditing one fixed surface. The six that take *other
loops* as input — LOOP-16 through LOOP-21 — are catalogued in
[Meta-Loops](#meta-loops--loops-that-run-the-catalog) below.

| # | Loop | Domain | Risk | What it does |
|---|------|--------|------|---------------|
| [01](skills/LOOP-01-backend-api.md) | Backend & API Hardening | Backend & API Architecture | branch-mutating | AST-driven audit: OWASP API Top 10 (BOLA/BOPLA/SSRF/auth/resource limits), N+1 queries, dead code, logging hygiene. |
| [02](skills/LOOP-02-frontend-a11y.md) | Frontend & Accessibility | Frontend & Accessibility | branch-mutating | Component/bundle audit plus a live Playwright accessibility-tree interrogation (roles, ARIA, focus traps, contrast) that static scanners miss. |
| [03](skills/LOOP-03-mobile-native.md) | Mobile & Native Hardening | Mobile & Native Platforms | branch-mutating | Dual-layer (JS/Dart + native) audit: bridge traffic, ANR hunters, list virtualization, manifest hardening, keystore/keychain, pinning. |
| [04](skills/LOOP-04-agent-runtime.md) | Agent Runtime & Tooling | Agent Runtime & Tooling | read-only→branch | Audits your own agent stack against the OWASP Agentic Top 10: MCP/tool schema strictness, least-privilege agency, prompt-injection surfaces. |
| [05](skills/LOOP-05-memory-ux.md) | Agentic Memory Hardening | Memory & Cognitive Architecture | branch-mutating | Four-tier memory audit (working/episodic/semantic/procedural), tenant isolation, unbounded growth, GDPR erasure UI. |
| [06](skills/LOOP-06-ux-ui-visual.md) | UX/UI Visual Integrity | UX/UI & Human Factors | branch-mutating | Visual regression, stateful UI battery, graceful-degradation checks, memory-transparency panel audit. |
| [07](skills/LOOP-07-infra-devops.md) | Infrastructure & DevOps | Infrastructure, Cloud & DevOps | infra-touching | Docker/K8s/Terraform/secrets/IAM/SBOM/supply-chain audit across your deployment mesh — read+plan, never live-mutates without approval. |
| [08](skills/LOOP-08-cicd-release.md) | CI/CD & Release Engineering | CI/CD & Release Engineering | branch-mutating | Pipeline audit: is CI *actually* running, caching, test gating, artifact signing, rollback automation, canary/blue-green, feature flags. |
| [09](skills/LOOP-09-data-layer.md) | Data Layer Integrity | Data Architecture & Persistence | infra-touching | Schema/migration safety, FK/orphan/cascade audit, index coverage, RLS/grant self-escalation sweep, backup **restore** verification. |
| [10](skills/LOOP-10-ai-security.md) | AI Security Red-Team | Governance, Compliance & Risk | read-only | Red-teams your own AI stack: prompt injection, RAG/memory/embedding poisoning, model supply chain, jailbreaks, goal drift, reward hacking. |
| [11](skills/LOOP-11-adversarial-review.md) | Adversarial Review Engine | Cross-cutting engine | read-only | The debate engine every other loop calls inline: generator vs. hostile reviewer, FREE-MAD default, silent-agreement detection. |
| [12](skills/LOOP-12-test-mutation-chaos.md) | Test, Mutation & Chaos | Continuous Evaluation | branch-mutating | Closes coverage gaps, mutation-tests your suite to find tests that don't actually test anything, injects chaos (DB/cache/LLM/MCP failures). |
| [13](skills/LOOP-13-drift-debt.md) | Architectural Drift & Debt | Continuous Evaluation | read-only | Detects layer violations, circular deps, dead APIs/services; scores technical debt 0–100 across six axes, trended over time. |
| [14](skills/LOOP-14-governance-telemetry.md) | Governance & Telemetry | Runtime Observability | read-only | Audits the autonomous system itself: is it improving, looping, degrading, wasting tokens, or getting less reliable? |
| [15](skills/LOOP-15-self-optimization.md) | Self-Optimization Meta-Loop | Continuous Evaluation | branch-mutating (loops only) | The recursive-improvement loop: failure → root cause → fix → generalized pattern → proposed diff to the loops themselves. Human-gated always. |
| [22](skills/LOOP-22-website-growth-overhaul.md) | Website Growth & Simplification Overhaul | Website Growth, Search Visibility & Generative Discovery | branch-mutating | Evidence-first whole-site overhaul: simplify routes/content/UI, repair technical SEO, validate entity truth, test generative retrieval, and protect accessibility, performance, and conversion. |

**Risk classes:** `read-only` never touches your code · `branch-mutating` works only on an isolated loop branch, never main · `infra-touching` reads live infrastructure and proposes plans, never applies changes without explicit approval. (Same three classes apply to the meta-loops and integration below.)

## Meta-Loops — Loops That Run the Catalog

LOOP-01 through LOOP-15 and LOOP-22 each audit one fixed surface. LOOP-16 through LOOP-20 are the five base meta-loops: they take *other loops* — or a plain-language goal — as their input. LOOP-21 is the first integration loop, composing all five into a full merge lifecycle. Notation below: `[NN + NN]` = loops feeding in, `→` = then, `?` = branch point.

| # | Loop | Kind | Risk | Takes as input |
|---|------|------|------|----------------|
| [16](skills/LOOP-16-fanout-orchestrator.md) | Fan-Out Orchestrator | meta | branch-mutating | Two or more loops with non-overlapping scope |
| [17](skills/LOOP-17-sparring-partners.md) | Sparring Partners | meta | branch-mutating | One breaker loop, one builder loop, one artifact |
| [18](skills/LOOP-18-the-ratchet.md) | The Ratchet | meta | branch-mutating | One loop with a single number or patch to tune |
| [19](skills/LOOP-19-idea-arena.md) | Idea Arena | meta | read-only | Open findings from any loops, as candidate ideas |
| [20](skills/LOOP-20-goal-pipeline.md) | Goal Pipeline | meta · **flagship** | read-only→branch | A goal in plain English |
| [21](skills/LOOP-21-merge-protocol.md) | Merge Protocol | integration | branch-mutating | A pull request, plus the five meta-loops above |

**[LOOP-20 — Goal Pipeline](skills/LOOP-20-goal-pipeline.md) is the one to start with** — the front door. Hand it a goal in plain English and it plans, checks, and dispatches the applicable catalog loops for you. Everything below is a tool LOOP-20 already knows how to reach for.

---

**[16 — Fan-Out Orchestrator](skills/LOOP-16-fanout-orchestrator.md)** · `branch-mutating`
Split one task into independent pieces, run each on its own worker in parallel, no waiting on the slowest one.
```
16: [01 + 02 + 07] → prove independent → 3 workers run parallel → collect → merge report
```
*Example: backend audit, frontend audit, and infra audit don't touch the same files — run all three at once instead of one after another.*
Pairs with: any two+ loops with non-overlapping scope · gated by LOOP-20's DAG proof.

**[17 — Sparring Partners](skills/LOOP-17-sparring-partners.md)** · `branch-mutating`
Standing attacker vs. defender match on one artifact — keeps something already audited from rotting back to unsafe.
```
17: breaker=[10] vs builder=[01] → shared findings/fix queue → round N → trend to human
```
*Example: LOOP-10 keeps red-teaming your auth module, LOOP-01 keeps patching what it finds, LOOP-12 regression-tests every builder fix so nothing silently reverts.*
Pairs with: 10 (breaker's toolkit) + 01/05 (builder's toolkit) + 12 (regression backstop).

**[18 — The Ratchet](skills/LOOP-18-the-ratchet.md)** · `branch-mutating`
Change one thing, measure, keep it only if proven better — never batches, never un-welds.
```
18: [06 + 15] mutate → 11 debate → pass? weld : revert + loop
```
*Example: LOOP-06 finds a UX patch candidate, LOOP-15 generalizes it into one testable change, LOOP-11 adversarially debates whether it's actually an improvement — pass welds it permanently, fail reverts and the ratchet tries a different single change next round.*
Pairs with: any loop that has one number/patch to tune (06, 08 timeouts, 12 fuzz corpus size) + 11 for the verdict.

**[19 — Idea Arena](skills/LOOP-19-idea-arena.md)** · `read-only`
Diverse candidate ideas, one shared debate-and-mutation arena, one converged idea with a paper trail.
```
19: idea1=[13 debt] + idea2=[14 drift] + idea3=[10 gap] → arena debate+mutate → converged idea → handoff
```
*Example: three loops each surface a different "what should we fix next" candidate — the arena doesn't just pick one, it merges the strongest parts of all three into one spec, then hands it to LOOP-20 to plan and dispatch.*
Pairs with: any loops with open findings to seed candidates from + 11 (final gate on the handoff) + 20 (receives it).

**[20 — Goal Pipeline](skills/LOOP-20-goal-pipeline.md)** · `read-only→branch` · **flagship**
Plain-language goal in, validated dependency-checked plan out, dispatched into whichever catalog loops fit.
```
20: goal="harden API + dedupe code" → decompose → [01] + [13] independent → 16 fan-out → 11 reviews plan → dispatch
```
*Example: one goal implies two unrelated tasks — LOOP-20 proves they don't conflict, hands both to LOOP-16 to run in parallel instead of you manually sequencing them, and keeps re-checking the plan as results come in.*
Pairs with: everything — this is the loop that decides which other loops to run.

**[21 — Merge Protocol](skills/LOOP-21-merge-protocol.md)** · `branch-mutating` · **integration**
Anchor the real remote trunk, capture a PR and its goals immutably, adversarially simplify it one verified change at a time, prove CI actually ran, merge only with operator approval, then replay the original contract over the entire integrated trunk and open a scoped follow-up PR for real gaps.
```
21: PR → capture remote+PR+goals → [20 plan + 16/17/19 inspect + 11 debate] → 18 ratchet → 08 gate → approve+merge → whole-trunk replay → follow-up PR
```
*Example: a PR is green on its own diff, but after merge an untouched caller violates the original acceptance criteria — the post-merge replay catches the seam and prepares a narrow, lineage-linked follow-up instead of declaring victory at the merge button.*
Composes: all five meta-loops (16–20) · hard gates: 08 (real CI liveness), 11 (hostile verdict), 15 (process learning only).

## How It Works

One shared contract in [`PROTOCOL.md`](PROTOCOL.md) — read it for the full spec:

- **4-step protocol** — ingest → scope → execute → adversarial check.
- **Confidence blocks** — every output scored, risk-rated, with explicit unknowns.
- **13-class failure taxonomy** — routes, never just "fails."
- **Checkpointed rollback** — every mutation on an isolated branch.
- **FREE-MAD debate** — a hostile reviewer persona before anything ships.
- **Quantitative exit criteria** — `FAIL-with-artifact` beats silent success.

## Installing as a Claude Code Skill

Each loop's YAML frontmatter (`name`, `description`, etc.) is already skill-shaped. To install one:

```bash
mkdir -p ~/.claude/skills/loop-backend-api
cp skills/LOOP-01-backend-api.md ~/.claude/skills/loop-backend-api/SKILL.md
```

Repeat per loop, or copy the whole `skills/` folder and adapt the frontmatter `name` field per file. Once installed, invoke with `/loop-backend-api` (or your agent's skill-invocation syntax) instead of pasting the `RUN PROMPT` manually.

## Suggested Cadence

A reasonable starting rhythm — tune it to your team:

| Cadence | Loops |
|---|---|
| Weekly sweep | 01 (backend), 02 (frontend), 13 (drift/debt) |
| Pre-release | 08 (CI/CD), 12 (test/mutation/chaos), 06 (UX/UI) |
| Monthly deep audit | 07 (infra), 09 (data layer), 10 (AI security), 05 (memory) |
| Continuous / every N runs | 14 (governance), then 15 (self-optimization) |
| Relaunch or growth overhaul | 22 (website growth, simplification, SEO/GEO) |

## Contributing

New loops, sharper adversarial personas, better exit criteria — all welcome, and
the best first PR is usually making an existing loop catch something it misses.

Nothing to install. The one command CI runs is the one you run:

```bash
python tools/validate_loops.py
```

It checks the frontmatter and section contract from [`PROTOCOL.md`](PROTOCOL.md)
section 14, catalog coverage, and every relative link in the repo. Full path
from idea to merged loop — including the safety rules a loop must not weaken —
in [`CONTRIBUTING.md`](CONTRIBUTING.md). Scoped starting points are labelled
[`good first issue`](https://github.com/AetherAI3/agentic-loops/labels/good%20first%20issue).

## License

[MIT](LICENSE) — use it, fork it, ship it.

---

<div align="center">

Built by **[Aether AI](https://github.com/AetherAI3)**

</div>
