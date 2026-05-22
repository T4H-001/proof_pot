# Pipedream Value Cycles — Core, Signal, and Operating Businesses

Date: 2026-05-22
Status: PARTIAL
Intent: Identify how Pipedream/String should create value across Troy’s portfolio without becoming another stalled tool.

## Executive read
Pipedream has value if it becomes the heartbeat layer: scheduled connector access, cheap deterministic workflows, file/evidence writes, and escalation when something matters. It should not become the brain, source of truth, or authority layer.

Canonical split:
- Pipedream = trigger, connector, heartbeat, lightweight routing
- GitHub/proof_pot = evidence/file drop and experiment ledger
- Supabase = structured state and portfolio memory
- Bridge = governed execution, receipts, code pushes, SQL, recovery
- Command Centre = visibility
- OpenAI/Claude = optional reasoning steps, not default runtime

## Cycle 1 — Core businesses
Scope: Tech 4 Humanity, AI Sweet Spots, MyNeuralSignal, LifeGraph+, Reading Buddy, WorkFamilyAI, Doolittles/Synal.

Primary value:
- Keep the evidence loop alive when Troy is not present.
- Find source material in Drive/GitHub/Notion and route it into a usable index.
- Watch product evidence, research claims, landing pages, and missing receipts.
- Feed evidence into proof_pot and later Supabase.

Useful workflows:
1. Evidence Harvester
   - Trigger: daily or webhook
   - Sources: Drive, GitHub, Notion
   - Output: /evidence/YYYY-MM-DD/*.md in proof_pot
   - No model call unless classification is needed

2. Claim-to-Evidence Checker
   - Trigger: scheduled weekly
   - Sources: website pages, GitHub docs, Drive files
   - Output: claims missing evidence, claims with evidence, stale claims
   - Destination: GitHub issue or CSV

3. Signal Product Watch
   - Trigger: daily
   - Sources: Vercel, GitHub, Supabase
   - Output: product health status for MyNeuralSignal/LifeGraph+/Reading Buddy

Business value:
- Turns scattered IP into indexed product evidence.
- Reduces forgotten assets.
- Creates audit-ready proof for research/product claims.
- Moves core businesses toward REAL rather than narrative-only status.

## Cycle 2 — Next/signal businesses
Scope: Doolittles, SpeechEvent, Synal, ConsentX, Outcome Ready signal products, Reading Buddy signal chain, AI Sweet Spots.

Primary value:
- Test the communication thesis directly: goal + sources + output + destination.
- Capture what each system hears, where it drifts, and what output pattern works.
- Create repeatable agent prompt grammars for unknown tools like String.

Useful workflows:
1. Prompt Listener Test Bench
   - Trigger: manual/webhook
   - Input: human intent
   - Output: machine-native prompt with goal, sources, action, output, destination, limit
   - Destination: /listener-tests/*.md

2. Agent Drift Logger
   - Trigger: after each automation run
   - Captures: intended task, interpreted task, executed task, failure point
   - Destination: Supabase later; GitHub CSV now

3. Signal-to-Outcome Ledger
   - Trigger: scheduled/manual
   - Captures: signal, intervention, output, evidence, business outcome
   - Destination: proof_pot then Supabase

Business value:
- Converts today’s live lesson into product IP.
- Produces the Doolittles/SpeechEvent evidence base.
- Creates reusable machine communication patterns.
- Helps sell “we make systems hear correctly” as a service/product.

## Cycle 3 — Operating businesses
Scope: AI4Tradies, Outcome Ready, Enter Australia, GC-BAT, Agent Channel, AISS-style assets, website portfolio, marketing/sales loops.

Primary value:
- Keep checking websites, deployments, repos, forms, leads, and outbound assets while Troy is offline.
- Create small daily progress instead of waiting for human attention.

Useful workflows:
1. Portfolio Audit Runner
   - Trigger: daily
   - Sources: GitHub + Vercel
   - Output:
     - /audit/latest/repos-no-deployment.csv
     - /audit/latest/deployments-no-repo.csv
     - /audit/latest/abandoned-projects.csv
     - /audit/runs/YYYY-MM-DD/run-summary.md
   - Evidence from test: 215 repos, 20 Vercel deployments, 211 repos without deployments, 56 abandoned projects.

2. Website Smoke Checker
   - Trigger: daily
   - Sources: Vercel deployments / domain list
   - Checks: status code, homepage title, obvious 404, form/contact page exists
   - Output: critical fixes only

3. Marketing Queue Builder
   - Trigger: daily/weekly
   - Sources: Drive, Notion, GitHub, website audit
   - Output: 5 queued marketing actions per business
   - Destination: GitHub issue or Notion table

4. Sales Nudge Queue
   - Trigger: daily/weekly
   - Sources: LinkedIn/Sheets/CRM later
   - Output: safe outreach candidates and draft actions
   - Requires more governance before sending anything externally

Business value:
- Websites get checked.
- Dead projects get surfaced.
- Marketing tasks get generated.
- Sales preparation continues.
- Troy wakes up to progress instead of backlog.

## Three-workflow free-tier strategy
If only three active workflows are available, use them as infrastructure, not business-specific toys.

1. CHECK
   - scheduled audit/health checks
   - GitHub, Vercel, websites, later Supabase

2. STORE
   - webhook inbox that writes any useful output to GitHub/proof_pot
   - no summarisation, no model call

3. ESCALATE
   - notify only for critical blockers, high-value opportunities, or failed loops
   - Telegram/Slack/email later

Everything else should be a mode/config of these three.

## Connector priority
Now:
- GitHub
- Vercel
- Supabase
- OpenAI/Anthropic as optional reasoning steps

Soon:
- Google Drive, only as reader/indexer first
- Notion, only if still useful as dashboard/project surface
- Google Sheets for cheap working tables

Later:
- Telegram/Slack for alerts
- LinkedIn Premium for sales intelligence, not automated spam
- AWS only when Bridge/Lambda monitoring is in scope

## Guardrails
- Do not give broad write/delete authority unless the workflow needs it.
- Use GitHub as the first evidence store.
- Avoid AI calls in scheduled runs unless classification/reasoning is required.
- Bridge only when execution needs receipts, code changes, SQL, recovery, or authority.
- Every run should write a durable artifact or it did not happen.

## Next action
Create the three active workflows as CHECK, STORE, ESCALATE. Start with STORE because it gives every agent a safe landing zone. Then implement CHECK using GitHub + Vercel. ESCALATE comes last.

## Reality Ledger
status: PARTIAL
result: Pipedream value model defined across core, signal, and operating businesses.
evidence:
- String/Pipedream test retrieved 215 GitHub repos and 20 Vercel deployments.
- Test found 211 repos without deployments and 56 abandoned projects before token quota failure.
- GitHub issue #1 created in TML-4PM/proof_pot for autonomous portfolio loop.
gaps:
- No recurring workflows created yet.
- No durable CSV output from String test yet.
- No Supabase ledger binding yet.
- No Bridge receipt yet.
next_action: create CHECK/STORE/ESCALATE workflows using Pipedream free-tier slots.
elevation: Pipedream should become heartbeat infrastructure for work-while-Troy-sleeps, not another agent toy.
pressure_flags:
- AI token quota dependency
- broad OAuth scopes
- workflow slot scarcity
- risk of tool sprawl
score: 0.91
