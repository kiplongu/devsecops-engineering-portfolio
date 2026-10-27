output "namespace" {
  description = "Managed namespace name."
  value       = kubernetes_namespace_v1.this.metadata[0].name
}

output "workload_service_account" {
  description = "Tokenless default service account for workloads."
  value       = kubernetes_service_account_v1.workload.metadata[0].name
}
