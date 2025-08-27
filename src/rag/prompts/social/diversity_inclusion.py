diversity_inclusion = {
    "tool_call" : [
        {
            "type": "function",
            "function": {
                "name": "diversity_inclusion",
                "description": "Extracts the company's diversity and inclusion efforts from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "gender_diversity": {
                            "type": "object",
                            "properties": {
                                "percentage_female_employees": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of female employees"
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
                                "percentage_female_leadership": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of females in leadership roles"
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
                            "required": ["percentage_female_employees", "percentage_female_leadership"]
                        },
                        "racial_ethnic_diversity": {
                            "type": "object",
                            "properties": {
                                "percentage_diverse_employees": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of employees from diverse racial/ethnic backgrounds"
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
                                "percentage_diverse_leadership": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of leadership from diverse racial/ethnic backgrounds"
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
                            "required": ["percentage_diverse_employees", "percentage_diverse_leadership"]
                        },
                        "employees_with_disabilities_percentage": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Percentage of employees with disabilities"
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
                        "diversity_training_hours_per_employee": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Diversity training hours per employee"
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
                        "pay_equity_ratio": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Pay equity ratio (gender pay gap)"
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
                        "gender_diversity",
                        "racial_ethnic_diversity",
                        "employees_with_disabilities_percentage",
                        "diversity_training_hours_per_employee",
                        "pay_equity_ratio"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt" : (
        "You are an HR analyst. Extract the company's diversity and inclusion efforts from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on gender diversity, racial/ethnic diversity, employees with disabilities, diversity training, and pay equity. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt" : (
        "Extract the company's diversity and inclusion efforts from the following text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    )

}