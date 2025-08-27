import asyncio
import logging
import json
from supabase import create_client, Client

from src.services.board_members import get_board_member_info
from src.services.environmental import get_environmental_data
from src.services.governance import get_governance_data
from src.services.social import get_social_data
from src.rag.create import instantiate_vectorstore
from colorlog import ColoredFormatter
from src.config import config



OUTPUT_DIR = "output"
url: str = "https://vuxvzlnwphczonlmagcr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1eHZ6bG53cGhjem9ubG1hZ2NyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTk0OTk4NSwiZXhwIjoyMDQxNTI1OTg1fQ.41kfakfDnIpK9yyf2enpYzelRD4uGXAN4mIzDemsANM"
supabase: Client = create_client(url, key)

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

async def update_table(esg_factors, esg_details, isn, year):
    try:
        await asyncio.to_thread(
            lambda: supabase.table(config["EXTRACTED_DATA_TABLE"])
            .delete()
            .eq("isn", isn)
            .eq("year", year)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["EXTRACTED_DATA_TABLE"])
            .insert({"isn": isn, "year": year, "esg_factors": esg_factors, "esg_details": esg_details})
            .execute()
        )
        print("Data inserted into Extracted Table successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert data into Supabase (Extracted Table): {e}")
        raise

async def update_extracted_table(filename, isn, year):
    try:
        try:
            vectorstore = await instantiate_vectorstore(filename)
            print(f"Vectorstore instantiated successfully.")
        except Exception as e:
            print(f"Failed to instantiate vectorstore: {e}")
            raise

        try:

            results = await asyncio.gather(
                get_environmental_data(vectorstore),
                get_social_data(vectorstore),
                get_governance_data(vectorstore)
            )
            env_data, soc_data, gov_data = results

            esg_factors = {
                "environmental": env_data,
                "social": soc_data,
                "governance": gov_data
            }
            print("ESG factors extracted successfully.")
        except Exception as e:
            print(f"Failed to extract ESG factors: {e}")
            raise

        try:
            esg_details = {
                "environmental": "",
                "social": "",
                "governance": {
                    "board_members": await get_board_member_info(vectorstore)
                }
            }
            print("Board Member information extracted successfully.")
        except Exception as e:
            print(f"Failed to extract Board Member details: {e}")
            raise

        data_to_write = {
            "isn": isn,
            "year": year,
            "esg_factors": esg_factors,
            "esg_details": esg_details
        }

        try:
            with open(f"{OUTPUT_DIR}/extracted_data.json", "w") as f:
                json.dump(data_to_write, f, indent=4)
            print("Extracted data written to JSON file successfully.")
        except Exception as e:
            print(f"Failed to write extracted data to JSON file: {e}")
            raise

        try:
            await update_table(esg_factors, esg_details, isn, year)
        except Exception as e:
            print(f"Failed to update table in Supabase: {e}")
            raise
    except Exception as e:
        print(f"Failed to update extracted table: {e}")

