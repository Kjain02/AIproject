import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI


async def community_engagement_social_responsibility_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the community engagement and social responsibility details.
    """

    # Define the function schema for extracting community engagement and social responsibility details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "community_engagement_social_responsibility",
                "description": "Extracts the company's community engagement and social responsibility initiatives from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investment_in_community_projects": {
                            "type": "string",
                            "description": "Total investment in community projects (in base currency)"
                        },
                        "employee_volunteer_hours": {
                            "type": "string",
                            "description": "Total volunteer hours contributed by employees"
                        },
                        "percentage_revenue_donated": {
                            "type": "string",
                            "description": "Percentage of revenue donated to charitable causes"
                        },
                        "number_of_beneficiaries_impacted": {
                            "type": "string",
                            "description": "Number of beneficiaries impacted by social programs"
                        }
                    },
                    "required": [
                        "investment_in_community_projects",
                        "employee_volunteer_hours",
                        "percentage_revenue_donated",
                        "number_of_beneficiaries_impacted"
                    ],
                    "additionalProperties": False,
                }
            }
        }
    ]

    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are a corporate social responsibility analyst. Extract the company's community engagement and social responsibility initiatives from the provided text. "
                "Include information on investment in community projects, employee volunteer hours, percentage of revenue donated to charitable causes, and number of beneficiaries impacted by social programs. "
                "If any of these values are not available, return 'N/A' instead of 0."
            )
        },
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's community engagement and social responsibility details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "community_engagement_social_responsibility"}},
        )

        # Extract the community engagement and social responsibility details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            community_engagement_details = function_data
            return community_engagement_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_community_engagement_social_responsibility(relevant_chunks):
    """
    Extract the company's community engagement and social responsibility details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    community_engagement_details = await community_engagement_social_responsibility_query(relevant_chunks)

    if not community_engagement_details:
        return {}

    return community_engagement_details
