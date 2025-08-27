labour_standards_human_rights = {
    "tool_call": [
        {
            "type": "function",
            "function": {
                "name": "labor_standards_human_rights",
                "description": "Extracts the company's compliance with labor standards and human rights policies from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fair_wage_percentage": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Percentage of employees receiving fair wage (compared to local living wage)"
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
                        "number_of_human_rights_violations": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of human rights violations reported"
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
                        "percentage_supply_chain_audits": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Percentage of supply chain audited for labor standards"
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
                        "child_labor_violations": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of child labor or forced labor incidents reported"
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
                        "fair_wage_percentage",
                        "number_of_human_rights_violations",
                        "percentage_supply_chain_audits",
                        "child_labor_violations"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt" : (
        "You are a human rights compliance analyst. Extract the company's compliance with labor standards and human rights policies from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on fair wage percentage, number of human rights violations reported, percentage of supply chain audited for labor standards, and number of child labor or forced labor incidents reported. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt" : (
        "Extract the company's compliance with labor standards and human rights policies from the following text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    )

}