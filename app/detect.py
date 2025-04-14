import os
import requests
import numpy as np
from PIL import Image
from collections import defaultdict

# Your Roboflow API key and model ID
ROBOFLOW_API_KEY = "TEHGbI0CKnrNwwzAMJPl"
ROBOFLOW_MODEL_ID = "apple-detection_0630/6"
ROBOFLOW_API_URL = f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}?api_key={ROBOFLOW_API_KEY}"

def classify_color(image):
    """
    Classify the color of an apple in an image based on average RGB values.
    """
    img = np.array(image)
    avg_color = img.mean(axis=0).mean(axis=0)
    r, g, b = avg_color[:3]

    # Define color classification rules
    if r > 150 and g < 100:  # Red apples are predominantly red with less green
        return "red"
    elif g > r and g > b:  # Green apples are mostly green
        return "green"
    else:
        return "yellow"  # Other apples are considered yellow

def detect_and_crop(file_path: str, crop_folder: str):
    """
    Detect apples in an image, classify them by color, crop them, and save them.
    """
    with open(file_path, "rb") as f:
        image_bytes = f.read()

    # Send the image to the Roboflow API for detection
    response = requests.post(
        ROBOFLOW_API_URL,
        files={"file": image_bytes},
        data={"name": os.path.basename(file_path)}
    )

    if response.status_code != 200:
        raise Exception(f"Failed Roboflow API request: {response.status_code} - {response.text}")

    # Parse the results from the API response
    result = response.json()
    predictions = result.get("predictions", [])

    # Open the image for cropping
    image = Image.open(file_path).convert("RGB")
    image_width, image_height = image.size

    # Prepare the directories for cropped images
    result_paths = {"red": [], "yellow": [], "green": []}
    result_names = {"red": [], "yellow": [], "green": []}
    color_counter = defaultdict(int)

    # Create the directories for each color if they don't exist
    for color in result_paths:
        os.makedirs(os.path.join(crop_folder, color), exist_ok=True)

    # Process each prediction from the Roboflow API
    for pred in predictions:
        x, y, w, h = pred["x"], pred["y"], pred["width"], pred["height"]

        # Calculate the coordinates for cropping the apple
        left = int(max(x - w / 2, 0))
        top = int(max(y - h / 2, 0))
        right = int(min(x + w / 2, image_width))
        bottom = int(min(y + h / 2, image_height))

        # Crop the image to the bounding box of the detected apple
        cropped = image.crop((left, top, right, bottom))

        # Classify the color of the cropped apple
        color = classify_color(cropped)
        color_counter[color] += 1

        # Save the cropped image in the appropriate color directory
        cropped_name = f"{color}_{color_counter[color]}.jpg"
        color_dir = os.path.join(crop_folder, color)
        cropped_path = os.path.join(color_dir, cropped_name)
        cropped.save(cropped_path)

        # Add the cropped image path and name to the result
        result_paths[color].append(f"/static/crops/{color}/{cropped_name}")
        result_names[color].append(cropped_name)

    # Return the paths for the uploaded image and the cropped images
    uploaded_image_url = f"/static/uploads/{os.path.basename(file_path)}"
    return {
        "file": uploaded_image_url,
        "results": result_paths,
        "names": result_names
    }
