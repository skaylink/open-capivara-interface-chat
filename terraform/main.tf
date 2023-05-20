# Configure the Azure provider
terraform {
  required_version = ">= 0.14.9"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.98.0"
    }
  }
  backend "azurerm" {
  }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id = var.tenant_id
  features {}
}

provider "azuread" {
  tenant_id = var.tenant_id
}

resource "azurerm_resource_group" "main" {
  name     = var.name
  location = "westeurope"
  tags = var.tags
}


######################
# Function apps
# TODO: configure health check at azure monitor
######################
module "azure-function-automation" {
  source               = "./modules/function-app"
  name                 = var.name
  resource_group_name  = azurerm_resource_group.main.name
  resource_group_id    = azurerm_resource_group.main.id
  location             = azurerm_resource_group.main.location
  subscription_id      = var.subscription_id
  runtime              = "python"
  code_path            = "azure-functions"
  service_plan_sku     = "Y1"
  env_variables        = merge(var.function_env, {
  })
  scripts_publish_name = "function_app_publish"
}

/**************************************
TODO: azure bot
app type: multitenant

creation type: create new microsoft app ID

Tier: standard
**************************************/


/**************************************
TODO: language service
tier S

Custom question answering, with tier F0 cognitive search
**************************************/