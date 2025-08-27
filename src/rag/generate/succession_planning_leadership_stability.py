import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of succession planning and leadership stability, including the number of leadership transitions, average tenure of senior executives, internal promotions, and external hires for executive roles."

async def succession_planning_leadership_stability_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the succession planning and leadership stability details.
    """

    # Define the function schema for extracting succession planning and leadership stability details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "succession_planning_leadership_stability",
                "description": "Extracts details of succession planning and leadership stability from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_leadership_transitions": {
                            "type": "string",
                            "description": "Number of leadership transitions (e.g., CEO, CFO)"
                        },
                        "average_tenure_senior_executives": {
                            "type": "string",
                            "description": "Average tenure of senior executives (years)"
                        },
                        "number_of_internal_promotions_to_executive_roles": {
                            "type": "string",
                            "description": "Number of internal promotions to executive roles"
                        },
                        "number_of_external_hires_for_executive_roles": {
                            "type": "string",
                            "description": "Number of external hires for executive roles"
                        }
                    },
                    "required": [
                        "number_of_leadership_transitions",
                        "average_tenure_senior_executives",
                        "number_of_internal_promotions_to_executive_roles",
                        "number_of_external_hires_for_executive_roles"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ]

    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are a corporate governance analyst. Extract the company's succession planning and leadership stability details from the provided text. "
                "Include information on the number of leadership transitions (e.g., CEO, CFO), average tenure of senior executives in years, number of internal promotions to executive roles, "
                "and number of external hires for executive roles. If any of these values are not available, return 'N/A' instead of 0."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's succession planning and leadership stability details from the following text:\n{concatenated_text}. "
            "For any missing data, return 'N/A' instead of 0."
        )
    }

    messages.append(user_message)

    chat_model = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    try:
        # Query the OpenAI Chat Completion API
        response = chat_model.chat.completions.create(
            model=AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "succession_planning_leadership_stability"}},
        )

        # Extract the succession planning and leadership stability details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            succession_planning_details = function_data
            return succession_planning_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_succession_planning_leadership_stability(relevant_chunks):
    """
    Extract the company's succession planning and leadership stability details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    succession_planning_details = await succession_planning_leadership_stability_query(relevant_chunks)

    if not succession_planning_details:
        return {}

    return succession_planning_details
