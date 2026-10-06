import streamlit as st
import tensorflow as tf
import numpy as np
import gdown
import os

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Detektor Ras Kucing AI", page_icon="🐱", layout="centered")

st.title("🐱 Detektor Ras Kucing AI")
st.write("Unggah foto kucing Anda, dan biarkan AI menebak rasnya secara otomatis!")

# Fungsi untuk mengunduh model dari Google Drive secara otomatis
@st.cache_resource
def load_model_from_drive():
    # 📌 PENTING: Ganti teks di dalam tanda kutip di bawah ini dengan ID Google Drive file Anda
    file_id = "1tjFvJcYgt15x4aPmn8PvnFdUeTnRRrsE"  
    output = "model_kucing_pintar.keras"
    
    # Cek apakah file model sudah ada di server awan
    if not os.path.exists(output):
        with st.spinner("Sedang mengunduh otak AI dari Google Drive... Mohon tunggu sebentar."):
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, output, quiet=False)
                
    return tf.keras.models.load_model(output)

# Memuat model AI
try:
    model = load_model_from_drive()
except Exception as e:
    st.error(f"Gagal memuat model. Pastikan Anda sudah memasukkan ID Google Drive yang benar dan aksesnya sudah diatur publik. Error: {e}")

# 📌 DAFTAR RAS KUCING (Harus sesuai abjad dari nama folder training Anda)
daftar_ras = ['anggora', 'bengal', 'persia', 'sphynx'] 

# Bagian Antarmuka Unggah Foto
st.markdown("---")
file_gambar = st.file_uploader("Pilih foto kucing (.jpg / .jpeg / .png)", type=["jpg", "jpeg", "png"])

if file_gambar is not None:
    # Tampilkan foto yang di-upload pengguna di layar web
    st.image(file_gambar, caption="Foto Kucing Pilihan Anda", use_container_width=True)
    
    # Proses gambar agar sesuai dengan ukuran saat training (150x150)
    img = tf.keras.utils.load_img(file_gambar, target_size=(150, 150))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    # Proses Prediksi oleh AI
    with st.spinner("AI sedang menganalisis foto kucing..."):
        prediksi = model.predict(img_array)
        score = tf.nn.softmax(prediksi[0])
        
        tebakan = daftar_ras[np.argmax(score)]
        keyakinan = 100 * np.max(score)
        
    # Tampilkan Hasil Akhir di Web
    st.markdown("### 📊 Hasil Prediksi:")
    st.success(f"**Ras Kucing:** {tebakan.upper()}")
    st.info(f"**Tingkat Keyakinan AI:** {keyakinan:.2f}%")