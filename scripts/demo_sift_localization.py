import cv2
import matplotlib.pyplot as plt
import numpy as np

start_filepath = "static/IMG_9077.jpg"
end_filepath = "static/IMG_9077.jpg"
target_filepath = "static/IMG_9078.jpg"

start_img = cv2.cvtColor(cv2.imread(start_filepath), cv2.COLOR_BGR2RGB)
end_img = cv2.cvtColor(cv2.imread(end_filepath), cv2.COLOR_BGR2RGB)
target_img = cv2.cvtColor(cv2.imread(target_filepath), cv2.COLOR_BGR2RGB)


# cv2.imwrite("start_img.jpg",start_img)


sift = cv2.SIFT_create()

kp_start, des_start = sift.detectAndCompute(start_img, None)
kp_end, des_end = sift.detectAndCompute(end_img, None)
kp_target, des_target = sift.detectAndCompute(target_img, None)

# bf = cv2.BFMatcher()
# matches = bf.knnMatch(des_start, des_target, k=2)

# good = []

# for m, n in matches:
#     if m.distance < 0.30 * n.distance:
#         good.append([m])

# Initiate SIFT detector
sift = cv2.SIFT_create()

# # find the keypoints and descriptors with SIFT
# kp1, des1 = sift.detectAndCompute(kp_start, None)
# kp2, des2 = sift.detectAndCompute(kp_end, None)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des_start, des_target, k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

# img_res = cv2.drawMatchesKnn(
#     start_img,
#     kp_start,
#     target_img,
#     kp_target,
#     good,
#     None,
#     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
# )

src_pts = np.float32([kp_start[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
dst_pts = np.float32([kp_target[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

print(M)

# plt.imshow(img_res)
# plt.show()

"""
matches = sorted(matches, key=lambda x:x.distance)
good_matches = matches[:10]

src_pts = np.float32([kp_start[m.queryIndex].pt for m in good_matches])
dst_pts = np.float32([kp_target[m.trainIndex].pt for m in good_matches])

print(src_pts)
print(dst_pts)
"""
