# PROTOCOL — The Loop Kernel

> Every loop in this collection inherits this protocol. Loop files reference it as `[PROTOCOL]`.
> A loop file is **runnable**: hand it to Claude Code (or any capable coding agent) with `Run LOOP-XX on <target>` and the agent executes it end-to-end under these rules.

---

## 1. The Four-Step Execution Protocol

Every loop node executes under this contract:

| Step | Action | Mechanics |
|------|--------|-----------|
| 1. Parse & Ingest | Manifest deserialization | Read the loop file, convert the Execution DAG into a strictly ordered graph. Identify parallel vs sequential nodes, required tools, and parameter mappings. This defines the formal execution boundary — nothing outside it runs. |
| 2. Environmental Scope | Context gathering | Sample application state BEFORE node 1: active branch, `git status`, deployment logs, env vars, and any available codebase map for the target files/modules. Prune context aggressively — never bulk-cat files. |
| 3. Monitored Execution | Gated action steps | Execute one node at a time. Catch runtime errors, evaluate against the node's declared failure conditions, pipe sanitized output to the next node. Every mutation happens on a checkpointed branch (see §6), never directly on main. |
| 4. Adversarial Check | Loop trigger check | Before marking a node or the loop resolved, pass the loop's completion criteria + the node output to an adversarial reviewer (LOOP-11 protocol, inline mode). If rejected, the loop resets to the failed node with the critique as new context. |

**Authority separation:** conversational authority (proposing, clarifying) is never execution authority. Execution flows only through actions that satisfy the loop's machine-readable constraints.

---

## 2. Context Discipline (MANDATORY)

- **Structured comprehension over raw grep.** If your project has a code-graph or knowledge-graph tool (an MCP server, an IDE's semantic index, `ast-grep`, Semgrep, ctags/LSP "find references"), use it to trace call graphs and dependencies. Raw string `grep` is fine only for locating literals (keys, error strings), never for tracing logic.
- **Read existing architecture docs/ADRs** for the target module before patching it — the highest-fan-in files carry the highest ripple risk.
- **Compress episodics.** Node outputs handed to the next node are structured summaries (findings tables, diffs, scores), never raw transcripts.

---

## 3. Confidence & Risk Scoring (every node output)

Every node and every final loop artifact MUST carry a confidence block:

```yaml
confidence_block:
  confidence: 0.00-1.00      # calibrated belief the output is correct
  risk: low|medium|high|critical
  evidence: [static-analysis, tests, tracing, manual-read, ...]
  unknown: ["what was NOT verified"]
  missing_evidence: ["what would raise confidence"]
```

**Gates:**
- `confidence < 0.70` → node output rejected, retry with critique (max retries per §5).
- `confidence < threshold declared in loop's Exit Criteria` → loop cannot terminate as PASS.
- Reviewer agents receive the confidence block and attack the `unknown` list first.

---

## 4. Failure Classification Taxonomy

Never report "task failed." Classify, then route:

| Class | Loop Reaction |
|-------|---------------|
| Syntax Failure | Auto-fix, re-run node (cheap tier) |
| Logic Failure | Re-reason with critique, escalate model tier after 2 strikes |
| Architecture Failure | Halt node, emit finding, require drift/debt follow-up (LOOP-13) |
| Security Failure | HALT LOOP. Emit CRITICAL artifact. Human approval required to continue. |
| Dependency Failure | Pin/resolve, re-run; if unresolvable → emit finding, skip node |
| Context Overflow | Compress inputs, re-scope node to smaller slice, resume |
| Tool Failure | Retry once; then degrade to fallback tool; log to governance |
| Rate Limit | Exponential backoff, max 3; then checkpoint + suspend |
| Timeout | Checkpoint, split node into sub-nodes, resume |
| Permission Failure | Stop, surface to operator — never self-escalate privileges |
| Model Hallucination | Discard output, re-run with adversarial verifier attached |
| Workflow Failure | Resume from last checkpoint (§7), never restart node 1 |
| Memory Failure | Rebuild context from artifacts on disk, not from recall |

---

## 5. Retry & Escalation Budget

- Max **3 retries per node**, max **2 full adversarial debate rounds per loop** unless the loop declares otherwise.
- Escalation ladder (cost-aware model routing):
  1. **Cheap tier** (small/fast model class): mechanical fixes, formatting, classification, first-pass scans.
  2. **Mid tier** (standard model class): standard audit nodes, code edits, test writing.
  3. **Reasoning tier** (frontier/deep-reasoning model class): architecture judgments, security verdicts, final adversarial review.
- **Verify cheap, escalate only on rejection.** A cheap verifier checks first; the reasoning tier is invoked only when the cheap verifier rejects or confidence is under gate.
- Prompt caching: keep the loop file + this protocol at the top of agent prompts so repeated nodes hit cache.

---

## 6. Rollback Engineering (GitOps rule)

Every mutating loop follows:

```
checkpoint (branch or git tag)
  → modify
  → test
  → verify (adversarial check)
  → commit (on loop branch)
  → rollback if confidence < loop threshold OR verifier rejects twice
```

- **Never edit main directly.** Loop work happens on `loop/<loop-id>-<date>` branches.
- Every commit message: `loop(<LOOP-ID>): <node> — <change>` + confidence score in body.
- Rollback = `git reset --hard <checkpoint>` on the loop branch + a governance event (§8). Rollbacks are data, not shame.

---

## 7. Workflow Recovery (Checkpoints)

- After every completed node, write a checkpoint artifact: `_loopstate/<loop-id>/<run-id>/node-<N>.json` containing node output summary + confidence block + git SHA.
- On any failure class that suspends the loop, resume = load last checkpoint, re-run failed node only. **Node 11 fails → resume at node 11, never node 1.**

---

## 8. Runtime Governance Metrics (emit every run)

Append one row per run to `_loopstate/governance-ledger.md`:

| Metric | Meaning |
|--------|---------|
| success_rate | Did the loop hit exit criteria? |
| retry_count | Infinite-loop detector |
| debate_rounds | Adversarial depth used |
| tool_success_pct | Broken integration detector |
| human_overrides | Autonomy quality |
| tokens_spent / tier_mix | Cost engineering |
| hallucinations_caught | Verifier value |
| false_positive_rate | Audit quality (findings rejected by verifier / total) |
| mttr | Time from finding → verified fix |
| rollbacks | Unsafe-patch detector |

Trend review of this ledger is LOOP-14's job.

---

## 9. Observability Trace (OpenTelemetry-for-AI shape)

Every agent invocation inside a loop records, in the run's checkpoint dir:

```
task_id → node → agent role (planner|researcher|security|reviewer|executor|verifier)
  reasoning_summary (≤5 lines)
  tools_used
  duration
  tokens (if available)
  confidence_block.confidence
  result: PASS|FAIL|<failure-class>
```

---

## 10. Human Approval Classes

| Action class | Approval |
|--------------|----------|
| Read / audit / report | Automatic |
| Write docs, tests, `_loopstate` artifacts | Automatic |
| Refactor on loop branch | Adversarial reviewer sign-off |
| Merge to main / open PR | Operator approval (hand back findings first) |
| DB migration, schema change | Human explicit approval |
| Production delete / deploy / secret rotation | Multi-step human approval — loop MUST halt |

Default posture: **loops produce branches + artifacts + findings; the operator merges.**

---

## 11. Adversarial Debate Protocols (used by LOOP-11 and inline checks)

| Protocol | Use when |
|----------|----------|
| Consensus (standard MAD) | Low-stakes: labeling, lint-class findings — fast convergence OK |
| **FREE-MAD** (consensus-free, score-based) | DEFAULT for audits/security — reviewers attack independently, no forced agreement, score-based verdict across rounds |
| MoE self-debate | Cheap rapid passes inside one agent (self-critique before handoff) |
| RA-CR (rank-adaptive) | Long-horizon refactors — judge reorders/silences reviewers per round to force diversity |

Anti-pattern to detect: **Silent Agreement** — if all reviewers agree in round 1 with no cited evidence, force one more round with a hostile persona.

---

## 12. Quantitative Exit Criteria (pattern)

Every loop declares measurable termination. Template (loops override values):

- All CRITICAL and HIGH findings resolved or explicitly operator-deferred
- Test pass rate ≥ 99% on touched surface
- Coverage on touched code ≥ 80%
- Zero unresolved OWASP-critical issues
- Perf regression within declared budget
- Retry count ≤ budget (§5)
- Final confidence ≥ 0.85
- Governance row written

A loop that cannot meet exit criteria terminates as **FAIL-with-artifact**, never as silent success.

---

## 13. Standard Loop Artifact (the handoff)

Every loop run ends with `_loopstate/<loop-id>/<run-id>/AUDIT-ARTIFACT.md`:

```markdown
# <LOOP-ID> Run Artifact
run_id / date / target / branch / git SHA
## Verdict: PASS | FAIL | HALTED-<class>
## Confidence block (final)
## Findings table: id | severity | domain | file:line | description | fix status
## Diffs applied (list of commits on loop branch)
## Tests generated (every bug found MUST leave a permanent regression test)
## Governance row (copy)
## Recommended next loops
```

This artifact is machine-readable — it's designed to compile 1:1 into any workflow engine's node schema, if you ever want to promote a loop from a Claude Code prompt into a fully automated pipeline.

---

## 14. Standard Loop File Template (all LOOP-XX files follow this)

```markdown
---
name: loop-<slug>
loop-id: LOOP-XX
description: <one line>
domain: <domain>
risk-class: read-only | read-only→branch | branch-mutating | infra-touching
default-debate: FREE-MAD | MAD | MoE | RA-CR
model-tiers: {scan: cheap, audit: mid, verdict: reasoning}
---
# Mission
# Trigger (when the operator runs this)
# Inputs (target repo/dir, scope flags)
# Preconditions
# Execution DAG (numbered nodes, [P] = parallelizable)
# Node Specs (per node: action, tools, failure conditions, output artifact)
# Adversarial Check (reviewer persona + what it attacks)
# Exit Criteria (quantitative, overrides protocol §12)
# Failure Routing (only deviations from protocol §4)
# Approval Gates (only deviations from protocol §10)
# RUN PROMPT (verbatim block you paste or invoke)
```

Notes on the template:

- `name` must be `loop-<slug>` and `loop-id` must be `LOOP-NN`, both matching the
  filename `LOOP-NN-<slug>.md`. `name` is how an agent invokes the skill, so a
  mismatch means the loop installs under a name nobody can call.
- A `risk-class` may carry a trailing parenthetical scope note —
  `branch-mutating (loops only)` — but the class before the parenthesis is one of
  the four above.
- Section headings may carry a parenthetical, but must begin with the section
  name and appear in the order listed, so any two loops diff cleanly.
- Optional `composed-of: [LOOP-NN, ...]` declares which loops a meta-loop
  orchestrates; optional `coordinates-with: [LOOP-NN, ...]` declares the loops a
  base loop hands findings to or defers to. Both are checked: a dangling
  reference is a loop telling an agent to reach for something that is not there.

`python tools/validate_loops.py` enforces all of the above, plus README catalog
coverage and relative links. It is standard library only and runs on a fresh
clone with no install.
