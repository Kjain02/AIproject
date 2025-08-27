# Tool Calling Templates
environment = {
    "carbon_emission_management": {
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
    },
    "climate_change_adaptation_risk": {
        "tool_call":[
            {
                "type": "function",
                "function": {
                    "name": "climate_change_adaptation_risk",
                    "description": "Extracts the company's climate change adaptation and risk mitigation details from the provided text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "climate_related_financial_impact": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Climate-related financial impact (in base currency)"
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
                            "investment_in_climate_risk_mitigation": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Investment in climate risk mitigation (in base currency)"
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
                            "number_of_climate_risks_identified": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Number of climate-related risks identified"
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
                            "expenditure_on_infrastructure_adaptation": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "Expenditure on infrastructure adaptation to climate change (in base currency)"
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
                        "required": [
                            "climate_related_financial_impact",
                            "investment_in_climate_risk_mitigation",
                            "number_of_climate_risks_identified",
                            "expenditure_on_infrastructure_adaptation"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        ],
        "system_prompt": (
            "You are an environmental analyst. Extract the company's climate change adaptation and risk mitigation details from the provided text. "
            "The text will be presented in the following chunk format: "
            "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
            "Include information on climate-related financial impact, investment in climate risk mitigation, number of climate-related risks identified, and expenditure on infrastructure adaptation. "
            "If any of these values are not available, return 'N/A' instead of 0."
        ),
        "user_prompt": "Extract the company's climate change adaptation and risk mitigation details from the following text.  For any missing data, return 'N/A' instead of 0 or false.",

    }
}


general = {
    "company_name" : {
        "tool_call": [
            {
                "type": "function",
                "function": {
                    "name": "company_name_and_year",
                    "description": "Extracts the company's name and the report year from the provided text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the company"
                            },
                            "year": {
                                "type": "string",
                                "description": "The year for which the financial report is being made"
                            }
                        },
                        "required": [
                            "name",
                            "year"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        ],
        "system_prompt": (
        "You are a financial analyst. Extract the company's name and the report year from the provided text. "
    ),
        "user_prompt": "Extract the company's name and the report year from the following text.",
    }
}


