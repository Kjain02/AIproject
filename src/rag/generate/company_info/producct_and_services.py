import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def company_products_services(all_chunks):
    """
    Queries the Azure OpenAI GPT-35 API with all relevant chunks concatenated to extract the company products and services.
    """

    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are a corporate analyst with expertise in summarizing the products and services of companies. "
                "Your task is to extract and write a concise, detailed description of a company's core products and services. "
                "Highlight the main offerings, solutions, and key business verticals, including any innovations, technologies, or platforms if relevant. "
                "Include information about how these offerings help clients achieve business goals globally. "
                "Avoid any headings or introductory labels—directly start with the core details of the company's offerings."
                "Ensure the description is between 150 and 170 words, and is clear, easy-to-read, and well-structured."
            )
        }
    ]

    # Concatenate the chunks into a single string
    concatenated_text = "\n".join(all_chunks)

    # Prepare the user message
    user_message = {
        "role": "user",
        "content": (
            f"Based on the following text, provide a detailed and concise summary of the company's products and services, "
            f"including key offerings, solutions, business verticals, and any innovations or technologies used. "
            f"Ensure the response is between 150 to 170 words, and avoid any headings or labels:\n\n{concatenated_text}"
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

        # Extract the products and services details from the response
        products_services = response.choices[0].message.content

        return products_services

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Interface function exposed to other modules

async def fetch_company_products_services(relevant_chunks):
    """
    Extract the company's product and service offerings from the relevant text chunks.
    """

    # Call the query function once with all relevant chunks
    products_services_details = await company_products_services(relevant_chunks)

    if not products_services_details:
        return {}

    return products_services_details
