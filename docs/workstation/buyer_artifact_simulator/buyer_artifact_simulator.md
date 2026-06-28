# Buyer Artifact Simulator

Status: scaffold  
Date: 2026-06-28

## Purpose

Generate safe synthetic buyer artifact cases to stress-test SpecShift intake and routing before real buyer data arrives.

## Synthetic cases

- clean trace file
- final-state-only claim
- buyer-retained label file
- support context
- mixed trace + label artifact
- prohibited prompt dump
- source code / model weight request
- compliance-certification request
- messy spreadsheet-style export
- out-of-scope artifact

## Command

    python3 tools/pilot_intake/buyer_artifact_simulator.py --output-dir tests/fixtures/buyer_artifact_simulator/synthetic_artifacts

## Boundary

The simulator generates synthetic fixtures only.

It does not use real buyer data and does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdicts, free-pilot commitments, autonomous client action, truth validation, or hidden-mechanism claims.
