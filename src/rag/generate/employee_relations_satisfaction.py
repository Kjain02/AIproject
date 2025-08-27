import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def employee_relations_satisfaction_query(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the employee relations and satisfaction details.
    """

    # Define the function schema for extracting employee relations and satisfaction details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "employee_relations_satisfaction",
                "description": "Extracts the company's employee relations and satisfaction details from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_turnover_rate": {
                            "type": "string",
                            "description": "Employee turnover rate (percentage)"
                        },
                        "average_employee_tenure": {
                            "type": "string",
                            "description": "Average tenure of employees (years)"
                        },
                        "employee_satisfaction_score": {
                            "type": "string",
                            "description": "Employee satisfaction score (from survey results, out of 100)"
                        },
                        "number_of_employee_grievances_filed": {
                            "type": "string",
                            "description": "Number of employee grievances filed"
                        },
                        "union_membership_percentage": {
                            "type": "string",
                            "description": "Percentage of employees in labor unions"
                        }
                    },
                    "required": [
                        "employee_turnover_rate",
                        "average_employee_tenure",
                        "employee_satisfaction_score",
                        "number_of_employee_grievances_filed",
                        "union_membership_percentage"
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
                "You are an HR analyst. Extract the company's employee relations and satisfaction details from the provided text. "
                "Include information on employee turnover rate, average employee tenure, employee satisfaction score, number of employee grievances filed, and union membership percentage. "
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
            f"Extract the company's employee relations and satisfaction details from the following text:\n{concatenated_text}. "
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
            tool_choice={"type": "function", "function": {"name": "employee_relations_satisfaction"}},
        )

        # Extract the employee relations and satisfaction details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            employee_relations_details = function_data
            return employee_relations_details
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_employee_relations_satisfaction(relevant_chunks):
    """
    Extract the company's employee relations and satisfaction details from the relevant text chunks.
    """

    # Since we are passing all chunks at once, we only need to call the query function once
    employee_relations_details = await employee_relations_satisfaction_query(relevant_chunks)

    if not employee_relations_details:
        return {}

    return employee_relations_details
