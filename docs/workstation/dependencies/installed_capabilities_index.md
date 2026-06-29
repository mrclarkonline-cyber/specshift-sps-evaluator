# Installed Capabilities Index

Status: current workstation capability index

## Purpose

Summarize what the SpecShift workstation can now do after the dependency, security, research-intelligence, QA, and systems-survey upgrades.

## Core command-line inspection

Installed/available tools include:

- `jq`: JSON inspection
- `yq`: YAML inspection
- `rg`: fast text search
- `fd`: fast file search
- `tree`: folder maps
- `coreutils`, `findutils`, `gnu-sed`, `grep`, `gawk`: GNU-compatible shell utilities

## QA and regression

SpecShift now has a working regression layer:

- `python3 tools/status/specshift_qa.py`
- `tools/bin/specshift_qa`
- `.venv_specshift_qa`
- `pytest`
- `ruff`
- `mypy`
- `pre-commit`

Current known QA state:

- pytest collects real tests
- pytest passes 13 tests
- `specshift_qa` runs 6 checks
- claim logic, audit gate, delivery packet generator, and evidence ledger smoke checks are covered

## Claim and boundary safety

Installed/available project tools include:

- `tools/claim_logic/claim_logic_classifier.py`
- `tools/claim_logic/claim_logic_audit_gate.py`

The classifier distinguishes:

- safe denial
- safe boundary language
- unsafe assertions
- unsafe certification
- unsafe verdicts
- unsafe hidden-mechanism claims
- ambiguous review language

## Buyer pilot scaffolding

Installed/available project tools include:

- buyer artifact simulator
- pilot readiness score
- red-team intake tester
- folder policy checker
- evidence ledger
- delivery packet generator
- systems survey audit

## Data and research

Installed/available tools include:

- `sqlite3`: local SQL database work
- `duckdb`: local analytical SQL and file querying
- `csvkit`: CSV inspection and conversion
- `mlr`: Miller command-line data processing
- `visidata`: terminal data exploration
- `hdf5`, `netcdf`, `cfitsio`: scientific data format support

## Geospatial and mapping

Installed/available tools include:

- `gdal`
- `geos`
- `proj`
- `tippecanoe`

These support geospatial inspection, conversion, projection, and vector-tile workflows.

## Document, PDF, image, and media inspection

Installed/available tools include:

- `pandoc`: document conversion
- `qpdf`: PDF inspection/repair
- `poppler` / `pdftotext`: PDF text extraction
- `exiftool`: metadata inspection
- `imagemagick` / `magick`: image conversion/inspection
- `ffmpeg`: media inspection/conversion

## Provenance, hashing, and supply-chain/security audit

Installed/available tools include:

- `hashdeep`
- `rhash`
- `cosign`
- `syft`
- `grype`
- `trivy`
- `gitleaks`
- `trufflehog`
- `lynis`
- `osquery`
- `fswatch`

## Security monitoring and local posture

Installed/available SpecShift commands include:

- `python3 tools/status/specshift_security_doctor.py`
- `python3 tools/status/specshift_path_watch.py`
- `python3 tools/status/specshift_security_scan.py`
- `python3 tools/status/specshift_systems_survey.py`

These check:

- FileVault
- firewall
- Gatekeeper
- SIP
- Homebrew taps
- PATH shadows
- Git state
- SSH key permissions
- secret scan posture
- QA status
- systems integration status

## Network and repo basics

Installed/available tools include:

- `curl`
- `wget`
- `whois`
- `dig`
- `gh`
- `git-lfs`

Important path hygiene note:

- `curl` shadow was quarantined.
- Microsoft/foundry tap was removed.
- `python3` and `pip3` shadows remain known review items.
- SpecShift QA should use `.venv_specshift_qa`, not global `pip3`.

## JupyterLab

Use the safe launcher:

    tools/bin/specshift_jupyterlab

This directly uses Homebrew JupyterLab and avoids the shadowed user-local `jupyter-lab`.

## Reproducibility records

Current installed state is recorded in:

- `memory_layer/wiki/operator_memory/workstation_dependencies/Brewfile`
- `memory_layer/wiki/operator_memory/workstation_dependencies/brew_installed_versions.txt`
- `memory_layer/wiki/operator_memory/workstation_dependencies/brew_taps.txt`
- `memory_layer/wiki/operator_memory/workstation_dependencies/active_python_pip_version.txt`
- `memory_layer/wiki/operator_memory/workstation_dependencies/active_python_pip_check.txt`

## Rules

- Do not use global `pip3` for SpecShift QA.
- Use `.venv_specshift_qa`.
- Do not add random Homebrew taps.
- Do not install offensive tooling as a default workstation baseline.
- Record all future installs in the wiki.
- Run `specshift_qa`, `specshift_security_doctor`, and `specshift_systems_survey` after meaningful changes.

## Boundary

This is workstation capability documentation only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
