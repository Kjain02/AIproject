import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def environmental_impact_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the environmental impact details.
    """

    # Define the function schema for extracting environmental impact details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "environmental_impact",
                "description": "Extracts the environmental impact details of the company's activities from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "total_carbon_footprint": {
                            "type": "string",
                            "description": "Total carbon footprint of the company in metric tons"
                        },
                        "total_energy_consumption": {
                            "type": "string",
                            "description": "Total energy consumption of the company in GWh or joules"
                        },
                        "water_usage": {
                            "type": "string",
                            "description": "Total water usage in cubic meters"
                        },
                        "air_pollutants_emitted": {
                            "type": "object",
                            "properties": {
                                "sox": {
                                    "type": "string",
                                    "description": "SOx emissions in metric tons"
                                },
                                "nox": {
                                    "type": "string",
                                    "description": "NOx emissions in metric tons"
                                },
                                "particulate_matter": {
                                    "type": "string",
                                    "description": "Particulate matter emissions in metric tons"
                                }
                            }
                        },
                        "hazardous_waste_generated": {
                            "type": "string",
                            "description": "Total hazardous waste generated in metric tons"
                        },
                        "non_hazardous_waste_generated": {
                            "type": "string",
                            "description": "Total non-hazardous waste generated in metric tons"
                        },
                        "biodiversity_impacts": {
                            "type": "string",
                            "description": "Summary of biodiversity impacts (e.g., deforestation, impacts on protected areas)"
                        }
                    },
                    "required": [
                        "total_carbon_footprint",
                        "total_energy_consumption",
                        "water_usage",
                        "air_pollutants_emitted",
                        "hazardous_waste_generated",
                        "non_hazardous_waste_generated",
                        "biodiversity_impacts"
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
                "You are an environmental analyst specializing in corporate sustainability. "
                "Your task is to extract detailed information about the environmental impact of the company's activities from the provided text. "
                "Specifically, identify and report on the total carbon footprint in metric tons, total energy consumption in GWh or joules, "
                "total water usage in cubic meters, emissions of air pollutants including SOx, NOx, and particulate matter in metric tons, "
                "total hazardous and non-hazardous waste generated in metric tons, and any impacts on biodiversity such as deforestation or effects on protected areas. "
                "If any of these values are not available, return 'N/A' instead of 0."
            )
        }
    ]

    # Concatenate all chunks into a single string
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Please extract the company's environmental impact details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "environmental_impact"}},
        )

        # Extract the environmental impact details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            environmental_impact_details = function_data
            return environmental_impact_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


async def fetch_environmental_impact(relevant_chunks):
    """
    Extract the company's environmental impact details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    environmental_impact_details = await environmental_impact_query(relevant_chunks)

    if not environmental_impact_details:
        return {}

    # Returning the details directly
    return environmental_impact_details
