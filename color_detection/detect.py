import cv2
import os
import numpy as np
import pandas as pd

def most_dominant_color(img):
    """
    Finds the most dominant color in an image using K means clustering.
    Idea was inspired by https://rb.gy/ik31uk

    Args:
        img : np array containing raw image data in RGB format

    Returns:
        numpy array [R, G, B] containing the RGB values of
        the most dominant color
    """
    # Convert to float32 array of N x 3, where each row is a pixel (R, G, B)
    pixels = np.float32(img.reshape(-1, 3))

    # Perform K Means clustering
    K = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, K, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    # Extract and return color with highest cluster count
    dominant = palette[np.argmax(counts)]
    return np.array(dominant)

def detect_color(img):
    """
    Finds the most dominant color in an image and matches it to
    a human readable string. (Eg. Red, Green, Blue, Yellow, etc.)

    Args:
        img : np array containing raw image data in RGB format

    Returns:
        [color_name, rgb]: String with the color's name, and a list
            containing the [R, G, B] pixels of the most dominant color
    """
    colors = pd.read_csv("{}/colors.csv".format(
        os.path.dirname(os.path.realpath(__file__))))
    mdc = most_dominant_color(img)

    mdc_name = ""
    min_dist = np.inf
    for _, row in colors.iterrows():
        rgb_array = np.array([row["R"], row["G"], row["B"]])

        dist = np.linalg.norm(mdc - rgb_array)
        if dist < min_dist:
            min_dist = dist
            mdc_name = row["Name"]

    return mdc_name, mdc.tolist()