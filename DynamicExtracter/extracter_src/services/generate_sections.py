import sys
import os
sys.path.append(os.path.abspath(".."))

import json
from src.rag.new_generate.function_call import llm_generate
from DynamicExtracter.extracter_src.services.file_operations import extract_text_from_pdf, async_write_to_file


tool_template = [
    {
        "type": "function",
        "function": {
            "name": "generate_section_metadata",
            "description": "Divides a document into logical and semantically similar sections, generating metadata for each section including its description, name, and prompts for further extraction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sections": {
                        "type": "array",
                        "description": "List of sections identified in the policy document, each represented by metadata.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "section_description": {
                                    "type": "string",
                                    "description": "A detailed description of the section's content and purpose."
                                },
                                "section_name": {
                                    "type": "string",
                                    "description": "The name or title of the section."
                                },
                                "system_prompt": {
                                    "type": "string",
                                    "description": "A detailed system prompt to guide extraction for this section."
                                },
                                "user_prompt": {
                                    "type": "string",
                                    "description": "A focused user prompt to provide context and extraction instructions for this section."
                                },
                                "rag_prompt": {
                                    "type": "string",
                                    "description": "A prompt for the RAG model to extract parameters from this section."
                                    
                                }
                            },
                            "required": ["section_description", "section_name", "system_prompt", "user_prompt"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["sections"],
                "additionalProperties": False
            }
        }
    }
]


# System and user prompts
system_prompt = """
You are an advanced assistant tasked with analyzing a large policy document and dividing it into logical and semantically similar sections. Your role is to:
1. Carefully read the provided document.
2. Identify and extract all logical sections based on structure, content, and semantic grouping.
3. Note that the sections needs to be disjoint and cover all relevant content. It is important to avoid overlap between sections.
5. The division of sections must be done in a way such that number of words in a section should not exceed 500. If a section is too large, consider breaking it down further.
6. You must not make any sections too large. Make sure that the sections are granular enough to capture specific information.
7. For each section, generate:
   - A `section_name` summarizing the content.
   - A `section_description` providing a detailed explanation of the section's purpose and content.
   - A tailored `system_prompt` to guide the extraction of parameters from this section.
   - A specific `user_prompt` for requesting the extraction of detailed parameters from this section.
   - A `rag_prompt` to guide the RAG model in extracting parameters from this section.

Ensure:
- All sections of the document are covered.
- Prompts are detailed, focused, and appropriate for guiding extraction tasks in subsequent calls.
- The output is clear, comprehensive, and logically segmented.

""" 

user_prompt = """
Here is a policy document. Your task is to:
1. Analyze the document and divide it into logical sections based on semantic similarity and structure.
2. For each section, provide:
   - A `section_name` summarizing the section.
   - A `section_description` explaining the section's purpose.
   - A `system_prompt` to guide the extraction of parameters for that section.
   - A `user_prompt` for extracting parameters from that section.
3. Divide the document into sections that are granular enough to capture specific information but not too large. Number of words in a section should not exceed 500.
Input Document: 
"""

# Main function to process the PDF and generate templates
async def generate_sections_metadata(pdf_path, thread_pool_executor):
    # Extract text chunks from PDF
    pdf_chunks = extract_text_from_pdf(pdf_path)
    pdf_path = pdf_path.split("/")[-1].split(".")[0]

    # Call the LLM to generate function templates
    templates = await llm_generate(pdf_chunks, tool_template, system_prompt, user_prompt)
    print(templates)
    result_path = f"extracter_src/output/pipeline_2/sections/{pdf_path}.json"

    await async_write_to_file(result_path, templates, thread_pool_executor)
    
    print(f"Template written to {result_path}")

    return templates



# Run the function for local testing
if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_sections_metadata("Business Responsibility and Sustainability Reporting by Listed Entities - Annexure 1.pdf"))
