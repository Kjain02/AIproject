import asyncio
import json
import logging
import random
from colorlog import ColoredFormatter

from src.database_update.esg.extraction import update_extracted_table
from src.database_update.esg.score import update_score_table
from src.database_update.company_info.history_awards_services import update_company_table
from src.database_update.ui.ui_table import update_ui_table
from src.config import config

OUTPUT_DIR = "output"
MAX_RETRY = 3  # Maximum number of retries
INITIAL_DELAY = 2  # Initial delay before first retry (in seconds)

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Function to load company data from JSON file
def load_companies_from_json(file_path):
    try:
        with open(file_path, 'r') as jsonfile:
            companies = json.load(jsonfile)
        print(f"Successfully loaded {len(companies)} companies from JSON file.")
        return companies
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        exit(1)

async def process_company(company):
    filepath = company["filepath"]
    isin = company["isin"]
    year = company["year"]
    
    try:
        await update_extracted_table(filepath, isin, year)
        print(f"Extracted table updated successfully for {isin}.")
        await update_score_table(isin, year)
        print(f"Score table updated successfully for {isin}.")
        await update_company_table(company)
        print(f"Company table updated successfully for {isin}.")
        await update_ui_table(company)
        print(f"UI table updated successfully for {isin}.")
        return True
    except Exception as e:
        print(f"Failed to process company {isin}: {e}")
        return False

async def retry_with_backoff(company, retry_count):
    """Retry processing the company with exponential backoff and jitter."""
    delay = INITIAL_DELAY * (2 ** retry_count) + random.uniform(0, 1)  
    print(f"Retrying {company['isin']} after {delay:.2f} seconds (Retry {retry_count+1}/{MAX_RETRY})")
    await asyncio.sleep(delay)
    return await process_company(company)

async def retry_failed_companies(retry_queue):
    """Handle retrying companies in the retry queue."""
    failed_companies = []
    while retry_queue:
        company, retry_count = retry_queue.pop(0)
        success = await retry_with_backoff(company, retry_count)
        if not success and retry_count + 1 < MAX_RETRY:
            failed_companies.append((company, retry_count + 1))
        elif not success:
            print(f"Max retries reached for {company['isin']}.")

    return failed_companies

async def main():
    # Load companies from JSON
    companies = load_companies_from_json(config['COMPANY_JSON_FILE'])
    
    retry_queue = []
    tasks = []
    
    # Process all companies and queue failures for retry
    for company in companies:
        success = await process_company(company)
        if not success:
            retry_queue.append((company, 0))  # Add to retry queue with initial retry count

    print(f"Batch processing completed. Checking for failed companies. {len(retry_queue)} companies failed.")
    # Retry failed companies until success or max retries reached
    while retry_queue:
        print(f"Retrying {len(retry_queue)} failed companies.")
        retry_queue = await retry_failed_companies(retry_queue)
    
    print("Batch processing completed.")

if __name__ == "__main__":
    asyncio.run(main())
