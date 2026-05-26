# Drain Table-of-Tables Schema Specification

Purpose: convert crawl/save into crawl/understand/route/evidence.

This is a design specification, not a live database migration.

## Core tables

### drain_runs

Tracks each Drain execution cycle.

Columns:

- id
- run_key
- source_count
- object_count
- status: REAL, PARTIAL, BLOCKED
- score
- gaps
- evidence
- created_at

### drain_sources

Tracks each inspected source.

Columns:

- id
- run_id
- source_type: website, repo, readme, package, route, pdf, chat, bookmark, browser_tab, drive_file, vercel_deployment
- source_uri
- source_title
- content_hash
- crawled_at
- metadata

### drain_objects

Tracks extracted semantic objects.

Columns:

- id
- run_id
- source_id
- object_type: brand, product, offer, audience, claim, legal_obligation, document, table_candidate, risk, action, widget, repo, route
- object_name
- object_summary
- extraction_confidence
- raw_excerpt
- metadata
- created_at

### drain_table_candidates

Tracks tables the system identifies or proposes.

Columns:

- id
- run_id
- table_name
- table_purpose
- proposed_columns
- source_object_ids
- confidence
- status: candidate, accepted, rejected, merged
- created_at

### drain_touch_map

Maps conversation/source/object blast radius across the operating estate.

Columns:

- id
- run_id
- object_id
- touched_domain: product, brand, legal, documentation, operations, research, sales, engineering, widget, evidence, finance
- touched_table
- touched_entity
- touch_type: creates, updates, depends_on, duplicates, risks, monetises, documents, evidences
- confidence
- rationale
- created_at

### drain_changes

Tracks change detection.

Columns:

- id
- run_id
- source_id
- prior_hash
- current_hash
- change_type: new, changed, deleted, stale, duplicate, redirected, dead
- change_score
- summary
- created_at

### drain_daily_metrics

Tracks the measurement layer Troy asked for.

Columns:

- metric_date
- conversations
- sources_crawled
- repos_inspected
- routes_discovered
- files_inspected
- objects_extracted
- tables_touched
- new_tables_proposed
- changed_objects
- duplicate_objects
- dead_links
- stale_assets
- unfinished_work_recovered
- revenue_paths_found
- risks_found
- real_promotions
- partial_items
- blocked_items
- updated_at

### drain_receipts

Tracks evidence receipts for every run.

Columns:

- id
- run_id
- receipt_type
- status: REAL, PARTIAL, BLOCKED
- evidence
- gaps
- next_action
- score
- created_at

## First report view

The first Command Centre view should show:

- runs today
- sources crawled
- repos inspected
- routes discovered
- files inspected
- objects extracted
- tables touched
- new table candidates
- unfinished work recovered
- revenue paths found
- risks found
- REAL/PARTIAL/BLOCKED counts

## Required extraction types

- markdown text
- screenshots
- README content
- package metadata
- route maps
- deployment metadata
- document summaries
- legal/compliance references
- product and offer references
- audience references
- evidence and receipt references

## Reality Ledger

status: PARTIAL

result: Schema specification created for Drain/Table-of-Tables.

evidence:
- GitHub file path: drain/specs/table-of-tables-schema.md

gaps:
- not deployed to Supabase
- not connected to Command Centre
- no live extractor has written rows yet

next_action:
- create adapter spec
- create metrics spec
- create bridge work order

score: 0.74
