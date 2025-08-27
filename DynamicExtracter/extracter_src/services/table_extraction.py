# # import os
# # import camelot
# # import pandas as pd

# # def extract_tables_from_pdf(pdf_path):
# #     tables = camelot.read_pdf(pdf_path, pages='all')
# #     return tables


# # if __name__ == "__main__":
# #     tab = extract_tables_from_pdf('../documents/brsr-form.pdf')

# #     ans = ""
# #     for i, table in enumerate(tab):
# #         ans += f"Table {i+1}\n"
# #         ans += table.df.to_string()
# #         ans += "\n\n"

# #     with open('tables.txt', 'w') as f:
# #         f.write(ans)


# import re
# import fitz
# import sys
# import os
# sys.path.append(os.path.abspath("../../.."))
# from PyPDF2 import PdfReader

# print(sys.path)

# from src.rag.new_generate.function_call import llm_generate


# tool_template = [
#     {
#         "type": "function",
#         "function": {
#             "name": "generate_section_metadata",
#             "description": "Divides a document into logical and semantically similar sections, generating metadata for each section including its description, name, and prompts for further extraction.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "sections": {
#                         "type": "array",
#                         "description": "List of sections identified in the policy document, each represented by metadata.",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "section_description": {
#                                     "type": "string",
#                                     "description": "A detailed description of the section's content and purpose."
#                                 },
#                                 "section_name": {
#                                     "type": "string",
#                                     "description": "The name or title of the section."
#                                 },
#                                 "system_prompt": {
#                                     "type": "string",
#                                     "description": "A detailed system prompt to guide extraction for this section."
#                                 },
#                                 "user_prompt": {
#                                     "type": "string",
#                                     "description": "A focused user prompt to provide context and extraction instructions for this section."
#                                 },
#                                 "rag_prompt": {
#                                     "type": "string",
#                                     "description": "A prompt for the RAG model to extract parameters from this section."
                                    
#                                 }
#                             },
#                             "required": ["section_description", "section_name", "system_prompt", "user_prompt"],
#                             "additionalProperties": False
#                         }
#                     }
#                 },
#                 "required": ["sections"],
#                 "additionalProperties": False
#             }
#         }
#     }
# ]


# system_prompt = """
# You are an advanced assistant tasked with analyzing a large policy document and dividing it into logical and semantically similar sections. Your role is to:
# 1. Carefully read the provided document.
# 2. Identify and extract all logical sections based on structure, content, and semantic grouping.
# 3. Note that the sections needs to be disjoint and cover all relevant content. It is important to avoid overlap between sections.
# 4. For each section, generate:
#    - A `section_name` summarizing the content.
#    - A `section_description` providing a detailed explanation of the section's purpose and content.
#    - A tailored `system_prompt` to guide the extraction of parameters from this section.
#    - A specific `user_prompt` for requesting the extraction of detailed parameters from this section.
#    - A `rag_prompt` to guide the RAG model in extracting parameters from this section.
# 5. The Some of received chunk text has been extracted from tables So make sure to include the table data in the section. 

# Ensure:
# - All sections of the document are covered.
# - Prompts are detailed, focused, and appropriate for guiding extraction tasks in subsequent calls.
# - The output is clear, comprehensive, and logically segmented.

# """ 

# user_prompt = """
# Here is a policy document. Your task is to:
# 1. Analyze the document and divide it into logical sections based on semantic similarity and structure.
# 2. For each section, provide:
#    - A `section_name` summarizing the section.
#    - A `section_description` explaining the section's purpose.
#    - A `system_prompt` to guide the extraction of parameters for that section.
#    - A `user_prompt` for extracting parameters from that section.

# Input Document: 
# """

# def extract_text_from_pdf(pdf_path):
#     # Open the PDF and extract text
#     doc = fitz.open('../documents/brsr-form.pdf')
#     text = []
#     for page in doc:
#         text.append(page.get_text())

#     # Clean the text: replace multiple empty lines with a single empty line
#     # for i in range(len(text)):
#     #     text[i] = re.sub(r'\n\s*\n', '\n', text[i])

#     # Write the cleaned text to a file
#     with open('text.txt', 'w') as f:
#         f.write(text)

#     return text

# def extract_text_from_pdf1(pdf_path):
#     reader = PdfReader(pdf_path)
#     text_chunks = [page.extract_text() for page in reader.pages]

#     with open('text1.txt', 'w') as f:
#         f.write(str(text_chunks))

#     return text_chunks


# async def generate_sections(pdf_path):
#     pdf_chunks = extract_text_from_pdf(pdf_path)

#     print(len(pdf_chunks))
    
#     templates = await llm_generate(pdf_chunks, tool_template, system_prompt, user_prompt)
#     print(templates)
#     print(type(templates))

    
#     with open('tables_sections.json', 'w') as f:
#         f.write(str(templates))

#     return templates


# import camelot
# import pdfplumber

# def extract_text_and_tables(pdf_file, output_file):
#     """
#     Extracts normal text (excluding tables) and tables from a PDF, writes both into the same file.
#     Text is followed by tables in CSV format for each page.
#     """
#     with open(output_file, "w", encoding="utf-8") as file:
#         with pdfplumber.open(pdf_file) as pdf:
#             for page_number, page in enumerate(pdf.pages, start=1):
#                 file.write(f"Page {page_number}:\n")
                
#                 # Extract and write normal text
#                 text_content = page.extract_text()
#                 if text_content:
#                     file.write(text_content.strip() + "\n")
#                 else:
#                     file.write("(No text found on this page)\n")

#                 # Extract tables and write as CSV format
#                 tables = camelot.read_pdf(pdf_file, pages=str(page_number))
#                 if tables.n > 0:
#                     for i, table in enumerate(tables, start=1):
#                         file.write(f"\nTable {i}:\n")
#                         # Convert the table to CSV (row by row)
#                         for row in table.df.values.tolist():
#                             # Remove '\n' characters from the table cells
#                             row = [str(cell).replace("\n", " ") for cell in row]
#                             file.write(",".join(map(str, row)) + "\n")

#                 file.write("\n" + "=" * 50 + "\n")

#     print(f"Data has been successfully written to {output_file}.")


import sys, os
sys.path.append(os.path.abspath("../../.."))
import pymupdf4llm
from src.azure_credentials import *

from src.rag.new_generate.function_call import llm_generate

from openai import AsyncAzureOpenAI
import json


import asyncio
        

async def pymupdf_llm(pdf_path: str):


    data = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)

    extracted_data = ""

    for entry in data:
        extracted_data += entry['text']
    
    with open("pymu_extracted_data.txt","w") as f:
        f.write(extracted_data)

    system_prompt = """The provided text contains several issues related to sequencing, duplication, and formatting of tables and textual content. To make the content structured and readable, you are required to:

1. Reorganize Table Sequence: The tables currently do not appear in logical order with respect to their descriptive textual content. Rearrange them so that each table is placed immediately after the relevant text. Ensure that the sequence aligns with the logical flow of information provided in the text.

2. Eliminate Duplication: Some tables are repeated unnecessarily. Identify and remove any duplicate instances of tables not any data. Each table should appear only once. Ensure that removing duplicates does not result in the loss of any important information, and do not remove any data which is heading or title.

3. Reformat Tables for Text Readability: Reformat the tables into a plain-text structure that is easy to read in a text-based document. Use clear delimiters or indentation to define rows and columns, ensuring that the information is presented logically and is comprehensible without relying on complex formatting. For example:

| Column 1 | Column 2 | Column 3 |  
|----------|----------|----------|  
| Data 1   | Data 2   | Data 3   |  

4. Remove Unnecessary Line Breaks: The text contains extraneous line breaks ('\n') that disrupt readability. Remove these while maintaining proper paragraph breaks and logical flow.

Your objective is to deliver a revised version of the content that is structured, concise, and readable in plain text. All tables must appear in the correct order, without duplication, and formatted clearly for human understanding."""

    tool_template = [
    {
        "type": "function",
        "function": {
            "name": "generate_section_metadata",
            "description": "The Given text has some tables which are out of sequence, Change the Sequence of tables to put them in the correct sequence and also Modify the Structure of Tables So that they Appear like tables in text",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The Given text has some tables which are out of sequence, Change the Sequence of tables in text to put them in the correct sequence and  also Modify the Structure of Tables So that they Appear like tables in text",
                    }
                },
                "required": ["content"],
                "additionalProperties": False
            }
        }
    }
]

    user_prompt = """The text I have provided has multiple issues with the sequencing of tables, duplication of data, and formatting inconsistencies. Here’s what I need you to do:

1. Fix Table Sequencing: The tables are not positioned correctly in relation to their corresponding textual descriptions. They should appear immediately after the text that explains or introduces them. Rearrange the order of tables so the information flows logically and seamlessly.

2. Remove Duplicate Tables: Some tables are repeated unnecessarily. Identify and remove any duplicate instances of tables not any data. Each table should appear only once. Ensure that removing duplicates does not result in the loss of any important information, and do not remove any data which is heading or title.

3. Reformat Tables for Clarity: Transform the tables into a text-based format that is both clean and easy to read. Use proper delimiters like pipes (|) or indentation to structure rows and columns. Each table should have clear headers and organized rows, making it accessible even in plain text format. For example:

| S. No | Particulars                  | Total (A) | Male (B) | % (B / A) | Female (C) | % (C / A) |  
|-------|------------------------------|-----------|----------|-----------|------------|-----------|  
| 1     | Permanent Employees         | 100       | 60       | 60%       | 40         | 40%       |  

4. Remove Unnecessary Line Breaks: The text has excessive and unnecessary line breaks (\n) that make it harder to read. Remove these extra breaks, but retain appropriate paragraph separations where necessary for clarity.

The final output should be a clean, logically ordered, and human-readable version of the text. Ensure that the tables are well-structured, properly placed, and formatted for easy understanding in plain text."""
     

    result = ""
    cnt = 0
    for entry in data:
        res = await llm_generate(entry['text'],tool_template=tool_template,system_prompt=system_prompt,user_prompt=user_prompt)
        res = res['content']
        # print(res)
        result += str(res)
        cnt += 1
        # if cnt > 4:
        #     break

    with open("Extracted_table_sequentially.txt","w") as f:
        f.write(result)

    return "Extracted_table_sequentially.txt"


from DynamicExtracter.generate_gri_template import get_generation_template


from DynamicExtracter.extracter_src.services.file_operations import async_write_to_file
from dynamic_prompts import system_prompt, tool_template, user_prompt, generate_prompts_for_section, topic_tool_template
from DynamicExtracter.extracter_src.services.function_map import transform_to_openai_function_template
from concurrent.futures import ThreadPoolExecutor

file_writer_executor = ThreadPoolExecutor()

async def process_topic(pdf_path, section, pdf_chunks, tool_template, file_writer_executor):
    # Generate system and user prompts for the section
    sys_prompt, user_prompt = generate_prompts_for_section(section["section_name"], section["section_description"])
    
    # Simulated API call - replace `llm_generate` with your actual async API call implementation
    params = await llm_generate(pdf_chunks, tool_template, sys_prompt, user_prompt)
    
    # Create a sanitized section name for file saving
    section_name = section["section_name"].replace(" ", "_")
    
    pdf_name = pdf_path.split("/")[-1].split(".")[0]

    # Save the results in a section-specific JSON file
    output_path = f"extracter_src/output/pipeline_2/section_wise_params/{pdf_name}/{section_name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    await async_write_to_file(output_path,params, file_writer_executor)
    
    return params



async def process_one_topic(pdf_path, section, thread_pool_executor):
    pdf_chunks = open(pdf_path, "r")
    params = await process_topic(pdf_path, section, pdf_chunks, topic_tool_template, thread_pool_executor)
    return params

async def extract_dynamic_contents(pdf_path, thread_pool_executor):
    # Extract text chunks from PDF
    pdf_chunks = open(pdf_path ,"r")

    pdf_path = pdf_path.split("/")[-1].split(".")[0]

    # Call the LLM to generate function templates
    templates = await llm_generate(pdf_chunks, tool_template, system_prompt, user_prompt)
    result_path = f"dynamic_results/sections/{pdf_path}.json"

    await async_write_to_file(result_path, templates, thread_pool_executor)
    
    print(f"Template written to {result_path}")

    return templates

async def get_dynamic_generation_template(pdf_path : str):

    sections = await extract_dynamic_contents(pdf_path, file_writer_executor)
    
    sections = sections['sections']

    # params = await process_all_sections(PDF_PATH, sections, file_writer_executor)

    all_section_template = []


    final_template = []
    for section in sections:
        section_params = await process_one_topic(pdf_path, section, file_writer_executor)

        print("THIS IS THE SECTION PARAMS: ", section_params)
        print("\n\n")


        final_template.append({
            "system_prompt": section['system_prompt'],
            "user_prompt": section['user_prompt'],
            "rag_prompt": section['rag_prompt'],
            "tool_template": transform_to_openai_function_template(section_params)
        })

    with open('final1.json', 'w') as f:
        json.dump(final_template, f, indent = 4)
    return final_template

async def dynamic_pipeline(pdf_path : str):
    

    template = await get_dynamic_generation_template(pdf_path)

    return template
    


if __name__ == "__main__":
    # asyncio.run(generate_sections('../documents/brsr-form.pdf'))
    # extract_text_from_pdf1('../documents/brsr-form.pdf')
    # extract_text_and_tables("../documents/brsr-form.pdf", "extracted_data.txt")
    # path = asyncio.run(pymupdf_llm("../documents/brsr-form.pdf"))
    asyncio.run(dynamic_pipeline("Extracted_table_sequentially.txt"))

