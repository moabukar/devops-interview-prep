#!/bin/bash

# DevOps Interview Prep - Always use latest version
# Usage: ./devops-ip.sh practice aws
#        ./devops-ip.sh topics
#        ./devops-ip.sh interview --count 10

IMAGE="moabukar/mockops:latest"
PLATFORM="linux/arm64"  # change to linux/amd64 if needed

echo "🔄 Pulling latest DevOps Interview Prep image..."
docker pull $IMAGE

echo "🚀 Starting DevOps Interview Prep..."
docker run --platform $PLATFORM -it --rm $IMAGE "$@"