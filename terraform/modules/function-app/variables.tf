variable "name" {
  type = string
}


variable "log_analytics_workspace" {
  type = string
  default = "" # if empty string, the resource will be created
}


############
## You can either specify the service plan, OR use an existing one
variable "service_plan" {
  type = string
  default = "" # if empty string, the resource will be created
}

variable "service_plan_sku" {
  type = string
  default = "Y1" #Enum["Y1", "P1v2"]
}

variable "always_on" { 
  # shoud be false if service_plan_sku=="Y1"
  # I've seen weird behavior when always_on==false and service_plan_sku=="P1v2"
  type = bool
  default = false
}

##########

variable "resource_group_name" {
  type = string
}

variable "subscription_id" {
  type = string
}

variable "resource_group_id" {
  type = string
}

variable "location" {
  type = string
}

variable "runtime" {
    type = string #Enum[python, node]
}

variable "code_path" {
    type = string
}

variable "shared_code_path" {
    type = string
    default = "" #if empty, nothing will be done
}

variable "scripts_path" {
    type = string
    default = "../scripts"
}

variable "scripts_publish_name" {
    type = string
    default = "function_app_publish"
}

variable "env_variables" {
    type = map
    default = {}
}