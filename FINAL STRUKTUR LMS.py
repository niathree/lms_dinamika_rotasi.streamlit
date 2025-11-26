import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid
import streamlit.components.v1 as components

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="LMS Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
ADMIN_PASSWORD = "admin123"
GURU_PASSWORD = "guru123"
UPLOAD_FOLDER = "uploaded_media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- FILE KONFIGURASI ---
FILES = {
    "data_hadir": "data_hadir.csv",
    "video_info": "video_info.json",
    # File-file baru untuk modul yang diganti
    "pre_test_soal": "pre_test_soal.json",
    "simulasi_virtual": "simulasi_virtual.json",
    "post_test": "post_test.json",
    "forum_diskusi": "forum_diskusi.json", # Ubah ke JSON agar sesuai dengan kode baru
    # File-file dari kode lama
    "deskripsi_materi": "deskripsi_materi.json",
    "media_pembelajaran": "media_pembelajaran_dinamika_rotasi.json",
    "lkpd": "lkpd_info.json",
    "refleksi": "refleksi_info.json",
    "hasil_nilai": "hasil_nilai.csv",
}

# File untuk menyimpan waktu terakhir update elemen (untuk notifikasi)
NOTIFIKASI_FILE = "notifikasi_update.json"

# Inisialisasi file jika belum ada
for key, file_path in FILES.items():
    if not os.path.exists(file_path):
        if file_path.endswith(".csv"):
            if key == "data_hadir":
                pd.DataFrame(columns=["email", "nama", "status", "waktu", "role"]).to_csv(file_path, index=False)
            elif key == "hasil_nilai":
                pd.DataFrame(columns=["email", "nama", "jenis_penilaian", "jawaban_json", "nilai", "waktu_kerja", "role"]).to_csv(file_path, index=False)
        elif file_path.endswith(".json"):
            # Data default untuk modul yang diganti
            if key == "pre_test_soal":
                default_data = {
                    "judul": "Pre-test Fisika: Dinamika Rotasi",
                    "deskripsi": "Jawablah pertanyaan berikut dengan jelas dan singkat.",
                    "soal_list": [
                        {
                            "id": "s1",
                            "teks": "Jelaskan pengertian momen gaya (torsi) dan tuliskan rumusnya. Jelaskan pula makna fisis dari masing-masing variabel dalam rumus tersebut.",
                            "kunci": "Momen gaya (torsi) adalah ukuran kecenderungan suatu gaya untuk memutar benda terhadap suatu poros. Rumus: τ = r × F = rF sin θ. r adalah lengan momen, F adalah gaya, θ adalah sudut antara r dan F.",
                            "rubrik": {
                                "3": "Menjelaskan torsi, menyebutkan rumus, dan menjelaskan makna masing-masing variabel.",
                                "2": "Menjelaskan torsi dan rumus, tetapi kurang menjelaskan makna variabel.",
                                "1": "Menjelaskan torsi saja atau menyebut rumus tanpa penjelasan.",
                                "0": "Tidak menjawab atau jawaban salah."
                            }
                        },
                        {
                            "id": "s2",
                            "teks": "Apa yang dimaksud dengan momen inersia? Jelaskan perbedaannya dengan massa dalam gerak translasi.",
                            "kunci": "Momen inersia adalah ukuran kelembaman benda terhadap perubahan gerak rotasi. Ia berperan dalam gerak rotasi seperti massa dalam gerak translasi. Semakin besar momen inersia, semakin sulit benda diputar.",
                            "rubrik": {
                                "3": "Menjelaskan definisi dan peran momen inersia serta perbedaannya dengan massa.",
                                "2": "Menjelaskan definisi dan menyebutkan perbedaannya, tetapi kurang lengkap.",
                                "1": "Menjelaskan definisi saja.",
                                "0": "Tidak menjawab atau jawaban salah."
                            }
                        },
                        {
                            "id": "s3",
                            "teks": "Tuliskan rumus momentum sudut dan jelaskan hukum kekekalan momentum sudut. Berikan contoh penerapannya dalam kehidupan sehari-hari.",
                            "kunci": "L = Iω. Hukum kekekalan momentum sudut menyatakan bahwa jika torsi luar nol, maka momentum sudut tetap. Contoh: pemain es skating memutar tubuhnya dengan mengurangi jari-jari (I berkurang, ω bertambah).",
                            "rubrik": {
                                "3": "Menuliskan rumus, menjelaskan hukum, dan memberikan contoh penerapan.",
                                "2": "Menuliskan rumus dan menjelaskan hukum, tetapi tanpa contoh.",
                                "1": "Menuliskan rumus saja.",
                                "0": "Tidak menjawab atau jawaban salah."
                            }
                        },
                        {
                            "id": "s4",
                            "teks": "Jelaskan perbedaan antara energi kinetik translasi dan energi kinetik rotasi. Tuliskan rumus masing-masing.",
                            "kunci": "Energi kinetik translasi adalah energi akibat gerak lurus (EK = 1/2 mv²). Energi kinetik rotasi adalah energi akibat gerak putar (EK = 1/2 Iω²).",
                            "rubrik": {
                                "3": "Menjelaskan perbedaan dan menuliskan kedua rumus dengan benar.",
                                "2": "Menjelaskan perbedaan tetapi hanya menuliskan satu rumus.",
                                "1": "Menjelaskan perbedaan tanpa rumus.",
                                "0": "Tidak menjawab atau jawaban salah."
                            }
                        },
                        {
                            "id": "s5",
                            "teks": "Sebuah silinder pejal dengan massa M dan jari-jari R menggelinding tanpa slip. Jika kecepatan sudutnya ω, hitung energi kinetik total silinder tersebut.",
                            "kunci": "EK_total = EK_translasi + EK_rotasi = 1/2 Mv² + 1/2 Iω². Karena v = ωR dan I = 1/2 MR², maka EK_total = 1/2 M(ωR)² + 1/2 (1/2 MR²)ω² = 3/4 Mω²R².",
                            "rubrik": {
                                "3": "Menyebutkan rumus total EK, substitusi v = ωR, dan I, lalu menghitung dengan benar.",
                                "2": "Menyebutkan rumus EK total dan substitusi v dan I, tetapi salah perhitungan.",
                                "1": "Menyebutkan rumus EK translasi dan rotasi saja.",
                                "0": "Tidak menjawab atau jawaban salah."
                            }
                        }
                    ]
                }
            elif key == "simulasi_virtual":
                default_data = {
                    "judul": "Simulasi Virtual: Dinamika Rotasi",
                    "deskripsi": "Eksplorasi konsep Torsi, Momen Inersia, dan Momentum Sudut secara interaktif dengan simulasi PhET 'Rotation'!",
                    "petunjuk_penggunaan": """📘 **Petunjuk Umum Penggunaan Simulasi PhET: Rotation**
💡 Simulasi ini akan membantu Anda memahami konsep-konsep penting dalam dinamika rotasi.
**Ikuti langkah-langkah berikut:**
1.  **Buka Simulasi**: Klik tombol "Buka Simulasi" di bawah untuk membuka simulasi di tab baru.
2.  **Pilih Tab**:
    - **"Torque"**: Untuk mempelajari torsi dan hubungannya dengan percepatan sudut.
    - **"Moment of Inertia"**: Untuk mempelajari momen inersia dari berbagai benda.
    - **"Angular Momentum"**: Untuk mempelajari momentum sudut dan hukum kekekalan momentum sudut.
3.  **Eksplorasi Variabel**:
    - **Force**: Atur besar gaya yang diberikan.
    - **Brake Force**: Gunakan untuk menghentikan rotasi.
    - **Applied Force Location**: Ubah posisi aplikasi gaya.
    - **Mass of the ladybug**: Ubah massa untuk memengaruhi momen inersia.
4.  **Amati Perubahan**:
    - Torsi (τ), percepatan sudut (α), kecepatan sudut (ω), dan momentum sudut (L).
5.  **Jawab Pertanyaan**:
    - Apa hubungan antara torsi dan percepatan sudut?
    - Bagaimana pengaruh distribusi massa terhadap momen inersia?
    - Apakah momentum sudut tetap jika tidak ada torsi luar?
> 🎯 **Tujuan**: Memahami prinsip Hukum II Newton untuk Rotasi (τ = Iα), kekekalan momentum sudut (L = konstan jika τ = 0), dan faktor-faktor yang memengaruhi gerak rotasi.
""",
                    "simulasi_list": [
                        {
                            "judul": "🔄 Rotation: Torque, Moment of Inertia & Angular Momentum - PhET",
                            "url": "https://phet.colorado.edu/sims/cheerpj/rotation/latest/rotation.html?simulation=torque",
                            "sumber": "PhET Colorado",
                            "petunjuk": """### Petunjuk Simulasi: Rotation
**Tab 1: Torque**
- Eksplorasi hubungan τ = Iα.
- Ubah gaya dan lengan momen.
- Amati perubahan torsi dan percepatan sudut.

**Tab 2: Moment of Inertia**
- Pilih bentuk benda dan ubah massanya.
- Lihat bagaimana momen inersia berubah.
- Bandingkan momen inersia benda padat dan berongga.

**Tab 3: Angular Momentum**
- Aktifkan "Angular Momentum Vector".
- Ubah momen inersia (misalnya, dengan memindahkan massa).
- Amati apakah momentum sudut (L) tetap (jika tidak ada torsi luar).
- Eksplorasi hukum kekekalan momentum sudut.
"""
                        }
                    ],
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            elif key == "post_test":
                default_data = {
                    "judul": "Post-test: Dinamika Rotasi",
                    "deskripsi": "Uji pemahamanmu tentang Torsi, Momen Inersia, Momentum Sudut, dan Energi Kinetik Rotasi.",
                    "soal_list": [
                        {
                            "id": 1,
                            "soal": "Sebuah silinder pejal (I = ½MR²) dan sebuah silinder berongga tipis (I = MR²) dengan massa dan jari-jari yang sama dilepaskan dari keadaan diam di puncak bidang miring yang sama. Manakah pernyataan yang benar mengenai gerak keduanya?",
                            "pilihan": ["A. Silinder berongga tiba di dasar lebih dulu karena memiliki momen inersia lebih besar.", "B. Silinder pejal tiba di dasar lebih dulu karena memiliki momen inersia lebih kecil.", "C. Keduanya tiba di dasar secara bersamaan karena massa dan jari-jarinya sama.", "D. Silinder berongga memiliki kecepatan linear akhir yang lebih besar.", "E. Silinder pejal memiliki energi kinetik rotasi yang lebih besar di dasar."],
                            "kunci": "B",
                            "poin": 11, # C4
                            "tingkat": "C4"
                        },
                        {
                            "id": 2,
                            "soal": "Sebuah roda dengan momen inersia 0,4 kg·m² berputar dengan kecepatan sudut 10 rad/s. Untuk menghentikannya dalam waktu 2 detik, torsi konstan yang harus diberikan adalah...",
                            "pilihan": ["A. 0,5 Nm", "B. 1,0 Nm", "C. 2,0 Nm", "D. 4,0 Nm", "E. 8,0 Nm"],
                            "kunci": "C",
                            "poin": 11, # C4
                            "tingkat": "C4"
                        },
                        {
                            "id": 3,
                            "soal": "Sebuah roda sepeda berdiameter 0,8 m diberi gaya 25 N secara tegak lurus pada tepinya. Besar torsi yang dihasilkan terhadap porosnya adalah...",
                            "pilihan": ["A. 5 Nm", "B. 10 Nm", "C. 20 Nm", "D. 25 Nm", "E. 40 Nm"],
                            "kunci": "C",
                            "poin": 7, # C3
                            "tingkat": "C3"
                        },
                        {
                            "id": 4,
                            "soal": "Sebuah kipas angin memiliki momen inersia 0,8 kg·m² dan mengalami torsi sebesar 4 Nm. Percepatan sudut kipas tersebut adalah...",
                            "pilihan": ["A. 0,2 rad/s²", "B. 0,4 rad/s²", "C. 2,0 rad/s²", "D. 5,0 rad/s²", "E. 8,0 rad/s²"],
                            "kunci": "D",
                            "poin": 7, # C3
                            "tingkat": "C3"
                        },
                        {
                            "id": 5,
                            "soal": "Seorang penari balet sedang berputar dengan lengan terentang. Ketika ia menarik kedua lengannya ke dada, kecepatan putarannya meningkat. Fenomena ini dapat dijelaskan dengan prinsip...",
                            "pilihan": ["A. Hukum II Newton untuk Rotasi.", "B. Kekekalan Energi Mekanik.", "C. Kekekalan Momentum Sudut.", "D. Hukum Kekekalan Energi Kinetik.", "E. Hukum Kekekalan Momen Inersia."],
                            "kunci": "C",
                            "poin": 7, # C3
                            "tingkat": "C3"
                        },
                        {
                            "id": 6,
                            "soal": "Dua gaya bekerja pada sebuah batang yang dapat berputar di titik poros O. Gaya A = 30 N, diberikan pada jarak 0,5 m dari O dengan sudut 90°. Gaya B = 40 N, diberikan pada jarak 0,4 m dari O dengan sudut 30°. Manakah pernyataan yang benar?",
                            "pilihan": ["A. Torsi dari gaya A dan B sama besar.", "B. Torsi dari gaya B lebih besar karena gayanya lebih besar.", "C. Torsi dari gaya A lebih besar karena menghasilkan torsi maksimum.", "D. Torsi dari gaya B lebih besar karena lengan momennya lebih panjang.", "E. Tidak dapat dibandingkan karena arah gayanya berbeda."],
                            "kunci": "C",
                            "poin": 11, # C4
                            "tingkat": "C4"
                        },
                        {
                            "id": 7,
                            "soal": "Jika lengan gaya dari sebuah pintu dikurangi menjadi sepertiganya, bagaimana perubahan torsi yang dihasilkan jika gaya yang diberikan tetap?",
                            "pilihan": ["A. Torsi menjadi tiga kali lebih besar.", "B. Torsi menjadi sepertiga dari semula.", "C. Torsi tetap sama.", "D. Torsi menjadi sembilan kali lebih kecil.", "E. Torsi menjadi nol."],
                            "kunci": "B",
                            "poin": 11, # C4
                            "tingkat": "C4"
                        },
                        {
                            "id": 8,
                            "soal": "Sebuah benda memiliki momen inersia sebesar I dan berotasi dengan kecepatan sudut ω. Jika kecepatan sudutnya diubah menjadi 2ω, bagaimana perubahan energi kinetik rotasinya?",
                            "pilihan": ["A. Menjadi dua kali lipat.", "B. Menjadi empat kali lipat.", "C. Menjadi setengahnya.", "D. Tidak berubah.", "E. Menjadi seperempatnya."],
                            "kunci": "B",
                            "poin": 11, # C4
                            "tingkat": "C4"
                        },
                        {
                            "id": 9,
                            "soal": "Dua roda identik memiliki massa yang sama, tetapi roda A massanya terkonsentrasi di tepi, sedangkan roda B massanya terkonsentrasi di pusat. Jika keduanya diberi torsi yang sama, roda mana yang lebih cepat mencapai kecepatan sudut tertentu?",
                            "pilihan": ["A. Roda A, karena momen inersianya lebih besar.", "B. Roda B, karena momen inersianya lebih kecil.", "C. Keduanya sama, karena massanya sama.", "D. Roda A, karena lebih stabil.", "E. Tidak dapat ditentukan tanpa mengetahui jari-jarinya."],
                            "kunci": "B",
                            "poin": 11, # C4
                            "tingkat": "C4"
                        },
                        {
                            "id": 10,
                            "soal": "Sebuah benda dikenai torsi sebesar 6 Nm, dengan gaya 20 N yang bekerja pada jarak 0,6 m dari sumbu putar. Berapakah besar sudut θ antara arah gaya dan lengan momen?",
                            "pilihan": ["A. 0°", "B. 30°", "C. 45°", "D. 60°", "E. 90°"],
                            "kunci": "B",
                            "poin": 13, # C4 (untuk mencapai total 100)
                            "tingkat": "C4"
                        }
                    ],
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            elif key == "forum_diskusi":
                default_data = {"topik": []}
            # Data default untuk modul dari kode lama
            elif key == "video_info":
                default_data = {
                    "judul": "Video Apersepsi: Dinamika Rotasi",
                    "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, kamu diminta menonton video apersepsi berikut untuk memicu rasa ingin tahumu tentang fenomena rotasi di sekitar kita.",
                    "file_video": "",
                    "waktu_update": ""
                }
            elif key == "deskripsi_materi":
                default_data = {
                    "judul": "Deskripsi Materi: Dinamika Rotasi",
                    "capaian_pembelajaran": "Pada fase F, peserta didik mampu menerapkan konsep dan prinsip vektor ke dalam kinematika dan dinamika gerak rotasi, usaha dan energi dalam sistem rotasi, serta dinamika fluida dalam gerak berputar. Peserta didik mampu memahami konsep tentang gerak rotasi dengan kecepatan sudut konstan serta mampu mengamati dan mengidentifikasi benda di sekitar yang mengalami gerak tersebut. Kemudian, peserta didik mampu memperdalam pemahaman fisika sesuai dengan minat untuk melanjutkan ke perguruan tinggi yang berhubungan dengan bidang fisika. Melalui kerja ilmiah, juga dibangun sikap ilmiah dan Profil Pelajar Pancasila, khususnya mandiri, inovatif, bernalar kritis, kreatif, dan bergotong royong.",
                    "tujuan_pembelajaran": [
                        "Peserta didik mampu menjelaskan konsep dinamika rotasi melalui eksplorasi langsung pada aplikasi simulasi berbasis Streamlit.",
                        "Peserta didik mampu menerapkan prinsip dinamika rotasi untuk memecahkan masalah kontekstual melalui simulasi dan latihan interaktif di platform Streamlit.",
                        "Peserta didik mampu menganalisis hubungan antara momen gaya, momen inersia, dan percepatan sudut dengan mengubah nilai parameter dalam simulasi virtual berbasis Streamlit."
                    ],
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            elif key == "media_pembelajaran":
                default_data = {
                    "judul": "Media Pembelajaran: Dinamika Rotasi",
                    "deskripsi": "Berikut adalah media pembelajaran tambahan untuk memperdalam pemahaman Anda tentang Dinamika Rotasi.",
                    "pertemuan_1": {
                        "judul": "Pertemuan 1",
                        "bahan_ajar": "### DINAMIKA ROTASI\nDinamika rotasi adalah ilmu yang mempelajari gerak rotasi (berputar) dengan mempertimbangkan komponen penyebabnya, yaitu momen gaya. Momen gaya atau torsi ini, menyebabkan percepatan sudut. Jika semua bagian suatu benda bergerak mengelilingi poros atau sumbu putarnya dan sumbu putarnya terletak pada salah satu bagiannya, benda tersebut dikatakan melakukan gerak rotasi (berputar). Dalam kehidupan sehari-hari, gerak rotasi dapat diamati pada berbagai objek seperti roda kendaraan yang berputar, baling – baling, kipas angin, atau gerakan planet yang mengorbit matahari.",
                        "deskripsi": "Bahan ajar untuk Pertemuan 1",
                        "videos": [
                            {"judul": "Contoh Gerak Rotasi - Skater", "url": "https://www.youtube.com/embed/FmnkQ2ytlO8", "sumber": "YouTube"}
                        ],
                        "images": [
                            {"judul": "Perbedaan Gerak Translasi dan Rotasi", "url": "https://mafia.mafiaol.com/wp-content/uploads/2014/01/gerak-translasi-dan-rotasi.png", "sumber": "Mafia Fisika"},
                            {"judul": "Ilustrasi Torsi", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Torque_animation.gif/220px-Torque_animation.gif", "sumber": "Wikimedia Commons"}
                        ]
                    },
                    "pertemuan_2": {
                        "judul": "Pertemuan 2",
                        "bahan_ajar": "### GERAK TRANSLASI vs GERAK ROTASI\n**Gerak Translasi:**\n- Energi kinetik itu energi yang dimiliki benda-benda yang bergerak.\n- Translasi bisa diartikan linear atau lurus.\n- Gerak translasi dapat didefinisikan sebagai gerak pergeseran suatu benda dengan bentuk dan lintasan yang sama di setiap titiknya.\n- Jadi sebuah benda dapat dikatakan melakukan gerak translasi (pergeseran) apabila setiap titik pada benda itu menempuh lintasan yang bentuk dan panjangnya sama.\n**Gerak Rotasi:**\n- Gerak rotasi adalah gerak suatu benda yang berputar terhadap sumbu tertentu.\n- Setiap titik pada benda tersebut bergerak dalam lintasan lingkaran yang berpusat di sumbu putarnya.\n- Besaran penting dalam gerak rotasi adalah momen inersia, torsi, dan percepatan sudut.",
                        "deskripsi": "Bahan ajar untuk Pertemuan 2",
                        "videos": [
                            {"judul": "Penerapan Konsep Torsi - Kunci Inggris", "url": "https://www.youtube.com/embed/kSSFq1cgVoA", "sumber": "YouTube"},
                            {"judul": "Momen Inersia dalam Aksi", "url": "https://www.youtube.com/embed/R68BjRLfm1Q", "sumber": "YouTube Short"}
                        ],
                    },
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            elif key == "lkpd":
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
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            elif key == "refleksi":
                default_data = {
                    "judul": "Refleksi Pembelajaran: Dinamika Rotasi",
                    "deskripsi": "Halo, Sobat Fisika! Setelah menyelesaikan pembelajaran dan praktikum tentang Dinamika Rotasi, saatnya kamu merefleksikan pengalaman belajarmu. Jawablah pertanyaan-pertanyaan berikut dengan jujur dan terbuka untuk membantu guru memahami pemikiran dan perkembanganmu.",
                    "pertanyaan_list": [
                        {"id": "r1", "teks": "Bagaimana perasaan Anda setelah mempelajari materi pada pertemuan ini?"},
                        {"id": "r2", "teks": "Materi apa yang belum Anda pahami pada pembelajaran ini?"},
                        {"id": "r3", "teks": "Menurut Anda, materi apa yang paling menyenangkan pada pembelajaran ini?"},
                        {"id": "r4", "teks": "Apa yang akan Anda lakukan untuk mempelajari materi yang belum Anda mengerti?"},
                        {"id": "r5", "teks": "Apa yang akan Anda lakukan untuk meningkatkan hasil belajar Anda?"}
                    ],
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)

# Inisialisasi file notifikasi jika belum ada
if not os.path.exists(NOTIFIKASI_FILE):
    default_notif = {
        "Daftar Hadir": "",
        "Video Apersepsi": "",
        "Pre-test": "",
        "Deskripsi Materi": "",
        "Media Pembelajaran": "",
        "Simulasi Virtual": "",
        "LKPD": "",
        "Refleksi Siswa": "",
        "Post-test": "",
        "Forum Diskusi": "",
        "Hasil Penilaian": ""
    }
    with open(NOTIFIKASI_FILE, "w") as f:
        json.dump(default_notif, f)

# Session state untuk login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "current_email" not in st.session_state:
    st.session_state.current_email = ""
if "last_access" not in st.session_state:
    st.session_state.last_access = {}

# === FUNGSI LOGIN ===
def login():
    st.title("🔐 Login LMS Dinamika Rotasi")
    email = st.text_input("📧 Masukkan Email Anda:", key="email_login_input")

    if email:
        if email == "guru@dinamikarotasi.sch.id":
            password = st.text_input("🔑 Password Guru", type="password", key="pwd_guru_input")
            if st.button("Login sebagai Guru"):
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
            if st.button("Login sebagai Admin", key="login_admin_btn"):
                if password == "admin123":
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
            if st.button("Login sebagai Siswa", key="login_siswa_btn"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title()
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

def periksa_notifikasi(item_key):
    """Cek apakah ada notifikasi baru untuk item tertentu."""
    # Muat waktu update dari file
    with open(NOTIFIKASI_FILE, "r") as f:
        notif_data = json.load(f)
    waktu_update = notif_data.get(item_key)
    if not waktu_update:
        return False
    waktu_update_obj = datetime.strptime(waktu_update, "%Y-%m-%d %H:%M:%S")
    # Ambil waktu akses terakhir dari session state
    waktu_akses_terakhir = st.session_state.last_access.get(item_key)
    if not waktu_akses_terakhir:
        return True # Belum pernah diakses, tampilkan notifikasi
    waktu_akses_obj = datetime.strptime(waktu_akses_terakhir, "%Y-%m-%d %H:%M:%S")
    return waktu_update_obj > waktu_akses_obj

def reset_notifikasi(item_key):
    """Reset notifikasi setelah siswa membuka item."""
    st.session_state.last_access[item_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def update_notifikasi(item_key):
    """Fungsi helper untuk memperbarui waktu notifikasi."""
    with open(NOTIFIKASI_FILE, "r") as f:
        notif = json.load(f)
    notif[item_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTIFIKASI_FILE, "w") as f:
        json.dump(notif, f)

# === MODUL PRE-TEST (kode baru) ===
def pre_test():
    # --- KODE PRE-TEST BARU ---
    import streamlit as st
    import pandas as pd
    import json
    import os
    from datetime import datetime

    SOAL_FILE = FILES["pre_test_soal"]
    # Perbaikan: Jangan gunakan dirname dari FILES["hasil_nilai"] jika hanya nama file
    hasil_nilai_path = FILES["hasil_nilai"] # e.g., "hasil_nilai.csv"
    dir_nama = os.path.dirname(hasil_nilai_path)
    if dir_nama == "":
        dir_nama = "." # Gunakan direktori saat ini
    JAWABAN_FILE = os.path.join(dir_nama, "pre_test_jawaban.csv")
    os.makedirs(dir_nama, exist_ok=True) # Perbaikan: Buat direktori dari dir_nama, bukan dirname JAWABAN_FILE

    def muat_soal():
        if os.path.exists(SOAL_FILE):
            with open(SOAL_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return muat_data("pre_test_soal")

    def simpan_soal(data):
        simpan_data("pre_test_soal", data)

    def simpan_jawaban(email, judul, jawaban_dict, skor_total):
        df = pd.DataFrame([{
            "email": email,
            "judul": judul,
            "timestamp": datetime.now().isoformat(),
            "skor": skor_total,
            **{f"jawaban_{k}": v for k, v in jawaban_dict.items()}
        }])
        if os.path.exists(JAWABAN_FILE):
            df_existing = pd.read_csv(JAWABAN_FILE)
            df = pd.concat([df_existing, df], ignore_index=True)
        df.to_csv(JAWABAN_FILE, index=False)

    def sudah_mengerjakan(email, judul):
        if not os.path.exists(JAWABAN_FILE):
            return False
        df = pd.read_csv(JAWABAN_FILE)
        return not df[(df["email"] == email) & (df["judul"] == judul)].empty

    def get_nilai_siswa(email, judul):
        if not os.path.exists(JAWABAN_FILE):
            return None
        df = pd.read_csv(JAWABAN_FILE)
        row = df[(df["email"] == email) & (df["judul"] == judul)]
        if not row.empty:
            return row.iloc[0]["skor"]
        return None

    # --- Halaman Guru Pre-test ---
    def guru_page():
        st.header("🧑‍🏫 Dashboard Guru: Pre-test Fisika")
        data = muat_soal()

        tab1, tab2 = st.tabs(["Edit Soal", "Lihat Hasil Siswa"])

        # --- Tab 1: Edit Soal + Kunci Jawaban + Rubrik ---
        with tab1:
            st.subheader("📝 Edit Soal Pre-test")
            judul = st.text_input("Judul", data.get("judul", ""))
            deskripsi = st.text_area("Deskripsi", data.get("deskripsi", ""), height=100)

            soal_list = data.get("soal_list", [])
            updated_soal = []
            for i, soal in enumerate(soal_list):
                st.markdown(f"#### Soal {i+1}")
                teks = st.text_area(f"Teks Soal {i+1}", soal["teks"], key=f"teks_{i}")
                kunci = st.text_area(f"Kunci Jawaban", soal["kunci"], key=f"kunci_{i}")

                st.markdown("**Rubrik Penilaian**")
                rubrik = soal["rubrik"]
                rubrik_3 = st.text_input("Skor 3", rubrik.get("3", ""), key=f"r3_{i}")
                rubrik_2 = st.text_input("Skor 2", rubrik.get("2", ""), key=f"r2_{i}")
                rubrik_1 = st.text_input("Skor 1", rubrik.get("1", ""), key=f"r1_{i}")
                rubrik_0 = st.text_input("Skor 0", rubrik.get("0", ""), key=f"r0_{i}")

                updated_soal.append({
                    "id": soal["id"],
                    "teks": teks,
                    "kunci": kunci,
                    "rubrik": {"3": rubrik_3, "2": rubrik_2, "1": rubrik_1, "0": rubrik_0}
                })

            if st.button("💾 Simpan Perubahan"):
                data["judul"] = judul
                data["deskripsi"] = deskripsi
                data["soal_list"] = updated_soal
                simpan_soal(data)
                # Update notifikasi
                update_notifikasi("Pre-test")
                st.success("✅ Soal berhasil diperbarui!")

        # --- Tab 2: Lihat Hasil Siswa ---
        with tab2:
            st.subheader("📊 Hasil Pre-test Siswa")
            if os.path.exists(JAWABAN_FILE):
                df = pd.read_csv(JAWABAN_FILE)
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info("Belum ada siswa yang mengerjakan.")
            else:
                st.info("Belum ada data jawaban.")

    # --- Halaman Siswa Pre-test ---
    def siswa_page():
        st.header("⚙️ Pre-test: Dinamika Rotasi")
        data = muat_soal()

        judul = data.get("judul", "")
        deskripsi = data.get("deskripsi", "")

        st.subheader(judul)
        st.info(deskripsi)

        email = st.session_state.current_email

        # Cek apakah sudah mengerjakan
        if sudah_mengerjakan(email, judul):
            skor = get_nilai_siswa(email, judul)
            st.success(f"✅ Anda sudah mengerjakan pre-test ini.")
            st.metric("Nilai Anda", f"{skor}/15")
            if skor >= 12:
                st.balloons()
                st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
            elif skor >= 8:
                st.info("👍 Bagus! Anda cukup memahami konsepnya.")
            else:
                st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")
            return

        # Form jawaban
        soal_list = data.get("soal_list", [])
        jawaban_dict = {}
        with st.form("form_pretest_siswa"):
            for i, soal in enumerate(soal_list):
                st.markdown(f"#### {i+1}. {soal['teks']}")
                jawaban = st.text_area(f"Jawaban {i+1}", key=soal["id"], height=120)
                jawaban_dict[soal["id"]] = jawaban

            submitted = st.form_submit_button("✅ Kirim & Lihat Nilai")

            if submitted:
                if any(not v.strip() for v in jawaban_dict.values()):
                    st.error("⚠️ Mohon isi semua jawaban.")
                else:
                    # Skor sementara: 3 per soal (asumsi otomatis = skor maksimal untuk demo)
                    skor_total = 15  # 5 soal x 3

                    simpan_jawaban(email, judul, jawaban_dict, skor_total)
                    # Simpan ke hasil_nilai.csv juga
                    df_nilai = muat_data("hasil_nilai")
                    jawaban_json_str = json.dumps(jawaban_dict)
                    new_entry = pd.DataFrame([{
                        "email": email,
                        "nama": st.session_state.current_user,
                        "jenis_penilaian": "Pre-test",
                        "jawaban_json": jawaban_json_str,
                        "nilai": skor_total,
                        "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "role": "siswa"
                    }])
                    df_nilai = pd.concat([df_nilai, new_entry], ignore_index=True)
                    simpan_data("hasil_nilai", df_nilai)

                    st.success("✅ Jawaban dikirim!")
                    st.metric("Nilai Anda", f"{skor_total}/15")
                    if skor_total >= 12:
                        st.balloons()
                        st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
                    elif skor_total >= 8:
                        st.info("👍 Bagus! Anda cukup memahami konsepnya.")
                    else:
                        st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")

    # --- Main Pre-test ---
    if st.session_state.role == "guru":
        guru_page()
    else:
        siswa_page()

# === MODUL SIMULASI VIRTUAL (kode baru) ===
def simulasi_virtual():
    # --- KODE SIMULASI VIRTUAL BARU ---
    import streamlit as st
    import streamlit.components.v1 as components
    import json
    import os
    from datetime import datetime

    SIMULASI_FILE = FILES["simulasi_virtual"]

    def muat_simulasi():
        if os.path.exists(SIMULASI_FILE):
            with open(SIMULASI_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return muat_data("simulasi_virtual")

    def simpan_simulasi(data_baru):
        simpan_data("simulasi_virtual", data_baru)

    # --- Halaman Guru Simulasi ---
    def guru_page():
        st.header("🧪 Edit Simulasi Virtual")
        simulasi_data = muat_simulasi()
        if not simulasi_data:
            st.error("Simulasi virtual belum diatur.")
            st.stop()

        with st.form("form_edit_simulasi"):
            judul_baru = st.text_input("Judul Simulasi Virtual", value=simulasi_data.get("judul", ""))
            desc_baru = st.text_area("Deskripsi", value=simulasi_data.get("deskripsi", ""), height=100)
            petunjuk_baru = st.text_area("Petunjuk Umum (Markdown)", value=simulasi_data.get("petunjuk_penggunaan", ""), height=200)

            simulasi_list_baru = []
            for i, simulasi in enumerate(simulasi_data.get("simulasi_list", [])):
                st.markdown(f"---\n#### Simulasi Utama")
                judul_sim_baru = st.text_input(f"Judul Simulasi", value=simulasi.get("judul", ""), key=f"judul_{i}")
                url_sim_baru = st.text_input(f"URL Simulasi", value=simulasi.get("url", ""), key=f"url_{i}")
                # Perbaikan: Gunakan .get() untuk menghindari KeyError
                sumber_sim_baru = st.text_input(f"Sumber Simulasi", value=simulasi.get("sumber", ""), key=f"sumber_{i}")
                petunjuk_sim_baru = st.text_area(f"Petunjuk Khusus (Markdown)", value=simulasi.get("petunjuk", ""), height=300, key=f"petunjuk_{i}")

                simulasi_baru = {
                    "judul": judul_sim_baru,
                    "url": url_sim_baru,
                    "sumber": sumber_sim_baru,
                    "petunjuk": petunjuk_sim_baru
                }
                simulasi_list_baru.append(simulasi_baru)

            submitted = st.form_submit_button("💾 Simpan Simulasi Virtual")

        if submitted:
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "petunjuk_penggunaan": petunjuk_baru,
                "simulasi_list": simulasi_list_baru,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_simulasi(data_baru)
            # Update notifikasi
            update_notifikasi("Simulasi Virtual")
            st.success("✅ Simulasi virtual berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Simulasi Virtual untuk Siswa")
        st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
        st.info(simulasi_data.get("deskripsi", ""))
        st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))

        for i, sim in enumerate(simulasi_data.get("simulasi_list", []), 1):
            st.markdown(f"---\n#### {i}. {sim['judul']}")
            # Perbaikan: Gunakan .get() untuk menghindari KeyError
            st.caption(f"Sumber: {sim.get('sumber', 'Tidak disebutkan')}")
            st.markdown(sim.get("petunjuk", ""))
            # Coba embed simulasi
            try:
                components.iframe(sim["url"], height=600, scrolling=True)
            except Exception:
                st.warning(f"Simulasi tidak dapat dimuat langsung. [Klik di sini untuk membuka di tab baru]({sim['url']})")

    # --- Halaman Siswa Simulasi ---
    def siswa_page():
        st.header("🧪 Simulasi Virtual: Dinamika Rotasi")
        simulasi_data = muat_simulasi()
        if not simulasi_data:
            st.error("Simulasi virtual belum diatur oleh guru.")
            st.stop()

        st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
        st.info(simulasi_data.get("deskripsi", ""))
        st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))

        simulasi_list = simulasi_data.get("simulasi_list", [])
        if not simulasi_list:
            st.warning("📁 Belum ada simulasi yang diatur oleh guru.")
            return

        for i, simulasi in enumerate(simulasi_list):
            st.markdown(f"---\n#### {simulasi['judul']}")
            # Perbaikan: Gunakan .get() untuk menghindari KeyError
            st.caption(f"Sumber: {simulasi.get('sumber', 'Tidak disebutkan')}")
            st.markdown(simulasi.get("petunjuk", ""))
            # Coba embed simulasi
            try:
                components.iframe(simulasi["url"], height=600, scrolling=True)
            except Exception:
                st.error(f"Simulasi '{simulasi['judul']}' tidak dapat dimuat langsung di halaman ini.")
                st.link_button(f"🔗 Buka Simulasi", simulasi["url"])
                st.info("💡 **Catatan:** Simulasi akan terbuka di tab baru browser Anda.")

    # --- Main Simulasi ---
    if st.session_state.role == "guru":
        guru_page()
    else:
        siswa_page()

# === MODUL POST-TEST (kode baru) ===
def post_test():
    # --- KODE POST-TEST BARU ---
    import streamlit as st
    import json
    import os
    from datetime import datetime

    POST_TEST_FILE = FILES["post_test"]
    # Perbaikan: Jangan gunakan dirname dari FILES["hasil_nilai"] jika hanya nama file
    hasil_nilai_path = FILES["hasil_nilai"] # e.g., "hasil_nilai.csv"
    dir_nama = os.path.dirname(hasil_nilai_path)
    if dir_nama == "":
        dir_nama = "." # Gunakan direktori saat ini
    JAWABAN_FILE = os.path.join(dir_nama, "post_test_jawaban.csv")
    os.makedirs(dir_nama, exist_ok=True) # Perbaikan: Buat direktori dari dir_nama, bukan dirname JAWABAN_FILE

    def muat_post_test():
        if os.path.exists(POST_TEST_FILE):
            with open(POST_TEST_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return muat_data("post_test")

    def simpan_post_test(data_baru):
        simpan_data("post_test", data_baru)

    def simpan_jawaban_siswa(email, jawaban_dict, skor_total):
        import pandas as pd
        df = pd.DataFrame([{
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "skor": skor_total,
            **{f"jawaban_{k}": v for k, v in jawaban_dict.items()}
        }])
        if os.path.exists(JAWABAN_FILE):
            df_existing = pd.read_csv(JAWABAN_FILE)
            df = pd.concat([df_existing, df], ignore_index=True)
        df.to_csv(JAWABAN_FILE, index=False)

    def sudah_mengerjakan(email):
        if not os.path.exists(JAWABAN_FILE):
            return False
        import pandas as pd
        df = pd.read_csv(JAWABAN_FILE)
        return not df[df["email"] == email].empty

    def get_nilai_siswa(email):
        if not os.path.exists(JAWABAN_FILE):
            return None
        import pandas as pd
        df = pd.read_csv(JAWABAN_FILE)
        row = df[df["email"] == email]
        if not row.empty:
            return row.iloc[0]["skor"]
        return None

    # --- Halaman Guru Post-test ---
    def guru_page():
        st.header("📝 Edit Soal Post-test")
        data = muat_post_test()

        # Edit soal
        with st.form("form_edit_post_test"):
            judul_baru = st.text_input("Judul Post-test", value=data.get("judul", ""))
            desc_baru = st.text_area("Deskripsi", value=data.get("deskripsi", ""), height=100)

            soal_list_baru = []
            for i, soal in enumerate(data.get("soal_list", [])):
                st.markdown(f"---\n#### Soal {i+1} (Tingkat: {soal.get('tingkat', 'C?')})")
                soal_baru = st.text_area(f"Soal", value=soal.get("soal", ""), key=f"soal_{i}", height=150)
                pilihan_baru = []
                for j, p in enumerate(soal.get("pilihan", [])):
                    pilihan_baru.append(st.text_input(f"Pilihan {chr(65+j)}", value=p, key=f"pil_{i}_{j}"))
                kunci_baru = st.selectbox(f"Kunci Jawaban Soal {i+1}", options=["A", "B", "C", "D", "E"], index=["A", "B", "C", "D", "E"].index(soal.get("kunci", "A")), key=f"kunci_{i}")
                # Poin otomatis berdasarkan tingkat kesulitan, kecuali soal ke-10 (index 9) = 13
                poin_default = 7 if soal.get("tingkat") == "C3" else 11
                if i == 9: # Soal ke-10 (index 9) kita atur manual jadi 13
                    poin_default = 13
                poin_baru = st.number_input(f"Poin Soal {i+1}", value=soal.get("poin", poin_default), min_value=1, max_value=20, step=1, key=f"poin_{i}")
                # Filter hanya C3 & C4
                tingkat_baru = st.selectbox(f"Tingkat Kesulitan Soal {i+1}", 
                                           options=["C3", "C4"], 
                                           index=["C3", "C4"].index(soal.get("tingkat", "C3")), 
                                           key=f"tingkat_{i}")

                soal_baru_dict = {
                    "id": i+1,
                    "soal": soal_baru,
                    "pilihan": pilihan_baru,
                    "kunci": kunci_baru,
                    "poin": poin_baru,
                    "tingkat": tingkat_baru
                }
                soal_list_baru.append(soal_baru_dict)

            submitted = st.form_submit_button("💾 Simpan Soal Post-test")

        if submitted:
            total_poin_baru = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in soal_list_baru])
            if total_poin_baru != 100:
                st.error(f"⚠️ Total poin soal saat ini adalah {total_poin_baru}. Harap atur ulang agar totalnya menjadi 100.")
            else:
                data_baru = {
                    "judul": judul_baru,
                    "deskripsi": desc_baru,
                    "soal_list": soal_list_baru,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                simpan_post_test(data_baru)
                # Update notifikasi
                update_notifikasi("Post-test")
                st.success("✅ Soal post-test berhasil disimpan!")

        # Pratinjau soal untuk siswa (dengan kunci jawaban dan poin)
        st.divider()
        st.subheader("👁️ Pratinjau Soal untuk Siswa (dengan Kunci Jawaban)")
        total_poin = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in data.get("soal_list", [])])
        # Hitung jumlah C3 & C4
        c3_count = sum(1 for s in data.get("soal_list", []) if s.get("tingkat") == "C3")
        c4_count = sum(1 for s in data.get("soal_list", []) if s.get("tingkat") == "C4")
        st.info(f"**Jumlah Soal: {c3_count} C3, {c4_count} C4 | Total Poin Maksimal: {total_poin}**")
        for soal in data.get("soal_list", []):
            st.markdown(f"**({soal['poin']} poin - {soal['tingkat']}) {soal['soal']}**")
            for p in soal["pilihan"]:
                st.write(p)
            st.write(f"**Kunci Jawaban: {soal['kunci']}**")
            st.divider()

    # --- Halaman Siswa Post-test ---
    def siswa_page():
        st.header("📝 Post-test: Dinamika Rotasi")
        data = muat_post_test()

        st.subheader(data.get("judul", "Post-test"))
        st.info(data.get("deskripsi", "Uji pemahamanmu."))

        # Cek apakah sudah mengerjakan
        if sudah_mengerjakan(st.session_state.current_email):
            skor = get_nilai_siswa(st.session_state.current_email)
            st.success(f"✅ Anda sudah mengerjakan post-test ini.")
            total_poin = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in data.get("soal_list", [])])
            st.metric("Nilai Anda", f"{skor}/{total_poin}")
            if skor >= 80:  # >= 80
                st.balloons()
                st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
            elif skor >= 60:  # >= 60
                st.info("👍 Bagus! Anda cukup memahami konsepnya.")
            else:
                st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")
            return

        # Form jawaban
        jawaban_dict = {}
        soal_list = data.get("soal_list", [])
        total_poin = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in soal_list])

        with st.form("form_post_test_siswa"):
            for i, soal in enumerate(soal_list):
                poin_soal = soal.get("poin", 7 if soal.get("tingkat") == "C3" else 11)
                tingkat = soal.get("tingkat", "C?")
                st.markdown(f"**({poin_soal} poin - {tingkat}) {i+1}. {soal['soal']}**")
                for p in soal["pilihan"]:
                    st.write(p)
                # Siswa hanya memilih jawaban, tidak melihat kunci
                jawaban = st.radio(f"Pilihan untuk soal {i+1}", options=["A", "B", "C", "D", "E"], key=f"jawaban_{i}", index=None)
                jawaban_dict[i+1] = jawaban

            submitted = st.form_submit_button("✅ Kirim Jawaban")

        if submitted:
            if any(v is None for v in jawaban_dict.values()):
                st.error("⚠️ Mohon jawab semua soal.")
            else:
                # Hitung skor
                skor_total = 0
                for i, soal in enumerate(soal_list):
                    id_soal = i + 1
                    jawaban_user = jawaban_dict[id_soal]
                    if jawaban_user == soal.get("kunci"):
                        skor_total += soal.get("poin", 7 if soal.get("tingkat") == "C3" else 11)

                simpan_jawaban_siswa(st.session_state.current_email, jawaban_dict, skor_total)
                # Simpan ke hasil_nilai.csv juga
                df_nilai = muat_data("hasil_nilai")
                jawaban_json_str = json.dumps(jawaban_dict)
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "jenis_penilaian": "Post-test",
                    "jawaban_json": jawaban_json_str,
                    "nilai": skor_total,
                    "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df_nilai = pd.concat([df_nilai, new_entry], ignore_index=True)
                simpan_data("hasil_nilai", df_nilai)

                st.success("✅ Jawaban berhasil dikirim!")
                st.metric("Nilai Anda", f"{skor_total}/100")
                if skor_total >= 80:  # >= 80
                    st.balloons()
                    st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
                elif skor_total >= 60:  # >= 60
                    st.info("👍 Bagus! Anda cukup memahami konsepnya.")
                else:
                    st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")

    # --- Main Post-test ---
    if st.session_state.role == "guru":
        guru_page()
    else:
        siswa_page()

# === MODUL FORUM DISKUSI (kode baru) ===
def forum_diskusi():
    # --- KODE FORUM DISKUSI BARU ---
    import streamlit as st
    import json
    import os
    from datetime import datetime

    FORUM_FILE = FILES["forum_diskusi"]

    def muat_forum():
        if os.path.exists(FORUM_FILE):
            with open(FORUM_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            return muat_data("forum_diskusi")

    def simpan_forum(data_baru):
        simpan_data("forum_diskusi", data_baru)

    # --- Halaman Forum ---
    st.header("💬 Forum Diskusi: Dinamika Rotasi")
    forum_data = muat_forum()

    # --- Form untuk membuat topik baru ---
    st.subheader("📝 Buat Topik Baru")
    with st.form("form_topik_baru"):
        judul_topik = st.text_input("Judul Topik")
        isi_topik = st.text_area("Isi Diskusi")
        kirim_topik = st.form_submit_button("Kirim Topik")

        if kirim_topik:
            if judul_topik and isi_topik:
                topik_baru = {
                    "id": len(forum_data["topik"]),
                    "judul": judul_topik,
                    "isi": isi_topik,
                    "author": st.session_state.current_user,
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "komentar": []
                }
                forum_data["topik"].append(topik_baru)
                simpan_forum(forum_data)
                # Update notifikasi
                update_notifikasi("Forum Diskusi")
                st.success("✅ Topik berhasil dibuat!")
                st.rerun()
            else:
                st.error("❌ Judul dan isi topik harus diisi.")

    # --- Tampilkan daftar topik ---
    st.subheader("📋 Daftar Topik")
    if not forum_data["topik"]:
        st.info("Belum ada topik diskusi. Jadilah yang pertama untuk memulai!")
    else:
        for topik in forum_data["topik"]:
            st.markdown(f"### {topik['judul']}")
            st.caption(f"Oleh: {topik['author']} | {topik['waktu']}")
            st.write(topik['isi'])

            # --- Form komentar ---
            with st.expander("💬 Komentar", expanded=False):
                with st.form(f"form_komentar_{topik['id']}"):
                    isi_komentar = st.text_area(f"Tambahkan komentar untuk topik ini", key=f"isi_komen_{topik['id']}")
                    kirim_komentar = st.form_submit_button(f"Kirim Komentar")

                    if kirim_komentar:
                        if isi_komentar:
                            komentar_baru = {
                                "id": len(topik["komentar"]),
                                "isi": isi_komentar,
                                "author": st.session_state.current_user,
                                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "balasan": []
                            }
                            topik["komentar"].append(komentar_baru)
                            simpan_forum(forum_data)
                            st.success("✅ Komentar berhasil dikirim!")
                            st.rerun()
                        else:
                            st.error("❌ Komentar tidak boleh kosong.")

                # --- Tampilkan komentar ---
                for komentar in topik["komentar"]:
                    st.markdown(f"**{komentar['author']}** - {komentar['waktu']}")
                    st.write(komentar['isi'])

                    # --- Form balasan ---
                    with st.form(f"form_balasan_{topik['id']}_{komentar['id']}"):
                        isi_balasan = st.text_area(f"Balas komentar ini", key=f"isi_balas_{topik['id']}_{komentar['id']}")
                        kirim_balasan = st.form_submit_button(f"Kirim Balasan")

                        if kirim_balasan:
                            if isi_balasan:
                                balasan_baru = {
                                    "isi": isi_balasan,
                                    "author": st.session_state.current_user,
                                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                komentar["balasan"].append(balasan_baru)
                                simpan_forum(forum_data)
                                st.success("✅ Balasan berhasil dikirim!")
                                st.rerun()
                            else:
                                st.error("❌ Balasan tidak boleh kosong.")

                    # --- Tampilkan balasan ---
                    for balasan in komentar["balasan"]:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;└ **{balasan['author']}** - {balasan['waktu']}")
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;└ {balasan['isi']}")

            st.divider()

# === MAIN APP ===
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "role", "current_user", "current_email", "hadir", "last_access"]:
            st.session_state.pop(key, None)
        st.rerun()

    # Urutan menu
    menu_options = [
        "Daftar Hadir",
        "Video Apersepsi",
        "Pre-test",
        "Deskripsi Materi",
        "Media Pembelajaran",
        "Simulasi Virtual",
        "LKPD",
        "Refleksi Siswa",
        "Post-test",
        "Forum Diskusi",
        "Hasil Penilaian"
    ]

    # Tampilkan notifikasi di sidebar untuk siswa
    if st.session_state.role == "siswa":
        st.sidebar.divider()
        st.sidebar.subheader("🔔 Notifikasi")
        # Periksa notifikasi untuk item yang diminta
        # GANTI BARIS INI:
        # items_to_check = ["Pre-test", "Media Pembelajaran", "Simulasi Virtual", "LKPD", "Post-test"]
        # MENJADI INI:
        items_to_check = ["Pre-test", "Media Pembelajaran", "Simulasi Virtual", "LKPD", "Post-test", "Forum Diskusi", "Hasil Penilaian"]
        for menu_item in items_to_check:
            if periksa_notifikasi(menu_item):
                st.sidebar.warning(f"Ada pembaruan di **{menu_item}**!")

    # Menu navigasi berdasarkan role
    if st.session_state.role in ["guru", "admin"]:
        menu = st.sidebar.selectbox("Navigasi Guru/Admin", menu_options)
    else: # Siswa
        menu = st.sidebar.selectbox("Navigasi Siswa", menu_options)

    # Tampilkan halaman berdasarkan menu dan role
    if menu == "Daftar Hadir":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: DAFTAR HADIR ---
            st.header("📋 Daftar Hadir Siswa")
            df = muat_data("data_hadir")
            if df is not None and not df.empty:
                df_siswa = df[df["role"] == "siswa"]
                st.dataframe(df_siswa[["nama", "email", "status", "waktu"]].sort_values(by="waktu", ascending=False))
            else:
                st.info("Belum ada data kehadiran siswa.")
        else: # Siswa
            # --- DASBOR SISWA: DAFTAR HADIR ---
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

    elif menu == "Video Apersepsi":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: VIDEO APREPSI ---
            st.header("🎥 Upload & Kelola Video Apersepsi")
            video_data = muat_data("video_info")
            if not video_data:
                st.error("File video info rusak.")
                st.stop()
            with st.form("form_video_apresiasi"):
                judul_baru = st.text_input("Judul Video", value=video_data.get("judul", ""))
                desc_baru = st.text_area("Deskripsi Video", value=video_data.get("deskripsi", ""), height=150)
                vid = st.file_uploader("Upload video (MP4)", type=["mp4"])
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
                # Update notifikasi
                update_notifikasi("Video Apersepsi")
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

        else: # Siswa
            # --- DASBOR SISWA: VIDEO APREPSI ---
            st.header("🎥 Video Apersepsi")
            check_hadir()
            video_data = muat_data("video_info")
            if not video_data:
                st.error("Video apersepsi belum diatur oleh guru.")
                st.stop()
            st.write(f"**{video_data.get('judul', 'Video Apersepsi')}**")
            st.info(video_data.get("deskripsi", "")) # ✅ Deskripsi ditampilkan
            if video_data.get("file_video"):
                video_path = os.path.join(UPLOAD_FOLDER, video_data["file_video"])
                if os.path.exists(video_path):
                    st.video(video_path)
                else:
                    st.warning("📁 File video belum ditemukan.")
            else:
                st.info("📁 Video belum diupload oleh guru.")
            reset_notifikasi("Video Apersepsi")

    elif menu == "Pre-test":
        # Gunakan kode baru
        pre_test()

    elif menu == "Deskripsi Materi":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: DESKRIPSI MATERI ---
            st.header("📚 Edit Deskripsi Materi")
            deskripsi_data = muat_data("deskripsi_materi")
            if not deskripsi_data:
                st.error("Deskripsi materi belum diatur.")
                st.stop()
            with st.form("form_edit_deskripsi"):
                judul_baru = st.text_input("Judul Deskripsi Materi", value=deskripsi_data.get("judul", ""))
                cp_baru = st.text_area("Capaian Pembelajaran (Fase F)", value=deskripsi_data.get("capaian_pembelajaran", ""), height=200)
                tp_list = deskripsi_data.get("tujuan_pembelajaran", [])
                tp_text = "\n".join(tp_list)
                tp_baru = st.text_area("Tujuan Pembelajaran (pisahkan dengan baris baru)", value=tp_text, height=150)
                submitted = st.form_submit_button("💾 Simpan Deskripsi Materi")

            if submitted:
                tp_list_baru = [item.strip() for item in tp_baru.split("\n") if item.strip()]
                data_baru = {
                    "judul": judul_baru,
                    "capaian_pembelajaran": cp_baru,
                    "tujuan_pembelajaran": tp_list_baru
                }
                simpan_data("deskripsi_materi", data_baru)
                # Update notifikasi
                update_notifikasi("Deskripsi Materi")
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

        else: # Siswa
            # --- DASBOR SISWA: DESKRIPSI MATERI ---
            st.header("📚 Deskripsi Materi: Dinamika Rotasi")
            check_hadir()
            deskripsi_data = muat_data("deskripsi_materi")
            if not deskripsi_data:
                st.error("Deskripsi materi belum diatur oleh guru.")
                st.stop()
            st.write(f"**{deskripsi_data.get('judul', 'Deskripsi Materi')}**")
            st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
            st.write(deskripsi_data.get("capaian_pembelajaran", ""))
            st.markdown("### 📌 Tujuan Pembelajaran")
            for i, tp in enumerate(deskripsi_data.get("tujuan_pembelajaran", []), 1):
                st.write(f"{i}. {tp}")
            reset_notifikasi("Deskripsi Materi")

    elif menu == "Media Pembelajaran":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: MEDIA PEMBELAJARAN ---
            st.header("📚 Upload & Edit Media Pembelajaran")
            media_data = muat_data("media_pembelajaran")
            if not media_data:
                st.error("Media pembelajaran belum diatur.")
                st.stop()
            tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

            # --- Pertemuan 1 ---
            with tab1:
                st.subheader("📅 Upload & Edit Media Pembelajaran - Pertemuan 1")
                p1_data = media_data.get("pertemuan_1", {})
                # Judul dan Deskripsi
                judul_p1 = st.text_input("Judul Pertemuan 1", value=p1_data.get("judul", ""))
                desc_p1 = st.text_area("Deskripsi Bahan Ajar", value=p1_data.get("deskripsi", ""), height=100)
                # Bahan Ajar (ditulis langsung)
                bahan_ajar_p1 = st.text_area("📝 Bahan Ajar Pertemuan 1 (Ditulis Langsung)", value=p1_data.get("bahan_ajar", ""), height=300)
                # Upload video & gambar tambahan
                st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 1")
                new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p1")
                new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p1")
                if st.button("➕ Tambahkan Video/Gambar Pertemuan 1"):
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
                    # Update notifikasi
                    update_notifikasi("Media Pembelajaran")
                    st.rerun()

                # Tombol Simpan
                if st.button("💾 Simpan Media Pembelajaran Pertemuan 1"):
                    p1_data["judul"] = judul_p1
                    p1_data["deskripsi"] = desc_p1
                    p1_data["bahan_ajar"] = bahan_ajar_p1
                    media_data["pertemuan_1"] = p1_data
                    media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    simpan_data("media_pembelajaran", media_data)
                    # Update notifikasi
                    update_notifikasi("Media Pembelajaran")
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

            # --- Pertemuan 2 ---
            with tab2:
                st.subheader("📅 Upload & Edit Media Pembelajaran - Pertemuan 2")
                p2_data = media_data.get("pertemuan_2", {})
                # Judul dan Deskripsi
                judul_p2 = st.text_input("Judul Pertemuan 2", value=p2_data.get("judul", ""))
                desc_p2 = st.text_area("Deskripsi Bahan Ajar", value=p2_data.get("deskripsi", ""), height=100)
                # Bahan Ajar (ditulis langsung)
                bahan_ajar_p2 = st.text_area("📝 Bahan Ajar Pertemuan 2 (Ditulis Langsung)", value=p2_data.get("bahan_ajar", ""), height=300)
                # Upload video & gambar tambahan
                st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 2")
                new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p2")
                new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p2")
                if st.button("➕ Tambahkan Video/Gambar Pertemuan 2"):
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
                    # Update notifikasi
                    update_notifikasi("Media Pembelajaran")
                    st.rerun()

                # Tombol Simpan
                if st.button("💾 Simpan Media Pembelajaran Pertemuan 2"):
                    p2_data["judul"] = judul_p2
                    p2_data["deskripsi"] = desc_p2
                    p2_data["bahan_ajar"] = bahan_ajar_p2
                    media_data["pertemuan_2"] = p2_data
                    media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    simpan_data("media_pembelajaran", media_data)
                    # Update notifikasi
                    update_notifikasi("Media Pembelajaran")
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

        else: # Siswa
            # --- DASBOR SISWA: MEDIA PEMBELAJARAN ---
            st.header("📚 Media Pembelajaran: Dinamika Rotasi")
            check_hadir()
            media_data = muat_data("media_pembelajaran")
            if not media_data:
                st.error("Media pembelajaran belum diatur oleh guru.")
                st.stop()
            st.write(f"**{media_data.get('judul', 'Media Pembelajaran')}**")
            st.info(media_data.get("deskripsi", ""))
            tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

            # --- Pertemuan 1 ---
            with tab1:
                p1_data = media_data.get("pertemuan_1", {})
                st.write(f"**{p1_data.get('judul', 'Pertemuan 1')}**")
                st.info(p1_data.get("deskripsi", ""))
                # Tampilkan Bahan Ajar
                st.markdown("### 📚 Bahan Ajar")
                st.write(p1_data.get("bahan_ajar", ""))
                # Tampilkan video & gambar tambahan
                st.subheader("🎬 Video Tambahan")
                for i, video in enumerate(p1_data.get("videos", [])):
                    st.markdown(f"**{i+1}. {video['judul']}**")
                    st.video(video["url"])
                    st.caption(f"Sumber: {video['sumber']}")

            # --- Pertemuan 2 ---
            with tab2:
                p2_data = media_data.get("pertemuan_2", {})
                st.write(f"**{p2_data.get('judul', 'Pertemuan 2')}**")
                st.info(p2_data.get("deskripsi", ""))
                # Tampilkan Bahan Ajar
                st.markdown("### 📚 Bahan Ajar")
                st.write(p2_data.get("bahan_ajar", ""))
                # Tampilkan video & gambar tambahan
                st.subheader("🎬 Video Tambahan")
                for i, video in enumerate(p2_data.get("videos", [])):
                    st.markdown(f"**{i+1}. {video['judul']}**")
                    st.video(video["url"])
                    st.caption(f"Sumber: {video['sumber']}")

            reset_notifikasi("Media Pembelajaran")

    elif menu == "Simulasi Virtual":
        # Gunakan kode baru
        simulasi_virtual()

    elif menu == "LKPD":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: LKPD ---
            st.header("📄 Edit LKPD")
            lkpd_data = muat_data("lkpd")
            if not lkpd_data:
                st.error("LKPD belum diatur.")
                st.stop()
            with st.form("form_edit_lkpd"):
                judul_baru = st.text_input("Judul LKPD", value=lkpd_data.get("judul", ""))
                desc_baru = st.text_area("Deskripsi LKPD", value=lkpd_data.get("deskripsi", ""), height=100)
                st.subheader("🎯 Tujuan Pembelajaran")
                tujuan_list = lkpd_data.get("tujuan", [])
                tujuan_text = "\n".join(tujuan_list)
                tujuan_baru = st.text_area("Tujuan (pisahkan dengan baris baru)", value=tujuan_text, height=150)
                st.subheader("📚 Dasar Teori")
                teori_baru = st.text_area("Dasar Teori", value=lkpd_data.get("materi", ""), height=200)
                st.subheader("📋 Petunjuk Pengerjaan")
                petunjuk_list = lkpd_data.get("petunjuk", [])
                petunjuk_text = "\n".join(petunjuk_list)
                petunjuk_baru = st.text_area("Petunjuk (pisahkan dengan baris baru)", value=petunjuk_text, height=150)
                st.subheader("🛠️ Alat dan Bahan")
                alat_list = lkpd_data.get("alat_bahan", [])
                alat_text = "\n".join(alat_list)
                alat_baru = st.text_area("Alat dan Bahan (pisahkan dengan baris baru)", value=alat_text, height=150)
                st.subheader("👣 Langkah Kerja")
                langkah_list = lkpd_data.get("langkah_kerja", [])
                langkah_text = "\n".join(langkah_list)
                langkah_baru = st.text_area("Langkah Kerja (pisahkan dengan baris baru)", value=langkah_text, height=200)
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
                kesimpulan_baru = st.text_area("Petunjuk Kesimpulan", value=lkpd_data.get("kesimpulan_petunjuk", ""), height=100)
                submitted = st.form_submit_button("💾 Simpan Seluruh Perubahan LKPD")

            if submitted:
                data_baru = {
                    "judul": judul_baru,
                    "deskripsi": desc_baru,
                    "tujuan": [item.strip() for item in tujuan_baru.split("\n") if item.strip()],
                    "materi": teori_baru,
                    "petunjuk": [item.strip() for item in petunjuk_baru.split("\n") if item.strip()],
                    "alat_bahan": [item.strip() for item in alat_baru.split("\n") if item.strip()],
                    "langkah_kerja": [item.strip() for item in langkah_baru.split("\n") if item.strip()],
                    "tabel_header": header_baru_list,
                    "analisis_pertanyaan": analisis_baru_list,
                    "kesimpulan_petunjuk": kesimpulan_baru,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                simpan_data("lkpd", data_baru)
                # Update notifikasi
                update_notifikasi("LKPD")
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
            st.table([header_list] + [["", "", "", "", ""]] * 3)
            st.markdown("### 🧠 Pertanyaan Analisis Data dan Diskusi")
            for i, q in enumerate(lkpd_data.get("analisis_pertanyaan", []), 1):
                st.markdown(f"**{i}. {q}**")
            st.markdown("### 🎯 Kesimpulan")
            st.write(lkpd_data.get("kesimpulan_petunjuk", ""))

        else: # Siswa
            # --- DASBOR SISWA: LKPD ---
            st.header("📄 LKPD: Dinamika Rotasi")
            check_hadir()
            lkpd_data = muat_data("lkpd")
            if not lkpd_data:
                st.error("LKPD belum diatur oleh guru.")
                st.stop()
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
            reset_notifikasi("LKPD")

    elif menu == "Refleksi Siswa":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: REFLEKSI SISWA ---
            st.header("💭 Edit Refleksi Siswa")
            refleksi_data = muat_data("refleksi")
            if not refleksi_data:
                st.error("Refleksi belum diatur.")
                st.stop()
            with st.form("form_edit_refleksi"):
                judul_baru = st.text_input("Judul Refleksi", value=refleksi_data.get("judul", ""))
                desc_baru = st.text_area("Deskripsi Refleksi", value=refleksi_data.get("deskripsi", ""), height=150)
                st.subheader("📝 Pertanyaan Refleksi")
                pertanyaan_list = refleksi_data.get("pertanyaan_list", [])
                pertanyaan_baru_list = []
                for i, q in enumerate(pertanyaan_list):
                    q_baru = st.text_area(f"Pertanyaan {i+1}", value=q.get("teks", ""), key=f"refleksi_q_{i}")
                    pertanyaan_baru_list.append({"id": q.get("id", f"r{i+1}"), "teks": q_baru})
                submitted = st.form_submit_button("💾 Simpan Refleksi Siswa")

            if submitted:
                data_baru = {
                    "judul": judul_baru,
                    "deskripsi": desc_baru,
                    "pertanyaan_list": pertanyaan_baru_list
                }
                simpan_data("refleksi", data_baru)
                # Update notifikasi
                update_notifikasi("Refleksi Siswa")
                st.success("✅ Refleksi siswa berhasil diperbarui!")

            # Tampilkan pratinjau
            st.divider()
            st.subheader("👁️‍🗨️ Pratinjau Refleksi untuk Siswa")
            st.write(f"**{refleksi_data.get('judul', 'Refleksi Siswa')}**")
            st.info(refleksi_data.get("deskripsi", ""))
            for i, q in enumerate(refleksi_data.get("pertanyaan_list", []), 1):
                st.markdown(f"#### {i}. {q['teks']}")

        else: # Siswa
            # --- DASBOR SISWA: REFLEKSI SISWA ---
            st.header("💭 Refleksi Pembelajaran")
            check_hadir()
            refleksi_data = muat_data("refleksi")
            if not refleksi_data:
                st.error("Refleksi belum diatur oleh guru.")
                st.stop()
            st.write(f"**{refleksi_data.get('judul', 'Refleksi Siswa')}**")
            st.info(refleksi_data.get("deskripsi", ""))
            jawaban_refleksi = {}
            for i, q in enumerate(refleksi_data.get("pertanyaan_list", []), 1):
                st.markdown(f"#### {i}. {q['teks']}")
                jawaban = st.text_area("Jawaban Anda:", key=q["id"], height=100)
                jawaban_refleksi[q["id"]] = jawaban
            if st.button("✅ Kirim Refleksi"):
                if any(not v.strip() for v in jawaban_refleksi.values()):
                    st.error("⚠️ Mohon jawab semua pertanyaan.")
                else:
                    df = muat_data("hasil_nilai")
                    jawaban_json_str = json.dumps(jawaban_refleksi)
                    new_entry = pd.DataFrame([{
                        "email": st.session_state.current_email,
                        "nama": st.session_state.current_user,
                        "jenis_penilaian": "Refleksi",
                        "jawaban_json": jawaban_json_str,
                        "nilai": 0, # Refleksi tidak dinilai
                        "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "role": "siswa"
                    }])
                    df = pd.concat([df, new_entry], ignore_index=True)
                    simpan_data("hasil_nilai", df)
                    st.success("✅ Refleksi berhasil dikirim!")
            reset_notifikasi("Refleksi Siswa")

    elif menu == "Post-test":
        # Gunakan kode baru
        post_test()

    elif menu == "Forum Diskusi":
        # Gunakan kode baru
        forum_diskusi()

    elif menu == "Hasil Penilaian":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: HASIL PENILAIAN ---
            st.header("📊 Hasil Penilaian Siswa")
            df = muat_data("hasil_nilai")
            if df is not None and not df.empty:
                df_siswa = df[df["role"] == "siswa"]
                st.dataframe(df_siswa[["nama", "jenis_penilaian", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
            else:
                st.info("Belum ada data penilaian.")

        else: # Siswa
            # --- DASBOR SISWA: HASIL PENILAIAN ---
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
        reset_notifikasi("Hasil Penilaian")