import asyncio
from src.rag.new_generate.function_call import llm_generate
from src.rag.prompts.governance.audit_risk_management import audit_risk_management as audit_risk_management_data
from src.rag.prompts.governance.board_structure_independence import board_structure_independence as board_structure_independence_data
from src.rag.prompts.governance.ethical_business_practices import ethical_business_practices as ethical_business_practices_data
from src.rag.prompts.governance.executive_compensation import executive_compensation as executive_compensation_data
from src.rag.prompts.governance.shareholder_rights_transparency import shareholder_rights_transparency as shareholder_rights_transparency_data
from src.rag.prompts.governance.stakeholder_engagement import stakeholder_engagement as stakeholder_engagement_data
from src.rag.prompts.governance.succession_planning_leadership_stability import succession_planning_leadership_stability as succession_planning_leadership_stability_data

from src.rag.template_query import rag_query
from src.rag.query import find_relevant_chunks


async def call_tool(vectorstore, data, query):
    tool_call = data['tool_call']
    system_prompt = data['system_prompt']
    user_prompt = data['user_prompt']
    relevant_chunks = await find_relevant_chunks(query, vectorstore)
    response = await llm_generate(relevant_chunks, tool_call, system_prompt, user_prompt)
    return response


async def get_governance_data(vectorstore):
    audit_risk_management_query = rag_query['audit_risk_management']    
    board_structure_independence_query = rag_query['board_structure_independence']
    ethical_business_practices_query = rag_query['ethical_business_practices']
    executive_compensation_query = rag_query['executive_compensation']
    shareholder_rights_transparency_query = rag_query['shareholder_rights_transparency']
    stakeholder_engagement_query = rag_query['stakeholder_engagement']
    succession_planning_leadership_stability_query = rag_query['succession_planning_leadership_stability']

    # Create coroutines for each tool call
    audit_risk_management_data_task = call_tool(vectorstore, audit_risk_management_data, audit_risk_management_query)
    board_structure_independence_data_task = call_tool(vectorstore, board_structure_independence_data, board_structure_independence_query)
    ethical_business_practices_data_task = call_tool(vectorstore, ethical_business_practices_data, ethical_business_practices_query)
    executive_compensation_data_task = call_tool(vectorstore, executive_compensation_data, executive_compensation_query)
    shareholder_rights_transparency_data_task = call_tool(vectorstore, shareholder_rights_transparency_data, shareholder_rights_transparency_query)
    stakeholder_engagement_data_task = call_tool(vectorstore, stakeholder_engagement_data, stakeholder_engagement_query)
    succession_planning_leadership_stability_data_task = call_tool(vectorstore, succession_planning_leadership_stability_data, succession_planning_leadership_stability_query)

    try:
        # Run all tasks in parallel using asyncio.gather
        audit_risk_management_result, board_structure_independence_result, ethical_business_practices_result, executive_compensation_result, shareholder_rights_transparency_result, stakeholder_engagement_result, succession_planning_leadership_stability_result = await asyncio.gather(
            audit_risk_management_data_task,
            board_structure_independence_data_task,
            ethical_business_practices_data_task,
            executive_compensation_data_task, 
            shareholder_rights_transparency_data_task,
            stakeholder_engagement_data_task,
            succession_planning_leadership_stability_data_task
        )  

        # Return the results as a dictionary or list
        return {
            "audit_risk_management": audit_risk_management_result,
            "board_structure_independence": board_structure_independence_result,
            "ethical_business_practices": ethical_business_practices_result,
            "executive_compensation": executive_compensation_result,
            "shareholder_rights_transparency": shareholder_rights_transparency_result,
            "stakeholder_engagement": stakeholder_engagement_result,
            "succession_planning_leadership_stability": succession_planning_leadership_stability_result
        }
    except Exception as e:
        print(f"Failed to get environmental data: {e}")
        raise
