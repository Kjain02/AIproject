


# system_prompt = '''You are an assistant designed to evaluate whether the values in a given dictionary are appropriate for their respective keys and if the key-value pairs are supported or extracted from a provided page of text. Your task is to:

# 1. Verify if the keys in the dictionary are relevant to the page text.
# 2. Check if the values in the dictionary align with the content or meaning associated with the keys from the page text.
# 3. For each key-value pair, determine if the value makes sense in the context of the key and the page text.
# 4. If the dictionary contains an invalid or irrelevant key-value pair based on the page text, flag it as inappropriate.

# Please follow these steps:
# - For each key in the dictionary, search for the key's relevance in the page text.
# - For each corresponding value, verify if it matches or makes sense in the context of the key and page text.
# - Return a confidence score between 0 and 1 for each key-value pair, where 1 means it is fully appropriate and supported, and 0 means it is not appropriate or unsupported by the page text.
# - If a key-value pair is inappropriate, explain why.
# '''

system_prompt = '''You are an assistant designed to evaluate whether the values in a given dictionary are appropriate for their respective keys and if the key-value pairs are supported or extracted from a provided page of text. Your task is to:

1. Verify if the keys in the dictionary are relevant to the page text.
2. Check if the values in the dictionary align with the content or meaning associated with the keys from the page text.
3. For each key-value pair, determine if the value makes sense in the context of the key and the page text.
4. If the dictionary contains an invalid or irrelevant key-value pair based on the page text, flag it as inappropriate.

Please follow these steps:
- For each key in the dictionary, search for the key's relevance in the page text.
- For each corresponding value, verify if it matches or makes sense in the context of the key and page text.
- Return True or False where True means the Dictionary matches the Extracted Data and False means it does not match the Extracted Data.
'''

# def user_prompt(page_text, response_dict):
#     return f'''Given the following page text and dictionary:

# Page Text: "{page_text}"

# Dictionary: {response_dict}

# For each key-value pair in the dictionary, check if the value is appropriate for the given key in the context of the page text. Determine if the key-value pair can be supported or found in the page text.

# Provide the following output:
# - A confidence score for each key-value pair (from 0 to 1).
# - If the confidence score is low, provide an explanation of why the pair is inappropriate.
# - If the key or value is not supported or doesn't make sense in the context of the page text, explain why.
# '''


def user_prompt(page_text, response_dict):
    return f'''Given the following page text and dictionary:

Page Text: "{page_text}"

Dictionary: {response_dict}

For each key-value pair in the dictionary, check if the value is appropriate for the given key in the context of the page text. Determine if the key-value pair can be supported or found in the page text.

Provide the following output:
- True if the Dictionary matches the Extracted Data and False if it does not match the Extracted Data.
- Give Output as True False Only
'''


tool_template = [
      {
        "type": "function",
        "function": {
          "name": "validate_results",
          "description": "Evaluates the confidence and provides remarks for the validation of extracted data.",
          "parameters": {
            "type": "object",
            "properties": {
              "confidence_score": {
                "type": "string",
                "description": "The confidence score of the validation, indicating the matching between the dictionary results and the text."
              },
              "validation_remarks": {
                "type": "string",
                "description": "A remark providing an explanation or reason for the confidence score (e.g., 'Data extracted from reliable sources', 'Ambiguity in data source')."
              }
            },
            "required": ["confidence_score", "validation_remarks"],
            "additionalProperties": False
          }
        }
      }
    ]