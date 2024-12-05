#!/bin/bash

# Update and upgrade the system
apt update && apt upgrade -y

# Install git if not already installed
if ! command -v git &>/dev/null; then
    apt install git -y
else
    echo "Git is already installed."
fi

# Install Python if not already installed
if ! command -v python3 &>/dev/null; then
    apt install python3 -y
    apt install python3-pip -y
else
    echo "Python is already installed."
fi

# Clone the repository if it doesn't already exist
REPO_DIR="Xray-Load-Balancer"
if [ ! -d "$REPO_DIR" ]; then
    git clone https://github.com/Surfboardv2ray/Xray-Load-Balancer.git
    cd $REPO_DIR
else
    echo "Repository already exists."
    cd $REPO_DIR
fi

# Install Python requirements
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found."
fi

# Run the Python script
if [ -f "server.py" ]; then
    python3 server.py
else
    echo "server.py not found."
fi