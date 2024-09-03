# filter.py
import cv2
import numpy as np

def apply_filter(image, kernel):
    # Terapkan filter kernel ke gambar
    return cv2.filter2D(image, -1, kernel)

def edge_detection_1(image):
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    return apply_filter(image, kernel)

def edge_detection_2(image):
    kernel = np.array([[1,  0, -1],
                       [0,  0,  0],
                       [-1, 0,  1]])
    return apply_filter(image, kernel)

def edge_detection_3(image):
    kernel = np.array([[0,  1,  0],
                       [1, -4,  1],
                       [0,  1,  0]])
    return apply_filter(image, kernel)

def gaussian_blur(image, ksize):
    return cv2.GaussianBlur(image, ksize, 0)

def identity_filter(image):
    kernel = np.array([[0,  0,  0],
                       [0,  1,  0],
                       [0,  0,  0]])
    return apply_filter(image, kernel)

def sharpen_filter(image):
    kernel = np.array([[ 0, -1,  0],
                       [-1,  5, -1],
                       [ 0, -1,  0]])
    return apply_filter(image, kernel)

def unsharp_masking_filter(image):
    gaussian_blur_image = cv2.GaussianBlur(image, (9, 9), 10.0)
    return cv2.addWeighted(image, 1.5, gaussian_blur_image, -0.5, 0)

def average_filter(image):
    kernel = np.ones((5, 5), np.float32) / 25
    return apply_filter(image, kernel)

def low_pass_filter(image):
    kernel = np.ones((3, 3), np.float32) / 9
    return apply_filter(image, kernel)

def high_pass_filter(image):
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    return apply_filter(image, kernel)

def bandstop_filter(image):
    kernel = np.array([[1,  1,  1],
                       [1, -7,  1],
                       [1,  1,  1]])
    return apply_filter(image, kernel)
