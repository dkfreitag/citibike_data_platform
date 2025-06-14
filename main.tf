terraform {
  backend "remote" {
    organization = "davidkfreitag"
    workspaces {
      name = "citibike-project-workspace"
    }
  }
}

# An example resource that does nothing.
resource "null_resource" "example" {
  triggers = {
    value = "A example resource that does nothing!"
  }
}
