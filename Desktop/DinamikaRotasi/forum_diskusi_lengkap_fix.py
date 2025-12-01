# forum_diskusi_lengkap.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="Forum Diskusi - Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
FORUM_FILE = "forum_diskusi_lengkap.csv" # File untuk menyimpan komentar forum

# Inisialisasi file forum jika belum ada
if not os.path.exists(FORUM_FILE):
    pd.DataFrame(columns=[
        "id", "parent_id", "email", "nama", "pesan", "waktu", "role"
    ]).to_csv(FORUM_FILE, index=False)

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
    st.title("🔐 Login Forum Diskusi")
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
def muat_forum():
    """Muat data forum dari file CSV."""
    if os.path.exists(FORUM_FILE):
        try:
            return pd.read_csv(FORUM_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    # Buat dataframe kosong jika file tidak ada atau kosong
    df_kosong = pd.DataFrame(columns=["id", "parent_id", "email", "nama", "pesan", "waktu", "role"])
    df_kosong.to_csv(FORUM_FILE, index=False)
    return df_kosong

def simpan_komentar_baru(pesan, parent_id=-1):
    """Simpan komentar baru ke file CSV."""
    df = muat_forum()
    try:
        new_id = df["id"].max() + 1 if not df.empty else 1
        new_entry = pd.DataFrame([{
            "id": new_id,
            "parent_id": parent_id, # -1 = komentar utama, >0 = balasan
            "email": st.session_state.current_email,
            "nama": st.session_state.current_user,
            "pesan": pesan.strip(),
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": st.session_state.role
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(FORUM_FILE, index=False)
    except Exception as e:
        st.error(f"Gagal menyimpan komentar: {e}")

def hapus_komentar(id_komentar):
    """Hapus komentar berdasarkan ID (untuk guru/admin)."""
    df = muat_forum()
    df = df[df["id"] != id_komentar]
    # Hapus juga balasan dari komentar yang dihapus
    df = df[(df["parent_id"] != id_komentar) | (df["id"] == id_komentar)] # Ini akan menyaring balasan
    df.to_csv(FORUM_FILE, index=False)

# === HALAMAN GURU: LIHAT, BALAS, EDIT (HAPUS) KOMENTAR ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Forum Diskusi Dinamika Rotasi")

    # Muat data forum
    df = muat_forum()

    # Filter hanya komentar dari siswa (opsional, bisa ditampilkan semua)
    df_siswa = df[df["role"] == "siswa"]
    df_guru = df[df["role"] == "guru"]
    df_admin = df[df["role"] == "admin"]

    st.subheader("📂 Daftar Komentar Forum")
    if df.empty:
        st.info("Belum ada komentar di forum.")
    else:
        # Tampilkan komentar utama (parent_id = -1) dan balasan
        komentar_utama = df[df["parent_id"] == -1].sort_values("id", ascending=False)
        
        for _, row in komentar_utama.iterrows():
            # Tampilkan komentar utama
            st.markdown(f"**{row['nama']}** ({row['email']}) • _{row['waktu']}_")
            st.write(row["pesan"])
            
            # Tombol hapus (hanya untuk guru/admin)
            if st.session_state.role in ["guru", "admin"]:
                if st.button(f"🗑️ Hapus Komentar #{row['id']}", key=f"hapus_{row['id']}"):
                    hapus_komentar(row["id"])
                    st.rerun()

            # Form balas komentar
            with st.form(f"form_balas_{row['id']}"):
                balasan = st.text_area(f"Balas komentar ini:", max_chars=500, key=f"balas_ta_{row['id']}")
                kirim_balas = st.form_submit_button("📤 Kirim Balasan", key=f"balas_btn_{row['id']}")

            if kirim_balas and balasan.strip():
                simpan_komentar_baru(balasan, parent_id=row["id"])
                st.success("✅ Balasan berhasil dikirim!")
                st.rerun()

            # Tampilkan balasan (jika ada)
            balasan_df = df[df["parent_id"] == row["id"]]
            if not balasan_df.empty:
                for _, reply in balasan_df.iterrows():
                    st.markdown(f"↳ **{reply['nama']}** ({reply['email']}) • _{reply['waktu']}_")
                    st.write(reply["pesan"])
                    
                    # Tombol hapus balasan (hanya untuk guru/admin)
                    if st.session_state.role in ["guru", "admin"]:
                        if st.button(f"🗑️ Hapus Balasan #{reply['id']}", key=f"hapus_reply_{reply['id']}"):
                            hapus_komentar(reply["id"])
                            st.rerun()
                    st.divider()
            
            st.divider()

# === HALAMAN SISWA: KIRIM & BALAS KOMENTAR ===
def siswa_page():
    st.header("💬 Forum Diskusi: Dinamika Rotasi")

    # Form untuk mengirim komentar baru
    with st.form("form_komentar_baru"):
        pesan_baru = st.text_area("Tulis komentar Anda (maks. 500 karakter):", max_chars=500)
        kirim = st.form_submit_button("📤 Kirim Komentar")

    if kirim and pesan_baru.strip():
        simpan_komentar_baru(pesan_baru)
        st.success("✅ Komentar berhasil dikirim!")
        st.rerun()

    st.divider()
    st.subheader("📜 Riwayat Diskusi")

    # Muat data forum
    df = muat_forum()
    if df.empty:
        st.info("Belum ada diskusi. Jadilah yang pertama mengirim pesan!")
    else:
        # Tampilkan komentar utama (parent_id = -1) dan balasan
        komentar_utama = df[df["parent_id"] == -1].sort_values("id", ascending=False)
        
        for _, row in komentar_utama.iterrows():
            # Tampilkan komentar utama
            st.markdown(f"**{row['nama']}** ({row['email']}) • _{row['waktu']}_")
            st.write(row["pesan"])

            # Form balas komentar
            with st.form(f"form_balas_{row['id']}"):
                balasan = st.text_area(f"Balas komentar ini:", max_chars=500, key=f"balas_ta_{row['id']}")
                kirim_balas = st.form_submit_button("📤 Kirim Balasan", key=f"balas_btn_{row['id']}")

            if kirim_balas and balasan.strip():
                simpan_komentar_baru(balasan, parent_id=row["id"])
                st.success("✅ Balasan berhasil dikirim!")
                st.rerun()

            # Tampilkan balasan (jika ada)
            balasan_df = df[df["parent_id"] == row["id"]]
            if not balasan_df.empty:
                for _, reply in balasan_df.iterrows():
                    st.markdown(f"↳ **{reply['nama']}** ({reply['email']}) • _{reply['waktu']}_")
                    st.write(reply["pesan"])
                    st.divider()
            
            st.divider()

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