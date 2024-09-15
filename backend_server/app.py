from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import cv2
from dotenv import load_dotenv

load_dotenv()
import os
import cohere
import requests


app = Flask(__name__)


GROCERY_LIST = []
ORIGINAL_GROCERY_LIST = []
LATITUDE = 43.471759983680
LONGITUDE = -80.53858848369224
sift = cv2.SIFT_create()


def create_prompt(user_resp) -> str:
    return f'Rewrite the following as a list of food, all lowercase, no spaces separting but commas separating and only keep food nouns: "{user_resp}"'


def return_user_instruction() -> str:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    text_list = co.chat(
        message="Generate generic grocery store navigation in less than 10 words. Do not generate any newlines."
    )
    return text_list.text


def get_current_state() -> dict:
    global ORIGINAL_GROCERY_LIST
    global GROCERY_LIST
    global LATITUDE
    global LONGITUDE
    state_dict = {
        "original_grocery_list": ORIGINAL_GROCERY_LIST,
        "live_grocery_list": GROCERY_LIST,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "instruction": return_user_instruction(),
        "img_uri": "https://d6af-129-97-124-163.ngrok-free.app/static/img/generic.jpg",
    }
    return state_dict


def post_to_frontend():
    POST_URL = ""
    resp = requests.post(POST_URL, json=get_current_state())


@app.route("/")
def hello_world():
    return "hello"


@app.route("/api/update_location", methods=["GET", "POST"])
def api_update_location():
    json_resp = request.json
    print(json_resp)
    return jsonify({"data": True})


@app.route("/api/view/dashboard")
def api_view_dashboard():
    return jsonify(get_current_state())


@app.route("/api/view/client", methods=["GET", "POST"])
def api_current():
    global GROCERY_LIST
    return jsonify({"grocery_list": GROCERY_LIST})


@app.route("/api/view/client/completed_item", methods=["GET", "POST"])
def api_view_client_completed_item():
    global GROCERY_LIST
    GROCERY_LIST.pop(0)
    return jsonify({"data": "substract one"})


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    global GROCERY_LIST
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    body = request.values.get("Body").lower()

    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    text_list = co.chat(message=create_prompt(body))
    resp.message(text_list.text)

    GROCERY_LIST = list(text_list.text.split(","))
    ORIGINAL_GROCERY_LIST = GROCERY_LIST.copy()
    print(GROCERY_LIST)

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
