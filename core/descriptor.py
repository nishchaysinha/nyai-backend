import core.prompt_template as prompt_template

def generate_title(chat, event_report):
    title_prompt = prompt_template.title_prompt(event_report)
    response = chat.send_message(title_prompt)
    return response.text

def generate_short_desc(chat, event_report):
    short_desc_prompt = prompt_template.short_desc_prompt(event_report)
    response = chat.send_message(short_desc_prompt)
    return response.text