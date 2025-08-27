ethical_business_practices = {
    "tool_call" : [
        {
            "type": "function",
            "function": {
                "name": "ethical_business_practices",
                "description": "Extracts the company's ethical business practices from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_corruption_bribery_incidents": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of corruption or bribery incidents reported"
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
                        "anti_corruption_policy_compliance_rate": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Anti-corruption policy compliance rate (percentage of employees trained)"
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
                        "number_of_whistleblower_reports": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of whistleblower reports filed"
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
                        "code_of_ethics_violations": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of code of ethics violations"
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
                        "number_of_corruption_bribery_incidents",
                        "anti_corruption_policy_compliance_rate",
                        "number_of_whistleblower_reports",
                        "code_of_ethics_violations"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt": (
        "You are a corporate governance analyst. Extract the company's ethical business practices from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on the number of corruption or bribery incidents reported, anti-corruption policy compliance rate "
        "(percentage of employees trained), number of whistleblower reports filed, and number of code of ethics violations. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt":(
        "You are a corporate governance analyst. Extract the company's ethical business practices from the provided text. "
        "For any missing data, return 'N/A' instead of 0."
    )

}