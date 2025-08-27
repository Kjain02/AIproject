import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def carbon_emissions_management_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the carbon emissions management details.
    """

    # Define the tools (functions) for extracting carbon emissions details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "carbon_emissions_management",
                "description": "Details of carbon emissions management strategies and performance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope_1_emissions": {
                            "type": "string",
                            "description": "Scope 1 emissions in metric tons CO2-equivalent"
                        },
                        "scope_2_emissions": {
                            "type": "string",
                            "description": "Scope 2 emissions in metric tons CO2-equivalent"
                        },
                        "scope_3_emissions": {
                            "type": "string",
                            "description": "Scope 3 emissions in metric tons CO2-equivalent"
                        },
                        "carbon_reduction_targets": {
                            "type": "string",
                            "description": "Summary of the company’s carbon reduction targets"
                        },
                        "carbon_offset_initiatives": {
                            "type": "string",
                            "description": "Description of any carbon offsetting activities undertaken by the company"
                        },
                        "reporting_compliance": {
                            "type": "string",
                            "description": "Is the company compliant with regulatory reporting (true/false)"
                        }
                    },
                    "required": ["scope_1_emissions", "scope_2_emissions", "scope_3_emissions"],
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
                "You are an environmental analyst. Extract the company's carbon emissions management details from the provided text. "
                "Include information on scope 1, scope 2, and scope 3 emissions, carbon reduction targets, carbon offset initiatives, and reporting compliance. "
                "If any of these values are not available, return 'N/A' instead of 0 or false."
            )
        },
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's carbon emissions management details from the following text:\n{concatenated_text}. "
            "For any missing data, return 'N/A' instead of 0 or false."
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
            tool_choice={"type": "function", "function": {"name": "carbon_emissions_management"}},
        )

        # Extract the carbon emissions details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            emissions_details = function_data
            return emissions_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


# Interface function exposed to other modules

async def fetch_carbon_emissions(relevant_chunks):
    """
    Extract the company's carbon emissions management details from the relevant text chunks.
    """

    emissions_details = await carbon_emissions_management_query(relevant_chunks)

    if not emissions_details:
        return {}

    return emissions_details
