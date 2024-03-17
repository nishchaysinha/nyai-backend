import google.generativeai as genai
import core.prompt_template as prompt_template
import utils.safetysetter as safety_types

def generate_title(event_report):
    title_prompt = prompt_template.title_prompt(event_report)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(title_prompt)
    return response.text

def generate_short_desc(event_report):
    short_desc_prompt = prompt_template.short_desc_prompt(event_report)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(short_desc_prompt, safety_settings=safety_types.safe)
    return response.text