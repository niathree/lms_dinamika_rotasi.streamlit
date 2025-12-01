import streamlit as st
import json
import os
from datetime import datetime

# --- Konfigurasi awal ---
st.set_page_config(
    page_title="Forum Diskusi: Dinamika Rotasi",
    layout="wide"
)

# --- File konfigurasi ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

FORUM_FILE = os.path.join(DATA_DIR, "forum_diskusi.json")

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

# --- Fungsi muat dan simpan data forum ---
def muat_forum():
    if os.path.exists(FORUM_FILE):
        with open(FORUM_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    else:
        # Buat struktur data awal
        data_awal = {"topik": []}
        with open(FORUM_FILE, "w", encoding='utf-8') as f:
            json.dump(data_awal, f, indent=4, ensure_ascii=False)
        return data_awal

def simpan_forum(data_baru):
    with open(FORUM_FILE, "w", encoding='utf-8') as f:
        json.dump(data_baru, f, indent=4, ensure_ascii=False)

# === HALAMAN FORUM (GURU & SISWA) ===
def forum_page():
    st.header("💬 Forum Diskusi: Dinamika Rotasi")
    forum_data = muat_forum()

    # --- Form untuk membuat topik baru ---
    st.subheader("📝 Buat Topik Baru")
    with st.form("form_topik_baru"):
        judul_topik = st.text_input("Judul Topik")
        isi_topik = st.text_area("Isi Diskusi")
        kirim_topik = st.form_submit_button("Kirim Topik")

        if kirim_topik:
            if judul_topik and isi_topik:
                topik_baru = {
                    "id": len(forum_data["topik"]),
                    "judul": judul_topik,
                    "isi": isi_topik,
                    "author": st.session_state.current_user,
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "komentar": []
                }
                forum_data["topik"].append(topik_baru)
                simpan_forum(forum_data)
                st.success("✅ Topik berhasil dibuat!")
                st.rerun()
            else:
                st.error("❌ Judul dan isi topik harus diisi.")

    # --- Tampilkan daftar topik ---
    st.subheader("📋 Daftar Topik")
    if not forum_data["topik"]:
        st.info("Belum ada topik diskusi. Jadilah yang pertama untuk memulai!")
    else:
        for topik in forum_data["topik"]:
            st.markdown(f"### {topik['judul']}")
            st.caption(f"Oleh: {topik['author']} | {topik['waktu']}")
            st.write(topik['isi'])

            # --- Form komentar ---
            with st.expander("💬 Komentar", expanded=False):
                with st.form(f"form_komentar_{topik['id']}"):
                    isi_komentar = st.text_area(f"Tambahkan komentar untuk topik ini", key=f"isi_komen_{topik['id']}")
                    kirim_komentar = st.form_submit_button(f"Kirim Komentar")

                    if kirim_komentar:
                        if isi_komentar:
                            komentar_baru = {
                                "id": len(topik["komentar"]),
                                "isi": isi_komentar,
                                "author": st.session_state.current_user,
                                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "balasan": []
                            }
                            topik["komentar"].append(komentar_baru)
                            simpan_forum(forum_data)
                            st.success("✅ Komentar berhasil dikirim!")
                            st.rerun()
                        else:
                            st.error("❌ Komentar tidak boleh kosong.")

                # --- Tampilkan komentar ---
                for komentar in topik["komentar"]:
                    st.markdown(f"**{komentar['author']}** - {komentar['waktu']}")
                    st.write(komentar['isi'])

                    # --- Form balasan ---
                    with st.form(f"form_balasan_{topik['id']}_{komentar['id']}"):
                        isi_balasan = st.text_area(f"Balas komentar ini", key=f"isi_balas_{topik['id']}_{komentar['id']}")
                        kirim_balasan = st.form_submit_button(f"Kirim Balasan")

                        if kirim_balasan:
                            if isi_balasan:
                                balasan_baru = {
                                    "isi": isi_balasan,
                                    "author": st.session_state.current_user,
                                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                komentar["balasan"].append(balasan_baru)
                                simpan_forum(forum_data)
                                st.success("✅ Balasan berhasil dikirim!")
                                st.rerun()
                            else:
                                st.error("❌ Balasan tidak boleh kosong.")

                    # --- Tampilkan balasan ---
                    for balasan in komentar["balasan"]:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;└ **{balasan['author']}** - {balasan['waktu']}")
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;└ {balasan['isi']}")

            st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.current_email = ""
        st.rerun()

# === MAIN ===
if not st.session_state.logged_in:
    login()
else:
    forum_page()