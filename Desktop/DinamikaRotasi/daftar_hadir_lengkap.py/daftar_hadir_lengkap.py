import streamlit as st
import pandas as pd
import os
from datetime import datetime

# === KONFIGURASI ===
DATA_FILE = "DAFTAR HADIR.csv"

# Email dan Password (sebaiknya disimpan di file konfigurasi atau environment variable untuk keamanan)
GURU_EMAIL = "guru@dinamikarotasi.sch.id"
GURU_PASSWORD = "guru123"
ADMIN_EMAIL = "admin@dinamikarotasi.sch.id"
ADMIN_PASSWORD = "admin123"

# Inisialisasi file jika belum ada
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["email", "nama", "status", "waktu", "role"]).to_csv(DATA_FILE, index=False)

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
    st.title("🔐 Login Daftar Hadir")
    email = st.text_input("Masukkan Email Anda:")

    if email:
        if email == GURU_EMAIL:
            password = st.text_input("Password Guru", type="password")
            if st.button("Login sebagai Guru"):
                if password == GURU_PASSWORD:
                    st.session_state.role = "guru"
                    st.session_state.current_user = "Guru"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Password salah!")
        elif email == ADMIN_EMAIL:
            password = st.text_input("Password Admin", type="password")
            if st.button("Login sebagai Admin"):
                if password == ADMIN_PASSWORD:
                    st.session_state.role = "admin"
                    st.session_state.current_user = "Admin"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Password salah!")
        else:
            # Asumsikan sebagai siswa jika email tidak cocok dengan guru/admin
            if st.button("Login sebagai Siswa"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title() # Ambil nama dari email
                st.session_state.current_email = email
                st.session_state.logged_in = True
                st.rerun()

# === HALAMAN SISWA: FORM HADIR ===
def siswa_page():
    st.header("📝 Daftar Hadir Siswa")

    # Jika nama belum diisi sebelumnya, minta input
    if "siswa_nama" not in st.session_state:
        nama = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
        if nama:
            st.session_state.siswa_nama = nama
    else:
        nama = st.session_state.siswa_nama

    status = st.radio("Status Kehadiran", ["Hadir", "Tidak Hadir"])

    if st.button("✅ Simpan Kehadiran"):
        if not nama.strip():
            st.error("Nama tidak boleh kosong!")
        else:
            new_entry = pd.DataFrame([{
                "email": st.session_state.current_email,
                "nama": nama.strip(),
                "status": status,
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "role": "siswa"
            }])
            new_entry.to_csv(DATA_FILE, mode='a', header=False, index=False)
            st.success(f"Terima kasih, **{nama.strip()}**! Anda telah terdaftar sebagai **{status}**.")

# === HALAMAN GURU: LIHAT KEHADIRAN ===
def guru_page():
    st.header("📋 Daftar Kehadiran Siswa")
    df = pd.read_csv(DATA_FILE)
    df_siswa = df[df["role"] == "siswa"]  # Filter hanya data siswa

    if df_siswa.empty:
        st.info("Belum ada data kehadiran siswa.")
    else:
        # Tambahkan kolom jumlah kehadiran per siswa (opsional)
        # rekap = df_siswa.groupby(["nama", "status"]).size().unstack(fill_value=0).reset_index()
        # rekap.columns = ["Nama Siswa", "Tidak Hadir", "Hadir"]
        # st.subheader("Rekap Kehadiran")
        # st.dataframe(rekap)

        st.subheader("Detail Kehadiran")
        # Urutkan berdasarkan waktu terbaru
        df_sorted = df_siswa.sort_values("waktu", ascending=False)
        st.dataframe(df_sorted)

        # Opsi untuk melihat berdasarkan status
        status_filter = st.selectbox("Filter berdasarkan status", ["Semua", "Hadir", "Tidak Hadir"])
        if status_filter != "Semua":
            df_filtered = df_sorted[df_sorted["status"] == status_filter]
            st.dataframe(df_filtered)

# === HALAMAN ADMIN: PANTAU SEMUA DATA ===
def admin_page():
    st.header("📊 Pantau Semua Data Kehadiran")
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        st.info("Belum ada data kehadiran.")
    else:
        st.subheader("Semua Catatan Kehadiran")
        # Urutkan berdasarkan waktu terbaru
        df_sorted = df.sort_values("waktu", ascending=False)
        st.dataframe(df_sorted)

        # Statistik berdasarkan role
        st.subheader("Statistik Berdasarkan Peran")
        role_counts = df["role"].value_counts()
        st.bar_chart(role_counts)

        # Filter berdasarkan role atau email
        role_filter = st.selectbox("Filter berdasarkan peran", ["Semua"] + list(df["role"].unique()))
        if role_filter != "Semua":
            df_filtered = df[df["role"] == role_filter]
            st.dataframe(df_filtered)

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
        if "siswa_nama" in st.session_state:
            del st.session_state["siswa_nama"]
        st.rerun()

    # Tampilkan halaman berdasarkan role
    if st.session_state.role == "siswa":
        siswa_page()
    elif st.session_state.role == "guru":
        guru_page()
    elif st.session_state.role == "admin":
        admin_page()