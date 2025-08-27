import json

def transform_to_openai_function_template(input_data):
    """
    Converts structured input data to an OpenAI-compatible function call template.
    
    Args:
        input_data (dict): Input data describing attributes and parameters.

    Returns:
        dict: OpenAI function call template.
    """
    def build_properties(parameter):
        """Helper function to build the properties schema for parameters and sub-parameters."""
        properties = {}
        required_fields = []

        # General fields for a parameter
        fields = {
            "value": {
                "type": "string",
                "description": parameter.get("parameter_description", "The value of the parameter, It should be logical value that contains some numerical value without the unit or some Descriptive text relevant to section description, name")
            },
            "source": {
                "type": "integer",
                "description": "The source from which the value is derived, identified by chunk's page number in format <page_number>{{page_num}}<page_number>, Need to return {{page_num}} as integer"
            },
            "explanation": {
                "type": "string",
                "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
            },
            "unit": {
                "type": "string",
                "description": """Unit of measurement for the value, Depending in text, it can be # Currency Units 'USD', 'EUR', 'GBP', 'INR', 'JPY', 'CNY', 'CAD', 'AUD', 'CHF', 'SEK', 'SGD', 'HKD', 'KRW', 'BRL', 'RUB', 'ZAR', 'AED', 'SAR', 'QAR', 'KWD', 'MXN', 'kilogram', 'kg', 'ton', 'tonne', 'metric ton', 'pound', 'lb', 'ounce', 'oz', 'meter', 'm', 'kilometer', 'km', 'mile', 'mi', 'yard', 'yd', 'foot', 'ft', 'inch', 'in', 'square meter', 'm²', 'square kilometer', 'km²', 'hectare', 'ha', 'acre', 'cubic meter', 'm³', 'liter', 'L', 'milliliter', 'mL', 'barrel', 'bbl', 'gallon', 'gal', 'joule', 'J', 'kilojoule', 'kJ', 'megajoule', 'MJ', 'gigajoule', 'GJ', 'calorie', 'cal','kilocalorie', 'kcal', 'BTU', 'megawatt-hour', 'MWh', 'kilowatt-hour', 'kWh', 'watt', 'W', 'kilowatt', 'kW', 'megawatt', 'MW', 'gigawatt', 'GW', 'horsepower', 'hp', 'kilometer per hour', 'km/h', 'mile per hour', 'mph', 'second', 's', 'minute', 'min', 'hour', 'h', 'day', 'd', 'week', 'wk', 'month', 'mo', 'year', 'yr', 'pascal', 'Pa', 'kilopascal', 'kPa', 'bar', 'atmosphere', 'atm', 'psi', 'celsius', '°C', 'fahrenheit', '°F', 'kelvin', 'K', 'hertz', 'Hz', 'megahertz', 'MHz', 'gigahertz', 'GHz','volt', 'V', 'kilovolt', 'kV', 'ampere', 'A', 'milliampere', 'mA', 'ohm', 'Ω', 'kilowatt-hour', 'kWh','bit', 'b', 'byte', 'B', 'kilobyte', 'KB', 'megabyte', 'MB', 'gigabyte', 'GB', 'terabyte', 'TB','basis point', 'bps', 'percentage', '%', 'P/E ratio', 'EPS', 'dividend yield', 'market cap', 'ROE', 'ROI', 'CAGR', 'EBITDA', 'gross margin', 'net margin', 'debt-to-equity ratio', 'price-to-book ratio', 'current ratio', 'quick ratio', 'barrel per day', 'bpd', 'tonnes per annum', 'tpa', 'million cubic feet per day', 'MMcfd', 'mole', 'mol', 'lumen', 'lm', 'lux', 'lx', 'candela', 'cd', 'N/m²' But If It donot Match Any the Give 'N/A' """
            }
        }

        # if the unit.description is empty, add a default description
        if not fields["unit"]["description"] or isinstance(fields["unit"]["description"], str) and len(fields["unit"]["description"].strip()) == 0:
            fields["unit"]["description"] = "The unit of measurement for the value"
        
        if not fields["value"]["description"] or isinstance(fields["value"]["description"], str) and len(fields["value"]["description"].strip()) == 0:
            fields["value"]["description"] = "The value of the parameter"

        # Add fields to properties
        for field_name, field_schema in fields.items():
            properties[field_name] = field_schema
            required_fields.append(field_name)

        return properties, required_fields

    def process_sub_parameters(sub_parameters):
        """Process sub-parameters into OpenAI schema format."""
        sub_properties = {}
        sub_required = []

        for sub_param in sub_parameters:
            sub_name = sub_param.get("sub_parameter_name")
            if not sub_name:
                continue

            sub_properties[sub_name] = {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "boolean",
                        "description": sub_param.get("sub_parameter_description", "The value of the sub-parameter")
                    },
                    "source": {
                        "type": "integer",
                        "description": "The source from which the value is derived, identified by chunk's page number in format <page_number>{{page_num}}<page_number>, Need to return {{page_num}} as integer"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Justification for why the model chose this value, which may include citing or directly quoting the line from the chunk"
                    },
                    "unit": {
                        "type": "string",
                        "description": """Unit of measurement for the value, Depending in text, it can be # Currency Units 'USD', 'EUR', 'GBP', 'INR', 'JPY', 'CNY', 'CAD', 'AUD', 'CHF', 'SEK', 'SGD', 'HKD', 'KRW', 'BRL', 'RUB', 'ZAR', 'AED', 'SAR', 'QAR', 'KWD', 'MXN', 'kilogram', 'kg', 'ton', 'tonne', 'metric ton', 'pound', 'lb', 'ounce', 'oz', 'meter', 'm', 'kilometer', 'km', 'mile', 'mi', 'yard', 'yd', 'foot', 'ft', 'inch', 'in', 'square meter', 'm²', 'square kilometer', 'km²', 'hectare', 'ha', 'acre', 'cubic meter', 'm³', 'liter', 'L', 'milliliter', 'mL', 'barrel', 'bbl', 'gallon', 'gal', 'joule', 'J', 'kilojoule', 'kJ', 'megajoule', 'MJ', 'gigajoule', 'GJ', 'calorie', 'cal','kilocalorie', 'kcal', 'BTU', 'megawatt-hour', 'MWh', 'kilowatt-hour', 'kWh', 'watt', 'W', 'kilowatt', 'kW', 'megawatt', 'MW', 'gigawatt', 'GW', 'horsepower', 'hp', 'kilometer per hour', 'km/h', 'mile per hour', 'mph', 'second', 's', 'minute', 'min', 'hour', 'h', 'day', 'd', 'week', 'wk', 'month', 'mo', 'year', 'yr', 'pascal', 'Pa', 'kilopascal', 'kPa', 'bar', 'atmosphere', 'atm', 'psi', 'celsius', '°C', 'fahrenheit', '°F', 'kelvin', 'K', 'hertz', 'Hz', 'megahertz', 'MHz', 'gigahertz', 'GHz','volt', 'V', 'kilovolt', 'kV', 'ampere', 'A', 'milliampere', 'mA', 'ohm', 'Ω', 'kilowatt-hour', 'kWh','bit', 'b', 'byte', 'B', 'kilobyte', 'KB', 'megabyte', 'MB', 'gigabyte', 'GB', 'terabyte', 'TB','basis point', 'bps', 'percentage', '%', 'P/E ratio', 'EPS', 'dividend yield', 'market cap', 'ROE', 'ROI', 'CAGR', 'EBITDA', 'gross margin', 'net margin', 'debt-to-equity ratio', 'price-to-book ratio', 'current ratio', 'quick ratio', 'barrel per day', 'bpd', 'tonnes per annum', 'tpa', 'million cubic feet per day', 'MMcfd', 'mole', 'mol', 'lumen', 'lm', 'lux', 'lx', 'candela', 'cd', 'N/m²' But If It donot Match Any the Give 'N/A' """
                    }
                },
                "required": ["value", "source", "explanation", "unit"],
            }

            # if the unit.description is empty, add a default description
            if not sub_properties[sub_name]["properties"]["unit"]["description"] or isinstance(sub_properties[sub_name]["properties"]["unit"]["description"], str) and len(sub_properties[sub_name]["properties"]["unit"]["description"].strip()) == 0:
                sub_properties[sub_name]["properties"]["unit"]["description"] = "The unit of measurement for the value"

            if not sub_properties[sub_name]["properties"]["value"]["description"] or isinstance(sub_properties[sub_name]["properties"]["value"]["description"], str) and len(sub_properties[sub_name]["properties"]["value"]["description"].strip()) == 0:
                sub_properties[sub_name]["properties"]["value"]["description"] = "The value of the sub-parameter"
            

            sub_required.append(sub_name)

        return sub_properties, sub_required

    # Initialize OpenAI-compatible template
    open_ai_template = {
        "type": "function",
        "function": {
            "name": "extraction_function",
            "description": input_data.get("section_description", ""),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    }

    all_required_parameters = []

    for attribute in input_data.get("attributes", []):
        if "parameters" in attribute:
            try:
                for parameter in attribute.get("parameters", []):
                    param_name = parameter.get("parameter_name")
                    if not param_name:
                        continue

                    param_dict = {"type": "object"}

                    # Handle sub-parameters if present
                    if "sub_parameters" in parameter and len(parameter["sub_parameters"]) > 0:
                        sub_properties, sub_required = process_sub_parameters(parameter["sub_parameters"])
                        param_dict["properties"] = sub_properties
                        param_dict["required"] = sub_required
                    else:
                        # Standard parameter processing
                        properties, required_fields = build_properties(parameter)
                        param_dict["properties"] = properties
                        param_dict["required"] = required_fields

                    # Add parameter to the properties
                    open_ai_template["function"]["parameters"]["properties"][param_name] = param_dict
                    if parameter.get("required", False):
                        all_required_parameters.append(param_name)
            except Exception as e:
                continue

    # Add all required parameters to the schema
    open_ai_template["function"]["parameters"]["required"] = all_required_parameters

    return open_ai_template


# input_data = {
#     "section_name": "Section G: Social Impact and Community Engagement",
#     "section_description": "This section highlights the company's involvement in community engagement, social responsibility initiatives, and the impact of its operations on surrounding communities. It specifically outlines social programs, CSR projects, and regular assessments of these initiatives to gauge their effectiveness and reach.",
#     "attributes": [
#         {
#             "attribute_name": "Social Programs",
#             "parameters": [
#                 {
#                     "parameter_name": "Name of Program",
#                     "parameter_type": "string",
#                     "parameter_description": "The name of the social program implemented by the company.",
#                     "parameter_unit": "",
#                     "parameter_source": "Section G",
#                     "parameter_explanation": "Identifies specific initiatives aimed at community engagement and social impact.",
#                     "required": True,
#                     "sub_parameters": []
#                 },
#                 {
#                     "parameter_name": "Target Beneficiaries",
#                     "parameter_type": "string",
#                     "parameter_description": "The groups of individuals targeted by the social program, such as children, women, or the elderly.",
#                     "parameter_unit": "",
#                     "parameter_source": "Section G",
#                     "parameter_explanation": "Clarifies whom the program aims to benefit in the community.",
#                     "required": True,
#                     "sub_parameters": []
#                 },
#                 {
#                     "parameter_name": "Duration of Program",
#                     "parameter_type": "string",
#                     "parameter_description": "The time period for which the social program is executed.",
#                     "parameter_unit": "Months",
#                     "parameter_source": "Section G",
#                     "parameter_explanation": "Shows commitment and planning in community engagement efforts.",
#                     "required": True,
#                     "sub_parameters": []
#                 },
#                 {
#                     "parameter_name": "Budget Allocated",
#                     "parameter_type": "number",
#                     "parameter_description": "The financial resources allocated to the social program.",
#                     "parameter_unit": "INR",
#                     "parameter_source": "Section G",
#                     "parameter_explanation": "Indicates the scale and seriousness of the program through funding.",
#                     "required": True,
#                     "sub_parameters": []
#                 },
#                 {
#                     "parameter_name": "Outcome Measurement",
#                     "parameter_type": "string",
#                     "parameter_description": "The methods used to measure the effectiveness and outcomes of the program.",
#                     "parameter_unit": "",
#                     "parameter_source": "Section G",
#                     "parameter_explanation": "Ensures accountability and assesses impact on the community.",
#                     "required": True,
#                     "sub_parameters": []
#                 }
#             ]
#         }
#     ],
#     "sub_parameters": [],
#     "required": True
# }
# ans = transform_to_openai_function_template(input_data)

# with open(f'../output/function_templates/{input_data["section_name"].replace(" ", "_")}.json', 'w') as f:
#     json.dump(ans, f, indent = 4)

