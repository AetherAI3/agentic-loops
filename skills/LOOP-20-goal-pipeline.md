---
name: loop-goal-pipeline
loop-id: LOOP-20
description: The catalog's entry gate — turns a plain-language goal into a validated, cycle-checked task DAG, adversarially reviews the plan, then dispatches it into any applicable catalog loops, re-verifying the DAG continuously as execution proceeds and routing verification failures back to goal clarification instead of running on a broken plan
domain: Goal Intake & Plan Validation — Catalog Entry Gate
risk-class: read-only→branch
default-debate: FREE-MAD
model-tiers: {scan: cheap, audit: mid, verdict: reasoning}
composed-of: [LOOP-11, LOOP-16]
---

# Mission

Every other loop in this catalog assumes it already knows its target and scope. LOOP-20 is what decides that — the front door a plain-language goal walks through before a catalog loop runs. A goal enters, gets validated for clarity and scope, decomposed into a task graph, checked for cycles and contradictions, adversarially reviewed, and only THEN dispatched — as one loop or, via LOOP-16's fan-out orchestrator, several independent loops running in parallel. Two properties separate this from a simple task-router: **the DAG is re-verified continuously as execution proceeds, not just once at intake** (a downstream loop's finding can invalidate an assumption the plan was built on — LOOP-20 catches that instead of letting execution drift silently out of sync with the plan), and **a verification failure routes back to goal clarification, not into a bad execution** (a cyclic or contradictory task graph means the goal itself was under-specified, and the fix belongs at the goal layer, not patched over in the DAG).

Without this loop, the other catalog loops are individually excellent but the operator has to manually decide "which loop, what scope, in what order" every time — and nothing catches a goal that implies a plan with a hidden circular dependency (e.g. "harden the API and also don't change any endpoint contracts the API hardening pass would need to change") until it's halfway executed. LOOP-20 is that missing layer: a validated goal produces a validated plan, and the plan's own execution keeps proving itself valid as it runs.

# Trigger

- Any time a goal is stated in plain language rather than as a specific `Run LOOP-NN on <target>` invocation — this is the loop that turns "hunt down and fix the flakiest part of this codebase" into a concrete dispatch plan.
- Before dispatching more than one loop from this catalog at once — LOOP-20's DAG-verify step is what proves the loops you're about to fan out (via LOOP-16) don't have a hidden ordering dependency or write-conflict.
- Whenever a running multi-loop plan needs to be re-validated mid-flight because one loop's findings changed what a downstream loop should do.
- On demand: `Run LOOP-20 with goal: "<plain-language goal>"`.

# Inputs (target repo/dir, scope flags)

- `target`: repo root.
- `goal`: the plain-language request. LOOP-20's node 1 is responsible for turning this into something structured — the operator does not need to pre-specify which of LOOP-01..19 applies.
- `synthetic_goal_set` (test/validation mode only): a hand-built set of goals including one with a deliberately circular implied dependency and one deliberately too vague to decompose, used to exercise nodes 3 and 6 against real cases rather than reasoning about them abstractly.
- `--validate-only`: nodes 1–5 only — produce the validated plan and adversarial-review verdict, do not dispatch.
- `--dispatch-existing-plan <plan-id>`: skip nodes 1–5, dispatch a previously validated plan (re-runs node 6's continuous DAG re-verify against it).

# Preconditions

- [PROTOCOL] read.
- The target catalog (this repo's `skills/LOOP-*.md`) readable, so node 2 can match goal-implied work to real loop capabilities rather than inventing dispatch targets that don't exist.
- Loop branch created before node 7 (dispatch) — nodes 1–6 are read-only planning; nothing mutates until a validated, adversarially-reviewed plan exists.

# Execution DAG (numbered nodes, [P] = parallelizable)

1. Goal clarity validation — is the goal specific enough to decompose? Reject-and-request-clarification if not, rather than guessing.
2. Task decomposition — break the validated goal into discrete tasks, each mapped to a candidate loop (one of LOOP-01..19) or a novel task with no existing loop match.
3. DAG construction & cycle verification — build the dependency graph between decomposed tasks, detect and resolve cycles.
4. [P] Novel-task flagging — any decomposed task with no LOOP-01..19 match is flagged for the operator rather than silently dropped or forced into an ill-fitting loop.
5. Adversarial plan review (LOOP-11 inline) — a hostile reviewer attacks the plan itself before execution, not just individual findings after the fact.
6. Dispatch — single loop directly, or multiple independent loops via LOOP-16's fan-out orchestrator if node 3's DAG shows genuine independence.
7. Continuous re-verification — as dispatched loops report findings, re-run node 3's DAG check against the CURRENT state, not the intake-time snapshot.
8. Failure routing — a node 3 or node 7 cycle/contradiction routes back to node 1 for goal re-clarification, carrying the specific contradiction as context (never a bare "try again").

Nodes 1→2→3 run sequentially (each depends on the prior's validated output). Node 4 runs in parallel with node 5 (both operate on node 3's output, independent concerns). Node 5 gates node 6 (no dispatch without a passing adversarial verdict). Node 7 runs continuously for the duration of node 6's dispatched work, not as a one-time step. Node 8 is a re-entry point triggered by node 3 or node 7's failure condition, not a normal forward edge.

# Node Specs

**Node 1 — Goal clarity validation.**
Action: check the goal against a concrete clarity bar — does it name a target (repo/dir/module), a scope boundary (what's explicitly out), and a success condition (how would you know it's done)? Missing any of the three does not get guessed at; the loop returns a specific clarification request naming exactly what's missing.
Tools: reasoning tier (this is a judgment call, not a mechanical check), Read (target repo structure for context).
Failure conditions: goal passes the clarity bar but the target doesn't exist/isn't readable → Dependency Failure, not a clarity failure — distinct failure class, distinct message.
Output artifact: `node-1-goal-validation.md` (pass/fail + specific gaps if fail).

**Node 2 — Task decomposition.**
Action: break the validated goal into discrete tasks. For each task, match it against this catalog's real loop descriptions (`skills/LOOP-*.md`) — a task like "audit the backend for OWASP issues" maps to LOOP-01, "close test coverage gaps" maps to LOOP-12, "overhaul website SEO/GEO and simplify the public experience" maps to LOOP-22, and "tune this one retry threshold" maps to LOOP-18. A task with no reasonable match is NOT force-fit; it's marked `novel` for node 4.
Tools: Read (catalog descriptions), reasoning tier for the matching judgment.
Failure conditions: goal decomposes into zero tasks (too abstract despite passing node 1) → route to node 8 (back to node 1) rather than proceeding with an empty plan.
Output artifact: `node-2-task-decomposition.md` — task table: `task | matched loop (or novel) | rationale`.

**Node 3 — DAG construction & cycle verification.**
Action: build the dependency graph from node 2's tasks (which tasks must complete before others can start — e.g. a task that changes an API contract must precede a task that hardens tests against that contract). Run cycle detection (DFS with visited/in-stack tracking, same mechanism any dependency-graph validator uses). If a cycle is found, do NOT silently break it and proceed — a cycle at the goal-decomposition level means the goal itself contains a contradiction, and that's node 8's job to route back, not this node's job to paper over.
Tools: Bash/mid tier (graph algorithm), Read.
Failure conditions: a cycle is found → this is the expected trigger for node 8, not an error state; report the exact cycle (which tasks, which dependency edges) so node 1's re-clarification request can be specific.
Output artifact: `node-3-dag.md` — the graph, cycle-free confirmation or the specific cycle found.

**Node 4 — Novel-task flagging [P].**
Action: for every task node 2 marked `novel` (no catalog match), surface it to the operator explicitly rather than dropping it from the plan or silently executing it with an ad-hoc, unaudited approach. A novel task is a signal the catalog itself may need a new loop (see LOOP-15's self-optimization meta-loop) — this node's job is to flag it clearly, not to solve it.
Tools: Read node 2's output.
Failure conditions: none halting; an empty novel-task list is a valid, common result.
Output artifact: `node-4-novel-tasks.md`.

**Node 5 — Adversarial plan review [P with node 4].**
Action: run [PROTOCOL] step 4 (LOOP-11 inline, FREE-MAD) against the WHOLE PLAN — not a single finding, the plan's structure itself. The reviewer attacks: does the task→loop matching in node 2 actually fit (a task loosely matched to a loop that doesn't really cover it is worse than marking it novel)? Does the dependency ordering in node 3 make sense, or does it force sequential execution where parallel dispatch was actually safe (or vice versa — claiming independence that isn't real)? Is the plan's scope actually bounded by the goal, or has it quietly grown?
Tools: LOOP-11 inline (FREE-MAD), reasoning tier.
Failure conditions: REJECT verdict → do not proceed to node 6; return to node 2 with the critique as new context (not node 1 — the goal itself was clear, the decomposition was the problem).
Output artifact: `node-5-plan-review.md` — verdict + critique if rejected.

**Node 6 — Dispatch.**
Action: for a single-task plan (or a plan whose DAG shows sequential dependency throughout), dispatch the matched loop(s) in dependency order. For a plan whose DAG shows genuinely independent branches (node 3's graph has no edges between them), dispatch via LOOP-16's Fan-Out Orchestrator — LOOP-20 does the independence PROOF (the DAG), LOOP-16 does the actual parallel execution and worker-isolation mechanics; this node doesn't reimplement LOOP-16's job, it hands off to it.
Tools: Bash/orchestration harness, LOOP-16 (for parallel branches).
Failure conditions: a loop fails to dispatch (repo access, missing tooling per that loop's own preconditions) → Dependency Failure for that task specifically; does not halt sibling tasks unless node 3's DAG shows a real dependency on the failed task.
Output artifact: dispatch manifest + per-task loop-run references.

**Node 7 — Continuous re-verification.**
Action: as dispatched loops report findings and complete, re-run node 3's cycle/contradiction check against the CURRENT state of the plan — not the intake-time snapshot. A concrete trigger: LOOP-13 (Drift & Debt) finds a circular dependency in the codebase that node 2's task list didn't know about when it assumed two tasks were independent; that's exactly the kind of live-state drift this node exists to catch, mid-execution, not after.
Tools: Read (in-flight loop status/findings), Bash (re-run node 3's cycle check), mid tier.
Failure conditions: a NEW cycle/contradiction surfaces mid-execution → route to node 8, but distinguish this from node 3's intake-time failure: some already-dispatched, already-committed work from before the contradiction surfaced may need to stand (it's on its own loop branch per that loop's own risk class) while remaining undispatched tasks route back.
Output artifact: `node-7-reverify-log.md` — running log, one entry per re-verification pass.

**Node 8 — Failure routing (re-entry, not a forward node).**
Action: package the specific contradiction/cycle from node 3 or node 7 (which tasks, which goal-implied assumption broke) as structured context, and re-enter node 1 with it — the re-clarification request names the exact conflict, not a generic "please rephrase."
Tools: Read node 3/7 output, reasoning tier for the clarification framing.
Failure conditions: three round-trips through node 8 without resolution → HALT, surface the full contradiction history to the operator directly rather than looping indefinitely on an unresolvable goal.
Output artifact: `node-8-reclarification-request.md`.

# Adversarial Check (reviewer persona + what it attacks)

Persona: **the Plan Skeptic** — assumes a task→loop match is wrong until the match is justified against the loop's actual description, and assumes a claimed independent-branch pair secretly shares a write surface until proven otherwise. FREE-MAD, attacks in order:

1. **Node 2's matches** — for each task→loop pairing, demands the specific line in that loop's `skills/LOOP-NN-*.md` description that justifies the match; a vibes-based match gets rejected back to `novel`.
2. **Node 3's independence claims** — for any two tasks the DAG treats as parallel-safe, checks whether both loops' scope (per their own Inputs sections) could touch the same files; an unverified independence claim is exactly LOOP-16's node-2 concern, imported here at the planning layer.
3. **Node 5's own review** — did it actually attack the plan's structure, or did it just restate node 2's task list approvingly? A review with no structural critique on a plan this loop hasn't seen before is Silent Agreement (forces a second round, [PROTOCOL] §1 step 4).
4. **Node 7's re-verify cadence** — is it actually running continuously, or only checked once and then forgotten for the rest of a long-running dispatch? Demands the re-verify log's timestamps, not a claim that it ran.

Maximum 2 debate rounds; survivors go to operator-deferred.

# Exit Criteria (quantitative, overrides [PROTOCOL])

- Every node 2 task→loop match cites the specific loop-description text that justifies it, or is marked `novel`.
- Node 3's DAG is cycle-free before node 6 dispatches anything — zero exceptions.
- Node 5's adversarial review produces a structural critique or an explicit "no structural issue found, here's what I checked" — never a bare pass.
- Node 7 re-verification runs at least once per completed dispatched task, not just at plan intake.
- Any node 8 re-entry carries the specific contradiction, never a generic retry.
- Final confidence ≥ 0.85; governance row written.

# Failure Routing (only deviations from [PROTOCOL])

- A node 3/7 cycle is the EXPECTED trigger for node 8, not a loop-halting error — the loop is designed to route on this, not crash on it.
- Three round-trips through node 8 without resolution is the one case that DOES halt — an unresolvable goal needs a human, not a fourth attempt.

# Approval Gates (only deviations from [PROTOCOL])

- Node 6's dispatch of any `branch-mutating` loop (per that loop's own risk-class) still requires that loop's own approval gates — LOOP-20 does not bypass a dispatched loop's individual sign-off requirements, it only decides WHICH loops run and WHEN.
- A plan touching 3+ loops simultaneously (via LOOP-16 fan-out) surfaces the full dispatch manifest to the operator before node 6 executes, even under an otherwise-automatic risk class — breadth of simultaneous mutation is its own risk dimension.

# RUN PROMPT

```
Run LOOP-20 (Goal Pipeline) on <repo> with goal: "<plain-language goal>".
Follow skills/LOOP-20-goal-pipeline.md under [PROTOCOL] (see PROTOCOL.md in
this repo). Validate the goal, decompose it against the real LOOP-01..19
catalog, build and cycle-check the DAG, run LOOP-11's adversarial review on
the PLAN itself before dispatching anything, then dispatch — via LOOP-16's
fan-out orchestrator if genuinely independent branches exist. Keep
re-verifying the DAG as dispatched loops report back; route any
contradiction to goal re-clarification, never patch over it silently. No
merge without my approval, same as every other loop here.
```
