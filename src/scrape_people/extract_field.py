import json
import os
import time
import numpy as np
import PyPDF2
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI as AsyncAzureOpenAI
from langchain.docstore.document import Document
import asyncio
from azure_credentials import *
import random
from openai import AzureOpenAI

async def gpt_extract_field(chunk, person_name):
    """
    Queries the Azure OpenAI GPT-35 API with the most relevant chunk and the input query using few-shot prompting.
    """

    # Define few-shot examples
    examples = [
        {
            "role": "user",
            "content": "Extract details about the person from the following text:\nJohn Doe is the CEO of ABC Corp with 20 years of experience in finance and banking. He holds an MBA from Stanford University."
        },
        {
            "role": "assistant",
            "content": json.dumps({
                "name": "John Doe",
                "designation": "CEO of ABC Corp",
                "educational_background": "MBA from Stanford University",
                "years_experience_same_industry": 20,
                "expertise": ["Finance", "Banking"]
            })
        },
        {
            "role": "user",
            "content": "Extract details about the person from the following text:\nJane Smith is a leading researcher at XYZ Institute with a PhD in Molecular Biology. She has over 15 years of experience in genetic research and has published numerous papers on the subject."
        },
        {
            "role": "assistant",
            "content": json.dumps({
                "name": "Jane Smith",
                "designation": "Leading Researcher at XYZ Institute",
                "educational_background": "PhD in Molecular Biology",
                "years_experience_same_industry": 15,
                "expertise": ["Genetic Research", "Molecular Biology"]
            })
        }
    ]

    # Define the system prompt and user query
    system_prompt = {
        "role": "system",
        "content": "You are an expert document analyzer. Use the supplied tools and examples to extract comprehensive and accurate information about a person from the provided text. If any field is not found, omit it from the response. Do not return any placeholder or incorrect values."
    }

    # Combine the system prompt, examples, and actual user query
    messages = [system_prompt] + examples + [
        {
            "role": "user",
            "content": f"You are given some text about {person_name}. Extract details about the person from the following text:\n{chunk}"
        }
    ]

    # Define the tools (functions) for extracting board details
    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_person_details",
                "description": "Extracts comprehensive details about a person from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The full name of the person, as mentioned in the document. This field is essential for identifying the individual.",
                        },
                        "designation": {
                            "type": "string",
                            "description": "The specific designation or role held by the person in the current organization. This description should include the full title and any relevant responsibilities.",
                        },
                        "age": {
                            "type": "integer",
                            "description": "The current age of the person, if mentioned. This should be an accurate representation based on the provided text.",
                        },
                        "gender": {
                            "type": "string",
                            "description": "The gender of the person as identified in the text. Ensure that this field is only included if explicitly stated.",
                        },
                        "remuneration": {
                            "type": "string",
                            "description": "Details about the remuneration or compensation package of the person in the current organization. Include specifics such as salary, bonuses, and other forms of compensation if available.",
                        },
                        "educational_background": {
                            "type": "string",
                            "description": "A detailed summary of the person's educational qualifications, including degrees, institutions attended, and any special recognitions or honors received.",
                        },
                        "professional_background": {
                            "type": "string",
                            "description": "An overview of the person's professional history, including previous positions, organizations, and relevant achievements in those roles.",
                        },
                        "years_experience_same_industry": {
                            "type": "integer",
                            "description": "The total number of years the person has spent working within the same industry. This should be a calculated figure based on the person's career timeline.",
                        },
                        "experience_different_industry": {
                            "type": "string",
                            "description": "Information about the person's experience in different industries. This should include the nature of roles and contributions made in those industries.",
                        },
                        "expertise": {
                            "type": "array",
                            "description": "A list of specific areas of expertise the person possesses. This should be based on their educational background, professional experiences, and any recognized skills.",
                            "items": {
                                "type": "string",
                                "description": "A distinct area of expertise, such as finance, marketing, or leadership.",
                            }
                        },
                    },
                    "required": ["name"],
                    "additionalProperties": False,
                },
            }
        }
    ]

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
            tool_choice = {"type": "function", "function": {"name": "extract_person_details"}},
        )

        # Extract the board details from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            return function_data
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
