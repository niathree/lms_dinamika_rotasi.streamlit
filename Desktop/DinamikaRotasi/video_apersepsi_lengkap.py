import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI ===
VIDEO_FILE = "aperspsi_rotasi.mp4"
DATA_PENONTON_FILE = "data_penonton.csv"
DESKRIPSI_FILE = "deskripsi_video.json" # File untuk deskripsi opsional guru

# Inisialisasi file jika belum ada
if not os.path.exists(DATA_PENONTON_FILE):
    pd.DataFrame(columns=["email", "nama", "waktu_nonton", "role"]).to_csv(DATA_PENONTON_FILE, index=False)
if not os.path.exists(DESKRIPSI_FILE):
    with open(DESKRIPSI_FILE, "w") as f:
        json.dump({"judul": "", "deskripsi": "", "waktu_upload": ""}, f)

# Session state untuk login (contoh sederhana)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "current_email" not in st.session_state:
    st.session_state.current_email = ""

# === FUNGSI LOGIN (Contoh sederhana, sebaiknya gunakan sistem autentikasi yang lebih aman) ===
def login():
    st.title("🔐 Login Video Apersepsi")
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

# === HALAMAN GURU: VIDEO APERSEPSI & LIHAT PENONTON ===
def guru_page():
    st.header("🎥 Upload & Pantau Video Apersepsi")

    # Upload Video & Deskripsi (opsional)
    st.subheader("Upload Video & Deskripsi Tambahan (Opsional)")
    vid = st.file_uploader("Pilih file video (MP4)", type=["mp4"])
    judul_video = st.text_input("Judul Video (Opsional)")
    deskripsi_video = st.text_area("Deskripsi Tambahan untuk Guru (Tidak Ditampilkan ke Siswa)", placeholder="Contoh: Video ini menunjukkan fenomena hukum kekekalan momentum sudut pada penari balet...")

    if st.button("Upload Video & Simpan Deskripsi"):
        if vid is not None:
            with open(VIDEO_FILE, "wb") as f:
                f.write(vid.read())
            st.success("✅ Video apersepsi berhasil diupload dan **disimpan secara permanen**!")

            # Simpan deskripsi tambahan ke file JSON
            deskripsi_data = {
                "judul": judul_video if judul_video else "Video Apersepsi",
                "deskripsi": deskripsi_video,
                "waktu_upload": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(DESKRIPSI_FILE, "w") as f:
                json.dump(deskripsi_data, f)
            st.success("✅ Deskripsi video tambahan berhasil disimpan.")
        else:
            st.error("❌ Silakan pilih file video terlebih dahulu.")


    st.divider()

    # Muat dan tampilkan deskripsi tambahan (hanya untuk guru)
    if os.path.exists(DESKRIPSI_FILE):
        with open(DESKRIPSI_FILE, "r") as f:
            deskripsi = json.load(f)
        st.subheader("📋 Deskripsi Tambahan (Hanya untuk Guru)")
        st.write(f"**Judul:** {deskripsi['judul']}")
        if deskripsi['deskripsi']:
            st.write(f"**Deskripsi:** {deskripsi['deskripsi']}")
        else:
            st.info("Deskripsi tambahan belum diisi.")
        if deskripsi['waktu_upload']:
            st.caption(f"Diupload pada: {deskripsi['waktu_upload']}")
    else:
        st.info("Deskripsi tambahan belum disimpan.")

    # Cek apakah file video ada
    if os.path.exists(VIDEO_FILE):
        st.video(VIDEO_FILE)
        st.success("✅ Pratinjau video berhasil dimuat.")
    else:
        st.warning("📁 File video belum diupload oleh guru.")

    st.divider()

    # Lihat Daftar Penonton
    st.subheader("📋 Daftar Siswa yang Sudah Menonton")
    df_penonton = pd.read_csv(DATA_PENONTON_FILE)
    df_penonton_siswa = df_penonton[df_penonton["role"] == "siswa"] # Filter hanya siswa

    if df_penonton_siswa.empty:
        st.info("Belum ada siswa yang menonton video.")
    else:
        # Urutkan berdasarkan waktu terbaru
        df_sorted = df_penonton_siswa.sort_values("waktu_nonton", ascending=False)
        st.dataframe(df_sorted)
        # Opsi tambahan: Statistik
        st.subheader("Statistik")
        total_siswa = df_penonton_siswa["email"].nunique()
        st.metric(label="Jumlah Siswa yang Menonton", value=total_siswa)

# === HALAMAN SISWA: VIDEO APERSEPSI & TANDAI SUDAH ===
def siswa_page():
    st.header("🎥 Video Apersepsi: Dinamika Rotasi")

    # Deskripsi statis yang selalu ditampilkan ke siswa
    st.markdown("""
    ### 🌟 Selamat Datang di Dunia Rotasi!
    **Dibawakan oleh: Nia Three Manurung**

    Sebelum kita memulai perjalanan memahami **Dinamika Rotasi**, mari kita menyaksikan dua fenomena menakjubkan berikut:

    - **Mengapa seorang penari balet bisa berputar lebih cepat saat menarik tangannya ke dada?**
    - **Mengapa lebih mudah membuka pintu dari ujungnya daripada dekat engsel?**

    > 💡 *Fenomena-fenomena ini adalah pintu gerbang menuju pemahaman tentang **Torsi, Momen Inersia**, dan **Momentum Sudut** — konsep utama dalam Dinamika Rotasi!*

    **Tonton video ini dengan saksama — nanti Anda akan menjawab beberapa pertanyaan berdasarkan video ini!**
    """)

    st.divider()

    # Cek apakah file video ada
    if os.path.exists(VIDEO_FILE):
        st.video(VIDEO_FILE)
        st.success("✅ Video berhasil dimuat.")

        # Tombol untuk menandai bahwa siswa telah menonton
        # Cek apakah siswa sudah menonton sebelumnya
        df_penonton = pd.read_csv(DATA_PENONTON_FILE)
        sudah_nonton = not df_penonton[(df_penonton["email"] == st.session_state.current_email) & (df_penonton["role"] == "siswa")].empty

        if sudah_nonton:
            st.info("✅ Anda sudah menonton video ini.")
        else:
            if st.button("✅ Saya Sudah Menonton"):
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "waktu_nonton": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                new_entry.to_csv(DATA_PENONTON_FILE, mode='a', header=False, index=False)
                st.success("✅ Status penontonan berhasil disimpan.")
                st.rerun() # Refresh halaman untuk menampilkan info "sudah menonton"
    else:
        st.warning("""
        📁 File video apersepsi belum diupload oleh guru.

        Silakan kembali nanti atau hubungi guru Anda.
        """)

    st.divider()

    st.info("💡 Setelah menonton, Anda akan diminta menjawab beberapa pertanyaan pemantik untuk memicu rasa ingin tahu Anda.")

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