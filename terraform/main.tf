terraform {
  required_version = ">= 1.1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_security_group" "app" {
  name        = "mosic-app-sg"
  description = "Allow HTTP traffic"

  ingress {
    from_port   = var.port
    to_port     = var.port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.app.id]

  user_data = <<-EOF2
              #!/bin/bash
              apt-get update
              apt-get install -y python3 python3-pip git
              git clone ${var.repo_url} /opt/mosic_ai_codex

              pip3 install -r /opt/mosic_ai_codex/requirements.txt
              PORT=${var.port} nohup python3 /opt/mosic_ai_codex/app.py &
              EOF2

  tags = {
    Name = "mosic-ai-codex"
  }
}

output "instance_public_ip" {
  value = aws_instance.app.public_ip
}
