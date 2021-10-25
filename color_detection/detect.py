import pandas as pd
import numpy as np
import cv2

# https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
def most_dominant_color(img):
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
    colors = pd.read_csv("color_detection/colors.csv")
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

if __name__ == "__main__":
    detect_color()