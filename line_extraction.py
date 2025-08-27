import sys
import os

sys.path.append(os.path.abspath("/DynamicExtracter"))

from DynamicExtracter.generate_gri_template import get_generation_template

from src.rag.create import instantiate_vectorstore
from src.rag.query import find_relevant_chunks

from src.rag.new_generate.function_call import llm_generate

import json
import asyncio


def find_page_no(chunk):
    chunk = chunk.split("<page_number>")
    page_no = chunk[1]
    content = chunk[2]
    return page_no, content

async def extract_lines_from_text():
    # Generate the GRI template
    # template = await get_generation_template()

    with open("final.json", "r") as f:
        template = json.load(f)


    # Instantiate the vector store
    file_path = "src/rag/data/tcs.pdf"
    vectorstore = await instantiate_vectorstore(file_path)

    total_output = []


    for section in template:
        relevant_chunks = await find_relevant_chunks(section['rag_prompt'], vectorstore)
        tool_call = []
        section['tool_template']['function']['name'] = "function_gri_topic"
        


        content_with_page_no = {}

        print(len(relevant_chunks))

        for chunk in relevant_chunks:
            page_no, content = find_page_no(chunk)
            print(page_no,content)
            content_with_page_no[page_no] = content

        print(content_with_page_no)

        # with open("Chunks.txt", "w") as f:
        #     for page_no, content in content_with_page_no.items():
        #         f.write(f"Page No: {page_no}\n")
        #         f.write(content)
        #         f.write("\n\n")
        

        


        # print(section['tool_template']['function']['name'])
        tool_call.append(section['tool_template'])
        generated_text = await llm_generate(relevant_chunks,tool_call, section['system_prompt'], section['user_prompt'])

        print(type(generated_text))

        total_output.append(generated_text)

        break

    with open("output1.json", "w") as f:
        json.dump(total_output, f, indent=4)


if __name__ == "__main__":
    asyncio.run(extract_lines_from_text())