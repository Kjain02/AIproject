import asyncio
from src.rag.new_generate.function_call import llm_generate
from src.rag.prompts.environment.carbon_emission_management import carbon_emission_management as carbon_data
from src.rag.prompts.environment.resource_usage_efficiency import resource_usage_efficiency as resource_data
from src.rag.prompts.environment.climate_change_adaptation_risk import climate_change_adaptation_risk as climate_data
from src.rag.prompts.environment.waste_management_pollution_control import waste_management_pollution_control as waste_data
from src.rag.prompts.environment.environmental_impact import environmental_impact as environmental_data

from src.rag.template_query import rag_query
from src.rag.query import find_relevant_chunks


async def call_tool(vectorstore, data, query):
    tool_call = data['tool_call']
    system_prompt = data['system_prompt']
    user_prompt = data['user_prompt']
    relevant_chunks = await find_relevant_chunks(query, vectorstore)
    response = await llm_generate(relevant_chunks, tool_call, system_prompt, user_prompt)
    return response


async def get_environmental_data(vectorstore):
    carbon_query = rag_query['carbon_emission_management']
    resource_query = rag_query['resource_usage_efficiency']
    climate_query = rag_query['climate_change_adaptation_risk']
    waste_query = rag_query['waste_management_pollution_control']
    impact_query = rag_query['environmental_impact']

    # Create coroutines for each tool call
    carbon_data_task = call_tool(vectorstore, carbon_data, carbon_query)
    resource_data_task = call_tool(vectorstore, resource_data, resource_query)
    climate_data_task = call_tool(vectorstore, climate_data, climate_query)
    waste_data_task = call_tool(vectorstore, waste_data, waste_query)
    environmental_data_task = call_tool(vectorstore, environmental_data, impact_query)

    try:
        # Run all tasks in parallel using asyncio.gather
        carbon_result, resource_result, climate_result, waste_result, environmental_result = await asyncio.gather(
            carbon_data_task,
            resource_data_task,
            climate_data_task,
            waste_data_task,
            environmental_data_task
        )

        # Return the results as a dictionary or list
        return {
            "carbon_emission_management": carbon_result,
            "resource_usage_efficiency": resource_result,
            "climate_change_adaptation_risk": climate_result,
            "waste_management_pollution_control": waste_result,
            "environmental_impact": environmental_result
        }
    except Exception as e:
        print(f"Failed to get environmental data: {e}")
        raise
