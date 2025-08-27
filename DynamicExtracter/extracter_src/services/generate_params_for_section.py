import sys
import os
sys.path.append(os.path.abspath(".."))
import asyncio
import json
from src.rag.new_generate.function_call import llm_generate
from DynamicExtracter.extracter_src.services.file_operations import extract_text_from_pdf, async_write_to_file, extract_with_tables



tool_template = [
    {
        "type": "function",
        "function": {
            "name": "extract_section_parameters",
            "description": (
                "Extracts all parameters for a specific topic disclosure in the GRI document, ensuring "
                "completeness and correctness by focusing on the requirements section, and using guidelines and "
                "recommendations for context."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "section_name": {
                        "type": "string",
                        "description": "The name of the topic disclosure from which parameters are to be extracted."
                    },
                    "section_description": {
                        "type": "string",
                        "description": "A detailed description of the topic disclosure's purpose and content."
                    },
                    "attributes": {
                        "type": "array",
                        "description": (
                            "List of attributes representing categories within the topic disclosure, "
                            "each with its parameters."
                        ),
                        "items": {
                            "type": "object",
                            "properties": {
                                "attribute_name": {
                                    "type": "string",
                                    "description": "The name of the attribute within the topic disclosure."
                                },
                                "parameters": {
                                    "type": "array",
                                    "description": "List of parameters related to this attribute.",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "parameter_name": {
                                                "type": "string",
                                                "description": "The name of the parameter associated with the attribute."
                                            },
                                            "parameter_type": {
                                                "type": "string",
                                                "description": "The data type of the parameter (e.g., string, integer, etc.)."
                                            },
                                            "parameter_description": {
                                                "type": "string",
                                                "description": (
                                                    "A detailed description of the parameter's purpose or context, "
                                                    "based on the requirements section."
                                                )
                                            },
                                            "parameter_unit": {
                                                "type": "string",
                                                "description": "The unit of measurement for the parameter value (if applicable)."
                                            },
                                            "parameter_source": {
                                                "type": "string",
                                                "description": "The source from which the value is derived (e.g., page number, section)."
                                            },
                                            "parameter_explanation": {
                                                "type": "string",
                                                "description": (
                                                    "Explanation or justification for including this parameter, "
                                                    "with references to the document."
                                                )
                                            },
                                            "required": {
                                                "type": "boolean",
                                                "description": (
                                                    "Indicates whether this parameter is mandatory based on the requirements section."
                                                )
                                            },
                                            "sub_parameters": {
                                                "type": "array",
                                                "description": (
                                                    "Optional nested sub-parameters for hierarchical data extraction."
                                                ),
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "sub_parameter_name": {
                                                            "type": "string",
                                                            "description": "The name of the sub-parameter."
                                                        },
                                                        "sub_parameter_type": {
                                                            "type": "string",
                                                            "description": (
                                                                "The data type of the sub-parameter (e.g., string, integer, etc.)."
                                                            )
                                                        },
                                                        "sub_parameter_description": {
                                                            "type": "string",
                                                            "description": (
                                                                "A description of the sub-parameter's purpose or context."
                                                            )
                                                        },
                                                        "sub_parameter_unit": {
                                                            "type": "string",
                                                            "description": (
                                                                "The unit of measurement for the sub-parameter value (if applicable)."
                                                            )
                                                        },
                                                        "sub_parameter_source": {
                                                            "type": "string",
                                                            "description": (
                                                                "The source from which the sub-parameter value is derived."
                                                            )
                                                        },
                                                        "sub_parameter_explanation": {
                                                            "type": "string",
                                                            "description": (
                                                                "Justification for why the sub-parameter value was selected."
                                                            )
                                                        },
                                                        "required": {
                                                            "type": "boolean",
                                                            "description": (
                                                                "Indicates whether this sub-parameter is mandatory."
                                                            )
                                                        }
                                                    },
                                                    "required": [
                                                        "sub_parameter_name", "sub_parameter_type",
                                                        "sub_parameter_description", "sub_parameter_source",
                                                        "sub_parameter_explanation", "required"
                                                    ],
                                                    "additionalProperties": False
                                                }
                                            }
                                        },
                                        "required": [
                                            "parameter_name", "parameter_type", "parameter_description",
                                            "parameter_unit", "parameter_source", "parameter_explanation", "required"
                                        ],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["attribute_name", "parameters"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["section_name", "section_description", "attributes"],
                "additionalProperties": False
            }
        }
    }
]


def generate_prompts_for_section(section_name, section_description, next_section_name):
    system_prompt = f"""
    You are an expert assistant tasked with extracting all parameters related to the section: "{section_name}".
    You have to extract EACH AND EVERY PARAMETER for section {section_name} till the start of the next section: "{next_section_name}" from the document.
    Note that the input data is present in markdown format. The data may also contain tables.
    Your goal is to:
    1. Focus solely on this section, avoiding parameters or information from other sections.
    2. Identify all attributes within this section and their associated parameters.
    3. For each parameter, include:
       - Name, type, and detailed description.
       - Unit of measurement (if applicable).
       - Source (page number or subsection from the document).
       - Justification or explanation for its inclusion.
       - Whether it is mandatory.
    4. Support hierarchical data by extracting nested sub-parameters where necessary.
    5. For tablular data, ensure that each row is treated as a separate parameter. All the columns within a row should be considered as sub-parameters.
    6. For example, if a table has 3 rows and 5 columns, you should extract 3 parameters, each with 5 sub-parameters.
    
    Ensure the extracted information is accurate, complete, and directly linked to the section: "{section_name}". 
    Respond only with a JSON object following the given schema and do not skip any parameters for this section.
    """

    user_prompt = f"""
    Please extract all parameters for the section titled: "{section_name}".
    The section's purpose is as follows: {section_description}.
    Focus exclusively on this section. Provide a detailed list of attributes and their associated parameters, including:
    - Parameter name, type, description, unit (if applicable), source, explanation, and whether mandatory.
    Ensure that EACH AND EVERY PARAMETER IS EXTRACTED, including sub-parameters where necessary.
    Ensure the output adheres to the JSON schema and that no parameters from other sections are included.
    Ensure that the tables are properly handled, with each row treated as a separate parameter and columns as sub-parameters.
    """

    return system_prompt, user_prompt


user_prompt = """
Here is a policy document. Your task is to:
1. Analyze the document and divide it into logical sections based on semantic similarity and structure.
2. For each section, provide:
   - A `section_name` summarizing the section.
   - A `section_description` explaining the section's purpose.
   - A `system_prompt` to guide the extraction of parameters for that section.
   - A `user_prompt` for extracting parameters from that section.

Input Document: 
"""

    


# Define the asynchronous function for generating parameters
async def process_section(pdf_path, section, next_section,  pdf_chunks, file_writer_executor):
    # Generate system and user prompts for the section

    if not next_section:
        next_section = {"section_name": "End of Document"}
    sys_prompt, user_prompt = generate_prompts_for_section(section["section_name"], section["section_description"], next_section["section_name"])
    
    # Simulated API call - replace `llm_generate` with your actual async API call implementation
    params = await llm_generate(pdf_chunks, tool_template, sys_prompt, user_prompt)
    
    print("\n")
    print(params)
    print("\n")

    # Create a sanitized section name for file saving
    section_name = section["section_name"].replace(" ", "_")
    
    pdf_name = pdf_path.split("/")[-1].split(".")[0]

    # Save the results in a section-specific JSON file
    output_path = f"extracter_src/output/pipeline_2/section_wise_params/{pdf_name}/{section_name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    await async_write_to_file(output_path,params, file_writer_executor)
    
    return params


async def process_one_section(pdf_path, section, next_section, thread_pool_executor):
    pdf_chunks = await extract_with_tables(pdf_path)

    print(f"\n\n Read pdf. extracting for section {section['section_name']}")

    params = await process_section(pdf_path, section, next_section,  pdf_chunks, thread_pool_executor)
    return params

