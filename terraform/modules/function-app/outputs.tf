output "function_app_name" {
  value = azurerm_function_app.main.name
  description = "Deployed function app name"
}

output "function_app_default_hostname" {
  value = azurerm_function_app.main.default_hostname
  description = "Deployed function app hostname"
}

output "function_app_id" {
  value = azurerm_function_app.main.id
  description = "Deployed function app id"
}

output "log_analytics_workspace" {
  value = var.log_analytics_workspace != "" ? var.log_analytics_workspace : azurerm_log_analytics_workspace.main[0].id
  description = "Used LA id"
}


output "service_plan" {
  value = var.service_plan != "" ? var.service_plan : azurerm_app_service_plan.main[0].id
  description = "Used SP id"
}

