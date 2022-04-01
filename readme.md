## Docker Container Project

* This Backend Script uses a Docker Container that automates , download and process several CSV files as a result  from a Azure Data Factory flow for data uploading to a AWS S3 Bucket


## Main Considerations
* previous installation of a recent version of Python (Stable version)
* previous installation of Docker Desktop (Recent Version)
* previous installation of rabbitmq
* previous Knowlegde of Python programming and docker main configuration
* Do not alter requiremets.txt
* if you share you keys you will compromise your aws and azure accounts.


## steps for executing this script:

* in the CLI of docker write this command to process a recent image of rabbitmq: **_docker-compose up -d_**
* to Build the image of this project you need to run in CLI this command: **_docker build -t azure_aws_app ._**
* to perform a connection between the host and this docker image write this in CLI : **_docker run --rm -it --network=host azure_aws_app_**
* for test and debugging a truly recommend use Visual studio Code or Pycharm

## Configuring Enviroment variables:

* for the security of this project and better practices the .env file is not attached, you need to create your own
* I don't recommend use Enviroment variables in the Dockerfile or yaml files it's not safe
* use .gitignore for avoid not safety files in your projects


## Basic tutorial for using Rabbit and boto3:

* for the use of Rabbit as a Python Microservice I truly recommend this tutorial: https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/amazon-mq-rabbitmq-pika.html
* I share this python tutorial for the use of the boto3 library for Bucket s3 processing : https://buildmedia.readthedocs.org/media/pdf/boto3/latest/boto3.pdf

## this project also is in my gitlab repo: https://gitlab.com/rikardoroa/azure_aws_docker_container

# Enjoy!!

# Just Python it!!!





