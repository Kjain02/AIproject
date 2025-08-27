import json
def generate_schema(input_data):
    schema = {
        "section_name": input_data["section_name"],
        "section_description": input_data["section_description"],
        "attributes": {}
    }

    for attribute in input_data["attributes"]:
        attribute_name = attribute["attribute_name"]
        schema["attributes"][attribute_name] = {}

        for parameter in attribute["parameters"]:
            if 'parameter_name' in parameter:
                parameter_name = parameter["parameter_name"]
                parameter_unit = parameter.get("parameter_unit", "")

                if parameter["parameter_type"] == "array" and "sub_parameters" in parameter:
                    sub_parameters = {
                        sub["sub_parameter_name"]: sub.get("sub_parameter_unit", "")
                        for sub in parameter["sub_parameters"]
                    }
                    schema["attributes"][attribute_name][parameter_name] = sub_parameters
                else:
                    schema["attributes"][attribute_name][parameter_name] = parameter_unit
            else:
                print (f"\n\nError occured at: {parameter}\n\n")

    return schema


# input_data = {
#     "section_name": "Disclosure 305-2: Energy Indirect (Scope 2) GHG Emissions",
#     "section_description": "Disclosure 305-2 outlines the reporting requirements for energy indirect GHG emissions, specifically emissions from the generation of purchased electricity and related energy sources, measured in metric tons of CO2 equivalent. It distinguishes between location-based and market-based emissions metrics and emphasizes the inclusion of various gases in the calculations. This disclosure supports organizations in assessing their indirect emissions and understanding their contribution to total GHG emissions.",
#     "attributes": [
#         {
#             "attribute_name": "Compilation Requirements",
#             "parameters": [
#                 {
#                     "parameter_name": "Gross location-based energy indirect GHG emissions",
#                     "parameter_type": "float",
#                     "parameter_description": "The total gross location-based energy indirect GHG emissions measured in metric tons of CO2 equivalent.",
#                     "parameter_unit": "metric tons CO2e",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "Required to understand the total GHG emissions associated with purchased electricity, heating, and cooling.",
#                     "required": True
#                 },
#                 {
#                     "parameter_name": "Gross market-based energy indirect GHG emissions",
#                     "parameter_type": "float",
#                     "parameter_description": "If applicable, the total gross market-based energy indirect GHG emissions measured in metric tons of CO2 equivalent.",
#                     "parameter_unit": "metric tons CO2e",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "This metric is essential for organizations choosing specific energy sources which may have different emissions profiles.",
#                     "required": False
#                 },
#                 {
#                     "parameter_name": "Gases included in the calculation",
#                     "parameter_type": "array",
#                     "parameter_description": "The types of gases included in calculating energy indirect (Scope 2) GHG emissions.",
#                     "parameter_unit": "",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "Understanding which gases are accounted for aids in assessing the overall impact of indirect emissions.",
#                     "required": False,
#                     "sub_parameters": [
#                         {
#                             "sub_parameter_name": "CO2",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Carbon Dioxide (CO2) is included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "CO2 is a primary greenhouse gas and is usually included.",
#                             "required": True,
#                             "sub_parameter_unit" : "test"

#                         },
#                         {
#                             "sub_parameter_name": "CH4",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Methane (CH4) is included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "Methane has a high Global Warming Potential (GWP) and is often relevant for indirect emissions.",
#                             "required": True
#                         },
#                         {
#                             "sub_parameter_name": "N2O",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Nitrous Oxide (N2O) is included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "N2O is relevant as it also contributes to GHG emissions significantly.",
#                             "required": True
#                         },
#                         {
#                             "sub_parameter_name": "HFCs",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Hydrofluorocarbons (HFCs) are included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "HFCs are often used as substitutes for Ozone Depleting Substances and contribute to GHG emissions.",
#                             "required": True
#                         },
#                         {
#                             "sub_parameter_name": "PFCs",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Perfluorocarbons (PFCs) are included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "PFCs are potent greenhouse gases and may be relevant to energy consumption emissions.",
#                             "required": True
#                         },
#                         {
#                             "sub_parameter_name": "SF6",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Sulphur Hexafluoride (SF6) is included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "SF6 has a very high global warming potential and is important to consider in indirect emissions.",
#                             "required": True
#                         },
#                         {
#                             "sub_parameter_name": "NF3",
#                             "sub_parameter_type": "boolean",
#                             "sub_parameter_description": "Indicates if Nitrogen Trifluoride (NF3) is included in the calculation.",
#                             "sub_parameter_source": "Page 11",
#                             "sub_parameter_explanation": "NF3 is also a greenhouse gas with strong warming potential.",
#                             "required": True
#                         }
#                     ]
#                 },
#                 {
#                     "parameter_name": "Base year for the calculation",
#                     "parameter_type": "string",
#                     "parameter_description": "If applicable, the historical year selected for context in calculating emissions, including rationale and significant changes affecting emissions.",
#                     "parameter_unit": "",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "Essential for tracking emissions reductions or increases over time compared to a fixed point.",
#                     "required": False
#                 },
#                 {
#                     "parameter_name": "Source of emission factors and GWP rates",
#                     "parameter_type": "string",
#                     "parameter_description": "Details on the sources of emission factors and Global Warming Potential (GWP) rates used in the calculations.",
#                     "parameter_unit": "",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "Provides transparency in how calculations were derived, supporting accurate reporting and comparisons.",
#                     "required": True
#                 },
#                 {
#                     "parameter_name": "Consolidation approach for emissions",
#                     "parameter_type": "string",
#                     "parameter_description": "The approach chosen for consolidating emissions which could be equity share, financial control, or operational control.",
#                     "parameter_unit": "",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "Different approaches affect the total reported GHG emissions, thereby impacting stakeholder understanding and decision-making.",
#                     "required": True
#                 },
#                 {
#                     "parameter_name": "Standards, methodologies, assumptions, and/or calculation tools used",
#                     "parameter_type": "string",
#                     "parameter_description": "List of standards, methodologies, assumptions made, and tools used for the calculation of GHG emissions.",
#                     "parameter_unit": "",
#                     "parameter_source": "Page 11",
#                     "parameter_explanation": "Transparency in methodologies ensures credibility and provides a framework for replication or verification.",
#                     "required": True
#                 }
#             ]
#         }
#     ]
# }


# schema = generate_schema(input_data)
# print(schema)

# # with open ('temp.json', 'w') as f:
# #     json.dumps(schema, f, indent=4)

# with open("temp.json", "w") as f:
#     json.dump(schema, f, indent=4)