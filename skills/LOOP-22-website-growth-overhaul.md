---
name: loop-website-growth-overhaul
loop-id: LOOP-22
description: Evidence-first website simplification and growth overhaul spanning crawlability, technical SEO, generative discovery, content clarity, information architecture, performance, accessibility, and conversion without ranking-hack claims
domain: Website Growth, Search Visibility & Generative Discovery
risk-class: branch-mutating
default-debate: FREE-MAD
model-tiers: {scan: cheap, audit: mid, verdict: reasoning}
coordinates-with: [LOOP-02, LOOP-06, LOOP-08, LOOP-11, LOOP-12, LOOP-13]
---

# Mission

Turn a public website into a simpler, clearer, faster, more trustworthy acquisition system
for both people and machine-mediated discovery. LOOP-22 audits the whole path from discovery
through conversion:

```text
discover -> crawl -> render -> index -> understand -> retrieve/cite -> visit -> act -> measure
```

The loop is deliberately broader than a metadata sweep and stricter than a redesign brief.
It may simplify routes, navigation, templates, components, content, structured data, and
client-side behavior, but every mutation must map to a declared user or growth outcome and
survive regression testing. Deleting complexity is preferred when it preserves intent and
evidence; adding another page, schema object, dependency, tracking script, or AI-specific file
requires proof that the added surface has a real consumer.

SEO is the durable foundation. GEO is treated as a measured extension: make canonical facts,
first-party evidence, authorship, product limits, and source relationships easy to retrieve and
attribute, then test actual systems instead of claiming a universal generative-engine ranking
formula. LOOP-22 never guarantees rankings, traffic, citations, or conversions from a code diff.
Those are post-deployment outcomes that require an observation window.

# Trigger (when the operator runs this)

- Before a website redesign, migration, domain change, CMS change, or public launch.
- After sustained loss in qualified organic traffic, index coverage, search impressions,
  generative citations, engagement, or conversion, after seasonality and tracking defects are
  considered.
- When navigation, route sprawl, duplicated content, or template proliferation makes the site
  difficult to understand or maintain.
- When public product facts, documentation, pricing, policies, or entity descriptions are
  inconsistent across routes.
- After a major search or generative-discovery platform change, provided the new behavior is
  verified from a primary source before it changes the mutation plan.
- On demand: `Run LOOP-22 on <repo> (scope: <public-site-dir-or-routes>)`.

# Inputs (target repo/dir, scope flags)

- `target`: repository or website source root.
- `scope`: `full-site`, a directory, route pattern, page list, or template set.
- `growth_goal`: the business outcome to support, with a named metric when available.
- `priority_journeys`: query or referral source -> landing route -> intended next action.
- `priority_routes`: canonical routes whose availability and intent must not regress.
- `baseline_queries`: optional representative branded, non-branded, commercial,
  informational, comparison, support, and conversational questions.
- `analytics`: optional first-party search, traffic, event, and conversion data. Read-only.
- `competitor_set`: optional comparison set for content-gap research, never permission to copy.
- `locales`, `devices`, `environments`: supported variants; default environment is local or
  staging. Production access is read-only.
- `measurement_window`: post-deployment observation period. Default 28 days; change it when
  seasonality, crawl cadence, or traffic volume makes that statistically dishonest.
- `risk_budget`: `low|medium|high`; default `medium`.
- `--audit-only`: run nodes 0-6 and emit the plan without source mutations.
- `--allow-content-rewrite`, `--allow-route-change`, `--allow-schema-change`,
  `--allow-navigation-change`, `--allow-analytics-change`: false unless explicitly supplied.

# Preconditions

1. [PROTOCOL] read; remote default branch and exact baseline SHA recorded.
2. Worktree clean or the loop isolated in a new worktree. Mutations occur only on
   `loop/LOOP-22-<YYYY-MM-DD>` (optional run-id suffix for concurrent runs).
3. Scope, growth goal, priority routes, and at least one reproducible priority journey are
   declared. Missing analytics limits the verdict to technical/readiness outcomes; it does not
   authorize invented traffic estimates.
4. Existing architecture, brand, content, SEO, analytics, privacy, and accessibility guidance
   for the target has been read before proposing a cross-template change.
5. Untouched build, test, crawl, render, accessibility, and performance baselines are captured
   where the repository supports them. Pre-existing failures are labeled, never attributed to
   this loop.
6. Live search-platform, analytics, and generative-engine checks use authorized access and
   respect terms, rate limits, robots controls, privacy, and data-retention rules.
7. A human owner exists for claims involving brand position, product capability, pricing,
   legal/policy text, health/finance, deletion, navigation, redirects, or analytics semantics.

# Evidence and Anti-Hype Rails

Evidence is ranked in this order: current primary platform documentation; first-party target
data; peer-reviewed or reproducible research; independently reproducible third-party data;
vendor opinion. Every finding records its evidence tier and observation date. A lower tier may
generate an experiment, but cannot override a higher-tier platform contract without direct
reproduction.

The execution agent must refresh time-sensitive guidance at run time. These sources establish
the starting contract, not eternal ranking rules:

- [Google's generative AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
  says foundational SEO, crawlability, useful non-commodity content, and clear site structure
  remain central. It also says Google Search ignores `llms.txt` for visibility and ranking.
- [Google Search Essentials](https://developers.google.com/search/docs/essentials) and
  [How Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works)
  define the crawl/index/serve baseline; compliance is eligibility, not a ranking guarantee.
- [Google structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
  supports machine-readable page understanding and rich-result eligibility; markup must match
  visible truth and does not create facts.
- [Core Web Vitals](https://web.dev/articles/vitals) provides the current user-experience
  metrics and field-measurement model; budgets must be versioned because metrics evolve.
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) is the default accessibility target.
- The KDD paper [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735)
  motivates query-based visibility experiments, citations, and evidence-rich content. Its
  findings are research results from specific systems and datasets, not a universal ranking API.
- [`llms.txt`](https://llmstxt.org/) is a community proposal for inference-time discovery.
  It is optional and consumer-specific: add or preserve it only when a declared consumer,
  experiment, or operator requirement justifies its maintenance cost.

Non-negotiable rails:

1. No keyword stuffing, doorway pages, scaled commodity content, fake freshness, fabricated
   authorship, statistics, reviews, ratings, prices, availability, credentials, or citations.
2. No schema type or property unsupported by visible content and a current consumer contract.
3. No `llms.txt`, schema depth, FAQ block, markdown mirror, or content chunking treated as a
   universal GEO requirement or direct ranking factor.
4. No competitor text is copied or lightly paraphrased. Gaps must be filled with first-party
   evidence, original analysis, clearer synthesis, or an explicit decision not to publish.
5. No route, redirect, navigation, or content deletion is applied from traffic data alone;
   backlinks, user tasks, locale, legal retention, and internal dependencies are checked first.
6. No visual simplification may hide required detail, weaken trust, break accessibility, or turn
   an informational journey into an aggressive sales funnel.
7. No causal growth claim is made from a same-session before/after test. The branch may prove
   readiness and non-regression; live impact requires the declared observation window.

# Artifact Contract

In addition to [PROTOCOL] checkpoint files and `AUDIT-ARTIFACT.md`, every run writes:

```text
_loopstate/LOOP-22/<run-id>/
  baseline-contract.md
  route-render-index-map.json
  journey-and-intent-map.json
  simplification-ledger.json
  entity-claim-evidence-register.json
  findings.json
  prioritized-mutation-dag.json
  measurement-contract.md
  post-deployment-monitoring.md
```

`simplification-ledger.json` records before, proposed, and verified-after values for routes,
navigation choices/depth, templates, component variants, dependencies, client JavaScript,
conversion steps, duplicate content clusters, and any target-specific complexity metric. `N/A`
is valid with evidence; a blank or guessed number is not.

Every finding uses:

```yaml
id: LOOP22-ISSUE-0001
category: crawl|render|technical-seo|entity|content|geo|simplification|a11y|performance|ux|measurement
severity: critical|high|medium|low
confidence: 0.00-1.00
evidence_tier: primary|first-party|research|reproducible-third-party|opinion
observation_date: YYYY-MM-DD
affected_routes: []
user_or_growth_outcome: ""
root_cause: ""
proposed_change: ""
complexity_delta: ""
tests: []
rollback: ""
approval_required: false
status: proposed|applied|verified|deferred|rejected
```

# Execution DAG (numbered nodes, [P] = parallelizable)

```text
0 Baseline and measurement contract
  -> 1 Route, crawl, render, and index truth
     -> 2 Journey, intent, and simplification model
        -> [3 Technical SEO and entity truth
            4 Content usefulness and generative retrieval
            5 UX, accessibility, performance, and reliability] [P: analysis only]
           -> 6 Prioritized mutation DAG and approval packet
              -> 7 Reversible implementation teeth
                 -> 8 Regression, adversarial, and retrieval verification
                    -> 9 Readiness verdict and monitoring handoff
```

Nodes 3-5 may inspect in parallel after node 2. Any overlapping writer paths serialize in node 7.
Use LOOP-16 only after file ownership and dependency edges prove independence. Every node runs
the [PROTOCOL] adversarial check before its checkpoint is accepted.

# Node Specs (per node: action, tools, failure conditions, output artifact)

**Node 0 - Baseline and measurement contract.**
Action: resolve remote truth, scope, priority journeys, source owners, analytics definitions,
release state, and observation window. Capture untouched build/test status plus available search,
traffic, conversion, citation, accessibility, performance, route, template, dependency, and bundle
baselines. Separate field data, lab data, model samples, and estimates. Pin query sets, locale,
device, engine, date, sample count, and model/search configuration where observable.
Tools: Git and repository metadata; existing build/test tools; read-only analytics/search sources;
browser/crawler; deterministic inventory tools.
Failure conditions: unknown target or baseline SHA; unresolved scope; priority journeys absent;
dirty overlapping worktree; metrics without definitions; production mutation requested (Permission
Failure). Missing external analytics becomes a named limitation, not a fabricated baseline.
Output artifact: `baseline-contract.md` plus node-0 checkpoint and confidence block.

**Node 1 - Route, crawl, render, and index truth.**
Action: build the canonical route inventory from routing code, CMS/content sources, sitemaps,
feeds, redirects, canonicals, alternates, robots controls, status codes, internal links, raw HTML,
rendered DOM, and accessibility tree. Exercise priority routes with JavaScript enabled/disabled,
mobile/desktop, slow network, failed third party, and supported locale/auth variants. Identify
orphans, duplicates, soft 404s, redirect chains/loops, canonical conflicts, hydration loss,
empty states, and content hidden from non-visual consumers.
Tools: code graph/LSP first for route generators and shared helpers; crawler and HTTP client;
browser automation; sitemap/robots/schema validators; server/build logs.
Failure conditions: site-wide crawler block, noindex, canonical corruption, or priority-route 5xx
= CRITICAL; crawler cannot distinguish public from private/auth routes = halt mutation and narrow
scope; client rendering cannot be reproduced = Tool Failure with explicit unknown.
Output artifact: `route-render-index-map.json` and severity-ranked findings.

**Node 2 - Journey, intent, and simplification model.**
Action: map each priority query/referral to the landing route, immediate answer, evidence, next
action, and success event. Inventory navigation choices, depth, page/template/component variants,
duplicate intent clusters, overlapping calls to action, dead ends, conversion steps, and cognitive
load. Propose keep/merge/redirect/archive/delete/split decisions but apply none here. A proposed
simplification must name what is removed, what user intent preserves it elsewhere, its dependency
edges, expected complexity delta, and rollback.
Tools: route and component graph; content inventory; browser task walkthroughs; accessibility
tree; first-party journey/search data when available; reasoning tier.
Failure conditions: a removal has no intent-preservation proof; a redirect target is not equivalent;
navigation proposal strands a priority route; simplicity is asserted only from visual taste.
Output artifact: `journey-and-intent-map.json` and initial `simplification-ledger.json`.

**Node 3 - Technical SEO and entity truth [P].**
Action: audit shared generators before individual pages: status/canonical/robots/sitemap/hreflang,
titles/descriptions, headings, semantic landmarks, breadcrumbs, media metadata, structured data,
entity identifiers, organization/product/service/person relationships, authorship, dates, pricing,
policies, and duplicate facts. Prefer one canonical source of truth and template-level repair.
Validate syntax, consumer eligibility, visible-content agreement, and contradictions across routes.
Tools: code graph; HTTP/browser; current primary platform docs; schema and rich-result validators;
deterministic contract tests.
Failure conditions: fabricated or unsupported entity property = Security/brand-integrity halt for
that patch; schema-valid but visible-content-inconsistent = HIGH; widespread canonical/robots
conflict = CRITICAL.
Output artifact: entity section of `entity-claim-evidence-register.json`, technical findings, and
contract-test plan.

**Node 4 - Content usefulness and generative retrieval [P].**
Action: score priority pages for intent satisfaction, originality, first-party experience,
evidence, source quality, authorship, limitations, freshness, readability, extractable answers,
and contradiction risk. Test the pinned baseline questions against the site corpus and authorized
live generative/search systems with repeated samples where outputs are non-deterministic. Record
answer accuracy, unsupported-claim rate, correct entity/product attribution, canonical-source
selection, citation/mention rate where observable, and variance. Propose direct answers and useful
structure for people first. Treat `llms.txt` or alternate machine-readable views as optional,
consumer-specific experiments with a maintenance owner.
Tools: content inventory; source verification; retrieval harness; authorized search/model APIs or
manual reproducible sampling; plagiarism/duplicate checks where available; reasoning tier.
Failure conditions: unsourced high-stakes claim; fake quote/statistic; paraphrased competitor copy;
single model response presented as a trend; optional machine surface contradicts canonical HTML.
Output artifact: content/claim sections of `entity-claim-evidence-register.json`, pinned GEO sample
results, and content findings.

**Node 5 - UX, accessibility, performance, and reliability [P].**
Action: replay priority journeys on mobile and desktop with keyboard, assistive semantics, slow
network/CPU, empty/error/loading states, and failed third parties. Establish current versioned Core
Web Vitals targets; use field 75th-percentile data when available and lab data for diagnosis, never
conflate them. Audit bundle/dependency cost, media, fonts, caching, layout stability, semantic
controls, labels, focus, contrast, error recovery, form preservation, analytics deduplication, and
conversion-event meaning. Reuse LOOP-02 and LOOP-06 batteries instead of weakening them.
Tools: browser automation, accessibility scanner plus scripted keyboard flows, performance tools,
bundle/dependency analyzers, visual regression, network inspection.
Failure conditions: priority journey broken; new WCAG 2.2 AA critical/serious violation; material
unapproved performance regression; conversion event fires incorrectly or more than once; error
recovery loses user input.
Output artifact: UX/a11y/performance/reliability findings and test evidence.

**Node 6 - Prioritized mutation DAG and approval packet.**
Action: deduplicate nodes 1-5 findings into root causes. Score opportunity, affected journey value,
severity, confidence, implementation cost, mutation risk, and evidence tier on documented scales.
Build a dependency-checked DAG of the smallest coherent patches. Prefer deletions and shared-source
repairs when they reduce surface area without losing intent. For each tooth, specify tests, expected
complexity delta, measurement classification (`immediate-readiness` or `post-deployment-outcome`),
rollback, and approval owner. Run LOOP-11 inline over the whole plan.
Tools: reasoning tier; code/content graphs; findings artifacts; LOOP-11 FREE-MAD.
Failure conditions: circular patch DAG; mixed unrelated mutations; growth forecast stated as fact;
high-risk patch lacks rollback or owner; reviewer REJECT returns to the evidence-owning node.
Output artifact: `prioritized-mutation-dag.json`, updated simplification ledger, and approval packet.

**Node 7 - Reversible implementation teeth.**
Action: after required approvals, apply one dependency-ordered tooth at a time on the loop branch:
modify -> targeted test -> adversarial verify -> commit or rollback. Keep application, content,
redirect, schema, analytics, and dependency changes logically isolated. Every fixed defect leaves a
permanent regression test. Run a secrets/privacy scan before commit. LOOP-18 may tune a single
numeric lever; it must not optimize several variables as one tooth.
Tools: Edit/Write; project build/test tools; browser/crawler/validators; Git; LOOP-18 when applicable.
Failure conditions: tooth changes undeclared routes or events; complexity increases outside its
budget; target test cannot reproduce the defect; claim loses evidence; verifier rejects twice ->
rollback and operator-defer under [PROTOCOL].
Output artifact: isolated commits, per-tooth evidence, updated `simplification-ledger.json`, and
LOOP-12 regression manifest.

**Node 8 - Regression, adversarial, and retrieval verification.**
Action: from a clean build, re-run route/index contracts, unit/integration/E2E tests, broken-link
checks, structured-data consistency, keyboard/accessibility flows, visual/performance budgets,
priority journeys, analytics semantics, and the pinned retrieval sample. Compare against node 0 and
report variance; never cherry-pick only favorable queries. Mutation-test high-risk canonical,
robots, sitemap, redirect, schema, and analytics helpers where practical. Run the Adversarial Check
below over the diff and evidence.
Tools: full deterministic suite; crawler/browser; authorized retrieval harness; visual diff;
mutation testing; LOOP-11 inline.
Failure conditions: new failing required test, broken priority route, critical visual/a11y regression,
schema contradiction, increased unsupported-claim rate, or material budget regression routes to the
introducing tooth; evidence cannot identify the tooth = Workflow Failure and halt.
Output artifact: verification matrix, before/after evidence, rejected/deferred tooth register.

**Node 9 - Readiness verdict and monitoring handoff.**
Action: classify `READY`, `READY-WITH-REVIEW`, `BLOCKED`, or `DEFERRED`. Assemble the standard
artifact, merge-readiness packet, measurement contract, dashboards/queries, and rollback triggers.
Immediate technical wins are reported separately from post-deployment hypotheses. Monitoring starts
only after an operator-approved merge/deploy and compares equivalent periods, queries, devices,
locales, and releases. Record seasonality, outages, campaigns, algorithm changes, and tracking drift.
Tools: reasoning tier; Git diff/commits; test artifacts; read-only monitoring integrations.
Failure conditions: outcome claim before observation window; monitoring metric lacks an owner or
baseline; rollback trigger is not actionable; merge attempted by the loop.
Output artifact: `AUDIT-ARTIFACT.md`, `measurement-contract.md`, and
`post-deployment-monitoring.md`.

# Adversarial Check (reviewer persona + what it attacks)

Persona: **skeptical search-quality engineer paired with a conversion researcher who distrusts
SEO cargo cults and redesign theater**, running FREE-MAD. They attack independently:

1. Every GEO claim: is it a current platform contract, first-party observation, bounded research
   result, or merely vendor folklore? `llms.txt`, schema, freshness, content length, citations, and
   heading patterns receive no credit without a named consumer or test.
2. Every simplification: was complexity actually removed, or merely hidden? Did a merge/delete lose
   a user intent, backlink destination, locale, policy, accessibility path, or source citation?
3. Every growth claim: could seasonality, paid campaigns, release timing, tracking changes, or query
   selection explain it? Same-session code checks may prove readiness, never durable traffic lift.
4. Every content improvement: is the evidence real, primary where possible, accurately scoped, and
   owned for refresh? Polished unsupported prose is a regression.
5. Every structured-data change: does visible content support it, and does a current consumer
   document it? Valid JSON alone is not success.
6. Every passing journey: was it tested on mobile, keyboard, constrained conditions, and failure
   states, or only on a happy-path desktop screenshot?
7. The confidence block's `unknown` and `missing_evidence` first. Silent Agreement in round 1 forces
   a second hostile round under [PROTOCOL]. Maximum two rounds; surviving material uncertainty
   becomes `READY-WITH-REVIEW` or `BLOCKED`, not optimism.

# Exit Criteria (quantitative, overrides protocol section 12)

- 100% of declared priority routes have a recorded status, canonical, indexability decision,
  render result, intent owner, and rollback path; zero unintended priority 4xx/5xx, noindex,
  robots blocks, canonical conflicts, redirect loops, or empty rendered bodies.
- 100% of sitemap, canonical, redirect, hreflang (when present), and structured-data mutations pass
  deterministic syntax/contract checks; zero fabricated properties or visible-content conflicts.
- 100% of modified material claims have a source/owner/verified date and limitation where needed;
  zero unresolved unsupported high-stakes or product-capability claims.
- Simplification ledger shows at least one verified decrease in a declared complexity metric and
  zero unexplained or unapproved increases across the rest. Every removed route/component/content
  surface has intent-preservation evidence and a tested migration or rollback path.
- All priority journeys pass desktop, mobile, keyboard, slow-network, and declared failure-state
  tests; zero new critical/serious WCAG 2.2 AA findings and zero user-input loss on recoverable forms.
- Current Core Web Vitals targets are version-pinned. No touched priority route materially regresses
  against its approved field or lab budget; field claims use the 75th percentile segmented by device.
- Required build/type/lint/test suites pass; touched-surface test pass rate >=99%; every fixed defect
  has a named regression test; high-risk shared helpers are mutation-tested where practical.
- GEO sample uses the pinned query set and records engine/date/sample count/configuration and
  variance. Unsupported-claim and entity-attribution accuracy do not regress. No citation/ranking
  lift is claimed until live post-deployment evidence satisfies the measurement contract.
- `llms.txt` is not required. If an approved consumer-specific implementation exists, it returns the
  intended status, follows its declared format, links only canonical factual sources, and has an owner.
- All CRITICAL/HIGH findings are verified resolved or explicitly operator-deferred; retries remain
  within [PROTOCOL]; final confidence >=0.85; governance row and standard artifact written.

# Failure Routing (only deviations from protocol section 4)

- Search or model behavior changes during the run -> checkpoint, date-stamp both regimes, refresh
  primary guidance, and rerun only affected measurements. Never average incompatible regimes.
- Insufficient traffic/sample volume -> mark outcome `INSUFFICIENT-DATA`; technical readiness may
  still pass, but growth/citation outcome remains unproven.
- Analytics disagreement across tools -> Measurement Failure: stop causal claims, verify event and
  attribution definitions, then resume from node 0/5 as appropriate.
- A simplification cannot preserve intent -> reject that tooth without failing unrelated repairs.
- A security/privacy defect discovered in public website or analytics handling follows [PROTOCOL]
  Security Failure and routes to LOOP-10 or the repository's security process.

# Approval Gates (only deviations from protocol section 10)

Protocol defaults apply. Explicit operator/content-owner approval is additionally required before:

- deleting, merging, archiving, or redirecting public content or a route with traffic/backlinks;
- changing primary navigation, brand positioning, product capability, price, policy, legal,
  medical, financial, or organization-level entity claims;
- adding/removing analytics events, consent behavior, third-party scripts, or attribution logic;
- broad visual redesign, CMS/framework migration, dependency change with broad runtime impact, or
  performance tradeoff outside the declared budget;
- publishing an optional AI-specific surface whose content could diverge from canonical HTML.

The loop never self-merges or deploys. A passing branch and artifact are the handoff.

# RUN PROMPT

```text
Run LOOP-22 on <repo> (scope: <public-site-dir-or-routes>, growth_goal: <goal>, priority_journeys: <list-or-file>). Read PROTOCOL.md and skills/LOOP-22-website-growth-overhaul.md, then execute the evidence-first DAG end-to-end. Baseline before mutation; simplify routes, navigation, templates, components, content, and dependencies only when intent is preserved and the complexity delta is measured. Treat GEO as a pinned retrieval experiment, not a ranking hack; do not require llms.txt unless a named consumer or operator requirement justifies it. Serialize overlapping mutations into small rollback-safe teeth, regression-test every fixed defect, and deliver the LOOP-22 artifact, simplification ledger, measurement contract, and loop branch. No merge or deploy without my approval.
```
