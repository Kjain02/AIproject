
import sys
import os
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import json
import asyncio

# Append the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


from DynamicExtracter.extracter_src.services.generate_sections import generate_sections_metadata
from DynamicExtracter.extracter_src.services.generate_params_for_section import process_one_section
from concurrent.futures import ThreadPoolExecutor
from DynamicExtracter.extracter_src.services.function_map import transform_to_openai_function_template
from DynamicExtracter.extracter_src.services.schema import generate_schema
# PDF_PATH = 'extracter_src/documents/brsr-form.pdf'

file_writer_executor = ThreadPoolExecutor()


async def get_generation_template(PDF_PATH):

    sections = await generate_sections_metadata(PDF_PATH, file_writer_executor)
    sections = sections['sections']

    final_template = []
    schemas = []

    for i in range (len(sections)):
        next_section = sections[i+1] if i+1 < len(sections) else None
        section_params = await process_one_section(PDF_PATH, sections[i], next_section, file_writer_executor)
        section = sections[i]
        section_name = section['section_name']
        # with open(f'{section_name}.json', 'w') as f:
        #     json.dump(section_params, f, indent = 4)

        final_template.append({
            "system_prompt": section['system_prompt'],
            "user_prompt": section['user_prompt'],
            "rag_prompt": section['rag_prompt'],
            "tool_template": transform_to_openai_function_template(section_params)
        })
        # schemas.append(generate_schema(section_params))
    with open('final.json', 'w') as f:
        json.dump(final_template, f, indent = 4)
    # with open('final_schema.json', 'w') as f:
    #     json.dump(schemas, f, indent = 4)

        
    # for section in sections:
    #     section_params = await process_one_section(PDF_PATH, section, file_writer_executor)
    #     section_name = section['section_name']
    #     with open(f'{section_name}.json', 'w') as f:
    #         json.dump(section_params, f, indent = 4)

    #     final_template.append({
    #         "system_prompt": section['system_prompt'],
    #         "user_prompt": section['user_prompt'],
    #         "rag_prompt": section['rag_prompt'],
    #         "tool_template": transform_to_openai_function_template(section_params)
    #     })
    #     schemas.append(generate_schema(section_params))
    # with open('final.json', 'w') as f:
    #     json.dump(final_template, f, indent = 4)
    # with open('final_schema.json', 'w') as f:
    #     json.dump(schemas, f, indent = 4)
    
    return final_template


async def main():
    print("here")

    # asyncio.run(get_generation_template('/home/somya/Documents/qnext/fin-analysis/DynamicExtracter/extracter_src/documents/brsr-form.pdf'))

    ans = await get_generation_template('/home/somya/Documents/qnext/fin-analysis/DynamicExtracter/extracter_src/documents/brsr-form.pdf')
    print(ans)


if __name__ == "__main__":
    asyncio.run(main())