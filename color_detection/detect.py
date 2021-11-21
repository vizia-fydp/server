import cv2
import os
import numpy as np
import pandas as pd

def top_k_colors(img, k):
    """
    Finds the most dominant k colors in an image using k means clustering.
    Idea was inspired by https://rb.gy/ik31uk

    Args:
        img : np array containing raw image data in RGB format
        k : how many colors to return

    Returns:
        List containing numpy arrays [R, G, B] of the most dominant colors in
        sorted order from most dominant to least dominant
    """
    # Convert to float32 array of N x 3, where each row is a pixel (R, G, B)
    pixels = np.float32(img.reshape(-1, 3))

    # Perform K Means clustering with 2*k means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, 2*k, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    # Sort color counts
    count_to_color = {}
    for i in range(len(counts)):
        count_to_color[counts[i]] = palette[i]

    colors_sorted = []
    for key in sorted(count_to_color, reverse=True):
        colors_sorted.append(np.array(count_to_color[key]))

    # Return top 3 colors only
    return colors_sorted[0:k]

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

def detect_color(img, k):
    """
    Finds the most dominant k colors in an image and matches it to
    a human readable string. (Eg. Red, Green, Blue, Yellow, etc.)

    Args:
        img : np array containing raw image data in RGB format
        k : how many colors to return

    Returns:
        [color_names, rgb_array]: Array of strings with the color's names, and
            a list containing the [R, G, B] pixels of those colors. Sorted
            from most dominant to least dominant.
    """
    colors = pd.read_csv("{}/colors_medium.csv".format(
        os.path.dirname(os.path.realpath(__file__))))
    top_k = top_k_colors(img, k)

    color_names = []
    top_k_list = []
    for color in top_k:
        top_k_list.append(color.tolist())

        # Convert to HSV
        # color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]

        min_dist = np.inf
        color_name = ""
        for _, row in colors.iterrows():
            # hsv_array = np.array([row["H"], row["S"], row["V"]])
            rgb_array = np.array([row["R"], row["G"], row["B"]])

            dist = np.linalg.norm(color - rgb_array)
            if dist < min_dist:
                min_dist = dist
                color_name = row["Name"]
        color_names.append(color_name)

    return color_names, top_k_list