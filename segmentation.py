import cv2
import matplotlib.pyplot as plt
import numpy as np

# Region Growing
def region_growing(img, seed_point, threshold):
    h, w = img.shape
    segmented = np.zeros((h, w), dtype=np.uint8)
    segmented[seed_point] = 255
    region_intensity = img[seed_point]

    to_check = [seed_point]

    while to_check:
        current_point = to_check.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x, y = current_point[0] + dx, current_point[1] + dy
                if 0 <= x < h and 0 <= y < w and segmented[x, y] == 0:
                    if abs(int(img[x, y]) - int(region_intensity)) <= threshold:
                        segmented[x, y] = 255
                        to_check.append((x, y))

    return segmented

# K-Means Clustering (k = 2)
def kmeans_clustering(image, k):
    pixel_values = image.reshape((-1, 1))
    pixel_values = np.float32(pixel_values)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(centers)
    segmented_image = center[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)

    return segmented_image

# Watershed Segmentation
def watershed_segmentation(image):
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img_bgr, markers)
    img_bgr[markers == -1] = [255, 0, 0]  # Ganti warna tepi menjadi merah

    return img_bgr

# Global Thresholding (T = 100)
def global_thresholding(image, threshold_value):
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_image

# Adaptive Thresholding
def adaptive_thresholding(image):
    adaptive_thresh_mean = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    adaptive_thresh_gaussian = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return adaptive_thresh_mean, adaptive_thresh_gaussian

# Fungsi untuk menampilkan gambar
def display_images(original, processed, title):
    plt.figure(figsize=(15, 10))

    # Tampilkan gambar asli
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title("Original Image")

    # Tampilkan hasil pemrosesan
    plt.subplot(1, 2, 2)
    plt.imshow(processed, cmap='gray')
    plt.title(title)

    plt.tight_layout()
    plt.show()
