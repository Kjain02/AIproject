import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of the company's diversity and inclusion efforts"

async def diversity_inclusion_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the diversity and inclusion details.
    """

    # Define the function schema for extracting diversity and inclusion details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "diversity_inclusion",
                "description": "Extracts the company's diversity and inclusion efforts from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "gender_diversity": {
                            "type": "object",
                            "properties": {
                                "percentage_female_employees": {
                                    "type": "string",
                                    "description": "Percentage of female employees"
                                },
                                "percentage_female_leadership": {
                                    "type": "string",
                                    "description": "Percentage of females in leadership roles"
                                }
                            },
                            "required": ["percentage_female_employees", "percentage_female_leadership"],
                            "additionalProperties": False
                        },
                        "racial_ethnic_diversity": {
                            "type": "object",
                            "properties": {
                                "percentage_diverse_employees": {
                                    "type": "string",
                                    "description": "Percentage of employees from diverse racial/ethnic backgrounds"
                                },
                                "percentage_diverse_leadership": {
                                    "type": "string",
                                    "description": "Percentage of leadership from diverse racial/ethnic backgrounds"
                                }
                            },
                            "required": ["percentage_diverse_employees", "percentage_diverse_leadership"],
                            "additionalProperties": False
                        },
                        "employees_with_disabilities_percentage": {
                            "type": "string",
                            "description": "Percentage of employees with disabilities"
                        },
                        "diversity_training_hours_per_employee": {
                            "type": "string",
                            "description": "Diversity training hours per employee"
                        },
                        "pay_equity_ratio": {
                            "type": "string",
                            "description": "Pay equity ratio (gender pay gap)"
                        }
                    },
                    "required": [
                        "gender_diversity",
                        "racial_ethnic_diversity",
                        "employees_with_disabilities_percentage",
                        "diversity_training_hours_per_employee",
                        "pay_equity_ratio"
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
                "You are an HR analyst. Extract the company's diversity and inclusion efforts from the provided text. "
                "Include information on gender diversity, racial/ethnic diversity, employees with disabilities, diversity training, and pay equity. "
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
            f"Extract the company's diversity and inclusion details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "diversity_inclusion"}},
        )

        # Extract the diversity and inclusion details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            diversity_inclusion_details = function_data
            return diversity_inclusion_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_diversity_inclusion(relevant_chunks):
    """
    Extract the company's diversity and inclusion details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    diversity_inclusion_details = await diversity_inclusion_query(relevant_chunks)

    if not diversity_inclusion_details:
        return {}

    return diversity_inclusion_details
