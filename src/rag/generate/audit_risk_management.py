import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of the company's audit and risk management practices, including percentage of independent audit committee members, number of financial restatements, audit fees paid, and internal control failures identified."

async def audit_risk_management_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the audit and risk management details.
    """

    # Define the function schema for extracting audit and risk management details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "audit_risk_management",
                "description": "Extracts the company's audit and risk management practices from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "percentage_independent_audit_committee_members": {
                            "type": "string",
                            "description": "Percentage of independent audit committee members"
                        },
                        "number_of_financial_restatements": {
                            "type": "string",
                            "description": "Number of financial restatements or revisions"
                        },
                        "audit_fees_paid": {
                            "type": "string",
                            "description": "Audit fees paid (in base currency)"
                        },
                        "internal_control_failures_identified": {
                            "type": "string",
                            "description": "Number of internal control failures or weaknesses identified"
                        }
                    },
                    "required": [
                        "percentage_independent_audit_committee_members",
                        "number_of_financial_restatements",
                        "audit_fees_paid",
                        "internal_control_failures_identified"
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
                "You are a corporate governance analyst. Extract the company's audit and risk management practices from the provided text. "
                "Include information on the percentage of independent audit committee members, number of financial restatements or revisions, "
                "audit fees paid, and number of internal control failures or weaknesses identified. "
                "If any of these values are not available in the text, return 'N/A' for that value instead of 0."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's audit and risk management details from the following text:\n{concatenated_text}. "
            "For any missing data, please return 'N/A' instead of 0."
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
            tool_choice={"type": "function", "function": {"name": "audit_risk_management"}},
        )

        # Extract the audit and risk management details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)

            # Return the extracted audit and risk management details
            audit_risk_management_details = function_data
            return audit_risk_management_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_audit_risk_management(relevant_chunks):
    """
    Extract the company's audit and risk management details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    audit_risk_management_details = await audit_risk_management_query(relevant_chunks)

    if not audit_risk_management_details:
        return {}

    return audit_risk_management_details
