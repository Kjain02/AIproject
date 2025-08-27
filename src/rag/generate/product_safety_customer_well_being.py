import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of the company's product safety and customer well-being initiatives"

async def product_safety_customer_well_being_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the product safety and customer well-being details.
    """

    # Define the function schema for extracting product safety and customer well-being details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "product_safety_customer_well_being",
                "description": "Extracts the company's product safety and customer well-being initiatives from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_product_recalls": {
                            "type": "string",
                            "description": "Number of product recalls"
                        },
                        "customer_satisfaction_score": {
                            "type": "string",
                            "description": "Customer satisfaction score (Net Promoter Score - NPS)"
                        },
                        "number_of_product_safety_incidents": {
                            "type": "string",
                            "description": "Number of product safety incidents reported"
                        },
                        "compliance_with_product_safety_standards": {
                            "type": "string",
                            "description": "Percentage compliance with product safety standards"
                        }
                    },
                    "required": [
                        "number_of_product_recalls",
                        "customer_satisfaction_score",
                        "number_of_product_safety_incidents",
                        "compliance_with_product_safety_standards"
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
                "You are a product safety analyst. Extract the company's product safety and customer well-being initiatives from the provided text. "
                "Include information on the number of product recalls, customer satisfaction score (NPS), number of product safety incidents reported, "
                "and percentage compliance with product safety standards. If any of these values are not available, return 'N/A' instead of 0."
            )
        },
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's product safety and customer well-being details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "product_safety_customer_well_being"}},
        )

        # Extract the product safety and customer well-being details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            product_safety_details = function_data
            return product_safety_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_product_safety_customer_well_being(relevant_chunks):
    """
    Extract the company's product safety and customer well-being details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    product_safety_details = await product_safety_customer_well_being_query(relevant_chunks)

    if not product_safety_details:
        return {}

    return product_safety_details
