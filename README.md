# DevOps Interview Prep

Interactive CLI tool for DevOps interview preparation. 150+ scenario-based questions across 12 topics, with difficulty tracking and mock interviews.

[![Build Status](https://github.com/moabukar/devops-interview-prep/workflows/CI/badge.svg)](https://github.com/moabukar/devops-interview-prep/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/moabukar/devops-interview-prep)](https://hub.docker.com/r/moabukar/devops-interview-prep)

## Quick Start

```bash
# Docker (recommended)
docker run -it --rm moabukar/devops-interview-prep practice aws

# Local
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep && pip install -e .
devops-ip practice aws --count 10
```

## Topics

| Topic | Questions | Topic | Questions |
|-------|-----------|-------|-----------|
| Kubernetes | 30 | Networking | 12 |
| AWS | 27 | Git | 11 |
| Linux | 17 | Terraform | 11 |
| Docker | 13 | CI/CD | 11 |
| Security | 5 | Monitoring | 5 |
| Ansible | 5 | Azure | 5 |

Difficulty split: 48 easy, 62 medium, 42 hard.

## Usage

```bash
# Practice by topic and difficulty
devops-ip practice <topic> --difficulty <easy|medium|hard> --count <number>

# Focus on weak areas
devops-ip weak-areas
devops-ip review-mistakes

# Mock interview
devops-ip interview --count 20 --company-type <faang|startup|enterprise>

# View progress
devops-ip analytics --topic <topic>
```

## Docker

```bash
# Practice a topic
docker run -it --rm moabukar/devops-interview-prep practice kubernetes

# Run a mock interview
docker run -it --rm moabukar/devops-interview-prep interview --count 15

# Export results
docker run -v $(pwd):/export -it --rm moabukar/devops-interview-prep practice aws --export /export/results.json
```

## Development

```bash
make setup          # Install dependencies
make test           # Run tests
make docker-build   # Build Docker image
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for adding questions, reporting issues, and development setup.

## License

MIT
