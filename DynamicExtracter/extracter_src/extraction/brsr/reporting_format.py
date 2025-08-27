import sys
import os
sys.path.append(os.path.abspath(".."))

import json
from PyPDF2 import PdfReader
from src.rag.new_generate.function_call import llm_generate
from DynamicExtracter.extracter_src.services.file_operations import extract_text_from_pdf


tool_template = [
    {
        "type": "function",
        "function": {
            "name": "generate_function_call_template",
            "description": "Generates dynamic JSON schema for OpenAI function calls that handles attributes, parameters, and their nested sub-parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "policy_document": {
                        "type": "string",
                        "description": "The policy document or template from which parameters need to be extracted. This will guide the generation of dynamic function call templates."
                    },
                    "attributes": {  
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "attribute_name": {
                                    "type": "string",
                                    "description": "The name of the attribute identified from the provided policy document."
                                },
                                "parameters": {
                                    "type": "array",
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
                                                "description": "A detailed description of the parameter's purpose or context."
                                            },
                                            "parameter_unit": {
                                                "type": "string",
                                                "description": "The unit of measurement for the parameter value (if applicable)."
                                            },
                                            "parameter_source": {
                                                "type": "string",
                                                "description": "The source of the parameter, such as the page number or section of the document."
                                            },
                                            "parameter_explanation": {
                                                "type": "string",
                                                "description": "Justification or reasoning for selecting this parameter value, referencing the source document."
                                            },
                                            "required": {
                                                "type": "boolean",
                                                "description": "Indicates whether this parameter is mandatory."
                                            },
                                            "sub_parameters": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "sub_parameter_name": {
                                                            "type": "string",
                                                            "description": "The name of the sub-parameter."
                                                        },
                                                        "sub_parameter_type": {
                                                            "type": "string",
                                                            "description": "The data type of the sub-parameter."
                                                        },
                                                        "sub_parameter_description": {
                                                            "type": "string",
                                                            "description": "A description of the sub-parameter's purpose or context."
                                                        },
                                                        "sub_parameter_unit": {
                                                            "type": "string",
                                                            "description": "The unit of measurement for the sub-parameter (if applicable)."
                                                        },
                                                        "sub_parameter_source": {
                                                            "type": "string",
                                                            "description": "The source of the sub-parameter, such as the page number or section of the document."
                                                        },
                                                        "sub_parameter_explanation": {
                                                            "type": "string",
                                                            "description": "Justification or reasoning for selecting this sub-parameter value."
                                                        },
                                                        "required": {
                                                            "type": "boolean",
                                                            "description": "Indicates whether this sub-parameter is mandatory."
                                                        }
                                                    },
                                                    "required": ["sub_parameter_name", "sub_parameter_type", "sub_parameter_description", "sub_parameter_source", "sub_parameter_explanation", "required"],
                                                    "additionalProperties": False
                                                },
                                                "description": "Nested sub-parameters specific to this parameter."
                                            }
                                        },
                                        "required": ["parameter_name", "parameter_type", "parameter_description", "parameter_unit", "parameter_source", "parameter_explanation", "required"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["attribute_name", "parameters"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["policy_document", "attributes"],
                "additionalProperties": False
            }
        }
    }
]


# System and user prompts
system_prompt = """
You are an advanced language model tasked with creating a JSON schema for structured data extraction from complex policy documents. Your role is to extract information section by section and generate a comprehensive schema that lists all parameters required to complete a form.

For each section:
1. Identify the section name and provide a description.
2. Extract all parameters within the section and include:
   - Name, type, and detailed description.
   - Unit of measurement (if applicable).
   - Source (page number or section identifier from the document).
   - Explanation or justification for including the parameter.
   - Whether the parameter is mandatory.
3. Support hierarchical data by including sub-parameters where necessary.

Ensure that:
- Every section of the document is processed, and all sections are included in the JSON schema.
- No sections or parameters are skipped.
- Each parameter and sub-parameter is linked to its source and context in the policy document.
- Output is precise, unambiguous, and complete.

Output only the JSON schema for the entire document. Do not skip sections or omit details.


"""

user_prompt = """
Here is the policy document: the Business Responsibility and Sustainability Reporting (BRSR) format.

Your task:
- Process the entire document section by section.
- For each section, extract all required parameters and generate a JSON schema.
- Include section names, descriptions, parameters, and their details (name, type, unit, source, explanation, and whether mandatory).
- Ensure all sections from the document (e.g., General Disclosures, Principle-wise Performance, etc.) are covered in the JSON.

Start by processing the document and extract parameters for **all sections**. Ensure the JSON schema includes every section and parameter, adhering to the following structure:

Example for a section:
{
    "policy_document": "BRSR",
    "sections": [
        {
            "section_name": "General Disclosures",
            "section_description": "Basic information about the company and its operations.",
            "parameters": [
                {
                    "parameter_name": "Corporate Identity Number (CIN)",
                    "parameter_type": "string",
                    "parameter_description": "The unique identifier for the company.",
                    "parameter_unit": null,
                    "parameter_source": "Section A, I.",
                    "parameter_explanation": "This parameter serves to uniquely identify the company within legal frameworks and regulatory standards.",
                    "required": true,
                    "sub_parameters": []
                }
            ]
        },
        {
            "section_name": "Principle 1: Ethics, Transparency, and Accountability",
            "section_description": "Details related to the company's ethical practices.",
            "parameters": [
                ...
            ]
        },
        ...
    ]
}
Ensure every section in the document is fully represented.

"""

# Main function to process the PDF and generate templates
async def brsr_reporting_format_generate(pdf_path):
    # Extract text chunks from PDF
    pdf_chunks = extract_text_from_pdf(pdf_path)

    pdf_path = pdf_path.split("/")[-1].split(".")[0]

    # Call the LLM to generate function templates
    templates = await llm_generate(pdf_chunks, tool_template, system_prompt, user_prompt)
    result_path = f"extracter_src/output/brsr/reporting_format/{pdf_path}.json"
    with open (result_path, "w") as f:
        json.dump(templates, f, indent=4)

    print(f"Template written to {result_path}")

    return templates



# Run the function for local testing
if __name__ == "__main__":
    import asyncio
    asyncio.run(brsr_reporting_format_generate("Business Responsibility and Sustainability Reporting by Listed Entities - Annexure 1.pdf"))
