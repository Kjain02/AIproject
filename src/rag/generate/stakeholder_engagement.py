import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI


async def stakeholder_engagement_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the stakeholder engagement details.
    """

    # Define the function schema for extracting stakeholder engagement details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "stakeholder_engagement",
                "description": "Extracts the company's stakeholder engagement efforts from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_stakeholder_meetings": {
                            "type": "string",
                            "description": "Number of stakeholder meetings held"
                        },
                        "percentage_stakeholders_consulted_in_decision_making": {
                            "type": "string",
                            "description": "Percentage of stakeholders consulted in decision-making processes"
                        },
                        "stakeholder_engagement_survey_results": {
                            "type": "string",
                            "description": "Stakeholder engagement survey satisfaction score (out of 100)"
                        },
                        "number_of_stakeholder_feedback_comments": {
                            "type": "string",
                            "description": "Number of stakeholder feedback comments disclosed"
                        }
                    },
                    "required": [
                        "number_of_stakeholder_meetings",
                        "percentage_stakeholders_consulted_in_decision_making",
                        "stakeholder_engagement_survey_results",
                        "number_of_stakeholder_feedback_comments"
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
                "You are a corporate governance analyst. Extract the company's stakeholder engagement efforts from the provided text. "
                "Include information on the number of stakeholder meetings held, percentage of stakeholders consulted in decision-making processes, "
                "stakeholder engagement survey satisfaction score out of 100, and the number of stakeholder feedback comments disclosed. "
                "If any of these values are not available, return 'N/A' instead of 0."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's stakeholder engagement details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "stakeholder_engagement"}},
        )

        # Extract the stakeholder engagement details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            stakeholder_engagement_details = function_data
            return stakeholder_engagement_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_stakeholder_engagement(relevant_chunks):
    """
    Extract the company's stakeholder engagement details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    stakeholder_engagement_details = await stakeholder_engagement_query(relevant_chunks)

    if not stakeholder_engagement_details:
        return {}

    return stakeholder_engagement_details
