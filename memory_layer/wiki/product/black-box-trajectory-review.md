# Black-Box Trajectory Review

Status: Active operational framing
Source(s): ChatGPT working sessions; SpecShift outreach conversations
Last updated: 2026-06-26
Public-safe: Yes, bounded
Private-safe: Yes
Counsel-only: No
Core-protected: Implementation details protected
Confidence: High
Contradictions: None known
Promotion status: Operational memory only

SpecShift reviews observable workflow behavior rather than model internals.

The public-safe framing:

Black-box reliability should depend less on trusting model claims and more on auditing observable behavior under real workflow pressure.

Relevant observable signals include requested objective, intermediate actions, permissions exercised, handoffs, exception states, reviewer interventions, claimed completion, and final system state.

Protected boundary: do not disclose proprietary scoring, internal diagnostic ordering, or implementation mechanics.
