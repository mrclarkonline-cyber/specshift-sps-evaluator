# Data Handling and Retention Policy

Status: scaffold
Date: 2026-06-28

```json
{
  "data_handling_policy": {
    "default_classifications": [
      "public",
      "public_candidate",
      "private",
      "protected",
      "archive_caution",
      "do_not_send",
      "do_not_first_send"
    ],
    "handling_rules": [
      "Classify artifacts before use.",
      "Preserve SHA-256, path, timestamp, and provenance where possible.",
      "Do not promote private/protected artifacts to public use by default.",
      "Do not include protected artifacts in first-send outreach.",
      "Use Claim Gauntlet and Promotion Gate before external-facing use.",
      "Client labels and final adjudication remain buyer-controlled.",
      "Retain only what is needed for workflow provenance unless professional advice says otherwise."
    ],
    "restricted_materials": [
      "raw client traces",
      "buyer labels",
      "protected method details",
      "source code",
      "security-sensitive materials",
      "confidential client documents",
      "contract drafts",
      "financial/payment records"
    ]
  },
  "retention_policy_scaffold": {
    "default": "Retain internal scaffold artifacts for provenance; treat client-specific/protected data as restricted and subject to client terms and professional review.",
    "deletion_or_return": "Client-specific deletion/return obligations must be set in written terms and reviewed professionally.",
    "restrict_or_minimize": [
      "client raw artifacts",
      "client labels",
      "protected implementation details",
      "contract drafts",
      "payment records",
      "security-sensitive documentation"
    ],
    "retain": [
      "workplan registrations",
      "audit reports",
      "hash/provenance records",
      "claim-boundary records",
      "professional-review packet indexes"
    ]
  }
}
```

## Boundary

This is a governance-readiness scaffold only. It is not legal advice, compliance certification, procurement approval, or a binding policy until reviewed and adopted by appropriate professionals.
