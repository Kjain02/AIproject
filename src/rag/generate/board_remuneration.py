import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def board_member_remuneration_query(board_members_groups, all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the remuneration details
    for the specified board members.
    """

    # Define the function schema for extracting remuneration details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_remuneration_details",
                "description": "Extracts the remuneration details for specified board members from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "remuneration_details": {
                            "type": "array",
                            "description": "A list of remuneration details for the specified board members.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Name of the board member. Provide 'N/A' if not present.",
                                    },
                                    "commission": {
                                        "type": "string",
                                        "description": "Commission earned by the board member. Provide 'N/A' if not present.",
                                    },
                                    "sitting_fees": {
                                        "type": "string",
                                        "description": "Sitting fees for attending meetings. Provide 'N/A' if not present.",
                                    },
                                    "salary": {
                                        "type": "string",
                                        "description": "Salary of the board member (if applicable). Provide 'N/A' if not present.",
                                    },
                                    "benefits_perquisites_allowances": {
                                        "type": "string",
                                        "description": "Benefits, perquisites, and allowances received. Provide 'N/A' if not present.",
                                    },
                                    "esps": {
                                        "type": "string",
                                        "description": "Employee Stock Purchase Scheme details (if applicable). Provide 'N/A' if not present.",
                                    },
                                    "currency": {
                                        "type": "string",
                                        "description": "Currency in which the remuneration is provided (e.g., INR, USD). Provide 'N/A' if not present.",
                                    },
                                    "unit": {
                                        "type": "string",
                                        "description": "Unit of the remuneration amounts (e.g., Lakh, Million). Provide 'N/A' if not present.",
                                    }
                                },
                                "required": ["name", "commission", "sitting_fees", "salary", "benefits_perquisites_allowances", "esps", "currency", "unit"],
                                "additionalProperties": False,
                            }
                        }
                    },
                    "required": ["remuneration_details"],
                    "additionalProperties": False,
                },
            }
        }
    ]

    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert financial analyst. Extract the remuneration details for the specified board members from the provided text. "
                "Please include the currency and unit for each remuneration amount separately. "
                "Be aware that there may be slight variations in the names of board members (e.g., abbreviations, initials, titles). "
                "Match the names as closely as possible and extract the corresponding remuneration details."
                "Currency field must be one of the following : INR, USD, GBP, EUR"
            )
        },
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    board_members = board_members_groups  

    board_member_names = ", ".join([member for member in board_members])

    user_message = {
        "role": "user",
        "content": (
            f"Extract remuneration details for the following board members from the text (consider slight variations in names):\n"
            f"{board_member_names}\n\nText to analyze:\n{concatenated_text}"
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
            tool_choice={"type": "function", "function": {"name": "extract_remuneration_details"}},
        )

        # Extract the remuneration details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            remuneration_details = function_data.get("remuneration_details", [])
            return remuneration_details
        else:
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Interface function exposed to other modules

async def fetch_bm_remuneration(relevant_chunks, board_details):
    """
    Find the most relevant board member details for the input query using the vectorstore.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    remuneration_details = await board_member_remuneration_query(board_details, relevant_chunks)

    if not remuneration_details:
        return []

    return remuneration_details
