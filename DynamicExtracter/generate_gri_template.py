import sys
import os
sys.path.append(os.path.abspath(".."))
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from DynamicExtracter.extracter_src.services.function_map import transform_to_openai_function_template

from DynamicExtracter.gri.gri_topics import extract_gri_topics
from DynamicExtracter.gri.gri_topic_params import process_one_topic
from DynamicExtracter.extracter_src.services.schema import generate_schema
from src.db import write_gri_template_table


VERBOSE = False

def verify_generation(final_template: list):
    for template in final_template:
    
        if 'system_prompt' not in template or not isinstance(template['system_prompt'], str):
            return False
        
        if 'user_prompt' not in template or not isinstance(template['user_prompt'], str):
            return False
        
        if 'rag_prompt' not in template or not isinstance(template['rag_prompt'], str):
            return False
        
        if 'tool_template' not in template or not isinstance(template['tool_template'], dict):

            if len(template['tool_template']) == 0:     
                return False
            else:
                for key, value in template['tool_template'].items():
                    if not isinstance(key, str) or not isinstance(value, str):
                        return False

    return True        



async def get_generation_template(job_args = [], common_args = []):

    PDF_PATH = job_args[0] if len(job_args) > 0 else None
    output_dir = common_args[0] if len(common_args) > 0 else None
    db_update = common_args[1] if len(common_args) > 1 else False
    name = job_args[1] if len(job_args) > 1 else None
    topic = job_args[2] if len(job_args) > 2 else None
    division = job_args[3] if len(job_args) > 3 else None
    id = job_args[4] if len(job_args) > 4 else None


    if PDF_PATH is None:
        print("PDF_PATH not provided.")
        return False

    file_writer_executor = ThreadPoolExecutor()
    file_name = os.path.basename(PDF_PATH)
    sections = await extract_gri_topics(PDF_PATH, file_writer_executor, f"{output_dir}/{file_name}/sections")
    
    if VERBOSE:
        print(f"Extracted GRI topics from {file_name}")
        print(f"Sections: {sections}")
        print("\n\n")

    sections = sections['sections']

    final_template = []
    schemas = []
    for section in sections:
        section_params = await process_one_topic(PDF_PATH, section, file_writer_executor, f"{output_dir}/{file_name}/sections_wise_params")


        ## Add instructons to system prompt about the generation guidelines

        extra_guildelines = '''
                            ## Generation Guidelines:
                            1. Ensure the unit is expressed as a standard, concise unit of measurement, such as "kg," "tonnes," "USD," "%," or "metric tons CO2e.
                            2. Avoid verbose strings for the unit; it should strictly represent a standard unit without descriptive phrases or full sentences.
                            3. The value of unit must not be a verbose string, it must be some standard unit of measurement.
                            5. The text will be presented in the following chunk format:  <page_number>{{page_num}}<page_number>    
                            {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ..., where the page_number is the page where the chunk is found and the text is the content of the chunk, You should report page_number as the source in integer format.
                            6. Make sure to extract the page number from this format for the source field. "
                            7. For each value, provide the page number of the chunk where the information was found as the source. "
                            8. In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
                            9. If any of these values are not available, return 'N/A' instead of 0."
                            10. If there are no values available return 'N/A', Donot Hallucinate the values."
                            '''

        section['system_prompt'] = section['system_prompt'] + extra_guildelines

        final_template.append({
            "system_prompt": section['system_prompt'],
            "user_prompt": section['user_prompt'],
            "rag_prompt": section['rag_prompt'],
            "tool_template": transform_to_openai_function_template(section_params),
            "section_name": section['section_name'],
            "section_description": section['section_description']
        })
        # schemas.append(generate_schema(section_params))

    if not verify_generation(final_template):
        print("Template generation failed.")
        print("Final Template: ", final_template)


        return False

    # Save final template to a file
    with open(f"{output_dir}/{file_name}/final_template.json", "w") as f:
        json.dump(final_template, f, indent=4)

    file_name = os.path.basename(PDF_PATH)

    if db_update:
        # Update the database
        if name is None or topic is None or division is None or id is None:
            print("Name, Topic or Division not provided.")
            return False 
        id = int(id)
        await write_gri_template_table(name, final_template, topic, division, id, schemas)

    return (True, final_template)
