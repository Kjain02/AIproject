import os, sys
import PyPDF2
import asyncio

sys.path.append(os.path.abspath(".."))

from src.rag.create import read_pdf
from src.db import read_gri_extraction_table
from src.azure_credentials import *
from openai import AsyncAzureOpenAI

from prompts import system_prompt, user_prompt, tool_template
import json
import math
import tiktoken


standard_dict = {
    "value": "VALUE",
    "source": "SOURCE",
    "explanation": "EXPLANATION",
    "unit": "UNIT",
}


global total_input_tokens
global total_output_tokens

total_input_tokens = 0
total_output_tokens = 0

def donotmatchstandard_dict(d:dict):
    """
    Check if the dictionary does not match the standard dictionary Keys.
    
    Args:
        d (dict): The dictionary to check.
    
    Returns:
        bool: True if the dictionary does not match the standard dictionary Keys, False otherwise.
    """
    for key, value in standard_dict.items():
        if key not in d:
            return True
    return False


def split_dict(d):
    """
    Split a nested dictionary into a list of dictionaries,
    where each dictionary contains one top-level key and its associated value.
    
    Args:
        d (dict): The dictionary to split.
    
    Returns:
        list: A list of dictionaries split as per the structure.
    """
    result = []
    
    for key, value in d.items():
        if isinstance(value, dict):

            # If there are no dictionary inside value dictionary
            if not any(isinstance(v, dict) for v in value.values()):
                result.append({key: value})
                continue

            # If the value is a recursive dictionary, recursively process it
            nested_result = split_dict(value)
            # Add the result back as a sub-dictionary under the current key
            for nested_dict in nested_result:
                result.append({key: nested_dict})
        else:
            # If it's not a dictionary, just include the key-value pair
            result.append({key: value})
    
    return result


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

    chat_model = AsyncAzureOpenAI(
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    input_token = sum(len(encoding.encode(message["content"])) for message in messages)
    # try:
    completion = await chat_model.chat.completions.create(
        model=AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME,
        messages=messages,
        # tools=tools,
        # tool_choice={"type": "function", "function": {"name": tool_template[0]["function"]["name"]}},
        temperature=0,
        logprobs=True,
        max_tokens=1,
        # top_logprobs=10,

    )
    output_token = len(encoding.encode(completion.choices[0].message.content))

    global total_input_tokens
    global total_output_tokens

    total_input_tokens += input_token
    total_output_tokens += output_token

    print(f"Input Tokens: {input_token}, Output Tokens: {output_token}")

    choice = completion.choices[0]
    confidence = math.exp(choice.logprobs.content[0].logprob)
    response = choice.message.content

    print(response, confidence)

    if response == "True":
        return {"confidence_score": confidence}

    elif response == "False":
        return {"confidence_score": 1 - confidence}
    else:
        print("Invalid response")
        return {"confidence_score": 0}


    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return []



async def other_llm_response(response_page: tuple, response_dict: dict):
    """
    Get the confidence score of the response from the LLM model.
    
    Args:
        response_page (tuple): The page text of the response.
        response_dict (dict): The dictionary containing the response.
    
    Returns:
        dict: The confidence score of the response.
    """

    page_text = response_page[1]

    

    # print(system_prompt)
    # print(user_prompt(page_text, response_dict))



    return await llm_generate([page_text], tool_template, system_prompt, user_prompt(page_text, response_dict))
    


def merge_dicts(dict1, dict2):
    merged = dict1.copy()  # Create a copy of dict1 to avoid modifying the original
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)  # Recursively merge if both values are dictionaries
        else:
            merged[key] = value  # Otherwise, simply set the value
    return merged

    

async def validation_function(file_path: str):
    res = await read_gri_extraction_table(101)
    res = res['extraction']

    # Extract pdf text
    print("length of res", len(res))
    pages = read_pdf(file_path)


    # Check Type of res
    if not isinstance(res, list):
        res = [res]
    
    # res = res[1:2]

    updated_results = []
    for entry in res:

        result_dict = {}

        if not isinstance(entry, dict):
            print(f"Entry is not a dictionary: {entry}")
            raise Exception("Entry is not a dictionary")
        
        # Flatten the dictionary
        flat_entry = split_dict(entry)
        
        for flat_dict in flat_entry:
            # Get the inner most dictionary
            # print(flat_dict)
            inner_dict = flat_dict
            while isinstance(inner_dict, dict):
                if not any(isinstance(v, dict) for v in inner_dict.values()):
                    break
                inner_dict = list(inner_dict.values())[0]
                
            
            if donotmatchstandard_dict(inner_dict):
                continue

            
            # temp_dict = flat_dict
            # path_list = []
            # while any(isinstance(v, dict) for v in temp_dict.values()):
            #     path_list.append(list(temp_dict.keys())[0])
            #     temp_dict = list(temp_dict.values())[0]
            
            # for dict_location in path_list:
            #     flat_dict = flat_dict[dict_location]

            # print(inner_dict['source'])

            try:
                if inner_dict['source'] == "N/A":
                    continue
                current_page = pages[int(inner_dict['source']) - 1]
            except Exception as e:
                print(f"Failed to get page number: {e}, source: {inner_dict['source']}")
                raise
            confidence_score_json = await other_llm_response(current_page, flat_dict)
            print(confidence_score_json)
            
            inner_dict['confidence_score'] = confidence_score_json['confidence_score']
            # inner_dict['validation_remarks'] = confidence_score_json['validation_remarks']

            # print(flat_dict)

            result_dict = merge_dicts(result_dict, flat_dict)

            
        updated_results.append(result_dict)

        # print(result_dict)
        # print('\n\n')

    with open("data/updated_results2.json", "w") as f:
        json.dump(updated_results, f, indent=4)

    
    print(f"Total Input Tokens: {total_input_tokens}")
    print(f"Total Output Tokens: {total_output_tokens}")

    return updated_results



            





if __name__ == "__main__":
    asyncio.run(validation_function("data/tcs.pdf"))
        

