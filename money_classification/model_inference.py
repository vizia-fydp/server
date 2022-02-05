from pathlib import Path

import torch
import torchvision
from torchvision import transforms as tf
from PIL import Image

CLASS_MAP = [1, 5, 10, 20, 50, 100]

transforms = tf.Compose([
    tf.Resize((384, 384)),
    tf.ToTensor(),
    tf.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def load_model(filename, device):
    # Assumes the model is located in money_classification folder
    model_path = Path(__file__).resolve().parent / filename

    # Init model class
    num_classes = len(CLASS_MAP)
    model = torchvision.models.resnet50()
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    # Load in the trained weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    return model

def run_inference(model, image, device):
    # Convert image to tensor and normalize
    img = transforms(Image.fromarray(image))

    # Add batch dim
    img  = torch.unsqueeze(img, dim=0)

    # Run image through model
    img = img.to(device)
    with torch.no_grad():
        output = model(img)

    # Get actual class prediction
    pred = torch.argmax(output, dim=1)[0].detach().cpu().numpy()
    class_pred = CLASS_MAP[pred]

    return class_pred
