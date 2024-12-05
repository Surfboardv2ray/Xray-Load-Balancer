#!/bin/bash

# Update and upgrade the system
apt update && apt upgrade -y

# Install git if not already installed
if ! command -v git &>/dev/null; then
    apt install git -y
else
    echo "Git is already installed."
fi

# Install Python pip if not already installed
if ! command -v pip3 &>/dev/null; then
    apt install python3-pip -y
else
    echo "pip3 is already installed."
fi

# Install Python venv if not already installed
if ! python3 -m venv --help &>/dev/null; then
    apt install python3-venv -y
else
    echo "python3-venv is already installed."
fi

# Upgrade pip
python3 -m pip install --upgrade pip

# Clone the repository if it doesn't already exist
REPO_DIR="Xray-Load-Balancer"
if [ ! -d "$REPO_DIR" ]; then
    git clone https://github.com/Surfboardv2ray/Xray-Load-Balancer.git
    cd $REPO_DIR
else
    echo "Repository already exists."
    cd $REPO_DIR
fi

# Create and activate a virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

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