import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def company_awards_recognition(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the company's awards and recognition.
    """

    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are a corporate analyst with expertise in summarizing awards and recognitions for companies. "
                "Your task is to extract and write a concise but detailed summary of the company's awards and recognitions. "
                "Highlight major accolades, industry awards, prestigious rankings, and recognitions in areas such as business performance, "
                "innovation, sustainability, and corporate governance. "
                "Do not include any headings or labels such as 'Awards and Recognitions'—start directly with the content."
                "Ensure the response is between 100 to 150 words."
            )
        }
    ]

    # Since we are passing all chunks at once, concatenate them
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Based on the following text, provide a detailed summary of the company's awards and recognitions, "
            f"including major industry accolades, rankings, and recognitions in areas like sustainability, corporate governance, and innovation. "
            f"Ensure the response is between 100 to 150 words and starts directly with the awards, without any labels:\n\n{concatenated_text}"
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

        # Extract the awards and recognition details from the response
        awards_recognition = response.choices[0].message.content

        return awards_recognition

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_company_awards_recognition(relevant_chunks):
    """
    Extract the company's awards and recognitions from the relevant text chunks.
    """

    # Call the query function once with all relevant chunks
    awards_recognition_details = await company_awards_recognition(relevant_chunks)

    if not awards_recognition_details:
        return {}

    return awards_recognition_details
