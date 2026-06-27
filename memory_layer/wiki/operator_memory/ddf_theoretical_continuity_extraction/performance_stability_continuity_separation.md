# Performance, Stability, and Continuity Separation

Date: 2026-06-27  
Status: internal extraction draft  
Source group: continuity / ownership / separability documents from the 18-document ∆∆F corpus

## Purpose

This page preserves the separation principle:

> Success is not the same as stability, and stability is not the same as continuity.

## Three-Layer Separation

| Layer | Question | Measures | Can fail when |
|---|---|---|---|
| Performance | Did it succeed? | reward, loss, completion, accuracy, final state | success is replayed, forced, or environmentally easy |
| Stability | Did the visible signal remain smooth or bounded? | variance, drift, boundedness, low error | smoothness is externally imposed or passively maintained |
| Continuity | Did structured correction persist under perturbation? | ∆∆F / κ, recurrence, null separation, perturbation response | correction is scrambled, replayed, forced, or decoupled from state |

## Separation Claim

A system can have:

- high performance
- smooth visible behavior
- low first-order error

and still fail a continuity test if its correction process is no longer internally organized or state-contingent.

## Example Pattern

A replayed trajectory can preserve visible success.

A frozen policy can preserve output under familiar conditions.

A forced controller can preserve smoothness.

But none of those alone establishes owned continuity.

## Diagnostic Implication

A continuity-oriented diagnostic should ask:

1. What observable trajectory is being measured?
2. What first-order performance is preserved?
3. What perturbation is applied?
4. What null or surrogate is used?
5. Does second-order structure separate from the null?
6. Does the structure degrade transparently when control authority is removed?
7. What would falsify the continuity interpretation?

## Safe Sentence

> Continuity is treated as an empirically vulnerable property of correction structure, not a metaphysical assumption.

## Unsafe Sentence

> Continuity proves the system has a self.

## SpecShift Translation

In buyer-facing terms:

> A workflow can end in an acceptable final state while still containing observable trajectory discrepancies that deserve review.

That is enough.

Do not claim the workflow “lost continuity” in buyer materials unless the term is defined, bounded, and tied to a specific review protocol.
