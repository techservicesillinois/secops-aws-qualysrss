.PHONY: deps validate_terraform validate_zip validate

deps:
	pip3 install -r requirements.in

qualys_rss.zip:
	./build-package.sh

validate_terraform:
	terraform init
	terraform validate
	terraform fmt -check -recursive

validate_zip:
	unzip qualys_rss.zip
	diff -w lambda_function.py src/lambda_function.py

validate: validate_zip validate_terraform
