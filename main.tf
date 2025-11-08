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

# Broker EC2 Instance
resource "aws_instance" "citibike_kafka_broker" {
  ami                         = "ami-020cba7c55df1f615"
  instance_type               = "t3.large"
  subnet_id                   = "subnet-0688a24b"
  vpc_security_group_ids      = ["sg-555a955a"]
  key_name                    = "key-pair-20250320"
  private_ip                  = "172.31.17.80"
  availability_zone           = "us-east-1a"
  
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    iops                  = 3000
    delete_on_termination = true
    encrypted             = false
  }
  
  credit_specification {
    cpu_credits = "unlimited"
  }
  
  ebs_optimized        = true
  monitoring           = false
  source_dest_check    = true
  
  disable_api_termination              = false
  instance_initiated_shutdown_behavior = "stop"
  
  tags = {
    Name = "citibike-kafka-broker"
  }
}

# Producer EC2 Instance
resource "aws_instance" "citibike_kafka_producer" {
  ami                         = "ami-020cba7c55df1f615"
  instance_type               = "t3.micro"
  subnet_id                   = "subnet-0688a24b"
  vpc_security_group_ids      = ["sg-555a955a"]
  key_name                    = "key-pair-20250320"
  private_ip                  = "172.31.20.18"
  availability_zone           = "us-east-1a"
  
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    iops                  = 3000
    delete_on_termination = true
    encrypted             = false
  }
  
  credit_specification {
    cpu_credits = "unlimited"
  }
  
  ebs_optimized        = true
  monitoring           = false
  source_dest_check    = true
  
  disable_api_termination              = false
  instance_initiated_shutdown_behavior = "stop"
  
  tags = {
    Name = "citibike-kafka-producer"
  }
}

# Consumer EC2 Instance
resource "aws_instance" "citibike_kafka_consumer" {
  ami                         = "ami-020cba7c55df1f615"
  instance_type               = "t3.micro"
  subnet_id                   = "subnet-0688a24b"
  vpc_security_group_ids      = ["sg-555a955a"]
  key_name                    = "key-pair-20250320"
  private_ip                  = "172.31.20.29"
  availability_zone           = "us-east-1a"
  
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    iops                  = 3000
    delete_on_termination = true
    encrypted             = false
  }
  
  credit_specification {
    cpu_credits = "unlimited"
  }
  
  ebs_optimized        = true
  monitoring           = false
  source_dest_check    = true
  
  disable_api_termination              = false
  instance_initiated_shutdown_behavior = "stop"
  
  tags = {
    Name = "citibike-kafka-consumer"
  }
}

# add a comment to trigger terraform rerun
