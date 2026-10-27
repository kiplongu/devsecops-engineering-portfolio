# Recruiter evidence map

Use this as a fast guided review.

| Question | Open this evidence |
|---|---|
| Can you build secure CI/CD? | `.github/workflows/security.yml` and its green run |
| Can you work across GitHub Actions and Jenkins? | `Jenkinsfile` and `docs/JENKINS.md` |
| How do you stop vulnerable releases? | `scripts/vulnerability_gate.py` and lifecycle fixtures |
| Do you understand remediation, not only scanning? | `scripts/verify_remediation.py` |
| Can you build reusable IaC? | `terraform/modules/kubernetes-baseline` and three env roots |
| How do you secure artifacts? | `.github/workflows/release.yml` and `docs/SUPPLY-CHAIN.md` |
| How do you use AI safely? | `tools/ai-triage` and its adversarial override test |
| Are the claims reproducible? | `docs/VALIDATION.md`, tests, artifacts and release evidence |

## Suggested interview summary

“I designed a fail-closed delivery reference where tests, SAST, secret scanning,
dependency policy, IaC checks and container scanning must all succeed before an
artifact can progress. Releases use immutable digests, dual-format SBOMs,
keyless Sigstore signatures and provenance. I also modelled the full
vulnerability lifecycle and constrained AI to explanation only, leaving risk
decisions with deterministic policy and a human reviewer.”
