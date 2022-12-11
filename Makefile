SOURCE?=hirsh
SERVICE?=hirsh

lint: ## Linting
	@ruff --fix $(SOURCE)
	@mypy --pretty $(SOURCE)

requirements:  ## Update requirements.txt file from poetry config
	@poetry export --without-hashes > requirements.txt

service-status:  ## Check status of the hirsh service
	@systemctl --user status $(SERVICE)

service-logs: ## Checking service logs via journalctl
	@journalctl --user-unit $(SERVICE)