import asyncio
import logging
import json
from supabase import create_client, Client

from src.services.company_info import get_company_info
from src.rag.create import instantiate_vectorstore
from colorlog import ColoredFormatter
from src.config import config
import os


OUTPUT_DIR = "output"
url: str = "https://vuxvzlnwphczonlmagcr.supabase.co"
key: str = os.getenv("SUPABASE_CLIENT_KEY")
supabase: Client = create_client(url, key)

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

async def update_table(isin, nse_symbol, bse_secutity_code, company_name, industry, sector, country, details, logo_url):
    try:
        await asyncio.to_thread(
            lambda: supabase.table(config["COMPANY_TABLE"])
            .delete()
            .eq("isin_no", isin)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["COMPANY_TABLE"])
            .insert({"isin_no": isin, "nse_symbol": nse_symbol, "bse_security_code": bse_secutity_code, "company_name": company_name, "industry": industry, "sector": sector, "country": country, "details": details, "logo": logo_url})
            .execute()
        )
        print("Data inserted into Company Table successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert data into Supabase (Company Table): {e}")
        raise


async def update_company_table(company_info):
    try:
        try:
            vectorstore = await instantiate_vectorstore(company_info["filepath"])
            print(f"Vectorstore instantiated successfully.")
        except Exception as e:
            print(f"Failed to instantiate vectorstore: {e}")
            raise

        try:
            hitory_awards_services = await get_company_info(vectorstore)
            print("Company info extracted successfully.")

            details = {
                "summary": hitory_awards_services,
            }

            try:
                result = await update_table(company_info["isin"], company_info["nse_symbol"], company_info["bse_security_code"], company_info["company_name"], company_info["industry"], company_info["sector"], company_info["country"], details, company_info["logo"])
                print("Company info inserted into Supabase successfully.")
                return result
            except Exception as e:
                print(f"Failed to insert company info into Supabase: {e}")
                raise
        except Exception as e:
            print(f"Failed to extract company info: {e}")
            raise


    except Exception as e:
        print(f"Failed to update company table: {e}")
        raise

