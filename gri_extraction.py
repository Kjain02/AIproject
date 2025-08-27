import sys, os
 
sys.path.append(os.path.abspath("/DynamicExtracter"))

from DynamicExtracter.generate_gri_template import get_generation_template

from src.rag.create import instantiate_vectorstore
from src.rag.query import find_relevant_chunks

from src.rag.new_generate.function_call import llm_generate

import json
import asyncio


async def get_gri_template(gri_document_path, output_path):
    job_args = [gri_document_path]
    common_args = [output_path]
    res = await get_generation_template(job_args, common_args)

    return res

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    output_path = "DynamicExtracter/extracter_src/documents_ouput"
    output = loop.run_until_complete(get_gri_template("DynamicExtracter/extracter_src/documents/GRI 302_ Energy 2016.pdf",output_path ))
    print(type(output))
    if isinstance(output, tuple):
        print("GRI Template generated successfully.")
        # print(output)
        template = output[1]
    else:
        print("GRI Template generation failed.")
        template = None
        exit()
    
    # template_path = "DynamicExtracter/extracter_src/documents_ouput/GRI 305_ Emissions 2016.pdf/final_template.json"

    # template = open(template_path, "r")

    # print(type(template))
    # print(template)
    # template = json.dumps(template)
    # print(type(template))
    file_path = "src/rag/data/tcs.pdf"
    vectorstore = loop.run_until_complete(instantiate_vectorstore(file_path))
    if not vectorstore:
        print("Vectorstore not instantiated.")
        exit()

    print("Vectorstore instantiated successfully.")

    total_output = []

    for section in template:
        print(section)
        relevant_chunks = loop.run_until_complete(find_relevant_chunks(section['rag_prompt'], vectorstore))
        tool_call = []
        section['tool_template']['function']['name'] = "function_gri_topic"

        tool_call.append(section['tool_template'])
        generated_text = loop.run_until_complete(llm_generate(relevant_chunks,tool_call ,section['system_prompt'],section['user_prompt']))
        total_output.append(generated_text)

    with open(f"{output_path}/ouput.json", "w") as f:
        json.dump(total_output, f)

        