import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def board_structure_independence_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the board structure and independence details.
    """

    # Define the function schema for extracting board structure and independence details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "board_structure_independence",
                "description": "Extracts the company's board structure and independence details from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_board_members": {
                            "type": "string",
                            "description": "Total number of board members"
                        },
                        "percentage_independent_board_members": {
                            "type": "string",
                            "description": "Percentage of independent board members"
                        },
                        "average_board_member_tenure": {
                            "type": "string",
                            "description": "Average tenure of board members (years)"
                        },
                        "gender_ethnic_diversity": {
                            "type": "object",
                            "properties": {
                                "percentage_gender_diverse_board_members": {
                                    "type": "string",
                                    "description": "Percentage of female board members"
                                },
                                "percentage_ethnically_diverse_board_members": {
                                    "type": "string",
                                    "description": "Percentage of board members from diverse ethnic backgrounds"
                                }
                            },
                            "required": ["percentage_gender_diverse_board_members", "percentage_ethnically_diverse_board_members"],
                            "additionalProperties": False
                        }
                    },
                    "required": [
                        "number_of_board_members",
                        "percentage_independent_board_members",
                        "average_board_member_tenure",
                        "gender_ethnic_diversity"
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
                "You are a corporate governance analyst. Extract the company's board structure and independence details from the provided text. "
                "Include information on the total number of board members, percentage of independent board members, average tenure, and gender and ethnic diversity statistics. "
                "If any of these values are not available, return 'N/A' instead of 0."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's board structure and independence details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "board_structure_independence"}},
        )

        # Extract the board structure and independence details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            board_structure_details = function_data
            return board_structure_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_board_structure_independence(relevant_chunks):
    """
    Extract the company's board structure and independence details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    board_structure_details = await board_structure_independence_query(relevant_chunks)

    if not board_structure_details:
        return {}

    return board_structure_details
