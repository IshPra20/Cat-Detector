import streamlit as st
import tensorflow as tf
import numpy as np
import gdown
import os

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Detektor Ras Kucing AI & Tips Perawatan", page_icon="🐱", layout="centered")

st.title("🐱 Detektor Ras Kucing AI Cerdas")
st.write("Unggah foto kucing Anda, biarkan AI mengenali rasnya dari 20 jenis ras, mendeteksi jika bukan kucing, dan melihat 3 peringkat teratas!")

# Fungsi untuk mengunduh model dari Google Drive secara otomatis
@st.cache_resource
def load_model_from_drive():
    # 📌 Ganti dengan ID Google Drive file model .keras Anda
    file_id = "MASUKKAN_ID_GOOGLE_DRIVE_ANDA_DI_SINI"  
    output = "model_kucing_pintar.keras"
    
    if not os.path.exists(output):
        with st.spinner("Sedang mengunduh otak AI dari Google Drive... Mohon tunggu sebentar."):
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, output, quiet=False)
                
    return tf.keras.models.load_model(output)

# Memuat model AI
try:
    model = load_model_from_drive()
except Exception as e:
    st.error(f"Gagal memuat model. Pastikan ID Google Drive benar dan aksesnya publik. Error: {e}")

# 📌 DAFTAR 20 RAS KUCING (Urut abjad sesuai dataset Anda)[cite: 1]
daftar_ras = [
    'Abyssinian', 'American Bobtail', 'American Curl', 'American Shorthair',
    'Bengal', 'Birman', 'Bombay', 'British Shorthair', 'Egyptian Mau',
    'Exotic Shorthair', 'Maine Coon', 'Manx', 'Norwegian Forest',
    'Persian', 'Ragdoll', 'Russian Blue', 'Scottish Fold', 'Siamese',
    'Sphynx', 'Turkish Angora'
]

# Kamus Tips Perawatan (Contoh untuk beberapa ras, bisa Anda lengkapi sendiri)
tips_perawatan = {
    'Persian': {
        "karakter": "Tenang, manja, menyukai lingkungan damai, dan memiliki bulu yang sangat lebat.",
        "perawatan": [
            "Wajib disisir setiap hari agar bulu panjangnya tidak menggumpal.",
            "Bersihkan area sekitar mata dan hidungnya secara rutin."
        ]
    },
    'Bengal': {
        "karakter": "Sangat aktif, berenergi tinggi, cerdas, dan memiliki corak bulu mirip macan.",
        "perawatan": [
            "Sediakan ruang gerak luas dan mainan menantang agar tidak bosan.",
            "Berikan stimulasi mental secara rutin."
        ]
    },
    'Siamese': {
        "karakter": "Sangat vokal, aktif, cerdas, dan penuh perhatian kepada pemiliknya.",
        "perawatan": [
            "Berikan banyak interaksi dan ajak bermain agar tidak stres.",
            "Sikat bulu pendeknya secara berkala."
        ]
    }
}

# Antarmuka Unggah Foto di Web
st.markdown("---")
file_gambar = st.file_uploader("Pilih foto (Kucing / objek lain) (.jpg / .jpeg / .png)", type=["jpg", "jpeg", "png"])

if file_gambar is not None:
    st.image(file_gambar, caption="Foto yang Anda Unggah", use_container_width=True)
    
    # Proses gambar (pastikan target_size sama dengan saat training, misal 150x150)
    img = tf.keras.utils.load_img(file_gambar, target_size=(150, 150))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    with st.spinner("AI sedang menganalisis gambar..."):
        prediksi = model.predict(img_array)
        score = tf.nn.softmax(prediksi[0])
        
        # Ambil nilai keyakinan tertinggi
        max_score = np.max(score)
        keyakinan_utama = 100 * max_score
        
        # Cari 3 peringkat ras tertinggi menggunakan argsort
        # argsort mengurutkan dari kecil ke besar, jadi kita ambil 3 dari belakang [::-1][:3]
        top_3_indices = np.argsort(score)[::-1][:3]

    st.markdown("### 📊 Hasil Analisis AI:")
    
    # 🚨 FITUR ERROR / FILTER: Jika keyakinan di bawah 45%, anggap bukan kucing atau foto tidak valid
    if keyakinan_utama < 45.0:
        st.error("❌ **Peringatan: Gambar Tidak Dikenali sebagai Kucing!**")
        st.warning(
            f"Tingkat keyakinan AI terlalu rendah (**{keyakinan_utama:.2f}%**). "
            "Kemungkinan besar foto ini **bukan kucing**, terlalu gelap, atau buram. "
            "Coba unggah foto kucing yang lebih jelas dan terang!"
        )
    else:
        # Jika lolos validasi, tampilkan pemenang utama
        juara_utama_key = daftar_ras[top_3_indices[0]]
        st.success(f"**Ras Kucing Utama:** {juara_utama_key.upper()} (Keyakinan: {keyakinan_utama:.2f}%)")
        
        # 🏆 Tampilkan Peringkat 3 Tertinggi
        st.markdown("#### 🥇🥈🥉 3 Peringkat Ras Teratas:")
        for i, idx in enumerate(top_3_indices):
            nama_ras = daftar_ras[idx]
            persen = 100 * score[idx]
            medali = ["🥇", "🥈", "🥉"][i]
            st.write(f"{medali} **{nama_ras}** — `{persen:.2f}%`")
        
        # 💡 Tampilkan Tips Perawatan Berdasarkan Ras Pemenang Utama
        if juara_utama_key in tips_perawatan:
            info = tips_perawatan[juara_utama_key]
            st.markdown("---")
            st.markdown(f"### 💡 Panduan & Tips Perawatan Kucing {juara_utama_key.upper()}:")
            st.write(f"**Karakter Umum:** {info['karakter']}")
            st.write("**Tips Perawatan:**")
            for tip in info['perawatan']:
                st.markdown(f"- {tip}")
        else:
            st.info(f"Tips perawatan untuk ras {juara_utama_key.upper()} akan segera ditambahkan!")