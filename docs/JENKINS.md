# Jenkins reference implementation

The [Jenkinsfile](../Jenkinsfile) demonstrates the same policy on a traditional
self-hosted delivery platform. It is an original reference implementation—not
an export of any private or production Jenkins pipeline.

## Expected agent tools

`go`, `python3`, `docker`, `gitleaks`, `terraform`, `trivy`, `syft`, and
optionally `cosign`. Recommended Jenkins plugins are Pipeline, Git,
Credentials Binding, Timestamper and JUnit.

The default build never pushes an image. A registry release is allowed only for
a Git tag, a configured `RELEASE_REGISTRY`, and the Jenkins credential
`portfolio-registry`. Console tracing is disabled while the credential is used.

Jenkins controller/plugin compatibility cannot be proven without a real
controller and plugin catalog. Shell commands and policy scripts are shared with
the locally validated and GitHub-hosted implementation.
