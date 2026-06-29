# curl Path Shadow Repair

Status: complete

## Issue

The `curl` command was shadowed by a SymCore terminal security wrapper:

    ~/WORK/tools/symcore/terminal_security/bin/curl

For SpecShift workstation reproducibility, network tooling should resolve to the standard system/Homebrew curl path unless a wrapper is intentionally documented.

## Repair

The SymCore curl shadow was quarantined under:

    ~/WORK/tools/symcore/terminal_security/QUARANTINED_PATH_SHADOWS/

The file was moved, not deleted.

## Rule

Do not allow undocumented command shadows for core network tools.

Core commands to keep clean:

- curl
- wget
- git
- python3
- pip3

## Boundary

This is workstation path hygiene documentation only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, surveillance authorization, truth validation, or hidden-mechanism claim.
