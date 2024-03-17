import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import core.llm as llm
import core.prompt_template as prompt_template
import utils.filter_json as filter_json

from structures.event_object import *
from core.descriptor import *

load_dotenv()

app = Flask(__name__)
GM = llm.GenerativeModel("gemini-pro", os.getenv("GOOGLE_API_KEY"))
chat = GM.chat_object()

@app.route('/init', methods=['POST'])
def init():
    try:
        final_json = event_default
        final_json['sender'] = request.json['sender']
        final_json['receiver'] = request.json['receiver']
        final_json['event_report'] = request.json['event_report']
        final_json['event_proof'] = request.json['event_proof']

        final_json['title'] = generate_title(chat, final_json['event_report'])
        final_json['short_desc'] = generate_short_desc(chat, final_json['event_report'])



        return jsonify(final_json)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/reportform', methods=['POST'])
def generate():
    try:
        response_text = request.json['response_text']
        response_prompt = prompt_template.generate_prompt(str(response_text))
        response = chat.send_message(response_prompt)
        response_text = filter_json.filter_json(response.text)
        return jsonify(response_text)
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(debug=True)

