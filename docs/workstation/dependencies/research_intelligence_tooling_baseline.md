# Research Intelligence Tooling Baseline

Status: recorded baseline

## Purpose

Prepare the SpecShift workstation for serious research, audit, data review, public-source investigation, provenance tracking, and reproducible local analysis.

## Installed/confirmed categories

- Data inspection: DuckDB, SQLite, csvkit, Miller, VisiData
- Scientific formats: HDF5, NetCDF, CFITSIO
- Geospatial: GDAL, GEOS, PROJ, Tippecanoe
- Document/media inspection: ExifTool, ImageMagick, FFmpeg, Pandoc, qpdf, Poppler
- Hashing/provenance: hashdeep, rhash
- Supply-chain/security audit: cosign, syft, grype, trivy
- Reproducibility/environment: Brewfile, direnv, mise
- Network basics: whois, dig, curl, wget

## Rules

- Prefer reproducible manifests over memory.
- Do not use global pip3 for SpecShift QA.
- Do not add random Homebrew taps without documenting purpose.
- Do not install offensive exploitation tooling as part of the default workstation.
- Keep public-source research lawful, bounded, and provenance-recorded.

## Boundary

This is workstation tooling documentation only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
