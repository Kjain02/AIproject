import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of executive compensation, including CEO-to-employee pay ratio, total compensation for top executives, performance-based pay percentage, and median employee compensation."

async def executive_compensation_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the executive compensation details.
    """

    # Define the function schema for extracting executive compensation details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "executive_compensation",
                "description": "Extracts details of executive compensation from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ceo_to_employee_pay_ratio": {
                            "type": "string",
                            "description": "CEO-to-employee pay ratio"
                        },
                        "total_compensation_for_top_executives": {
                            "type": "string",
                            "description": "Total compensation for top executives (in base currency)"
                        },
                        "performance_based_pay_percentage": {
                            "type": "string",
                            "description": "Performance-based pay as a percentage of total executive compensation"
                        },
                        "median_employee_compensation": {
                            "type": "string",
                            "description": "Median employee compensation (in base currency)"
                        }
                    },
                    "required": [
                        "ceo_to_employee_pay_ratio",
                        "total_compensation_for_top_executives",
                        "performance_based_pay_percentage",
                        "median_employee_compensation"
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
                "You are a corporate governance analyst. Extract the company's executive compensation details from the provided text. "
                "Include information on the CEO-to-employee pay ratio, total compensation for top executives, performance-based pay percentage, "
                "and median employee compensation. If any of these values are not available, return 'N/A' instead of 0."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's executive compensation details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "executive_compensation"}},
        )

        # Extract the executive compensation details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            executive_compensation_details = function_data
            return executive_compensation_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_executive_compensation(relevant_chunks):
    """
    Extract the company's executive compensation details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    executive_compensation_details = await executive_compensation_query(relevant_chunks)

    if not executive_compensation_details:
        return {}

    return executive_compensation_details
