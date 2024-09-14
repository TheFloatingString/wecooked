from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "hello"


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
