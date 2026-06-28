# World News RSS Verification and Intake Pipeline

Date created: 2026-06-27
Status: Draft v0.1
Scope: Public world-news awareness.

## Tool

tools/pipelines/world_news_rss_fetch.py

## Dry-run

python3 tools/pipelines/world_news_rss_fetch.py --dry-run

## Verify-only

python3 tools/pipelines/world_news_rss_fetch.py --verify-only

## Live fetch

python3 tools/pipelines/world_news_rss_fetch.py --limit 10

## Boundary

Single-source news remains preliminary. Reuters/AP are verify-first because feed access can change. BBC World RSS is the initial stable feed.
