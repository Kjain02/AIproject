import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def generate_social_scores_query(social_data):
    """
    Queries the OpenAI API to generate social scores based on social data.
    """
    # Define the function (tool)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_social_scores",
                "description": "Generates social scores based on provided company social data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                                "employee_relations_satisfaction": {
                                    "type": "number",
                                    "description": "Score for the company's employee relations and satisfaction."
                                },
                                "diversity_inclusion": {
                                    "type": "number",
                                    "description": "Score for the company's diversity and inclusion efforts."
                                },
                                "health_safety_practices": {
                                    "type": "number",
                                    "description": "Score for the company's health and safety practices."
                                },
                                "labor_standards_human_rights": {
                                    "type": "number",
                                    "description": "Score for the company's compliance with labor standards and human rights."
                                },
                                "community_engagement_social_responsibility": {
                                    "type": "number",
                                    "description": "Score for the company's community engagement and social responsibility initiatives."
                                },
                                "product_safety_customer_well_being": {
                                    "type": "number",
                                    "description": "Score for the company's product safety and customer well-being initiatives."
                                }
                            }
                        }
                    },
                    "required": ["employee_relations_satisfaction", "diversity_inclusion", "health_safety_practices", "labor_standards_human_rights", "community_engagement_social_responsibility", "product_safety_customer_well_being"],
                    "additionalProperties": False
                },
            
    ]

    # Prepare the system message with enhanced prompts
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert social responsibility analyst with extensive knowledge of global industry standards, regulatory requirements, "
                "and best practices in social performance assessment. You will be provided with detailed social data for a company, "
                "including the numerical values, units of measurement, and comprehensive descriptions of each metric's significance. "
                "Your task is to critically evaluate this data and generate objective scores for each specified social factor. "
                "\n\n"
                "Instructions:\n"
                "- Each score should be an integer between 25 and 98, where 25 represents the worst performance and 98 represents the best performance.\n"
                "- Carefully consider the units and meanings of each field when assessing the company's performance.\n"
                "- Compare the company's metrics against industry benchmarks, regulatory limits, and best practice standards.\n"
                "- Take into account any initiatives, targets, or compliance efforts described in the data.\n"
                "- Provide a fair and unbiased evaluation based on the information provided.\n"
                "- Ensure that your final output strictly adheres to the specified JSON schema for the function 'generate_social_scores'."
                "If any field contains 'N/A', ignore that field when calculating the scores."
            )
        },
    ]

    # Prepare the user message with social data, including units and field meanings
    user_message_content = (
        "Please generate the social scores based on the following company data. "
        "Each data point includes the value, units, and a detailed description to assist in your assessment. "
        "Use this information to accurately evaluate the company's performance in each social area, "
        "comparing it to industry standards, regulatory requirements, and best practices.\n\n"
        "Company Social Data:\n\n"
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
        "employee_relations_data": {
            "employee_turnover_rate": {
                "unit": "percentage",
                "meaning": "The rate at which employees leave the company over a period."
            },
            "average_employee_tenure": {
                "unit": "years",
                "meaning": "Average number of years employees stay with the company."
            },
            "employee_satisfaction_score": {
                "unit": "score out of 100",
                "meaning": "Employee satisfaction level based on surveys."
            },
            "number_of_employee_grievances_filed": {
                "unit": "count",
                "meaning": "Total number of grievances filed by employees."
            },
            "union_membership_percentage": {
                "unit": "percentage",
                "meaning": "Percentage of employees who are members of a labor union."
            }
        },
        "diversity_data": {
            "gender_diversity": {
                "percentage_female_employees": {
                    "unit": "percentage",
                    "meaning": "Percentage of employees who are female."
                },
                "percentage_female_leadership": {
                    "unit": "percentage",
                    "meaning": "Percentage of leadership positions held by females."
                }
            },
            "racial_ethnic_diversity": {
                "percentage_diverse_employees": {
                    "unit": "percentage",
                    "meaning": "Percentage of employees from diverse racial/ethnic backgrounds."
                },
                "percentage_diverse_leadership": {
                    "unit": "percentage",
                    "meaning": "Percentage of leadership from diverse racial/ethnic backgrounds."
                }
            },
            "employees_with_disabilities_percentage": {
                "unit": "percentage",
                "meaning": "Percentage of employees with disabilities."
            },
            "diversity_training_hours_per_employee": {
                "unit": "hours",
                "meaning": "Average number of diversity training hours per employee."
            },
            "pay_equity_ratio": {
                "unit": "ratio",
                "meaning": "Ratio comparing pay between different demographic groups."
            }
        },
        "health_safety_data": {
            "workplace_injury_rate": {
                "unit": "incidents per 1,000 employees",
                "meaning": "Number of workplace injuries per 1,000 employees."
            },
            "ltifr": {
                "unit": "rate",
                "meaning": "Lost-Time Injury Frequency Rate."
            },
            "number_of_workplace_fatalities": {
                "unit": "count",
                "meaning": "Total number of fatalities occurring at the workplace."
            },
            "employee_wellness_program_participation": {
                "unit": "percentage",
                "meaning": "Percentage of employees participating in wellness programs."
            },
            "safety_training_hours_per_employee": {
                "unit": "hours",
                "meaning": "Average number of safety training hours per employee."
            }
        },
        "labor_standards_data": {
            "fair_wage_percentage": {
                "unit": "percentage",
                "meaning": "Percentage of employees receiving a fair wage compared to local living wage."
            },
            "number_of_human_rights_violations": {
                "unit": "count",
                "meaning": "Number of reported human rights violations."
            },
            "percentage_supply_chain_audits": {
                "unit": "percentage",
                "meaning": "Percentage of supply chain audited for labor standards."
            },
            "child_labor_violations": {
                "unit": "count",
                "meaning": "Number of child labor or forced labor incidents reported."
            }
        },
        "community_engagement_data": {
            "investment_in_community_projects": {
                "unit": "USD",
                "meaning": "Total investment in community projects."
            },
            "employee_volunteer_hours": {
                "unit": "hours",
                "meaning": "Total number of volunteer hours contributed by employees."
            },
            "percentage_revenue_donated": {
                "unit": "percentage",
                "meaning": "Percentage of company revenue donated to charitable causes."
            },
            "number_of_beneficiaries_impacted": {
                "unit": "count",
                "meaning": "Number of individuals benefited from social programs."
            }
        },
        "product_safety_data": {
            "number_of_product_recalls": {
                "unit": "count",
                "meaning": "Total number of product recalls issued."
            },
            "customer_satisfaction_score": {
                "unit": "score out of 100",
                "meaning": "Customer satisfaction level based on surveys (e.g., NPS)."
            },
            "number_of_product_safety_incidents": {
                "unit": "count",
                "meaning": "Number of reported product safety incidents."
            },
            "compliance_with_product_safety_standards": {
                "unit": "percentage",
                "meaning": "Degree of compliance with product safety standards."
            }
        }
    }

    # Format the social data with units and meanings
    formatted_social_data = format_data_with_units(social_data["social"], field_descriptions)

    # Append the formatted data to the user message content
    user_message_content += json.dumps(formatted_social_data, indent=2)

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
            tool_choice={"type": "function", "function": {"name": "generate_social_scores"}},
        )

        # Extract the function arguments from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            social_data_response = function_data
            return social_data_response
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


async def calculate_social_score(social_data):
    """
    Calculate social scores based on the provided social data.
    """

    social_scores = await generate_social_scores_query(social_data)

    if not social_scores:
        return {}


    # Returning the social scores directly
    return social_scores
