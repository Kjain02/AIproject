import asyncio
import logging
from src.rag.query import find_relevant_chunks
from src.rag.template_query import company_info_query

from src.rag.generate.company_info.awards_and_recognition import fetch_company_awards_recognition
from src.rag.generate.company_info.history import fetch_company_history
from src.rag.generate.company_info.producct_and_services import fetch_company_products_services
from colorlog import ColoredFormatter
import asyncio

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def company_hisrtory(vectorstore):
    try:
        query = company_info_query['company_history']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        company_history = await fetch_company_history(relevant_chunks)
        print("Company history fetched successfully.")
        return company_history
    except Exception as e:
        print(f"Failed to fetch company history: {e}")
        raise

async def company_awards_recognition(vectorstore):
    try:
        query = company_info_query['awards_and_recognition']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        company_awards_recognition = await fetch_company_awards_recognition(relevant_chunks)
        print("Company awards and recognition fetched successfully.")
        return company_awards_recognition
    except Exception as e:
        print(f"Failed to fetch company awards and recognition: {e}")
        raise

async def company_products_services(vectorstore):
    try:
        query = company_info_query['products_and_services']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        company_products_services = await fetch_company_products_services(relevant_chunks)
        print("Company products and services fetched successfully.")
        return company_products_services
    except Exception as e:
        print(f"Failed to fetch company products and services: {e}")
        raise


async def get_company_info(vectorstore):
    try:
        results = await asyncio.gather(
            company_hisrtory(vectorstore),
            company_awards_recognition(vectorstore),
            company_products_services(vectorstore)
        )
        history, awards_recognition, products_services = results
        company_info = {
            "company_history": history,
            "awards_and_recognition": awards_recognition,
            "products_and_services": products_services
        }
        print("Company information fetched successfully.")
        return company_info
    except Exception as e:
        print(f"Failed to fetch company information: {e}")
        raise