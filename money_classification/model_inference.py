import numpy as np
import cv2


CLASS_MAP = ["no_bill", "1", "5", "10", "20", "50", "100"]
IMG_SIZE = (384, 384)
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def preprocess_img(img):
    """
    Prepares numpy image for model inference. Needs to transform the tensor to
    the required dimensions (1, 3, H, W), normalize, and convert to float32.
    """
    # Downsize to required model size
    img = cv2.resize(img, IMG_SIZE, interpolation=cv2.INTER_AREA)

    # Need to normalize using given MEAN and STD and move channel dim to match torch convention
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = (img - MEAN[:, np.newaxis, np.newaxis]) / STD[:, np.newaxis, np.newaxis]

    # Add batch dim
    img = img[np.newaxis, :]

    return img

def run_inference(session, img):
    """
    Runs inference using given onnx session then converts result to class name using class map.
    """
    # Prep image and then run inference using onnx session
    img = preprocess_img(img)
    output = session.run(None, {'input': img})[0]

    # Get actual class prediction using clas map
    pred = output.argmax(1)[0]
    class_pred = CLASS_MAP[pred]

    return class_pred
