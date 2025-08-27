import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def extract_board_details_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the board member details.
    """

    # Define the tools (functions) for extracting board member details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_board_details",
                "description": "Extracts a list of board members, including their names, designations, membership types, and additional details such as age, educational and professional background, years of industry experience, areas of expertise, committees, Director Identification Number (DIN), age, and gender.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "board_members": {
                            "type": "array",
                            "description": "A list of board members and their detailed information.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the board member."
                                    },
                                    "designation": {
                                        "type": "string",
                                        "description": "The role or designation of the board member."
                                    },
                                    "membership_type": {
                                        "type": "string",
                                        "description": "Type of membership: 'Non-Independent, Executive Director', 'Non-Independent, Non-Executive Director', or 'Independent, Non-Executive Director'."
                                    },
                                    "age": {
                                        "type": "string",
                                        "description": "The age of the board member. Return 'N/A' if not available."
                                    },
                                    "educational_background": {
                                        "type": "string",
                                        "description": "The educational background of the board member. Return 'N/A' if not available."
                                    },
                                    "professional_background": {
                                        "type": "string",
                                        "description": "The professional background of the board member. Return 'N/A' if not available."
                                    },
                                    "year_of_experience_in_same_industry": {
                                        "type": "string",
                                        "description": "The number of years of experience in the same industry. Return 'N/A' if not available."
                                    },
                                    "expertise": {
                                        "type": "array",
                                        "description": "The areas of expertise of the board member.",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "member_committees": {
                                        "type": "array",
                                        "description": "Committees the board member is part of.",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "din": {
                                        "type": "string",
                                        "description": "Director Identification Number (DIN) of the board member."
                                    },
                                    "gender": {
                                        "type": "string",
                                        "description": "The gender of the board member. Return 'N/A' if not available."
                                    }
                                },
                                "required": ["name", "designation", "membership_type", "age", "educational_background", "professional_background", "year_of_experience_in_same_industry", "expertise", "member_committees", "din", "gender"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["board_members"],
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
                "You are an expert corporate analyst. Extract the details of board members from the provided text. "
                "For each board member, include the name, designation, membership type, age, educational and professional background, years of industry experience, areas of expertise, committees, Director Identification Number (DIN), and gender."
                "Ensure that membership type is one of: 'Non-Independent, Executive Director', 'Non-Independent, Non-Executive Director', or 'Independent, Non-Executive Director'."
                "If any details are missing for a board member, return 'N/A' for that field."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the board members' details from the following text:\n{concatenated_text}"
        )
    }

    messages.append(user_message)

    chat_model = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    try:
        # Query the OpenAI Chat Completion API using the same function calling syntax as previous codes
        response = chat_model.chat.completions.create(
            model=AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "extract_board_details"}},
        )

        # Extract the board member details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)

            # Ensure every field is populated with 'N/A' if not present
            board_members_details = [
                {
                    "name": member.get("name", "N/A"),
                    "designation": member.get("designation", "N/A"),
                    "membership_type": member.get("membership_type", "N/A"),
                    "age": member.get("age", "N/A"),
                    "educational_background": member.get("educational_background", "N/A"),
                    "professional_background": member.get("professional_background", "N/A"),
                    "year_of_experience_in_same_industry": member.get("year_of_experience_in_same_industry", "N/A"),
                    "expertise": member.get("expertise", ["N/A"]),
                    "member_committees": member.get("member_committees", ["N/A"]),
                    "din": member.get("din", "N/A"),
                    "gender": member.get("gender", "N/A")
                }
                for member in function_data.get("board_members", [])
            ]

            return board_members_details
        else:
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Interface function exposed to other modules

async def fetch_board_details(relevant_chunks):
    """
    Extract the board members' details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    board_members_details = await extract_board_details_query(relevant_chunks)

    if not board_members_details:
        return []

    return board_members_details
