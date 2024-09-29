# Makefile

# Default target: help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the Scrapy spider"
	@echo "  make clean     - Clean up generated files"
	@echo "  make venv      - Set up virtual environment"

# Install dependencies
install:
	pip install -r requirements.txt

# Set up virtual environment
venv:
	python -m venv .venv
	@echo "Run 'source .venv/bin/activate' to activate the virtual environment."

# Run the Scrapy spider
run:
	scrapy crawl jobs -o jobs.json

# Clean up generated files
clean:
	rm -f jobs.json
