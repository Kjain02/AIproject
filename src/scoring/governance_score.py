import json
import asyncio
from src.azure_credentials import *
from openai import AzureOpenAI

async def generate_governance_scores_query(governance_data):
    """
    Queries the OpenAI API to generate governance scores based on governance data.
    """
    # Define the function (tool)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_governance_scores",
                "description": "Generates governance scores based on provided company governance data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                                "board_structure_independence": {
                                    "type": "number",
                                    "description": "Score for the company's board structure and independence."
                                },
                                "executive_compensation": {
                                    "type": "number",
                                    "description": "Score for executive compensation practices."
                                },
                                "shareholder_rights_transparency": {
                                    "type": "number",
                                    "description": "Score for shareholder rights and transparency."
                                },
                                "audit_risk_management": {
                                    "type": "number",
                                    "description": "Score for audit and risk management practices."
                                },
                                "ethical_business_practices": {
                                    "type": "number",
                                    "description": "Score for the company's ethical business practices."
                                },
                                "succession_planning_leadership_stability": {
                                    "type": "number",
                                    "description": "Score for succession planning and leadership stability."
                                },
                                "stakeholder_engagement": {
                                    "type": "number",
                                    "description": "Score for stakeholder engagement efforts."
                                }
                            }
                        }
                    },
                    "required": ["board_structure_independence", "executive_compensation", "shareholder_rights_transparency",],
                    "additionalProperties": False
                },       
    ]
    
    # Prepare the system message with enhanced prompts
    messages = [
        {
            "role": "system",
            "content": (
                "The scores must be between 25 and 98. 25 being the worst and 98 being the best. "
                "You are an expert in corporate governance analysis with extensive knowledge of global industry standards, regulatory requirements, "
                "and best practices in governance performance assessment. You will be provided with detailed governance data for a company, "
                "including the numerical values, units of measurement, and comprehensive descriptions of each metric's significance. "
                "Your task is to critically evaluate this data and generate objective scores for each specified governance factor. "
                "\n\n"
                "Instructions:\n"
                "- Each score should be an integer between 25 and 98, where 25 represents the worst performance and 98 represents the best performance.\n"
                "- Carefully consider the units and meanings of each field when assessing the company's performance.\n"
                "- Compare the company's metrics against industry benchmarks, regulatory limits, and best practice standards.\n"
                "- Take into account any initiatives, policies, or compliance efforts described in the data.\n"
                "- Provide a fair and unbiased evaluation based on the information provided.\n"
                "- Ensure that your final output strictly adheres to the specified JSON schema for the function 'generate_governance_scores'."
                "If any field contains 'N/A', ignore that field when calculating the scores."
            )
        },
    ]

    # Prepare the user message with governance data, including units and field meanings
    user_message_content = (
        "Please generate the governance scores based on the following company data. "
        "Each data point includes the value, units, and a detailed description to assist in your assessment. "
        "Use this information to accurately evaluate the company's performance in each governance area, "
        "comparing it to industry standards, regulatory requirements, and best practices.\n\n"
        "Company Governance Data:\n\n"
    )

    # Function to add units and descriptions to each field
    def format_data_with_units(data, field_descriptions):
        formatted_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                sub_descriptions = field_descriptions.get(key, {})
                if isinstance(value, list):
                    formatted_list = []
                    for item in value:
                        formatted_list.append(format_data_with_units(item, sub_descriptions))
                    formatted_data[key] = formatted_list
                else:
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
        "board_structure_data": {
            "number_of_board_members": {
                "unit": "count",
                "meaning": "Total number of board members."
            },
            "percentage_independent_board_members": {
                "unit": "percentage",
                "meaning": "Percentage of board members who are independent."
            },
            "average_board_member_tenure": {
                "unit": "years",
                "meaning": "Average tenure of board members."
            },
            "gender_ethnic_diversity": {
                "percentage_gender_diverse_board_members": {
                    "unit": "percentage",
                    "meaning": "Percentage of board members who are female."
                },
                "percentage_ethnically_diverse_board_members": {
                    "unit": "percentage",
                    "meaning": "Percentage of board members from diverse ethnic backgrounds."
                }
            }
        },
        "executive_compensation_data": {
            "ceo_to_employee_pay_ratio": {
                "unit": "ratio",
                "meaning": "Ratio of CEO pay to median employee pay."
            },
            "total_compensation_for_top_executives": {
                "unit": "million INR",
                "meaning": "Total compensation paid to top executives in million INR."
            },
            "performance_based_pay_percentage": {
                "unit": "percentage",
                "meaning": "Percentage of executive compensation that is performance-based."
            },
            "median_employee_compensation": {
                "unit": "lakh INR",
                "meaning": "Median compensation for employees in lakh INR."
            },
            "total_executive_compensation_unit": {
                "unit": "currency unit",
                "meaning": "Unit of currency for total executive compensation."
            },
            "percentage_executive_compensation_revenue_unit": {
                "unit": "percentage",
                "meaning": "Executive compensation as a percentage of revenue."
            },
            "percentage_executive_compensation_expenses_unit": {
                "unit": "percentage",
                "meaning": "Executive compensation as a percentage of expenses."
            }
        },
        "shareholder_rights_data": {
            "voting_rights_per_share_class": {
                "class_name": {
                    "unit": "string",
                    "meaning": "Name of the share class."
                },
                "voting_rights": {
                    "unit": "number",
                    "meaning": "Voting rights per share for this class."
                }
            },
            "shareholder_proposal_submission_rates": {
                "unit": "percentage",
                "meaning": "Rate at which shareholders submit proposals."
            },
            "number_of_shareholder_meetings": {
                "unit": "count",
                "meaning": "Number of shareholder meetings held."
            },
            "disclosure_level_based_on_esg": {
                "gri_disclosure": {
                    "unit": "percentage",
                    "meaning": "Disclosure level based on GRI framework."
                },
                "sasb_disclosure": {
                    "unit": "percentage",
                    "meaning": "Disclosure level based on SASB framework."
                }
            }
        },
        "audit_risk_data": {
            "percentage_independent_audit_committee_members": {
                "unit": "percentage",
                "meaning": "Percentage of audit committee members who are independent."
            },
            "number_of_financial_restatements": {
                "unit": "count",
                "meaning": "Number of times financial statements were restated."
            },
            "audit_fees_paid": {
                "unit": "USD",
                "meaning": "Fees paid for auditing services in USD."
            },
            "internal_control_failures_identified": {
                "unit": "count",
                "meaning": "Number of internal control failures identified."
            }
        },
        "ethical_business_data": {
            "number_of_corruption_bribery_incidents": {
                "unit": "count",
                "meaning": "Number of reported incidents of corruption or bribery."
            },
            "anti_corruption_policy_compliance_rate": {
                "unit": "percentage",
                "meaning": "Compliance rate with anti-corruption policies."
            },
            "number_of_whistleblower_reports": {
                "unit": "count",
                "meaning": "Number of whistleblower reports filed."
            },
            "code_of_ethics_violations": {
                "unit": "count",
                "meaning": "Number of code of ethics violations."
            }
        },
        "succession_planning_data": {
            "number_of_leadership_transitions": {
                "unit": "count",
                "meaning": "Number of leadership transitions (e.g., CEO, CFO)."
            },
            "average_tenure_senior_executives": {
                "unit": "years",
                "meaning": "Average tenure of senior executives."
            },
            "number_of_internal_promotions_to_executive_roles": {
                "unit": "count",
                "meaning": "Number of internal promotions to executive roles."
            },
            "number_of_external_hires_for_executive_roles": {
                "unit": "count",
                "meaning": "Number of external hires for executive roles."
            }
        },
        "stakeholder_engagement_data": {
            "number_of_stakeholder_meetings": {
                "unit": "count",
                "meaning": "Number of stakeholder meetings held."
            },
            "percentage_stakeholders_consulted_in_decision_making": {
                "unit": "percentage",
                "meaning": "Percentage of stakeholders consulted in decision-making processes."
            },
            "stakeholder_engagement_survey_results": {
                "unit": "score out of 100",
                "meaning": "Stakeholder engagement survey satisfaction score."
            },
            "number_of_stakeholder_feedback_comments": {
                "unit": "count",
                "meaning": "Number of stakeholder feedback comments disclosed."
            }
        }
    }

    # Format the governance data with units and meanings
    formatted_governance_data = format_data_with_units(governance_data["governance"], field_descriptions)

    # Append the formatted data to the user message content
    user_message_content += json.dumps(formatted_governance_data, indent=2)

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
            tool_choice={"type": "function", "function": {"name": "generate_governance_scores"}},
        )

        # Extract the function arguments from the response
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # Extract the arguments from the first tool call
            function_arguments = tool_calls[0].function.arguments
            function_data = json.loads(function_arguments)
            governance_data_response = function_data
            return governance_data_response
        else:
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


async def calculate_governance_score(governance_data):
    """
    Calculate governance scores based on the provided governance data.
    """

    governance_scores = await generate_governance_scores_query(governance_data)

    if not governance_scores:
        return {}
    return governance_scores
