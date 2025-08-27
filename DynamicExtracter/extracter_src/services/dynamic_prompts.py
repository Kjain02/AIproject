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
                                        "A prompt for the RAG model to extract parameters from this topic disclosure."
                                    ),
                                },
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


topic_tool_template = [
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

Ensure:
- The output includes only the topic disclosure sections (e.g., 305-1 to 305-7).
- Prompts are detailed, focused, and appropriate for guiding parameter extraction in subsequent calls.
- The output is clear, comprehensive, and accurately represents the structure of the GRI document.
"""

user_prompt = """
Here is a GRI document. Your task is to:
1. Analyze the document and identify its seven topic disclosure sections.
2. For each topic disclosure section, provide:
   - A `section_name` summarizing the topic disclosure.
   - A `section_description` explaining the disclosure's purpose and content.
   - A `system_prompt` to guide the extraction of parameters for that disclosure.
   - A `user_prompt` for extracting parameters from that disclosure.
   - A `rag_prompt` to guide extraction of parameters from that disclosure.

Input Document:
"""


def generate_prompts_for_section(section_name, section_description):
    system_prompt = f"""
    You are an expert assistant tasked with extracting all parameters related to the topic disclosure: "{section_name}".
    Your goal is to:
    1. Focus exclusively on this topic disclosure, avoiding parameters or information from other sections.
    2. Identify all attributes and their associated parameters as mentioned in the requirements section.
    3. For each parameter, provide:
       - Name, type, and detailed description from the requirements section.
       - Unit of measurement (if applicable).
       - Source (page number or subsection from the document).
       - Explanation or justification, including references to the guidelines and recommendations sections.
       - Generate all parameters, including sub-parameters if applicable.
       - Whether it is mandatory based on the requirements section.
    4. Include hierarchical data by extracting nested sub-parameters if applicable.
    5. Use information from the guidelines and recommendations sections to enhance the context of extracted parameters.
    6. Parameter names should be elaborate and descriptive, ensuring clarity and relevance to the topic disclosure.

    Ensure all parameters are complete, accurate, and directly linked to the topic disclosure: "{section_name}". 
    Respond only with a JSON object adhering to the schema.
    """

    user_prompt = f"""
    Please extract all parameters for the topic disclosure titled: "{section_name}".
    The disclosure's purpose is as follows: {section_description}.
    Focus exclusively on this topic disclosure. Provide a detailed list of attributes and their associated parameters, including:
    - Parameter name, type, description, unit (if applicable), source, explanation, and whether mandatory.
    - Extract all parameters comprehensively, ensuring no relevant information is omitted.
    - Parameter names should be clear and descriptive, reflecting the content of the topic disclosure.
    Use the guidelines and recommendations sections for additional context where relevant.
    Ensure the output adheres to the JSON schema and does not include parameters from other disclosures.
    """

    return system_prompt, user_prompt