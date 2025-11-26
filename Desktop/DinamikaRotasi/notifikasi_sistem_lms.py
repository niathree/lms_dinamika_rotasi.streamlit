# notifikasi_sistem_lms_dinamika_rotasi_fix.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="LMS Dinamika Rotasi - Notifikasi", layout="wide")

# --- KONSTANTA ---
ADMIN_PASSWORD = "admin123"
GURU_PASSWORD = "guru123"
DATA_SISWA_FILE = "data_siswa_notifikasi.csv"
DATA_HADIR_FILE = "data_hadir.csv"
DATA_LKPD_FILE = "data_lkpd.csv"
DATA_REFLEKSI_FILE = "data_refleksi.json"
DATA_ASESMEN_FILE = "data_asesmen.csv"
FORUM_FILE = "forum_diskusi.csv"

# Inisialisasi file data siswa jika belum ada
if not os.path.exists(DATA_SISWA_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "elemen_diakses", "waktu_akses", "role"
    ]).to_csv(DATA_SISWA_FILE, index=False)

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
    st.title("🔐 Login Notifikasi Sistem")
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

def muat_notifikasi():
    """Muat data notifikasi dari file JSON."""
    NOTIFIKASI_FILE = "notifikasi_sistem.json"
    if os.path.exists(NOTIFIKASI_FILE):
        try:
            with open(NOTIFIKASI_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return None

def simpan_notifikasi(data):
    """Simpan data notifikasi ke file JSON."""
    NOTIFIKASI_FILE = "notifikasi_sistem.json"
    try:
        with open(NOTIFIKASI_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Gagal menyimpan data notifikasi: {e}")

def muat_data_siswa():
    """Muat data akses siswa dari file CSV."""
    if os.path.exists(DATA_SISWA_FILE):
        try:
            return pd.read_csv(DATA_SISWA_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError):
            pass
    return pd.DataFrame(columns=["email", "nama", "elemen_diakses", "waktu_akses", "role"])

def simpan_data_siswa(data):
    """Simpan data akses siswa ke file CSV."""
    try:
        data.to_csv(DATA_SISWA_FILE, index=False)
    except Exception as e:
        st.error(f"Gagal menyimpan data akses siswa: {e}")

def cek_notifikasi(elemen_nama):
    """Cek apakah ada notifikasi baru untuk elemen tertentu."""
    # Muat data notifikasi
    notif_data = muat_notifikasi()
    if not notif_data:
        return False

    # Muat data akses siswa
    df_siswa = muat_data_siswa()
    df_siswa_ini = df_siswa[
        (df_siswa["email"] == st.session_state.current_email) & 
        (df_siswa["role"] == "siswa") &
        (df_siswa["elemen_diakses"] == elemen_nama)
    ]

    # Ambil waktu update terakhir dari guru
    waktu_update_guru_str = notif_data.get(elemen_nama, "")
    if not waktu_update_guru_str:
        return False # Tidak ada update

    try:
        waktu_update_guru = datetime.strptime(waktu_update_guru_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False # Format waktu salah

    # Jika siswa belum pernah akses elemen ini, tampilkan notifikasi
    if df_siswa_ini.empty:
        return True

    # Jika siswa pernah akses, bandingkan waktu
    waktu_akses_siswa_str = df_siswa_ini["waktu_akses"].max()
    try:
        waktu_akses_siswa = datetime.strptime(waktu_akses_siswa_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False # Format waktu salah

    # Jika waktu update guru lebih baru dari waktu akses siswa, tampilkan notifikasi
    return waktu_update_guru > waktu_akses_siswa

def reset_notifikasi(elemen_nama):
    """Reset notifikasi setelah siswa membuka elemen."""
    # Muat data akses siswa
    df_siswa = muat_data_siswa()

    # Tambahkan atau perbarui entri akses
    new_entry = pd.DataFrame([{
        "email": st.session_state.current_email,
        "nama": st.session_state.current_user,
        "elemen_diakses": elemen_nama,
        "waktu_akses": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": "siswa"
    }])
    df_siswa = pd.concat([df_siswa, new_entry], ignore_index=True)
    simpan_data_siswa(df_siswa)

# === HALAMAN GURU: KELOLA NOTIFIKASI ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Kelola Notifikasi Sistem")

    # Muat data notifikasi
    notif_data = muat_notifikasi()
    # 🔥 PERBAIKAN: Tambahkan ":" di akhir if
    if not notif_data:
        # Struktur default jika file tidak ditemukan
        notif_data = {
            "Daftar Hadir": "",
            "Video Apersepsi": "",
            "Pre-test": "",
            "Deskripsi Materi": "",
            "Media Pembelajaran": "",
            "Simulasi Virtual": "",
            "LKPD": "",
            "Refleksi Siswa": "",
            "Post-test": "",
            "Forum Diskusi": "",
            "Hasil Penilaian": "",
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        simpan_notifikasi(notif_data)
        st.info("File notifikasi sistem berhasil dibuat.")

    # Tampilkan dan izinkan guru mengedit waktu update
    st.subheader("🔔 Edit Waktu Update Elemen")
    st.info("Ubah waktu update elemen untuk memicu notifikasi ke siswa. Format: YYYY-MM-DD HH:MM:SS")

    updated_data = {}
    for elemen in [
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
    ]:
        waktu_lama = notif_data.get(elemen, "")
        waktu_baru = st.text_input(f"Waktu Update {elemen}", value=waktu_lama, key=f"notif_{elemen.replace(' ', '_')}")
        updated_data[elemen] = waktu_baru

    if st.button("💾 Simpan Perubahan Notifikasi"):
        updated_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        simpan_notifikasi(updated_data)
        st.success("✅ Semua notifikasi berhasil diperbarui!")

    # Tampilkan pratinjau
    st.divider()
    st.subheader("👁️‍🗨️ Pratinjau Notifikasi untuk Siswa")
    for elemen, waktu in updated_data.items():
        if elemen != "waktu_update":
            if waktu:
                st.write(f"**{elemen}**: ✅ Terakhir diperbarui pada {waktu}")
            else:
                st.write(f"**{elemen}**: 🕐 Belum ada update.")

# === HALAMAN SISWA: LIHAT NOTIFIKASI DI SIDEBAR ===
def siswa_page():
    st.header("🎓 Dasbor Siswa: LMS Dinamika Rotasi")

    # Muat data notifikasi
    notif_data = muat_notifikasi()
    if not notif_data:
        st.error("Notifikasi sistem belum diatur oleh guru.")
        return

    # Tampilkan notifikasi di sidebar
    with st.sidebar:
        st.subheader("🔔 Notifikasi Terbaru")
        menu_urutan = [
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

        ada_notif = False
        for elemen in menu_urutan:
            if cek_notifikasi(elemen):
                st.warning(f"🔔 Ada pembaruan pada **{elemen}**!")
                ada_notif = True
        
        if not ada_notif:
            st.info("Tidak ada notifikasi baru.")

    # Menu navigasi siswa
    menu = st.sidebar.selectbox(
        "Navigasi",
        menu_urutan
    )

    # Tampilkan halaman sesuai menu dan reset notifikasi
    if menu == "Daftar Hadir":
        st.subheader("📝 Daftar Hadir")
        # ... (kode daftar hadir seperti biasa)
        reset_notifikasi("Daftar Hadir")

    elif menu == "Video Apersepsi":
        st.subheader("🎥 Video Apersepsi")
        # ... (kode video apersepsi seperti biasa)
        reset_notifikasi("Video Apersepsi")

    elif menu == "Pre-test":
        st.subheader("🧠 Pre-test")
        # ... (kode pre-test seperti biasa)
        reset_notifikasi("Pre-test")

    elif menu == "Deskripsi Materi":
        st.subheader("📚 Deskripsi Materi")
        # ... (kode deskripsi materi seperti biasa)
        reset_notifikasi("Deskripsi Materi")

    elif menu == "Media Pembelajaran":
        st.subheader("📚 Media Pembelajaran")
        # ... (kode media pembelajaran seperti biasa)
        reset_notifikasi("Media Pembelajaran")

    elif menu == "Simulasi Virtual":
        st.subheader("🧪 Simulasi Virtual")
        # ... (kode simulasi virtual seperti biasa)
        reset_notifikasi("Simulasi Virtual")

    elif menu == "LKPD":
        st.subheader("📄 LKPD")
        # ... (kode LKPD seperti biasa)
        reset_notifikasi("LKPD")

    elif menu == "Refleksi Siswa":
        st.subheader("💭 Refleksi Siswa")
        # ... (kode refleksi siswa seperti biasa)
        reset_notifikasi("Refleksi Siswa")

    elif menu == "Post-test":
        st.subheader("📝 Post-test")
        # ... (kode post-test seperti biasa)
        reset_notifikasi("Post-test")

    elif menu == "Forum Diskusi":
        st.subheader("💬 Forum Diskusi")
        # ... (kode forum diskusi seperti biasa)
        reset_notifikasi("Forum Diskusi")

    elif menu == "Hasil Penilaian":
        st.subheader("📊 Hasil Penilaian")
        # ... (kode hasil penilaian seperti biasa)
        reset_notifikasi("Hasil Penilaian")

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