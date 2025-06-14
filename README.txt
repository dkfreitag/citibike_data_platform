Create VPC
EC2
EC2 on the VPC
Login to EC2
Install docker
Run Kafka in docker - must update ip address in docker compose


# In the current working directory
pip install kafka_python --target .

# Then, zip the file



bin/kafka-topics.sh --create --topic station-status --bootstrap-server localhost:9092
bin/kafka-console-consumer.sh --topic station-status --bootstrap-server localhost:9092




# I don't have a VPC yet from here: https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc-internet.html
# Created this VPC and more:

aws ec2 create-vpc --cidr-block "10.0.0.0/16" --instance-tenancy "default" --tag-specifications '{"resourceType":"vpc","tags":[{"key":"Name","value":"citibike-project-vpc-vpc"}]}' 
aws ec2 modify-vpc-attribute --vpc-id "preview-vpc-1234" --enable-dns-hostnames '{"value":true}' 
aws ec2 describe-vpcs --vpc-ids "preview-vpc-1234" 
aws ec2 create-vpc-endpoint --vpc-id "preview-vpc-1234" --service-name "com.amazonaws.us-east-1.s3" --tag-specifications '{"resourceType":"vpc-endpoint","tags":[{"key":"Name","value":"citibike-project-vpc-vpce-s3"}]}' 
aws ec2 create-subnet --vpc-id "preview-vpc-1234" --cidr-block "10.0.0.0/20" --availability-zone "us-east-1a" --tag-specifications '{"resourceType":"subnet","tags":[{"key":"Name","value":"citibike-project-vpc-subnet-public1-us-east-1a"}]}' 
aws ec2 create-subnet --vpc-id "preview-vpc-1234" --cidr-block "10.0.16.0/20" --availability-zone "us-east-1b" --tag-specifications '{"resourceType":"subnet","tags":[{"key":"Name","value":"citibike-project-vpc-subnet-public2-us-east-1b"}]}' 
aws ec2 create-subnet --vpc-id "preview-vpc-1234" --cidr-block "10.0.128.0/20" --availability-zone "us-east-1a" --tag-specifications '{"resourceType":"subnet","tags":[{"key":"Name","value":"citibike-project-vpc-subnet-private1-us-east-1a"}]}' 
aws ec2 create-subnet --vpc-id "preview-vpc-1234" --cidr-block "10.0.144.0/20" --availability-zone "us-east-1b" --tag-specifications '{"resourceType":"subnet","tags":[{"key":"Name","value":"citibike-project-vpc-subnet-private2-us-east-1b"}]}' 
aws ec2 create-internet-gateway --tag-specifications '{"resourceType":"internet-gateway","tags":[{"key":"Name","value":"citibike-project-vpc-igw"}]}' 
aws ec2 attach-internet-gateway --internet-gateway-id "preview-igw-1234" --vpc-id "preview-vpc-1234" 
aws ec2 create-route-table --vpc-id "preview-vpc-1234" --tag-specifications '{"resourceType":"route-table","tags":[{"key":"Name","value":"citibike-project-vpc-rtb-public"}]}' 
aws ec2 create-route --route-table-id "preview-rtb-public-0" --destination-cidr-block "0.0.0.0/0" --gateway-id "preview-igw-1234" 
aws ec2 associate-route-table --route-table-id "preview-rtb-public-0" --subnet-id "preview-subnet-public-0" 
aws ec2 associate-route-table --route-table-id "preview-rtb-public-0" --subnet-id "preview-subnet-public-1" 
aws ec2 allocate-address --domain "vpc" --tag-specifications '{"resourceType":"elastic-ip","tags":[{"key":"Name","value":"citibike-project-vpc-eip-us-east-1a"}]}' 
aws ec2 allocate-address --domain "vpc" --tag-specifications '{"resourceType":"elastic-ip","tags":[{"key":"Name","value":"citibike-project-vpc-eip-us-east-1b"}]}' 
aws ec2 create-nat-gateway --subnet-id "preview-subnet-public-0" --allocation-id "preview-eipalloc-0" --tag-specifications '{"resourceType":"natgateway","tags":[{"key":"Name","value":"citibike-project-vpc-nat-public1-us-east-1a"}]}' 
aws ec2 create-nat-gateway --subnet-id "preview-subnet-public-1" --allocation-id "preview-eipalloc-1" --tag-specifications '{"resourceType":"natgateway","tags":[{"key":"Name","value":"citibike-project-vpc-nat-public2-us-east-1b"}]}' 
aws ec2 describe-nat-gateways --nat-gateway-ids "preview-nat-0" "preview-nat-1" --filter '{"Name":"state","Values":["available"]}' 
aws ec2 create-route-table --vpc-id "preview-vpc-1234" --tag-specifications '{"resourceType":"route-table","tags":[{"key":"Name","value":"citibike-project-vpc-rtb-private1-us-east-1a"}]}' 
aws ec2 create-route --route-table-id "preview-rtb-private-1" --destination-cidr-block "0.0.0.0/0" --nat-gateway-id "preview-nat-0" 
aws ec2 associate-route-table --route-table-id "preview-rtb-private-1" --subnet-id "preview-subnet-private-2" 
aws ec2 create-route-table --vpc-id "preview-vpc-1234" --tag-specifications '{"resourceType":"route-table","tags":[{"key":"Name","value":"citibike-project-vpc-rtb-private2-us-east-1b"}]}' 
aws ec2 create-route --route-table-id "preview-rtb-private-2" --destination-cidr-block "0.0.0.0/0" --nat-gateway-id "preview-nat-1" 
aws ec2 associate-route-table --route-table-id "preview-rtb-private-2" --subnet-id "preview-subnet-private-3" 
aws ec2 describe-route-tables --route-table-ids   "preview-rtb-private-1" "preview-rtb-private-2" 
aws ec2 modify-vpc-endpoint --vpc-endpoint-id "preview-vpce-1234" --add-route-table-ids "preview-rtb-private-1" "preview-rtb-private-2" 



# Terraform:

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "citibike_project_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "citibike-project-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.citibike_project_vpc.id

  tags = {
    Name = "citibike-project-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.citibike_project_vpc.id
  cidr_block              = "10.0.0.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "citibike-project-subnet-public1-us-east-1a"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.citibike_project_vpc.id
  cidr_block              = "10.0.16.0/20"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "citibike-project-subnet-public2-us-east-1b"
  }
}

# Private Subnets
resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.citibike_project_vpc.id
  cidr_block        = "10.0.128.0/20"
  availability_zone = "us-east-1a"

  tags = {
    Name = "citibike-project-subnet-private1-us-east-1a"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.citibike_project_vpc.id
  cidr_block        = "10.0.144.0/20"
  availability_zone = "us-east-1b"

  tags = {
    Name = "citibike-project-subnet-private2-us-east-1b"
  }
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat_eip_1" {
  domain = "vpc"

  tags = {
    Name = "citibike-project-eip-1"
  }
}

resource "aws_eip" "nat_eip_2" {
  domain = "vpc"

  tags = {
    Name = "citibike-project-eip-2"
  }
}

# NAT Gateways
resource "aws_nat_gateway" "nat_gateway_1" {
  allocation_id = aws_eip.nat_eip_1.id
  subnet_id     = aws_subnet.public_subnet_1.id

  tags = {
    Name = "citibike-project-nat-1"
  }
}

resource "aws_nat_gateway" "nat_gateway_2" {
  allocation_id = aws_eip.nat_eip_2.id
  subnet_id     = aws_subnet.public_subnet_2.id

  tags = {
    Name = "citibike-project-nat-2"
  }
}

# Public Route Table
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.citibike_project_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "citibike-project-rtb-public"
  }
}

# Private Route Tables
resource "aws_route_table" "private_route_table_1" {
  vpc_id = aws_vpc.citibike_project_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_1.id
  }

  tags = {
    Name = "citibike-project-rtb-private1-us-east-1a"
  }
}

resource "aws_route_table" "private_route_table_2" {
  vpc_id = aws_vpc.citibike_project_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_2.id
  }

  tags = {
    Name = "citibike-project-rtb-private2-us-east-1b"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public_subnet_1_association" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "public_subnet_2_association" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "private_subnet_1_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table_1.id
}

resource "aws_route_table_association" "private_subnet_2_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_route_table_2.id
}

# VPC Endpoint for S3 (optional)
resource "aws_vpc_endpoint" "s3_endpoint" {
  vpc_id            = aws_vpc.citibike_project_vpc.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [
    aws_route_table.private_route_table_1.id,
    aws_route_table.private_route_table_2.id
  ]
  tags = {
    Name = "citibike-project-s3-endpoint"
  }
}






# Terraform for the EC2 that runs Kafka:

provider "aws" {
  region = "us-east-1"
}

# EC2 Instance
resource "aws_instance" "kafka_instance_citibike_project" {
  ami                         = "ami-020cba7c55df1f615"
  instance_type               = "t2.micro"
  subnet_id                   = "subnet-09a319f3609c9e057"
  vpc_security_group_ids      = ["sg-0a6efd0b4674df3f1"]
  key_name                    = "key-pair-20250320"
  private_ip                  = "10.0.3.157"
  associate_public_ip_address = true
  
  root_block_device {
    volume_type           = "gp2"  # General Purpose SSD
    delete_on_termination = true
  }
  
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
    instance_metadata_tags      = "disabled"
  }
  
  source_dest_check = true
  
  credit_specification {
    cpu_credits = "standard"
  }
  
  tags = {
    Name = "kafka-instance-citibike-project"
  }
}

# Optional: If you want to reference existing resources instead of hardcoding IDs
# Uncomment and use these data sources

# data "aws_vpc" "existing_vpc" {
#   id = "vpc-024f55db7acbe65d1"
# }

# data "aws_subnet" "existing_subnet" {
#   id = "subnet-09a319f3609c9e057"
# }

# data "aws_security_group" "default" {
#   id = "sg-0a6efd0b4674df3f1"
# }

# data "aws_ami" "existing_ami" {
#   owners = ["amazon"]
#   filter {
#     name   = "image-id"
#     values = ["ami-020cba7c55df1f615"]
#   }
# }



docker run -p 9092:9092 \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://10.0.3.157:9092 \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
  -e KAFKA_NUM_PARTITIONS=1 \
  apache/kafka:4.0.0