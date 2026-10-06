import streamlit as st
import tensorflow as tf
import numpy as np
import gdown
import os

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Detektor Ras Kucing AI & Tips Perawatan", page_icon="🐱", layout="centered")

st.title("🐱 Detektor Ras Kucing AI & Tips Perawatan")
st.write("Unggah foto kucing Anda, biarkan AI mengenali rasnya dari 20 jenis ras yang ada, dan dapatkan tips perawatannya secara instan!")

# Fungsi untuk mengunduh model dari Google Drive secara otomatis
@st.cache_resource
def load_model_from_drive():
    # 📌 Ganti dengan ID Google Drive file model .keras Anda yang sebenarnya
    file_id = "1tjFvJcYgt15x4aPmn8PvnFdUeTnRRrsE"  
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
    'Abyssinian', 
    'American Bobtail', 
    'American Curl', 
    'American Shorthair',
    'Bengal',
    'Birman',
    'Bombay',
    'British Shorthair',
    'Egyptian Mau',
    'Exotic Shorthair',
    'Maine Coon',
    'Manx',
    'Norwegian Forest',
    'Persian',
    'Ragdoll',
    'Russian Blue',
    'Scottish Fold',
    'Siamese',
    'Sphynx',
    'Turkish Angora'
]

# 💡 KAMUS TIPS PERAWATAN LENGKAP UNTUK 20 RAS KUCING
tips_perawatan = {
    'Abyssinian': {
        "karakter": "Sangat aktif, cerdas, lincah, dan sangat suka memanjat.",
        "perawatan": [
            "Sediakan pohon kucing (*cat tree*) atau ruang panjat yang tinggi.",
            "Berikan mainan interaktif untuk melatih kecerdasan dan energi mereka.",
            "Bulu pendeknya cukup disikat seminggu sekali untuk mengangkat bulu mati."
        ]
    },
    'American Bobtail': {
        "karakter": "Ramah, mudah beradaptasi, cerdas, dan mirip seperti anjing kecil.",
        "perawatan": [
            "Ajak bermain secara rutin karena mereka senang berinteraksi dengan pemilik.",
            "Sisir bulunya secara berkala untuk menjaga kebersihannya."
        ]
    },
    'American Curl': {
        "karakter": "Penuh kasih sayang, sangat bersahabat, dan tetap playful hingga dewasa.",
        "perawatan": [
            "Bersihkan telinganya dengan hati-hati secara rutin karena bentuk telinganya yang melengkung.",
            "Berikan perhatian dan kasih sayang yang cukup karena mereka sangat manja."
        ]
    },
    'American Shorthair': {
        "karakter": "Tenang, mudah bergaul, penurut, dan bertubuh atletis.",
        "perawatan": [
            "Awasi porsi makannya agar tidak mengalami kelebihan berat badan (*obesitas*).",
            "Sikat bulunya seminggu sekali untuk menjaga kilau bulunya."
        ]
    },
    'Bengal': {
        "karakter": "Sangat aktif, berenergi tinggi, cerdas, dan memiliki corak bulu mirip macan.",
        "perawatan": [
            "Wajib sediakan banyak ruang gerak dan mainan menantang agar tidak stres.",
            "Berikan stimulasi mental karena mereka sangat cepat bosan.",
            "Bulu pendeknya sangat mudah dirawat, cukup disikat sesekali."
        ]
    },
    'Birman': {
        "karakter": "Tenang, lembut, penuh kasih sayang, dan memiliki mata biru yang indah.",
        "perawatan": [
            "Sisir bulunya secara rutin agar terhindar dari kusut meskipun tidak sepanjang Persia.",
            "Nikmati momen santai bersama karena mereka suka berada di dekat manusia."
        ]
    },
    'Bombay': {
        "karakter": "Seperti mini panter hitam yang ramah, hangat, dan sangat suka mencari perhatian.",
        "perawatan": [
            "Berikan banyak interaksi sosial agar mereka tidak merasa kesepian.",
            "Sikat bulu hitam mengkilapnya secara rutin agar tetap tampak sehat."
        ]
    },
    'British Shorthair': {
        "karakter": "Mandiri, tenang, berwajah bulat (*chubby*), dan sangat bersahabat.",
        "perawatan": [
            "Kontrol jumlah makanannya karena ras ini cenderung malas bergerak setelah dewasa.",
            "Sisir bulunya seminggu sekali untuk merontokkan bulu mati."
        ]
    },
    'Egyptian Mau': {
        "karakter": "Kucing tercepat di ras domestik, cerdas, setia, dan aktif.",
        "perawatan": [
            "Sediakan ruang lari yang cukup dan mainan kejar-kejaran.",
            "Perhatikan pola makannya agar tubuh atletisnya tetap terjaga."
        ]
    },
    'Exotic Shorthair': {
        "karakter": "Tenang, manis, setia, mirip kucing Persia namun berbulu pendek.",
        "perawatan": [
            "Bersihkan lipatan wajah dan area mata secara rutin karena rentan berair.",
            "Nikmati sifat santainya yang suka tidur di pangkuan Anda."
        ]
    },
    'Maine Coon': {
        "karakter": "Raksasa yang lembut (*gentle giant*), sangat ramah, dan suka dengan air.",
        "perawatan": [
            "Sisir bulu tebalnya beberapa kali seminggu agar tidak mudah gimbal.",
            "Sediakan wadah air minum yang luas karena mereka suka bermain air."
        ]
    },
    'Manx': {
        "karakter": "Cerdas, setia, dan terkenal karena tidak memiliki ekor (berekor pendek/boncel).",
        "perawatan": [
            "Perhatikan kesehatan tulang belakang dan area pinggulnya secara berkala ke dokter hewan.",
            "Ajak bermain tangkas untuk melatih keseimbangan tubuhnya."
        ]
    },
    'Norwegian Forest': {
        "karakter": "Tangguh, suka memanjat pohon, mandiri, namun sangat sayang pada keluarga.",
        "perawatan": [
            "Bulu tebalnya tahan air, namun tetap perlu disisir rutin terutama saat musim ganti bulu.",
            "Sediakan media panjat yang kokoh di dalam rumah."
        ]
    },
    'Persian': {
        "karakter": "Tenang, manja, menyukai lingkungan damai, dan memiliki bulu yang sangat lebat.",
        "perawatan": [
            "**Wajib disisir setiap hari** agar bulu panjangnya tidak menggumpal/gimbal.",
            "Bersihkan area sekitar mata dan hidungnya setiap hari karena rentan bernoda.",
            "Jaga kebersihan kandang atau ruangan tempat tinggalnya."
        ]
    },
    'Ragdoll': {
        "karakter": "Sangat tenang, penurut, dan lemas seperti 'boneka kain' ketika digendong.",
        "perawatan": [
            "Sisir bulunya secara rutin untuk menghindari kusut.",
            "Berikan lingkungan indoor yang aman karena mereka kurang memiliki insting membela diri."
        ]
    },
    'Russian Blue': {
        "karakter": "Tenang, sedikit pemalu kepada orang asing, cerdas, dan anggun berbulu abu-abu.",
        "perawatan": [
            "Jaga lingkungan rumah agar tetap tenang dan damai.",
            "Sikat bulu halusnya secara teratur untuk menjaga kelembutannya."
        ]
    },
    'Scottish Fold': {
        "karakter": "Unik dengan telinga melipat ke depan, manis, tenang, dan mudah beradaptasi.",
        "perawatan": [
            "Rutin bersihkan lipatan telinganya secara lembut untuk mencegah infeksi.",
            "Perhatikan persendian tulangnya karena bentuk telinganya berkaitan dengan gen tulang rawan."
        ]
    },
    'Siamese': {
        "karakter": "Sangat vokal (suka 'berbicara' mengeong), aktif, cerdas, dan penuh perhatian.",
        "perawatan": [
            "Berikan banyak perhatian dan ajak komunikasi karena mereka tidak suka diabaikan.",
            "Sediakan mainan yang merangsang keaktifan otak mereka."
        ]
    },
    'Sphynx': {
        "karakter": "Unik tanpa bulu, sangat ramah, aktif, dan senang mencari kehangatan.",
        "perawatan": [
            "**Wajib dimandikan secara rutin** (1–2 minggu sekali) untuk membersihkan minyak alami kulitnya.",
            "Lindungi kulitnya dari paparan matahari langsung atau suhu ruangan yang terlalu dingin.",
            "Bersihkan kotoran telinganya secara berkala."
        ]
    },
    'Turkish Angora': {
        "karakter": "Anggun, sangat aktif, cerdas, lincah, dan memiliki bulu semi-panjang yang lembut.",
        "perawatan": [
            "Sisir bulunya secara rutin seminggu sekali agar tidak mudah kusut.",
            "Ajak bermain air atau sediakan mainan interaktif karena mereka sangat energik."
        ]
    }
}

# Bagian Antarmuka Unggah Foto di Web
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
        
        tebakan_key = daftar_ras[np.argmax(score)]
        tebakan_nama = tebakan_key.upper()
        keyakinan = 100 * np.max(score)
        
    # Tampilkan Hasil Akhir di Web
    st.markdown("### 📊 Hasil Prediksi AI:")
    st.success(f"**Ras Kucing:** {tebakan_nama}")
    st.info(f"**Tingkat Keyakinan AI:** {keyakinan:.2f}%")
    
    # 💡 Tampilkan Prompt / Kotak Tips Perawatan Sesuai Ras yang Terdeteksi
    if tebakan_key in tips_perawatan:
        info = tips_perawatan[tebakan_key]
        st.markdown("---")
        st.markdown(f"### 💡 Panduan & Tips Perawatan Kucing {tebakan_nama}:")
        st.write(f"**Karakter Umum:** {info['karakter']}")
        st.write("**Tips Perawatan:**")
        for tip in info['perawatan']:
            st.markdown(f"- {tip}")