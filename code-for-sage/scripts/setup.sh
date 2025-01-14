#!/bin/bash

# Setup script for development environment

echo "Setting up Sage Career Mentor Bot..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
if [ -d ".venv/Scripts" ]; then
    # Windows
    source .venv/Scripts/activate
else
    # Unix/MacOS
    source .venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set up environment
echo "Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from example"
fi

echo "Setup complete! Next steps:"
echo "1. Edit .env with your actual API keys"
echo "2. Run 'flask run' to start the development server"
