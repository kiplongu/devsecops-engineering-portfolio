# Software supply-chain security

Release evidence is attached to an immutable image digest rather than a mutable
tag. The tag workflow performs these operations in order:

1. build and push one image;
2. capture its registry digest;
3. scan that digest with the release vulnerability policy;
4. create SPDX and CycloneDX SBOMs;
5. keyless-sign the digest with Cosign and GitHub OIDC;
6. verify the certificate identity and issuer immediately;
7. attach a CycloneDX attestation and GitHub build provenance;
8. publish the verified release and evidence.

Example consumer verification:

```bash
cosign verify \
  --certificate-identity-regexp='^https://github.com/kiplongu/devsecops-engineering-portfolio/.github/workflows/release.yml@refs/tags/v.*$' \
  --certificate-oidc-issuer='https://token.actions.githubusercontent.com' \
  ghcr.io/kiplongu/devsecops-engineering-portfolio@sha256:REPLACE_ME
```

No long-lived signing key is stored in GitHub Secrets.
