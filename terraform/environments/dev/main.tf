terraform {
  backend "local" { path = "state/dev.tfstate" }
}

provider "kubernetes" { config_path = var.kubeconfig_path }

module "baseline" {
  source       = "../../modules/kubernetes-baseline"
  namespace    = "portfolio-dev"
  environment  = "dev"
  cpu_limit    = "2"
  memory_limit = "4Gi"
  pod_limit    = 10
}

variable "kubeconfig_path" {
  type        = string
  description = "Path to kubeconfig; supplied at plan/apply time."
  sensitive   = true
  default     = "~/.kube/config"
}

output "namespace" { value = module.baseline.namespace }
