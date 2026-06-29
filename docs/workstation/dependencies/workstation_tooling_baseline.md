# Workstation Tooling Baseline

Status: recorded baseline

## Purpose

Document the durable command-line tooling baseline for SpecShift workstation work.

## Installed/confirmed categories

- JSON/YAML/search/file inspection: jq, yq, ripgrep, fd, tree
- shell quality: shellcheck, shfmt
- GNU utilities: coreutils, findutils, gnu-sed, grep, gawk
- workflow utilities: watch, entr, tmux
- data tools: sqlite, duckdb, csvkit
- document/PDF tools: pandoc, qpdf, poppler
- repo tools: gh, git-lfs
- secrets/signing readiness: age, sops, gnupg, pinentry-mac

## Python rule

Do not use global pip3 for SpecShift QA.

Use the isolated QA environment:

    source .venv_specshift_qa/bin/activate
    python -m pytest
    python tools/status/specshift_qa.py

## JupyterLab note

Homebrew JupyterLab is available at:

    /opt/homebrew/opt/jupyterlab/bin/jupyter-lab

The plain `jupyter-lab` command may be shadowed by a user-local install.

## Tap rule

Do not add random Homebrew taps unless there is a specific need and it is documented.

Microsoft/foundry is intentionally not used.

## Boundary

This is workstation tooling documentation only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim.
