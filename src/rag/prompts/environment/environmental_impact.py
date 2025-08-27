environmental_impact =  {
    "tool_call" :[
        {
            "type": "function",
            "function": {
                "name": "environmental_impact",
                "description": "Extracts the environmental impact details of the company's activities from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "total_carbon_footprint": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total carbon footprint of the company in metric tons"
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
                        "total_energy_consumption": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total energy consumption of the company in GWh or joules"
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
                        "water_usage": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total water usage in cubic meters"
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
                        "air_pollutants_emitted": {
                            "type": "object",
                            "properties": {
                                "sox": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "SOx emissions in metric tons"
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
                                "nox": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "NOx emissions in metric tons"
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
                                            "description": "Particulate matter emissions in metric tons"
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
                        },
                        "hazardous_waste_generated": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total hazardous waste generated in metric tons"
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
                        "non_hazardous_waste_generated": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total non-hazardous waste generated in metric tons"
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
                        "biodiversity_impacts": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Summary of biodiversity impacts (e.g., deforestation, impacts on protected areas)"
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
                        "total_carbon_footprint",
                        "total_energy_consumption",
                        "water_usage",
                        "air_pollutants_emitted",
                        "hazardous_waste_generated",
                        "non_hazardous_waste_generated",
                        "biodiversity_impacts"
                    ],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt" : (
        "You are an environmental analyst specializing in corporate sustainability. "
        "Your task is to extract detailed information about the environmental impact of the company's activities from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Specifically, identify and report on the total carbon footprint in metric tons, total energy consumption in GWh or joules, "
        "total water usage in cubic meters, emissions of air pollutants including SOx, NOx, and particulate matter in metric tons, "
        "total hazardous and non-hazardous waste generated in metric tons, and any impacts on biodiversity such as deforestation or effects on protected areas. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt" : (
        "Extract the environmental impact details of the company's activities from the following text. "
        "For any missing data, return 'N/A' instead of 0."
    )
}