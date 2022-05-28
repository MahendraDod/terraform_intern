provider "aws" {
  access_key = "AKIATK2T2WR5YFSMU4K5"
  secret_key = "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"
  region  = "ap-south-1"
}
resource "aws_instance" "myfirstEC" {
  ami           = "ami-079b5e5b3971bd10d"
  instance_type = "t2.micro"
  key_name      = "terraform_key_pair"
  security_groups = ["security_jenkins_port"]
  tags = {
    Name = "Linux Server-A"
  }
}
resource "aws_security_group" "security_jenkins_port" {
  name        = "security_jenkins_port"
  description = "security group for jenkins"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

 ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

 # outbound from jenkis server
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags= {
    Name = "security_jenkins_port"
  }
}