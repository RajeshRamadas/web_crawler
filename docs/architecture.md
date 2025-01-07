
# Web Crawler Design

## Folder Structure

```plaintext
web_crawler/
├── config/
│   ├── settings.py            # Configuration settings (e.g., API keys, timeout, DB settings)
│   ├── logger_config.py       # Logging configuration
│   └── __init__.py
├── core/
│   ├── __init__.py
│   ├── downloader.py          # Handles HTTP requests to fetch web pages
│   ├── frontier.py            # Manages the URL frontier (queue, deduplication, prioritization)
│   ├── parser.py              # Parses content, extracts data and links
│   ├── scheduler.py           # Orchestrates crawling logic and task distribution
│   └── robots_handler.py      # Fetches and respects robots.txt policies
├── db/
│   ├── storage.py             # Manages storage of crawled data (e.g., raw HTML, metadata)
│   ├── indexer.py             # Indexing logic for search or analysis
│   └── __init__.py
├── tests/
│   ├── test_downloader.py     # Unit tests for downloader
│   ├── test_frontier.py       # Unit tests for URL frontier
│   ├── test_parser.py         # Unit tests for parser
│   ├── test_scheduler.py      # Unit tests for scheduler
│   ├── test_robots_handler.py # Unit tests for robots.txt handler
│   └── __init__.py
├── utils/
│   ├── logger.py              # Utility for logging
│   ├── url_utils.py           # Utilities for URL normalization and validation
│   └── __init__.py
├── scripts/
│   ├── seed_urls.py           # Script to initialize seed URLs for the crawler
│   ├── monitor.py             # Script to monitor crawler performance
│   └── __init__.py
├── docs/
│   ├── architecture.md        # Documentation of the system design
│   ├── usage.md               # Instructions for using the crawler
│   └── requirements.md        # List of functional and non-functional requirements
├── main.py                    # Entry point for running the crawler
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview and setup instructions

# Web Crawler Project Structure

This document provides an overview of the folder structure for the web crawler project.

## Description of Key Folders

### 1. `config/`
Stores all configuration settings to centralize configuration management.
- **`settings.py`**: Contains settings like database credentials, timeout limits, user agents, etc.
- **`logger_config.py`**: Configuration for logging levels and formats.

### 2. `core/`
Contains the main logic for the crawler.
- **`downloader.py`**: Implements HTTP requests using libraries like `requests` or `aiohttp`.
- **`frontier.py`**: Manages the queue of URLs to crawl and handles prioritization/deduplication.
- **`parser.py`**: Parses HTML or other content types, extracts links and useful data.
- **`scheduler.py`**: Orchestrates crawling, delegates tasks to workers or distributed nodes.
- **`robots_handler.py`**: Fetches and processes `robots.txt` to respect crawling rules.

### 3. `db/`
Handles data storage and indexing for efficient querying and analysis.
- **`storage.py`**: Implements raw content and metadata storage (e.g., using MongoDB, Elasticsearch).
- **`indexer.py`**: Provides indexing functionality for efficient search and data retrieval.

### 4. `tests/`
Contains unit tests for each component to ensure reliability and robustness.

### 5. `utils/`
Provides helper functions for common tasks.
- **`logger.py`**: Sets up logging utilities.
- **`url_utils.py`**: Functions for URL normalization, validation, and deduplication.

### 6. `scripts/`
Standalone scripts for specific tasks.
- **`seed_urls.py`**: Adds initial URLs to the frontier.
- **`monitor.py`**: Tracks system performance, logs, and metrics for debugging.

### 7. `docs/`
Includes documentation for the system.
