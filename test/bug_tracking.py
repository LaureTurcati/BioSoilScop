# bug tracking functions

import numpy as np
import matplotlib.pyplot as plt 
import time 
import cv2 


def detect_shape(picture, render_detected_shapes=False):
    ##### paramètres
    # flou 
    blur_kernel = 9 # 13 5
    # canny 
    canny_threshold_1 = 10 # 10 40 5 avec 40 très peu de faux négatifs, avec 5 beaucoup de faux négatifs
    canny_threshold_2 = 3*canny_threshold_1
    # fermeture morphologique 
    closing_kernel = 5
    closing_iterations = 2
    # quelles formes on conserve 
    min_area_threshold = 10 # 25 50 10


    # flou gaussien 
    blurred = cv2.GaussianBlur(picture, (blur_kernel, blur_kernel), 0)
    
    # Détection des contours
    edges = cv2.Canny(blurred, canny_threshold_1, canny_threshold_2)

    # Fermeture des contours détectés
    kernel_size = (closing_kernel, closing_kernel)
    kernel = np.ones(kernel_size, np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=closing_iterations)
    contours, _ = cv2.findContours(closed_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Verification de la forme des contours : approximation par un polygone et vérification de l'aire
    patatoide_contours = []
    shape_areas = []
    shape_speeds = []
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) >= 5 and cv2.contourArea(contour) > min_area_threshold:
            patatoide_contours.append(contour)
            shape_areas.append(cv2.contourArea(contour))
            u_mean = np.mean(picture[cv2.drawContours(np.zeros_like(picture, dtype=np.uint8), [contour], -1, 255, -1) == 255])
            shape_speeds.append(u_mean)
        else:
            print(f"rejecting contour of len {len(approx)} and area {cv2.contourArea(contour)}")
    img = np.zeros_like(picture)
    if render_detected_shapes:
        color = (1,1,1)
        for contour in patatoide_contours:
            cv2.drawContours(img, [contour], -1, color, 2)
            cv2.fillPoly(img, [contour], color)
    
    return img, shape_areas, shape_speeds


def detect_blobs(picture, render_detected_shapes=False):
    ##### paramètres
    blur_kernel = 13
    min_area_threshold = 25

    # Flou gaussien 
    blurred = cv2.GaussianBlur(picture, (blur_kernel, blur_kernel), 0)

    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = min_area_threshold
    params.maxArea = 10000  # pour la taille max des insects
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(thresh)

    shape_areas = []
    shape_speeds = []
    img = np.zeros_like(picture)

    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        r = int(kp.size / 2)

        # masque circulaire pour identifier une zone dans laquelle on moyenne la vitesse moyenne
        mask = np.zeros_like(picture, dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, -1)

        area = np.pi * (r**2)
        shape_areas.append(area)

        u_mean = np.mean(picture[mask == 255])
        shape_speeds.append(u_mean)

        if render_detected_shapes:
            cv2.circle(img, (x, y), r, 255, -1)

    return img, shape_areas, shape_speeds


def compute_speed(img0, img1, dt):
    flow = cv2.calcOpticalFlowFarneback(
        img0, img1, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2,
        flags=0
    )
    u, v = flow[:,:,0], flow[:,:,1]
    speed = np.sqrt(u**2 + v**2) / dt
    return speed, u, v

def crop_and_resize(img, target_size=(640, 480)):
    target_w, target_h = target_size
    h, w = img.shape[:2]
    input_ratio = w / h
    target_ratio = target_w / target_h

    if input_ratio > target_ratio:
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        img_cropped = img[:, x1:x1+new_w]
    else:
        new_h = int(w / target_ratio)
        y1 = (h - new_h) // 2
        img_cropped = img[y1:y1+new_h, :]

    img_resized = cv2.resize(img_cropped, (target_w, target_h), interpolation=cv2.INTER_AREA)
    return img_resized

