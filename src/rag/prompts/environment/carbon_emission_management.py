carbon_emission_management = {
        "tool_call": [
            {
                "type": "function",
                "function": {
                    "name": "carbon_emissions_management",
                    "description": "Details of carbon emissions management strategies and performance",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scope_1_emissions": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Scope 1 emissions in metric tons CO2-equivalent"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "The source from which the value is derived, identified by chunk's page number (e.g., 'Page 3')"
                                    },
                                    "explanation": {
                                        "type": "string",
                                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                    }
                                },
                                "required": ["value", "source", "explanation"]
                            },
                            "scope_2_emissions": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Scope 2 emissions in metric tons CO2-equivalent"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "The source from which the value is derived, identified by chunk's page number (e.g., 'Page 5')"
                                    },
                                    "explanation": {
                                        "type": "string",
                                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                    }
                                },
                                "required": ["value", "source", "explanation"]
                            },
                            "scope_3_emissions": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Scope 3 emissions in metric tons CO2-equivalent"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "The source from which the value is derived, identified by chunk's page number (e.g., 'Page 8')"
                                    },
                                    "explanation": {
                                        "type": "string",
                                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                    }
                                },
                                "required": ["value", "source", "explanation"]
                            },
                            "carbon_reduction_targets": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Summary of the company’s carbon reduction targets"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "The source from which the value is derived, identified by chunk's page number"
                                    },
                                    "explanation": {
                                        "type": "string",
                                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                    }
                                },
                                "required": ["value", "source", "explanation"]
                            },
                            "carbon_offset_initiatives": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Description of any carbon offsetting activities undertaken by the company"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "The source from which the value is derived, identified by chunk's page number"
                                    },
                                    "explanation": {
                                        "type": "string",
                                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                    }
                                },
                                "required": ["value", "source", "explanation"]
                            },
                            "reporting_compliance": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Is the company compliant with regulatory reporting (true/false)"
                                    },
                                    "source": {
                                        "type": "string",
                                        "description": "The source from which the value is derived, identified by chunk's page number"
                                    },
                                    "explanation": {
                                        "type": "string",
                                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                                    }
                                },
                                "required": ["value", "source", "explanation"]
                            }
                        },
                        "required": ["scope_1_emissions", "scope_2_emissions", "scope_3_emissions"],
                        "additionalProperties": False,
                    }
                }
            }
        ],
        "system_prompt": (
            "You are an environmental analyst. Extract the company's carbon emissions management details from the provided text. "
            "The text will be presented in the following chunk format: "
            "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
            "Make sure to extract the page number from this format for the source field. "
            "Include information on scope 1, scope 2, and scope 3 emissions, carbon reduction targets, carbon offset initiatives, and reporting compliance. "
            "For each value, provide the page number of the chunk where the information was found as the source. "
            "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
            "If any of these values are not available, return 'N/A' instead of 0 or false."
        ),
        "user_prompt": "Extract the company's carbon emissions management details from the following text. For any missing data, return 'N/A' instead of 0 or false. ",
}