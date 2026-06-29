# JupyterLab Path Repair

Status: complete

## Issue

The plain `jupyter-lab` command is shadowed by a user-local install:

    /Users/benjaminjustinclark/.local/bin/jupyter-lab

This can make it unclear which JupyterLab is being launched.

## Repair

A safe explicit launcher was added:

    tools/bin/specshift_jupyterlab

It runs the Homebrew JupyterLab directly from:

    /opt/homebrew/opt/jupyterlab/bin/jupyter-lab

## Usage

From the repo:

    tools/bin/specshift_jupyterlab

Check version:

    tools/bin/specshift_jupyterlab --version

## Rule

Do not repair this by changing global Python packages or deleting user-local files unless there is a specific reason.

## Boundary

This is workstation path documentation only. It does not create legal advice, financial advice, binding terms, compliance certification, production validation, automated verdict, free pilot commitment, autonomous client action, truth validation, or hidden-mechanism claim.
