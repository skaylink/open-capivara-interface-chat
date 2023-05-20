variable "name" {
  type = string
  default = "SOC-bot"
}

variable "name_simple" {
  type = string
  default = "socbot"
}



variable "tags" {
  type = map
  default = {
    "owner"   = "leonardo benitez"
    "managed" = "terraform"
  }
}

variable "function_env" {
  type = map
  sensitive = true
}

## Accounts
variable "subscription_id" {
  type = string
  nullable = false
}

variable "tenant_id" {
  type = string
  nullable = false
}
