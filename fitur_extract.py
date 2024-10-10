import pandas as pd
from PIL import Image
import os

def ekstraksi_warna(image_path):
    # Buka gambar menggunakan jalur yang diberikan
    image = Image.open(image_path)
    
    # Simulasi proses ekstraksi warna dari gambar
    pixels = list(image.getdata())
    avg_r = sum([p[0] for p in pixels]) / len(pixels)
    avg_g = sum([p[1] for p in pixels]) / len(pixels)
    avg_b = sum([p[2] for p in pixels]) / len(pixels)
    
    # Ekstrak nama file dari jalur gambar
    nama_gambar = os.path.basename(image_path)
    
    # Buat DataFrame dengan hasil ekstraksi
    data_warna = {
        'No.': [None],  # Akan diisi setelah membaca data yang ada
        'Nama': [nama_gambar],
        'R': [avg_r],
        'G': [avg_g],
        'B': [avg_b]
    }
    
    df_warna = pd.DataFrame(data_warna)
    
    # Menentukan jalur output
    output_path = r'D:/ekstraksi_fitur/ekstraksi_warna.xlsx'
    
    # Cek jika file Excel sudah ada
    if os.path.exists(output_path):
        # Membaca file yang sudah ada
        df_existing = pd.read_excel(output_path)
        # Menentukan nomor urut berikutnya
        next_index = len(df_existing) + 1
        df_warna['No.'] = next_index  # Menetapkan nomor urut
        # Menggabungkan data baru dengan data yang sudah ada
        df_final = pd.concat([df_existing, df_warna], ignore_index=True)
    else:
        # Jika file tidak ada, mulai dengan data baru
        df_warna['No.'] = 1  # Menetapkan nomor urut pertama
        df_final = df_warna
    
    # Menyimpan hasil ke file .xlsx
    df_final.to_excel(output_path, index=False)
    
    print(f"Ekstraksi warna selesai untuk {image_path}. Hasil disimpan di '{output_path}'.")

def ekstraksi_tekstur(image_path):
    # Buka gambar menggunakan jalur yang diberikan
    image = Image.open(image_path)
    
    # Simulasi proses ekstraksi tekstur dari gambar
    width, height = image.size
    kekasaran = (width + height) / 2
    kontras = (width - height) ** 2
    homogenitas = 1 / (1 + kekasaran)
    energi = kekasaran * kontras * homogenitas  # Contoh perhitungan energi
    korelasi = (kontras + homogenitas) / 2  # Contoh perhitungan korelasi

    # Ekstrak nama file dari jalur gambar
    nama_gambar = os.path.basename(image_path)
    
    # Buat DataFrame dengan hasil ekstraksi
    data_tekstur = {
        'Nama': [nama_gambar],
        'Kontras': [kontras],
        'Homogenitas': [homogenitas],
        'Energi': [energi],
        'Korelasi': [korelasi]
    }
    
    df_tekstur = pd.DataFrame(data_tekstur)
    
    # Menentukan jalur output
    output_path = r'D:/ekstraksi_fitur/ekstraksi_tekstur.xlsx'
    
    # Cek jika file Excel sudah ada
    if os.path.exists(output_path):
        # Membaca file yang sudah ada
        df_existing = pd.read_excel(output_path)
        # Menentukan nomor urut berikutnya
        next_index = len(df_existing) + 1
        df_tekstur.insert(0, 'No.', next_index)  # Menetapkan nomor urut
        # Menggabungkan data baru dengan data yang sudah ada
        df_final = pd.concat([df_existing, df_tekstur], ignore_index=True)
    else:
        # Jika file tidak ada, mulai dengan data baru
        df_tekstur.insert(0, 'No.', 1)  # Menetapkan nomor urut pertama
        df_final = df_tekstur
    
    # Menyimpan hasil ke file .xlsx
    df_final.to_excel(output_path, index=False)
    
    print(f"Ekstraksi tekstur selesai untuk {image_path}. Hasil disimpan di '{output_path}'.")
