import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import core.llm as llm
import core.prompt_template as prompt_template
import utils.filter_json as filter_json
import utils.id_generator as id_generator
import random
import json
from ocr_utils.img_convert import base64_to_image
from ocr_utils.ocr import ocr


from flask_cors import CORS
from structures.event_object import *
from core.descriptor import *

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from core.judgement import judgement

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
        final_json["_id"] = id_generator.generate_case_id()  # Generate a new _id for each document
        final_json['case_id'] = final_json["_id"]
        final_json['sender'] = request.json['sender']
        final_json['receiver'] = request.json['receiver']
        final_json['event_report'] = request.json['event_report']
        final_json['event_proof'] = request.json['event_proof']
        final_json['event_proof_ocr'] = []
        for i in range(len(final_json['event_proof'])):
            
            image = base64_to_image(final_json['event_proof'][i])

            final_json['event_proof_ocr'].append(ocr(image))
            

        final_json['title'] = generate_title(final_json['event_report'])
        final_json['short_desc'] = generate_short_desc(final_json['event_report'])

        # Store data in MongoDB
        client.db.events.insert_one(final_json)
        return jsonify({"case_id": final_json["case_id"]})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/reply_to_case', methods=['POST'])
def reply_to_case():
    try:
        case_id = request.json['case_id']
        # Get the case from the database
        case = client.db.events.find_one({"case_id": case_id})
        if case is None:
            return jsonify({"error": "Case not found."})
        if case['approval'] != "pending":
            return jsonify({"error": "Case already approved or rejected."})
        # Update the case with the receiver's report and proof
        case['receiver_report'] = request.json['receiver_report']
        case['receiver_proof'] = request.json['receiver_proof']
        # run judgement check
        judge = judgement(case)
        judge = filter_json.filter_json(judge)
        judge = json.loads(judge)
        case['judgement'] = judge['judgement']
        case['reasoning'] = judge['reasoning']
        case['confidence'] = judge['confidence']
        if float(case["confidence"]) < 0.75:
            case['approval'] = "False"
        else:
            case['approval'] = "True"
        # Store the updated case in the database
        client.db.events.update_one({"case_id": case_id}, {"$set": case})
        return jsonify(case)

        return jsonify(case)
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(debug=True)

