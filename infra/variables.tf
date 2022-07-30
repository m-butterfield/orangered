variable "default_region" {
  type = string
}

variable "project" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_host" {
  type      = string
  sensitive = true
}

variable "recaptcha_site_key" {
  type      = string
  sensitive = true
}

variable "recaptcha_secret_key" {
  type      = string
  sensitive = true
}
