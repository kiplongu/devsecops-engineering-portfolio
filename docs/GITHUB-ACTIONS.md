# GitHub Actions controls

The security workflow runs on pushes, pull requests and manual requests. Each
job receives only its required permission, checkout credentials are not
persisted, concurrency prevents stale runs, and high/critical policies fail the
build.

| Stage | Control | Failure behavior |
|---|---|---|
| Test | format, race tests, coverage, vet, Python policy tests | blocks |
| CodeQL | Go and Actions SAST | blocks |
| Gitleaks | full-history secret detection with redaction | blocks |
| Dependency Review | high-severity and license policy on PRs | blocks |
| Terraform | format, init without backend, validation | blocks |
| Trivy IaC | high/critical misconfiguration | blocks |
| Trivy filesystem/image | vulnerabilities, secrets and configuration | blocks |
| SBOM | SPDX and CycloneDX artifacts | missing output blocks |

The release workflow has a separate privilege boundary and runs only for a
semantic version tag. Branch protection should require the **Fail-closed release
gate** status before merge.
