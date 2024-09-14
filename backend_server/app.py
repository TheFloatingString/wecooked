from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


GROCERY_LIST = ["bananas", "oranges", "cocacola"]


@app.route("/")
def hello_world():
    return "hello"


@app.route("/api/view/client")
def api_current():
    return jsonify({"data": "we cooked."})


@app.route("/api/view/client/completed_item", methods=["GET", "POST"])
def api_view_client_completed_item():
    return jsonify({"substract one"})


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    body = request.values.get("Body").lower()
    resp.message(body)

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
