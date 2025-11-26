# lms_dinamika_rotasi_gabungan_fix.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid
import base64

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="LMS Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
ADMIN_PASSWORD = "admin123"
GURU_PASSWORD = "guru123"
UPLOAD_FOLDER = "uploaded_media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File untuk menyimpan data
FILES = {
    "daftar_hadir": "data_hadir.csv",
    "video_apresiasi": "video_info.json",
    "pre_test": "pre_test_info.json",
    "deskripsi_materi": "deskripsi_materi.json",
    "media_pembelajaran": "media_info.json",
    "simulasi_virtual": "simulasi_virtual_info.json",
    "lkpd": "lkpd_info.json",
    "refleksi_siswa": "refleksi_info.json",
    "post_test": "post_test_info.json",
    "forum_diskusi": "forum_diskusi.csv",
    "hasil_penilaian": "hasil_nilai.csv"
}

# Inisialisasi file jika belum ada
for key, file_path in FILES.items():
    if not os.path.exists(file_path):
        if file_path.endswith(".csv"):
            if key == "daftar_hadir":
                pd.DataFrame(columns=["email", "nama", "status", "waktu", "role"]).to_csv(file_path, index=False)
            elif key == "forum_diskusi":
                pd.DataFrame(columns=["id", "parent_id", "email", "nama", "pesan", "waktu", "role"]).to_csv(file_path, index=False)
            elif key == "hasil_penilaian":
                pd.DataFrame(columns=["email", "nama", "jenis_penilaian", "nilai", "waktu_kerja", "role"]).to_csv(file_path, index=False)
        elif file_path.endswith(".json"):
            if key == "video_apresiasi":
                default_data = {
                    "judul": "Video Apersepsi: Dinamika Rotasi",
                    "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, kamu diminta menonton video apersepsi berikut untuk memicu rasa ingin tahumu tentang fenomena rotasi di sekitar kita.",
                    "file_video": "",
                    "waktu_update": ""
                }
            elif key == "pre_test":
                default_data = {
                    "judul": "Pre-test: Dinamika Rotasi",
                    "deskripsi": "Halo, Sobat Fisika ! Sebelum memulai pembelajaran hari ini, kamu diminta menjawab beberapa pertanyaan berikut berdasarkan pengalaman atau dugaanmu sendiri. Jawabanmu tidak dinilai, tetapi akan membantu guru memahami pemikiran awalmu. Jawablah dengan jujur dan sejujurnya — gunakan kata-katamu sendiri! Tidak ada jawaban salah ! Setelah menjawab, kamu akan menonton video apersepsi dan melakukan eksplorasi melalui simulasi interaktif untuk memperdalam pemahamanmu. Selamat bereksplorasi!",
                    "soal_list": [
                        {"id": "p1_q1", "teks": "Pernahkah kamu membuka pintu? Di bagian mana lebih mudah mendorongnya: dekat engsel atau di gagang pintu? Mengapa menurutmu?"},
                        {"id": "p1_q2", "teks": "Jika kamu menggunakan kunci inggris untuk membuka baut, apakah lebih mudah memegang ujungnya atau dekat baut? Jelaskan!"},
                        {"id": "p1_q3", "teks": "Bayangkan dua roda sepeda: satu polos, satu dipasangi beban di pinggirnya. Roda mana yang menurutmu lebih sulit diputar dari keadaan diam? Mengapa?"},
                        {"id": "p1_q4", "teks": "Menurutmu, apa yang membuat suatu benda “sulit” atau “mudah” berputar?"}
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
                default_data = {
                    "judul": "Media Pembelajaran: Dinamika Rotasi",
                    "deskripsi": "Berikut adalah media pembelajaran tambahan untuk memperdalam pemahaman Anda tentang Dinamika Rotasi.",
                    "pertemuan_1": {
                        "judul": "Pertemuan 1",
                        "file_bahan_ajar": "",
                        "deskripsi": "Bahan ajar untuk Pertemuan 1",
                        "videos": [],
                        "images": []
                    },
                    "pertemuan_2": {
                        "judul": "Pertemuan 2",
                        "file_bahan_ajar": "",
                        "deskripsi": "Bahan ajar untuk Pertemuan 2",
                        "videos": [],
                        "images": []
                    }
                }
            elif key == "simulasi_virtual":
                default_data = {
                    "judul": "Simulasi Virtual: Dinamika Rotasi",
                    "deskripsi": "Eksplorasi konsep Dinamika Rotasi secara interaktif!",
                    "simulasi_list": [
                        {"judul": "Simulasi Torsi", "url": "https://phet.colorado.edu/sims/html/rotation/latest/rotation_en.html"},
                        {"judul": "Simulasi Momen Inersia", "url": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_en.html"}
                    ]
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
                    "waktu_update": ""
                }
            elif key == "refleksi_siswa":
                default_data = {
                    "judul": "Refleksi Pembelajaran: Dinamika Rotasi",
                    "deskripsi": "Halo, Sobat Fisika! Setelah menyelesaikan pembelajaran dan praktikum tentang Dinamika Rotasi, saatnya kamu merefleksikan pengalaman belajarmu. Jawablah pertanyaan-pertanyaan berikut dengan jujur dan terbuka untuk membantu guru memahami pemikiran dan perkembanganmu.",
                    "pertanyaan_list": [
                        {"id": "r1", "teks": "Bagaimana perasaan Anda setelah mempelajari materi pada pertemuan ini?"},
                        {"id": "r2", "teks": "Materi apa yang belum Anda pahami pada pembelajaran ini?"},
                        {"id": "r3", "teks": "Menurut Anda, materi apa yang paling menyenangkan pada pembelajaran ini?"},
                        {"id": "r4", "teks": "Apa yang akan Anda lakukan untuk mempelajari materi yang belum Anda mengerti?"},
                        {"id": "r5", "teks": "Apa yang akan Anda lakukan untuk meningkatkan hasil belajar Anda?"}
                    ]
                }
            elif key == "post_test":
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

# === FUNGSI LOGIN ===
def login():
    st.title("🔐 Login LMS Dinamika Rotasi")
    email = st.text_input("📧 Masukkan Email Anda:")

    if email:
        if email == "guru@dinamikarotasi.sch.id":
            password = st.text_input("🔑 Password Guru", type="password")
            if st.button("Login sebagai Guru"):
                if password == "guru123":
                    st.session_state.role = "guru"
                    st.session_state.current_user = "Guru"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.session_state.hadir = True
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
        elif email == "admin@dinamikarotasi.sch.id":
            password = st.text_input("🔑 Password Admin", type="password")
            if st.button("Login sebagai Admin"):
                if password == "admin123":
                    st.session_state.role = "admin"
                    st.session_state.current_user = "Admin"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.session_state.hadir = True
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
        else:
            if st.button("Login sebagai Siswa"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title()
                st.session_state.current_email = email
                st.session_state.logged_in = True
                st.session_state.hadir = False
                st.rerun()

# === HALAMAN UTAMA BERDASARKAN ROLE ===
def main_page():
    st.sidebar.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "role", "current_user", "current_email", "hadir"]:
            st.session_state.pop(key, None)
        st.rerun()

    # Urutan menu sesuai permintaan
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
    
    menu = st.sidebar.selectbox("Navigasi", menu_options)

    # Tampilkan halaman berdasarkan menu
    if menu == "Daftar Hadir":
        halaman_daftar_hadir()
    elif menu == "Video Apersepsi":
        halaman_video_apresiasi()
    elif menu == "Pre-test":
        halaman_pre_test()
    elif menu == "Deskripsi Materi":
        halaman_deskripsi_materi()
    elif menu == "Media Pembelajaran":
        halaman_media_pembelajaran()
    elif menu == "Simulasi Virtual":
        halaman_simulasi_virtual()
    elif menu == "LKPD":
        halaman_lkpd()
    elif menu == "Refleksi Siswa":
        halaman_refleksi_siswa()
    elif menu == "Post-test":
        halaman_post_test()
    elif menu == "Forum Diskusi":
        halaman_forum_diskusi()
    elif menu == "Hasil Penilaian":
        halaman_hasil_penilaian()

# === HALAMAN: Daftar Hadir ===
def halaman_daftar_hadir():
    st.header("📝 Daftar Hadir")
    
    if st.session_state.role == "siswa":
        nama = st.text_input("Nama Lengkap", value=st.session_state.current_user)
        status = st.radio("Status Kehadiran", ["Hadir", "Tidak Hadir"])

        if st.button("✅ Simpan Kehadiran"):
            if not nama.strip():
                st.error("Nama tidak boleh kosong!")
            else:
                df = muat_data("daftar_hadir")
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": nama.strip(),
                    "status": status,
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                simpan_data("daftar_hadir", df)
                st.session_state.hadir = (status == "Hadir")
                st.success(f"✅ Terima kasih, **{nama}**! Status kehadiran Anda: **{status}**.")

    elif st.session_state.role in ["guru", "admin"]:
        st.subheader("📋 Daftar Kehadiran Siswa")
        df = muat_data("daftar_hadir")
        if df is not None and not df.empty:
            df_siswa = df[df["role"] == "siswa"]
            st.dataframe(df_siswa[["nama", "email", "status", "waktu"]].sort_values(by="waktu", ascending=False))
        else:
            st.info("Belum ada data kehadiran siswa.")

# === HALAMAN: Video Apersepsi ===
def halaman_video_apresiasi():
    st.header("🎥 Video Apersepsi")
    
    if st.session_state.role in ["guru", "admin"]:
        st.subheader("📤 Upload & Edit Video Apersepsi")
        video_data = muat_data("video_apresiasi")
        if not video_data:
            st.error("File video info rusak.")
            return

        with st.form("form_video_apresiasi"):
            judul_baru = st.text_input("Judul Video", value=video_data.get("judul", ""))
            desc_baru = st.text_area("Deskripsi Video", value=video_data.get("deskripsi", ""), height=150)
            vid = st.file_uploader("Upload video (MP4)", type=["mp4"])
            submitted = st.form_submit_button("💾 Simpan Video & Deskripsi")

        if submitted:
            if vid is not None:
                unique_filename = f"{uuid.uuid4().hex}_{vid.name}"
                video_path_simpan = os.path.join(UPLOAD_FOLDER, unique_filename)
                with open(video_path_simpan, "wb") as f:
                    f.write(vid.read())
                video_data["file_video"] = unique_filename
            video_data["judul"] = judul_baru
            video_data["deskripsi"] = desc_baru
            video_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simpan_data("video_apresiasi", video_data)
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

    elif st.session_state.role == "siswa":
        check_hadir()
        video_data = muat_data("video_apresiasi")
        if not video_data:
            st.error("Video apersepsi belum diatur oleh guru.")
            return

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

# === HALAMAN: Pre-test ===
def halaman_pre_test():
    st.header("🧠 Pre-test")
    check_hadir()
    
    pre_test_data = muat_data("pre_test")
    if not pre_test_data:
        st.error("Soal pre-test belum diatur oleh guru.")
        return

    st.write(f"**{pre_test_data.get('judul', 'Pre-test')}**")
    st.info(pre_test_data.get("deskripsi", ""))

    jawaban_dict = {}
    soal_list = pre_test_data.get("soal_list", [])

    with st.form("form_pre_test"):
        for i, soal in enumerate(soal_list):
            st.markdown(f"#### {i+1}. {soal['teks']}")
            jawaban = st.text_area("Jawaban Anda:", key=soal["id"], height=100)
            jawaban_dict[soal["id"]] = jawaban

        submitted = st.form_submit_button("✅ Kirim Jawaban Pre-test")

        if submitted:
            if any(not v.strip() for v in jawaban_dict.values()):
                st.error("⚠️ Mohon jawab semua pertanyaan.")
            else:
                df = muat_data("hasil_penilaian")
                jawaban_json_str = json.dumps(jawaban_dict)
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "jenis_penilaian": "Pre-test",
                    "jawaban_json": jawaban_json_str,
                    "nilai": 0,
                    "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                simpan_data("hasil_penilaian", df)
                st.success("✅ Jawaban pre-test berhasil dikirim!")

# === HALAMAN: Deskripsi Materi ===
def halaman_deskripsi_materi():
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

# === HALAMAN: Media Pembelajaran ===
def halaman_media_pembelajaran():
    st.header("📚 Media Pembelajaran")
    check_hadir()

    media_data = muat_data("media_pembelajaran")
    if not media_data:
        st.error("Media pembelajaran belum diatur oleh guru.")
        return

    st.write(f"**{media_data.get('judul', 'Media Pembelajaran')}**")
    st.info(media_data.get("deskripsi", ""))

    tab1, tab2 = st.tabs(["Pertemuan 1", "Pertemuan 2"])

    with tab1:
        p1_data = media_data.get("pertemuan_1", {})
        st.write(f"**{p1_data.get('judul', 'Pertemuan 1')}**")
        st.info(p1_data.get("deskripsi", ""))
        if p1_data.get("file_bahan_ajar"):
            pdf_path = os.path.join(UPLOAD_FOLDER, p1_data["file_bahan_ajar"])
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Unduh Bahan Ajar Pertemuan 1", f, p1_data["file_bahan_ajar"], "application/pdf")
            else:
                st.warning("📁 File PDF Pertemuan 1 tidak ditemukan.")
        else:
            st.info("📁 Bahan ajar belum diupload oleh guru.")

        # Tampilkan video & gambar
        st.subheader("🎬 Video Pertemuan 1")
        for i, url in enumerate(p1_data.get("videos", [])):
            st.markdown(f"{i+1}. {url}")
            st.video(url)
        st.subheader("🖼️ Gambar Pertemuan 1")
        for i, url in enumerate(p1_data.get("images", [])):
            st.markdown(f"{i+1}. {url}")
            st.image(url, caption=f"Gambar {i+1}", use_column_width=True)

    with tab2:
        p2_data = media_data.get("pertemuan_2", {})
        st.write(f"**{p2_data.get('judul', 'Pertemuan 2')}**")
        st.info(p2_data.get("deskripsi", ""))
        if p2_data.get("file_bahan_ajar"):
            pdf_path = os.path.join(UPLOAD_FOLDER, p2_data["file_bahan_ajar"])
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Unduh Bahan Ajar Pertemuan 2", f, p2_data["file_bahan_ajar"], "application/pdf")
            else:
                st.warning("📁 File PDF Pertemuan 2 tidak ditemukan.")
        else:
            st.info("📁 Bahan ajar belum diupload oleh guru.")

        # Tampilkan video & gambar
        st.subheader("🎬 Video Pertemuan 2")
        for i, url in enumerate(p2_data.get("videos", [])):
            st.markdown(f"{i+1}. {url}")
            st.video(url)
        st.subheader("🖼️ Gambar Pertemuan 2")
        for i, url in enumerate(p2_data.get("images", [])):
            st.markdown(f"{i+1}. {url}")
            st.image(url, caption=f"Gambar {i+1}", use_column_width=True)

    # --- MENU GURU: UPLOAD BAHAN AJAR & TAMBAH MEDIA ---
    if st.session_state.role in ["guru", "admin"]:
        st.divider()
        st.subheader("📤 Upload Bahan Ajar & Media Tambahan (Guru)")

        tab1_guru, tab2_guru = st.tabs(["Pertemuan 1", "Pertemuan 2"])

        with tab1_guru:
            st.write(f"**{media_data['pertemuan_1'].get('judul', 'Pertemuan 1')}**")
            desc_p1 = st.text_area("Deskripsi Bahan Ajar Pertemuan 1", value=media_data["pertemuan_1"].get("deskripsi", ""), height=100)
            pdf_p1 = st.file_uploader("Upload Bahan Ajar Pertemuan 1 (PDF)", type=["pdf"], key="pdf_p1")
            if pdf_p1 is not None:
                unique_filename = f"pert1_{uuid.uuid4().hex}_{pdf_p1.name}"
                pdf_path_simpan = os.path.join(UPLOAD_FOLDER, unique_filename)
                with open(pdf_path_simpan, "wb") as f:
                    f.write(pdf_p1.read())
                media_data["pertemuan_1"]["file_bahan_ajar"] = unique_filename
                st.success("✅ Bahan ajar Pertemuan 1 berhasil diupload!")
            if st.button("💾 Simpan Deskripsi Pertemuan 1"):
                media_data["pertemuan_1"]["deskripsi"] = desc_p1
                simpan_data("media_pembelajaran", media_data)
                st.success("✅ Deskripsi Bahan Ajar Pertemuan 1 berhasil disimpan!")

            # Upload video & gambar
            st.subheader("🖼️ Upload Video & Gambar Pertemuan 1")
            new_video_url = st.text_input("URL Video (YouTube embed)", key="new_video_p1")
            new_image_url = st.text_input("URL Gambar", key="new_image_p1")
            if st.button("➕ Tambah Video/Gambar Pertemuan 1"):
                if new_video_url:
                    media_data["pertemuan_1"]["videos"].append(new_video_url)
                    st.success("✅ Video berhasil ditambahkan!")
                if new_image_url:
                    media_data["pertemuan_1"]["images"].append(new_image_url)
                    st.success("✅ Gambar berhasil ditambahkan!")
                simpan_data("media_pembelajaran", media_data)
                st.rerun()

        with tab2_guru:
            st.write(f"**{media_data['pertemuan_2'].get('judul', 'Pertemuan 2')}**")
            desc_p2 = st.text_area("Deskripsi Bahan Ajar Pertemuan 2", value=media_data["pertemuan_2"].get("deskripsi", ""), height=100)
            pdf_p2 = st.file_uploader("Upload Bahan Ajar Pertemuan 2 (PDF)", type=["pdf"], key="pdf_p2")
            if pdf_p2 is not None:
                unique_filename = f"pert2_{uuid.uuid4().hex}_{pdf_p2.name}"
                pdf_path_simpan = os.path.join(UPLOAD_FOLDER, unique_filename)
                with open(pdf_path_simpan, "wb") as f:
                    f.write(pdf_p2.read())
                media_data["pertemuan_2"]["file_bahan_ajar"] = unique_filename
                st.success("✅ Bahan ajar Pertemuan 2 berhasil diupload!")
            if st.button("💾 Simpan Deskripsi Pertemuan 2"):
                media_data["pertemuan_2"]["deskripsi"] = desc_p2
                simpan_data("media_pembelajaran", media_data)
                st.success("✅ Deskripsi Bahan Ajar Pertemuan 2 berhasil disimpan!")

            # Upload video & gambar
            st.subheader("🖼️ Upload Video & Gambar Pertemuan 2")
            new_video_url = st.text_input("URL Video (YouTube embed)", key="new_video_p2")
            new_image_url = st.text_input("URL Gambar", key="new_image_p2")
            if st.button("➕ Tambah Video/Gambar Pertemuan 2"):
                if new_video_url:
                    media_data["pertemuan_2"]["videos"].append(new_video_url)
                    st.success("✅ Video berhasil ditambahkan!")
                if new_image_url:
                    media_data["pertemuan_2"]["images"].append(new_image_url)
                    st.success("✅ Gambar berhasil ditambahkan!")
                simpan_data("media_pembelajaran", media_data)
                st.rerun()

# === HALAMAN: Simulasi Virtual ===
def halaman_simulasi_virtual():
    st.header("🧪 Simulasi Virtual")
    check_hadir()

    simulasi_data = muat_data("simulasi_virtual")
    if not simulasi_data:
        st.error("Simulasi virtual belum diatur oleh guru.")
        return

    st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
    st.info(simulasi_data.get("deskripsi", ""))
    for i, sim in enumerate(simulasi_data.get("simulasi_list", []), 1):
        st.markdown(f"#### {i}. {sim['judul']}")
        st.components.v1.iframe(sim["url"], height=600, scrolling=True)

# === HALAMAN: LKPD ===
def halaman_lkpd():
    st.header("📄 LKPD: Dinamika Rotasi")
    check_hadir()

    lkpd_data = muat_data("lkpd")
    if not lkpd_data:
        st.error("LKPD belum diatur oleh guru.")
        return

    st.write(f"**{lkpd_data.get('judul', 'LKPD')}**")
    st.info(lkpd_data.get("deskripsi", ""))

    # Tampilkan Tujuan, Materi, Petunjuk, Alat&Bahan, Langkah Kerja
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

    # Tabel Hasil Pengamatan
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

    # Pertanyaan Analisis Data dan Diskusi
    st.markdown("### 🧠 Pertanyaan Analisis Data dan Diskusi")
    jawaban_analisis = {}
    for i, q in enumerate(lkpd_data.get("analisis_pertanyaan", []), 1):
        st.markdown(f"**{i}. {q}**")
        jawaban = st.text_area("Jawaban Anda:", key=f"analisis_q{i}", height=100)
        jawaban_analisis[f"analisis_q{i}"] = jawaban

    # Kesimpulan
    st.markdown("### 🎯 Kesimpulan")
    kesimpulan = st.text_area(lkpd_data.get("kesimpulan_petunjuk", "Tulis kesimpulan kelompok Anda:"), height=150)

    # Tombol Simpan
    if st.button("✅ Simpan Jawaban LKPD"):
        if any(not v.strip() for v in jawaban_analisis.values()) or not kesimpulan.strip():
            st.error("⚠️ Mohon jawab semua pertanyaan dan isi kesimpulan!")
        else:
            df = muat_data("hasil_penilaian")
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
            simpan_data("hasil_penilaian", df)
            st.success("✅ Jawaban LKPD berhasil disimpan!")

# === HALAMAN: Refleksi Siswa ===
def halaman_refleksi_siswa():
    st.header("💭 Refleksi Pembelajaran")
    check_hadir()

    refleksi_data = muat_data("refleksi_siswa")
    if not refleksi_data:
        st.error("Refleksi belum diatur oleh guru.")
        return

    st.write(f"**{refleksi_data.get('judul', 'Refleksi Siswa')}**")
    st.info(refleksi_data.get("deskripsi", ""))

    jawaban_refleksi = {}
    pertanyaan_list = refleksi_data.get("pertanyaan_list", [])
    for i, q in enumerate(pertanyaan_list):
        st.markdown(f"#### {i+1}. {q['teks']}")
        jawaban = st.text_area("Jawaban Anda:", key=q["id"], height=100)
        jawaban_refleksi[q["id"]] = jawaban

    if st.button("✅ Kirim Refleksi"):
        if any(not v.strip() for v in jawaban_refleksi.values()):
            st.error("⚠️ Mohon jawab semua pertanyaan.")
        else:
            df = muat_data("hasil_penilaian")
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
            simpan_data("hasil_penilaian", df)
            st.success("✅ Refleksi berhasil dikirim!")

# === HALAMAN: Post-test ===
def halaman_post_test():
    st.header("📝 Post-test: Dinamika Rotasi")
    check_hadir()

    post_test_data = muat_data("post_test")
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
            nilai_total = 0
            for soal in soal_list:
                if jawaban_dict.get(soal["id"]) == soal["kunci"]:
                    nilai_total += soal["skor"]
            
            df = muat_data("hasil_penilaian")
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
            simpan_data("hasil_penilaian", df)
            
            st.success("✅ Jawaban post-test berhasil dikirim!")
            st.subheader("📊 Hasil Penilaian Anda")
            total_skor = sum(soal["skor"] for soal in soal_list)
            st.metric("Nilai Total", f"{nilai_total}/{total_skor}")
            
            persentase = (nilai_total / total_skor) * 100 if total_skor > 0 else 0
            if persentase >= 75:
                st.balloons()
                st.success("🎉 Luar biasa! Pemahaman Anda sangat baik. Pertahankan semangat belajar!")
            elif persentase >= 60:
                st.info("👍 Bagus! Pemahaman Anda sudah cukup. Tingkatkan lagi untuk hasil yang lebih maksimal!")
            else:
                st.warning("📚 Hasil belajar Anda perlu ditingkatkan. Pelajari kembali materinya dan jangan ragu bertanya!")

# === HALAMAN: Forum Diskusi ===
def halaman_forum_diskusi():
    st.header("💬 Forum Diskusi")
    check_hadir()

    with st.form("form_diskusi"):
        pesan = st.text_area("Tulis pesan Anda:", max_chars=300)
        kirim = st.form_submit_button("📤 Kirim")

    if kirim and pesan.strip():
        df = muat_data(FORUM_FILE)
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
        simpan_data(FORUM_FILE, df)
        st.success("✅ Pesan berhasil dikirim!")
        st.rerun()

    # Tampilkan riwayat diskusi
    st.divider()
    st.subheader("📜 Riwayat Diskusi")
    df = muat_data(FORUM_FILE)
    if df is not None and not df.empty:
        df_siswa = df[df["role"] == "siswa"]
        for _, row in df_siswa.sort_values(by="id", ascending=False).iterrows():
            st.markdown(f"**{row['nama']}** ({row['email']}) • _{row['waktu']}_")
            st.write(row["pesan"])
            st.divider()
    else:
        st.info("Belum ada diskusi. Jadilah yang pertama mengirim pesan!")

# === HALAMAN: Hasil Penilaian ===
def halaman_hasil_penilaian():
    st.header("📊 Hasil Penilaian Anda")
    check_hadir()

    df = muat_data("hasil_penilaian")
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

    # Tampilkan halaman berdasarkan role dan menu
    if st.session_state.role == "guru":
        dashboard_guru()
    elif st.session_state.role == "admin":
        dashboard_admin() # Admin bisa melihat halaman guru
    elif st.session_state.role == "siswa":
        main_page()