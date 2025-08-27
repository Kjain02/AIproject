import sys
import os
sys.path.append(os.path.abspath(".."))

import json
from PyPDF2 import PdfReader
from src.rag.new_generate.function_call import llm_generate
from DynamicExtracter.extracter_src.services.file_operations import extract_text_from_pdf


# Define the tool template for generating function calls
tool_template = [
    {
        "type": "function",
        "function": {
            "name": "generate_function_call_template",
            "description": "Generates dynamic JSON schema for OpenAI function calls that handles attributes, parameters, and their nested sub-parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "attributes": {  # Array of attributes for flexibility
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "attribute_name": {  # Name of the attribute
                                    "type": "string",
                                    "description": "The name of the attribute identified from the provided document."
                                },
                                "parameters": {  # Array of parameters related to this attribute
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "parameter_name": {  # Name of the parameter
                                                "type": "string",
                                                "description": "The name of the parameter associated with the attribute."
                                            },
                                            "parameter_type": {  # Data type of the parameter
                                                "type": "string",
                                                "description": "The data type of the parameter (e.g., string, integer, etc.)."
                                            },
                                            "parameter_description": {  # Description of the parameter
                                                "type": "string",
                                                "description": "A detailed description of the parameter's purpose or context."
                                            },
                                            "parameter_unit" :{
                                                "type": "string",
                                                "description": "The unit of measurement for the parameter value."
                                            },
                                            "parameter_source": {
                                                "type": "string",
                                                "description": "The source from which the value is derived, identified by chunk's page number"
                                            },
                                            "parameter_explaination": {
                                                "type": "string",
                                                "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                            },
                                            "required": {  # Whether the parameter is required or optional
                                                "type": "boolean",
                                                "description": "Indicates whether this parameter is mandatory."
                                            },
                                            "sub_parameters": {  # Nested sub-parameters (optional, only if needed)
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "sub_parameter_name": {  # Name of the sub-parameter
                                                            "type": "string",
                                                            "description": "The name of the sub-parameter."
                                                        },
                                                        "sub_parameter_type": {  # Data type of the sub-parameter
                                                            "type": "string",
                                                            "description": "The data type of the sub-parameter (e.g., string, integer, etc.)."
                                                        },
                                                        "sub_parameter_description": {  # Description of the sub-parameter
                                                            "type": "string",
                                                            "description": "A description of the sub-parameter's purpose or context."
                                                        },
                                                        "sub_parameter_unit" :{
                                                            "type": "string",
                                                            "description": "The unit of measurement for the sub-parameter value."
                                                        },
                                                        "sub_paramter_source": {
                                                            "type": "string",
                                                            "description": "The source from which the value is derived, identified by chunk's page number"
                                                        },
                                                        "sub_paramter_explaination": {
                                                            "type": "string",
                                                            "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                                        },
                                                        "required": {  # Whether the sub-parameter is required or not
                                                            "type": "boolean",
                                                            "description": "Indicates whether this sub-parameter is mandatory."
                                                        }
                                                    },
                                                    "required": ["sub_parameter_name", "sub_parameter_type", "sub_parameter_description","sub_paramter_source", "sub_parameter_explaination", "required"],
                                                    "additionalProperties": False
                                                },
                                                "description": "Optional nested sub-parameters specific to this parameter."
                                            }
                                        },
                                        "required": ["parameter_name", "parameter_type", "parameter_description","parameter_unit", "parameter_source", "parameter_explaination", "required"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["attribute_name", "parameters"],  # Ensuring each attribute has its parameters
                            "additionalProperties": False  # Prevent additional, unspecified fields
                        }
                    }
                },
                "required": ["attributes"],  # The schema must include the 'attributes' field
                "additionalProperties": False  # Prevent any unintended extra fields
            }
        }
    }
]



# System and user prompts
system_prompt = """
You are a technical assistant. Your task is to generate OpenAI function call templates in JSON schema format.
Follow these steps:
1. Identify the attributes from the provided text.
2. For each attribute, identify the relevant parameters.
3. Generate a JSON function call template for each attribute and its parameters.
Ensure that the generated output strictly adheres to the JSON schema format for OpenAI function calls.
"""

user_prompt = """
Extract function call templates for attributes and parameters mentioned in the text. Return the output in JSON format.
"""

# Main function to process the PDF and generate templates
async def brsr_template_generate(pdf_path):
    # Extract text chunks from PDF
    pdf_chunks = extract_text_from_pdf(pdf_path)

    pdf_path = pdf_path.split("/")[-1].split(".")[0]

    # Call the LLM to generate function templates
    templates = await llm_generate(pdf_chunks, tool_template, system_prompt, user_prompt)
    result_path = f"extracter_src/output/brsr/annexture/{pdf_path}.json"
    with open (result_path, "w") as f:
        json.dump(templates, f, indent=4)

    print(f"Template written to {result_path}")

    return templates



# Run the function for local testing
if __name__ == "__main__":
    import asyncio
    asyncio.run(brsr_template_generate("Business Responsibility and Sustainability Reporting by Listed Entities - Annexure 1.pdf"))
