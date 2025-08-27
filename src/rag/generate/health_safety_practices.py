import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def health_safety_practices_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the health and safety practices details.
    """

    # Define the function schema for extracting health and safety practices details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "health_safety_practices",
                "description": "Extracts the company's health and safety practices from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "workplace_injury_rate": {
                            "type": "string",
                            "description": "Workplace injury rate (per 1,000 employees)"
                        },
                        "ltifr": {
                            "type": "string",
                            "description": "Lost-time injury frequency rate (LTIFR)"
                        },
                        "number_of_workplace_fatalities": {
                            "type": "string",
                            "description": "Number of workplace fatalities"
                        },
                        "employee_wellness_program_participation": {
                            "type": "string",
                            "description": "Percentage of employees participating in wellness programs"
                        },
                        "safety_training_hours_per_employee": {
                            "type": "string",
                            "description": "Safety training hours per employee"
                        }
                    },
                    "required": [
                        "workplace_injury_rate",
                        "ltifr",
                        "number_of_workplace_fatalities",
                        "employee_wellness_program_participation",
                        "safety_training_hours_per_employee"
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
                "You are a health and safety analyst. Extract the company's health and safety practices from the provided text. "
                "Include information on workplace injury rate, lost-time injury frequency rate (LTIFR), number of workplace fatalities, "
                "employee wellness program participation, and safety training hours per employee. If any of these values are not available, return 'N/A' instead of 0."
            )
        },
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's health and safety practices details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "health_safety_practices"}},
        )

        # Extract the health and safety practices details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            health_safety_details = function_data
            return health_safety_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_health_safety_practices(relevant_chunks):
    """
    Extract the company's health and safety practices details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    health_safety_details = await health_safety_practices_query(relevant_chunks)

    if not health_safety_details:
        return {}

    return health_safety_details
