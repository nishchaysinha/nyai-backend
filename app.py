import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import core.llm as llm
import core.prompt_template as prompt_template
import utils.filter_json as filter_json
import utils.id_generator as id_generator
import random
from flask_cors import CORS


from structures.event_object import *
from core.descriptor import *

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)
cors = CORS(app)

GM = llm.GenerativeModel("gemini-pro", os.getenv("GOOGLE_API_KEY"))
chat = GM.chat_object()

@app.route('/ping')
def ping():
    return jsonify({"pong": random.randint(0, 100)})

@app.route('/create_case', methods=['POST'])
def create_case():
    try:
        final_json = event_default
        final_json["case_id"] = id_generator.generate_case_id()
        final_json['sender'] = request.json['sender']
        final_json['receiver'] = request.json['receiver']
        final_json['event_report'] = request.json['event_report']
        final_json['event_proof'] = request.json['event_proof']

        final_json['title'] = generate_title(chat, final_json['event_report'])
        final_json['short_desc'] = generate_short_desc(chat, final_json['event_report'])

        #store data in mongodb
        client.db.events.insert_one(final_json)

        return jsonify({"case_id": final_json["case_id"]})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/reply_to_case', methods=['POST'])
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

