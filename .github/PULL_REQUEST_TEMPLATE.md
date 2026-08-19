## What changes, and what failure made it necessary

<!--
A loop changes because something got through, something false-alarmed, or
something was unrunnable on a normal repo. Name it. "Improved wording" without a
motivating failure is hard to review and impossible to regression-test.
-->

## Validation

- [ ] `python tools/validate_loops.py` passes locally (no install needed).
- [ ] I ran the changed `RUN PROMPT` against a real repo with a real agent, and the run is described below.

**Agent and model used:**
**Target shape (language, framework, rough size):**
**What the run produced:**

<!--
If you could not run it, say so here rather than leaving it blank - a
documentation-only change does not need a run, and pretending otherwise costs
the next reviewer more than admitting it.
-->

## Safety boundary

- [ ] The loop stays inside its declared `risk-class`, or this PR changes the class deliberately and says so.
- [ ] Nothing merges to a default branch without operator approval.
- [ ] No project-specific paths, hostnames, tool names, or infrastructure assumptions were introduced.

## For a new loop only

- [ ] `loop-id` and `name` match the filename.
- [ ] All eleven sections from PROTOCOL.md section 14 are present, in order.
- [ ] The `RUN PROMPT` is a fenced block that works verbatim.
- [ ] The loop is added to the README catalog table.
