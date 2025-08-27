import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def labor_standards_human_rights_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the labor standards and human rights details.
    """

    # Define the function schema for extracting labor standards and human rights details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "labor_standards_human_rights",
                "description": "Extracts the company's compliance with labor standards and human rights policies from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fair_wage_percentage": {
                            "type": "string",
                            "description": "Percentage of employees receiving fair wage (compared to local living wage)"
                        },
                        "number_of_human_rights_violations": {
                            "type": "string",
                            "description": "Number of human rights violations reported"
                        },
                        "percentage_supply_chain_audits": {
                            "type": "string",
                            "description": "Percentage of supply chain audited for labor standards"
                        },
                        "child_labor_violations": {
                            "type": "string",
                            "description": "Number of child labor or forced labor incidents reported"
                        }
                    },
                    "required": [
                        "fair_wage_percentage",
                        "number_of_human_rights_violations",
                        "percentage_supply_chain_audits",
                        "child_labor_violations"
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
                "You are a human rights compliance analyst. Extract the company's compliance with labor standards and human rights policies from the provided text. "
                "Include information on fair wage percentage, number of human rights violations reported, percentage of supply chain audited for labor standards, and number of child labor or forced labor incidents reported. "
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
            f"Extract the company's labor standards and human rights details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "labor_standards_human_rights"}},
        )

        # Extract the labor standards and human rights details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            labor_standards_details = function_data
            return labor_standards_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_labor_standards_human_rights(relevant_chunks):
    """
    Extract the company's labor standards and human rights details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    labor_standards_details = await labor_standards_human_rights_query(relevant_chunks)

    if not labor_standards_details:
        return {}

    return labor_standards_details
