#!/bin/bash

# Add the project root to the PYTHONPATH
export PYTHONPATH=$(pwd):$(pwd)/app

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app/main.py
