# FindHotel's Machine Learning Engineer assignment

## Introduction

This assignment is part of the recruitment process of Machine Learning Engineers here at FindHotel.
The purpose is to asses the technical skills of our candidatess in a generic scenario, similar to the one they would experience at FindHotel.

> **_NOTE_**: Please, read carefully all the instructions before starting to work on your solution and feel free to contact us if you have any questions.

## Repository content

The content of this repository is organised as follows:
- Root directory including:
  - [Dockerfile](Dockerfile) used to build the `client` docker image for the assignment.
  - [docker-compose](docker-compose.yaml) file used to launch the `localstack` and `client` docker containers.
  - [Makefile](Makefile) used in the `client` docker container and that should be used to execute all the necessary steps of the assignment.
  - [zip-lambdas](zip-lambdas.sh) auxiliary script that can be used to zip the code of the AWS Lambda function(s) deployed in the `localstack` docker container. It also takes care of installing and zipping any Python requirement specified in a `requirements.txt` file stored in the same path as the Lambda function code.
- [aws](aws/) directory including a credentials file that allows connecting from the `client` docker container to the `localstack` docker container using the AWS CLI.
- [deployment](deployment/) directory including a sample Terraform script that deploys a S3 bucket and a Lambda function.
- [lambda](lambda/) directory including a `test` Python script for the sample Lambda function.

## Environment

The default configuration in this repository will create two Docker containers:
- `localstack`:
  - Uses the [localstack](https://hub.docker.com/r/localstack/localstack) Docker image
  - [LocalStack](https://docs.localstack.cloud) is a local and limited emulation of AWS, which allows deploying a subset of the AWS resources.
  - It will be used to deploy a simple data infrastructure and run the assignment tasks.
  - This container should be used as is.
- `client`
  - Uses a custom Docker image defined in the [Dockerfile](Dockerfile) and it is based on Ubuntu 20.04.
  - It is used to interact with the `localstack` container.
  - It has some tools pre-installed (Terraform, AWS CLI, Python, etc.).
  - This container and/or its components can (and should) be modified in order to complete the assignment.

The `client` container is configured in the following way:
- All the necessary tools and resources are installed and copied using the [Dockerfile](Dockerfile).
- The entry point of the container is the [Makefile](Makefile).
- The default [Makefile](Makefile) takes care of:
  - Waiting for the `localstack` container to be up and running.
  - Zipping the [lambda](lambda/) function code.
  - Deploying a `test` S3 bucket and a `test` Lambda function defined in the [main.tf](deployment/main.tf) Terraform script.
  - Checking the deployed resources using the AWS CLI.
  - Invoking the Lambda function every 60 seconds using the AWS CLI.

The sample [test](lambda/test/test.py) Lambda function creates a dummy `YYYYMMDDhhmmss.json` object in S3 every time it is invoked.

## Quick start

Follow this steps to get your environment ready for the assignment

1) Fork this repository and clone it in your computer.

2) Install [Docker](https://docs.docker.com/get-docker/).

3) Go to the root folder of the project and execute the following command to create the Docker images and run the containers:

```bash
$ cd data-engineer-assignment
$ docker-compose up
```

4) You will be working with the `client` container. Whenever you change anything, it is recommended to remove the existing container and image to ensure the latest version is used. You can do this with:

```bash
$ docker ps -a

CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS        PORTS  NAMES
e30532b91de5   data-engineer-assignment_client   "/bin/sh -c make"        29 minutes ago   Up 8 seconds         client
fc6259295a34   localstack/localstack             "docker-entrypoint.sh"   25 hours ago     Up 9 seconds   ...   localstack

$ docker stop client
$ docker rm client

$ docker image list

REPOSITORY                        TAG         IMAGE ID       CREATED          SIZE
data-engineer-assignment_client   latest      513762759561   32 minutes ago   619MB
localstack/localstack             latest      24d3ad4fc839   4 days ago       1.52GB

$ docker image rm data-engineer-assignment_client
```

5) You can open a SSH session in the `client` container with:

```bash
$ docker exec -it client /bin/bash
```

6) You can also run specific commands. For example, you can use the AWS CLI to list the files in the `test` S3 bucket:

```bash
$ docker exec client aws --endpoint-url=http://localstack:4566 s3 ls test

2022-05-03 15:17:06         31 20220503151706.json
2022-05-03 15:18:08         31 20220503151808.json
```

## Assignment

In this assignment you will be working with internal data from two data sources.

The overal purpose is to prepare a scalable end to end machine learning pipeline that our data scientist can easily plugin in and update given some training files and some inference python file.

We want you to be able to use any orchestration tool of choice (but we would favour Metaflow or step function)

The assignment is divided in 2 parts, the first one focused on end to end training to batch inference. The second part is mainly focused on how you would monitor the model relative to business and model metrics such that we have a model that keep performing since the model is going to be mission critical.

>**_NOTE_**: The environment that we provide for the assignment and the examples in it use Terraform to create the infrastructure and Python for the Lambda functions.
However, you are free to choose your own tools for this assignment.
For example, if you feel more comfortable using the AWS CLI to the create the infrastructure or you prefer to use Go in your Lambda functions, that's perfectly fine.
Just remember that, in that case, you may need to install other tools in the `client` docker container and adapt the provided scripts.

### Part 1 - Create an end to end pipeline for inference on the training script

In this first part of the assignment the objective is to go from the training code and model to inference.

```mermaid
flowchart LR
  s[Training] --> l(Model store)
  l(Model store) --> d[Inference]
  d[Inference] --> s[Training]
```
>**_NOTE:_** We are particular about this cycle in the context of batch inference.


### Part 2 - Add metrics measuring for circuit breaking the model in production environment

In this part of the assignment you will help business stakeholders and users of your model's inference to have high level of confidence in your model by providing some monitoring environment for evaluating your model and determining when there is an emergency.


### Bonus - Evaluate how to go from data scientist's training and inference code update to deploying new version of the model.

## Evaluation

We expect the solution to be self-contained, as the sample infrastructure provided.
Therefore, we will test your solution by running:

```bash
$ docker-compose up
```

> **_NOTE_**: We suggest using the Makefile to run all the necessary steps in the `client` container, like we do in the sample. However, you are free to do it any way you want, as long as everything that needs to run does so automatically when the containers are launched.

We will then use the AWS CLI in the `client` container to inspect S3 and its contents:

```bash
$ docker exec client aws --endpoint-url=http://localstack:4566 s3 ls <my_bucket>
```

We will also check all the code provided in the repository and evaluate it focusing on:
- Code quality
- Best practices
- Architectural design
- Scalability
- Testing

## References

- [LocalStack docs](https://docs.localstack.cloud/overview/)
- [Terraform docs](https://www.terraform.io/docs)
- [Terraform AWS provider docs](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [AWS CLI docs](https://docs.aws.amazon.com/cli/latest/index.html)
- [AWS Python SDK docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Open-Meteo Weather Forecast API docs](https://open-meteo.com/en/docs)
- [Latitude and Longitude finder](https://www.latlong.net/)
