# daftar_hadir_dinamika_rotasi.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="Daftar Hadir - Dinamika Rotasi", layout="centered")

# --- KONSTANTA ---
DATA_HADIR_FILE = "data_hadir.csv" # File untuk menyimpan data kehadiran siswa
INFO_HADIR_FILE = "info_daftar_hadir.json" # File untuk menyimpan info/judul daftar hadir

# Inisialisasi file info daftar hadir jika belum ada
# Data diambil dari MODUL AJAR DAN BAHAN AJAR DINAMIKA ROTASI.pdf
if not os.path.exists(INFO_HADIR_FILE):
    default_info = {
        "judul": "📋 Daftar Hadir: Dinamika Rotasi",
        "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, silakan tandai kehadiran Anda dengan jujur. Kehadiran Anda sangat penting untuk memantau proses belajar dan memastikan semua peserta didik aktif dalam pembelajaran. Jawablah dengan jujur dan sejujurnya — tidak ada jawaban salah !",
        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(INFO_HADIR_FILE, "w", encoding='utf-8') as f:
        json.dump(default_info, f, indent=4, ensure_ascii=False)

# Inisialisasi file data kehadiran siswa jika belum ada
if not os.path.exists(DATA_HADIR_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "status_kehadiran", "waktu_submit", "role"
    ]).to_csv(DATA_HADIR_FILE, index=False)

# Session state untuk login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "current_email" not in st.session_state:
    st.session_state.current_email = ""

# === FUNGSI LOGIN (Contoh sederhana) ===
def login():
    st.title("🔐 Login Daftar Hadir")
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
def muat_info_hadir():
    """Muat info daftar hadir dari file JSON."""
    if os.path.exists(INFO_HADIR_FILE):
        try:
            with open(INFO_HADIR_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            st.error("File info daftar hadir rusak atau tidak ditemukan.")
    return None

def simpan_info_hadir(data_baru):
    """Simpan info daftar hadir ke file JSON."""
    try:
        with open(INFO_HADIR_FILE, "w", encoding='utf-8') as f:
            json.dump(data_baru, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Gagal menyimpan info daftar hadir: {e}")

def muat_data_hadir():
    """Muat data kehadiran siswa dari file CSV."""
    if os.path.exists(DATA_HADIR_FILE):
        try:
            return pd.read_csv(DATA_HADIR_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    # Buat dataframe kosong jika file tidak ada atau kosong
    df_kosong = pd.DataFrame(columns=["email", "nama", "status_kehadiran", "waktu_submit", "role"])
    df_kosong.to_csv(DATA_HADIR_FILE, index=False)
    return df_kosong

def simpan_kehadiran_baru(nama, status):
    """Simpan kehadiran baru siswa ke file CSV."""
    df = muat_data_hadir()
    new_entry = pd.DataFrame([{
        "email": st.session_state.current_email,
        "nama": nama.strip(),
        "status_kehadiran": status,
        "waktu_submit": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": "siswa"
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_HADIR_FILE, index=False)

# === HALAMAN GURU: EDIT INFO & LIHAT DAFTAR HADIR ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Daftar Hadir Dinamika Rotasi")

    # Muat info daftar hadir
    info = muat_info_hadir()
    if not info:
        st.error("Info daftar hadir belum diatur atau rusak.")
        return

    tab_edit, tab_lihat = st.tabs(["📝 Edit Info Daftar Hadir", "📂 Lihat Daftar Kehadiran Siswa"])

    # --- TAB 1: Edit Info Daftar Hadir ---
    with tab_edit:
        st.subheader("📝 Edit Informasi Daftar Hadir")

        # Form untuk mengedit judul dan deskripsi
        judul_baru = st.text_input("📄 Judul Daftar Hadir", value=info.get("judul", ""))
        desc_baru = st.text_area("ℹ️ Deskripsi", value=info.get("deskripsi", ""), height=150)

        if st.button("💾 Simpan Info Daftar Hadir"):
            data_baru = {
                "judul": judul_baru.strip(),
                "deskripsi": desc_baru.strip(),
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_info_hadir(data_baru)
            st.success("✅ Info daftar hadir berhasil diperbarui!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau untuk Siswa")
        st.write(f"**{judul_baru.strip()}**")
        st.info(desc_baru.strip())

    # --- TAB 2: Lihat Daftar Kehadiran Siswa ---
    with tab_lihat:
        st.subheader("📂 Lihat Daftar Kehadiran Siswa")

        # Muat data kehadiran
        df = muat_data_hadir()
        df_siswa = df[df["role"] == "siswa"] # Filter hanya data siswa

        if df_siswa.empty:
            st.info("Belum ada siswa yang mendaftar hadir.")
        else:
            # Tampilkan statistik singkat
            total_siswa = df_siswa["email"].nunique()
            hadir_count = df_siswa[df_siswa["status_kehadiran"] == "Hadir"].shape[0]
            tidak_hadir_count = df_siswa[df_siswa["status_kehadiran"] == "Tidak Hadir"].shape[0]

            col1, col2, col3 = st.columns(3)
            col1.metric("👥 Total Siswa", total_siswa)
            col2.metric("✅ Hadir", hadir_count)
            col3.metric("❌ Tidak Hadir", tidak_hadir_count)

            # Tampilkan daftar lengkap
            st.divider()
            st.subheader("📋 Daftar Kehadiran Lengkap")
            st.dataframe(df_siswa[["nama", "email", "status_kehadiran", "waktu_submit"]].sort_values(by="waktu_submit", ascending=False))

            # Filter berdasarkan status
            st.divider()
            st.subheader("🔍 Filter Berdasarkan Status")
            status_filter = st.radio("Pilih Status:", ["Semua", "Hadir", "Tidak Hadir"], horizontal=True)
            if status_filter != "Semua":
                df_filter = df_siswa[df_siswa["status_kehadiran"] == status_filter]
            else:
                df_filter = df_siswa
            
            if df_filter.empty:
                st.info(f"Belum ada siswa yang memilih status '{status_filter}'.")
            else:
                st.dataframe(df_filter[["nama", "email", "status_kehadiran", "waktu_submit"]].sort_values(by="waktu_submit", ascending=False))

# === HALAMAN SISWA: ISI DAFTAR HADIR ===
def siswa_page():
    st.header("📝 Daftar Hadir: Dinamika Rotasi")

    # Muat info daftar hadir
    info = muat_info_hadir()
    if not info:
        st.error("Info daftar hadir belum diatur oleh guru.")
        return

    # Tampilkan judul dan deskripsi
    st.write(f"**{info.get('judul', '📋 Daftar Hadir')}**")
    st.info(info.get("deskripsi", ""))

    # Cek apakah siswa sudah mendaftar hadir
    df = muat_data_hadir()
    sudah_hadir = not df[
        (df["email"] == st.session_state.current_email) & 
        (df["role"] == "siswa")
    ].empty

    if sudah_hadir:
        st.success("✅ Terima kasih! Anda sudah mendaftar hadir.")
    else:
        # Form daftar hadir
        with st.form("form_daftar_hadir"):
            nama = st.text_input(">Nama Lengkap:", value=st.session_state.current_user)
            status = st.radio(">Status Kehadiran:", ["Hadir", "Tidak Hadir"], horizontal=True)

            submitted = st.form_submit_button("✅ Simpan Kehadiran")

            if submitted:
                if not nama.strip():
                    st.error("⚠️ Nama tidak boleh kosong!")
                else:
                    simpan_kehadiran_baru(nama, status)
                    st.success(f"✅ Terima kasih, **{nama.strip()}**! Status kehadiran Anda: **{status}**.")

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