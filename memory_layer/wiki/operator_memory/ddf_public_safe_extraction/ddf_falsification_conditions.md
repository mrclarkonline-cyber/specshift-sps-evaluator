# ∆∆F Falsification Conditions

Date: 2026-06-27  
Status: internal extraction draft  
Source group: diagnostic-core documents from the 18-document ∆∆F corpus

## Purpose

This page preserves the rule that ∆∆F / κ must remain empirically vulnerable.

A result is not useful merely because curvature appears. It becomes useful only when it survives appropriate nulls, perturbations, and negative controls.

## Core Falsifier

The diagnostic fails when a null or surrogate construction reproduces the observed curvature distribution and temporal structure within stated tolerance.

## Falsification Conditions

### 1. Scramble-control match

Failure condition:

> If a scrambled-control surrogate preserving marginal statistics matches the observed κ / ∆∆F distribution and temporal structure within tolerance, the diagnostic fails for that setting.

Interpretation:

The apparent structure may be explained by marginal statistics rather than state-conditional or temporally organized correction.

### 2. Random-walk consistency

Failure condition:

> If curvature behaves as a random walk consistent with the null across interventions, the diagnostic fails.

Interpretation:

The observed second-order variation is not distinguishable from unstructured noise under the tested perturbation design.

### 3. No separable scaling

Failure condition:

> If regulated and passive cases show no separable scaling behavior as perturbation amplitude changes, the diagnostic fails for the tested separation claim.

Interpretation:

The diagnostic did not distinguish regulated correction from passive or externally maintained dynamics.

### 4. Conditional-independence break has no effect

Failure condition:

> If breaking conditional-independence or state-action coupling constraints produces no measurable shift in curvature statistics, the operational separability claim fails.

Interpretation:

The diagnostic did not detect the specific structure it was supposed to detect.

### 5. Null divergence

Failure condition:

> If true null conditions produce systematic divergence beyond noise bounds, the diagnostic is invalid or miscalibrated.

Interpretation:

The test is too sensitive, biased, or improperly normalized.

### 6. Failure amplification

Failure condition:

> If degradation of control authority amplifies spurious signal instead of producing transparent collapse or interpretable degradation, the diagnostic is invalid or unsafe for that context.

Interpretation:

The diagnostic may confuse failure with meaningful structure.

### 7. Non-robust ordering

Failure condition:

> If qualitative ordering does not persist across reasonable perturbations of environment, observation, controller family, or noise level, the diagnostic lacks robustness.

Interpretation:

The signal may be an artifact of a narrow implementation.

### 8. Post-hoc functional selection

Failure condition:

> If the scalar functional F or observable mapping is chosen after seeing outcomes in order to maximize curvature, the diagnostic claim is not valid.

Interpretation:

The result may be curve-fitted narrative rather than pre-specified evidence.

## Required Reporting

Every serious diagnostic report should state:

- observable used
- perturbation family
- null construction
- tolerance threshold
- sample size or horizon
- summary statistic
- confidence interval or uncertainty estimate where available
- success criterion
- failure criterion
- known limitations

## Reviewer Rule

A ∆∆F result that cannot fail is not a ∆∆F diagnostic result.

It is only an interpretation.
