from setuptools import setup, find_packages

# Handle README gracefully for Docker builds
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Interactive DevOps Interview Preparation CLI Tool"

try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = ["click>=8.0.0", "colorama>=0.4.4"]

setup(
    name="mockops",
    version="1.2.0",
    author="DevOps Interview Prep",
    author_email="hello@devopsip.io",
    description="Interactive DevOps Interview Preparation CLI Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moabukar/devops-interview-prep",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mockops=devops_interview_prep.cli:cli",
            "devops-ip=devops_interview_prep.cli:cli",
        ],
    },
    keywords="devops, interview, preparation, cli, aws, kubernetes, docker, terraform, cicd",
)