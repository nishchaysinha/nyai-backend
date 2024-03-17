import re
import json
from flask import jsonify

def filter_json(input_string):
    match = re.search(r'\{.*\}', input_string, re.DOTALL)
    if match:
        json_string = match.group()
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError as e:
            return json.dumps({})
    else:
        return json.dumps({})
