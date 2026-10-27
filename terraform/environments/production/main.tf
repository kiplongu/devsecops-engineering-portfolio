terraform {
  backend "local" { path = "state/production.tfstate" }
}

provider "kubernetes" { config_path = var.kubeconfig_path }

module "baseline" {
  source       = "../../modules/kubernetes-baseline"
  namespace    = "portfolio-production"
  environment  = "production"
  cpu_limit    = "8"
  memory_limit = "16Gi"
  pod_limit    = 40
}

variable "kubeconfig_path" {
  type        = string
  description = "Path to kubeconfig; supplied at plan/apply time."
  sensitive   = true
  default     = "~/.kube/config"
}

output "namespace" { value = module.baseline.namespace }
