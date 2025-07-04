#!/bin/bash

# Isaac Sim 5.0 Python Bindings - Remote Setup Script
# This script sets up the remote environment for Isaac Sim 5.0 development

set -e

echo "🚀 Isaac Sim 5.0 Python Bindings - Remote Setup"
echo "================================================"

# Configuration
REMOTE_HOST="3.239.124.24"
SSH_KEY="~/g1-stabilization-key.pem"
REMOTE_USER="ubuntu"
REMOTE_DIR="/workspace/IsaacSimPython"

echo "�� Configuration:"
echo "   Remote Host: $REMOTE_HOST"
echo "   SSH Key: $SSH_KEY"
echo "   Remote User: $REMOTE_USER"
echo "   Remote Directory: $REMOTE_DIR"

# Check if SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    echo "Please ensure the SSH key is in the correct location"
    exit 1
fi

echo "✅ SSH key found"

# Test SSH connection
echo "🔍 Testing SSH connection..."
if ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "echo 'SSH connection successful'"; then
    echo "✅ SSH connection successful"
else
    echo "❌ SSH connection failed"
    exit 1
fi

# Create remote directory
echo "📁 Creating remote directory..."
ssh -i "$SSH_KEY" "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $REMOTE_DIR"

# Copy project files to remote
echo "📤 Copying project files to remote..."
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
    -e "ssh -i $SSH_KEY" \
    ./ "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

echo "✅ Files copied to remote"

# Set up Python environment on remote
echo "🐍 Setting up Python environment on remote..."
ssh -i "$SSH_KEY" "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt"

echo "✅ Python environment set up"

# Test remote setup
echo "🧪 Testing remote setup..."
ssh -i "$SSH_KEY" "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && \
    source venv/bin/activate && \
    python3 -c 'from src.bindings import IsaacSimEnvironment; print(\"✅ Import successful\")'"

echo "✅ Remote setup completed successfully!"

echo ""
echo "�� Remote Environment Information:"
echo "   SSH Command: ssh -i $SSH_KEY $REMOTE_USER@$REMOTE_HOST"
echo "   Remote Directory: $REMOTE_DIR"
echo "   WebRTC Stream: http://$REMOTE_HOST:8211"
echo "   REST API: http://$REMOTE_HOST:3009"
echo ""
echo "�� Next Steps:"
echo "   1. SSH into the remote machine"
echo "   2. Navigate to $REMOTE_DIR"
echo "   3. Activate the virtual environment: source venv/bin/activate"
echo "   4. Run examples: python3 src/examples/basic_usage.py"
