SOURCE?=outage_detector

lint: ## Linting
	@ruff --fix $(SOURCE)
	@mypy --pretty $(SOURCE)

deploy:  ## Deploy the monitor
	@TODO