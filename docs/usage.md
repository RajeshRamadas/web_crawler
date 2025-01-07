# Usage Instructions for Web Crawler

## Prerequisites
1. **Python Environment**:
   - Install Python (version >= 3.8).
   - Ensure pip (Python package installer) is available.

2. **Dependencies**:
   - Install required libraries from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

3. **Database Setup**:
   - Set up the database for storing crawled data (e.g., MongoDB, Elasticsearch).
   - Update the connection settings in `config/settings.py`.

4. **Seed URLs**:
   - Add initial URLs to the `scripts/seed_urls.py` file or directly to the database.

5. **Configuration**:
   - Modify `config/settings.py` for custom settings (e.g., timeout, user agent, database credentials).
   - Set up logging preferences in `config/logger_config.py`.

---

## Running the Crawler

1. **Start the Crawler**:
   - Run the main entry point:
     ```bash
     python main.py
     ```

2. **Monitor Logs**:
   - Logs will be generated in the specified location (configured in `logger_config.py`).
   - Use `scripts/monitor.py` for real-time performance metrics:
     ```bash
     python scripts/monitor.py
     ```

3. **Customizing the Crawl**:
   - To change the crawling logic, edit `core/scheduler.py` or `core/frontier.py`.
   - Update crawling rules in `core/robots_handler.py` for specific domains.

---

## File Descriptions

### Config Files
- **`config/settings.py`**: Holds configurable parameters like database credentials, timeout limits, and user agents.
- **`config/logger_config.py`**: Configures logging levels and file locations.

### Core Modules
- **`core/downloader.py`**: Manages HTTP requests for fetching pages.
- **`core/frontier.py`**: Handles URL queues and deduplication.
- **`core/parser.py`**: Extracts links and useful data from pages.
- **`core/scheduler.py`**: Orchestrates crawling tasks.
- **`core/robots_handler.py`**: Ensures compliance with robots.txt rules.

### Scripts
- **`scripts/seed_urls.py`**: Initializes the seed URLs for crawling.
- **`scripts/monitor.py`**: Monitors crawler performance and system metrics.

### Database Modules
- **`db/storage.py`**: Handles storage of raw data, metadata, and parsed content.
- **`db/indexer.py`**: Provides indexing functionality for fast data retrieval.

---

## Testing
1. **Unit Tests**:
   - Run unit tests for individual components (located in `tests/`):
     ```bash
     pytest tests/
     ```

2. **Test Coverage**:
   - Check test coverage to ensure robustness:
     ```bash
     pytest --cov=core tests/
     ```

---

## Scaling the Crawler
1. **Distributed Crawling**:
   - Use multiple instances of the crawler to handle high volumes.
   - Configure a distributed queue like Kafka or RabbitMQ.

2. **Sharding**:
   - Divide the URL frontier into shards based on domains for parallel processing.

3. **Database Scaling**:
   - Use scalable storage solutions like HDFS or cloud-based databases for large datasets.

---

## Ethical Crawling Practices
1. **Respect Robots.txt**:
   - Ensure the crawler adheres to directives specified in robots.txt.

2. **Rate Limits**:
   - Set delays between requests to avoid overloading servers.

3. **Data Privacy**:
   - Avoid storing sensitive or personal data without user consent.

---

## Debugging
1. **Common Issues**:
   - **Connection Errors**: Check network settings and retry logic in `core/downloader.py`.
   - **Parsing Errors**: Debug HTML parsing logic in `core/parser.py`.

2. **Error Logs**:
   - Refer to logs generated in the specified directory for troubleshooting.

---

## Future Enhancements
1. Add support for new content types (e.g., videos, audio).
2. Implement machine learning models for prioritizing URLs.
3. Enhance scalability using container orchestration tools like Kubernetes.

