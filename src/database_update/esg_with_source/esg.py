from src.database_update.esg_with_source.environment import get_environmental_data
from src.database_update.esg_with_source.governance import get_governance_data
from src.database_update.esg_with_source.social import get_social_data
from src.rag.create import instantiate_vectorstore
import asyncio



async def get_esg_data(filepath):

    vectorstore = await instantiate_vectorstore(filepath)

    # Create coroutines for each ESG category
    social_data_task = get_social_data(vectorstore)
    governance_data_task = get_governance_data(vectorstore)
    environmental_data_task = get_environmental_data(vectorstore)

    try:
        # Run all tasks in parallel using asyncio.gather
        social_result, governance_result, environmental_result = await asyncio.gather(
            social_data_task,
            governance_data_task,
            environmental_data_task
        )

        # Return the results as a dictionary
        return {
            "social": social_result,
            "governance": governance_result,
            "environmental": environmental_result
        }
    except Exception as e:
        print(f"Failed to get ESG data: {e}")
        raise