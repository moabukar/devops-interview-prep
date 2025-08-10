# DevOps Interview Prep

Interactive CLI tool for DevOps interview preparation with real-world scenario questions.

[![Build Status](https://github.com/moabukar/devops-interview-prep/workflows/CI/badge.svg)](https://github.com/moabukar/devops-interview-prep/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/moabukar/devops-interview-prep)](https://hub.docker.com/r/moabukar/devops-interview-prep)

## Quick Start

```bash
# Docker (recommended)
docker run -it --rm moabukar/devops-interview-prep practice aws

# Local installation  
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep && pip install -e .
devops-ip practice kubernetes --count 5
```

## Features

- **200+ interview questions** across 10 DevOps topics
- **Scenario-based questions** from real interviews
- **Adaptive difficulty** tracking weak areas
- **Progress analytics** with performance insights
- **Company-specific** question tags (FAANG, startup, enterprise)
- **Mock interviews** with realistic timing

## Topics Covered

AWS • Kubernetes • Docker • Linux • Git • Networking • Terraform • CI/CD • Security • Monitoring • Ansible • Azure

## Usage

```bash
# Practice specific topics
devops-ip practice aws --difficulty medium --count 10
devops-ip weak-areas                    # Focus on struggling topics  
devops-ip review-mistakes              # Retry failed questions

# Interview simulation
devops-ip interview --count 20 --company-type faang
devops-ip mock-interview --duration 45min

# Progress tracking
devops-ip progress --export results.json
devops-ip analytics --topic kubernetes
```

## Docker Usage

```bash
# Basic practice
docker run -it --rm moabukar/devops-interview-prep practice aws

# Full interview simulation
docker run -it --rm moabukar/devops-interview-prep interview --count 15

# Export results
docker run -v $(pwd):/export -it --rm moabukar/devops-interview-prep practice aws --export /export/results.json
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new questions
- Reporting issues  
- Development setup
- Code style requirements

## Development

```bash
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep
make setup          # Install dependencies
make test           # Run tests
make docker-build   # Build Docker image
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**500+ professionals have used this tool to prepare for DevOps interviews at top tech companies.**