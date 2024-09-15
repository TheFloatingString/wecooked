import time
import requests
import cv2
import base64
import numpy as np

# grocery_list = ["coca-cola", "bananas", "orange", "snicker-bar"]
BASE_URL = "https://d6af-129-97-124-163.ngrok-free.app"

while True:
    # perform localization
    time.sleep(1)
    localization_filepath = "static\\localization\\sample_1.jpg"
    img = cv2.cvtColor(cv2.imread(localization_filepath), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))
    cv2.imshow("frame", img)
    cv2.waitKey()

    resp = requests.post(f"{BASE_URL}/api/view/client")
    print(resp.json())
    grocery_list = resp.json()["data"]

    # tap
    input("press enter to tap:")

    # detect object of interest
    detection_filepath = "static\\detection\\cocacola.jpg"
    img = cv2.cvtColor(cv2.imread(detection_filepath), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))
    cv2.imshow("frame", img)
    cv2.waitKey()

    # print(grocery_list)
    # grocery_list.pop()
    resp = requests.post(f"{BASE_URL}/api/view/client/completed_item")
    # print(resp.json())

    # tap
    input("press enter to tap:")
    print(len(grocery_list))

    if len(grocery_list) <= 1:
        break
