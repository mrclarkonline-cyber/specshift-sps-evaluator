# Human Review Policy

Status: scaffold
Date: 2026-06-28

```json
{
  "default": "Human review required for interpretation, delivery, client-facing claims, public-facing claims, and professional thresholds.",
  "non_delegable_decisions": [
    "final discrepancy interpretation",
    "client delivery approval",
    "public claim approval",
    "contract acceptance",
    "pricing/paid-pilot acceptance",
    "protected-method disclosure",
    "regulated-use approval"
  ],
  "system_outputs_are": [
    "candidate",
    "scaffold",
    "review prompt",
    "index",
    "audit record",
    "delivery structure"
  ],
  "system_outputs_are_not": [
    "findings",
    "truth determinations",
    "certifications",
    "legal conclusions",
    "financial conclusions",
    "autonomous instructions"
  ]
}
```

## Boundary

This is a governance-readiness scaffold only. It is not legal advice, compliance certification, procurement approval, or a binding policy until reviewed and adopted by appropriate professionals.
