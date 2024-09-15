from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from twilio.twiml.messaging_response import MessagingResponse
import cv2
from dotenv import load_dotenv

load_dotenv()
import os
import cohere
import requests
import numpy as np


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


GROCERY_LIST = []
ORIGINAL_GROCERY_LIST = []
LATITUDE = 43.471759983680
LONGITUDE = -80.53858848369224
sift = cv2.SIFT_create()


coordinates_dict = {
    "corner_1": (43.47173942543805, -80.53866917414487),
    "corner_2": (43.47164247930744, -80.5387775283001),
    "corner_4": (43.47156229364812, -80.53863486981209),
    "corner_3": (43.47165225659944, -80.53853125699004),
}


def match_count_score(matches: int, n_kp1: int, n_kp2: int) -> float:
    return 100 * (matches / min(n_kp1, n_kp2))


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
    global LATITUDE
    global LONGITUDE

    json_resp = request.json
    print(json_resp)

    sift = cv2.SIFT_create()
    kp_query, des_query = sift.detectAndCompute(
        np.asarray(json_resp["data"], dtype=np.uint8), None
    )
    cv2.imwrite("curr_frame.png", np.asarray(json_resp["data"], dtype=np.uint8))

    max_similarity_score = -1
    most_similar_corner = -1

    for i in range(1, 5):
        img_target_query = f"static\\img\\corner_{i}.jpg"
        # if DEBUG:
        #     print(img_target_query)
        target_img = cv2.cvtColor(cv2.imread(img_target_query), cv2.COLOR_BGR2RGB)
        kp_target, des_target = sift.detectAndCompute(target_img, None)

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des_query, des_target, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        curr_score = match_count_score(
            matches=len(good), n_kp1=len(kp_query), n_kp2=len(kp_target)
        )

        if curr_score > max_similarity_score:
            max_similarity_score = curr_score
            most_similar_corner = i

    LATITUDE = coordinates_dict[f"corner_{i}"][0]
    LONGITUDE = coordinates_dict[f"corner_{i}"][1]

    print(get_current_state())

    return jsonify({"data": True})


@app.route("/api/view/dashboard")
@cross_origin()
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
