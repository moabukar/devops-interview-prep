# DevOps Interview Prep

Interactive CLI tool for DevOps interview preparation with real-world scenario questions.

[![Build Status](https://github.com/moabukar/devops-interview-prep/workflows/CI/badge.svg)](https://github.com/moabukar/devops-interview-prep/actions)

[![Docker Pulls](https://img.shields.io/docker/pulls/moabukar/devops-interview-prep)](https://hub.docker.com/r/moabukar/devops-interview-prep)

## Features

- **200+ interview questions** across 10 DevOps topics
- **Scenario-based questions** from real interviews
- **Adaptive difficulty** tracking weak areas
- **Progress analytics** with performance insights
- **Company-specific** question tags (FAANG, startup, enterprise)
- **Mock interviews** with realistic timing

## Topics

AWS • Kubernetes • Docker • Linux • Git • Networking • Terraform • CI/CD • Security • Monitoring • Ansible • Azure

## Quick Start

```bash
# Docker (recommended)
docker run -it --rm moabukar/devops-interview-prep practice <topic> 
# e.g. docker run -it --rm moabukar/devops-interview-prep practice aws

# Local installation  
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep && pip install -e .
devops-ip practice <topic> --count <number>
# e.g. devops-ip practice aws --count 10
```

## Usage

```bash
# Practice specific topics
devops-ip practice <topic> --difficulty <easy|medium|hard> --count <number>
devops-ip weak-areas                    # Focus on struggling topics  
devops-ip review-mistakes               # Retry failed questions

# Interview simulation
devops-ip interview --count <number> --company-type <faang|startup|enterprise>
devops-ip mock-interview --duration 45min -> [Command coming soon]

# Progress tracking
devops-ip progress --export results.json -> [Command coming soon]
devops-ip analytics --topic <topic>
```

## Docker Usage

```bash
# Basic practice
docker run -it --rm moabukar/devops-interview-prep practice <topic>

# Full interview simulation
docker run -it --rm moabukar/devops-interview-prep interview --count <number>

# Export results
docker run -v $(pwd):/export -it --rm moabukar/devops-interview-prep practice <topic> --export /export/results.json
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


Interactive CLI tool for DevOps interview preparation with real-world scenario questions.

[![Build Status](https://github.com/moabukar/devops-interview-prep/workflows/CI/badge.svg)](https://github.com/moabukar/devops-interview-prep/actions)

[![Docker Pulls](https://img.shields.io/docker/pulls/moabukar/devops-interview-prep)](https://hub.docker.com/r/moabukar/devops-interview-prep)

## Features

- **200+ interview questions** across 10 DevOps topics
- **Scenario-based questions** from real interviews
- **Adaptive difficulty** tracking weak areas
- **Progress analytics** with performance insights
- **Company-specific** question tags (FAANG, startup, enterprise)
- **Mock interviews** with realistic timing

## Topics

AWS • Kubernetes • Docker • Linux • Git • Networking • Terraform • CI/CD • Security • Monitoring • Ansible • Azure

## Quick Start

```bash
# Docker (recommended)
docker run -it --rm moabukar/devops-interview-prep practice <topic> 
# e.g. docker run -it --rm moabukar/devops-interview-prep practice aws

# Local installation  
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep && pip install -e .
devops-ip practice <topic> --count <number>
# e.g. devops-ip practice aws --count 10
```

## Usage

```bash
# Practice specific topics
devops-ip practice <topic> --difficulty <easy|medium|hard> --count <number>
devops-ip weak-areas                    # Focus on struggling topics  
devops-ip review-mistakes               # Retry failed questions

# Interview simulation
devops-ip interview --count <number> --company-type <faang|startup|enterprise>
devops-ip mock-interview --duration 45min -> [Command coming soon]

# Progress tracking
devops-ip progress --export results.json -> [Command coming soon]
devops-ip analytics --topic <topic>
```

## Docker Usage

```bash
# Basic practice
docker run -it --rm moabukar/devops-interview-prep practice <topic>

# Full interview simulation
docker run -it --rm moabukar/devops-interview-prep interview --count <number>

# Export results
docker run -v $(pwd):/export -it --rm moabukar/devops-interview-prep practice <topic> --export /export/results.json
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
