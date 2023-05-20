#version: 0.1.6
# References:
#   https://www.maxivanov.io/publish-azure-functions-code-with-terraform/ (using the mode app service)
# Changelog:
#   0.1.6: added if-else in function_app_publish
resource "azurerm_storage_account" "main" {
    name                     = lower(replace(var.name, "-", ""))
    resource_group_name      = var.resource_group_name
    location                 = var.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
}


resource "azurerm_storage_container" "main" {
    name                  = "contents"
    storage_account_name  = azurerm_storage_account.main.name
    container_access_type = "private"
}

# if log_analytics_workspace == '', the resource is created
resource "azurerm_log_analytics_workspace" "main" {
  count               = var.log_analytics_workspace == "" ? 1 : 0
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "main" {
    name                = var.name
    location            = var.location
    resource_group_name = var.resource_group_name
    application_type    = var.runtime=="python" ? "web" : "Node.JS"
    workspace_id        = var.log_analytics_workspace != "" ? var.log_analytics_workspace : azurerm_log_analytics_workspace.main[0].id

    # https://github.com/terraform-providers/terraform-provider-azurerm/issues/1303
    tags = {
        "hidden-link:${var.resource_group_id}/providers/Microsoft.Web/sites/${var.name}" = "Resource"
    }
}

resource "azurerm_app_service_plan" "main" {
    count               = var.service_plan == "" ? 1 : 0
    name                = var.name
    location            = var.location
    resource_group_name = var.resource_group_name
    kind                = var.service_plan_sku == "Y1" ? "FunctionApp" : "Linux"
    reserved            = true

    sku {
        tier = var.service_plan_sku == "Y1" ? "Dynamic" : "PremiumV2"    
        size = var.service_plan_sku
    }
}

resource "azurerm_function_app" "main" {
    name                       = var.name
    location                   = var.location
    resource_group_name        = var.resource_group_name
    app_service_plan_id        = var.service_plan != "" ? var.service_plan : azurerm_app_service_plan.main[0].id
    storage_account_name       = azurerm_storage_account.main.name
    storage_account_access_key = azurerm_storage_account.main.primary_access_key
    https_only                 = true
    version                    = "~3"
    os_type                    = "linux"

    app_settings = merge({
        # TODO: set eiter APPLICATIONINSIGHTS_CONNECTION_STRING or APPINSIGHTS_INSTRUMENTATIONKEY
        "WEBSITE_RUN_FROM_PACKAGE" = "1"
        "FUNCTIONS_WORKER_PROCESS_COUNT" = "10" #this is the max value, but I'm not even sure what it does; see more here https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings#functions_worker_process_count and https://learn.microsoft.com/en-us/azure/azure-functions/python-scale-performance-reference#set-up-max-workers-within-a-language-worker-process
        "FUNCTIONS_WORKER_RUNTIME" = var.runtime
        "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.main.instrumentation_key
        "APPLICATIONINSIGHTS_CONNECTION_STRING" = "InstrumentationKey=${azurerm_application_insights.main.instrumentation_key};IngestionEndpoint=https://japaneast-0.in.applicationinsights.azure.com/"
        "PYTHON_ENABLE_DEBUG_LOGGING" = 1
    }, var.env_variables)

    site_config {
        always_on = var.always_on
        linux_fx_version= var.runtime=="python" ? "Python|3.8" : "node|14"
        ftps_state = "Disabled"
        use_32_bit_worker_process = false

        cors {
            allowed_origins = [
                "*" #TODO: this should be a parameter
            ]
        }
    }

    lifecycle {
        ignore_changes = [
            app_settings["WEBSITE_RUN_FROM_PACKAGE"],
        ]
    }

    # These two tags I saw after modifying in the Portal, then comparing the changes by terraform apply
    tags = {
        "hidden-link: /app-insights-instrumentation-key" = azurerm_application_insights.main.instrumentation_key,
        "hidden-link: /app-insights-resource-id"         = azurerm_application_insights.main.id
    }
}

# If nul, do not create the resource
resource "local_file" "function_app_publish" {
    count = var.scripts_publish_name == null ? 0 : 1
    filename = "${var.scripts_path}/${var.scripts_publish_name}.sh"
    content = <<-EOT
    #!/usr/bin/env bash
    ${var.shared_code_path=="" ? "" : "cp -r ${var.shared_code_path} ./${var.code_path}/shared/"}
    cd "${var.code_path}"

    # Deploy
    func azure functionapp publish ${var.name} ${var.runtime=="python" ? "--python" : "--javascript"}
    az functionapp restart --name ${var.name} --resource-group ${var.resource_group_name}

    ${var.shared_code_path=="" ? "" : "rm -r ./shared/"}
    EOT
}