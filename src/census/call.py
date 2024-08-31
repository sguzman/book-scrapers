import os
import time
import requests
import logging
from urllib.parse import urlparse
from census import gather

# Set up logging
logging.basicConfig(filename='census_download.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def download_url(url, output_folder):
    """
    Download a URL, cache the response, and handle errors.
    """

    sleep_time=1

    # Create a filename based on the URL
    parsed_url = urlparse(url)
    filename = os.path.join(output_folder, parsed_url.path.strip('/').replace('/', '_') + '.html')

    # Check if the file already exists in cache
    if os.path.exists(filename):
        logging.info(f"Cache hit for {url}")
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    # Sleep before making the request
    time.sleep(sleep_time)

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the response to cache
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        logging.info(f"Successfully downloaded and cached {url}")
        return response.text
    
    except requests.RequestException as e:
        logging.error(f"Failed to download {url}: {str(e)}")
        return None

def download_census_urls(urls, output_folder):
    """
    Download a list of census URLs, caching results and handling errors.
    """
    for url in urls:
        result = download_url(url, output_folder)
        if result:
            print(f"Successfully processed: {url}")
        else:
            print(f"Failed to process: {url}")

if __name__ == "__main__":
    # Use the generate_census_urls function from gather.py
    census_urls = gather.payload()
    output_folder = "census_cache"
    
    download_census_urls(census_urls, output_folder)