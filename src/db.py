import asyncio
import logging
import json
from supabase import create_client, Client
import datetime
from colorlog import ColoredFormatter
from src.config import config
import uvloop
import uvloop
import os

OUTPUT_DIR = "output"
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_CLIENT_KEY")
supabase: Client = create_client(url, key)


url_extraction = "https://vvblngfsnsoraabwhbtu.supabase.co"
key_extraction = os.getenv("SUPABASE_KEY")
            
supabase_extraction: Client = create_client(url_extraction, key_extraction)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def write_extracted_table(esg_factors, esg_details, isn, year):
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


async def read_extracted_table(isn, year):
    try:
        result, count = await asyncio.to_thread(
            lambda: supabase.table(config["EXTRACTED_DATA_TABLE"])
            .select("*")
            .eq("isn", isn)
            .eq("year", year)
            .execute()
        )
        print("Extracted data read successfully from Supabase.")
        result = result[1][0]
        return result
    except Exception as e:
        print(f"Failed to read extracted data: {e}")
        raise


async def write_score_table(isn, year, strategy_id, score):
    try:
        
        await asyncio.to_thread(
            lambda: supabase.table(config["SCORES_TABLE"])
            .delete()
            .eq("isn", isn)
            .eq("year", year)
            .eq("strategy_id", strategy_id)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["SCORES_TABLE"])
            .insert({"isn": isn, "year": year, "strategy_id": strategy_id, "score": score})
            .execute()
        )
        print("Score data inserted into Supabase successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert score data into Supabase: {e}")
        raise


async def read_score_table(isn, year):
    try:
        result, count = await asyncio.to_thread(
            lambda: supabase.table(config["SCORES_TABLE"])
            .select("*")
            .eq("isn", isn)
            .eq("year", year)
            .execute()
        )
        result = result[1][0]
        print("Score data read successfully from Supabase.")
        return result
    except Exception as e:
        print(f"Failed to read score data: {e}")
        raise


async def write_company_table(isin, nse_symbol, bse_secutity_code, company_name, industry, sector, country, details, logo_url):
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


async def read_company_table(isin):
    try:
        result, countc = await asyncio.to_thread(
            lambda: supabase.table(config["COMPANY_TABLE"])
            .select("*")
            .eq("isin_no", isin)
            .execute()
        )
        print("Company data read successfully from Supabase.")
        result = result[1][0]
        return result
    except Exception as e:
        print(f"Failed to read company data: {e}")
        raise


async def write_ui_table(isin_no, name, summary, details):
    try:
        await asyncio.to_thread(
            lambda: supabase.table(config["UI_TABLE"])
            .delete()
            .eq("isin_no", isin_no)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["UI_TABLE"])
            .insert({"isin_no": isin_no, "name": name, "summary": summary, "details": details})
            .execute()
        )
        print("Data inserted into UI Table successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert data into Supabase (UI Table): {e}")
        raise


async def update_user_table_entry(user_id, company_name, file_id):
    try:
        result, _ = await asyncio.to_thread(
            lambda: supabase.table(config["USERS_TABLE"])
            .select("*")
            .eq("id", user_id)
            .execute()
        )
        result = result[1][0]

        

        for company_file in result["company_files"]:
            if company_file["id"] == file_id:
                company_file["company_name"] = company_name
                company_file["status"] = "Completed"
                company_file["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
    


        # for isin_file in result["isin_files"]:
        #     if isin_file["id"] == isin_files["file_id"]:
        #         isin_file["name"] = isin_files["name"]
        #         isin_file["url"] = isin_files["url"]
        #         isin_file["status"] = isin_files["status"]
        #         isin_file["timestamp"] = isin_files["timestamp"]
        #         break
        
        await asyncio.to_thread(
            lambda: supabase.table(config["USERS_TABLE"])
            .update({"company_files": result["company_files"]})
            .eq("id", user_id)
            .execute()
        )
        print("User table updated successfully.")
    except Exception as e:
        print(f"Failed to update user table: {e}")
        raise


async def write_extracted_with_source_table(isin, esg_factors, year, user_id = "FinQ_default"):
    try:
        await asyncio.to_thread(
            lambda: supabase.table(config["EXTRACTED_WITH_SOURCE_TABLE"])
            .delete()
            .eq("isin", isin)
            .eq("year", year)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["EXTRACTED_WITH_SOURCE_TABLE"])
            .insert({"isin": isin, "esg_factors": esg_factors, "year": year, "user_id": user_id})
            .execute()
        )
        print("Data inserted into 'Extracted with Source' Table successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert data into Supabase ('Extracted with Source' Table): {e}")
        raise


async def read_user_table_entry(user_id):
    try:
        result, _ = await asyncio.to_thread(
            lambda: supabase.table(config["USERS_TABLE"])
            .select("*")
            .eq("id", user_id)
            .execute()
        )
        result = result[1][0]
        print("User data read successfully from Supabase.")
        return result
    except Exception as e:
        print(f"Failed to read user data: {e}")
        raise


async def write_gri_template_table(name, format, topic, division, id ):
    try:
        await asyncio.to_thread(
            lambda: supabase.table(config["GRI_TEMPLATE_TABLE"])
            .delete()
            .eq("id", id)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["GRI_TEMPLATE_TABLE"])
            .insert({"name": name, "format": format, "topic": topic, "division": division, "id": id})
            .execute()
        )
        print("Data inserted into GRI Template Table successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert data into Supabase (GRI Template Table): {e}")
        raise


async def read_gri_template(template_id):
    try:
        result, count = await asyncio.to_thread(
            lambda: supabase.table(config["GRI_TEMPLATE_TABLE"])
            .select("*")
            .eq("id", template_id)
            .execute()
        )
        result = result[1][0]
        print("GRI Template read successfully from Supabase.")
        return result
    except Exception as e:
        print(f"Failed to read GRI Template: {e}")
        raise


async def write_gri_extraction_table(isin, topic_id, extracted_data):
    try:
        await asyncio.to_thread(
            lambda: supabase.table(config["GRI_EXTRACTION_TABLE"])
            .delete()
            .eq("isin", isin)
            .eq("topic_id", topic_id)
            .execute()
        )
        result = await asyncio.to_thread(
            lambda: supabase.table(config["GRI_EXTRACTION_TABLE"])
            .insert({"isin": isin, "topic_id": topic_id, "extraction": extracted_data})
            .execute()
        )
        print(f"Data inserted into GRI Extraction Table for {isin} successfully.")
        return result
    except Exception as e:
        print(f"Failed to insert data into Supabase (GRI Extraction Table) for {isin}: {e}")
        raise

async def read_gri_extraction_table(topic_id):
    try:
        result, count = await asyncio.to_thread(
            lambda: supabase.table(config["GRI_EXTRACTION_TABLE"])
            .select("*")
            .eq("topic_id", topic_id)
            .execute()
        )
        result = result[1][0]
        print("GRI Extraction data read successfully from Supabase.")
        return result
    except Exception as e:
        print(f"Failed to read GRI Extraction data: {e}")
        raise

async def get_all_gri_extraction():
    try:
        result, count = await asyncio.to_thread(
            lambda: supabase.table(config["GRI_EXTRACTION_TABLE"])
            .select("topic_id")
            .execute()
        )
        result = result[1]
        print("GRI Extraction data read successfully from Supabase.")
        return result
    except Exception as e:
        print(f"Failed to read GRI Extraction data: {e}")
        raise