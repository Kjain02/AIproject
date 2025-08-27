import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of the company's ethical business practices, including the number of corruption or bribery incidents reported, anti-corruption policy compliance rate, number of whistleblower reports filed, and number of code of ethics violations."

async def ethical_business_practices_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the ethical business practices details.
    """

    # Define the function schema for extracting ethical business practices details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "ethical_business_practices",
                "description": "Extracts the company's ethical business practices from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_corruption_bribery_incidents": {
                            "type": "string",
                            "description": "Number of corruption or bribery incidents reported"
                        },
                        "anti_corruption_policy_compliance_rate": {
                            "type": "string",
                            "description": "Anti-corruption policy compliance rate (percentage of employees trained)"
                        },
                        "number_of_whistleblower_reports": {
                            "type": "string",
                            "description": "Number of whistleblower reports filed"
                        },
                        "code_of_ethics_violations": {
                            "type": "string",
                            "description": "Number of code of ethics violations"
                        }
                    },
                    "required": [
                        "number_of_corruption_bribery_incidents",
                        "anti_corruption_policy_compliance_rate",
                        "number_of_whistleblower_reports",
                        "code_of_ethics_violations"
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
                "You are a corporate governance analyst. Extract the company's ethical business practices from the provided text. "
                "Include information on the number of corruption or bribery incidents reported, anti-corruption policy compliance rate "
                "(percentage of employees trained), number of whistleblower reports filed, and number of code of ethics violations. "
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
            f"Extract the company's ethical business practices details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "ethical_business_practices"}},
        )

        # Extract the ethical business practices details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            ethical_business_practices_details = function_data
            return ethical_business_practices_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_ethical_business_practices(relevant_chunks):
    """
    Extract the company's ethical business practices details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    ethical_business_practices_details = await ethical_business_practices_query(relevant_chunks)

    if not ethical_business_practices_details:
        return {}

    return ethical_business_practices_details
