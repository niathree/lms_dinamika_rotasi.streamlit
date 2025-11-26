# deskripsi_materi_dinamika_rotasi.py
import streamlit as st
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali, sebelum fungsi apapun) ===
st.set_page_config(page_title="Deskripsi Materi - Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
DESKRIPSI_FILE = "deskripsi_materi.json"

# Inisialisasi file jika belum ada
if not os.path.exists(DESKRIPSI_FILE):
    default_data = {
        "capaian_pembelajaran": """Pada fase F, peserta didik mampu menerapkan konsep dan prinsip vektor ke dalam kinematika dan dinamika gerak rotasi, usaha dan energi dalam sistem rotasi, serta dinamika fluida dalam gerak berputar. Peserta didik mampu memahami konsep tentang gerak rotasi dengan kecepatan sudut konstan serta mampu mengamati dan mengidentifikasi benda di sekitar yang mengalami gerak tersebut. Kemudian, peserta didik mampu memperdalam pemahaman fisika sesuai dengan minat untuk melanjutkan ke perguruan tinggi yang berhubungan dengan bidang fisika. Melalui kerja ilmiah, juga dibangun sikap ilmiah dan profil pelajar Pancasila, khususnya mandiri, inovatif, bernalar kritis, kreatif, dan bergotong royong.""",
        "tujuan_pembelajaran": [
            "Peserta didik mampu menjelaskan konsep dinamika rotasi melalui eksplorasi langsung pada aplikasi simulasi berbasis Streamlit.",
            "Peserta didik mampu menerapkan prinsip dinamika rotasi untuk memecahkan masalah kontekstual melalui simulasi dan latihan interaktif di platform Streamlit.",
            "Peserta didik mampu menganalisis hubungan antara momen gaya, momen inersia, dan percepatan sudut dengan mengubah nilai parameter dalam simulasi virtual berbasis Streamlit."
        ],
        "waktu_update": ""
    }
    with open(DESKRIPSI_FILE, "w", encoding='utf-8') as f:
        json.dump(default_data, f, indent=4, ensure_ascii=False)

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
    st.title("🔐 Login Deskripsi Materi")
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

# === HALAMAN GURU: EDIT CP & TP ===
def guru_page():
    st.header("📚 Edit Capaian & Tujuan Pembelajaran")

    # Muat data dari file
    with open(DESKRIPSI_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)

    # Form untuk mengedit CP
    st.subheader("🎯 Capaian Pembelajaran (Fase F)")
    cp_baru = st.text_area("Capaian Pembelajaran (CP)", value=data.get("capaian_pembelajaran", ""), height=200)

    # Form untuk mengedit TP
    st.subheader("📌 Tujuan Pembelajaran")
    tp_list = data.get("tujuan_pembelajaran", [])
    tp_baru_list = []
    for i, tp in enumerate(tp_list):
        tp_baru = st.text_input(f"Tujuan Pembelajaran {i+1}", value=tp, key=f"tp_{i}")
        tp_baru_list.append(tp_baru)

    # Tombol untuk menambah TP baru
    if st.button("➕ Tambah Tujuan Pembelajaran"):
        tp_baru_list.append("")
        st.rerun()

    if st.button("💾 Simpan Capaian & Tujuan Pembelajaran"):
        # Filter TP kosong
        tp_akhir = [tp.strip() for tp in tp_baru_list if tp.strip()]
        if not cp_baru.strip():
            st.error("Capaian Pembelajaran tidak boleh kosong!")
        else:
            data_baru = {
                "capaian_pembelajaran": cp_baru.strip(),
                "tujuan_pembelajaran": tp_akhir,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(DESKRIPSI_FILE, "w", encoding='utf-8') as f:
                json.dump(data_baru, f, indent=4, ensure_ascii=False)
            st.success("✅ Capaian dan Tujuan Pembelajaran berhasil disimpan!")

    # Tampilkan pratinjau terbaru
    st.divider()
    st.subheader("👁️‍🗨️ Pratinjau untuk Siswa")
    st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
    st.write(cp_baru.strip())
    st.markdown("### 📌 Tujuan Pembelajaran")
    for i, tp in enumerate(tp_baru_list):
        if tp.strip():
            st.write(f"{i+1}. {tp.strip()}")

# === HALAMAN SISWA: LIHAT CP & TP ===
def siswa_page():
    st.header("📚 Deskripsi Materi: Dinamika Rotasi")

    # Muat data dari file
    if os.path.exists(DESKRIPSI_FILE):
        with open(DESKRIPSI_FILE, "r", encoding='utf-8') as f:
            data = json.load(f)
    else:
        st.error("Deskripsi materi belum diatur oleh guru.")
        return

    # Tampilkan CP dan TP
    st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
    st.write(data["capaian_pembelajaran"])

    st.markdown("### 📌 Tujuan Pembelajaran")
    for i, tp in enumerate(data["tujuan_pembelajaran"], 1):
        st.write(f"{i}. {tp}")

    if data.get("waktu_update"):
        st.caption(f"Deskripsi terakhir diperbarui oleh guru pada: {data['waktu_update']}")

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