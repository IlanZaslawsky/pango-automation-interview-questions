#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create necessary directories
mkdir -p automation_framework/logs

echo "Setup completed successfully!"
echo "To activate the virtual environment, run: source venv/bin/activate" 