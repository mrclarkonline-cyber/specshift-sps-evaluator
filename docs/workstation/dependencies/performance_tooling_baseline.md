# Performance Tooling Baseline

Status: recorded baseline

## Purpose

Add safe local tools that help speed up SpecShift workstation work, measure runtime, and identify bottlenecks without changing the working QA architecture.

## Installed tools

- `uv`: fast Python package/project tooling
- `hyperfine`: benchmark terminal commands
- `parallel`: run batch jobs across CPU cores
- `ccache`: C/C++ compilation cache
- `sccache`: broader compiler cache
- `dust`: fast disk usage inspection
- `btm`: terminal system/resource monitor
- `procs`: process inspection
- `sd`: fast find/replace

## Current rule

Do not replace `.venv_specshift_qa` yet.

Use these tools first for measurement and acceleration support. The hard gate remains:

    python3 tools/status/specshift_qa.py

## Useful commands

Benchmark QA:

    hyperfine --warmup 1 --runs 3 'python3 tools/status/specshift_qa.py'

Fast disk review:

    dust -d 2 .

Process review:

    procs python

System monitor:

    btm

## Boundary

This is workstation performance tooling documentation only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
