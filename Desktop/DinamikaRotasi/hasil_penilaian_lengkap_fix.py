# hasil_penilaian_dinamika_rotasi_final.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="Hasil Penilaian - Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
LKPD_DATA_FILE = "data_lkpd.csv"
REFLEKSI_DATA_FILE = "data_refleksi.json"
POST_TEST_DATA_FILE = "data_asesmen.csv"
NILAI_AKHIR_FILE = "nilai_akhir_siswa.csv"

# Inisialisasi file data jawaban siswa jika belum ada
if not os.path.exists(LKPD_DATA_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "kelompok", "tabel_pengamatan_json",
        "analisis_q1", "analisis_q2", "analisis_q3",
        "kesimpulan", "waktu_kumpul", "role"
    ]).to_csv(LKPD_DATA_FILE, index=False)

if not os.path.exists(REFLEKSI_DATA_FILE):
    with open(REFLEKSI_DATA_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(POST_TEST_DATA_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "jawaban_json", "nilai_total", "waktu_kerja", "role"
    ]).to_csv(POST_TEST_DATA_FILE, index=False)

if not os.path.exists(NILAI_AKHIR_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "nilai_lkpd", "nilai_refleksi", "nilai_post_test", "nilai_akhir", "waktu_update", "role"
    ]).to_csv(NILAI_AKHIR_FILE, index=False)

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
    # JANGAN GUNAKAN st.set_page_config() DI SINI!
    st.title("🔐 Login Hasil Penilaian")
    email = st.text_input("📧 Masukkan Email Anda:")

    if email:
        if email == "guru@dinamikarotasi.sch.id":
            password = st.text_input("🔑 Password Guru", type="password")
            if st.button("Login sebagai Guru"):
                if password == "guru123":
                    st.session_state.role = "guru"
                    st.session_state.current_user = "Guru"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Password salah!")
        elif email == "admin@dinamikarotasi.sch.id":
            password = st.text_input("🔑 Password Admin", type="password")
            if st.button("Login sebagai Admin"):
                if password == "admin123":
                    st.session_state.role = "admin"
                    st.session_state.current_user = "Admin"
                    st.session_state.current_email = email
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Password salah!")
        else:
            if st.button("Login sebagai Siswa"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title()
                st.session_state.current_email = email
                st.session_state.logged_in = True
                st.rerun()

# === FUNGSI PEMBANTU ===
def muat_data_lkpd():
    """Muat data jawaban LKPD siswa dari file CSV."""
    if os.path.exists(LKPD_DATA_FILE):
        try:
            return pd.read_csv(LKPD_DATA_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    df_kosong = pd.DataFrame(columns=[
        "email", "nama", "kelompok", "tabel_pengamatan_json",
        "analisis_q1", "analisis_q2", "analisis_q3",
        "kesimpulan", "waktu_kumpul", "role"
    ])
    df_kosong.to_csv(LKPD_DATA_FILE, index=False)
    return df_kosong

def muat_data_refleksi():
    """Muat data jawaban refleksi siswa dari file JSON."""
    if os.path.exists(REFLEKSI_DATA_FILE):
        try:
            with open(REFLEKSI_DATA_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    data_kosong = []
    with open(REFLEKSI_DATA_FILE, "w") as f:
        json.dump(data_kosong, f)
    return data_kosong

def muat_data_post_test():
    """Muat data jawaban post-test siswa dari file CSV."""
    if os.path.exists(POST_TEST_DATA_FILE):
        try:
            return pd.read_csv(POST_TEST_DATA_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    df_kosong = pd.DataFrame(columns=[
        "email", "nama", "jawaban_json", "nilai_total", "waktu_kerja", "role"
    ])
    df_kosong.to_csv(POST_TEST_DATA_FILE, index=False)
    return df_kosong

def muat_nilai_akhir():
    """Muat data nilai akhir siswa dari file CSV."""
    if os.path.exists(NILAI_AKHIR_FILE):
        try:
            return pd.read_csv(NILAI_AKHIR_FILE)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    df_kosong = pd.DataFrame(columns=[
        "email", "nama", "nilai_lkpd", "nilai_refleksi", "nilai_post_test", "nilai_akhir", "waktu_update", "role"
    ])
    df_kosong.to_csv(NILAI_AKHIR_FILE, index=False)
    return df_kosong

# === HALAMAN GURU ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: Hasil Penilaian Dinamika Rotasi")
    
    # Muat semua data
    df_lkpd = muat_data_lkpd()
    df_refleksi = muat_data_refleksi()
    df_post_test = muat_data_post_test()
    df_nilai = muat_nilai_akhir()

    # Filter hanya jawaban siswa
    df_lkpd_siswa = df_lkpd[df_lkpd["role"] == "siswa"]
    df_post_test_siswa = df_post_test[df_post_test["role"] == "siswa"]
    df_nilai_siswa = df_nilai[df_nilai["role"] == "siswa"]

    # Tab untuk Lihat Data Siswa
    tab_lkpd, tab_refleksi, tab_post_test, tab_nilai = st.tabs([
        "📄 LKPD Siswa", "💭 Refleksi Siswa", "📝 Post-test Siswa", "📊 Nilai Akhir Siswa"
    ])

    # --- TAB 1: LKPD Siswa ---
    with tab_lkpd:
        st.header("📄 LKPD Siswa")
        if df_lkpd_siswa.empty:
            st.info("Belum ada siswa yang mengumpulkan LKPD.")
        else:
            # Tampilkan daftar siswa yang mengumpulkan
            st.subheader("📋 Daftar Siswa yang Mengumpulkan LKPD")
            st.dataframe(df_lkpd_siswa[["nama", "email", "kelompok", "waktu_kumpul"]].sort_values(by="waktu_kumpul", ascending=False))

            # Detail jawaban siswa tertentu
            st.divider()
            st.subheader("🔍 Lihat Jawaban Lengkap Siswa")
            emails_unik = df_lkpd_siswa["email"].unique()
            email_pilihan = st.selectbox("Pilih Email Siswa:", ["Pilih..."] + list(emails_unik))

            if email_pilihan != "Pilih...":
                # Ambil jawaban terakhir dari email yang dipilih
                df_pilihan = df_lkpd_siswa[df_lkpd_siswa["email"] == email_pilihan].iloc[-1]
                st.write(f"**Nama:** {df_pilihan['nama']}")
                st.write(f"**Kelompok:** {df_pilihan['kelompok']}")
                st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kumpul']}")

                # Tampilkan Tabel Pengamatan
                st.markdown("#### 📊 Tabel Hasil Pengamatan")
                try:
                    tabel_data = json.loads(df_pilihan['tabel_pengamatan_json'])
                    df_tabel = pd.DataFrame(tabel_data)
                    st.dataframe(df_tabel)
                except Exception as e:
                    st.error(f"Error memuat tabel: {e}")

                # Tampilkan Analisis
                st.markdown("#### 🧠 Analisis Data dan Diskusi")
                st.write(f"**1.** {df_pilihan['analisis_q1']}")
                st.write(f"**2.** {df_pilihan['analisis_q2']}")
                st.write(f"**3.** {df_pilihan['analisis_q3']}")

                # Tampilkan Kesimpulan
                st.markdown("#### 🎯 Kesimpulan")
                st.write(df_pilihan['kesimpulan'])

    # --- TAB 2: Refleksi Siswa ---
    with tab_refleksi:
        st.header("💭 Refleksi Siswa")
        if not df_refleksi:
            st.info("Belum ada siswa yang mengisi refleksi.")
        else:
            # Tampilkan daftar siswa yang mengisi
            st.subheader("📋 Daftar Siswa yang Mengisi Refleksi")
            df_ref = pd.DataFrame(df_refleksi)
            df_ref_siswa = df_ref[df_ref["role"] == "siswa"]
            if df_ref_siswa.empty:
                st.info("Belum ada siswa yang mengisi refleksi.")
            else:
                st.dataframe(df_ref_siswa[["nama", "email", "waktu_kumpul"]].sort_values(by="waktu_kumpul", ascending=False))

                # Detail jawaban siswa tertentu
                st.divider()
                st.subheader("🔍 Lihat Jawaban Lengkap Siswa")
                emails_unik = df_ref_siswa["email"].unique()
                email_pilihan = st.selectbox("Pilih Email Siswa (Refleksi):", ["Pilih..."] + list(emails_unik))

                if email_pilihan != "Pilih...":
                    # Ambil jawaban terakhir dari email yang dipilih
                    df_pilihan = df_ref_siswa[df_ref_siswa["email"] == email_pilihan].iloc[-1]
                    st.write(f"**Nama:** {df_pilihan['nama']}")
                    st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kumpul']}")

                    # Tampilkan jawaban
                    st.markdown("#### Jawaban Refleksi:")
                    try:
                        jawaban_list = df_pilihan['jawaban_json']
                        for i, jawaban in enumerate(jawaban_list, 1):
                            st.write(f"**{i}.** {jawaban}")
                            st.divider()
                    except Exception as e:
                        st.error(f"Error memuat jawaban refleksi: {e}")

    # --- TAB 3: Post-test Siswa ---
    with tab_post_test:
        st.header("📝 Post-test Siswa")
        if df_post_test_siswa.empty:
            st.info("Belum ada siswa yang mengerjakan post-test.")
        else:
            # Tampilkan daftar siswa yang mengerjakan
            st.subheader("📋 Daftar Siswa yang Mengerjakan Post-test")
            st.dataframe(df_post_test_siswa[["nama", "email", "nilai_total", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))

            # Detail jawaban siswa tertentu
            st.divider()
            st.subheader("🔍 Lihat Jawaban Lengkap Siswa")
            emails_unik = df_post_test_siswa["email"].unique()
            email_pilihan = st.selectbox("Pilih Email Siswa (Post-test):", ["Pilih..."] + list(emails_unik))

            if email_pilihan != "Pilih...":
                # Ambil jawaban terakhir dari email yang dipilih
                df_pilihan = df_post_test_siswa[df_post_test_siswa["email"] == email_pilihan].iloc[-1]
                st.write(f"**Nama:** {df_pilihan['nama']}")
                st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kerja']}")
                st.write(f"**Nilai Total:** {df_pilihan['nilai_total']}")

                # Tampilkan jawaban
                st.markdown("#### Jawaban Post-test:")
                try:
                    jawaban_dict = json.loads(df_pilihan['jawaban_json'])
                    for soal_id, jawaban in jawaban_dict.items():
                        st.write(f"**Soal {soal_id.split('_')[-1][1:]}:** {jawaban}")
                        st.divider()
                except Exception as e:
                    st.error(f"Error memuat jawaban post-test: {e}")

    # --- TAB 4: Nilai Akhir Siswa ---
    with tab_nilai:
        st.header("📊 Nilai Akhir Siswa")
        if df_nilai_siswa.empty:
            st.info("Belum ada nilai akhir yang dihitung.")
        else:
            # Tampilkan daftar nilai akhir
            st.subheader("📋 Daftar Nilai Akhir Siswa")
            st.dataframe(df_nilai_siswa[["nama", "email", "nilai_lkpd", "nilai_refleksi", "nilai_post_test", "nilai_akhir", "waktu_update"]].sort_values(by="nilai_akhir", ascending=False))

            # Statistik singkat
            st.divider()
            st.subheader("📈 Statistik Nilai")
            avg_nilai = df_nilai_siswa["nilai_akhir"].mean()
            max_nilai = df_nilai_siswa["nilai_akhir"].max()
            min_nilai = df_nilai_siswa["nilai_akhir"].min()
            st.metric("Rata-rata Nilai Akhir", f"{avg_nilai:.2f}")
            st.metric("Nilai Tertinggi", f"{max_nilai:.2f}")
            st.metric("Nilai Terendah", f"{min_nilai:.2f}")

# === HALAMAN SISWA ===
def siswa_page():
    st.header("📊 Hasil Penilaian Anda: Dinamika Rotasi")

    # Muat semua data
    df_lkpd = muat_data_lkpd()
    df_refleksi = muat_data_refleksi()
    df_post_test = muat_data_post_test()
    df_nilai = muat_nilai_akhir()

    # Filter hanya jawaban milik siswa ini
    email_siswa = st.session_state.current_email
    nama_siswa = st.session_state.current_user

    df_lkpd_siswa_ini = df_lkpd[
        (df_lkpd["email"] == email_siswa) & (df_lkpd["role"] == "siswa")
    ]
    df_post_test_siswa_ini = df_post_test[
        (df_post_test["email"] == email_siswa) & (df_post_test["role"] == "siswa")
    ]
    df_nilai_siswa_ini = df_nilai[
        (df_nilai["email"] == email_siswa) & (df_nilai["role"] == "siswa")
    ]

    st.header(f"👤 **{nama_siswa}** ({email_siswa})")

    # Tab untuk Lihat Nilai & Jawaban Sendiri
    tab_lkpd, tab_refleksi, tab_post_test, tab_nilai = st.tabs([
        "📄 LKPD Saya", "💭 Refleksi Saya", "📝 Post-test Saya", "📊 Nilai Saya"
    ])

    # --- TAB 1: LKPD Saya ---
    with tab_lkpd:
        st.header("📄 LKPD Saya")
        if df_lkpd_siswa_ini.empty:
            st.info("Anda belum mengumpulkan LKPD.")
        else:
            # Ambil jawaban terakhir
            df_pilihan = df_lkpd_siswa_ini.iloc[-1]
            st.write(f"**Kelompok:** {df_pilihan['kelompok']}")
            st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kumpul']}")

            # Tampilkan Tabel Pengamatan
            st.markdown("#### 📊 Tabel Hasil Pengamatan")
            try:
                tabel_data = json.loads(df_pilihan['tabel_pengamatan_json'])
                df_tabel = pd.DataFrame(tabel_data)
                st.dataframe(df_tabel)
            except Exception as e:
                st.error(f"Error memuat tabel: {e}")

            # Tampilkan Analisis
            st.markdown("#### 🧠 Analisis Data dan Diskusi")
            st.write(f"**1.** {df_pilihan['analisis_q1']}")
            st.write(f"**2.** {df_pilihan['analisis_q2']}")
            st.write(f"**3.** {df_pilihan['analisis_q3']}")

            # Tampilkan Kesimpulan
            st.markdown("#### 🎯 Kesimpulan")
            st.write(df_pilihan['kesimpulan'])

    # --- TAB 2: Refleksi Saya ---
    with tab_refleksi:
        st.header("💭 Refleksi Saya")
        # Filter jawaban refleksi milik siswa ini
        jawaban_siswa_ini = [
            entry for entry in df_refleksi 
            if entry.get("email") == email_siswa and entry.get("role") == "siswa"
        ]
        if not jawaban_siswa_ini:
            st.info("Anda belum mengisi refleksi.")
        else:
            # Ambil jawaban terakhir
            df_pilihan = jawaban_siswa_ini[-1]
            st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kumpul']}")

            # Tampilkan jawaban
            st.markdown("#### Jawaban Refleksi:")
            try:
                jawaban_list = df_pilihan['jawaban_json']
                for i, jawaban in enumerate(jawaban_list, 1):
                    st.write(f"**{i}.** {jawaban}")
                    st.divider()
            except Exception as e:
                st.error(f"Error memuat jawaban refleksi: {e}")

    # --- TAB 3: Post-test Saya ---
    with tab_post_test:
        st.header("📝 Post-test Saya")
        if df_post_test_siswa_ini.empty:
            st.info("Anda belum mengerjakan post-test.")
        else:
            # Ambil jawaban terakhir
            df_pilihan = df_post_test_siswa_ini.iloc[-1]
            st.write(f"**Waktu Kumpul:** {df_pilihan['waktu_kerja']}")
            st.write(f"**Nilai Total:** {df_pilihan['nilai_total']}")

            # Tampilkan jawaban
            st.markdown("#### Jawaban Post-test:")
            try:
                jawaban_dict = json.loads(df_pilihan['jawaban_json'])
                for soal_id, jawaban in jawaban_dict.items():
                    st.write(f"**Soal {soal_id.split('_')[-1][1:]}:** {jawaban}")
                    st.divider()
            except Exception as e:
                st.error(f"Error memuat jawaban post-test: {e}")

    # --- TAB 4: Nilai Saya ---
    with tab_nilai:
        st.header("📊 Nilai Saya")
        if df_nilai_siswa_ini.empty:
            st.info("Nilai Anda belum dihitung oleh guru.")
        else:
            # Ambil nilai terakhir
            df_pilihan = df_nilai_siswa_ini.iloc[-1]
            st.write(f"**Waktu Update Nilai:** {df_pilihan['waktu_update']}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📄 Nilai LKPD", f"{df_pilihan['nilai_lkpd']:.2f}")
            with col2:
                st.metric("💭 Nilai Refleksi", f"{df_pilihan['nilai_refleksi']:.2f}")
            with col3:
                st.metric("📝 Nilai Post-test", f"{df_pilihan['nilai_post_test']:.2f}")
            with col4:
                st.metric("🏆 Nilai Akhir", f"{df_pilihan['nilai_akhir']:.2f}")

            # Deskripsi singkat berdasarkan nilai akhir
            nilai_akhir = df_pilihan['nilai_akhir']
            if nilai_akhir >= 85:
                st.balloons()
                st.success("🎉 Luar biasa! Pemahaman Anda sangat baik. Pertahankan semangat belajar!")
            elif nilai_akhir >= 75:
                st.info("👍 Bagus! Pemahaman Anda sudah cukup. Tingkatkan lagi untuk hasil yang lebih maksimal!")
            else:
                st.warning("📚 Hasil belajar Anda perlu ditingkatkan. Pelajari kembali materi dan jangan ragu bertanya!")

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