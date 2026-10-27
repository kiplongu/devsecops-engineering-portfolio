variable "namespace" {
  description = "Kubernetes namespace receiving the secure baseline."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", var.namespace))
    error_message = "namespace must be a valid DNS label."
  }
}

variable "environment" {
  description = "Deployment environment recorded on managed resources."
  type        = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "environment must be dev, staging, or production."
  }
}

variable "cpu_limit" {
  description = "Aggregate CPU quota for the namespace."
  type        = string
  default     = "4"
}

variable "memory_limit" {
  description = "Aggregate memory quota for the namespace."
  type        = string
  default     = "8Gi"
}

variable "pod_limit" {
  description = "Maximum number of pods in the namespace."
  type        = number
  default     = 20

  validation {
    condition     = var.pod_limit >= 1 && var.pod_limit <= 200
    error_message = "pod_limit must be between 1 and 200."
  }
}
