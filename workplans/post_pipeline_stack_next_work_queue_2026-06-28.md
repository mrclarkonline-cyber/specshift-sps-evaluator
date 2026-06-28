# Post-Pipeline Stack Next Work Queue

Date created: 2026-06-27
Status: Optional hardening queue
Scope: Work after initial 18/18 pipeline stack completion

## Status

The initial workstation pipeline stack is complete.

This queue is not required to claim the initial workplan is done.

Use this queue for hardening, polish, and operational improvements.

## Next Work Queue

### 1. Add source health history

Purpose:
Track source availability across days instead of one-time status.

Deliver:

- source health history JSONL
- last_successful_fetch
- last_failure
- failure_count
- degraded/failing status

### 2. Add retention policy

Purpose:
Prevent raw report folders from growing without control.

Deliver:

- raw report retention note
- archive/compress option
- keep summaries longer than raw payloads
- never delete without explicit command

### 3. Add smoke tests

Purpose:
Make sure each pipeline dry-run works before live fetch.

Deliver:

- tests/test_pipeline_dry_runs.py
- one command to run all dry-runs
- non-network default tests

### 4. Add scheduler notes

Purpose:
Prepare cron/launchd instructions without turning on unattended collection too early.

Deliver:

- docs/workstation/scheduling_notes.md
- manual-first recommended cadence
- launchd example kept disabled by default

### 5. Add report index

Purpose:
Make generated reports easy to browse.

Deliver:

- reports/fast_relevance/INDEX.md
- latest report pointers
- daily digest links

### 6. Add source expansion backlog

Purpose:
Track future sources without rushing unstable integrations.

Candidates:

- NVD
- GitHub Advisories
- OSV
- PubMed
- Semantic Scholar
- Crossref
- Congress.gov
- FRED
- Cloudflare Radar
- NASA DONKI
- NASA EONET
- GDELT

### 7. Add outward-facing digest template

Purpose:
Create a public-safe summary format.

Boundary:

- no raw dumps
- no unsupported claims
- no buyer overclaiming
- no protected method disclosure

### 8. Add SpecShift outreach trigger review

Purpose:
Turn buyer-trigger report items into cautious draft opportunities.

Boundary:

- human review required
- no incident exploitation
- no production validation claim
- no claim that buyer has a problem

## Immediate Recommendation

Do not build all extensions at once.

Recommended next block:

Add source health history and report index.

Reason:
These improve operational control without increasing interpretive risk.
