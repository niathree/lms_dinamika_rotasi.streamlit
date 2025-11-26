# media_pembelajaran_dinamika_rotasi_dengan_hapus_video.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import uuid

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="Media Pembelajaran - Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
UPLOAD_FOLDER = "uploaded_media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MEDIA_PEMBELAJARAN_FILE = "media_pembelajaran_dengan_hapus_video.json" # File untuk menyimpan bahan ajar & media

# Inisialisasi file media pembelajaran jika belum ada
if not os.path.exists(MEDIA_PEMBELAJARAN_FILE):
    # Struktur default berdasarkan modul ajar
    default_media = {
        "judul": "Media Pembelajaran: Dinamika Rotasi",
        "deskripsi": "Berikut adalah media pembelajaran tambahan untuk memperdalam pemahaman Anda tentang Dinamika Rotasi.",
        "pertemuan_1": {
            "judul": "Pertemuan 1",
            "bahan_ajar": "", # Guru bisa menulis langsung di sini
            "deskripsi": "Bahan ajar untuk Pertemuan 1",
            "videos": [], # Video tambahan dari guru
            "images": []  # Gambar tambahan dari guru
        },
        "pertemuan_2": {
            "judul": "Pertemuan 2",
            "bahan_ajar": "", # Guru bisa menulis langsung di sini
            "deskripsi": "Bahan ajar untuk Pertemuan 2",
            "videos": [], # Video tambahan dari guru
            "images": []  # Gambar tambahan dari guru
        },
        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(MEDIA_PEMBELAJARAN_FILE, "w", encoding='utf-8') as f:
        json.dump(default_media, f, indent=4, ensure_ascii=False)

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
    st.title("🔐 Login Media Pembelajaran")
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

def muat_media():
    """Muat data media pembelajaran dari file JSON."""
    if os.path.exists(MEDIA_PEMBELAJARAN_FILE):
        try:
            with open(MEDIA_PEMBELAJARAN_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return None

def simpan_media(data):
    """Simpan data media pembelajaran ke file JSON."""
    try:
        with open(MEDIA_PEMBELAJARAN_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Gagal menyimpan data media: {e}")

# === HALAMAN GURU: EDIT MEDIA PEMBELAJARAN & HAPUS VIDEO/GAMBAR ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Media Pembelajaran Dinamika Rotasi")

    # Muat data media
    media_data = muat_media()
    if not media_data:
        st.error("File media pembelajaran rusak atau tidak ditemukan.")
        return

    tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

    # --- TAB 1: Pertemuan 1 ---
    with tab1:
        st.subheader("📅 Edit Media Pembelajaran - Pertemuan 1")
        p1_data = media_data.get("pertemuan_1", {})
        
        # Judul dan Deskripsi
        judul_p1 = st.text_input("📄 Judul Pertemuan 1", value=p1_data.get("judul", ""))
        desc_p1 = st.text_area("ℹ️ Deskripsi Bahan Ajar Pertemuan 1", value=p1_data.get("deskripsi", ""), height=100)
        
        # Bahan Ajar (ditulis langsung, bukan upload PDF)
        bahan_ajar_p1 = st.text_area("📝 Bahan Ajar Pertemuan 1 (Ditulis Langsung)", value=p1_data.get("bahan_ajar", ""), height=300)
        
        # Upload video & gambar tambahan
        st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 1")
        new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p1")
        new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p1")
        if st.button("➕ Tambahkan Video/Gambar Pertemuan 1"):
            if new_video_url:
                # Validasi sederhana untuk URL embed
                if "youtube.com/embed/" in new_video_url:
                    p1_data["videos"].append({
                        "judul": f"Video {len(p1_data['videos']) + 1}",
                        "url": new_video_url,
                        "sumber": "YouTube/Guru"
                    })
                    st.success("✅ Video berhasil ditambahkan!")
                else:
                    st.error("Harap gunakan URL 'embed' YouTube yang valid. Contoh: https://www.youtube.com/embed/VIDEO_ID")
            if new_image_url:
                p1_data["images"].append({
                    "judul": f"Gambar {len(p1_data['images']) + 1}",
                    "url": new_image_url,
                    "sumber": "Guru"
                })
                st.success("✅ Gambar berhasil ditambahkan!")
            media_data["pertemuan_1"] = p1_data
            media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simpan_media(media_data)
            st.rerun()

        # Tombol Simpan
        if st.button("💾 Simpan Media Pembelajaran Pertemuan 1"):
            p1_data["judul"] = judul_p1
            p1_data["deskripsi"] = desc_p1
            p1_data["bahan_ajar"] = bahan_ajar_p1
            media_data["pertemuan_1"] = p1_data
            media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simpan_media(media_data)
            st.success("✅ Media Pembelajaran Pertemuan 1 berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Media Pembelajaran untuk Siswa")
        st.write(f"**{p1_data.get('judul', 'Pertemuan 1')}**")
        st.info(p1_data.get("deskripsi", ""))
        st.markdown("### 📚 Bahan Ajar")
        st.write(p1_data.get("bahan_ajar", ""))
        
        # Tampilkan video & gambar tambahan
        st.subheader("🎬 Video Tambahan")
        for i, video in enumerate(p1_data.get("videos", [])):
            st.markdown(f"**{i+1}. {video['judul']}**")
            st.video(video["url"])
            st.caption(f"Sumber: {video['sumber']}")
            # Tombol hapus video
            if st.button(f"🗑️ Hapus Video {i+1}", key=f"hapus_video_p1_{i}"):
                p1_data["videos"].pop(i)
                media_data["pertemuan_1"] = p1_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_media(media_data)
                st.success("✅ Video berhasil dihapus!")
                st.rerun()
        
        st.subheader("🖼️ Gambar Tambahan")
        for i, image in enumerate(p1_data.get("images", [])):
            st.markdown(f"**{i+1}. {image['judul']}**")
            st.image(image["url"], caption=image["sumber"], use_column_width=True)
            # Tombol hapus gambar
            if st.button(f"🗑️ Hapus Gambar {i+1}", key=f"hapus_gambar_p1_{i}"):
                p1_data["images"].pop(i)
                media_data["pertemuan_1"] = p1_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_media(media_data)
                st.success("✅ Gambar berhasil dihapus!")
                st.rerun()

    # --- TAB 2: Pertemuan 2 ---
    with tab2:
        st.subheader("📅 Edit Media Pembelajaran - Pertemuan 2")
        p2_data = media_data.get("pertemuan_2", {})
        
        # Judul dan Deskripsi
        judul_p2 = st.text_input("📄 Judul Pertemuan 2", value=p2_data.get("judul", ""))
        desc_p2 = st.text_area("ℹ️ Deskripsi Bahan Ajar Pertemuan 2", value=p2_data.get("deskripsi", ""), height=100)
        
        # Bahan Ajar (ditulis langsung, bukan upload PDF)
        bahan_ajar_p2 = st.text_area("📝 Bahan Ajar Pertemuan 2 (Ditulis Langsung)", value=p2_data.get("bahan_ajar", ""), height=300)
        
        # Upload video & gambar tambahan
        st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 2")
        new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p2")
        new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p2")
        if st.button("➕ Tambahkan Video/Gambar Pertemuan 2"):
            if new_video_url:
                # Validasi sederhana untuk URL embed
                if "youtube.com/embed/" in new_video_url:
                    p2_data["videos"].append({
                        "judul": f"Video {len(p2_data['videos']) + 1}",
                        "url": new_video_url,
                        "sumber": "YouTube/Guru"
                    })
                    st.success("✅ Video berhasil ditambahkan!")
                else:
                    st.error("Harap gunakan URL 'embed' YouTube yang valid. Contoh: https://www.youtube.com/embed/VIDEO_ID")
            if new_image_url:
                p2_data["images"].append({
                    "judul": f"Gambar {len(p2_data['images']) + 1}",
                    "url": new_image_url,
                    "sumber": "Guru"
                })
                st.success("✅ Gambar berhasil ditambahkan!")
            media_data["pertemuan_2"] = p2_data
            media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simpan_media(media_data)
            st.rerun()

        # Tombol Simpan
        if st.button("💾 Simpan Media Pembelajaran Pertemuan 2"):
            p2_data["judul"] = judul_p2
            p2_data["deskripsi"] = desc_p2
            p2_data["bahan_ajar"] = bahan_ajar_p2
            media_data["pertemuan_2"] = p2_data
            media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simpan_media(media_data)
            st.success("✅ Media Pembelajaran Pertemuan 2 berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Media Pembelajaran untuk Siswa")
        st.write(f"**{p2_data.get('judul', 'Pertemuan 2')}**")
        st.info(p2_data.get("deskripsi", ""))
        st.markdown("### 📚 Bahan Ajar")
        st.write(p2_data.get("bahan_ajar", ""))
        
        # Tampilkan video & gambar tambahan
        st.subheader("🎬 Video Tambahan")
        for i, video in enumerate(p2_data.get("videos", [])):
            st.markdown(f"**{i+1}. {video['judul']}**")
            st.video(video["url"])
            st.caption(f"Sumber: {video['sumber']}")
            # Tombol hapus video
            if st.button(f"🗑️ Hapus Video {i+1}", key=f"hapus_video_p2_{i}"):
                p2_data["videos"].pop(i)
                media_data["pertemuan_2"] = p2_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_media(media_data)
                st.success("✅ Video berhasil dihapus!")
                st.rerun()
        
        st.subheader("🖼️ Gambar Tambahan")
        for i, image in enumerate(p2_data.get("images", [])):
            st.markdown(f"**{i+1}. {image['judul']}**")
            st.image(image["url"], caption=image["sumber"], use_column_width=True)
            # Tombol hapus gambar
            if st.button(f"🗑️ Hapus Gambar {i+1}", key=f"hapus_gambar_p2_{i}"):
                p2_data["images"].pop(i)
                media_data["pertemuan_2"] = p2_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_media(media_data)
                st.success("✅ Gambar berhasil dihapus!")
                st.rerun()

# === HALAMAN SISWA: UNDUH BAHAN AJAR & AKSES MEDIA ===
def siswa_page():
    st.header("📚 Media Pembelajaran: Dinamika Rotasi")
    check_hadir()

    # Muat data media
    media_data = muat_media()
    if not media_data:
        st.error("Media pembelajaran belum diatur oleh guru.")
        return

    st.write(f"**{media_data.get('judul', 'Media Pembelajaran')}**")
    st.info(media_data.get("deskripsi", ""))

    tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

    # --- TAB 1: Pertemuan 1 ---
    with tab1:
        p1_data = media_data.get("pertemuan_1", {})
        st.write(f"**{p1_data.get('judul', 'Pertemuan 1')}**")
        st.info(p1_data.get("deskripsi", ""))
        
        # Tampilkan Bahan Ajar
        st.markdown("### 📚 Bahan Ajar")
        st.write(p1_data.get("bahan_ajar", ""))
        
        # Tampilkan video & gambar tambahan
        st.subheader("🎬 Video Tambahan")
        for i, video in enumerate(p1_data.get("videos", [])):
            st.markdown(f"**{i+1}. {video['judul']}**")
            st.video(video["url"])
            st.caption(f"Sumber: {video['sumber']}")

        st.subheader("🖼️ Gambar Tambahan")
        for i, image in enumerate(p1_data.get("images", [])):
            st.markdown(f"**{i+1}. {image['judul']}**")
            st.image(image["url"], caption=image["sumber"], use_column_width=True)

    # --- TAB 2: Pertemuan 2 ---
    with tab2:
        p2_data = media_data.get("pertemuan_2", {})
        st.write(f"**{p2_data.get('judul', 'Pertemuan 2')}**")
        st.info(p2_data.get("deskripsi", ""))
        
        # Tampilkan Bahan Ajar
        st.markdown("### 📚 Bahan Ajar")
        st.write(p2_data.get("bahan_ajar", ""))
        
        # Tampilkan video & gambar tambahan
        st.subheader("🎬 Video Tambahan")
        for i, video in enumerate(p2_data.get("videos", [])):
            st.markdown(f"**{i+1}. {video['judul']}**")
            st.video(video["url"])
            st.caption(f"Sumber: {video['sumber']}")

        st.subheader("🖼️ Gambar Tambahan")
        for i, image in enumerate(p2_data.get("images", [])):
            st.markdown(f"**{i+1}. {image['judul']}**")
            st.image(image["url"], caption=image["sumber"], use_column_width=True)

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