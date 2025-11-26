import streamlit as st
import json
import os
from datetime import datetime

# --- Konfigurasi awal ---
st.set_page_config(
    page_title="Simulasi Virtual: Dinamika Rotasi",
    layout="wide"
)

# --- File konfigurasi ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATA_FILE = os.path.join(DATA_DIR, "simulasi_virtual.json")
NOTIFIKASI_FILE = os.path.join(DATA_DIR, "notifikasi.json")

# --- Inisialisasi session state untuk login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "current_email" not in st.session_state:
    st.session_state.current_email = ""

# --- FUNGSI LOGIN ===
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
                st.rerun()

# --- Fungsi muat dan simpan data ---
def muat_data(key):
    file_path = os.path.join(DATA_DIR, f"{key}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    else:
        # Buat file default jika tidak ada
        if key == "simulasi_virtual":
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
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)
            return default_data
        return None

def simpan_data(key, data_baru):
    file_path = os.path.join(DATA_DIR, f"{key}.json")
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data_baru, f, indent=4, ensure_ascii=False)

# === HALAMAN GURU ===
def guru_page():
    st.header("🧪 Edit Simulasi Virtual")
    simulasi_data = muat_data("simulasi_virtual")
    if not simulasi_data:  # <-- Perbaikan: tambahkan "data"
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
        simpan_data("simulasi_virtual", data_baru)
        # Update notifikasi
        if os.path.exists(NOTIFIKASI_FILE):
            with open(NOTIFIKASI_FILE, "r") as f:
                notif = json.load(f)
        else:
            notif = {}
        notif["Simulasi Virtual"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTIFIKASI_FILE, "w") as f:
            json.dump(notif, f)
        st.success("✅ Simulasi virtual berhasil disimpan!")

    # Tampilkan pratinjau
    st.divider()
    st.subheader("👁️‍🗨️ Pratinjau Simulasi Virtual untuk Siswa")
    st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
    st.info(simulasi_data.get("deskripsi", ""))
    st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))

    for i, sim in enumerate(simulasi_data.get("simulasi_list", []), 1):
        st.markdown(f"---\n#### {i}. {sim['judul']}")
        st.caption(f"Sumber: {sim['sumber']}")
        st.markdown(sim.get("petunjuk", ""))
        st.link_button("🔗 Buka Simulasi PhET", sim["url"])
        st.info("💡 **Catatan:** Simulasi akan terbuka di tab baru browser Anda.")

# === HALAMAN SISWA ===
def siswa_page():
    st.header("🧪 Simulasi Virtual: Dinamika Rotasi")
    # check_hadir() # Anda bisa aktifkan jika fungsi ini sudah didefinisikan di tempat lain
    simulasi_data = muat_data("simulasi_virtual")
    if not simulasi_data:  # <-- Perbaikan: tambahkan "data"
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
        st.caption(f"Sumber: {simulasi['sumber']}")
        st.markdown(simulasi.get("petunjuk", ""))
        st.link_button("🔗 Buka Simulasi PhET", simulasi["url"])
        st.info("💡 **Catatan:** Simulasi akan terbuka di tab baru browser Anda.")

    # reset_notifikasi("Simulasi Virtual") # Anda bisa aktifkan jika fungsi ini sudah didefinisikan di tempat lain

# === MAIN ===
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role in ["guru", "admin"]:
        guru_page()
    elif st.session_state.role == "siswa":
        siswa_page()
    else:
        st.error("Role tidak dikenali.")