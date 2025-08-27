import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def company_history(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the company history.
    """

    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are a corporate governance analyst. Your task is to extract and write a concise company history. "
                "Focus only on the core historical details such as the company's founding, major milestones, key achievements, and significant expansions. "
                "Avoid unnecessary headings, introductions, or labels such as 'Company History'—just directly generate the history itself. "
                "Ensure the history is between 150 to 170 words."
            )
        }
    ]

    # Concatenate the chunks into a single string
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Extract the company's history from the following text and generate a direct, concise summary of the company's historical details. "
            f"Ensure the response directly starts with the history and is between 150 to 170 words:\n\n{concatenated_text}"
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
            messages=messages
        )

        # Extract the company history details from the response
        company_history = response.choices[0].message.content

        return company_history

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_company_history(relevant_chunks):
    """
    Extract the company's history from the relevant text chunks.
    """

    # Call the query function once with all relevant chunks
    company_history_details = await company_history(relevant_chunks)

    if not company_history_details:
        return {}

    return company_history_details
