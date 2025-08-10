# Get version from git tag, fallback to commit hash if no tag
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
IMAGE_NAME := moabukar/devops-interview-prep

.PHONY: help install dev test clean docker-setup docker-build-multi docker-build-local docker-test docker-run docker-push docker-pull

help:
	@echo "DevOps Interview Prep CLI - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  install          Install the package"
	@echo "  dev              Install in development mode"
	@echo "  test             Run tests"
	@echo "  clean            Clean build artifacts"
	@echo ""
	@echo "Docker (Local):"
	@echo "  docker-build-local   Build Docker image for current platform"
	@echo "  docker-run           Run Docker container"
	@echo "  docker-test          Test Docker image"
	@echo ""
	@echo "Docker (Production):"
	@echo "  docker-setup         Setup buildx for multi-platform builds"
	@echo "  docker-build-multi   Build for multiple platforms and push (auto-versioned)"
	@echo "  docker-pull          Pull from Docker Hub"
	@echo ""
	@echo "Current version: $(VERSION)"
	@echo ""
	@echo "Usage examples:"
	@echo "  make dev && devops-ip practice aws"
	@echo "  git tag v1.0.3 && make docker-build-multi  # Build with version tag"
	@echo "  docker run -it --rm $(IMAGE_NAME) practice aws"

install:
	pip install -r requirements.txt
	pip install .

dev:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m pytest tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Setup buildx for multi-platform builds
docker-setup:
	docker buildx create --name multiplatform --use || true
	docker buildx inspect --bootstrap

# Build for multiple platforms and push with automatic versioning
docker-build-multi:
	@echo "Building $(IMAGE_NAME) with version: $(VERSION)"
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t $(IMAGE_NAME):latest \
		-t $(IMAGE_NAME):$(VERSION) \
		--push .
	@echo "✅ Built and pushed:"
	@echo "   $(IMAGE_NAME):latest"
	@echo "   $(IMAGE_NAME):$(VERSION)"

# Build for local platform only
docker-build-local:
	@echo "Building $(IMAGE_NAME):$(VERSION) locally"
	docker build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

# Test the image
docker-test:
	@echo "Testing $(IMAGE_NAME):$(VERSION)"
	docker run --rm $(IMAGE_NAME):$(VERSION) --help
	docker run --rm $(IMAGE_NAME):$(VERSION) topics
	docker run --rm $(IMAGE_NAME):$(VERSION) stats

# Run interactive container
docker-run:
	docker run -it --rm $(IMAGE_NAME):$(VERSION)

docker-pull:
	docker pull $(IMAGE_NAME):latest

# Show current version
version:
	@echo "Current version: $(VERSION)"
	@echo "Image tags that will be created:"
	@echo "  $(IMAGE_NAME):latest"
	@echo "  $(IMAGE_NAME):$(VERSION)"

# Build and tag a release (use after creating git tag)
release: docker-build-multi
	@echo "🚀 Release $(VERSION) complete!"
	@echo "Users can now run:"
	@echo "  docker run -it --rm $(IMAGE_NAME):$(VERSION) practice aws"
	@echo "  docker run -it --rm $(IMAGE_NAME):latest practice aws"

# Quick development workflow
docker-dev: docker-build-local docker-test

# Production deployment
docker-prod: docker-build-multi
	@echo "✅ Multi-platform image built and pushed!"
	@echo "🚀 Users can now run: docker run -it --rm $(IMAGE_NAME) practice aws"

# Quick development setup
setup: dev
	@echo "✅ Setup complete! Try: devops-ip practice aws"

# Run a sample interview
demo:
	devops-ip practice aws --count 3 --interview-mode

# Show available topics
topics:
	devops-ip topics

# Test what files are included in Docker build context
docker-debug:
	@echo "Files that will be sent to Docker build context:"
	@echo "================================================"
	@tar -czf - . --exclude-from=.dockerignore | tar -tzf - | head -20
	@echo "..."
	@echo "================================================"
	@echo "Checking for essential files:"
	@echo -n "setup.py: "
	@if tar -czf - . --exclude-from=.dockerignore | tar -tzf - | grep -q "setup.py"; then echo "✅ INCLUDED"; else echo "❌ EXCLUDED"; fi
	@echo -n "requirements.txt: "
	@if tar -czf - . --exclude-from=.dockerignore | tar -tzf - | grep -q "requirements.txt"; then echo "✅ INCLUDED"; else echo "❌ EXCLUDED"; fi
	@echo -n "devops_ip/: "
	@if tar -czf - . --exclude-from=.dockerignore | tar -tzf - | grep -q "devops_ip/"; then echo "✅ INCLUDED"; else echo "❌ EXCLUDED"; fi
	@echo -n "questions/: "
	@if tar -czf - . --exclude-from=.dockerignore | tar -tzf - | grep -q "questions/"; then echo "✅ INCLUDED"; else echo "❌ EXCLUDED"; fi