import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI API Key
api_key = os.getenv("HTN_OPENAI_API_KEY")


def is_cocacola(image_path):
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Is there coca-cola can this image? Only respond with Yes or No.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    # print(response.json())

    return response.json()


print(is_cocacola("static\\IMG_9096.jpg")["choices"][0]["message"]["content"])
print(is_cocacola("static\\IMG_9097.jpg")["choices"][0]["message"]["content"])
