import os
import sqlite3
from typing import Optional, Dict

class Storage:
    def __init__(self, db_path="crawled_data.db", storage_dir="crawled"):
        self.db_path = db_path
        self.storage_dir = storage_dir

        # Ensure storage directory exists
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

        # Initialize database
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database for storing metadata."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create the table if it doesn't exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS crawled_pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    file_path TEXT NOT NULL,
                    metadata TEXT
                )
                """
            )
            # Check and add the `metadata` column if it doesn't exist
            cursor.execute("PRAGMA table_info(crawled_pages)")
            columns = [row[1] for row in cursor.fetchall()]
            if "metadata" not in columns:
                cursor.execute("ALTER TABLE crawled_pages ADD COLUMN metadata TEXT")
            conn.commit()

    def save_content(self, url: str, html: str, metadata: Optional[Dict] = None):
        """Save the HTML content and metadata for a crawled URL."""
        # Save HTML content to a file
        sanitized_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        file_path = os.path.join(self.storage_dir, sanitized_filename + ".html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html)

        # Save metadata to the database
        metadata_str = str(metadata) if metadata else None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO crawled_pages (url, file_path, metadata)
                VALUES (?, ?, ?)
                """,
                (url, file_path, metadata_str)
            )
            conn.commit()

    def get_metadata(self, url: str) -> Optional[Dict]:
        """Retrieve metadata for a given URL."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT metadata FROM crawled_pages WHERE url = ?
                """,
                (url,)
            )
            result = cursor.fetchone()
            if result:
                return eval(result[0])  # Convert metadata string back to dictionary
        return None

    def list_crawled_pages(self):
        """List all crawled pages with their metadata."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT url, file_path, metadata FROM crawled_pages
                """
            )
            return cursor.fetchall()

if __name__ == "__main__":
    storage = Storage()

    # Example usage
    test_url = "https://example.com"
    test_html = "<html><body><h1>Example</h1></body></html>"
    test_metadata = {"status": 200, "content_type": "text/html"}

    storage.save_content(test_url, test_html, test_metadata)

    print("Metadata:", storage.get_metadata(test_url))
    print("Crawled Pages:", storage.list_crawled_pages())
