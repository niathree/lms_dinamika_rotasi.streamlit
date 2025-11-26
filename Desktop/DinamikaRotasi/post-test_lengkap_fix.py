# post_test_dua_pertemuan_lengkap.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid

# === KONFIGURASI ===
st.set_page_config(page_title="Post-test Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
POST_TEST_INFO_FILE = "post_test_info_dua_pertemuan.json" # File untuk menyimpan soal dan kunci jawaban
POST_TEST_JAWABAN_FILE = "post_test_jawaban_siswa_dua_pertemuan.csv" # File untuk menyimpan jawaban & nilai siswa
UPLOAD_FOLDER = "uploaded_media_post_test"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inisialisasi file soal post-test jika belum ada
# Data diambil dari MODUL AJAR DAN BAHAN AJAR DINAMIKA ROTASI.pdf dan file terkait
if not os.path.exists(POST_TEST_INFO_FILE):
    # Struktur soal untuk Pertemuan 1 dan Pertemuan 2
    default_soal = {
        "pertemuan_1": {
            "judul": "Post-test: Dinamika Rotasi - Pertemuan 1",
            "deskripsi": "Uji pemahamanmu setelah mempelajari konsep dasar Dinamika Rotasi, seperti torsi dan momen inersia.",
            "soal_list": [
                {
                    "id": "p1_q1",
                    "teks": "(C2) Perbedaan utama antara gerak translasi dan rotasi adalah...",
                    "gambar": "",
                    "opsi": ["A. Gerak translasi lebih cepat daripada rotasi", "B. Gerak translasi tidak melibatkan poros", "C. Gerak rotasi hanya terjadi pada benda bulat", "D. Gerak rotasi tidak memiliki percepatan", "E. Gerak translasi tidak melibatkan gaya"],
                    "kunci": "B",
                    "skor": 2
                },
                {
                    "id": "p1_q2",
                    "teks": "(C2) Apa yang dimaksud dengan torsi?",
                    "gambar": "",
                    "opsi": ["A. Gaya yang bekerja pada benda diam", "B. Momen inersia yang menyebabkan percepatan", "C. Momen gaya yang menyebabkan rotasi", "D. Energi yang tersimpan dalam benda berputar", "E. Percepatan sudut benda"],
                    "kunci": "C",
                    "skor": 2
                },
                {
                    "id": "p1_q3",
                    "teks": "(C3) Sebuah roda sepeda berdiameter 0,5 m diberi gaya 10 N pada tepinya. Hitung torsi yang dihasilkan!",
                    "gambar": "",
                    "opsi": ["A. 2,5 Nm", "B. 5 Nm", "C. 10 Nm", "D. 15 Nm", "E. 20 Nm"],
                    "kunci": "A",
                    "skor": 7
                },
                {
                    "id": "p1_q4",
                    "teks": "(C3) Sebuah kipas angin memiliki momen inersia 0,5 kg·m². Jika torsi yang diberikan 10 Nm, hitung percepatan sudutnya!",
                    "gambar": "",
                    "opsi": ["A. 5 rad/s²", "B. 10 rad/s²", "C. 15 rad/s²", "D. 20 rad/s²", "E. 25 rad/s²"],
                    "kunci": "D",
                    "skor": 7
                },
                {
                    "id": "p1_q5",
                    "teks": "(C3) Seorang skater menarik tangannya ke dalam saat berputar. Fenomena ini menjelaskan prinsip...",
                    "gambar": "https://i.ibb.co/8XzRvZP/skater.png", # Gambar dari unggahan Anda
                    "opsi": ["A. Hukum II Newton untuk Rotasi", "B. Hukum Kekekalan Energi", "C. Hukum Kekekalan Momentum Sudut", "D. Hukum Gravitasi", "E. Hukum Pascal"],
                    "kunci": "C",
                    "skor": 7
                }
            ],
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "pertemuan_2": {
            "judul": "Post-test: Dinamika Rotasi - Pertemuan 2",
            "deskripsi": "Uji pemahamanmu setelah mempelajiki konsep lanjutan Dinamika Rotasi, seperti momentum sudut dan hukum kekekalan momentum sudut.",
            "soal_list": [
                {
                    "id": "p2_q1",
                    "teks": "(C4) Jika jarak dorong pintu dikurangi setengah, bagaimana perubahan torsinya?",
                    "gambar": "https://i.ibb.co/3YxVrJf/pintu.png", # Gambar dari unggahan Anda
                    "opsi": ["A. Torsi menjadi setengah dari semula", "B. Torsi menjadi dua kali lebih besar", "C. Torsi tetap sama", "D. Torsi meningkat 4 kali", "E. Tidak bisa ditentukan karena tidak ada informasi arah gaya"],
                    "kunci": "A",
                    "skor": 15
                },
                {
                    "id": "p2_q2",
                    "teks": "(C4) Penari balet menarik tangan ke badan → kecepatan sudut...",
                    "gambar": "",
                    "opsi": ["A. Kecepatan sudut meningkat karena energi kinetik bertambah", "B. Kecepatan sudut meningkat karena momentum sudut kekal", "C. Kecepatan sudut menurun karena momen inersia berkurang", "D. Kecepatan sudut tetap sama meskipun momen inersia berubah", "E. Kecepatan sudut meningkat karena massa penari bertambah"],
                    "kunci": "B",
                    "skor": 15
                },
                {
                    "id": "p2_q3",
                    "teks": "(C4) Siapa menghasilkan torsi lebih besar: A (30N, 0,5m, 90°) atau B (40N, 0,4m, 30°)?",
                    "gambar": "",
                    "opsi": ["A. Orang A, karena gaya lebih tegak lurus", "B. Orang B, karena gaya lebih besar", "C. Torsinya sama karena gaya dan jarak saling mengimbangi", "D. Orang A, karena menghasilkan torsi maksimum", "E. Tidak bisa ditentukan tanpa mengetahui massa batang"],
                    "kunci": "D",
                    "skor": 15
                },
                {
                    "id": "p2_q4",
                    "teks": "(C4) Torsi di titik A (r=0,8m) vs B (r=0,4m) dengan gaya sama?",
                    "gambar": "",
                    "opsi": ["A. Torsi di titik A lebih kecil karena lengan gayanya lebih panjang", "B. Torsi di titik B lebih besar karena lengan gayanya lebih pendek", "C. Torsi di titik A dua kali lebih besar daripada di titik B", "D. Torsi di titik A dan B sama besar karena gayanya sama", "E. Torsi tidak dapat dibandingkan karena tergantung massa pintu"],
                    "kunci": "C",
                    "skor": 15
                },
                {
                    "id": "p2_q5",
                    "teks": "(C4) Jika τ=6 Nm, F=20N, r=0,6m, maka sudut θ = ?",
                    "gambar": "",
                    "opsi": ["A. Sudutnya adalah 30° karena sin θ = 0,5", "B. Sudutnya adalah 60° karena sin θ = √3/2", "C. Sudutnya adalah 90° karena sin θ = 1", "D. Sudutnya adalah 45° karena sin θ = √2/2", "E. Tidak dapat ditentukan karena tidak ada informasi arah gaya"],
                    "kunci": "A",
                    "skor": 15
                }
            ],
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    with open(POST_TEST_INFO_FILE, "w") as f:
        json.dump(default_soal, f)

# Inisialisasi file data jawaban siswa jika belum ada
if not os.path.exists(POST_TEST_JAWABAN_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "pertemuan", "jawaban_json", "nilai_total", "waktu_kerja", "role"
    ]).to_csv(POST_TEST_JAWABAN_FILE, index=False)

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
    st.title("🔐 Login Post-test")
    email = st.text_input("Masukkan Email Anda:")

    if email:
        if email == "guru@dinamikarotasi.sch.id": # Ganti dengan email guru Anda
            password = st.text_input("Password Guru", type="password")
            if st.button("Login sebagai Guru"):
                if password == "guru123": # Ganti dengan password guru Anda
                    st.session_state.role = "guru"
                    st.session_state.current_user = "Guru"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Password salah!")
        elif email == "admin@dinamikarotasi.sch.id": # Ganti dengan email admin Anda
            password = st.text_input("Password Admin", type="password")
            if st.button("Login sebagai Admin"):
                if password == "admin123": # Ganti dengan password admin Anda
                    st.session_state.role = "admin"
                    st.session_state.current_user = "Admin"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Password salah!")
        else:
            # Asumsikan sebagai siswa
            if st.button("Login sebagai Siswa"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title() # Ambil nama dari email
                st.session_state.current_email = email
                st.session_state.logged_in = True
                st.rerun()

# === FUNGSI PEMBANTU ===
def muat_soal():
    """Muat soal post-test dari file JSON."""
    if os.path.exists(POST_TEST_INFO_FILE):
        with open(POST_TEST_INFO_FILE, "r") as f:
            return json.load(f)
    return None

def simpan_soal(data):
    """Simpan soal post-test ke file JSON."""
    with open(POST_TEST_INFO_FILE, "w") as f:
        json.dump(data, f, indent=4)

def muat_jawaban():
    """Muat jawaban siswa dari file CSV."""
    if os.path.exists(POST_TEST_JAWABAN_FILE):
        return pd.read_csv(POST_TEST_JAWABAN_FILE)
    return pd.DataFrame(columns=["email", "nama", "pertemuan", "jawaban_json", "nilai_total", "waktu_kerja", "role"])

def simpan_jawaban_baru(pertemuan, jawaban_dict, nilai):
    """Simpan jawaban baru siswa ke file CSV."""
    df = muat_jawaban()
    jawaban_json_str = json.dumps(jawaban_dict)
    new_entry = pd.DataFrame([{
        "email": st.session_state.current_email,
        "nama": st.session_state.current_user,
        "pertemuan": pertemuan,
        "jawaban_json": jawaban_json_str,
        "nilai_total": nilai,
        "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": "siswa"
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(POST_TEST_JAWABAN_FILE, index=False)

# === HALAMAN GURU: LIHAT & KELOLA SOAL POST-TEST ===
def guru_page():
    st.title("👩‍🏫 Dasbor Guru: Post-test Dinamika Rotasi")
    
    # Muat data soal
    data_soal = muat_soal()
    if not data_soal:
        st.error("File soal tidak ditemukan atau rusak.")
        return

    # Tab untuk Lihat Soal dan Lihat Hasil
    tab_soal, tab_hasil = st.tabs(["📝 Lihat Soal Post-test", "📂 Lihat Hasil Siswa"])

    # --- TAB 1: LIHAT SOAL POST-TEST (Termasuk Kunci & Skor) ---
    with tab_soal:
        st.header("📝 Lihat Soal Post-test (Lengkap dengan Kunci Jawaban & Skor)")

        # Pertemuan 1
        st.subheader("📅 Pertemuan 1")
        p1_data = data_soal.get("pertemuan_1", {})
        st.write(f"**Judul:** {p1_data.get('judul', 'Belum diatur')}")
        st.info(p1_data.get("deskripsi", ""))
        
        total_skor_p1 = sum(soal.get("skor", 0) for soal in p1_data.get("soal_list", []))
        st.metric("🏆 Total Skor Maksimal", total_skor_p1)

        for i, soal in enumerate(p1_data.get("soal_list", [])):
            st.markdown(f"#### Soal {i+1}: {soal['teks']}")
            if soal.get("gambar"):
                if soal["gambar"].startswith("http"):
                    st.image(soal["gambar"], width=300)
                elif os.path.exists(os.path.join(UPLOAD_FOLDER, soal["gambar"])):
                    st.image(os.path.join(UPLOAD_FOLDER, soal["gambar"]), width=300)
                else:
                    st.caption("*(Gambar tidak ditemukan)*")
            
            for opsi in soal.get("opsi", []):
                st.write(opsi)
            
            st.write(f"**Kunci Jawaban (Guru):** {soal['kunci']}")
            st.write(f"**Skor:** {soal['skor']}")
            st.divider()

        # Pertemuan 2
        st.subheader("📅 Pertemuan 2")
        p2_data = data_soal.get("pertemuan_2", {})
        st.write(f"**Judul:** {p2_data.get('judul', 'Belum diatur')}")
        st.info(p2_data.get("deskripsi", ""))
        
        total_skor_p2 = sum(soal.get("skor", 0) for soal in p2_data.get("soal_list", []))
        st.metric("🏆 Total Skor Maksimal", total_skor_p2)

        for i, soal in enumerate(p2_data.get("soal_list", [])):
            st.markdown(f"#### Soal {i+1}: {soal['teks']}")
            if soal.get("gambar"):
                if soal["gambar"].startswith("http"):
                    st.image(soal["gambar"], width=300)
                elif os.path.exists(os.path.join(UPLOAD_FOLDER, soal["gambar"])):
                    st.image(os.path.join(UPLOAD_FOLDER, soal["gambar"]), width=300)
                else:
                    st.caption("*(Gambar tidak ditemukan)*")
            
            for opsi in soal.get("opsi", []):
                st.write(opsi)
            
            st.write(f"**Kunci Jawaban (Guru):** {soal['kunci']}")
            st.write(f"**Skor:** {soal['skor']}")
            st.divider()

    # --- TAB 2: LIHAT HASIL SISWA ---
    with tab_hasil:
        st.header("📂 Lihat Hasil Post-test Siswa")
        df_jawaban = muat_jawaban()

        if df_jawaban.empty:
            st.info("Belum ada siswa yang mengerjakan post-test.")
        else:
            # Filter hanya jawaban siswa
            df_siswa = df_jawaban[df_jawaban["role"] == "siswa"]

            if df_siswa.empty:
                st.info("Belum ada siswa yang mengerjakan post-test.")
            else:
                # Tampilkan daftar siswa yang mengumpulkan
                st.subheader("📋 Daftar Siswa yang Mengumpulkan")
                st.dataframe(df_siswa[["nama", "email", "pertemuan", "nilai_total", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))

                # Detail jawaban siswa tertentu
                st.divider()
                st.subheader("🔍 Lihat Jawaban Lengkap Siswa")
                emails_unik = df_siswa["email"].unique()
                email_pilihan = st.selectbox("Pilih Email Siswa:", ["Pilih..."] + list(emails_unik))

                if email_pilihan != "Pilih...":
                    # Ambil jawaban terakhir dari email yang dipilih
                    df_pilihan = df_siswa[df_siswa["email"] == email_pilihan].iloc[-1]
                    st.write(f"**Nama:** {df_pilihan['nama']}")
                    st.write(f"**Pertemuan:** {df_pilihan['pertemuan']}")
                    st.write(f"**Waktu Kerja:** {df_pilihan['waktu_kerja']}")
                    st.write(f"**Nilai Total:** {df_pilihan['nilai_total']}")

                    # Tampilkan jawaban
                    st.markdown("#### Jawaban Siswa:")
                    try:
                        jawaban_dict = json.loads(df_pilihan['jawaban_json'])
                        
                        # Muat soal untuk pertemuan yang dipilih
                        key_pertemuan = "pertemuan_1" if "1" in df_pilihan['pertemuan'] else "pertemuan_2"
                        soal_pertemuan = data_soal.get(key_pertemuan, {}).get("soal_list", [])
                        
                        for soal in soal_pertemuan:
                            soal_id = soal["id"]
                            st.markdown(f"**Soal:** {soal['teks']}")
                            if soal.get("gambar"):
                                if soal["gambar"].startswith("http"):
                                    st.image(soal["gambar"], width=200)
                                elif os.path.exists(os.path.join(UPLOAD_FOLDER, soal["gambar"])):
                                    st.image(os.path.join(UPLOAD_FOLDER, soal["gambar"]), width=200)
                                else:
                                    st.caption("*(Gambar tidak ditemukan)*")
                            st.write(f"**Jawaban Siswa:** {jawaban_dict.get(soal_id, '_Tidak dijawab_')}")
                            st.write(f"**Kunci Jawaban (Guru):** {soal['kunci']}")
                            st.divider()
                    except json.JSONDecodeError:
                        st.error("Format jawaban rusak.")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

# === HALAMAN SISWA: MENGERJAKAN POST-TEST ===
def siswa_page():
    st.title("📝 Post-test: Dinamika Rotasi")

    # Muat data soal
    data_soal = muat_soal()
    if not data_soal:
        st.error("Soal post-test belum diatur oleh guru.")
        return

    # Pilih Pertemuan
    st.subheader("📅 Pilih Pertemuan Post-test")
    pertemuan = st.radio("Pilih Pertemuan:", ["Pertemuan 1", "Pertemuan 2"], horizontal=True)
    
    key_pertemuan = "pertemuan_1" if pertemuan == "Pertemuan 1" else "pertemuan_2"
    data_pertemuan = data_soal.get(key_pertemuan, {})
    
    if not data_pertemuan:
        st.error(f"Soal untuk {pertemuan} belum diatur oleh guru.")
        return

    st.header(data_pertemuan.get("judul", f"Post-test {pertemuan}"))
    st.info(data_pertemuan.get("deskripsi", ""))

    # Cek apakah siswa sudah mengisi post-test untuk pertemuan ini
    df_jawaban = muat_jawaban()
    sudah_isi = not df_jawaban[
        (df_jawaban["email"] == st.session_state.current_email) & 
        (df_jawaban["pertemuan"] == pertemuan)
    ].empty

    if sudah_isi:
        st.success(f"✅ Terima kasih! Anda sudah mengerjakan post-test untuk {pertemuan}.")
        
        # Tampilkan nilai jika ada
        df_siswa = df_jawaban[
            (df_jawaban["email"] == st.session_state.current_email) & 
            (df_jawaban["pertemuan"] == pertemuan)
        ].iloc[-1]
        nilai = df_siswa["nilai_total"]
        st.subheader(f"📊 Nilai Anda: **{nilai}/100**")
        
        # Deskripsi singkat berdasarkan nilai
        if nilai >= 75:
            st.balloons()
            st.success("🎉 Luar biasa! Pemahaman Anda sangat baik.")
        elif nilai >= 60:
            st.info("👍 Bagus! Pemahaman Anda sudah cukup. Tingkatkan lagi untuk hasil yang lebih maksimal!")
        else:
            st.warning("📚 Hasil belajar Anda perlu ditingkatkan. Pelajari kembali materi dan jangan ragu bertanya.")
    else:
        # Form jawaban
        jawaban_dict = {}
        soal_list = data_pertemuan.get("soal_list", [])
        total_skor_max = sum(soal.get("skor", 0) for soal in soal_list)

        with st.form(f"form_post_test_{key_pertemuan}"):
            for i, soal in enumerate(soal_list):
                st.markdown(f"#### {i+1}. {soal['teks']}")
                # Tampilkan gambar jika ada
                if soal.get("gambar"):
                    if soal["gambar"].startswith("http"):
                        st.image(soal["gambar"], width=300)
                    elif os.path.exists(os.path.join(UPLOAD_FOLDER, soal["gambar"])):
                        st.image(os.path.join(UPLOAD_FOLDER, soal["gambar"]), width=300)
                    else:
                        st.caption("*(Gambar tidak ditemukan)*")
                
                # Opsi jawaban
                opsi_list = soal.get("opsi", [])
                pilihan = [f"{chr(65+j)}. {opsi}" for j, opsi in enumerate(opsi_list)]
                jawaban = st.radio("Pilih jawaban:", pilihan, key=soal["id"])
                # Simpan hanya hurufnya (A, B, C, D, E)
                if jawaban:
                    jawaban_dict[soal["id"]] = jawaban[0] # Ambil huruf pertama

            submitted = st.form_submit_button("✅ Kirim Jawaban Post-test")

            if submitted:
                if len(jawaban_dict) != len(soal_list):
                    st.error("⚠️ Mohon jawab semua pertanyaan.")
                else:
                    # Hitung nilai
                    nilai_total = 0
                    for soal in soal_list:
                        soal_id = soal["id"]
                        if jawaban_dict.get(soal_id) == soal["kunci"]:
                            nilai_total += soal["skor"]
                    
                    # Simpan jawaban ke file CSV
                    simpan_jawaban_baru(pertemuan, jawaban_dict, nilai_total)
                    
                    # Tampilkan hasil
                    st.success("✅ Jawaban post-test berhasil dikirim!")
                    st.subheader(f"📊 Nilai Anda: **{nilai_total}/{total_skor_max}**")
                    
                    # Deskripsi singkat berdasarkan nilai
                    persentase = (nilai_total / total_skor_max) * 100 if total_skor_max > 0 else 0
                    if persentase >= 75:
                        st.balloons()
                        st.success("🎉 Luar biasa! Pemahaman Anda sangat baik.")
                    elif persentase >= 60:
                        st.info("👍 Bagus! Pemahaman Anda sudah cukup. Tingkatkan lagi untuk hasil yang lebih maksimal!")
                    else:
                        st.warning("📚 Hasil belajar Anda perlu ditingkatkan. Pelajari kembali materi dan jangan ragu bertanya.")

# === HALAMAN ADMIN (Bisa melihat halaman guru) ===
def admin_page():
    guru_page() # Admin bisa melihat halaman guru

# === MAIN APP ===
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.current_user = ""
        st.session_state.current_email = ""
        st.rerun()

    # Tampilkan halaman berdasarkan role
    if st.session_state.role == "guru":
        guru_page()
    elif st.session_state.role == "admin":
        admin_page()
    elif st.session_state.role == "siswa":
        siswa_page()