terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 1) Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.location
}

# 2) App Service Plan (Linux, B1 or S1)
resource "azurerm_service_plan" "plan" {
  name                = "${var.name_prefix}-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = var.plan_sku
}

# 3) Linux Web App (Python 3.12)
resource "azurerm_linux_web_app" "app" {
  name                = "${var.name_prefix}-web"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack { python_version = "3.12" }
  }

  app_settings = {
    SCM_DO_BUILD_DURING_DEPLOYMENT = "true" # Oryx will install requirements.txt and use startup.txt if present
  }

  https_only = true
}
