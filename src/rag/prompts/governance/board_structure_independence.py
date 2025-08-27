board_structure_independence = {
    "tool_call": [
        {
            "type": "function",
            "function": {
                "name": "board_structure_independence",
                "description": "Extracts the company's board structure and independence details from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_board_members": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total number of board members"
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
                        "percentage_independent_board_members": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Percentage of independent board members"
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
                        "average_board_member_tenure": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Average tenure of board members (years)"
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
                        "gender_ethnic_diversity": {
                            "type": "object",
                            "properties": {
                                "percentage_gender_diverse_board_members": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of female board members"
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
                                "percentage_ethnically_diverse_board_members": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of board members from diverse ethnic backgrounds"
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
                            }
                        }
                    },
                    "required": [
                        "number_of_board_members",
                        "percentage_independent_board_members",
                        "average_board_member_tenure",
                        "gender_ethnic_diversity"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt": (
        "You are a corporate governance analyst. Extract the company's board structure and independence details from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on the total number of board members, percentage of independent board members, average tenure, and gender and ethnic diversity statistics. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt": (
        "Extract the company's board structure and independence details from the following text. "
        "For any missing data, return 'N/A' instead of 0."
    )

} 