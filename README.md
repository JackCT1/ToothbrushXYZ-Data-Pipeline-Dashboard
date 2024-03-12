![Toothbrushxyz](https://user-images.githubusercontent.com/90726430/191836934-65e122c7-f0fe-4fb2-b4c6-c3fd61853fbf.png)

# Case Study: ToothbrushXYZ

## Data Pipeline

![Architecture](https://raw.githubusercontent.com/JackCT1/ToothbrushXYZ-ETL-Pipeline/main/pipeline-architecture.png)


## Setup: Docker

### View Images

```Bash
docker images
```

### Local

_Build_

```Bash
docker build . -t {IMAGE_NAME}
```

_Run_

```Bash
docker run -d {IMAGE_NAME}
```

### AWS

_Build_

```Bash
docker build . -t {IMAGE_NAME} --platform "linux/amd64"
```

_Credentials_

```Bash
aws ecr get-login-password --region {REGION} | docker login --username AWS --password-stdin {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com
```

_Tag_

```Bash
docker tag {IMAGE_ID} {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPO}:{IMAGE_NAME}-{TAG}
```

_Push_

```Bash
docker push {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPO}:{IMAGE_NAME}-{TAG}
```

### EC2 SSH

_Copy .env_

```Bash
scp -i {PATH_TO_PEM} {PATH_TO_ENV} ec2-user@{INSTANCE_IP}:/home/ec2-user
```

_Access sudo_

```Bash
ssh -i {PATH_TO_PEM} ec2-user@{INSTANCE_IP}
sudo yum update
```

_Install docker_

```Bash
sudo yum install docker
sudo systemctl enable docker.service
sudo systemctl start docker.service
```

_Pull from AWS_

```Bash
aws ecr get-login-password --region {REGION} | sudo docker login --username AWS --password-stdin {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com

sudo docker pull {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPO}:{IMAGE_NAME}-{TAG}

screen

sudo docker run -d -p 8080:8080 --env-file ./.env {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPO}:{IMAGE_NAME}-{TAG}
```

## Dependencies

- dash
- matplotlib
- plotly
- pandas
- dash_bootstrap_components
- python-dotenv
- psycopg2-binary
- sqlalchemy
- s3fs
- scipy
