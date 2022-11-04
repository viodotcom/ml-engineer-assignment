.DEFAULT_GOAL := run

# Wait for LocalSrack to be up and running
wait-for-localstack:
	@echo "Waiting for LocalStack to be up and running"
	@until curl -s http://localstack:4566/health | jq '[.services[] == "available"] | all'; do \
    	echo "LocalStack not yet available..."; \
    	sleep 20; \
	done
	@echo "Localstack available!"

# Deploy Terraform resources
run-terraform:
	@echo "Deploying Terraform resources"
	@cd deployment && terraform init && terraform apply -auto-approve

# Check AWS resouces
check-resources:
	@echo "Checking AWS buckets"
	@aws --endpoint-url=http://localstack:4566 s3api list-buckets


run: wait-for-localstack run-terraform check-resources

# TODO 1: Add rule for train
# TODO 2: Add rule for inference