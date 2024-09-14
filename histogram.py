import numpy as np
import matplotlib.pyplot as plt

def plot_histogram(image_np, title="Image Histogram"):
    plt.figure(figsize=(8, 4))  # Ukuran grafik lebih kecil
    
    # Hitung statistik distribusi intensitas piksel
    pixel_values = image_np.ravel()
    min_pixel = np.min(pixel_values)
    max_pixel = np.max(pixel_values)
    
    # Tentukan apakah gambar mendekati nilai 0 (gelap) atau 255 (terang)
    intensity_range = max_pixel - min_pixel
    
    # Jumlah bin yang lebih sedikit
    num_bins = 128
    
    # Jika gambar grayscale
    if len(image_np.shape) == 2:  
        if intensity_range > 100:  # Banyak variasi intensitas
            plt.hist(pixel_values, bins=num_bins, range=(0, 256), color='purple', edgecolor='black')
        else:  # Intensitas rendah (gelap)
            plt.hist(pixel_values, bins=num_bins, range=(0, 256), color='gray', edgecolor='black')

    # Jika gambar RGB
    elif len(image_np.shape) == 3 and image_np.shape[2] == 3:  
        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            histogram, bin_edges = np.histogram(image_np[..., i], bins=num_bins, range=(0, 256))
            
            # Jika rentang intensitas besar (gambar terang)
            if intensity_range > 100:
                plt.plot(bin_edges[:-1], histogram, color=color, linestyle='-', linewidth=2, label=f'{color.upper()} channel')
            else:
                # Gunakan warna grayscale jika gambar cenderung gelap
                gray_color = 'gray'
                plt.plot(bin_edges[:-1], histogram, color=gray_color, linestyle='--', linewidth=2, label=f'{color.upper()} channel')
    
    else:
        print("Error: Unsupported image dimensions")
        return

    plt.title(title)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
