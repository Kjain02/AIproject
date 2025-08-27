executive_compensation = {
    "tool_call" : [
        {
            "type": "function",
            "function": {
                "name": "executive_compensation",
                "description": "Extracts details of executive compensation from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ceo_to_employee_pay_ratio": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "CEO-to-employee pay ratio"
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
                        "total_compensation_for_top_executives": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total compensation for top executives (in base currency)"
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
                        "performance_based_pay_percentage": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Performance-based pay as a percentage of total executive compensation"
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
                        "median_employee_compensation": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Median employee compensation (in base currency)"
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
                        "ceo_to_employee_pay_ratio",
                        "total_compensation_for_top_executives",
                        "performance_based_pay_percentage",
                        "median_employee_compensation"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt": (
        "You are a corporate governance analyst. Extract the company's executive compensation details from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on the CEO-to-employee pay ratio, total compensation for top executives, performance-based pay percentage, "
        "and median employee compensation. For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt": (
        "Extract the company's executive compensation details from the following text. "
        "For any missing data, return 'N/A' instead of 0."
    )

}