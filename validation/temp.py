import os, sys

sys.path.append(os.path.abspath(".."))

from src.azure_credentials import *

from openai import AsyncAzureOpenAI
import json

import asyncio

import math

async def check_openai_api_key(api_key):
    system_prompt = "Capital Of India with Description"
    user_prompt = "Capital Of India with Description"
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    user_message = {
        "role": "user",
        "content": (
            f"{user_prompt}"
        )
    }
    messages.append(user_message)

    chat_model = AsyncAzureOpenAI(
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    print(AZURE_OPENAI_API_VERSION)
    print(AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME)
    completion = await chat_model.chat.completions.create(
        model=AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME,
        messages=messages,
        temperature=0,
        logprobs=True,
    )

    print(completion)


    choice = completion.choices[0]
    confidence = math.exp(choice.logprobs.content[0].logprob)
    return choice.message.content, confidence

print(asyncio.run(check_openai_api_key(AZURE_OPENAI_GPT_API_KEY)))










# Another Job


# import os, sys

# sys.path.append(os.path.abspath(".."))
# from src.db import read_gri_extraction_table, get_all_gri_extraction
# import asyncio

# import json



# if __name__ == "__main__":
#     lst = asyncio.run(get_all_gri_extraction())
#     print(lst)

#     ans = []
#     for i in lst:
#         temp_ans = asyncio.run(read_gri_extraction_table(i['topic_id']))
#         temp_ans = temp_ans['extraction']
        
#         for j in temp_ans:
#             # print(type(j))
#             j = json.dumps(j)
#             ans.append(j)

#     with open("gri_combined.json", "w") as f:
#         f.write(str(ans))

