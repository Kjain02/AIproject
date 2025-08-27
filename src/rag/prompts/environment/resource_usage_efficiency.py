resource_usage_efficiency = {
    "tool_call": [
        {
            "type": "function",
            "function": {
                "name": "resource_usage_efficiency",
                "description": "Extracts the resource usage and efficiency details from the provided text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "energy_consumption": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Total energy consumption (in MWh or GJ)"
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
                        "percentage_renewable_energy": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Percentage of renewable energy used"
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
                        "water_usage_per_unit": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Water usage (cubic meters per production unit)"
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
                        "material_efficiency_ratio": {
                            "type": "object",
                            "properties": {
                                "value": {
                                    "type": "string",
                                    "description": "Material efficiency (input vs. output ratio)"
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
                        "waste_vs_recycled": {
                            "type": "object",
                            "properties": {
                                "total_waste_generated": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Waste generated (in tons)"
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
                                "recycled_waste_percentage": {
                                    "type": "object",
                                    "properties": {
                                        "value": {
                                            "type": "string",
                                            "description": "Percentage of waste recycled"
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
                    "required": ["energy_consumption", "percentage_renewable_energy", "water_usage_per_unit", "material_efficiency_ratio", "waste_vs_recycled"],
                    "additionalProperties": False
                }
            }
        }
    ],
    "system_prompt": (
        "You are an expert environmental analyst. Extract the resource usage and efficiency details from the provided text. "
        "The text will be presented in the following chunk format: "
        "<page_number>{{page_num}}<page_number>    {{text}}\\n\\n<page_number>{{page_num}}<page_number>    {{text}} ... "
        "Make sure to extract the page number from this format for the source field. "
        "Include information on energy consumption, percentage of renewable energy used, water usage per unit, material efficiency ratio, and waste management details. "
        "For each value, provide the page number of the chunk where the information was found as the source. "
        "In the explanation, justify why you chose the value by either citing relevant parts or quoting directly from the chunk text. "
        "If any of these values are not available, return 'N/A' instead of 0."
    ),
    "user_prompt": (
        "Extract the company's resource usage and efficiency details from the following text. "
        "For any missing data, return 'N/A' instead of 0."
    )

}