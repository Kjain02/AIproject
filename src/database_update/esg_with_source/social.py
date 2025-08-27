from src.rag.new_generate.function_call import llm_generate
from src.rag.prompts.social.community_engagement_social_responsibility import community_engagement_social_responsibility as community_data
from src.rag.prompts.social.diversity_inclusion import diversity_inclusion as diversity_data
from src.rag.prompts.social.employee_relations_satidfaction import employee_relations_satisfaction as employee_data
from src.rag.prompts.social.health_safety_practices import health_safety_practices as health_data
from src.rag.prompts.social.labour_standards_human_rights import labour_standards_human_rights as labour_data
from src.rag.prompts.social.product_safety_customer_well_being import product_safety_customer_well_being as product_data
from src.rag.template_query import rag_query
from src.rag.query import find_relevant_chunks

import asyncio

async def call_tool(vectorstore, data, query):
    tool_call = data['tool_call']
    system_prompt = data['system_prompt']
    user_prompt = data['user_prompt']
    relevant_chunks = await find_relevant_chunks(query, vectorstore)
    response = await llm_generate(relevant_chunks, tool_call, system_prompt, user_prompt)
    return response


async def get_social_data(vectorstore):
    community_query = rag_query['community_engagement_social_responsibility']
    diversity_query = rag_query['diversity_inclusion']
    employee_query = rag_query['employee_relations_satisfaction']
    health_query = rag_query['health_safety_practices']
    labour_query = rag_query['labor_standards_human_rights']
    product_query = rag_query['product_safety_customer_well_being']

    # Create coroutines for each tool call
    community_data_task = call_tool(vectorstore, community_data, community_query)
    diversity_data_task = call_tool(vectorstore, diversity_data, diversity_query)
    employee_data_task = call_tool(vectorstore, employee_data, employee_query)
    health_data_task = call_tool(vectorstore, health_data, health_query)
    labour_data_task = call_tool(vectorstore, labour_data, labour_query)
    product_data_task = call_tool(vectorstore, product_data, product_query)

    try:
        # Run all tasks in parallel using asyncio.gather
        community_result, diversity_result, employee_result, health_result, labour_result, product_result = await asyncio.gather(
            community_data_task,
            diversity_data_task,
            employee_data_task,
            health_data_task,
            labour_data_task,
            product_data_task
        )

        # Return the results as a dictionary or list
        return {
            "community_engagement_social_responsibility": community_result,
            "diversity_inclusion": diversity_result,
            "employee_relations_satisfaction": employee_result,
            "health_safety_practices": health_result,
            "labor_standards_human_rights": labour_result,
            "product_safety_customer_well_being": product_result
        }
    except Exception as e:
        print(f"Failed to get social data: {e}")
        raise
    


