#!/bin/bash
# Simple script to run the RSS generator

# Ensure virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the script
echo "Running RSS generator..."
python firstwordpharma_rss_scraper.py

echo "Done!"