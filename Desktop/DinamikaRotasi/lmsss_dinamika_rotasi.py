# lms_dinamika_rotasi_fix_error_kutipan.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid
import math
import numpy as np
import matplotlib.pyplot as plt

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="LMS Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
ADMIN_PASSWORD = "admin123"
GURU_PASSWORD = "guru123"
UPLOAD_FOLDER = "uploaded_media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FILES = {
    "data_hadir": "data_hadir.csv",
    "video_info": "video_info.json",
    "pre_test_info_p1": "pre_test_pertemuan_1.json",
    "pre_test_info_p2": "pre_test_pertemuan_2.json",
    "deskripsi_materi": "deskripsi_materi.json",
    "media_pembelajaran": "media_pembelajaran.json",
    "simulasi_virtual": "simulasi_virtual_info.json",
    "lkpd_info": "lkpd_info.json",
    "refleksi_info": "refleksi_info.json",
    "post_test_info": "post_test_info.json",
    "forum_diskusi": "forum_diskusi.csv",
    "hasil_nilai": "hasil_nilai.csv"
}

# Inisialisasi file jika belum ada
for key, file_path in FILES.items():
    if not os.path.exists(file_path):
        if file_path.endswith(".csv"):
            if key == "data_hadir":
                pd.DataFrame(columns=["email", "nama", "status", "waktu", "role"]).to_csv(file_path, index=False)
            elif key == "forum_diskusi":
                pd.DataFrame(columns=["id", "parent_id", "email", "nama", "pesan", "waktu", "role"]).to_csv(file_path, index=False)
            elif key == "hasil_nilai":
                pd.DataFrame(columns=["email", "nama", "jenis_penilaian", "jawaban_json", "nilai", "waktu_kerja", "role"]).to_csv(file_path, index=False)
        elif file_path.endswith(".json"):
            if key == "video_info":
                default_data = {
                    "judul": "Video Apersepsi: Dinamika Rotasi",
                    "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, kamu diminta menonton video apersepsi berikut untuk memicu rasa ingin tahumu tentang fenomena rotasi di sekitar kita.",
                    "file_video": "",
                    "waktu_update": ""
                }
            elif key == "pre_test_info_p1":
                default_data = {
                    "judul": "Pre-test: Dinamika Rotasi - Pertemuan 1",
                    "deskripsi": "Halo, Sobat Fisika ! Sebelum memulai pembelajaran hari ini, kamu diminta menjawab beberapa pertanyaan berikut berdasarkan pengalaman atau dugaanmu sendiri. Jawabanmu tidak dinilai, tetapi akan membantu guru memahami pemikiran awalmu. Jawablah dengan jujur dan sejujurnya — gunakan kata-katamu sendiri! Tidak ada jawaban salah ! Setelah menjawab, kamu akan menonton video apersepsi dan melakukan eksplorasi melalui simulasi interaktif untuk memperdalam pemahamanmu. Selamat bereksplorasi!",
                    "soal_list": [
                        {"id": "p1_q1", "teks": "Pernahkah kamu membuka pintu? Di bagian mana lebih mudah mendorongnya: dekat engsel atau di gagang pintu? Mengapa menurutmu?"},
                        {"id": "p1_q2", "teks": "Jika kamu menggunakan kunci inggris untuk membuka baut, apakah lebih mudah memegang ujungnya atau dekat baut? Jelaskan!"},
                        {"id": "p1_q3", "teks": "Bayangkan dua roda sepeda: satu polos, satu dipasangi beban di pinggirnya. Roda mana yang menurutmu lebih sulit diputar dari keadaan diam? Mengapa?"},
                        {"id": "p1_q4", "teks": "Menurutmu, apa yang membuat suatu benda “sulit” atau “mudah” berputar?"}
                    ]
                }
            elif key == "pre_test_info_p2":
                default_data = {
                    "judul": "Pre-test: Dinamika Rotasi - Pertemuan 2",
                    "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, coba jawab pertanyaan berikut berdasarkan intuisi atau pengalaman sehari-harimu. Jawabanmu hanya untuk memicu rasa ingin tahu — tidak ada yang dinilai benar atau salah. Tulislah jawabanmu sejujurnya. Setelah ini, kamu akan menjelajahi konsep-konsep menarik melalui simulasi virtual dan diskusi kelompok. Yuk, mulai eksplorasi !",
                    "soal_list": [
                        {"id": "p2_q1", "teks": "Pernah lihat penari balet atau pesenam berputar? Saat mereka menarik tangan ke badan, putarannya jadi lebih cepat atau lambat? Menurutmu, kenapa?"},
                        {"id": "p2_q2", "teks": "Jika sebuah roda sepeda sedang berputar bebas di udara (tanpa gesekan), apakah putarannya akan berhenti sendiri? Mengapa?"},
                        {"id": "p2_q3", "teks": "Apa perbedaan antara gerak lurus (translasi) dan gerak berputar (rotasi)? Berikan satu contoh benda yang mengalami kedua jenis gerak tersebut sekaligus (misalnya roda yang menggelinding)."},
                        {"id": "p2_q4", "teks": "Bisakah suatu benda berputar semakin cepat tanpa didorong lagi? Jika ya, dalam situasi apa?"}
                    ]
                }
            elif key == "deskripsi_materi":
                default_data = {
                    "judul": "Deskripsi Materi: Dinamika Rotasi",
                    "capaian_pembelajaran": "Pada fase F, peserta didik mampu menerapkan konsep dan prinsip vektor ke dalam kinematika dan dinamika gerak rotasi, usaha dan energi dalam sistem rotasi, serta dinamika fluida dalam gerak berputar. Peserta didik mampu memahami konsep tentang gerak rotasi dengan kecepatan sudut konstan serta mampu mengamati dan mengidentifikasi benda di sekitar yang mengalami gerak tersebut. Kemudian, peserta didik mampu memperdalam pemahaman fisika sesuai dengan minat untuk melanjutkan ke perguruan tinggi yang berhubungan dengan bidang fisika. Melalui kerja ilmiah, juga dibangun sikap ilmiah dan Profil Pelajar Pancasila, khususnya mandiri, inovatif, bernalar kritis, kreatif, dan bergotong royong.",
                    "tujuan_pembelajaran": [
                        "Peserta didik mampu menjelaskan konsep dinamika rotasi melalui eksplorasi langsung pada aplikasi simulasi berbasis Streamlit.",
                        "Peserta didik mampu menerapkan prinsip dinamika rotasi untuk memecahkan masalah kontekstual melalui simulasi dan latihan interaktif di platform Streamlit.",
                        "Peserta didik mampu menganalisis hubungan antara momen gaya, momen inersia, dan percepatan sudut dengan mengubah nilai parameter dalam simulasi virtual berbasis Streamlit."
                    ]
                }
            elif key == "media_pembelajaran":
                # 🔥 PERBAIKAN: Struktur lengkap untuk Pertemuan 1 & 2
                default_data = {
                    "judul": "Media Pembelajaran: Dinamika Rotasi",
                    "deskripsi": "Berikut adalah media pembelajaran tambahan untuk memperdalam pemahaman Anda tentang Dinamika Rotasi.",
                    "pertemuan_1": {
                        "judul": "Pertemuan 1",
                        "bahan_ajar": "### DINAMIKA ROTASI\nDinamika rotasi adalah ilmu yang mempelajari gerak rotasi (berputar) dengan mempertimbangkan komponen penyebabnya, yaitu momen gaya. Momen gaya atau torsi ini, menyebabkan percepatan sudut. Jika semua bagian suatu benda bergerak mengelilingi poros atau sumbu putarnya dan sumbu putarnya terletak pada salah satu bagiannya, benda tersebut dikatakan melakukan gerak rotasi (berputar). Dalam kehidupan sehari-hari, gerak rotasi dapat diamati pada berbagai objek seperti roda kendaraan yang berputar, baling – baling, kipas angin, atau gerakan planet yang mengorbit matahari.\n\n### Percobaan Sederhana: Menyelidiki Momen Inersia pada Pemutar Kayu\n\n**Tujuan:** Mengamati bagaimana massa dan distribusinya mempengaruhi momen inersia.\n\n**Alat dan Bahan:**\n- Piringan kayu atau CD/DVD bekas\n- Paku atau baut kecil sebagai poros\n- Benang dan pemberat kecil (misal baut atau mur)\n- Stopwatch\n- Penggaris untuk mengukur\n\n**Langkah Kerja:**\n1. Ambil piringan kayu atau CD/DVD dan buat lubang kecil di tengahnya untuk dijadikan poros.\n2. Pasang poros pada meja atau papan kayu sehingga piringan bisa berputar bebas.\n3. Ikat benang di tepi piringan dan lilitkan beberapa kali.\n4. Gantung pemberat di ujung benang sehingga saat dilepas, benang akan menarik piringan dan membuatnya berputar.\n5. Lepaskan pemberat dan gunakan stopwatch untuk mencatat waktu yang dibutuhkan untuk menyelesaikan satu putaran.\n6. Tambahkan massa di tepi piringan (misalnya dengan menempelkan koin atau mur di pinggir).\n7. Bandingkan perbedaan waktu putaran.",
                        "deskripsi": "Bahan ajar untuk Pertemuan 1",
                        "videos": [
                            {
                                "judul": "Contoh Gerak Rotasi - Skater",
                                "url": "https://www.youtube.com/embed/FmnkQ2ytlO8",
                                "sumber": "YouTube"
                            }
                        ],
                        "images": [
                            {
                                "judul": "Perbedaan Gerak Translasi dan Rotasi",
                                "url": "https://mafia.mafiaol.com/wp-content/uploads/2014/01/gerak-translasi-dan-rotasi.png",
                                "sumber": "Mafia Fisika"
                            },
                            {
                                "judul": "Ilustrasi Torsi",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Torque_animation.gif/220px-Torque_animation.gif",
                                "sumber": "Wikimedia Commons"
                            }
                        ]
                    },
                    "pertemuan_2": {
                        "judul": "Pertemuan 2",
                        "bahan_ajar": "### DINAMIKA ROTASI\nDinamika rotasi adalah ilmu yang mempelajari gerak rotasi (berputar) dengan mempertimbangkan komponen penyebabnya, yaitu momen gaya. Momen gaya atau torsi ini, menyebabkan percepatan sudut. Jika semua bagian suatu benda bergerak mengelilingi poros atau sumbu putarnya dan sumbu putarnya terletak pada salah satu bagiannya, benda tersebut dikatakan melakukan gerak rotasi (berputar). Dalam kehidupan sehari-hari, gerak rotasi dapat diamati pada berbagai objek seperti roda kendaraan yang berputar, baling – baling, kipas angin, atau gerakan planet yang mengorbit matahari.\n\n### Gerak Translasi vs Gerak Rotasi\n\n**Gerak Translasi:**\n- Energi kinetik itu energi yang dimiliki benda-benda yang bergerak.\n- Translasi bisa diartikan linear atau lurus.\n- Gerak translasi dapat didefinisikan sebagai gerak pergeseran suatu benda dengan bentuk dan lintasan yang sama di setiap titiknya.\n- Jadi sebuah benda dapat dikatakan melakukan gerak translasi (pergeseran) apabila setiap titik pada benda itu menempuh lintasan yang bentuk dan panjangnya sama.\n\n**Gambar 6: Contoh Gerak Translasi**\n\n**Gerak Rotasi:**\n- Gerak rotasi adalah gerak suatu benda yang berputar terhadap sumbu tertentu.\n- Setiap titik pada benda tersebut bergerak dalam lintasan lingkaran yang berpusat di sumbu putarnya.\n- Besaran penting dalam gerak rotasi adalah momen inersia, torsi, dan percepatan sudut.\n\n**Hubungan antara Gerak Translasi dan Rotasi:**\n- Gerak translasi dan rotasi sering terjadi bersamaan, misalnya roda sepeda yang berguling.\n- Pada gerak berguling, benda mengalami gerak translasi (berpindah tempat) dan gerak rotasi (berputar).",
                        "deskripsi": "Bahan ajar untuk Pertemuan 2",
                        "videos": [
                            {
                                "judul": "Penerapan Konsep Torsi - Kunci Inggris",
                                "url": "https://www.youtube.com/embed/kSSFq1cgVoA",
                                "sumber": "YouTube"
                            },
                            {
                                "judul": "Momen Inersia dalam Aksi",
                                "url": "https://www.youtube.com/embed/R68BjRLfm1Q",
                                "sumber": "YouTube Short"
                            }
                        ],
                        "images": [
                            {
                                "judul": "Ilustrasi Torsi",
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Torque_animation.gif/220px-Torque_animation.gif",
                                "sumber": "Wikimedia Commons"
                            }
                        ]
                    }
                }
            elif key == "simulasi_virtual":
                default_data = {
                    "judul": "Simulasi Virtual: Dinamika Rotasi",
                    "deskripsi": "Eksplorasi konsep Dinamika Rotasi secara interaktif!",
                    "petunjuk_penggunaan": """📘 **Petunjuk Penggunaan Simulasi PhET: Balancing Act**

💡 Simulasi ini akan membantu Anda memahami konsep kesetimbangan dan torsi secara interaktif.

**Ikuti langkah-langkah berikut untuk menggunakan simulasi:**

1.  **Buka PhET Simulasi**:
    Klik tautan berikut untuk membuka simulasi:  
    🔗 [https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_en.html](https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_en.html)

2.  **Pilih "Balance Lab"**:
    Setelah simulasi terbuka, pilih tab **"Balance Lab"** untuk memulai eksperimen kesetimbangan.

3.  **Tempatkan Massa ke Jungkat-Jungkit**:
    - Seret massa (benda kotak) ke posisi yang diinginkan di jungkat-jungkit.
    - Amati bagaimana jungkat-jungkit bereaksi terhadap penempatan massa.
    - Cobalah membuat jungkat-jungkit seimbang dengan mengatur posisi dan jumlah massa.

4.  **Pilih "Game"**:
    - Klik tab **"Game"** untuk menguji pemahaman Anda.
    - Pilih level permainan yang sesuai (Level 1 - 4).
    - Selesaikan tantangan dengan menyeimbangkan jungkat-jungkit sesuai instruksi.

5.  **Simulasikan Sesuai Perintah**:
    - Ikuti instruksi di setiap level permainan.
    - Gunakan pengetahuan tentang torsi dan kesetimbangan untuk menyelesaikan tantangan.
    - Catat hasil dan pengamatan Anda untuk laporan LKPD.

> 🎯 **Tujuan**: Memahami prinsip kesetimbangan rotasi dan hubungan antara massa, jarak, dan torsi.
""",
                    "simulasi_list": [
                        {"judul": "⚖️ Balancing Act (Aktivitas Keseimbangan) - PhET", "url": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_en.html", "sumber": "PhET Colorado"}
                    ]
                }
            elif key == "lkpd_info":
                default_data = {
                    "judul": "LKPD: Dinamika Rotasi - Analisis Torsi dan Durasi Putaran Gasing",
                    "deskripsi": "Lembar Kerja Peserta Didik untuk menganalisis hubungan antara gaya, lengan gaya, dan torsi dalam gerak rotasi menggunakan model gasing.",
                    "tujuan": [
                        "Peserta didik mampu menganalisis hubungan antara gaya, lengan gaya, dan torsi dalam gerak rotasi menggunakan model gasing.",
                        "Peserta didik mampu mengevaluasi hasil percobaan rotasi gasing untuk menentukan faktor-faktor yang mempengaruhi durasi dan kecepatan putaran.",
                        "Peserta didik mampu menyajikan data dalam bentuk laporan praktikum dan mempresentasikan di depan kelas."
                    ],
                    "materi": "Dinamika rotasi adalah ilmu yang mempelajari gerak rotasi (berputar) dengan mempertimbangkan komponen penyebabnya, yaitu momen gaya. Momen gaya atau torsi ini, menyebabkan percepatan sudut. Jika semua bagian suatu benda bergerak mengelilingi poros atau sumbu putarnya dan sumbu putarnya terletak pada salah satu bagiannya, benda tersebut dikatakan melakukan gerak rotasi (berputar). Dalam kehidupan sehari-hari, gerak rotasi dapat diamati pada berbagai objek seperti roda kendaraan yang berputar, baling – baling, kipas angin, atau gerakan planet yang mengorbit matahari.",
                    "petunjuk": [
                        "Perhatikan simulasi yang sudah dilakukan dalam pembelajaran.",
                        "Lakukan simulasi sesuai langkah kerja!",
                        "Jawablah pertanyaan-pertanyaan yang terdapat di LKPD ini secara berkelompok."
                    ],
                    "alat_bahan": [
                        "1 buah gasing (bisa dibuat dari CD bekas, tutup botol)",
                        "Stopwatch",
                        "Penggaris atau meteran",
                        "Tali (untuk memutar gasing)",
                        "Buku catatan"
                    ],
                    "langkah_kerja": [
                        "Rakit atau siapkan gasing (misalnya gasing dari CD bekas atau tutup botol).",
                        "Tentukan titik pusat poros gasing dan ukur panjang tali yang digunakan untuk memutar gasing.",
                        "Buat hipotesis: “Semakin besar gaya yang diberikan saat memutar gasing, maka semakin lama gasing berputar”.",
                        "Ukur panjang lengan gaya (jarak dari pusat poros ke titik gaya) untuk setiap percobaan.",
                        "Putar gasing dengan tiga variasi gaya (lemah, sedang, kuat).",
                        "Catat lama waktu putaran dengan stopwatch dari awal hingga berhenti.",
                        "Lakukan setiap variasi gaya sebanyak 3 kali."
                    ],
                    "tabel_header": ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"],
                    "analisis_pertanyaan": [
                        "Berdasarkan data waktu putar dari masing-masing gaya (lemah, sedang, kuat), bagaimana pengaruh besar gaya terhadap torsi dan durasi putaran gasing?",
                        "Hitung dan bandingkan nilai torsi relatif dari setiap gaya yang digunakan pada percobaan. Apakah data tersebut konsisten atau relevan dengan teori bahwa torsi berbanding lurus dengan gaya?",
                        "Dari hasil percobaan, gasing yang ditarik dengan gaya lebih besar dapat mencapai putaran awal yang lebih cepat dan berputar lebih lama. Jelaskan bagaimana fenomena ini terjadi berdasarkan prinsip torsi dalam sistem rotasi!"
                    ],
                    "kesimpulan_petunjuk": "Tulis kesimpulan kelompok Anda berdasarkan percobaan dan analisis di atas:",
                    "waktu_update": ""
                }
                    ]
                }
            elif key == "post_test_info":
                default_data = {
                    "judul": "Post-test: Dinamika Rotasi",
                    "deskripsi": "Uji pemahamanmu setelah mempelajari Dinamika Rotasi.",
                    "soal_list": [
                        {
                            "id": "pt1",
                            "teks": "(C2) Perbedaan utama antara gerak translasi dan rotasi adalah...",
                            "opsi": ["A. Gerak translasi lebih cepat daripada rotasi", "B. Gerak translasi tidak melibatkan poros", "C. Gerak rotasi hanya terjadi pada benda bulat", "D. Gerak rotasi tidak memiliki percepatan", "E. Gerak translasi tidak melibatkan gaya"],
                            "kunci": "B",
                            "skor": 2
                        },
                        {
                            "id": "pt2",
                            "teks": "(C2) Apa yang dimaksud dengan torsi?",
                            "opsi": ["A. Gaya yang bekerja pada benda diam", "B. Momen inersia yang menyebabkan percepatan", "C. Momen gaya yang menyebabkan rotasi", "D. Energi yang tersimpan dalam benda berputar", "E. Percepatan sudut benda"],
                            "kunci": "C",
                            "skor": 2
                        },
                        {
                            "id": "pt3",
                            "teks": "(C3) Sebuah roda sepeda berdiameter 0,5 m diberi gaya 10 N pada tepinya. Hitung torsi yang dihasilkan!",
                            "opsi": ["A. 2,5 Nm", "B. 5 Nm", "C. 10 Nm", "D. 15 Nm", "E. 20 Nm"],
                            "kunci": "A",
                            "skor": 7
                        },
                        {
                            "id": "pt4",
                            "teks": "(C3) Sebuah kipas angin memiliki momen inersia 0,5 kg·m². Jika torsi yang diberikan 10 Nm, hitung percepatan sudutnya!",
                            "opsi": ["A. 5 rad/s²", "B. 10 rad/s²", "C. 15 rad/s²", "D. 20 rad/s²", "E. 25 rad/s²"],
                            "kunci": "D",
                            "skor": 7
                        },
                        {
                            "id": "pt5",
                            "teks": "(C3) Seorang skater menarik tangannya ke dalam saat berputar. Fenomena ini menjelaskan prinsip...",
                            "opsi": ["A. Hukum II Newton untuk Rotasi", "B. Hukum Kekekalan Energi", "C. Hukum Kekekalan Momentum Sudut", "D. Hukum Gravitasi", "E. Hukum Pascal"],
                            "kunci": "C",
                            "skor": 7
                        },
                        {
                            "id": "pt6",
                            "teks": "(C4) Jika jarak dorong pintu dikurangi setengah, bagaimana perubahan torsinya?",
                            "opsi": ["A. Torsi menjadi setengah dari semula", "B. Torsi menjadi dua kali lebih besar", "C. Torsi tetap sama", "D. Torsi meningkat 4 kali", "E. Tidak bisa ditentukan karena tidak ada informasi arah gaya"],
                            "kunci": "A",
                            "skor": 15
                        },
                        {
                            "id": "pt7",
                            "teks": "(C4) Penari balet menarik tangan ke badan → kecepatan sudut...",
                            "opsi": ["A. Kecepatan sudut meningkat karena energi kinetik bertambah", "B. Kecepatan sudut meningkat karena momentum sudut kekal", "C. Kecepatan sudut menurun karena momen inersia berkurang", "D. Kecepatan sudut tetap sama meskipun momen inersia berubah", "E. Kecepatan sudut meningkat karena massa penari bertambah"],
                            "kunci": "B",
                            "skor": 15
                        },
                        {
                            "id": "pt8",
                            "teks": "(C4) Siapa menghasilkan torsi lebih besar: A (30N, 0,5m, 90°) atau B (40N, 0,4m, 30°)?",
                            "opsi": ["A. Orang A, karena gaya lebih tegak lurus", "B. Orang B, karena gaya lebih besar", "C. Torsinya sama karena gaya dan jarak saling mengimbangi", "D. Orang A, karena menghasilkan torsi maksimum", "E. Tidak bisa ditentukan tanpa mengetahui massa batang"],
                            "kunci": "D",
                            "skor": 15
                        },
                        {
                            "id": "pt9",
                            "teks": "(C4) Torsi di titik A (r=0,8m) vs B (r=0,4m) dengan gaya sama?",
                            "opsi": ["A. Torsi di titik A lebih kecil karena lengan gayanya lebih panjang", "B. Torsi di titik B lebih besar karena lengan gayanya lebih pendek", "C. Torsi di titik A dua kali lebih besar daripada di titik B", "D. Torsi di titik A dan B sama besar karena gayanya sama", "E. Torsi tidak dapat dibandingkan karena tergantung massa pintu"],
                            "kunci": "C",
                            "skor": 15
                        },
                        {
                            "id": "pt10",
                            "teks": "(C4) Jika τ=6 Nm, F=20N, r=0,6m, maka sudut θ = ?",
                            "opsi": ["A. Sudutnya adalah 30° karena sin θ = 0,5", "B. Sudutnya adalah 60° karena sin θ = √3/2", "C. Sudutnya adalah 90° karena sin θ = 1", "D. Sudutnya adalah 45° karena sin θ = √2/2", "E. Tidak dapat ditentukan karena tidak ada informasi arah gaya"],
                            "kunci": "A",
                            "skor": 15
                        }
                    ]
                }
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)

# Session state untuk login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "current_email" not in st.session_state:
    st.session_state.current_email = ""

# === FUNGSI LOGIN ===
def login():
    st.title("🔐 Login LMS Dinamika Rotasi")
    # 🔥 PERBAIKAN: Tambahkan key unik untuk text_input
    email = st.text_input("📧 Masukkan Email Anda:", key="email_login_input")

    if email:
        if email == "guru@dinamikarotasi.sch.id": # Ganti dengan email guru Anda
            password = st.text_input("🔑 Password Guru", type="password", key="pwd_guru_input")
            if st.button("Login sebagai Guru", key="btn_login_guru"):
                if password == "guru123": # Ganti dengan password guru Anda
                    st.session_state.role = "guru"
                    st.session_state.current_user = "Guru"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.session_state.hadir = True # Guru otomatis hadir
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
        elif email == "admin@dinamikarotasi.sch.id": # Ganti dengan email admin Anda
            password = st.text_input("🔑 Password Admin", type="password", key="pwd_admin_input")
            if st.button("Login sebagai Admin", key="btn_login_admin"):
                if password == "admin123": # Ganti dengan password admin Anda
                    st.session_state.role = "admin"
                    st.session_state.current_user = "Admin"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.session_state.hadir = True # Admin otomatis hadir
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
        else:
            # Asumsikan sebagai siswa
            if st.button("Login sebagai Siswa", key="btn_login_siswa"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title() # Ambil nama dari email
                st.session_state.current_email = email
                st.session_state.logged_in = True
                st.session_state.hadir = False # Siswa harus daftar hadir
                st.rerun()

# === FUNGSI PEMBANTU ===
def check_hadir():
    """Cek apakah siswa sudah daftar hadir."""
    if not st.session_state.get("hadir", False):
        st.warning("🔒 Silakan daftar hadir terlebih dahulu.")
        st.stop()

def muat_data(file_key):
    """Muat data dari file JSON atau CSV."""
    file_path = FILES[file_key]
    if os.path.exists(file_path):
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r", encoding='utf-8') as f:
                    return json.load(f)
            elif file_path.endswith(".csv"):
                return pd.read_csv(file_path)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return None

def simpan_data(file_key, data):
    """Simpan data ke file JSON atau CSV."""
    file_path = FILES[file_key]
    try:
        if file_path.endswith(".json"):
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif file_path.endswith(".csv"):
            data.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"Gagal menyimpan data ke {file_path}: {e}")

# === DASHBOARD GURU ===
def guru_page():
    menu = st.sidebar.selectbox(
        "Navigasi Guru",
        [
            "Daftar Hadir",
            "Video Apersepsi",
            "Pre-test",
            "Deskripsi Materi",
            "Media Pembelajaran",
            "Simulasi Virtual",
            "LKPD",
            "Post-test",
            "Forum Diskusi",
            "Hasil Penilaian"
        ]
    )

    # === MENU: Daftar Hadir ===
    if menu == "Daftar Hadir":
        st.header("📋 Daftar Hadir Siswa")
        df = muat_data("data_hadir")
        if df is not None and not df.empty:
            df_siswa = df[df["role"] == "siswa"]
            st.dataframe(df_siswa[["nama", "email", "status", "waktu"]].sort_values(by="waktu", ascending=False))
        else:
            st.info("Belum ada data kehadiran siswa.")

    # === MENU: Video Apersepsi ===
    elif menu == "Video Apersepsi":
        st.header("🎥 Upload & Kelola Video Apersepsi")
        video_data = muat_data("video_info")
        if not video_data:
            st.error("File video info rusak.")
            return

        with st.form("form_video_apresiasi"):
            judul_baru = st.text_input("Judul Video", value=video_data.get("judul", ""), key="judul_video_guru")
            desc_baru = st.text_area("Deskripsi Video", value=video_data.get("deskripsi", ""), height=150, key="desc_video_guru")
            vid = st.file_uploader("Upload video (MP4)", type=["mp4"], key="upload_video_guru")
            submitted = st.form_submit_button("💾 Simpan Video & Deskripsi")

        if submitted:
            if vid is not None:
                # Simpan video dengan nama unik
                unique_filename = f"{uuid.uuid4().hex}_{vid.name}"
                video_path_simpan = os.path.join(UPLOAD_FOLDER, unique_filename)
                with open(video_path_simpan, "wb") as f:
                    f.write(vid.read())
                video_data["file_video"] = unique_filename
            video_data["judul"] = judul_baru
            video_data["deskripsi"] = desc_baru
            video_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simpan_data("video_info", video_data)
            st.success("✅ Video apersepsi & deskripsi berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Video Apersepsi untuk Siswa")
        st.write(f"**{video_data.get('judul', 'Video Apersepsi')}**")
        st.info(video_data.get("deskripsi", ""))
        if video_data.get("file_video"):
            video_path = os.path.join(UPLOAD_FOLDER, video_data["file_video"])
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.warning("📁 File video belum ditemukan.")
        else:
            st.info("📁 Video belum diupload oleh guru.")

    # === MENU: Pre-test ===
    elif menu == "Pre-test":
        st.header("🧠 Edit Soal Pre-test")
        # Pilih pertemuan
        pertemuan = st.radio("Pilih Pertemuan:", ["Pertemuan 1", "Pertemuan 2"], horizontal=True, key="pilih_pertemuan_pre_guru")

        key_file = "pre_test_info_p1" if pertemuan == "Pertemuan 1" else "pre_test_info_p2"
        pre_test_data = muat_data(key_file)
        if not pre_test_data:
            st.error(f"Soal pre-test {pertemuan} belum diatur oleh guru.")
            return

        with st.form(f"form_edit_pre_test_{pertemuan.lower().replace(' ', '_')}"):
            judul_baru = st.text_input("Judul Pre-test", value=pre_test_data.get("judul", ""), key=f"judul_pre_{pertemuan.lower().replace(' ', '_')}")
            desc_baru = st.text_area("Deskripsi Pre-test", value=pre_test_data.get("deskripsi", ""), height=150, key=f"desc_pre_{pertemuan.lower().replace(' ', '_')}")
            
            soal_list = pre_test_data.get("soal_list", [])
            soal_baru_list = []
            for i, soal in enumerate(soal_list):
                teks_baru = st.text_area(f"Soal {i+1}", value=soal.get("teks", ""), key=f"pre_soal_{pertemuan.lower().replace(' ', '_')}_{i}")
                soal_baru_list.append({"id": soal.get("id", f"p1_q{i+1}"), "teks": teks_baru})

            submitted = st.form_submit_button(f"💾 Simpan Soal Pre-test {pertemuan}")

        if submitted:
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "soal_list": soal_baru_list
            }
            simpan_data(key_file, data_baru)
            st.success(f"✅ Soal pre-test {pertemuan} berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader(f"👁️‍🗨️ Pratinjau Pre-test {pertemuan} untuk Siswa")
        st.write(f"**{pre_test_data.get('judul', f'Pre-test {pertemuan}')}**")
        st.info(pre_test_data.get("deskripsi", ""))
        for i, soal in enumerate(pre_test_data.get("soal_list", []), 1):
            st.markdown(f"#### {i}. {soal['teks']}")

    # === MENU: Deskripsi Materi ===
    elif menu == "Deskripsi Materi":
        st.header("📚 Edit Deskripsi Materi")
        deskripsi_data = muat_data("deskripsi_materi")
        if not deskripsi_data:
            st.error("Deskripsi materi belum diatur oleh guru.")
            return

        with st.form("form_edit_deskripsi_guru"):
            judul_baru = st.text_input("Judul Deskripsi Materi", value=deskripsi_data.get("judul", ""), key="judul_deskripsi_guru")
            cp_baru = st.text_area("Capaian Pembelajaran (Fase F)", value=deskripsi_data.get("capaian_pembelajaran", ""), height=200, key="cp_deskripsi_guru")
            tp_list = deskripsi_data.get("tujuan_pembelajaran", [])
            tp_text = "\n".join(tp_list)
            tp_baru = st.text_area("Tujuan Pembelajaran (pisahkan dengan baris baru)", value=tp_text, height=150, key="tp_deskripsi_guru")
            submitted = st.form_submit_button("💾 Simpan Deskripsi Materi")

        if submitted:
            tp_list_baru = [item.strip() for item in tp_baru.split("\n") if item.strip()]
            data_baru = {
                "judul": judul_baru,
                "capaian_pembelajaran": cp_baru,
                "tujuan_pembelajaran": tp_list_baru
            }
            simpan_data("deskripsi_materi", data_baru)
            st.success("✅ Deskripsi materi berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Deskripsi Materi untuk Siswa")
        st.write(f"**{deskripsi_data.get('judul', 'Deskripsi Materi')}**")
        st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
        st.write(deskripsi_data.get("capaian_pembelajaran", ""))
        st.markdown("### 📌 Tujuan Pembelajaran")
        for i, tp in enumerate(deskripsi_data.get("tujuan_pembelajaran", []), 1):
            st.write(f"{i}. {tp}")

    # === MENU: Media Pembelajaran ===
    elif menu == "Media Pembelajaran":
        st.header("📚 Upload & Edit Media Pembelajaran")
        media_data = muat_data("media_pembelajaran")
        if not media_data:
            st.error("Media pembelajaran belum diatur oleh guru.")
            return

        tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

        # --- Pertemuan 1 ---
        with tab1:
            st.subheader("📅 Upload & Edit Media Pembelajaran - Pertemuan 1")
            p1_data = media_data.get("pertemuan_1", {})
            
            # Judul dan Deskripsi
            judul_p1 = st.text_input("Judul Pertemuan 1", value=p1_data.get("judul", ""), key="judul_p1")
            desc_p1 = st.text_area("Deskripsi Bahan Ajar Pertemuan 1", value=p1_data.get("deskripsi", ""), height=100, key="desc_p1")
            
            # Bahan Ajar (ditulis langsung, bukan upload PDF)
            bahan_ajar_p1 = st.text_area("📝 Bahan Ajar Pertemuan 1 (Ditulis Langsung)", value=p1_data.get("bahan_ajar", ""), height=300, key="bahan_p1")
            
            # Upload video & gambar tambahan
            st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 1")
            new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p1")
            new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p1")
            if st.button("➕ Tambahkan Video/Gambar Pertemuan 1", key="tambah_media_p1"):
                if new_video_url:
                    # Validasi sederhana untuk URL embed
                    if "youtube.com/embed/" in new_video_url:
                        p1_data["videos"].append({
                            "judul": f"Video {len(p1_data['videos']) + 1}",
                            "url": new_video_url,
                            "sumber": "YouTube/Guru"
                        })
                        st.success("✅ Video berhasil ditambahkan!")
                    else:
                        st.error("Harap gunakan URL 'embed' YouTube yang valid. Contoh: https://www.youtube.com/embed/VIDEO_ID")
                if new_image_url:
                    p1_data["images"].append({
                        "judul": f"Gambar {len(p1_data['images']) + 1}",
                        "url": new_image_url,
                        "sumber": "Guru"
                    })
                    st.success("✅ Gambar berhasil ditambahkan!")
                media_data["pertemuan_1"] = p1_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data("media_pembelajaran", media_data)
                st.rerun()

            # Tombol Simpan
            if st.button("💾 Simpan Media Pembelajaran Pertemuan 1", key="simpan_p1"):
                p1_data["judul"] = judul_p1
                p1_data["deskripsi"] = desc_p1
                p1_data["bahan_ajar"] = bahan_ajar_p1
                media_data["pertemuan_1"] = p1_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data("media_pembelajaran", media_data)
                st.success("✅ Media Pembelajaran Pertemuan 1 berhasil disimpan!")

            # Tampilkan pratinjau
            st.divider()
            st.subheader("👁️‍🗨️ Pratinjau Media Pembelajaran untuk Siswa")
            st.write(f"**{p1_data.get('judul', 'Pertemuan 1')}**")
            st.info(p1_data.get("deskripsi", ""))
            st.markdown("### 📚 Bahan Ajar")
            st.write(p1_data.get("bahan_ajar", ""))
            
            # Tampilkan video & gambar tambahan
            st.subheader("🎬 Video Tambahan")
            for i, video in enumerate(p1_data.get("videos", [])):
                st.markdown(f"**{i+1}. {video['judul']}**")
                st.video(video["url"])
                st.caption(f"Sumber: {video['sumber']}")
            
            st.subheader("🖼️ Gambar Tambahan")
            for i, image in enumerate(p1_data.get("images", [])):
                st.markdown(f"**{i+1}. {image['judul']}**")
                st.image(image["url"], caption=image["sumber"], use_column_width=True)

        # --- Pertemuan 2 ---
        with tab2:
            st.subheader("📅 Upload & Edit Media Pembelajaran - Pertemuan 2")
            p2_data = media_data.get("pertemuan_2", {})
            
            # Judul dan Deskripsi
            judul_p2 = st.text_input("Judul Pertemuan 2", value=p2_data.get("judul", ""), key="judul_p2")
            desc_p2 = st.text_area("Deskripsi Bahan Ajar Pertemuan 2", value=p2_data.get("deskripsi", ""), height=100, key="desc_p2")
            
            # Bahan Ajar (ditulis langsung, bukan upload PDF)
            bahan_ajar_p2 = st.text_area("📝 Bahan Ajar Pertemuan 2 (Ditulis Langsung)", value=p2_data.get("bahan_ajar", ""), height=300, key="bahan_p2")
            
            # Upload video & gambar tambahan
            st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 2")
            new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p2")
            new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p2")
            if st.button("➕ Tambahkan Video/Gambar Pertemuan 2", key="tambah_media_p2"):
                if new_video_url:
                    # Validasi sederhana untuk URL embed
                    if "youtube.com/embed/" in new_video_url:
                        p2_data["videos"].append({
                            "judul": f"Video {len(p2_data['videos']) + 1}",
                            "url": new_video_url,
                            "sumber": "YouTube/Guru"
                        })
                        st.success("✅ Video berhasil ditambahkan!")
                    else:
                        st.error("Harap gunakan URL 'embed' YouTube yang valid. Contoh: https://www.youtube.com/embed/VIDEO_ID")
                if new_image_url:
                    p2_data["images"].append({
                        "judul": f"Gambar {len(p2_data['images']) + 1}",
                        "url": new_image_url,
                        "sumber": "Guru"
                    })
                    st.success("✅ Gambar berhasil ditambahkan!")
                media_data["pertemuan_2"] = p2_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data("media_pembelajaran", media_data)
                st.rerun()

            # Tombol Simpan
            if st.button("💾 Simpan Media Pembelajaran Pertemuan 2", key="simpan_p2"):
                p2_data["judul"] = judul_p2
                p2_data["deskripsi"] = desc_p2
                p2_data["bahan_ajar"] = bahan_ajar_p2
                media_data["pertemuan_2"] = p2_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data("media_pembelajaran", media_data)
                st.success("✅ Media Pembelajaran Pertemuan 2 berhasil disimpan!")

            # Tampilkan pratinjau
            st.divider()
            st.subheader("👁️‍🗨️ Pratinjau Media Pembelajaran untuk Siswa")
            st.write(f"**{p2_data.get('judul', 'Pertemuan 2')}**")
            st.info(p2_data.get("deskripsi", ""))
            st.markdown("### 📚 Bahan Ajar")
            st.write(p2_data.get("bahan_ajar", ""))
            
            # Tampilkan video & gambar tambahan
            st.subheader("🎬 Video Tambahan")
            for i, video in enumerate(p2_data.get("videos", [])):
                st.markdown(f"**{i+1}. {video['judul']}**")
                st.video(video["url"])
                st.caption(f"Sumber: {video['sumber']}")
            
            st.subheader("🖼️ Gambar Tambahan")
            for i, image in enumerate(p2_data.get("images", [])):
                st.markdown(f"**{i+1}. {image['judul']}**")
                st.image(image["url"], caption=image["sumber"], use_column_width=True)

    # === MENU: Simulasi Virtual ===
    elif menu == "Simulasi Virtual":
        st.header("🧪 Edit Simulasi Virtual")
        simulasi_data = muat_data("simulasi_virtual")
        if not simulasi_data:
            st.error("Simulasi virtual belum diatur oleh guru.")
            return

        with st.form("form_edit_simulasi_guru"):
            judul_baru = st.text_input("Judul Simulasi Virtual", value=simulasi_data.get("judul", ""), key="judul_simulasi_guru")
            desc_baru = st.text_area("Deskripsi", value=simulasi_data.get("deskripsi", ""), height=100, key="desc_simulasi_guru")
            petunjuk_baru = st.text_area("Petunjuk Penggunaan (Markdown)", value=simulasi_data.get("petunjuk_penggunaan", ""), height=300, key="petunjuk_simulasi_guru")
            
            # Edit simulasi list
            simulasi_list = simulasi_data.get("simulasi_list", [])
            simulasi_baru_list = []
            for i, sim in enumerate(simulasi_list):
                judul_sim_baru = st.text_input(f"Judul Simulasi {i+1}", value=sim.get("judul", ""), key=f"judul_sim_{i}")
                url_sim_baru = st.text_input(f"URL Simulasi {i+1}", value=sim.get("url", ""), key=f"url_sim_{i}")
                simulasi_baru_list.append({"judul": judul_sim_baru, "url": url_sim_baru})

            submitted = st.form_submit_button("💾 Simpan Simulasi Virtual")

        if submitted:
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "petunjuk_penggunaan": petunjuk_baru,
                "simulasi_list": simulasi_baru_list
            }
            simpan_data("simulasi_virtual", data_baru)
            st.success("✅ Simulasi virtual berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Simulasi Virtual untuk Siswa")
        st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
        st.info(simulasi_data.get("deskripsi", ""))
        st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))
        for i, sim in enumerate(simulasi_data.get("simulasi_list", []), 1):
            st.markdown(f"#### {i}. {sim['judul']}")
            # PhET mungkin tidak bisa diembed langsung, jadi gunakan tombol link
            st.link_button("🔗 Buka Simulasi", sim["url"])

    # === MENU: LKPD ===
    elif menu == "LKPD":
        st.header("📄 Edit LKPD")
        lkpd_data = muat_data("lkpd_info")
        if not lkpd_data:
            st.error("LKPD belum diatur oleh guru.")
            return

        with st.form("form_edit_lkpd_guru"):
            judul_baru = st.text_input("Judul LKPD", value=lkpd_data.get("judul", ""), key="judul_lkpd_guru")
            desc_baru = st.text_area("Deskripsi LKPD", value=lkpd_data.get("deskripsi", ""), height=100, key="desc_lkpd_guru")
            
            st.subheader("🎯 Tujuan Pembelajaran")
            tujuan_list = lkpd_data.get("tujuan", [])
            tujuan_text = "\n".join(tujuan_list)
            tujuan_baru = st.text_area("Tujuan (pisahkan dengan baris baru)", value=tujuan_text, height=150, key="tujuan_lkpd_guru")
            
            st.subheader("📚 Dasar Teori")
            teori_baru = st.text_area("Dasar Teori", value=lkpd_data.get("materi", ""), height=200, key="teori_lkpd_guru")
            
            st.subheader("📋 Petunjuk Pengerjaan")
            petunjuk_list = lkpd_data.get("petunjuk", [])
            petunjuk_text = "\n".join(petunjuk_list)
            petunjuk_baru = st.text_area("Petunjuk (pisahkan dengan baris baru)", value=petunjuk_text, height=150, key="petunjuk_lkpd_guru")
            
            st.subheader("🛠️ Alat dan Bahan")
            alat_list = lkpd_data.get("alat_bahan", [])
            alat_text = "\n".join(alat_list)
            alat_baru = st.text_area("Alat dan Bahan (pisahkan dengan baris baru)", value=alat_text, height=150, key="alat_lkpd_guru")
            
            st.subheader("👣 Langkah Kerja")
            langkah_list = lkpd_data.get("langkah_kerja", [])
            langkah_text = "\n".join(langkah_list)
            langkah_baru = st.text_area("Langkah Kerja (pisahkan dengan baris baru)", value=langkah_text, height=200, key="langkah_lkpd_guru")
            
            st.subheader("📊 Tabel Hasil Pengamatan")
            header_lama = lkpd_data.get("tabel_header", [])
            header_baru_list = []
            cols_header = st.columns(len(header_lama))
            for i, col in enumerate(cols_header):
                if i < len(header_lama):
                    val = header_lama[i]
                else:
                    val = f"Kolom {i+1}"
                header_val = col.text_input(f"Header {i+1}", value=val, key=f"header_{i}")
                header_baru_list.append(header_val)
            
            st.subheader("🧠 Pertanyaan Analisis Data dan Diskusi")
            analisis_list = lkpd_data.get("analisis_pertanyaan", [])
            analisis_baru_list = []
            for i, q in enumerate(analisis_list):
                q_baru = st.text_area(f"Pertanyaan {i+1}", value=q, key=f"analisis_q_{i}")
                analisis_baru_list.append(q_baru)
            
            st.subheader("🎯 Petunjuk untuk Menulis Kesimpulan")
            kesimpulan_baru = st.text_area("Petunjuk Kesimpulan", value=lkpd_data.get("kesimpulan_petunjuk", ""), height=100, key="kesimpulan_lkpd_guru")
            
            submitted = st.form_submit_button("💾 Simpan Seluruh Perubahan LKPD")

        if submitted:
            tujuan_list_baru = [item.strip() for item in tujuan_baru.split("\n") if item.strip()]
            petunjuk_list_baru = [item.strip() for item in petunjuk_baru.split("\n") if item.strip()]
            alat_list_baru = [item.strip() for item in alat_baru.split("\n") if item.strip()]
            langkah_list_baru = [item.strip() for item in langkah_baru.split("\n") if item.strip()]
            
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "tujuan": tujuan_list_baru,
                "materi": teori_baru,
                "petunjuk": petunjuk_list_baru,
                "alat_bahan": alat_list_baru,
                "langkah_kerja": langkah_list_baru,
                "tabel_header": header_baru_list,
                "analisis_pertanyaan": analisis_baru_list,
                "kesimpulan_petunjuk": kesimpulan_baru,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data("lkpd_info", data_baru)
            st.success("✅ Seluruh LKPD berhasil diperbarui!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau LKPD untuk Siswa")
        st.write(f"**{lkpd_data.get('judul', 'LKPD')}**")
        st.info(lkpd_data.get("deskripsi", ""))
        
        st.markdown("### 🎯 Tujuan Pembelajaran")
        for i, t in enumerate(lkpd_data.get("tujuan", []), 1):
            st.write(f"{i}. {t}")
        
        st.markdown("### 📚 Dasar Teori")
        st.write(lkpd_data.get("materi", ""))
        
        st.markdown("### 📋 Petunjuk Pengerjaan")
        for i, p in enumerate(lkpd_data.get("petunjuk", []), 1):
            st.write(f"{i}. {p}")
        
        st.markdown("### 🛠️ Alat dan Bahan")
        for a in lkpd_data.get("alat_bahan", []):
            st.write(f"- {a}")
        
        st.markdown("### 👣 Langkah Kerja")
        for i, l in enumerate(lkpd_data.get("langkah_kerja", []), 1):
            st.write(f"{i}. {l}")
        
        st.markdown("### 📊 Tabel Hasil Pengamatan")
        header_list = lkpd_data.get("tabel_header", ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"])
        st.table([header_list] + [["", "", "", "", ""]] * 3) # Tampilkan tabel kosong untuk pratinjau
        
        st.markdown("### 🧠 Pertanyaan Analisis Data dan Diskusi")
        for i, q in enumerate(lkpd_data.get("analisis_pertanyaan", []), 1):
            st.markdown(f"**{i}. {q}**")
        
        st.markdown("### 🎯 Kesimpulan")
        st.write(lkpd_data.get("kesimpulan_petunjuk", ""))

    # === MENU: Post-test ===
    elif menu == "Post-test":
        st.header("📝 Edit Soal Post-test")
        post_test_data = muat_data("post_test_info")
        if not post_test_data:
            st.error("Soal post-test belum diatur oleh guru.")
            return

        with st.form("form_edit_post_test_guru"):
            judul_baru = st.text_input("Judul Post-test", value=post_test_data.get("judul", ""), key="judul_post_test_guru")
            desc_baru = st.text_area("Deskripsi Post-test", value=post_test_data.get("deskripsi", ""), height=150, key="desc_post_test_guru")
            
            st.subheader("📄 Daftar Soal Post-test (10 Soal)")
            soal_list = post_test_data.get("soal_list", [])
            soal_baru_list = []
            for i in range(10): # Pastikan ada 10 soal
                if i < len(soal_list):
                    soal = soal_list[i]
                else:
                    soal = {
                        "id": f"pt{i+1}",
                        "teks": "",
                        "opsi": ["", "", "", "", ""],
                        "kunci": "A",
                        "skor": 10
                    }
                st.markdown(f"#### Soal {i+1}")
                teks_baru = st.text_area("Teks Soal", value=soal.get("teks", ""), key=f"pt_teks_{i}")
                opsi_baru_text = ", ".join(soal.get("opsi", []))
                opsi_baru = st.text_input("Opsi Jawaban (pisahkan dengan koma)", value=opsi_baru_text, key=f"pt_opsi_{i}")
                kunci_lama = soal.get("kunci", "A")
                kunci_baru = st.selectbox("Kunci Jawaban", ["A", "B", "C", "D", "E"], index=["A", "B", "C", "D", "E"].index(kunci_lama) if kunci_lama in ["A", "B", "C", "D", "E"] else 0, key=f"pt_kunci_{i}")
                skor_baru = st.number_input("Skor Soal", min_value=1, value=soal.get("skor", 10), key=f"pt_skor_{i}")
                
                soal_baru_list.append({
                    "id": soal.get("id", f"pt{i+1}"),
                    "teks": teks_baru,
                    "opsi": [item.strip() for item in opsi_baru.split(",") if item.strip()],
                    "kunci": kunci_baru,
                    "skor": skor_baru
                })

            submitted = st.form_submit_button("💾 Simpan Soal Post-test")

        if submitted:
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "soal_list": soal_baru_list,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data("post_test_info", data_baru)
            st.success("✅ Soal post-test berhasil diperbarui!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Post-test untuk Siswa")
        st.write(f"**{post_test_data.get('judul', 'Post-test')}**")
        st.info(post_test_data.get("deskripsi", ""))
        for i, soal in enumerate(post_test_data.get("soal_list", []), 1):
            st.markdown(f"#### {i}. {soal['teks']}")
            opsi_list = soal.get("opsi", [])
            for j, opsi in enumerate(opsi_list):
                st.write(f"{chr(65+j)}. {opsi}")
            st.write(f"**Kunci Jawaban (Guru Only):** {soal['kunci']}")
            st.write(f"**Skor:** {soal['skor']}")
            st.divider()

    # === MENU: Forum Diskusi ===
    elif menu == "Forum Diskusi":
        st.header("💬 Forum Diskusi")
        df = muat_data("forum_diskusi")
        if df is not None and not df.empty:
            df_siswa = df[df["role"] == "siswa"]
            for _, row in df_siswa.sort_values(by="id", ascending=False).iterrows():
                st.markdown(f"**{row['nama']}** ({row['email']}) • _{row['waktu']}_")
                st.write(row["pesan"])
                st.divider()
        else:
            st.info("Belum ada diskusi.")

    # === MENU: Hasil Penilaian ===
    elif menu == "Hasil Penilaian":
        st.header("📊 Hasil Penilaian Siswa")
        df = muat_data("hasil_nilai")
        if df is not None and not df.empty:
            df_siswa = df[df["role"] == "siswa"]
            st.dataframe(df_siswa[["nama", "jenis_penilaian", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
        else:
            st.info("Belum ada data penilaian.")

# === DASHBOARD SISWA ===
def siswa_page():
    menu = st.sidebar.selectbox(
        "Navigasi Siswa",
        [
            "Daftar Hadir",
            "Video Apersepsi",
            "Pre-test",
            "Deskripsi Materi",
            "Media Pembelajaran",
            "Simulasi Virtual",
            "LKPD",
            "Post-test",
            "Forum Diskusi",
            "Hasil Penilaian"
        ]
    )

    # === MENU: Daftar Hadir ===
    if menu == "Daftar Hadir":
        st.header("📝 Daftar Hadir")
        nama = st.text_input("Nama Lengkap", value=st.session_state.current_user)
        status = st.radio("Status Kehadiran", ["Hadir", "Tidak Hadir"])

        if st.button("✅ Simpan Kehadiran"):
            if not nama.strip():
                st.error("Nama tidak boleh kosong!")
            else:
                df = muat_data("data_hadir")
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": nama.strip(),
                    "status": status,
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                simpan_data("data_hadir", df)
                st.session_state.hadir = (status == "Hadir")
                st.success(f"✅ Terima kasih, **{nama}**! Status kehadiran Anda: **{status}**.")

    # === MENU: Video Apersepsi ===
    elif menu == "Video Apersepsi":
        st.header("🎥 Video Apersepsi")
        check_hadir()
        video_data = muat_data("video_info")
        if not video_data:
            st.error("Video apersepsi belum diatur oleh guru.")
            return

        st.write(f"**{video_data.get('judul', 'Video Apersepsi')}**")
        # ✅ Tambahkan deskripsi video
        st.info(video_data.get("deskripsi", ""))
        if video_data.get("file_video"):
            video_path = os.path.join(UPLOAD_FOLDER, video_data["file_video"])
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.warning("📁 File video belum ditemukan.")
        else:
            st.info("📁 Video belum diupload oleh guru.")

    # === MENU: Pre-test ===
    elif menu == "Pre-test":
        st.header("🧠 Pre-test")
        check_hadir()
        # Pilih pertemuan
        pertemuan = st.selectbox("Pilih Pertemuan:", ["Pertemuan 1", "Pertemuan 2"], key="pilih_pertemuan_pre_siswa")

        key_file = "pre_test_info_p1" if pertemuan == "Pertemuan 1" else "pre_test_info_p2"
        pre_test_data = muat_data(key_file)
        if not pre_test_data:
            st.error(f"Soal pre-test {pertemuan} belum diatur oleh guru.")
            return

        st.write(f"**{pre_test_data.get('judul', f'Pre-test {pertemuan}')}**")
        st.info(pre_test_data.get("deskripsi", ""))

        jawaban_dict = {}
        soal_list = pre_test_data.get("soal_list", [])

        with st.form(f"form_pre_test_{pertemuan.lower().replace(' ', '_')}"):
            for i, soal in enumerate(soal_list):
                st.markdown(f"#### {i+1}. {soal['teks']}")
                jawaban = st.text_area("Jawaban Anda:", key=soal["id"], height=100)
                jawaban_dict[soal["id"]] = jawaban

            submitted = st.form_submit_button(f"✅ Kirim Jawaban Pre-test {pertemuan}")

            if submitted:
                if any(not v.strip() for v in jawaban_dict.values()):
                    st.error("⚠️ Mohon jawab semua pertanyaan.")
                else:
                    # Simpan jawaban ke file CSV
                    df = muat_data("hasil_nilai")
                    jawaban_json_str = json.dumps(jawaban_dict)
                    new_entry = pd.DataFrame([{
                        "email": st.session_state.current_email,
                        "nama": st.session_state.current_user,
                        "jenis_penilaian": f"Pre-test {pertemuan}",
                        "jawaban_json": jawaban_json_str,
                        "nilai": 0, # Pre-test tidak dinilai
                        "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "role": "siswa"
                    }])
                    df = pd.concat([df, new_entry], ignore_index=True)
                    simpan_data("hasil_nilai", df)
                    st.success(f"✅ Jawaban pre-test {pertemuan} berhasil dikirim!")

    # === MENU: Deskripsi Materi ===
    elif menu == "Deskripsi Materi":
        st.header("📚 Deskripsi Materi: Dinamika Rotasi")
        check_hadir()
        deskripsi_data = muat_data("deskripsi_materi")
        if not deskripsi_data:
            st.error("Deskripsi materi belum diatur oleh guru.")
            return

        st.write(f"**{deskripsi_data.get('judul', 'Deskripsi Materi')}**")
        st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
        st.write(deskripsi_data.get("capaian_pembelajaran", ""))
        st.markdown("### 📌 Tujuan Pembelajaran")
        for i, tp in enumerate(deskripsi_data.get("tujuan_pembelajaran", []), 1):
            st.write(f"{i}. {tp}")

    # === MENU: Media Pembelajaran ===
    elif menu == "Media Pembelajaran":
        st.header("📚 Media Pembelajaran")
        check_hadir()
        media_data = muat_data("media_pembelajaran")
        if not media_data:
            st.error("Media pembelajaran belum diatur oleh guru.")
            return

        st.write(f"**{media_data.get('judul', 'Media Pembelajaran')}**")
        st.info(media_data.get("deskripsi", ""))

        tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

        # --- TAB 1: Pertemuan 1 ---
        with tab1:
            p1_data = media_data.get("pertemuan_1", {})
            st.write(f"**{p1_data.get('judul', 'Pertemuan 1')}**")
            st.info(p1_data.get("deskripsi", ""))
            
            # Tampilkan Bahan Ajar (teks langsung dari guru)
            st.markdown("### 📚 Bahan Ajar")
            st.write(p1_data.get("bahan_ajar", ""))
            
            # Tampilkan video & gambar tambahan
            st.subheader("🎬 Video Tambahan")
            for i, video in enumerate(p1_data.get("videos", [])):
                st.markdown(f"**{i+1}. {video['judul']}**")
                st.video(video["url"])
                st.caption(f"Sumber: {video['sumber']}")
            
            st.subheader("🖼️ Gambar Tambahan")
            for i, image in enumerate(p1_data.get("images", [])):
                st.markdown(f"**{i+1}. {image['judul']}**")
                st.image(image["url"], caption=image["sumber"], use_column_width=True)

        # --- TAB 2: Pertemuan 2 ---
        with tab2:
            p2_data = media_data.get("pertemuan_2", {})
            st.write(f"**{p2_data.get('judul', 'Pertemuan 2')}**")
            st.info(p2_data.get("deskripsi", ""))
            
            # Tampilkan Bahan Ajar (teks langsung dari guru)
            st.markdown("### 📚 Bahan Ajar")
            st.write(p2_data.get("bahan_ajar", ""))
            
            # Tampilkan video & gambar tambahan
            st.subheader("🎬 Video Tambahan")
            for i, video in enumerate(p2_data.get("videos", [])):
                st.markdown(f"**{i+1}. {video['judul']}**")
                st.video(video["url"])
                st.caption(f"Sumber: {video['sumber']}")
            
            st.subheader("🖼️ Gambar Tambahan")
            for i, image in enumerate(p2_data.get("images", [])):
                st.markdown(f"**{i+1}. {image['judul']}**")
                st.image(image["url"], caption=image["sumber"], use_column_width=True)

    # === MENU: Simulasi Virtual ===
    elif menu == "Simulasi Virtual":
        st.header("🧪 Simulasi Virtual")
        check_hadir()
        simulasi_data = muat_data("simulasi_virtual")
        if not simulasi_data:
            st.error("Simulasi virtual belum diatur oleh guru.")
            return

        st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
        st.info(simulasi_data.get("deskripsi", ""))
        st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))
        
        # Simulasi Internal Torsi (Contoh)
        st.subheader("⚖️ Simulasi Torsi (τ = r × F × sin(θ))")
        col1, col2, col3 = st.columns(3)
        with col1:
            r = st.slider("Jarak dari poros (r) [m]", 0.1, 2.0, 1.0, 0.1)
        with col2:
            F = st.slider("Besar gaya (F) [N]", 1, 20, 10, 1)
        with col3:
            theta_deg = st.slider("Sudut gaya (θ) [derajat]", 0, 180, 90, 5)
        
        import math
        theta_rad = math.radians(theta_deg)
        torsi = r * F * math.sin(theta_rad)
        
        st.success(f"**Torsi yang dihasilkan:** *{torsi:.2f} N·m*")
        
        # Simulasi Internal Momen Inersia (Contoh sederhana)
        st.subheader("(inertia) Simulasi Momen Inersia")
        st.info("Pilih bentuk benda untuk melihat rumus momen inersia (I).")
        bentuk = st.selectbox("Pilih Bentuk Benda:", ["Silinder Pejal", "Silinder Berongga", "Bola Pejal", "Bola Berongga"])
        rumus_i = {
            "Silinder Pejal": "I = ½ M R²",
            "Silinder Berongga": "I = M R²",
            "Bola Pejal": "I = (2/5) M R²",
            "Bola Berongga": "I = (2/3) M R²"
        }
        st.write(f"**{bentuk}**: {rumus_i[bentuk]}")
        
        # Tampilkan link PhET (karena embed mungkin diblokir)
        st.divider()
        st.subheader("🔗 Simulasi PhET (Eksternal)")
        simulasi_list = simulasi_data.get("simulasi_list", [])
        for i, sim in enumerate(simulasi_list, 1):
            st.markdown(f"#### {i}. {sim['judul']}")
            st.link_button("🔗 Buka Simulasi", sim["url"])

    # === MENU: LKPD ===
    elif menu == "LKPD":
        st.header("📄 LKPD: Dinamika Rotasi")
        check_hadir()
        lkpd_data = muat_data("lkpd_info")
        if not lkpd_data:
            st.error("LKPD belum diatur oleh guru.")
            return

        st.write(f"**{lkpd_data.get('judul', 'LKPD')}**")
        st.info(lkpd_data.get("deskripsi", ""))

        st.markdown("### 🎯 Tujuan Pembelajaran")
        for i, t in enumerate(lkpd_data.get("tujuan", []), 1):
            st.write(f"{i}. {t}")

        st.markdown("### 📚 Dasar Teori")
        st.write(lkpd_data.get("materi", ""))

        st.markdown("### 📋 Petunjuk Pengerjaan")
        for i, p in enumerate(lkpd_data.get("petunjuk", []), 1):
            st.write(f"{i}. {p}")

        st.markdown("### 🛠️ Alat dan Bahan")
        for a in lkpd_data.get("alat_bahan", []):
            st.write(f"- {a}")

        st.markdown("### 👣 Langkah Kerja")
        for i, l in enumerate(lkpd_data.get("langkah_kerja", []), 1):
            st.write(f"{i}. {l}")

        st.markdown("### 📊 Tabel Hasil Pengamatan")
        header_list = lkpd_data.get("tabel_header", ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"])
        tabel_data = []
        for i in range(3): # Misalnya 3 baris untuk 3 variasi gaya
            cols = st.columns(len(header_list))
            baris_data = {}
            for j, header in enumerate(header_list):
                with cols[j]:
                    if j == 0: # Kolom No.
                        st.write(f"**{i+1}**")
                        baris_data[header] = str(i+1)
                    else:
                        nilai = st.text_input("", key=f"tabel_{i}_{j}")
                        baris_data[header] = nilai
            tabel_data.append(baris_data)

        st.markdown("### 🧠 Analisis Data dan Diskusi")
        jawaban_analisis = {}
        for i, q in enumerate(lkpd_data.get("analisis_pertanyaan", []), 1):
            st.markdown(f"**{i}. {q}**")
            jawaban = st.text_area("Jawaban Anda:", key=f"analisis_q{i}", height=100)
            jawaban_analisis[f"analisis_q{i}"] = jawaban

        st.markdown("### 🎯 Kesimpulan")
        kesimpulan = st.text_area(lkpd_data.get("kesimpulan_petunjuk", "Tulis kesimpulan kelompok Anda:"), height=150)

        if st.button("✅ Simpan Jawaban LKPD"):
            if any(not v.strip() for v in jawaban_analisis.values()) or not kesimpulan.strip():
                st.error("⚠️ Mohon jawab semua pertanyaan dan isi kesimpulan!")
            else:
                df = muat_data("hasil_nilai")
                jawaban_lkpd = {
                    "tabel": str(tabel_data),
                    "analisis": str(jawaban_analisis),
                    "kesimpulan": kesimpulan.strip()
                }
                jawaban_json_str = json.dumps(jawaban_lkpd)
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "jenis_penilaian": "LKPD",
                    "jawaban_json": jawaban_json_str,
                    "nilai": 0, # Nilai akan diisi oleh guru
                    "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                simpan_data("hasil_nilai", df)
                st.success("✅ Jawaban LKPD berhasil disimpan!")

    # === MENU: Post-test ===
    elif menu == "Post-test":
        st.header("📝 Post-test: Dinamika Rotasi")
        check_hadir()
        post_test_data = muat_data("post_test_info")
        if not post_test_data:
            st.error("Soal post-test belum diatur oleh guru.")
            return

        st.write(f"**{post_test_data.get('judul', 'Post-test')}**")
        st.info(post_test_data.get("deskripsi", ""))

        jawaban_dict = {}
        soal_list = post_test_data.get("soal_list", [])
        for i, soal in enumerate(soal_list):
            st.markdown(f"#### {i+1}. {soal['teks']}")
            opsi_list = soal.get("opsi", [])
            pilihan = [f"{chr(65+j)}. {opsi}" for j, opsi in enumerate(opsi_list)]
            jawaban = st.radio("Pilih jawaban:", pilihan, key=soal["id"])
            jawaban_dict[soal["id"]] = jawaban[0] if jawaban else ""

        if st.button("✅ Kirim Jawaban Post-test"):
            if any(not v.strip() for v in jawaban_dict.values()):
                st.error("⚠️ Mohon jawab semua pertanyaan.")
            else:
                # Hitung nilai
                nilai_total = 0
                for soal in soal_list:
                    if jawaban_dict.get(soal["id"]) == soal["kunci"]:
                        nilai_total += soal["skor"]
                
                # Simpan jawaban ke file CSV
                df = muat_data("hasil_nilai")
                jawaban_json_str = json.dumps(jawaban_dict)
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "jenis_penilaian": "Post-test",
                    "jawaban_json": jawaban_json_str,
                    "nilai": nilai_total,
                    "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                simpan_data("hasil_nilai", df)
                
                # Tampilkan hasil
                st.success("✅ Jawaban post-test berhasil dikirim!")
                st.subheader("📊 Hasil Penilaian Anda")
                total_skor = sum(soal["skor"] for soal in soal_list)
                st.metric("Nilai Total", f"{nilai_total}/{total_skor}")
                
                # Deskripsi singkat berdasarkan nilai
                persentase = (nilai_total / total_skor) * 100 if total_skor > 0 else 0
                if persentase >= 75:
                    st.balloons()
                    st.success("🎉 Luar biasa! Pemahaman Anda sangat baik. Pertahankan semangat belajar!")
                elif persentase >= 60:
                    st.info("👍 Bagus! Pemahaman Anda sudah cukup. Tingkatkan lagi untuk hasil yang lebih maksimal!")
                else:
                    st.warning("📚 Hasil belajar Anda perlu ditingkatkan. Pelajari kembali materinya dan jangan ragu bertanya!")

    # === MENU: Forum Diskusi ===
    elif menu == "Forum Diskusi":
        st.header("💬 Forum Diskusi")
        check_hadir()
        
        with st.form("form_diskusi"):
            pesan = st.text_area("Tulis pesan Anda:", max_chars=300)
            kirim = st.form_submit_button("📤 Kirim")

        if kirim and pesan.strip():
            df = muat_data("forum_diskusi")
            new_id = df["id"].max() + 1 if not df.empty else 1
            new_row = pd.DataFrame([{
                "id": new_id,
                "parent_id": -1,
                "email": st.session_state.current_email,
                "nama": st.session_state.current_user,
                "pesan": pesan.strip(),
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "role": "siswa"
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(FILES["forum_diskusi"], index=False)
            st.success("✅ Pesan berhasil dikirim!")
            st.rerun()

        # Tampilkan riwayat diskusi
        st.divider()
        st.subheader("📜 Riwayat Diskusi")
        df = muat_data("forum_diskusi")
        if df is not None and not df.empty:
            df_siswa = df[df["role"] == "siswa"]
            for _, row in df_siswa.sort_values(by="id", ascending=False).iterrows():
                st.markdown(f"**{row['nama']}** ({row['email']}) • _{row['waktu']}_")
                st.write(row["pesan"])
                st.divider()
        else:
            st.info("Belum ada diskusi. Jadilah yang pertama mengirim pesan!")

    # === MENU: Hasil Penilaian ===
    elif menu == "Hasil Penilaian":
        st.header("📊 Hasil Penilaian Anda")
        check_hadir()
        
        df = muat_data("hasil_nilai")
        if df is not None and not df.empty:
            df_siswa = df[
                (df["email"] == st.session_state.current_email) & 
                (df["role"] == "siswa")
            ]
            if df_siswa.empty:
                st.info("Anda belum mengerjakan penilaian.")
            else:
                st.dataframe(df_siswa[["jenis_penilaian", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
        else:
            st.info("Belum ada data penilaian.")

# === MAIN APP ===
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "role", "current_user", "current_email", "hadir"]:
            st.session_state.pop(key, None)
        st.rerun()

    # Tampilkan halaman berdasarkan role
    if st.session_state.role == "guru":
        dashboard_guru()
    elif st.session_state.role == "admin":
        # Admin bisa melihat halaman guru
        dashboard_guru()
    elif st.session_state.role == "siswa":
        dashboard_siswa()