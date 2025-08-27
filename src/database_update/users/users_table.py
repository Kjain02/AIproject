import asyncio
import logging
import json

from src.services.board_members import get_board_member_info
from src.services.environmental import get_environmental_data
from src.services.governance import get_governance_data
from src.services.social import get_social_data
from src.rag.create import instantiate_vectorstore
from colorlog import ColoredFormatter

from src.rag.template_query import rag_query
from src.rag.new_generate.function_call import llm_generate
from src.rag.new_generate.template import general
from src.rag.query import find_relevant_chunks
from src.scoring.social_score import calculate_social_score
from src.scoring.environment_score import calculate_environmental_score
from src.scoring.governance_score import calculate_governance_score
from src.scoring.aggreagated_scores import calculate_esg_scorecard
from src.db import update_user_table_entry
import datetime


OUTPUT_DIR = "output"

# Configure logging with color and styling
log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s"
formatter = ColoredFormatter(log_format)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def get_company_name(vectorstore):
    try:
        query = """Find the full legal name of the company, including any subsidiaries or affiliated entities. This information is essential for
                identifying the company accurately and ensuring that the details provided are specific to the correct organization.
                Additionally, extract the year for which this financial report is being made to determine the reporting period covered.
                """
        relevant_chunks = await find_relevant_chunks(query, vectorstore)
        tool_template = general['company_name']['tool_call']
        system_prompt = general['company_name']['system_prompt']
        user_prompt = general['company_name']['user_prompt']
        response = await llm_generate(relevant_chunks, tool_template, system_prompt, user_prompt) 
        return response
    except Exception as e:
        print(f"Failed to get company name: {e}")
        raise



async def update_user_table(filename,file_id, user_id):
    try:
        try:
            vectorstore = await instantiate_vectorstore(filename)
            print(f"Vectorstore instantiated successfully.")
        except Exception as e:
            print(f"Failed to instantiate vectorstore: {e}")
            raise
        
        company = await get_company_name(vectorstore)
        # company_name = json.loads(company_name)

        print(company)

        company_name = company['name']
        company_year = company['year']
        print(f"Company name extracted successfully: {company_name}")
        # try:

        #     results = await asyncio.gather(
        #         get_environmental_data(vectorstore),
        #         get_social_data(vectorstore),
        #         get_governance_data(vectorstore)
        #     )
        #     env_data, soc_data, gov_data = results

        #     esg_factors = {
        #         "environmental": env_data,
        #         "social": soc_data,
        #         "governance": gov_data
        #     }
        #     print("ESG factors extracted successfully.")
        # except Exception as e:
        #     print(f"Failed to extract ESG factors: {e}")
        #     raise

        # try:
        #     esg_details = {
        #         "environmental": "",
        #         "social": "",
        #         "governance": {
        #             "board_members": await get_board_member_info(vectorstore)
        #         }
        #     }
        #     print("Board Member information extracted successfully.")
        # except Exception as e:
        #     print(f"Failed to extract Board Member details: {e}")
        #     raise

        # download_data = {}
        # download_data["extracted"] = {
        #     "esg_factors": esg_factors,
        #     "esg_details": esg_details,
        # }

        # environment_score = await calculate_environmental_score(esg_factors)
        # social_score = await calculate_social_score(esg_factors)
        # governance_score = await calculate_governance_score(esg_factors)
        # esg_score = {
        #         "environment_score": environment_score,
        #         "social_score": social_score,
        #         "governance_score": governance_score
        #     }
        # total_esg_score = calculate_esg_scorecard(esg_score)
        # print(f"Calculated the ESG Score for {company_name}: {total_esg_score}")

        # download_data["score"] = {
        #     "esg_score": esg_score,
        #     "total_esg_score": total_esg_score
        # }

        # isin_file = {}
        # isin_file["file_id"] = file_id
        # isin_file["name"] = company_name
        # isin_file["status"] = "Completed"
        # isin_file["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # isin_file["url"] = url

        # company_file = isin_file
        # company_file["download_data"] = download_data


        await update_user_table_entry(user_id, company_name, file_id)
        return vectorstore, company_year
    except Exception as e:
        print(f"Failed to update extracted table: {e}")
        raise
