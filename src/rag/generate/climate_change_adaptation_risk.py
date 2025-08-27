import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of the company's climate change adaptation and risk mitigation"

async def climate_change_adaptation_risk_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the climate change adaptation and risk mitigation details.
    """

    # Define the function schema for extracting climate change adaptation and risk mitigation details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "climate_change_adaptation_risk",
                "description": "Extracts the company's climate change adaptation and risk mitigation details from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "climate_related_financial_impact": {
                            "type": "string",
                            "description": "Climate-related financial impact (in base currency)"
                        },
                        "investment_in_climate_risk_mitigation": {
                            "type": "string",
                            "description": "Investment in climate risk mitigation (in base currency)"
                        },
                        "number_of_climate_risks_identified": {
                            "type": "string",
                            "description": "Number of climate-related risks identified"
                        },
                        "expenditure_on_infrastructure_adaptation": {
                            "type": "string",
                            "description": "Expenditure on infrastructure adaptation to climate change (in base currency)"
                        }
                    },
                    "required": [
                        "climate_related_financial_impact",
                        "investment_in_climate_risk_mitigation",
                        "number_of_climate_risks_identified",
                        "expenditure_on_infrastructure_adaptation"
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
                "You are an environmental analyst. Extract the company's climate change adaptation and risk mitigation details from the provided text. "
                "Include information on climate-related financial impact, investment in climate risk mitigation, number of climate-related risks identified, and expenditure on infrastructure adaptation. "
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
            f"Extract the company's climate change adaptation and risk mitigation details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "climate_change_adaptation_risk"}},
        )

        # Extract the climate change adaptation and risk mitigation details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            climate_risk_details = function_data
            return climate_risk_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_climate_change_adaptation_risk(relevant_chunks):
    """
    Extract the company's climate change adaptation and risk mitigation details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    climate_risk_details = await climate_change_adaptation_risk_query(relevant_chunks)

    if not climate_risk_details:
        return {}

    return climate_risk_details
