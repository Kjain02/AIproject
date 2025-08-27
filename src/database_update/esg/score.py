import asyncio
import logging
from colorlog import ColoredFormatter

from supabase import create_client, Client
from src.scoring.social_score import calculate_social_score
from src.scoring.environment_score import calculate_environmental_score
from src.scoring.governance_score import calculate_governance_score
from src.scoring.aggreagated_scores import calculate_esg_scorecard
from src.config import config


# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

url: str = "https://vuxvzlnwphczonlmagcr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1eHZ6bG53cGhjem9ubG1hZ2NyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNTk0OTk4NSwiZXhwIjoyMDQxNTI1OTg1fQ.41kfakfDnIpK9yyf2enpYzelRD4uGXAN4mIzDemsANM"
supabase: Client = create_client(url, key)

async def read_extracted_data(isn, year):
    try:
        result = await asyncio.to_thread(
            lambda: supabase.table(config["EXTRACTED_DATA_TABLE"])
            .select("esg_factors")
            .eq("isn", isn)
            .eq("year", year)
            .execute()
        )
        print("Extracted data read successfully from Supabase.")
        return result
    except Exception as e:
        print(f"Failed to read extracted data: {e}")
        raise

async def update_score_table_db(isn, year, strategy_id, score):
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

async def update_score_table(isn, year):
    try:
        extracted_data, count = await read_extracted_data(isn, year)
        if isinstance(extracted_data, tuple) and len(extracted_data) > 1:
            esg_data = extracted_data[1][0].get('esg_factors', {})
            
            print("Starting Score Aggregation...")

            environment_score = await calculate_environmental_score(esg_data)
            social_score = await calculate_social_score(esg_data)
            governance_score = await calculate_governance_score(esg_data)
            
            esg_score = {
                "environment_score": environment_score,
                "social_score": social_score,
                "governance_score": governance_score
            }

            total_esg_score = calculate_esg_scorecard(esg_score)
            print(f"ESG score: {esg_score}")
            
            score = {
                "esg_score": esg_score,
                "total_esg_score": total_esg_score
            }

            try:
                await update_score_table_db(isn, year, "default", score)
            except Exception as e:
                print(f"Failed to update score table in Supabase: {e}")
                raise
        else:
            logger.warning("No ESG data found.")
    except Exception as e:
        print(f"An error occurred while updating score table: {e}")
        raise
