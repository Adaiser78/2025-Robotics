import cv2
import numpy as np

""""
cv2 is the computer vision module being used for all sorts of vision tasks. 
numpy is the numerical processing module being used for all sorts of mathematical tasks.
"""

CROP_VALUE = 50
LOWER_THRESHOLD = 30
UPPER_THRESHOLD = 100
BALLOON_WIDTH = ''
BALLOON_HEIGHT = ''


def crop_image(img, crop_val):
    """Crops the top portion of an image by the specified number of pixels.
    Requires 2 arguments (image, cropVal)."""
    h, w, c = img.shape
    # Crops the image by selecting only a portion of the rows of the image.
    img = img[crop_val:]
    return img


def pre_process(img):

    # Crops the image.
    cropped_img = crop_image(img, CROP_VALUE)
    # Converts to grayscale.
    img_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    # Applies a blur.
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # Draws lines on edges of objects.
    img_edges = cv2.Canny(img_blur, LOWER_THRESHOLD, UPPER_THRESHOLD)
    # Dilates the lines, makes them enlarged.
    kernel = np.ones((5, 5), np.uint8)
    img_dilated = cv2.dilate(img_edges, kernel)
    return img_dilated


def find_contours(img):
    # Preprocesses the image then detects the contours.
    processed_img = pre_process(img)
    contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # List of np arrays.
    return contours


def draw_bounding_boxes(img, contours):

    img = crop_image(img, CROP_VALUE)
    for contour in contours:  # Loops through the previous obtained arrays.
        x, y, w, h = cv2.boundingRect(contour)  # Finds the smallest possible bounding rectangle coordinates.
        # Draws rectangle around the balloon.
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color in BGR
    return img


def crop_objects(img, contours):
    # This function was modified and currently doesn't support cropping multiple balloons. """""" represent old code.

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # After getting object dimensions, verify in verifyObject()
        is_balloon = verify_object(w, h)
        # If the object is a balloon, return the cropped image
        if is_balloon:
            cropped_img = img[y:y+h, x:x+w]
            return cropped_img, is_balloon

    return 0, False

def verify_object(w, h):
    # FIXME: Why is it 78 and 177, and not 200 and 250?
    tolerance = 0.20

    w_upper_lim = 78 * (1 + tolerance)
    w_lower_lim = 78 * (1 - tolerance)
    h_upper_lim = 127 * (1 + tolerance)
    h_lower_lim = 127 * (1 - tolerance)

    if (w_lower_lim <= w <= w_upper_lim) and (h_lower_lim <= h <= h_upper_lim):
        return True
