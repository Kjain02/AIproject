import sys
import os
sys.path.append(os.path.abspath(".."))
import asyncio
import json
from src.rag.new_generate.function_call import llm_generate
from DynamicExtracter.extracter_src.services.file_operations import extract_text_from_pdf, async_write_to_file


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
                                                "description": "The unit of measurement for the parameter value (if applicable). It should be from this list ''"
                                            },
                                            "parameter_source": {
                                                "type": "integer",
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
                                                            "type": "integer",
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

def generate_prompts_for_section(section_name, section_description):
    system_prompt = f"""
    You are an expert assistant tasked with extracting all parameters related to the topic disclosure: "{section_name}".
    Your goal is to:
    1. Focus exclusively on this topic disclosure, avoiding parameters or information from other sections.
    2. Identify all attributes and their associated parameters as mentioned in the requirements section.
    3. For each parameter, provide:
       - Name, type, and detailed description from the requirements section.
       - Unit of measurement (if applicable).
       - Source (page number or subsection from the document), which should be an integer.
       - Explanation or justification, including references to the guidelines and recommendations sections.
       - Generate all parameters, including sub-parameters if applicable.
       - Whether it is mandatory based on the requirements section.
    4. Include hierarchical data by extracting nested sub-parameters if applicable.
    5. Use information from the guidelines and recommendations sections to enhance the context of extracted parameters.
    6. Ensure every parameter is comprehensively reported. For any parameter that has associated sub-parameters (e.g., lists or nested items), extract all related sub-parameters explicitly and represent them in a clear parent-parameter to sub-parameter structure. For example:
       - If the document contains a point such as:
         "a. Base year for the calculation, if applicable, including:
            i. the rationale for choosing it;
            ii. emissions in the base year;
            iii. the context for any significant changes in emissions that triggered recalculations of base year emissions."
         Then:
         - The entry "Base year for the calculation" becomes the parent parameter.
         - The sublist items (i, ii, iii) become its sub-parameters.
         - These must be structured in a parent-child relationship.
    7. Section name , Parameters Name and Subparameters Name should be extracted as they appear in the document and They should be very descriptive.
    Ensure that all parameters and sub-parameters are complete, accurately extracted, and directly linked to the topic disclosure: "{section_name}".
    Respond only with a JSON object adhering to the schema.
    """


    user_prompt = f"""
    Please extract all parameters for the topic disclosure titled: "{section_name}".
    The disclosure's purpose is as follows: {section_description}.
    Focus exclusively on this topic disclosure. Provide a detailed list of attributes and their associated parameters, including:
    - Parameter name, type, description, unit (if applicable), source, explanation, and whether mandatory.
    - Extract all parameters comprehensively, ensuring no relevant information is omitted.
    - Parameter names should be clear and descriptive, reflecting the content of the topic disclosure.
    - Parameter Names and Subparameter names should be extracted as they appear in the document and They should be very descriptive.
    Use the guidelines and recommendations sections for additional context where relevant.
    Ensure the output adheres to the JSON schema and does not include parameters from other disclosures.
    """

    return system_prompt, user_prompt
 


# Define the asynchronous function for generating parameters
async def process_topic(pdf_path, section, pdf_chunks, tool_template, file_writer_executor, output_dir = None):
    # Generate system and user prompts for the section
    sys_prompt, user_prompt = generate_prompts_for_section(section["section_name"], section["section_description"])
    
    # Simulated API call - replace `llm_generate` with your actual async API call implementation
    params = await llm_generate(pdf_chunks, tool_template, sys_prompt, user_prompt)
    
    # Create a sanitized section name for file saving
    section_name = section["section_name"].replace(" ", "_")
    
    pdf_name = pdf_path.split("/")[-1].split(".")[0]

    # Save the results in a section-specific JSON file
    output_path = f"{output_dir}/{section_name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    await async_write_to_file(output_path,params, file_writer_executor)
    
    return params



async def process_one_topic(pdf_path, section, thread_pool_executor, output_dir = None):
    pdf_chunks = extract_text_from_pdf(pdf_path)

    # create output directory if it doesn't exist
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
    params = await process_topic(pdf_path, section, pdf_chunks, tool_template, thread_pool_executor, output_dir)
    return params



# # Run the function for local testing
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(process_all_sections("Business Responsibility and Sustainability Reporting by Listed Entities - Annexure 1.pdf"))
