import time
import requests
import cv2
import base64
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
BASE_URL = "https://d6af-129-97-124-163.ngrok-free.app"
api_key = os.getenv("HTN_OPENAI_API_KEY")


def match_count_score(matches: int, n_kp1: int, n_kp2: int) -> float:
    return 100 * (matches / min(n_kp1, n_kp2))


def run_localization(img_query):
    sift = cv2.SIFT_create()
    kp_query, des_query = sift.detectAndCompute(img_query, None)

    max_similarity_score = -1
    most_similar_img = None

    for i in range(100, 108):
        img_target_query = f"static\\store_phone\\IMG_9{i}.jpg"
        if DEBUG:
            print(img_target_query)
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

        print(
            match_count_score(
                matches=len(good), n_kp1=len(kp_query), n_kp2=len(kp_target)
            )
        )


def is_object_in_image(image_path: str, object_name: str):
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
                        "text": f"Is there {object_name} this image? Only respond with Yes or No.",
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

    return response.json()["choices"][0]["message"]["content"]


while True:
    # perform localization
    time.sleep(1)
    localization_filepath = "static\\localization\\sample_1.jpg"
    img_query = cv2.cvtColor(cv2.imread(localization_filepath), cv2.COLOR_BGR2RGB)
    img_query = cv2.resize(img_query, (256, 256))
    run_localization(img_query=img_query)

    # cv2.imshow("frame", img)
    # cv2.waitKey()

    resp = requests.post(f"{BASE_URL}/api/view/client")
    print(resp.json())
    grocery_list = resp.json()["grocery_list"]

    # tap
    input("press enter to tap:")

    # detect object of interest
    detection_filepath = "static\\detection\\cocacola.jpg"
    img = cv2.imread(detection_filepath)
    img = cv2.resize(img, (256, 256))
    cv2.imwrite("tmp.jpg", img)

    resp = is_object_in_image(image_path="tmp.jpg", object_name=grocery_list[0])
    print(resp)

    # cv2.imshow("frame", img)
    # cv2.waitKey()

    resp = requests.post(f"{BASE_URL}/api/view/client/completed_item")
    print(resp)

    # tap
    input("press enter to tap:")
    print(len(grocery_list))

    if len(grocery_list) <= 1:
        break
