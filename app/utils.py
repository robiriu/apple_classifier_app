import cv2
import numpy as np
import os

def classify_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    avg_hue = hsv[:, :, 0].mean()

    # Rough classification based on hue range
    if avg_hue < 20 or avg_hue > 160:
        return "red"
    elif 20 <= avg_hue < 40:
        return "yellow"
    else:
        return "green"

def save_cropped_image(image, filename):
    path = os.path.join("app/static/crops", filename)
    cv2.imwrite(path, image)
