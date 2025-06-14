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

variable "aws_secret_key" {
  type      = string
  sensitive = true
}

provider "aws" {  
  region = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# EC2 Instance
resource "aws_instance" "new_citibike_kafka_broker" {
  ami                         = "ami-020cba7c55df1f615"
  instance_type               = "t2.large"
  subnet_id                   = "subnet-21f4937e"
  vpc_security_group_ids      = ["sg-555a955a"]
  key_name                    = "key-pair-20250320"
  private_ip                  = "172.31.41.227"
  associate_public_ip_address = true
  availability_zone           = "us-east-1b"
  
  root_block_device {
    volume_type           = "gp2"  # General Purpose SSD
    delete_on_termination = true
  }
  
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"  # IMDSv2
    http_put_response_hop_limit = 2
    instance_metadata_tags      = "disabled"
  }
  
  source_dest_check = true
  monitoring        = false
  ebs_optimized     = false
  
  credit_specification {
    cpu_credits = "standard"
  }
  
  tags = {
    Name = "new-citibike-kafka-broker"
  }
}