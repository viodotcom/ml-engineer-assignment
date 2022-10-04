# Use Ubuntu 20.04 LTS as the base image
FROM ubuntu:20.04

# Install Ubuntu packages
RUN apt-get update --fix-missing
RUN apt-get install python3-pip wget zip unzip curl jq -y

# Instal AWS CLI and Virtualenv
RUN pip3 install awscli
RUN pip3 install virtualenv

# Install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.1.9/terraform_1.1.9_linux_amd64.zip
RUN unzip terraform_1.1.9_linux_amd64.zip -d /usr/local/bin
RUN rm terraform_1.1.9_linux_amd64.zip

# Create directories for the assignment
RUN mkdir -p /root/.aws
RUN mkdir -p /assignment/deployment
RUN mkdir -p /assignment/codes
RUN mkdir -p /assignment/data

# Copy files
COPY aws/credentials /root/.aws
COPY Makefile /assignment
COPY model_config.yml /assignment
COPY requirements.txt /assignment
COPY deployment/ /assignment/deployment
COPY codes/ /assignment/codes
COPY data/ /assignment/data

RUN pip3 install -r /assignment/requirements.txt

# Move to the assignment directory
WORKDIR /assignment

# Entry point
CMD ["/bin/sh"]
