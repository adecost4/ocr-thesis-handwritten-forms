import cv2
import numpy as np
from PIL import Image


def pil_to_cv(image: Image.Image) -> np.ndarray:
    """
    Convert a PIL image to an OpenCV-compatible RGB array.
    """
    return np.array(image.convert("RGB"))


def cv_to_pil(image: np.ndarray) -> Image.Image:
    """
    Convert an OpenCV/NumPy image back to PIL.
    """
    if len(image.shape) == 2:
        return Image.fromarray(image)

    return Image.fromarray(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    )


def grayscale(image: Image.Image) -> Image.Image:
    """
    Convert an image to grayscale.
    """
    img = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    return Image.fromarray(gray)


def threshold_otsu(image: Image.Image) -> Image.Image:
    """
    Convert image to grayscale and apply Otsu thresholding.
    """
    img = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return Image.fromarray(binary)


def enhance_contrast(image: Image.Image) -> Image.Image:
    """
    Improve local contrast using CLAHE.
    """
    img = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    return Image.fromarray(enhanced)


def denoise(image: Image.Image) -> Image.Image:
    """
    Reduce grayscale image noise using Non-Local Means.
    """
    img = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    cleaned = cv2.fastNlMeansDenoising(
        gray,
        None,
        h=10,
        templateWindowSize=7,
        searchWindowSize=21
    )

    return Image.fromarray(cleaned)