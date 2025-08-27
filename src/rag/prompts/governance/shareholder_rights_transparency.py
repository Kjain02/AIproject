shareholder_rights_transparency = {
    "tool_call" : [
        {
            "type": "function",
            "function": {
                "name": "shareholder_rights_transparency",
                "description": "Extracts details of shareholder rights and transparency from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "voting_rights_per_share_class": {
                            "type": "array",
                            "description": "Details of voting rights for each class of shares",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "class_name": {
                                        "type": "object",
                                        "properties": {
                                            "value": {
                                                "type": "string",
                                                "description": "Name of the share class"
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
                                    "voting_rights": {
                                        "type": "object",
                                        "properties": {
                                            "value": {
                                                "type": "string",
                                                "description": "Voting rights per share"
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
                                "required": ["class_name", "voting_rights"],
                                "additionalProperties": False
                            }
                        },
                        "shareholder_proposal_submission_rates": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of shareholder proposals submitted"
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
                        "number_of_shareholder_meetings": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Number of shareholder meetings held"
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
                        "disclosure_level_based_on_esg": {
                            "type": "object",
                            "properties": {
                                "gri_disclosure": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Disclosure level based on GRI framework"
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
                                "sasb_disclosure": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Disclosure level based on SASB framework"
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
                            "required": ["gri_disclosure", "sasb_disclosure"],
                            "additionalProperties": False
                        }
                    },
                    "required": [
                        "voting_rights_per_share_class",
                        "shareholder_proposal_submission_rates",
                        "number_of_shareholder_meetings",
                        "disclosure_level_based_on_esg"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt": (
        "You are a corporate governance analyst. Extract the company's shareholder rights and transparency details from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on voting rights per share class, shareholder proposal submission rates, number of shareholder meetings held, "
        "and disclosure levels based on ESG frameworks such as GRI and SASB. For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt": (
        "Extract the company's shareholder rights and transparency details from the following text. "
        "For any missing data, return 'N/A' instead of 0."
    )

}