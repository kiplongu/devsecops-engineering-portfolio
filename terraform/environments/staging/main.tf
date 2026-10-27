terraform {
  backend "local" { path = "state/staging.tfstate" }
}

provider "kubernetes" { config_path = var.kubeconfig_path }

module "baseline" {
  source       = "../../modules/kubernetes-baseline"
  namespace    = "portfolio-staging"
  environment  = "staging"
  cpu_limit    = "4"
  memory_limit = "8Gi"
  pod_limit    = 20
}

variable "kubeconfig_path" {
  type        = string
  description = "Path to kubeconfig; supplied at plan/apply time."
  sensitive   = true
  default     = "~/.kube/config"
}

output "namespace" { value = module.baseline.namespace }
