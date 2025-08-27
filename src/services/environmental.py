import json
import asyncio
import logging
from src.rag.query import find_relevant_chunks
from src.rag.template_query import rag_query

from src.rag.generate.carbon_emission_management import fetch_carbon_emissions
from src.rag.generate.resource_usage_efficiency import fetch_resource_usage_efficiency
from src.rag.generate.waste_management_pollution_control import fetch_waste_management_pollution_control
from src.rag.generate.climate_change_adaptation_risk import fetch_climate_change_adaptation_risk
from src.rag.generate.environmental_impact import fetch_environmental_impact
from src.config import config
import time
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

OUTPUT_DIR = "output"
filename = "rag/data/Sample-Statements-20240823T132542Z-001/Sample-Statements/2023-24.pdf"

async def environmental_impact(vectorstore):
    try:
        query = rag_query['environmental_impact']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        environmental_impact_details = await fetch_environmental_impact(relevant_chunks)
        print("Environmental impact data fetched successfully.")
        return environmental_impact_details
    except Exception as e:
        print(f"Failed to fetch environmental impact data: {e}")
        raise

async def carbon_emission_management(vectorstore):
    try:
        query = rag_query['carbon_emission_management']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        emissions_details = await fetch_carbon_emissions(relevant_chunks)
        print("Carbon emission management data fetched successfully.")
        return emissions_details
    except Exception as e:
        print(f"Failed to fetch carbon emission management data: {e}")
        raise

async def resource_usage_efficiency(vectorstore):
    try:
        query = rag_query['resource_usage_efficiency']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        resource_usage_details = await fetch_resource_usage_efficiency(relevant_chunks)
        print("Resource usage efficiency data fetched successfully.")
        return resource_usage_details
    except Exception as e:
        print(f"Failed to fetch resource usage efficiency data: {e}")
        raise

async def climate_change_adaptation_risk(vectorstore):
    try:
        query = rag_query['climate_change_adaptation_risk']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        climate_change_details = await fetch_climate_change_adaptation_risk(relevant_chunks)
        print("Climate change adaptation risk data fetched successfully.")
        return climate_change_details
    except Exception as e:
        print(f"Failed to fetch climate change adaptation risk data: {e}")
        raise

async def waste_management_pollution_control(vectorstore):
    try:
        query = rag_query['waste_management_pollution_control']
        relevant_chunks = await find_relevant_chunks(query, vectorstore, top_n=5)
        waste_management_details = await fetch_waste_management_pollution_control(relevant_chunks)
        print("Waste management and pollution control data fetched successfully.")
        return waste_management_details
    except Exception as e:
        print(f"Failed to fetch waste management and pollution control data: {e}")
        raise



async def get_environmental_data(vectorstore):
    try:
        
        # Gather the results of all tasks concurrently
        results = await asyncio.gather(
            carbon_emission_management(vectorstore),
            resource_usage_efficiency(vectorstore),
            climate_change_adaptation_risk(vectorstore),
            waste_management_pollution_control(vectorstore),
            environmental_impact(vectorstore)
        )
        
        # Assign each result to corresponding variables
        carbon_emission_data, resource_usage_data, climate_change_data, waste_management_data, environmental_impact_data = results

        environmental_data = {
            "carbon_emission_data": carbon_emission_data,
            "resource_usage_data": resource_usage_data,
            "climate_change_data": climate_change_data,
            "waste_management_data": waste_management_data,
            "environmental_impact_data": environmental_impact_data
        }

        print("Environmental data fetched successfully.")
        return environmental_data
    
    except Exception as e:
        print(f"Failed to fetch environmental data: {e}")
        raise
