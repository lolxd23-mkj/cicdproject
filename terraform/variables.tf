variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-southeast-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "Name of an existing EC2 key pair (must already exist in AWS)"
  type        = string
  default     = "ecommerce-ec2-key"
}

variable "my_ip_cidr" {
  description = "Your IP address in CIDR notation, e.g. 203.0.113.5/32. Find yours at https://checkip.amazonaws.com"
  type        = string
  # No default on purpose — you must set this in terraform.tfvars
}
