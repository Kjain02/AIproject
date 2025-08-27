import sys
import os
sys.path.append(os.path.abspath("../../.."))
sys.path.append(os.path.abspath("../"))

print (sys.path)


from src.azure_credentials import *
from openai import AsyncAzureOpenAI
import json
import tiktoken


import asyncio





async def llm_generate(all_chunks, tool_template, system_prompt, user_prompt):
    tools = tool_template
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    concatenated_text = "\n\n".join(all_chunks)
    user_message = {
        "role": "user",
        "content": (
            f"{user_prompt}\n{concatenated_text}"
        )
    }
    messages.append(user_message)

    # count the number of tokens in the user message
    encoding = tiktoken.encoding_for_model("gpt-4o-turbo")
    total_message = system_prompt + user_prompt + concatenated_text
    tokens = encoding.encode(total_message)
    print(f"Number of tokens in user message: {len(tokens)}")


    chat_model = AsyncAzureOpenAI(
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )


    try:
        response = await chat_model.chat.completions.create(
            model=AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": tool_template[0]["function"]["name"]}},
        )
        response = response.choices[0].message.tool_calls[0].function.arguments
        return json.loads(response)
    except Exception as e:
        print(f"An error occurred: {e}")
        
        return []

