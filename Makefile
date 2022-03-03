PHONY: all precommit fmt lint test run docker.build docker.run

# Loads env vars from .env file with each `make` call
include .env
export

all: fmt lint test run

precommit: fmt lint test

fmt:
	black -l 79 .

lint:
	flake8

test:
	pytest tests/unit
	pytest tests/integration

run:
	python main.py --githubToken=$(GITHUB_TOKEN) \
		--owner=$(REPOSITORY_OWNER) \
		--repo=$(REPOSITORY_NAME) \
		--smtpAddress=$(SMTP_ADDRESS) \
		--smtpUser=$(SMTP_USERNAME) \
		--smtpPasswd=$(SMTP_PASSWORD) \
		--smtpPort=$(SMTP_PORT) \
		--recipient=$(RECIPIENT)

docker.build:
	docker build -t reporeport:local .

docker.run:
	docker run --rm -it --env-file=".env" reporeport:local python main.py \
		--githubToken=$(GITHUB_TOKEN) \
		--owner=$(REPOSITORY_OWNER) \
		--repo=$(REPOSITORY_NAME) \
		--smtpAddress=$(SMTP_ADDRESS) \
		--smtpUser=$(SMTP_USERNAME) \
		--smtpPasswd=$(SMTP_PASSWORD) \
		--smtpPort=$(SMTP_PORT) \
		--recipient=$(RECIPIENT)
