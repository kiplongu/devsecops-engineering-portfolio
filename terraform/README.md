# Terraform Kubernetes baseline

This module creates a namespace with Pod Security Admission labels, a tokenless
service account, quotas, default resource limits, default-deny networking and an
explicit DNS exception. The `dev`, `staging`, and `production` roots keep state
and inputs isolated. The local backend is deliberate for this no-cost reference;
a real team should replace it with an encrypted, locked remote backend.

Validation requires no cluster:

```bash
terraform -chdir=environments/dev init -backend=false
terraform -chdir=environments/dev validate
```

Applying is intentionally not automated because it requires an explicitly
selected Kubernetes context:

```bash
terraform -chdir=environments/dev plan -out=plan.tfplan
terraform -chdir=environments/dev apply plan.tfplan
```
