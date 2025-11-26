# pre_test_dinamika_rotasi_benar_v2.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali, sebelum fungsi apapun) ===
st.set_page_config(page_title="Pre-test Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
PRE_TEST_INFO_FILE = "pre_test_info_benar_v2.json" # File untuk menyimpan soal pre-test
PRE_TEST_JAWABAN_FILE = "pre_test_jawaban_siswa_benar_v2.csv" # File untuk menyimpan jawaban siswa

# Inisialisasi file soal pre-test jika belum ada
if not os.path.exists(PRE_TEST_INFO_FILE):
    # Data soal diambil dari modul ajar
    default_soal = {
        "pertemuan_1": {
            "judul": "Pre-test Pertemuan 1: Dinamika Rotasi",
            "deskripsi": "Halo, Sobat Fisika ! Sebelum memulai pembelajaran hari ini, kamu diminta menjawab beberapa pertanyaan berikut berdasarkan pengalaman atau dugaanmu sendiri. Jawabanmu tidak dinilai, tetapi akan membantu guru memahami pemikiran awalmu. Jawablah dengan jujur dan sejujurnya — gunakan kata-katamu sendiri! Tidak ada jawaban salah ! Setelah menjawab, kamu akan menonton video apersepsi dan melakukan eksplorasi melalui simulasi interaktif untuk memperdalam pemahamanmu. Selamat bereksplorasi!",
            "soal_list": [
                {
                    "id": "p1_q1",
                    "teks": "Pernahkah kamu membuka pintu? Di bagian mana lebih mudah mendorongnya: dekat engsel atau di gagang pintu? Mengapa menurutmu?"
                },
                {
                    "id": "p1_q2",
                    "teks": "Jika kamu menggunakan kunci inggris untuk membuka baut, apakah lebih mudah memegang ujungnya atau dekat baut? Jelaskan!"
                },
                {
                    "id": "p1_q3",
                    "teks": "Bayangkan dua roda sepeda: satu polos, satu dipasangi beban di pinggirnya. Roda mana yang menurutmu lebih sulit diputar dari keadaan diam? Mengapa?"
                },
                {
                    "id": "p1_q4",
                    "teks": "Menurutmu, apa yang membuat suatu benda “sulit” atau “mudah” berputar?"
                }
            ],
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "pertemuan_2": {
            "judul": "Pre-test Pertemuan 2: Dinamika Rotasi",
            "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, coba jawab pertanyaan berikut berdasarkan intuisi atau pengalaman sehari-harimu. Jawabanmu hanya untuk memicu rasa ingin tahu — tidak ada yang dinilai benar atau salah. Tulislah jawabanmu sejujurnya. Setelah ini, kamu akan menjelajahi konsep-konsep menarik melalui simulasi virtual dan diskusi kelompok. Yuk, mulai eksplorasi !",
            "soal_list": [
                {
                    "id": "p2_q1",
                    "teks": "Pernah lihat penari balet atau pesenam berputar? Saat mereka menarik tangan ke badan, putarannya jadi lebih cepat atau lambat? Menurutmu, kenapa?"
                },
                {
                    "id": "p2_q2",
                    "teks": "Jika sebuah roda sepeda sedang berputar bebas di udara (tanpa gesekan), apakah putarannya akan berhenti sendiri? Mengapa?"
                },
                {
                    "id": "p2_q3",
                    "teks": "Apa perbedaan antara gerak lurus (translasi) dan gerak berputar (rotasi)? Berikan satu contoh benda yang mengalami kedua jenis gerak tersebut sekaligus (misalnya roda yang menggelinding)."
                },
                {
                    "id": "p2_q4",
                    "teks": "Bisakah suatu benda berputar semakin cepat tanpa didorong lagi? Jika ya, dalam situasi apa?"
                }
            ],
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    with open(PRE_TEST_INFO_FILE, "w", encoding='utf-8') as f:
        json.dump(default_soal, f, indent=4, ensure_ascii=False)

# Inisialisasi file data jawaban siswa jika belum ada
if not os.path.exists(PRE_TEST_JAWABAN_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "pertemuan", "jawaban_json", "waktu_submit", "role"
    ]).to_csv(PRE_TEST_JAWABAN_FILE, index=False)

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
    st.title("🔐 Login Pre-test")
    email = st.text_input("📧 Masukkan Email Anda:")

    if email:
        if email == "guru@dinamikarotasi.sch.id": # Ganti dengan email guru Anda
            password = st.text_input("🔑 Password Guru", type="password")
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
            password = st.text_input("🔑 Password Admin", type="password")
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
    """Muat soal pre-test dari file JSON."""
    if os.path.exists(PRE_TEST_INFO_FILE):
        try:
            with open(PRE_TEST_INFO_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            st.error("File soal pre-test rusak atau tidak ditemukan.")
    return None

def simpan_jawaban_baru(pertemuan, jawaban_dict):
    """Simpan jawaban baru siswa ke file CSV."""
    df = pd.read_csv(PRE_TEST_JAWABAN_FILE)
    try:
        jawaban_json_str = json.dumps(jawaban_dict, ensure_ascii=False)
        new_entry = pd.DataFrame([{
            "email": st.session_state.current_email,
            "nama": st.session_state.current_user,
            "pertemuan": pertemuan,
            "jawaban_json": jawaban_json_str,
            "waktu_submit": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": "siswa"
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(PRE_TEST_JAWABAN_FILE, index=False)
    except Exception as e:
        st.error(f"Gagal menyimpan jawaban: {e}")

# === HALAMAN GURU: LIHAT SOAL PRE-TEST ===
def guru_page():
    st.title("👩‍🏫 Dasbor Guru: Pre-test Dinamika Rotasi")

    # Muat data soal pre-test
    data_soal = muat_soal()
    if not data_soal:
        st.error("Data soal pre-test belum diatur atau rusak.")
        return

    tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

    # --- TAB 1: Pertemuan 1 ---
    with tab1:
        st.header("📅 Pre-test Pertemuan 1")
        p1_data = data_soal.get("pertemuan_1", {})
        st.subheader(p1_data.get("judul", "Pre-test Pertemuan 1"))
        st.info(p1_data.get("deskripsi", ""))
        
        soal_list_p1 = p1_data.get("soal_list", [])
        for i, soal in enumerate(soal_list_p1):
            st.markdown(f"#### {i+1}. {soal['teks']}")

    # --- TAB 2: Pertemuan 2 ---
    with tab2:
        st.header("📅 Pre-test Pertemuan 2")
        p2_data = data_soal.get("pertemuan_2", {})
        st.subheader(p2_data.get("judul", "Pre-test Pertemuan 2"))
        st.info(p2_data.get("deskripsi", ""))
        
        soal_list_p2 = p2_data.get("soal_list", [])
        for i, soal in enumerate(soal_list_p2):
            st.markdown(f"#### {i+1}. {soal['teks']}")

# === HALAMAN SISWA: MENGERJAKAN PRE-TEST ===
def siswa_page():
    st.title("📝 Pre-test: Dinamika Rotasi")

    # Muat data soal pre-test
    data_soal = muat_soal()
    if not data_soal:
        st.error("Soal pre-test belum diatur oleh guru.")
        return

    # Pilih Pertemuan
    st.subheader("📅 Pilih Pertemuan Pre-test")
    pertemuan = st.radio("Pilih Pertemuan:", ["Pertemuan 1", "Pertemuan 2"], horizontal=True)
    
    key_pertemuan = "pertemuan_1" if pertemuan == "Pertemuan 1" else "pertemuan_2"
    data_pertemuan = data_soal.get(key_pertemuan, {})
    
    if not data_pertemuan:
        st.error(f"Soal untuk {pertemuan} belum diatur oleh guru.")
        return

    st.header(data_pertemuan.get("judul", f"Pre-test {pertemuan}"))
    st.info(data_pertemuan.get("deskripsi", ""))

    # Cek apakah siswa sudah mengisi pre-test untuk pertemuan ini
    df_jawaban = pd.read_csv(PRE_TEST_JAWABAN_FILE)
    sudah_isi = not df_jawaban[
        (df_jawaban["email"] == st.session_state.current_email) & 
        (df_jawaban["pertemuan"] == pertemuan)
    ].empty

    if sudah_isi:
        st.success(f"✅ Terima kasih! Anda sudah mengisi pre-test untuk {pertemuan}.")
    else:
        # Form jawaban
        jawaban_dict = {}
        soal_list = data_pertemuan.get("soal_list", [])

        with st.form(f"form_pre_test_{pertemuan.lower().replace(' ', '_')}"):
            for i, soal in enumerate(soal_list):
                soal_id = soal["id"]
                st.subheader(f"{i+1}. {soal['teks']}")
                jawaban = st.text_area("Jawaban Anda:", key=soal_id, height=100)
                jawaban_dict[soal_id] = jawaban

            submitted = st.form_submit_button("✅ Kirim Jawaban Pre-test")

            if submitted:
                if any(not v.strip() for v in jawaban_dict.values()):
                    st.error("⚠️ Mohon jawab semua pertanyaan.")
                else:
                    simpan_jawaban_baru(pertemuan, jawaban_dict)
                    st.success(f"✅ Jawaban pre-test {pertemuan} Anda berhasil dikirim!")

# === MAIN APP ===
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    with st.sidebar:
        st.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
        if st.button("🚪 Logout"):
            for key in ["logged_in", "role", "current_user", "current_email"]:
                st.session_state.pop(key, None)
            st.rerun()

    # Tampilkan halaman berdasarkan role
    if st.session_state.role == "guru":
        guru_page()
    elif st.session_state.role == "admin":
        # Admin bisa melihat halaman guru
        guru_page()
    elif st.session_state.role == "siswa":
        siswa_page()