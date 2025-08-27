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
            "description": (
                "Divides a GRI document into topic disclosure sections, "
                "generating metadata for each section including its description, name, and prompts for further extraction."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sections": {
                        "type": "array",
                        "description": (
                            "List of topic disclosure sections identified in the GRI document, "
                            "each represented by metadata."
                        ),
                        "items": {
                            "type": "object",
                            "properties": {
                                "section_description": {
                                    "type": "string",
                                    "description": (
                                        "A detailed description of the topic disclosure's content and purpose."
                                    ),
                                },
                                "section_name": {
                                    "type": "string",
                                    "description": (
                                        "The name or title of the topic disclosure (e.g., 'Disclosure 305-1: Direct GHG Emissions')."
                                    ),
                                },
                                "system_prompt": {
                                    "type": "string",
                                    "description": (
                                        "A detailed system prompt to guide extraction of parameters from this topic disclosure."
                                    ),
                                },
                                "user_prompt": {
                                    "type": "string",
                                    "description": (
                                        "A focused user prompt to provide context and extraction instructions for this topic disclosure."
                                    ),
                                },
                                "rag_prompt": {
                                    "type": "string",
                                    "description": (
                                        "This is a detailed prompt for the RAG (Retrieval-Augmented Generation) model, designed to guide the model in extracting highly relevant and accurate parameters or information from a given topic disclosure. The prompt should be carefully crafted to ensure that the model is able to query the vector store efficiently, retrieving specific and contextually appropriate chunks of information. The goal is to provide the RAG model with a clear, precise request that leads to the selection of the most pertinent data from the vector store, which will then be used to answer queries or enhance further processing. When creating the prompt, consider incorporating detailed instructions regarding the type of data you need, any context, and any constraints that should be followed. This helps the model narrow down the search space and improves the relevance and quality of the retrieved chunks, making them more valuable for the task at hand."
                                    )
                                }
                            },
                            "required": ["section_description", "section_name", "system_prompt", "user_prompt"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["sections"],
                "additionalProperties": False,
            },
        },
    }
]

# Revised System and User Prompts
system_prompt = """  
You are an advanced assistant tasked with analyzing a GRI document and identifying its topic disclosure sections. Your role is to:  
1. Carefully read the provided document.  
2. Identify the seven topic disclosure sections based on their structure, headings, and semantic content.  
3. For each topic disclosure section, generate:  
   - A `section_name` summarizing the content (e.g., 'Disclosure 305-1: Direct GHG Emissions').  
   - A `section_description` providing a detailed explanation of the disclosure's purpose and content.  
   - A tailored `system_prompt` to guide the extraction of parameters from this disclosure.  
   - A specific `user_prompt` for requesting the extraction of detailed parameters from this disclosure.  
   - A `rag_prompt` to guide the RAG model in extracting parameters from this disclosure.  

### Special Instructions for `rag_prompt` Generation:  
- Ensure the `rag_prompt` is verbose and includes relevant technical terminology, structured phrases, and synonyms derived from the document to improve keyword matching and retrieval performance. You should try to keep the length of rag prompt above 3-4 sentences.
- Incorporate exact phrases, acronyms, and structured language commonly found in the document. For instance, include metrics, numerical identifiers, and compliance terminology (e.g., 'Direct GHG Emissions', 'Disclosure 305-1', 'sustainability performance indicators').  
- The `rag_prompt` should describe the context and structure of the specific disclosure section in detail, referencing key elements such as data fields, metrics, frameworks, or compliance requirements.  
- Use multiple descriptive phrases and synonyms to enhance both semantic similarity and exact match retrieval for ensemble systems like BM25 + Faiss.  

Ensure:  
- The output includes only the topic disclosure sections (e.g., 305-1 to 305-7).  
- Prompts are detailed, verbose, and tailored to guide precise parameter extraction in subsequent calls.  
- The content is aligned with the structure and terminology of the GRI document to maximize retrieval performance.  
 
"""  


user_prompt = """
Here is a GRI document. Your task is to:
1. Analyze the document and identify its seven topic disclosure sections.

Input Document:
"""



# Main function to process the PDF and generate templates
async def extract_gri_topics(pdf_path, thread_pool_executor, output_dir = None):
    # Extract text chunks from PDF
    pdf_chunks = extract_text_from_pdf(pdf_path)

    pdf_path = pdf_path.split("/")[-1].split(".")[0]

    # create output directory if it doesn't exist
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        
    # Call the LLM to generate function templates
    templates = await llm_generate(pdf_chunks, tool_template, system_prompt, user_prompt)
    result_path = f"{output_dir}/{pdf_path}.json"

    await async_write_to_file(result_path, templates, thread_pool_executor)
    
    print(f"Template written to {result_path}")

    return templates

