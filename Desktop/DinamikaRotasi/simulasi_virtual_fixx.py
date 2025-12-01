# simulasi_virtual_dengan_petunjuk_satu_halaman.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="Simulasi Virtual Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
UPLOAD_FOLDER = "uploaded_media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SIMULASI_INFO_FILE = "simulasi_info_dengan_petunjuk.json" # File untuk menyimpan info simulasi

# Inisialisasi file simulasi jika belum ada
if not os.path.exists(SIMULASI_INFO_FILE):
    default_simulasi = {
        "judul": "Simulasi Virtual: Dinamika Rotasi - Hanya Balancing Act",
        "deskripsi": "Eksplorasi konsep Dinamika Rotasi secara interaktif hanya dengan simulasi PhET 'Balancing Act'!",
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
            {
                "judul": "⚖️ Balancing Act (Aktivitas Keseimbangan) - PhET",
                "url": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_en.html",
                "sumber": "PhET Colorado"
            }
        ],
        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(SIMULASI_INFO_FILE, "w", encoding='utf-8') as f:
        json.dump(default_simulasi, f, indent=4, ensure_ascii=False)

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
    st.title("🔐 Login Simulasi Virtual")
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
                    st.session_state.hadir = True # Guru otomatis hadir
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
        elif email == "admin@dinamikarotasi.sch.id": # Ganti dengan email admin Anda
            password = st.text_input("🔑 Password Admin", type="password")
            if st.button("Login sebagai Admin"):
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
            if st.button("Login sebagai Siswa"):
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

def muat_simulasi():
    """Muat data simulasi dari file JSON."""
    if os.path.exists(SIMULASI_INFO_FILE):
        try:
            with open(SIMULASI_INFO_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return None

def simpan_simulasi(data):
    """Simpan data simulasi ke file JSON."""
    try:
        with open(SIMULASI_INFO_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Gagal menyimpan data simulasi: {e}")

# === HALAMAN GURU: KELOLA SIMULASI VIRTUAL ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Simulasi Virtual Dinamika Rotasi")

    # Muat data simulasi
    data_simulasi = muat_simulasi()
    if not data_simulasi:
        st.error("File simulasi info rusak atau tidak ditemukan.")
        return

    tab_edit, tab_lihat = st.tabs(["✏️ Edit Simulasi Virtual", "👁️‍🗨️ Pratinjau Simulasi untuk Siswa"])

    # --- TAB 1: Edit Simulasi Virtual ---
    with tab_edit:
        st.subheader("✏️ Edit Simulasi Virtual - Hanya Balancing Act")
        
        # Judul dan Deskripsi
        judul_baru = st.text_input("📄 Judul Simulasi Virtual", value=data_simulasi.get("judul", ""))
        desc_baru = st.text_area("ℹ️ Deskripsi Simulasi Virtual", value=data_simulasi.get("deskripsi", ""), height=150)
        
        # Petunjuk Penggunaan
        st.subheader("📘 Petunjuk Penggunaan Simulasi PhET: Balancing Act")
        petunjuk_baru = st.text_area("📝 Petunjuk Penggunaan (Markdown)", value=data_simulasi.get("petunjuk_penggunaan", ""), height=300)
        
        # Simulasi List (hanya 1 item untuk Balancing Act)
        simulasi_list = data_simulasi.get("simulasi_list", [])
        if simulasi_list:
            simulasi = simulasi_list[0] # Hanya ambil simulasi pertama (Balancing Act)
            st.markdown("#### ⚖️ Simulasi PhET: Balancing Act")
            judul_sim_baru = st.text_input("Judul Simulasi", value=simulasi.get("judul", ""))
            url_sim_baru = st.text_input("URL Embed PhET (Balancing Act)", value=simulasi.get("url", ""))
            sumber_sim_baru = st.text_input("Sumber Simulasi", value=simulasi.get("sumber", ""))
            
            simulasi_baru = {
                "judul": judul_sim_baru,
                "url": url_sim_baru,
                "sumber": sumber_sim_baru
            }
        else:
            st.error("Simulasi PhET Balancing Act belum diatur.")
            return

        # Tombol Simpan
        if st.button("💾 Simpan Seluruh Perubahan Simulasi Virtual"):
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "petunjuk_penggunaan": petunjuk_baru,
                "simulasi_list": [simulasi_baru], # Hanya 1 simulasi
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_simulasi(data_baru)
            st.success("✅ Seluruh simulasi virtual berhasil diperbarui!")

    # --- TAB 2: Pratinjau Simulasi untuk Siswa ---
    with tab_lihat:
        st.subheader("👁️‍🗨️ Pratinjau Simulasi Virtual untuk Siswa")
        
        st.write(f"**{data_simulasi.get('judul', 'Simulasi Virtual')}**")
        st.info(data_simulasi.get("deskripsi", ""))
        
        # Tampilkan Petunjuk Penggunaan
        st.markdown(data_simulasi.get("petunjuk_penggunaan", ""))
        
        # Tampilkan Simulasi PhET
        simulasi_list = data_simulasi.get("simulasi_list", [])
        if simulasi_list:
            simulasi = simulasi_list[0] # Hanya ambil simulasi pertama (Balancing Act)
            st.markdown(f"#### {simulasi['judul']}")
            st.caption(f"Sumber: {simulasi['sumber']}")
            
            # Tampilkan simulasi menggunakan iframe
            st.components.v1.iframe(simulasi["url"], height=600, scrolling=True)
        else:
            st.warning("📁 Simulasi PhET Balancing Act belum diatur.")

# === HALAMAN SISWA: MENCOBA SIMULASI VIRTUAL ===
def siswa_page():
    st.header("🧪 Simulasi Virtual: Dinamika Rotasi")
    check_hadir()

    # Muat data simulasi
    data_simulasi = muat_simulasi()
    if not data_simulasi:
        st.error("Simulasi virtual belum diatur oleh guru.")
        return

    st.write(f"**{data_simulasi.get('judul', 'Simulasi Virtual')}**")
    st.info(data_simulasi.get("deskripsi", ""))

    # Tampilkan Petunjuk Penggunaan
    st.markdown(data_simulasi.get("petunjuk_penggunaan", ""))

    st.divider()

    # Tampilkan Simulasi PhET
    simulasi_list = data_simulasi.get("simulasi_list", [])
    if simulasi_list:
        simulasi = simulasi_list[0] # Hanya ambil simulasi pertama (Balancing Act)
        st.markdown(f"#### {simulasi['judul']}")
        st.caption(f"Sumber: {simulasi['sumber']}")
        
        # Tampilkan simulasi menggunakan iframe
        st.components.v1.iframe(simulasi["url"], height=600, scrolling=True)
    else:
        st.warning("📁 Simulasi PhET Balancing Act belum diatur.")

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
        guru_page()
    elif st.session_state.role == "admin":
        # Admin bisa melihat halaman guru
        guru_page()
    elif st.session_state.role == "siswa":
        siswa_page()