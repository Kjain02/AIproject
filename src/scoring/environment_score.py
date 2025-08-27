

import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def generate_environmental_scores_query(environmental_data):
    """
    Queries the OpenAI API to generate environmental scores based on environmental data.
    """
    # Define the function (tool)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_environmental_scores",
                "description": "Generates environmental scores based on provided company environmental data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        
                                "environmental_impact": {
                                    "type": "number",
                                    "description": "Score for the company's environmental impact, such as total GHG emissions, water consumption, land use, etc."
                                },
                                "carbon_emissions_management": {
                                    "type": "number",
                                    "description": "Score for carbon emissions management, including Scope 1, 2, and 3 emissions."
                                },
                                "resource_usage_efficiency": {
                                    "type": "number",
                                    "description": "Score for resource usage efficiency, including energy consumption, renewable energy usage, and material efficiency."
                                },
                                "waste_management_pollution_control": {
                                    "type": "number",
                                    "description": "Score for waste management and pollution control, including waste generated, hazardous waste, and recycling rates."
                                },
                                "climate_change_adaptation_risk": {
                                    "type": "number",
                                    "description": "Score for climate change adaptation and risk mitigation, such as investments in risk mitigation and climate-related financial risks."
                                }
                            }
                        }
                    },
                    "required": ["environmental_impact", "carbon_emissions_management", "resource_usage_efficiency", "waste_management_pollution_control", "climate_change_adaptation_risk"],
                    "additionalProperties": False
                },
    ]

    # Prepare the system message
    # Prepare the system message
    messages = [
        {
            "role": "system",
            "content": (
                "The scores must be between 25 and 98. 25 being the worst and 98 being the best. "
                "You are an expert environmental analyst with deep knowledge of industry standards and best practices. "
                "You will be provided with a company's environmental data, including the units used and detailed descriptions "
                "of each field. Based on this data, generate scores for each environmental factor. Each score should be an integer "
                "between 25 and 98, where 25 represents the worst performance and 98 represents the best performance. "
                "Ensure your evaluation considers the units and meanings of each field, and adheres to industry benchmarks. "
                "If any field contains 'N/A', ignore that field when calculating the scores."
            )
        }
    ]


    # Prepare the user message with environmental data, including units and field meanings
    user_message_content = (
        "Please generate the environmental scores based on the following company data. "
        "Each data point includes units and a description to help you make an accurate assessment.\n\n"
        "Company Environmental Data:\n\n"
    )

    # Function to add units and descriptions to each field
    def format_data_with_units(data, field_descriptions):
        formatted_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                sub_descriptions = field_descriptions.get(key, {})
                formatted_data[key] = format_data_with_units(value, sub_descriptions)
            else:
                description = field_descriptions.get(key, {})
                unit = description.get('unit', '')
                meaning = description.get('meaning', '')
                formatted_data[key] = {
                    'value': value,
                    'unit': unit,
                    'meaning': meaning
                }
        return formatted_data

    # Field descriptions with units and meanings
    field_descriptions = {
        "carbon_emission_data": {
            "scope_1_emissions": {
                "unit": "metric tons CO2-equivalent",
                "meaning": "Direct GHG emissions from owned or controlled sources"
            },
            "scope_2_emissions": {
                "unit": "metric tons CO2-equivalent",
                "meaning": "Indirect GHG emissions from the generation of purchased energy"
            },
            "scope_3_emissions": {
                "unit": "metric tons CO2-equivalent",
                "meaning": "All other indirect emissions that occur in a company's value chain"
            },
            "carbon_reduction_targets": {
                "unit": "N/A",
                "meaning": "Company's targets for reducing carbon emissions"
            },
            "carbon_offset_initiatives": {
                "unit": "N/A",
                "meaning": "Activities undertaken to offset carbon emissions"
            },
            "reporting_compliance": {
                "unit": "Boolean",
                "meaning": "Compliance with regulatory reporting requirements"
            }
        },
        "resource_usage_data": {
            "energy_consumption": {
                "unit": "million kWh",
                "meaning": "Total energy consumed by the company"
            },
            "percentage_renewable_energy": {
                "unit": "percentage",
                "meaning": "Portion of energy consumption from renewable sources"
            },
            "water_usage_per_unit": {
                "unit": "cubic meters per unit",
                "meaning": "Water usage per production unit"
            },
            "material_efficiency_ratio": {
                "unit": "ratio",
                "meaning": "Ratio of material input to output, indicating efficiency"
            },
            "waste_vs_recycled": {
                "total_waste_generated": {
                    "unit": "metric tons",
                    "meaning": "Total waste generated by the company"
                },
                "recycled_waste_percentage": {
                    "unit": "percentage",
                    "meaning": "Percentage of waste that is recycled"
                }
            }
        },
        "climate_change_data": {
            "climate_related_financial_impact": {
                "unit": "USD",
                "meaning": "Financial impact due to climate-related events"
            },
            "investment_in_climate_risk_mitigation": {
                "unit": "USD",
                "meaning": "Investment in mitigating climate risks"
            },
            "number_of_climate_risks_identified": {
                "unit": "count",
                "meaning": "Number of climate-related risks identified"
            },
            "expenditure_on_infrastructure_adaptation": {
                "unit": "USD",
                "meaning": "Spending on adapting infrastructure to climate change"
            }
        },
        "waste_management_data": {
            "total_waste_generated": {
                "unit": "metric tons",
                "meaning": "Total waste generated by the company"
            },
            "hazardous_waste": {
                "unit": "metric tons",
                "meaning": "Amount of hazardous waste generated"
            },
            "recycling_rate": {
                "unit": "percentage",
                "meaning": "Rate at which waste is recycled"
            },
            "pollutant_emissions": {
                "nox_emissions": {
                    "unit": "metric tons",
                    "meaning": "Emissions of nitrogen oxides"
                },
                "sox_emissions": {
                    "unit": "metric tons",
                    "meaning": "Emissions of sulfur oxides"
                },
                "particulate_matter": {
                    "unit": "metric tons",
                    "meaning": "Emissions of particulate matter"
                }
            }
        },
        "environmental_impact_data": {
            "total_carbon_footprint": {
                "unit": "metric tons",
                "meaning": "Total carbon footprint of the company"
            },
            "total_energy_consumption": {
                "unit": "GWh or joules",
                "meaning": "Total energy consumption of the company"
            },
            "water_usage": {
                "unit": "cubic meters",
                "meaning": "Total water usage"
            },
            "air_pollutants_emitted": {
                "sox": {
                    "unit": "metric tons",
                    "meaning": "Emissions of sulfur oxides"
                },
                "nox": {
                    "unit": "metric tons",
                    "meaning": "Emissions of nitrogen oxides"
                },
                "particulate_matter": {
                    "unit": "metric tons",
                    "meaning": "Emissions of particulate matter"
                }
            },
            "hazardous_waste_generated": {
                "unit": "metric tons",
                "meaning": "Total hazardous waste generated"
            },
            "non_hazardous_waste_generated": {
                "unit": "metric tons",
                "meaning": "Total non-hazardous waste generated"
            },
            "biodiversity_impacts": {
                "unit": "N/A",
                "meaning": "Summary of biodiversity impacts"
        }
        }
    }

    # Format the environmental data with units and meanings
    formatted_environmental_data = format_data_with_units(environmental_data["environmental"], field_descriptions)

    # Append the formatted data to the user message content
    user_message_content += json.dumps(formatted_environmental_data, indent=2)

    user_message = {
        "role": "user",
        "content": user_message_content
    }

    messages.append(user_message)
    chat_model = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_GPT_ENDPOINT,
        api_key=AZURE_OPENAI_GPT_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    try:
        # Query the OpenAI Chat Completion API
        response = chat_model.chat.completions.create(
            model=AZURE_OPENAI_GPT_CHAT_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "generate_environmental_scores"}},
        )

        # Extract the function arguments from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            environment_data_response = function_data
            return environment_data_response
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


async def calculate_environmental_score(environmental_data):
    """
    Calculate environmental scores based on the provided environmental data.
    """

    environmental_scores = await generate_environmental_scores_query(environmental_data)

    if not environmental_scores:
        return {}

    return environmental_scores