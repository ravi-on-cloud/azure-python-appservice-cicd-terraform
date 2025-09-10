variable "name_prefix" {
  description = "Prefix for plan and app names"
  type        = string
}

variable "rg_name" {
  description = "Resource group name"
  type        = string
}

variable "location" {
  description = "Azure region (e.g., australiacentral, eastus)"
  type        = string
}

variable "plan_sku" {
  description = "App Service Plan SKU (B1 or S1 for Linux)"
  type        = string
}
