import google.generativeai as genai
import core.prompt_template as prompt_template
import utils.safetysetter as safety_types

def judgement(event_data_json):
    initial_prompt_template = prompt_template.init_prompt(event_data_json)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(initial_prompt_template, safety_settings=safety_types.safe)
    return response.text

