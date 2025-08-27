climate_change_adaptation_risk = {
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