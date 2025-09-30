install-docker.sh
```bash
#!/bin/bash
# Install Docker
sudo yum update -y
sudo yum install -y docker

# Start Docker service and enable it to run at boot
sudo systemctl start docker
sudo systemctl enable docker

# Add the ec2-user to the docker group to allow running Docker without sudo
sudo usermod -aG docker ec2-user

# Apply group changes without logging out
newgrp docker

# Confirm Docker is working for the ec2-user
docker --version
```

Dockerfile example
```Dockerfile
FROM python:3.11.6-slim-bookworm

LABEL maintainer="test@test.com"

COPY ./ ./app
WORKDIR ./app

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8443"]
```

requirements.txt
```txt
click==8.0.1
Flask==2.0.1
itsdangerous==2.0.1
Jinja2==3.0.1
MarkupSafe==2.0.1
Werkzeug==2.0.1
```

```bash
# unzip lab samples
unzip lab_codes.zip
# Install docker
cd /home/ec2-user/install_scripts/
./install_docker.sh

# Define few variables
cd /home/ec2-user/first_app/
region=${region:-us-east-1}
repo_name="my_app"
account=$(aws sts get-caller-identity --query Account --output text)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${repo_name}:latest"

# Elastic Container Repository Creation
aws ecr create-repository --repository-name "${repo_name}"
# Authenticate Docker to ECR
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${fullname}

# Build container
docker build -t ${repo_name} .
# Check images
docker images --filter reference=my_app
# Tag and push to ECR
docker tag ${repo_name} ${fullname}
docker push ${fullname}

cd /home/ec2-user/install_scripts
./push_second_app.sh
```

push_second_app.sh
```bash
#!/bin/bash
# Get the region defined (default to us-east-1 if none defined)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
region=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/placement/region 2> /dev/null)
region=${region:-us-east-1}

# Get account ID
account=$(aws sts get-caller-identity --query Account --output text)

# Create repository name
repo_name="my_second_app"
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${repo_name}:latest"

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${repo_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${repo_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
aws ecr get-login-password --region ${region}|docker login --username AWS --password-stdin ${fullname}

# Build the docker image locally with the image name and then push it to ECR
cd /home/ec2-user/second_app
docker build  -t ${repo_name} .
docker tag ${repo_name} ${fullname}
docker push ${fullname}
```


710355026123.dkr.ecr.us-east-1.amazonaws.com/my_app:latest