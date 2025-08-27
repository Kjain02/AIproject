import json
import asyncio
import logging
from colorlog import ColoredFormatter
from src.rag.query import find_relevant_chunks
from src.rag.template_query import rag_query
from src.config import config
import time

from src.rag.generate.employee_relations_satisfaction import fetch_employee_relations_satisfaction
from src.rag.generate.diversity_inclusion import fetch_diversity_inclusion
from src.rag.generate.health_safety_practices import fetch_health_safety_practices
from src.rag.generate.labor_standards_human_rights import fetch_labor_standards_human_rights
from src.rag.generate.community_engagement_social_responsibility import fetch_community_engagement_social_responsibility
from src.rag.generate.product_safety_customer_well_being import fetch_product_safety_customer_well_being

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

OUTPUT_DIR = "output"
filename = "rag/data/Sample-Statements-20240823T132542Z-001/Sample-Statements/2023-24.pdf"

async def employee_relations_satisfaction(vectorstore):
    try:
        query = rag_query['employee_relations_satisfaction']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        employee_relations_details = await fetch_employee_relations_satisfaction(relevant_chunks)
        print("Employee relations and satisfaction data fetched successfully.")
        return employee_relations_details
    except Exception as e:
        print(f"Failed to fetch employee relations and satisfaction data: {e}")
        raise

async def diversity_inclusion(vectorstore):
    try:
        query = rag_query['diversity_inclusion']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        diversity_details = await fetch_diversity_inclusion(relevant_chunks)
        print("Diversity and inclusion data fetched successfully.")
        return diversity_details
    except Exception as e:
        print(f"Failed to fetch diversity and inclusion data: {e}")
        raise

async def health_safety_practices(vectorstore):
    try:
        query = rag_query['health_safety_practices']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        health_safety_details = await fetch_health_safety_practices(relevant_chunks)
        print("Health and safety practices data fetched successfully.")
        return health_safety_details
    except Exception as e:
        print(f"Failed to fetch health and safety practices data: {e}")
        raise

async def labor_standards_human_rights(vectorstore):
    try:
        query = rag_query['labor_standards_human_rights']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        labor_standards_details = await fetch_labor_standards_human_rights(relevant_chunks)
        print("Labor standards and human rights data fetched successfully.")
        return labor_standards_details
    except Exception as e:
        print(f"Failed to fetch labor standards and human rights data: {e}")
        raise

async def community_engagement_social_responsibility(vectorstore):
    try:
        query = rag_query['community_engagement_social_responsibility']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        community_engagement_details = await fetch_community_engagement_social_responsibility(relevant_chunks)
        print("Community engagement and social responsibility data fetched successfully.")
        return community_engagement_details
    except Exception as e:
        print(f"Failed to fetch community engagement and social responsibility data: {e}")
        raise

async def product_safety_customer_well_being(vectorstore):
    try:
        query = rag_query['product_safety_customer_well_being']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        product_safety_details = await fetch_product_safety_customer_well_being(relevant_chunks)
        print("Product safety and customer well-being data fetched successfully.")
        return product_safety_details
    except Exception as e:
        print(f"Failed to fetch product safety and customer well-being data: {e}")
        raise

async def get_social_data(vectorstore):
    try:
        results = await asyncio.gather(
            employee_relations_satisfaction(vectorstore),
            diversity_inclusion(vectorstore),
            health_safety_practices(vectorstore),
            labor_standards_human_rights(vectorstore),
            community_engagement_social_responsibility(vectorstore),
            product_safety_customer_well_being(vectorstore)
        )
        employee_relations_data, diversity_data, health_safety_data, labor_standards_data, community_engagement_data, product_safety_data = results
        
        social_data = {
            "employee_relations_data": employee_relations_data,
            "diversity_data": diversity_data,
            "health_safety_data": health_safety_data,
            "labor_standards_data": labor_standards_data,
            "community_engagement_data": community_engagement_data,
            "product_safety_data": product_safety_data
        }
        print("Social data fetched successfully.")
        return social_data
    except Exception as e:
        print(f"Failed to fetch social data: {e}")
        raise