import json
import logging
from pathlib import Path

CACHE_DIR = Path("cache")
LOG_FILE = "gather.log"

# Set up logging
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(LOG_FILE),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def get_cached_files():
    return sorted(CACHE_DIR.glob("response_*.json"))

def extract_document_urls(data):
    documents = data.get("documents", [])
    return [doc.get("docUrl", "") for doc in documents]

def transform_url(url):
    if url.startswith("https://www.census.gov/library/working-papers/"):
        # Split the URL into parts
        parts = url.split("/")
        # Change 'www' to 'www2'
        parts[2] = "www2.census.gov"
        # Change the file extension from 'html' to 'pdf'
        parts[-1] = parts[-1].replace(".html", ".pdf")
        # Reconstruct the URL
        return "/".join(parts)
    return url

def process_urls(urls):
    return [transform_url(url) for url in urls]


def payload():
    logger.info("Starting document URL aggregation process")
    
    all_urls = set()
    cached_files = get_cached_files()
    
    logger.info(f"Found {len(cached_files)} cached JSON files")
    
    for file_path in cached_files:
        logger.info(f"Processing file: {file_path}")
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            urls = extract_document_urls(data)
            all_urls.update(urls)
            
            logger.info(f"Extracted {len(urls)} URLs from {file_path}")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
    
    logger.info(f"Total unique URLs found: {len(all_urls)}")
    
    # https://www.census.gov/library/working-papers/2024/demo/sehsd-wp2024-20.html
    # https://www2.census.gov/library/working-papers/2024/demo/sehsd-wp2024-20.pdf
    out = []
    for url in sorted(all_urls):
        new_url = transform_url(url)
        out.append(new_url)
        print(new_url)
    
    logger.info("Document URL aggregation process completed")
    return out

def main():
    out = payload()
    logger.info(f"Found {len(out)} URLs")

if __name__ == "__main__":
    main()