# 🚀 DevOps Interview Prep - Master Your Next DevOps Interview

An interactive CLI tool designed to help you ace your DevOps interviews with real-world scenario-based questions covering all essential topics.

## Features

- **Interview-focused questions**: Real scenarios you'll face in DevOps interviews
- **Comprehensive coverage**: AWS, Kubernetes, Docker, Linux, Git, Networking, Terraform, CI/CD, Security, Monitoring
- **Multiple difficulty levels**: Easy, Medium, Hard - from junior to senior level questions
- **Interview simulation mode**: Practice like you're in a real interview
- **Performance tracking**: See your strengths and areas for improvement
- **Quick practice**: Single questions for rapid learning
- **Docker support**: Run anywhere with Docker

## Perfect For

- **DevOps Engineers** preparing for interviews
- **SREs** looking to brush up on fundamentals
- **Developers** transitioning to DevOps roles
- **Students** learning DevOps concepts
- **Professionals** upskilling in cloud technologies

## Quick Start

### Option 1: Docker (Recommended - No installation required!)

```bash
# Practice AWS questions (5 questions by default)
docker run -it --rm moabukar/devops-interview-prep practice aws

# Practice Kubernetes with specific difficulty
docker run -it --rm moabukar/devops-interview-prep practice kubernetes --difficulty hard --count 10

# Full interview simulation
docker run -it --rm moabukar/devops-interview-prep interview --count 15

# See all available topics
docker run --rm moabukar/devops-interview-prep topics
```

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep

# Install in development mode
pip install -e .

# Start practicing!
devops-ip practice aws
```

### Option 3: Interactive Docker Session

```bash
# Start an interactive container for multiple commands
docker run -it --rm moabukar/devops-interview-prep bash

# Inside the container, run multiple commands:
devops-ip topics
devops-ip practice aws --interview-mode
devops-ip interview --count 10
exit
```

## 📖 Usage Examples

### Docker Commands

```bash
# Practice specific topics
docker run -it --rm moabukar/devops-interview-prep practice aws --count 5
docker run -it --rm moabukar/devops-interview-prep practice kubernetes --difficulty medium

# Quick single question
docker run -it --rm moabukar/devops-interview-prep quick terraform hard

# Full interview simulation
docker run -it --rm moabukar/devops-interview-prep interview --count 20

# Get information
docker run --rm moabukar/devops-interview-prep topics
docker run --rm moabukar/devops-interview-prep stats
```

### Local Commands (if installed locally)

```bash
# Practice AWS questions (5 questions by default)
devops-ip practice aws

# Focus on hard Kubernetes questions
devops-ip practice kubernetes --difficulty hard --count 10

# Full interview simulation mode
devops-ip practice docker --interview-mode

# Quick single question practice
devops-ip quick terraform medium
```

### Interview Simulation

```bash
# Full interview simulation with mixed topics
devops-ip interview --count 15

# Timed interview practice
devops-ip interview --count 20 --time-limit 30
```

### Information Commands

```bash
# List all available topics
devops-ip topics

# Get detailed info about a topic
devops-ip focus kubernetes

# Show question bank statistics
devops-ip stats
```

## Interview Simulation Mode

Experience real interview conditions:

```bash
$ devops-ip practice aws --interview-mode

🎯 Starting Interview Practice: AWS
🎭 Interview Simulation Mode: Answer like you're in a real interview!
📊 Questions: 5

📝 Question 1/5 | Difficulty: MEDIUM
======================================================================
🎭 Interview Scenario:
   You're deploying a web application that needs database credentials and API keys.

❓ Interview Question:
   What is the best practice for storing sensitive configuration data in AWS?

   1. Store in EC2 user data
   2. Hardcode in application
   3. Use AWS Systems Manager Parameter Store or Secrets Manager
   4. Store in S3 bucket

Your answer (1-4): 3
✅ Correct! Great job!
💡 Explanation: AWS Systems Manager Parameter Store and Secrets Manager are designed specifically for storing sensitive configuration data securely with encryption and access controls.

Ready for the next question? [Y/n]:
```

## 📊 Performance Tracking

Get detailed feedback on your interview readiness:

```bash
🎯 INTERVIEW PREP SUMMARY
======================================================================
Overall Score: 8/10 (80.0%)
Session Duration: 5m 23s

📊 Performance by Topic:
   • AWS: 3/4 (75%)
   • KUBERNETES: 2/2 (100%)
   • DOCKER: 3/4 (75%)

🎓 Interview Readiness Assessment:
🚀 Great work! You're almost ready!
```

## 📚 Available Topics

Current topics with question counts:

- **AWS**: Cloud services, security, architecture, cost optimization
- **Kubernetes**: Pods, services, deployments, troubleshooting, RBAC
- **Docker**: Containers, images, volumes, optimization, security
- **Linux**: Commands, file systems, process management, troubleshooting
- **Git**: Version control, branching, collaboration, advanced workflows
- **Networking**: Protocols, troubleshooting, load balancing, security
- **Terraform**: Infrastructure as code, state management, best practices
- **CI/CD**: GitHub Actions, pipelines, deployment strategies, testing
- **Security**: Best practices, compliance, incident response, encryption
- **Monitoring**: Observability, alerting, performance optimization, SLI/SLO

## 🐳 Docker Usage

### Quick Docker Commands

```bash
# Build the image
docker build -t devops-interview-prep .

# Run practice session
docker run -it --rm devops-interview-prep practice aws --count 3

# Interactive shell for multiple commands
docker run -it --rm devops-interview-prep bash
```

### Docker Compose

```bash
# Start the service
docker-compose up -d

# Run commands
docker-compose exec devops-ip devops-ip practice kubernetes
docker-compose exec devops-ip devops-ip interview --count 10
```

## 📁 Project Structure

```
devops-interview-prep/
├── devops_ip/
│   ├── __init__.py
│   └── cli.py                 # Main CLI application
├── questions/
│   └── interview_questions.json  # Interview question bank
├── tests/                     # Test files
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── Makefile                  # Build automation
└── README.md                 # This file
```

## 🔧 Development

### Local Development Setup

```bash
# Clone and setup
git clone https://github.com/moabukar/devops-interview-prep.git
cd devops-interview-prep

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
make dev
# or manually: pip install -e .

# Test the CLI
devops-ip --help
```

### Adding New Questions

Questions are stored in `questions/interview_questions.json`. Follow this structure:

```json
{
  "id": "aws-s3-security-001",
  "topic": "aws",
  "difficulty": "medium",
  "question": "How would you secure an S3 bucket containing sensitive customer data?",
  "options": [
    "Make the bucket public with strong passwords",
    "Use bucket policies, IAM roles, and encryption",
    "Only use ACLs for access control",
    "Store encryption keys in the bucket metadata"
  ],
  "correct_answer": 2,
  "explanation": "S3 security requires multiple layers: bucket policies for access control, IAM roles for service access, server-side encryption for data protection, and versioning with MFA delete for data integrity.",
  "scenario": "You're designing a secure architecture for storing customer PII data that must comply with GDPR requirements."
}
```

## 🎯 Interview Tips

### How to Use This Tool Effectively

1. **Start with basics**: Begin with easy questions to build confidence
2. **Focus on weak areas**: Use the `focus` command to drill down on specific topics
3. **Simulate real conditions**: Use `--interview-mode` to practice explaining your answers
4. **Review explanations**: Always read the explanations, even for correct answers
5. **Mixed practice**: Use the `interview` command for comprehensive preparation

### What Interviewers Look For

- **Problem-solving approach**: How you break down complex problems
- **Real-world experience**: Practical knowledge, not just theory
- **Best practices**: Understanding of industry standards and security
- **Troubleshooting skills**: How you diagnose and fix issues
- **Communication**: Ability to explain technical concepts clearly

## 🚀 Roadmap

- [ ] Progress tracking and analytics
- [ ] Custom question sets for specific roles
- [ ] Integration with popular learning platforms
- [ ] Mobile app companion
- [ ] Team/organization features
- [ ] AI-powered question generation
- [ ] Mock interview recordings

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add new questions**: Submit PRs with interview questions you've encountered
2. **Improve explanations**: Make explanations clearer and more comprehensive
3. **Report issues**: Found a bug? Let us know!
4. **Feature requests**: Suggest new features for interview preparation

### Contributing Questions

Please follow these guidelines:
- Questions should be based on real interview experiences
- Include detailed explanations with reasoning
- Add realistic scenarios when possible
- Ensure questions test practical knowledge, not just memorization

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- DevOps community for sharing interview experiences
- Open source projects that inspired this tool
- Contributors who help improve the question bank

---

**Ready to ace your next DevOps interview? Let's practice! 🎯**

```bash
devops-ip practice aws --interview-mode
```
