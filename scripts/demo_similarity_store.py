import cv2
from tqdm import trange
from src.similarity_score import match_count_score

DEBUG = False

img_query_filepath = "static\\store_phone\\IMG_9099.jpg"
img_query = cv2.cvtColor(cv2.imread(img_query_filepath), cv2.COLOR_BGR2RGB)

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
        match_count_score(matches=len(good), n_kp1=len(kp_query), n_kp2=len(kp_target))
    )
