import asyncio
import logging
import json
from supabase import create_client, Client
from colorlog import ColoredFormatter
from src.config import config
url: str = "https://vuxvzlnwphczonlmagcr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1eHZ6bG53cGhjem9ubG1hZ2NyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTk0OTk4NSwiZXhwIjoyMDQxNTI1OTg1fQ.41kfakfDnIpK9yyf2enpYzelRD4uGXAN4mIzDemsANM"
supabase: Client = create_client(url, key)
from src.db import read_extracted_table, read_score_table, read_company_table, write_ui_table

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def update_ui_table(company_info):
    extracted_data = await read_extracted_table(company_info["isin"], company_info["year"])
    score_data = await read_score_table(company_info["isin"], company_info["year"])
    company_data = await read_company_table(company_info["isin"])

    summary = {}
    summary["sector"] = company_info["sector"]
    summary["history"] = company_data["details"]["summary"]["company_history"]
    summary["product_and_services"] = company_data["details"]["summary"]["products_and_services"]
    summary["awards_or_recognition"] = company_data["details"]["summary"]["awards_and_recognition"]
    summary["industry"] = company_info["industry"]
    summary["nse_symbol"] = company_info["nse_symbol"]
    summary["company_name"] = company_info["company_name"]
    summary["bse_security_code"] = company_info["bse_security_code"]
    summary["primary_listing_country"] = company_info["country"]
    summary["primary_operating_country"] = company_info["country"]

    details = []
    base_json = {}
    base_json["year"] = company_info["year"]
    base_json["derived"] = score_data["score"]
    base_json["extracted"] = extracted_data["esg_details"]

    details.append(base_json)

    try:
        result = await write_ui_table(company_info["isin"],company_info["company_name"], summary, details)
        print("UI data inserted into Supabase successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert UI data into Supabase: {e}")
        raise



