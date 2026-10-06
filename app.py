import streamlit as st
import tensorflow as tf
import numpy as np
import gdown
import os

st.set_page_config(page_title="AI Detektor Ras Kucing & Tips Perawatan", page_icon="🐱", layout="centered")

st.title("🐱 AI Detektor Ras Kucing")
st.write("Unggah foto kucing Anda, biarkan AI mengenali rasnya dari 20 jenis ras, mendeteksi jika bukan kucing, dan melihat 3 peringkat teratas beserta tips perawatannya!")

@st.cache_resource
def load_model_from_drive():
    file_id = "1TtMg3HZyh-1r82h5Eb0_VSZJxxZnM_8-"  
    output = "model_kucing_pintar.keras"
    
    if not os.path.exists(output):
        with st.spinner("Sedang mengunduh otak AI MobileNetV3 dari Google Drive... Mohon tunggu sebentar."):
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, output, quiet=False)
                
    return tf.keras.models.load_model(output)

try:
    model = load_model_from_drive()
except Exception as e:
    st.error(f"Gagal memuat model. Pastikan ID Google Drive benar dan aksesnya publik. Error: {e}")

daftar_ras = [
    'Abyssinian', 'American Bobtail', 'American Curl', 'American Shorthair',
    'Bengal', 'Birman', 'Bombay', 'British Shorthair', 'Egyptian Mau',
    'Exotic Shorthair', 'Maine Coon', 'Manx', 'Norwegian Forest',
    'Persian', 'Ragdoll', 'Russian Blue', 'Scottish Fold', 'Siamese',
    'Sphynx', 'Turkish Angora'
]

tips_perawatan = {
    'Abyssinian': {
        "karakter": "Sangat aktif, cerdas, lincah, dan sangat suka memanjat.",
        "perawatan": [
            "Sediakan pohon kucing (cat tree) atau ruang panjat yang tinggi.",
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
            "Awasi porsi makannya agar tidak mengalami kelebihan berat badan (obesitas).",
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
            "Sisir bulunya secara rutin agar terhindar dari kusut.",
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
        "karakter": "Mandiri, tenang, berwajah bulat (chubby), dan sangat bersahabat.",
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
        "karakter": "Raksasa yang lembut (gentle giant), sangat ramah, dan suka dengan air.",
        "perawatan": [
            "Sisir bulu tebalnya beberapa kali seminggu agar tidak mudah gimbal.",
            "Sediakan wadah air minum yang luas karena mereka suka bermain air."
        ]
    },
    'Manx': {
        "karakter": "Cerdas, setia, dan terkenal karena tidak memiliki ekor.",
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
            "Wajib disisir setiap hari agar bulu panjangnya tidak menggumpal/gimbal.",
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
        "karakter": "Sangat vokal, aktif, cerdas, dan penuh perhatian kepada pemiliknya.",
        "perawatan": [
            "Berikan banyak interaksi dan ajak komunikasi agar tidak stres.",
            "Sikat bulu pendeknya secara berkala."
        ]
    },
    'Sphynx': {
        "karakter": "Unik tanpa bulu, sangat ramah, aktif, dan senang mencari kehangatan.",
        "perawatan": [
            "Wajib dimandikan secara rutin (1–2 minggu sekali) untuk membersihkan minyak alami kulitnya.",
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

st.markdown("---")
file_gambar = st.file_uploader("Pilih foto (Kucing / objek lain) (.jpg / .jpeg / .png)", type=["jpg", "jpeg", "png"])

if file_gambar is not None:
    st.image(file_gambar, caption="Foto yang Anda Unggah", use_container_width=True)
    
    # Proses gambar disesuaikan ke ukuran input 240x240
    img = tf.keras.utils.load_img(file_gambar, target_size=(240, 240))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    with st.spinner("AI sedang menganalisis gambar..."):
        prediksi = model.predict(img_array)
        score = prediksi[0]
        
        max_score = np.max(score)
        keyakinan_utama = 100 * max_score
        
        top_3_indices = np.argsort(score)[::-1][:3]

    st.markdown("### 📊 Hasil Analisis AI:")
    
    if keyakinan_utama < 45.0:
        st.error("❌ **Peringatan: Gambar Tidak Dikenali sebagai Kucing!**")
        st.warning(
            f"Tingkat keyakinan AI terlalu rendah (**{keyakinan_utama:.2f}%**). "
            "Kemungkinan besar foto ini **bukan kucing**, terlalu gelap, atau buram. "
            "Coba unggah foto kucing yang lebih jelas dan terang!"
        )
    else:
        juara_utama_key = daftar_ras[top_3_indices[0]]
        st.success(f"**Ras Kucing Utama:** {juara_utama_key.upper()} (Keyakinan: {keyakinan_utama:.2f}%)")
        
        st.markdown("#### 🥇🥈🥉 3 Peringkat Ras Teratas:")
        for i, idx in enumerate(top_3_indices):
            nama_ras = daftar_ras[idx]
            persen = 100 * score[idx]
            medali = ["🥇", "🥈", "🥉"][i]
            st.write(f"{medali} **{nama_ras}** — `{persen:.2f}%`")
        
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