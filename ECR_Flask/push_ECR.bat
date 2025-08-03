@REM AWS CLI command to log in to ECR and push the Docker image
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 773245100111.dkr.ecr.ap-northeast-1.amazonaws.com
docker build -t soa/main/flask .
docker tag soa/main/flask:latest 773245100111.dkr.ecr.ap-northeast-1.amazonaws.com/soa/main/flask:latest
docker push 773245100111.dkr.ecr.ap-northeast-1.amazonaws.com/soa/main/flask:latest