import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

rag_query = "Details of shareholder rights and transparency, including voting rights per share class, shareholder proposal submission rates, number of shareholder meetings, and disclosure levels based on ESG frameworks."

async def shareholder_rights_transparency_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the shareholder rights and transparency details.
    """

    # Define the function schema for extracting shareholder rights and transparency details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "shareholder_rights_transparency",
                "description": "Extracts details of shareholder rights and transparency from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "voting_rights_per_share_class": {
                            "type": "array",
                            "description": "Details of voting rights for each class of shares",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "class_name": {
                                        "type": "string",
                                        "description": "Name of the share class"
                                    },
                                    "voting_rights": {
                                        "type": "string",
                                        "description": "Voting rights per share"
                                    }
                                },
                                "required": ["class_name", "voting_rights"],
                                "additionalProperties": False
                            }
                        },
                        "shareholder_proposal_submission_rates": {
                            "type": "string",
                            "description": "Number of shareholder proposals submitted"
                        },
                        "number_of_shareholder_meetings": {
                            "type": "string",
                            "description": "Number of shareholder meetings held"
                        },
                        "disclosure_level_based_on_esg": {
                            "type": "object",
                            "description": "Disclosure levels based on ESG frameworks",
                            "properties": {
                                "gri_disclosure": {
                                    "type": "string",
                                    "description": "Disclosure level based on GRI framework"
                                },
                                "sasb_disclosure": {
                                    "type": "string",
                                    "description": "Disclosure level based on SASB framework"
                                }
                            },
                            "required": ["gri_disclosure", "sasb_disclosure"],
                            "additionalProperties": False
                        }
                    },
                    "required": [
                        "voting_rights_per_share_class",
                        "shareholder_proposal_submission_rates",
                        "number_of_shareholder_meetings",
                        "disclosure_level_based_on_esg"
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
                "You are a corporate governance analyst. Extract the company's shareholder rights and transparency details from the provided text. "
                "Include information on voting rights per share class, shareholder proposal submission rates, number of shareholder meetings held, "
                "and disclosure levels based on ESG frameworks such as GRI and SASB. If any of these values are not available, return 'N/A' instead of 0."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's shareholder rights and transparency details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "shareholder_rights_transparency"}},
        )

        # Extract the shareholder rights and transparency details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            shareholder_rights_details = function_data
            return shareholder_rights_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_shareholder_rights_transparency(relevant_chunks):
    """
    Extract the company's shareholder rights and transparency details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    shareholder_rights_details = await shareholder_rights_transparency_query(relevant_chunks)

    if not shareholder_rights_details:
        return {}

    return shareholder_rights_details
