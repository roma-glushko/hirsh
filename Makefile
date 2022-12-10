SOURCE?=hirsh

lint: ## Linting
	@ruff --fix $(SOURCE)
	@mypy --pretty $(SOURCE)

