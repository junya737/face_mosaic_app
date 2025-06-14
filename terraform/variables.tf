variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
}

variable "port" {
  description = "Port number the app will use"
  type        = number
  default     = 8000
}
