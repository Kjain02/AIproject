import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def waste_management_pollution_control_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the waste management and pollution control details.
    """

    # Define the function schema for extracting waste management and pollution control details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "waste_management_pollution_control",
                "description": "Extracts the company's waste management and pollution control efforts from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "total_waste_generated": {
                            "type": "string",
                            "description": "Total waste generated (in tons)"
                        },
                        "hazardous_waste": {
                            "type": "string",
                            "description": "Hazardous waste (in tons)"
                        },
                        "recycling_rate": {
                            "type": "string",
                            "description": "Recycling rate (percentage of total waste recycled)"
                        },
                        "pollutant_emissions": {
                            "type": "object",
                            "properties": {
                                "nox_emissions": {
                                    "type": "string",
                                    "description": "NOx emissions (in metric tons)"
                                },
                                "sox_emissions": {
                                    "type": "string",
                                    "description": "SOx emissions (in metric tons)"
                                },
                                "particulate_matter": {
                                    "type": "string",
                                    "description": "Particulate matter emissions (in metric tons)"
                                }
                            },
                            "required": ["nox_emissions", "sox_emissions", "particulate_matter"],
                            "additionalProperties": False,
                        }
                    },
                    "required": ["total_waste_generated", "hazardous_waste", "recycling_rate", "pollutant_emissions"],
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
                "You are an environmental analyst. Extract the company's waste management and pollution control details from the provided text. "
                "Include information on total waste generated, hazardous waste, recycling rates, and emissions of pollutants like NOx, SOx, and particulate matter. "
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
            f"Extract the company's waste management and pollution control details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "waste_management_pollution_control"}},
        )

        # Extract the waste management and pollution control details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            waste_management_details = function_data
            return waste_management_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_waste_management_pollution_control(relevant_chunks):
    """
    Extract the company's waste management and pollution control details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    waste_management_details = await waste_management_pollution_control_query(relevant_chunks)

    if not waste_management_details:
        return {}

    return waste_management_details
