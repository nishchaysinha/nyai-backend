import json
import re

def filter_json(text_response):
    # Find the first occurrence of '{' and the last occurrence of '}'
    start = text_response.find('{')
    end = text_response.rfind('}') + 1  # '+1' to include the '}' in the slice

    # Extract the JSON string
    json_str = text_response[start:end]

    # Convert the JSON string to a dictionary

    return json_str