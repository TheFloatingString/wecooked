import time

grocery_list = ["coca-cola", "bananas", "orange", "snicker-bar"]

while len(grocery_list) > 0:
    # perform localization
    time.sleep(1)

    # detect object of interest
    print(grocery_list)
    grocery_list.pop()
