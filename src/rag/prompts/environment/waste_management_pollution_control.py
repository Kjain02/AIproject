waste_management_pollution_control =  {
    "tool_call": [
        {
            "type": "function",
            "function": {
                "name": "waste_management_pollution_control",
                "description": "Extracts the company's waste management and pollution control efforts from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "total_waste_generated": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total waste generated (in tons)"
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
                        "hazardous_waste": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Hazardous waste (in tons)"
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
                        "recycling_rate": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Recycling rate (percentage of total waste recycled)"
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
                        "pollutant_emissions": {
                            "type": "object",
                            "properties": {
                                "nox_emissions": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "NOx emissions (in metric tons)"
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
                                "sox_emissions": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "SOx emissions (in metric tons)"
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
                                "particulate_matter": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Particulate matter emissions (in metric tons)"
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
                        "total_waste_generated",
                        "hazardous_waste",
                        "recycling_rate",
                        "pollutant_emissions"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt": (
        "You are an environmental analyst. Extract the company's waste management and pollution control details from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on total waste generated, hazardous waste, recycling rates, and emissions of pollutants like NOx, SOx, and particulate matter. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt": (
        "Extract the company's waste management and pollution control details from the following text. "
        "For any missing data, return 'N/A' instead of 0."
    )

}