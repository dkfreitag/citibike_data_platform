terraform {
  backend "remote" {
    organization = "davidkfreitag"
    workspaces {
      name = "citibike-project-workspace"
    }
  }
}

variable "aws_access_key" {
  type      = string
  sensitive = true
}
