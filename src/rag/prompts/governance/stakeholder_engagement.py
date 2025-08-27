stakeholder_engagement = {
    "tool_call" : [
        {
            "type": "function",
            "function": {
                "name": "stakeholder_engagement",
                "description": "Extracts the company's stakeholder engagement efforts from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_stakeholder_meetings": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of stakeholder meetings held"
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
                        "percentage_stakeholders_consulted_in_decision_making": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Percentage of stakeholders consulted in decision-making processes"
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
                        "stakeholder_engagement_survey_results": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Stakeholder engagement survey satisfaction score (out of 100)"
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
                        "number_of_stakeholder_feedback_comments": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of stakeholder feedback comments disclosed"
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
                        "number_of_stakeholder_meetings",
                        "percentage_stakeholders_consulted_in_decision_making",
                        "stakeholder_engagement_survey_results",
                        "number_of_stakeholder_feedback_comments"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt" : (
        "You are a corporate governance analyst. Extract the company's stakeholder engagement efforts from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on the number of stakeholder meetings held, percentage of stakeholders consulted in decision-making processes, "
        "stakeholder engagement survey satisfaction score out of 100, and the number of stakeholder feedback comments disclosed. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt" : (
        "Extract the company's stakeholder engagement efforts from the provided text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    )

}