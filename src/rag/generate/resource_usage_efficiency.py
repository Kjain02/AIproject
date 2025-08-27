import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def resource_usage_efficiency_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the resource usage and efficiency details.
    """

    # Define the function schema for extracting resource usage and efficiency details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "resource_usage_efficiency",
                "description": "Extracts the resource usage and efficiency details from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "energy_consumption": {
                            "type": "string",
                            "description": "Total energy consumption (in MWh or GJ)"
                        },
                        "percentage_renewable_energy": {
                            "type": "string",
                            "description": "Percentage of renewable energy used"
                        },
                        "water_usage_per_unit": {
                            "type": "string",
                            "description": "Water usage (cubic meters per production unit)"
                        },
                        "material_efficiency_ratio": {
                            "type": "string",
                            "description": "Material efficiency (input vs. output ratio)"
                        },
                        "waste_vs_recycled": {
                            "type": "object",
                            "properties": {
                                "total_waste_generated": {
                                    "type": "string",
                                    "description": "Waste generated (in tons)"
                                },
                                "recycled_waste_percentage": {
                                    "type": "string",
                                    "description": "Percentage of waste recycled"
                                }
                            }
                        }
                    },
                    "required": ["energy_consumption", "percentage_renewable_energy", "water_usage_per_unit", "material_efficiency_ratio", "waste_vs_recycled"],
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
                "You are an expert environmental analyst. Extract the resource usage and efficiency details from the provided text. "
                "Include information on energy consumption, percentage of renewable energy used, water usage per unit, material efficiency ratio, and waste management details. "
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
            f"Extract the company's resource usage and efficiency details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "resource_usage_efficiency"}},
        )

        # Extract the resource usage and efficiency details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            resource_details = function_data
            return resource_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_resource_usage_efficiency(relevant_chunks):
    """
    Extract the company's resource usage and efficiency details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    resource_details = await resource_usage_efficiency_query(relevant_chunks)

    if not resource_details:
        return {}

    return resource_details
