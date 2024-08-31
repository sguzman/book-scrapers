import requests
import json
from pathlib import Path
import time
import logging

BASE_URL = "https://xilinxcomprode2rjoqok.org.coveo.com/rest/search/v2?organizationId=xilinxcomprode2rjoqok"
CACHE_DIR = Path("amd_cache")
total_results = 1531

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer xx5ee91b6a-e227-4c6f-83f2-f2120ca3509e",
    "content-length": "9268",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://www.amd.com",
    "priority": "u=1, i",
    "referer": "https://www.amd.com/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

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
        "locale": "en",
        "debug": False,
        "tab": "default",
        "referrer": "https://www.bing.com/",
        "timezone": "America/Los_Angeles",
        "cq": "(@amd_result_type==\"Documents\") AND (@amd_curated_category==\"Processor Tech Docs\" OR @amd_curated_category==\"Pensando Tech Docs\" OR @amd_curated_category==\"Radeon Tech Docs\" OR @amd_curated_category==\"EPYC Technical Docs\" OR @amd_curated_category==\"EPYC Business Docs\" OR @amd_curated_category==\"Instinct Business Docs\" OR @amd_curated_category==\"Pensando Business Docs\" OR @amd_curated_category==\"Instinct Tech Docs\" OR @amd_curated_category==\"Archived Tech Docs\")",
        "context": {"amd_lang": "en"},
        "fieldsToInclude": [
            "author", "language", "urihash", "objecttype", "collection", "source",
            "permanentid", "date", "filetype", "parents", "ec_price", "ec_name",
            "ec_description", "ec_brand", "ec_category", "ec_item_group_id",
            "ec_shortdesc", "ec_thumbnails", "ec_images", "ec_promo_price",
            "ec_in_stock", "ec_rating", "amd_result_type", "amd_release_date",
            "amd_lang", "amd_result_image", "limessageissolution",
            "lithreadhassolution", "description", "amd_partner", "amd_cta_link",
            "amd_hub_pull_command", "amd_child_design_file",
            "amd_child_associated_file", "amd_video_date", "amd_video_duration",
            "amd_video_views", "ytlikecount", "amd_document_id", "amd_document_type",
            "amd_document_location", "amd_claim_text", "amd_cert_driver_app_name",
            "amd_cert_driver_app_version", "amd_cert_driver_brand_name",
            "amd_cert_driver_isv", "amd_cert_driver_name", "amd_cert_driver_os",
            "amd_cert_driver_url", "amd_cert_driver_video_card",
            "amd_support_article_type", "amd_app_type", "amd_category",
            "amd_product_category", "amd_supported_workloads",
            "amd_target_platforms", "amd_product_vendor", "amd_vendor_type",
            "amd_is_external_link"
        ],
        "q": "",
        "enableQuerySyntax": False,
        "searchHub": "tech-docs-hub-sh",
        "sortCriteria": "@amd_release_date descending",
        "queryCorrection": {
            "enabled": False,
            "options": {"automaticallyCorrect": "whenNoResults"}
        },
        "enableDidYouMean": True,
        "facets": [
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "AMD.com",
                "state": "idle"
                },
                {
                "value": "Partner Hosted",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_document_location",
            "field": "amd_document_location"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "Active",
                "state": "idle"
                },
                {
                "value": "Archived",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_archive_status",
            "field": "amd_archive_status"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "Solution Briefs",
                "state": "idle"
                },
                {
                "value": "Performance Briefs",
                "state": "idle"
                },
                {
                "value": "White Papers",
                "state": "idle"
                },
                {
                "value": "Datasheets",
                "state": "idle"
                },
                {
                "value": "Design Tools",
                "state": "idle"
                },
                {
                "value": "Tuning Guides",
                "state": "idle"
                },
                {
                "value": "Programmer References",
                "state": "idle"
                },
                {
                "value": "Application Notes",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_document_type",
            "field": "amd_document_type"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "Technical",
                "state": "idle"
                },
                {
                "value": "Business",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_audience",
            "field": "amd_audience"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "Servers",
                "state": "idle"
                },
                {
                "value": "Desktops",
                "state": "idle"
                },
                {
                "value": "Workstations",
                "state": "idle"
                },
                {
                "value": "Laptops",
                "state": "idle"
                },
                {
                "value": "Embedded Platforms",
                "state": "idle"
                },
                {
                "value": "SmartSwitch",
                "state": "idle"
                },
                {
                "value": "Semi-Custom",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_form_factor",
            "field": "amd_form_factor"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "Processors",
                "state": "idle"
                },
                {
                "value": "Accelerators",
                "state": "idle"
                },
                {
                "value": "Graphics",
                "state": "idle"
                },
                {
                "value": "Networking Infrastructure",
                "state": "idle"
                },
                {
                "value": "Software & Applications",
                "state": "idle"
                },
                {
                "value": "Development Tools",
                "state": "idle"
                },
                {
                "value": "Adaptive SoCs & FPGAs",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_product_type",
            "field": "amd_product_type",
            "customSort": [
                "Processors",
                "Accelerators",
                "Graphics"
            ]
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "EPYC",
                "state": "idle"
                },
                {
                "value": "EPYC Embedded",
                "state": "idle"
                },
                {
                "value": "Ryzen Threadripper PRO",
                "state": "idle"
                },
                {
                "value": "Ryzen Threadripper",
                "state": "idle"
                },
                {
                "value": "Ryzen PRO",
                "state": "idle"
                },
                {
                "value": "Ryzen",
                "state": "idle"
                },
                {
                "value": "Instinct",
                "state": "idle"
                },
                {
                "value": "Radeon RX",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_product_brand",
            "field": "amd_product_brand",
            "customSort": [
                "EPYC",
                "EPYC Embedded",
                "Ryzen Threadripper PRO",
                "Ryzen Threadripper",
                "Ryzen PRO",
                "Ryzen",
                "Ryzen Embedded",
                "Athlon",
                "Instinct",
                "Radeon PRO",
                "Radeon RX",
                "Radeon R9 / R7 / R5",
                "Radeon HD",
                "Radeon 600 500 400",
                "Legacy Graphics"
            ]
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "EPYC 9004 Series",
                "state": "idle"
                },
                {
                "value": "EPYC 8004 Series",
                "state": "idle"
                },
                {
                "value": "EPYC 7003 Series",
                "state": "idle"
                },
                {
                "value": "EPYC 7002 Series",
                "state": "idle"
                },
                {
                "value": "EPYC 7001 Series",
                "state": "idle"
                },
                {
                "value": "Ryzen Threadripper PRO 5000 WX-Series",
                "state": "idle"
                },
                {
                "value": "Ryzen Threadripper 3000 Series",
                "state": "idle"
                },
                {
                "value": "Ryzen Threadripper 2000 Series",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_product_series",
            "field": "amd_product_series",
            "customSort": [
                "EPYC 9004 Series",
                "EPYC 8004 Series",
                "EPYC 7003 Series",
                "EPYC 7002 Series",
                "EPYC 7001 Series",
                "EPYC Embedded 9004 Series",
                "EPYC Embedded 7003 Series",
                "EPYC Embedded 7002 Series",
                "EPYC Embedded 7001 Series",
                "EPYC Embedded 3000 Series",
                "Ryzen Threadripper PRO 5000 WX-Series",
                "Ryzen Threadripper PRO 3000 WX-Series",
                "Ryzen Threadripper 3000 Series",
                "Ryzen Threadripper 2000 Series",
                "Ryzen Threadripper 1000 Series",
                "Ryzen PRO 7000 Series",
                "Ryzen PRO 6000 Series",
                "Ryzen PRO 5000 Series",
                "Ryzen PRO 4000 Series",
                "Ryzen PRO 3000 Series",
                "Ryzen PRO 2000 Series",
                "Ryzen PRO 1000 Series",
                "Ryzen 7000 Series",
                "Ryzen 6000 Series",
                "Ryzen 5000 Series"
            ]
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "High Performance Computing",
                "state": "idle"
                },
                {
                "value": "Database & Data Analytics",
                "state": "idle"
                },
                {
                "value": "HCI & Virtualization",
                "state": "idle"
                },
                {
                "value": "Design & Simulation",
                "state": "idle"
                },
                {
                "value": "Cloud Computing",
                "state": "idle"
                },
                {
                "value": "AI & Machine Learning",
                "state": "idle"
                },
                {
                "value": "Network & Infrastructure Acceleration",
                "state": "idle"
                },
                {
                "value": "Hosting",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_applications_technologies",
            "field": "amd_applications_technologies"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "HPE",
                "state": "idle"
                },
                {
                "value": "Dell",
                "state": "idle"
                },
                {
                "value": "Lenovo",
                "state": "idle"
                },
                {
                "value": "Microsoft Azure",
                "state": "idle"
                },
                {
                "value": "AWS",
                "state": "idle"
                },
                {
                "value": "Google Cloud",
                "state": "idle"
                },
                {
                "value": "Supermicro",
                "state": "idle"
                },
                {
                "value": "Cisco",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_partner",
            "field": "amd_partner"
            },
            {
            "filterFacetCount": True,
            "injectionDepth": 1000,
            "numberOfValues": 8,
            "sortCriteria": "occurrences",
            "resultsMustMatch": "atLeastOneValue",
            "type": "specific",
            "currentValues": [
                {
                "value": "Data Center (Cloud & Hosting Services)",
                "state": "idle"
                },
                {
                "value": "Software & Sciences",
                "state": "idle"
                },
                {
                "value": "Design & Manufacturing",
                "state": "idle"
                },
                {
                "value": "Media & Entertainment",
                "state": "idle"
                },
                {
                "value": "Healthcare & Sciences",
                "state": "idle"
                },
                {
                "value": "Electronic Design Automation",
                "state": "idle"
                },
                {
                "value": "Financial Services",
                "state": "idle"
                },
                {
                "value": "Supercomputing & Research",
                "state": "idle"
                }
            ],
            "freezeCurrentValues": False,
            "isFieldExpanded": False,
            "preventAutoSelect": False,
            "facetId": "amd_industries",
            "field": "amd_industries"
            }
        ],
        "numberOfResults": 96,
        "firstResult": start_row,
        "facetOptions": {"freezeFacetOrder": False}
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
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