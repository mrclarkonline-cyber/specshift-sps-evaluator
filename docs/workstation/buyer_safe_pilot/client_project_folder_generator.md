# Client Project Folder Generator

Status: scaffold  
Date: 2026-06-28

## Purpose

client_project_folder_generator.py creates a buyer-safe project folder for an observable-only pilot.

## Command

Run:

    python3 tools/buyer_safe_pilot/client_project_folder_generator.py "Client Name" --workflow "Workflow under review"

Dry run:

    python3 tools/buyer_safe_pilot/client_project_folder_generator.py "Client Name" --workflow "Workflow under review" --dry-run

## Created folders

- 00_admin/
- 01_intake/
- 02_buyer_exports_observable_only/
- 03_labels_buyer_controlled/
- 04_redaction_and_field_dictionary/
- 05_working_review/
- 06_candidate_discrepancy_memos/
- 07_delivery/
- 08_provenance/
- 09_archive_or_delete/
- DO_NOT_SEND/
- PROTECTED/

## Boundary

The generator creates local project scaffolds only.

It does not authorize data transfer, retention, public use, legal/compliance claims, paid pilot terms, production validation, automated verdicts, or autonomous client action.
