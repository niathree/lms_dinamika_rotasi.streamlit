# refleksi_siswa_dinamika_rotasi_v3.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="Refleksi Siswa Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
REFLEKSI_INFO_FILE = "refleksi_info_v3.json" # File untuk menyimpan pertanyaan refleksi
REFLEKSI_DATA_FILE = "refleksi_data_siswa_v3.csv" # File untuk menyimpan jawaban siswa

# Inisialisasi file pertanyaan refleksi jika belum ada
# Data diambil dari LKPD DINAMIKA ROTASI revisi.pdf
if not os.path.exists(REFLEKSI_INFO_FILE):
    default_pertanyaan = {
        "judul": "Refleksi Pembelajaran: Dinamika Rotasi",
        "deskripsi": "Halo, Sobat Fisika! Setelah menyelesaikan pembelajaran dan praktikum tentang Dinamika Rotasi, saatnya kamu merefleksikan pengalaman belajarmu. Jawablah pertanyaan-pertanyaan berikut dengan jujur dan terbuka untuk membantu guru memahami pemikiran dan perkembanganmu.",
        "pertanyaan_list": [
            {
                "id": "q1",
                "teks": "Bagaimana perasaan Anda setelah mempelajari materi pada pertemuan ini?"
            },
            {
                "id": "q2",
                "teks": "Materi apa yang belum Anda pahami pada pembelajaran ini?"
            },
            {
                "id": "q3",
                "teks": "Menurut Anda, materi apa yang paling menyenangkan pada pembelajaran ini?"
            },
            {
                "id": "q4",
                "teks": "Apa yang akan Anda lakukan untuk mempelajari materi yang belum Anda mengerti?"
            },
            {
                "id": "q5",
                "teks": "Apa yang akan Anda lakukan untuk meningkatkan hasil belajar Anda?"
            }
        ],
        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(REFLEKSI_INFO_FILE, "w", encoding='utf-8') as f:
        json.dump(default_pertanyaan, f, indent=4, ensure_ascii=False)

# Inisialisasi file data jawaban siswa jika belum ada
if not os.path.exists(REFLEKSI_DATA_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "jawaban_json", "waktu_kumpul", "role"
    ]).to_csv(REFLEKSI_DATA_FILE, index=False)

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
    st.title("🔐 Login Refleksi Siswa")
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
def muat_refleksi():
    """Muat pertanyaan refleksi dari file JSON."""
    if os.path.exists(REFLEKSI_INFO_FILE):
        try:
            with open(REFLEKSI_INFO_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            st.error("File pertanyaan refleksi rusak atau tidak ditemukan.")
    return None

def simpan_refleksi(data_baru):
    """Simpan pertanyaan refleksi ke file JSON."""
    try:
        with open(REFLEKSI_INFO_FILE, "w", encoding='utf-8') as f:
            json.dump(data_baru, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Gagal menyimpan pertanyaan refleksi: {e}")

def muat_jawaban():
    """Muat jawaban siswa dari file CSV."""
    if os.path.exists(REFLEKSI_DATA_FILE):
        try:
            return pd.read_csv(REFLEKSI_DATA_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    # Buat dataframe kosong jika file tidak ada atau kosong
    df_kosong = pd.DataFrame(columns=["email", "nama", "jawaban_json", "waktu_kumpul", "role"])
    df_kosong.to_csv(REFLEKSI_DATA_FILE, index=False)
    return df_kosong

def simpan_jawaban_baru(jawaban_dict):
    """Simpan jawaban baru siswa ke file CSV."""
    df = muat_jawaban()
    try:
        jawaban_json_str = json.dumps(jawaban_dict, ensure_ascii=False)
        new_entry = pd.DataFrame([{
            "email": st.session_state.current_email,
            "nama": st.session_state.current_user,
            "jawaban_json": jawaban_json_str,
            "waktu_kumpul": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": "siswa"
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(REFLEKSI_DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Gagal menyimpan jawaban: {e}")

# === HALAMAN GURU: EDIT PERTANYAAN & LIHAT JAWABAN SISWA ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Refleksi Siswa Dinamika Rotasi")

    # Muat data refleksi
    data_refleksi = muat_refleksi()
    if not data_refleksi:
        st.error("Data refleksi belum diatur atau rusak.")
        return

    tab_edit, tab_hasil = st.tabs(["📝 Edit Pertanyaan Refleksi", "📂 Lihat Jawaban Siswa"])

    # --- TAB 1: Edit Pertanyaan Refleksi ---
    with tab_edit:
        st.subheader("📝 Edit Pertanyaan Refleksi Siswa")

        # Judul dan Deskripsi
        judul_baru = st.text_input("📄 Judul Refleksi", value=data_refleksi.get("judul", ""))
        desc_baru = st.text_area("ℹ️ Deskripsi", value=data_refleksi.get("deskripsi", ""), height=150)

        # Daftar Pertanyaan
        st.subheader("📄 Daftar Pertanyaan Refleksi")
        pertanyaan_list = data_refleksi.get("pertanyaan_list", [])
        pertanyaan_baru_list = []

        for i, q in enumerate(pertanyaan_list):
            st.markdown(f"#### Pertanyaan {i+1}")
            q_id = q.get("id", f"q{i+1}")
            teks_baru = st.text_area(f"Teks Pertanyaan {i+1}", value=q.get("teks", ""), key=f"ref_q_{i}")
            pertanyaan_baru_list.append({
                "id": q_id,
                "teks": teks_baru
            })

        # Tombol Simpan
        if st.button("💾 Simpan Pertanyaan Refleksi"):
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "pertanyaan_list": pertanyaan_baru_list,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_refleksi(data_baru)
            st.success("✅ Pertanyaan refleksi berhasil diperbarui!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau untuk Siswa")
        st.write(f"**{judul_baru}**")
        st.info(desc_baru)
        for i, q in enumerate(pertanyaan_baru_list, 1):
            st.markdown(f"**{i}. {q['teks']}**")

    # --- TAB 2: Lihat Jawaban Siswa ---
    with tab_hasil:
        st.subheader("📂 Lihat Jawaban Refleksi Siswa")

        df_jawaban = muat_jawaban()
        df_siswa = df_jawaban[df_jawaban["role"] == "siswa"] # Filter hanya jawaban siswa

        if df_siswa.empty:
            st.info("Belum ada siswa yang mengumpulkan jawaban refleksi.")
        else:
            # Tampilkan daftar siswa yang mengumpulkan
            st.dataframe(df_siswa[["nama", "email", "waktu_kumpul"]].sort_values(by="waktu_kumpul", ascending=False))

            # Detail jawaban siswa tertentu
            st.divider()
            st.subheader("🔍 Lihat Jawaban Lengkap Siswa")
            emails_unik = df_siswa["email"].unique()
            email_pilihan = st.selectbox("Pilih Email Siswa:", ["Pilih..."] + list(emails_unik))

            if email_pilihan != "Pilih...":
                # Ambil jawaban terakhir dari email yang dipilih
                df_pilihan = df_siswa[df_siswa["email"] == email_pilihan].iloc[-1]
                st.write(f"**Nama:** {df_pilihan['nama']}")
                st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kumpul']}")

                # Tampilkan jawaban
                st.markdown("#### Jawaban Refleksi:")
                try:
                    jawaban_dict = json.loads(df_pilihan['jawaban_json'])
                    
                    # Muat pertanyaan terbaru untuk menampilkan teks soal
                    data_refleksi_terbaru = muat_refleksi()
                    pertanyaan_list_terbaru = data_refleksi_terbaru.get("pertanyaan_list", [])
                    
                    for q in pertanyaan_list_terbaru:
                        q_id = q["id"]
                        st.markdown(f"**{q['id'].split('_')[-1][1:]}. {q['teks']}**")
                        jawaban_siswa = jawaban_dict.get(q_id, "_Tidak dijawab_")
                        if jawaban_siswa.strip():
                            st.write(jawaban_siswa)
                        else:
                            st.write("_Tidak dijawab_")
                        st.divider()
                except json.JSONDecodeError:
                    st.error("Format jawaban rusak.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# === HALAMAN SISWA: MENGERJAKAN REFLEKSI ===
def siswa_page():
    st.header("💭 Refleksi Pembelajaran: Dinamika Rotasi")

    # Muat data refleksi
    data_refleksi = muat_refleksi()
    if not data_refleksi:
        st.error("Refleksi belum diatur oleh guru.")
        return

    st.subheader(data_refleksi.get("judul", "Refleksi Siswa"))
    st.info(data_refleksi.get("deskripsi", ""))

    # Cek apakah siswa sudah mengisi refleksi
    df_jawaban = muat_jawaban()
    sudah_isi = not df_jawaban[
        (df_jawaban["email"] == st.session_state.current_email) & 
        (df_jawaban["role"] == "siswa")
    ].empty

    if sudah_isi:
        st.success("✅ Terima kasih! Anda sudah mengisi refleksi.")
    else:
        # Form jawaban
        jawaban_dict = {}
        pertanyaan_list = data_refleksi.get("pertanyaan_list", [])

        with st.form("form_refleksi"):
            for i, q in enumerate(pertanyaan_list):
                q_id = q["id"]
                st.subheader(f"{i+1}. {q['teks']}")
                jawaban = st.text_area("Jawaban Anda:", key=q_id, height=100)
                jawaban_dict[q_id] = jawaban

            submitted = st.form_submit_button("✅ Kirim Jawaban Refleksi")

            if submitted:
                if any(not v.strip() for v in jawaban_dict.values()):
                    st.error("⚠️ Mohon jawab semua pertanyaan.")
                else:
                    simpan_jawaban_baru(jawaban_dict)
                    st.success("✅ Jawaban refleksi Anda berhasil dikirim!")

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
        # Admin bisa melihat halaman guru
        guru_page()
    elif st.session_state.role == "siswa":
        siswa_page()