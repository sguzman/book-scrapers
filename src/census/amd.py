import requests
import json
from pathlib import Path
import time
import logging

BASE_URL = "https://xilinxcomprode2rjoqok.org.coveo.com/rest/search/v2?organizationId=xilinxcomprode2rjoqok"
CACHE_DIR = Path("amd_cache")

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_directories():
    logger.info("Creating necessary directories")
    CACHE_DIR.mkdir(exist_ok=True)
    logger.info(f"Directories created: {CACHE_DIR}")

def get_cached_response(start_row):
    cache_file = CACHE_DIR / f"response_{start_row}.json"
    if cache_file.exists():
        logger.info(f"Cache hit: Using cached data for startRow {start_row}")
        with open(cache_file, "r") as f:
            return json.load(f)
    logger.info(f"Cache miss: No cached data found for startRow {start_row}")
    return None

def save_cached_response(start_row, data):
    cache_file = CACHE_DIR / f"response_{start_row}.json"
    with open(cache_file, "w") as f:
        json.dump(data, f)
    logger.info(f"Cached response saved for startRow {start_row}")

def fetch_data(start_row):
    cached_response = get_cached_response(start_row)
    if cached_response:
        return cached_response

    time.sleep(1)
    logger.info(f"Fetching data from API for startRow {start_row}")
    payload = {
        "baseTags": ["Census:Type/Working-Paper"],
        "documentPath": "/content/census/en/library/working-papers",
        "matchType": "all",
        "programs": [],
        "topics": [],
        "years": [],
        "geographies": [],
        "authors": [],
        "startRow": start_row,
        "sortBy": ["DATE_DESCENDING", "DATE_DESCENDING"]
    }

    try:
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched data for startRow {start_row}")
        save_cached_response(start_row, data)
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data for startRow {start_row}: {e}")
        raise

def main():
    logger.info("Starting Census working papers download process")
    create_directories()
    start_row = 0
    total_results = 4348

    while start_row < total_results:
        logger.info(f"Processing batch: startRow {start_row}")
        try:
            data = fetch_data(start_row)

            results_count = len(data.get("documents", []))
            logger.info(f"Processed {results_count} results in this batch")

            start_row += results_count
        except Exception as e:
            logger.error(f"An error occurred while processing startRow {start_row}: {e}")
            break

    logger.info("Census working papers download process completed")

if __name__ == "__main__":
    main()