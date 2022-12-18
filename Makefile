.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

SOURCE?=hirsh
SERVICE?=hirsh

clean: ## Clean temporary files
	@echo "🧹 Cleaning temporary files.."
	@rm -rf .mypy_cache .ruff_cache .pytest_cache
	@rm -rf dist
	@rm -rf htmlcov .coverage

lint: ## Linting
	@echo "🧹 Ruff"
	@ruff --fix $(SOURCE)
	@echo "🧽 MyPy"
	@mypy --pretty $(SOURCE)

requirements:  ## Update requirements.txt file from poetry config
	@poetry export --without-hashes > requirements.txt

service-status:  ## Check status of the hirsh service
	@systemctl --user status $(SERVICE)

service-logs: ## Checking service logs via journalctl
	@journalctl --user-unit $(SERVICE)

test: ## Run tests
	@coverage run -m pytest tests $(SOURCE)

test-cov: ## Generate test coverage
	@coverage report --show-missing
	@coverage html
	@open htmlcov/index.html