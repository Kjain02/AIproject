import sys
import os

sys.path.append(os.path.abspath("/DynamicExtracter"))

import asyncio

from DynamicExtracter.generate_gri_template import get_generation_template
from src.rag.create import instantiate_vectorstore
from src.rag.query import find_relevant_chunks
from src.rag.new_generate.function_call import llm_generate
import json


file_path = "src/rag/data/TCS.pdf"

async def find_matching_percentage(current_data, relevant_chunks):
    """
    Calculate the percentage of relevant_chunks that is already present in current_data.

    :param current_data: List of strings representing cached data.
    :param relevant_chunks: List of strings representing relevant data to check.
    :return: current_data, Percentage of relevant_chunks present in current_data.
    """
    if not relevant_chunks:  # Avoid division by zero
        return current_data, 0.0

    # Use a set for faster lookup
    current_data_set = set(current_data)

    # Count the matches
    matches = sum(1 for chunk in relevant_chunks if chunk in current_data_set)

    # Calculate percentage
    matching_percentage = (matches / len(relevant_chunks)) * 100

    # Update the current data with the new chunks
    for chunk in relevant_chunks:
        if chunk not in current_data_set:
            current_data.append(chunk)

    return current_data, matching_percentage


async def caching_demo():

    total_output = []

    vectorstore = await instantiate_vectorstore(file_path)
    template = await get_generation_template()
    # with open("final1.json", "r") as f:
    #     template = json.load(f)

    matching_res = []
    matching_res.append(0.0)

    current_data = []

    for section in template:
        relevant_chunks = await find_relevant_chunks(section['rag_prompt'], vectorstore)
        tool_call = []
        section['tool_template']['function']['name'] = "function_gri_topic"

        print(section['tool_template']['function']['name'])
        tool_call.append(section['tool_template'])

        current_data, percentage_match_with_previous = await find_matching_percentage(current_data, relevant_chunks)
        matching_res.append(percentage_match_with_previous)

        generated_text = await llm_generate(relevant_chunks,tool_call, section['system_prompt'], section['user_prompt'])
        total_output.append(generated_text)

    with open("output1.json", "w") as f:
        json.dump(total_output, f, indent=4)

    print("Matching percentage with previous sections: ", matching_res)


if __name__ == "__main__":
    asyncio.run(caching_demo())