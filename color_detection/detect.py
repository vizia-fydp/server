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
    Uses k-means clustering to find images.

    Args:
        img : np array containing raw image data in RGB format
        k : how many colors to return

    Returns:
        [color_names, rgb_array]: Array of strings with the color's names, and
            a list containing the [R, G, B] pixels of those colors. Sorted
            from most dominant to least dominant.
    """
    # Load color database into numpy arrays
    colors = pd.read_csv("{}/colors_medium.csv".format(
        os.path.dirname(os.path.realpath(__file__))))
    color_array = colors[['R','G','B']].to_numpy()
    color_names = colors.Name.to_numpy()

    # Get top k colors from image. Each color is in [R, G, B] format
    top_k = top_k_colors(img, k)

    # Match each [R, G, B] to a color name, eg. "Red"
    top_k_names = []
    top_k_list = []
    for color in top_k:
        top_k_list.append(color.tolist())
        dist = np.linalg.norm(color - color_array, axis=1)
        color_idx = np.argmin(dist)
        top_k_names.append(color_names[color_idx])

    return top_k_names, top_k_list


def detect_color_2(img, k):
    """
    Finds the most dominant k colors in an image and matches it to
    a human readable string. (Eg. Red, Green, Blue, Yellow, etc.)
    Uses euclidean distance from each pixel to a color dataset to find
    top colors.

    Args:
        img : np array containing raw image data in RGB format
        k : how many colors to return

    Returns:
        color_names : Array of strings with the color's names
    """
    # Load color database into numpy arrays
    colors = pd.read_csv("{}/colors_medium.csv".format(
        os.path.dirname(os.path.realpath(__file__))))
    color_array = colors[['R','G','B']].to_numpy()
    color_names = colors.Name.to_numpy()

    # Flatten image into (N, 3) array
    pixels = img.reshape((-1, 3))

    # Copy pixels into shape (N, num_colors, 3)
    pixels_copy = np.repeat(pixels[:, np.newaxis, :], color_array.shape[0], axis=1)

    # Get euclidean distance between each pixel and each color
    dist = np.linalg.norm(pixels_copy - color_array, axis=2)

    # Get index of color with smallest distance for each pixel
    color_idx = np.argmin(dist, axis=1)

    # Get pixel counts for each color
    unique, counts = np.unique(color_idx, return_counts=True)

    # Get k colors with highest counts
    max_idx = np.argpartition(counts, -k)[-k:]

    # Result is not sorted, sort to get order of 1st, 2nd, 3rd
    max_idx = np.sort(max_idx)
    top_colors = color_names[unique[max_idx]]

    return top_colors
