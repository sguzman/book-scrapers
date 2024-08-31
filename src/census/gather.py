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
        out.append(url)
        print(url)
    
    logger.info("Document URL aggregation process completed")
    return out

def main():
    out = payload()
    logger.info(f"Found {len(out)} URLs")

if __name__ == "__main__":
    main()