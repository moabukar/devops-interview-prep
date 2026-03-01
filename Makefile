# DevOps Interview Prep - Balanced Development Makefile
.DEFAULT_GOAL := help

# Configuration
PYTHON := python3
PIP := pip
PACKAGE_NAME := devops_interview_prep
SRC_DIR := src/devops_interview_prep
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
IMAGE_NAME := moabukar/mockops

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

.PHONY: help setup install clean test lint docker

help: ## Show this help message
	@echo "$(BLUE)DevOps Interview Prep - Development Commands$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-25s$(RESET) %s\n", $$1, $$2}'

## ========================================
## 🐍 Python Development
## ========================================

install: ## Install package in production mode
	$(PIP) install .

install-dev: ## Install package in development mode with all dependencies
	$(PIP) install -e ".[dev,test]"

install-tools: ## Install development tools globally
	$(PIP) install black isort flake8 mypy pytest pre-commit build twine

setup: clean install-dev install-pre-commit ## Complete development setup
	@echo "$(GREEN)✓ Development environment ready!$(RESET)"
	@echo "Try: $(BLUE)make test$(RESET) or $(BLUE)mockops practice aws$(RESET)"

install-pre-commit: ## Install pre-commit hooks
	pre-commit install --install-hooks

env-info: ## Show development environment info
	@echo "$(BLUE)Development Environment$(RESET)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo "Package: $(PACKAGE_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Source: $(SRC_DIR)"

## ========================================
## 🧪 Testing & Quality
## ========================================

test: ## Run all tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=$(PACKAGE_NAME) --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without slow tests
	pytest tests/ -v -m "not slow"

test-unit: ## Run only unit tests
	pytest tests/unit/ -v

test-integration: ## Run integration tests
	pytest tests/integration/ -v

validate-questions: ## Validate question JSON format
	$(PYTHON) scripts/validate_questions.py

## ========================================
## 🔍 Code Quality & Linting
## ========================================

lint: ## Run all linters
	@echo "$(BLUE)Running flake8...$(RESET)"
	flake8 $(SRC_DIR) tests
	@echo "$(BLUE)Running mypy...$(RESET)"
	mypy $(SRC_DIR)

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(RESET)"
	black $(SRC_DIR) tests
	isort $(SRC_DIR) tests

format-check: ## Check code formatting without modifying
	black --check $(SRC_DIR) tests
	isort --check-only $(SRC_DIR) tests

type-check: ## Run type checking with mypy
	mypy $(SRC_DIR)

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

check: format-check lint test ## Run all checks (format + lint + test)

## ========================================
## 🐳 Docker Development
## ========================================

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(RESET)"
	docker build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

docker-build-prod: ## Build production Docker image
	docker build -f Dockerfile.production -t $(IMAGE_NAME):prod .

docker-test: ## Test Docker image functionality
	@echo "$(BLUE)Testing Docker image...$(RESET)"
	docker run --rm $(IMAGE_NAME):latest --help
	docker run --rm $(IMAGE_NAME):latest topics
	docker run --rm $(IMAGE_NAME):latest stats

docker-run: ## Run Docker container interactively
	docker run -it --rm \
		-v mockops-data:/home/devops-interviewer/.mockops \
		$(IMAGE_NAME):latest

docker-practice: ## Run practice session in Docker
	docker run -it --rm \
		-v mockops-data:/home/devops-interviewer/.mockops \
		$(IMAGE_NAME):latest practice aws -c 3

docker-shell: ## Get shell access to container
	docker run -it --rm \
		-v mockops-data:/home/devops-interviewer/.mockops \
		$(IMAGE_NAME):latest bash

## ========================================
## 🏗️ Multi-Platform Docker
## ========================================

docker-setup-buildx: ## Setup Docker Buildx for multi-platform
	docker buildx create --name multiplatform --driver docker-container --use 2>/dev/null || true
	docker buildx inspect --bootstrap

docker-build-multi: ## Build multi-platform image
	@echo "$(BLUE)Building multi-platform Docker image...$(RESET)"
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t $(IMAGE_NAME):$(VERSION) \
		-t $(IMAGE_NAME):latest \
		--push .

docker-test-platforms: ## Test Docker image on different platforms
	@echo "$(BLUE)Testing AMD64...$(RESET)"
	docker run --platform linux/amd64 --rm $(IMAGE_NAME):latest --help
	@echo "$(BLUE)Testing ARM64...$(RESET)"
	docker run --platform linux/arm64 --rm $(IMAGE_NAME):latest --help

docker-info: ## Show Docker platform information
	@echo "$(BLUE)Docker Info:$(RESET)"
	@echo "Current platform: $(shell docker version --format '{{.Client.Os}}/{{.Client.Arch}}')"
	@docker buildx ls 2>/dev/null || echo "Run 'make docker-setup-buildx' for multi-platform"

## ========================================
## 📦 Package Management
## ========================================

build: clean ## Build package for distribution
	$(PYTHON) -m build

publish-test: build ## Publish to TestPyPI
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI
	$(PYTHON) -m twine upload dist/*

version: ## Show current version
	@echo "Version: $(VERSION)"

## ========================================
## 🧹 Cleanup & Maintenance
## ========================================

clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .tox/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

clean-docker: ## Clean Docker images and containers
	@echo "$(BLUE)Cleaning Docker resources...$(RESET)"
	docker-compose down -v 2>/dev/null || true
	docker system prune -f
	docker rmi $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):prod 2>/dev/null || true

clean-all: clean clean-docker ## Clean everything

## ========================================
## 🔄 Development Workflows
## ========================================

dev: install-dev ## Quick development setup
	@echo "$(GREEN)✓ Development mode ready$(RESET)"

dev-test: install-dev test ## Install and run tests
	@echo "$(GREEN)✓ Development setup and tests completed$(RESET)"

ci: format-check lint test validate-questions ## Run CI pipeline locally
	@echo "$(GREEN)✓ All CI checks passed$(RESET)"

ci-docker: docker-build docker-test ## CI pipeline with Docker
	@echo "$(GREEN)✓ Docker CI checks passed$(RESET)"

release-check: clean check validate-questions docker-build docker-test ## Pre-release validation
	@echo "$(GREEN)✓ Release validation completed$(RESET)"
	@echo "Next steps:"
	@echo "  1. Update version in pyproject.toml"
	@echo "  2. git tag v<version>"
	@echo "  3. git push origin v<version>"

## ========================================
## 🎯 Quick Actions
## ========================================

demo: ## Run a quick demo
	@echo "$(BLUE)Running demo...$(RESET)"
	mockops topics || echo "$(YELLOW)Run 'make install-dev' first$(RESET)"

demo-docker: ## Run demo in Docker
	docker run --rm $(IMAGE_NAME):latest topics

status: ## Show project status
	@echo "$(BLUE)Project Status$(RESET)"
	@echo "Git branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repo')"
	@echo "Git status: $(shell git status --porcelain | wc -l | tr -d ' ') files changed"
	@echo "Version: $(VERSION)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Questions: $(shell mockops stats 2>/dev/null | grep "Total questions" | cut -d: -f2 || echo "Unknown")"

debug: ## Debug common issues
	@echo "$(BLUE)Debugging...$(RESET)"
	@echo "1. Testing imports:"
	@$(PYTHON) -c "from $(PACKAGE_NAME).models.question import Question; print('✓ Models OK')" 2>/dev/null || echo "❌ Models import failed"
	@$(PYTHON) -c "from $(PACKAGE_NAME).core.question_bank import question_bank; print('✓ Question bank OK')" 2>/dev/null || echo "❌ Question bank import failed"
	@$(PYTHON) -c "from $(PACKAGE_NAME).cli import cli; print('✓ CLI OK')" 2>/dev/null || echo "❌ CLI import failed"
	@echo "2. Testing CLI:"
	@mockops --help >/dev/null 2>&1 && echo "✓ CLI command works" || echo "❌ CLI command failed"

## ========================================
## 📊 Utilities
## ========================================

question-stats: ## Show question bank statistics
	mockops stats

logs: ## Show recent git logs
	git log --oneline -10

branches: ## Show git branches
	git branch -a

## ========================================
## ⚡ Quick Commands (Most Used)
## ========================================

quick-test: dev test ## Quick development test cycle
	@echo "$(GREEN)✓ Quick test completed$(RESET)"

quick-docker: docker-build docker-test ## Quick Docker test cycle
	@echo "$(GREEN)✓ Quick Docker test completed$(RESET)"

quick-check: format lint ## Quick code quality check
	@echo "$(GREEN)✓ Quick quality check completed$(RESET)"

all: clean setup check docker-build docker-test ## Do everything
	@echo "$(GREEN)✓ Complete build and test cycle completed$(RESET)"