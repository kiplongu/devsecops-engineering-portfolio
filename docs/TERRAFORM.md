# Terraform design

The reusable module applies a Kubernetes namespace security baseline:

- Pod Security Admission `restricted` enforcement, audit and warnings
- a workload service account without automatic token mounting
- namespace CPU, memory and pod quotas
- default container requests and limits
- default-deny ingress and egress
- an explicit, narrow DNS egress exception

Dev, staging and production are separate root modules with distinct state paths
and capacity. A real organization should replace the local backend with its
encrypted, locked remote backend and use workload identity rather than static
cloud credentials.

CI performs `init -backend=false` and `validate`; it cannot contact a cluster or
change infrastructure. Applying is a human-controlled operation against an
explicit kubeconfig context.
