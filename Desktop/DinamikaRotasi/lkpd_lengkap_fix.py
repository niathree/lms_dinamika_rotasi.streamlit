# lkpd_dinamika_rotasi_v3.py
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI AWAL (Harus di awal sekali) ===
st.set_page_config(page_title="LKPD Dinamika Rotasi", layout="wide")

# --- KONSTANTA ---
LKPD_INFO_FILE = "lkpd_info_v3.json" # File untuk menyimpan soal LKPD dan kunci jawaban
LKPD_DATA_FILE = "lkpd_data_siswa_v3.csv" # File untuk menyimpan jawaban siswa
GURU_KUNCI_PASSWORD = "kunci123" # Password untuk melihat kunci jawaban

# Inisialisasi file LKPD jika belum ada
# Data diambil dari LKPD DINAMIKA ROTASI revisi.pdf dan modul terkait
if not os.path.exists(LKPD_INFO_FILE):
    default_lkpd = {
        "judul": "LKPD: Dinamika Rotasi - Analisis Torsi dan Durasi Putaran Gasing",
        "tujuan": [
            "Peserta didik mampu menganalisis hubungan antara gaya, lengan gaya, dan torsi dalam gerak rotasi menggunakan model gasing.",
            "Peserta didik mampu mengevaluasi hasil percobaan rotasi gasing untuk menentukan faktor-faktor yang mempengaruhi durasi dan kecepatan putaran.",
            "Peserta didik mampu menyajikan data dalam bentuk laporan praktikum dan mempresentasikan di depan kelas."
        ],
        "dasar_teori": "Momen gaya atau dikenal sebagai torsi (τ), adalah besaran vektor yang menggerakkan suatu benda tegar untuk berotasi atau berputar terhadap suatu poros tertentu. Rumus torsi: τ = r × F × sin(θ), dengan r adalah lengan gaya, F adalah besar gaya, dan θ adalah sudut antara vektor gaya dan lengan momen. Momen inersia (I) adalah ukuran kelembaman suatu benda terhadap perubahan keadaan rotasinya.",
        "petunjuk": [
            "Perhatikan simulasi yang sudah dilakukan dalam pembelajaran.",
            "Lakukan simulasi sesuai langkah kerja!",
            "Jawablah pertanyaan-pertanyaan yang terdapat di LKPD ini secara berkelompok."
        ],
        "alat_bahan": [
            "1 buah gasing (bisa dibuat dari CD bekas, tutup botol)",
            "Stopwatch",
            "Penggaris atau meteran",
            "Tali (untuk memutar gasing)",
            "Buku catatan"
        ],
        "langkah_kerja": [
            "Rakit atau siapkan gasing (misalnya gasing dari CD bekas atau tutup botol).",
            "Tentukan titik pusat poros gasing dan ukur panjang tali yang digunakan untuk memutar gasing.",
            "Buat hipotesis: “Semakin besar gaya yang diberikan saat memutar gasing, maka semakin lama gasing berputar”.",
            "Ukur panjang lengan gaya (jarak dari pusat poros ke titik gaya) untuk setiap percobaan.",
            "Putar gasing dengan tiga variasi gaya (lemah, sedang, kuat).",
            "Catat lama waktu putaran dengan stopwatch dari awal hingga berhenti.",
            "Lakukan setiap variasi gaya sebanyak 3 kali."
        ],
        "tabel_header": ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"],
        "analisis_pertanyaan": [
            "Berdasarkan data waktu putar dari masing-masing gaya (lemah, sedang, kuat), bagaimana pengaruh besar gaya terhadap torsi dan durasi putaran gasing?",
            "Hitung dan bandingkan nilai torsi relatif dari setiap gaya yang digunakan pada percobaan. Apakah data tersebut konsisten atau relevan dengan teori bahwa torsi berbanding lurus dengan gaya?",
            "Dari hasil percobaan, gasing yang ditarik dengan gaya lebih besar dapat mencapai putaran awal yang lebih cepat dan berputar lebih lama. Jelaskan bagaimana fenomena ini terjadi berdasarkan prinsip torsi dalam sistem rotasi!"
        ],
        "kunci_jawaban_analisis": {
            "q1": "Pengaruh gaya terhadap torsi dan durasi putaran: Semakin besar gaya yang diberikan, semakin besar torsi yang dihasilkan, sehingga gasing berputar lebih cepat dan berlangsung lebih lama.",
            "q2": "Perbandingan torsi relatif: Jika jarak lengan gaya tetap, torsi berbanding lurus dengan besar gaya. Data menunjukkan torsi meningkat seiring peningkatan gaya (lemah < sedang < kuat), yang konsisten dengan teori τ=r⋅F .",
            "q3": "Penjelasan fenomena: Gaya yang lebih besar menghasilkan torsi lebih besar, memberikan percepatan sudut awal lebih tinggi. Akibatnya, gasing mencapai kecepatan sudut awal lebih besar, sehingga energi kinetik rotasinya lebih besar dan memerlukan waktu lebih lama untuk berhenti akibat gesekan."
        },
        "kesimpulan_petunjuk": "Tulis kesimpulan kelompok Anda berdasarkan percobaan dan analisis di atas:",
        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(LKPD_INFO_FILE, "w", encoding='utf-8') as f:
        json.dump(default_lkpd, f, indent=4, ensure_ascii=False)

# Inisialisasi file data jawaban siswa jika belum ada
if not os.path.exists(LKPD_DATA_FILE):
    pd.DataFrame(columns=[
        "email", "nama", "kelompok", "tabel_pengamatan_json",
        "analisis_q1", "analisis_q2", "analisis_q3",
        "kesimpulan", "waktu_kumpul", "role"
    ]).to_csv(LKPD_DATA_FILE, index=False)

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
    st.title("🔐 Login LKPD")
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
def muat_lkpd():
    """Muat data LKPD dari file JSON."""
    if os.path.exists(LKPD_INFO_FILE):
        with open(LKPD_INFO_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    return None

def simpan_lkpd(data):
    """Simpan data LKPD ke file JSON."""
    with open(LKPD_INFO_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def muat_jawaban():
    """Muat jawaban siswa dari file CSV."""
    if os.path.exists(LKPD_DATA_FILE):
        try:
            return pd.read_csv(LKPD_DATA_FILE)
        except pd.errors.EmptyDataError:
            pass
    # Buat dataframe kosong jika file tidak ada atau kosong
    df_kosong = pd.DataFrame(columns=[
        "email", "nama", "kelompok", "tabel_pengamatan_json",
        "analisis_q1", "analisis_q2", "analisis_q3",
        "kesimpulan", "waktu_kumpul", "role"
    ])
    df_kosong.to_csv(LKPD_DATA_FILE, index=False)
    return df_kosong

def simpan_jawaban_baru(jawaban_dict):
    """Simpan jawaban baru siswa ke file CSV."""
    df = muat_jawaban()
    # Konversi tabel pengamatan ke string JSON
    tabel_json_str = json.dumps(jawaban_dict.get("tabel_pengamatan", []))
    new_entry = pd.DataFrame([{
        "email": st.session_state.current_email,
        "nama": jawaban_dict.get("nama", ""),
        "kelompok": jawaban_dict.get("kelompok", ""),
        "tabel_pengamatan_json": tabel_json_str,
        "analisis_q1": jawaban_dict.get("analisis_q1", ""),
        "analisis_q2": jawaban_dict.get("analisis_q2", ""),
        "analisis_q3": jawaban_dict.get("analisis_q3", ""),
        "kesimpulan": jawaban_dict.get("kesimpulan", ""),
        "waktu_kumpul": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": "siswa"
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LKPD_DATA_FILE, index=False)

# === HALAMAN GURU: EDIT SOAL LKPD & LIHAT KUNCI JAWABAN ===
def guru_page():
    st.header("👩‍🏫 Dasbor Guru: LKPD Dinamika Rotasi")

    # Muat data LKPD
    data_lkpd = muat_lkpd()
    if not data_lkpd:
        st.error("File LKPD tidak ditemukan atau rusak.")
        return

    tab_edit, tab_hasil = st.tabs(["📝 Edit Soal LKPD", "📂 Lihat Hasil & Kunci Jawaban"])

    # --- TAB 1: Edit Soal LKPD ---
    with tab_edit:
        st.subheader("📝 Edit Isi LKPD")

        # Judul LKPD
        judul_baru = st.text_input("📄 Judul LKPD", value=data_lkpd.get("judul", ""))
        
        # Tujuan
        st.subheader("🎯 Tujuan Pembelajaran")
        tujuan_list = data_lkpd.get("tujuan", [])
        tujuan_text = "\n".join(tujuan_list)
        tujuan_baru = st.text_area("Tujuan (pisahkan dengan baris baru)", value=tujuan_text, height=150)

        # Dasar Teori
        st.subheader("📚 Dasar Teori")
        teori_baru = st.text_area("Dasar Teori", value=data_lkpd.get("dasar_teori", ""), height=200)

        # Petunjuk
        st.subheader("📋 Petunjuk Pengerjaan")
        petunjuk_list = data_lkpd.get("petunjuk", [])
        petunjuk_text = "\n".join(petunjuk_list)
        petunjuk_baru = st.text_area("Petunjuk (pisahkan dengan baris baru)", value=petunjuk_text, height=150)

        # Alat dan Bahan
        st.subheader("🛠️ Alat dan Bahan")
        alat_list = data_lkpd.get("alat_bahan", [])
        alat_text = "\n".join(alat_list)
        alat_baru = st.text_area("Alat dan Bahan (pisahkan dengan baris baru)", value=alat_text, height=150)

        # Langkah Kerja
        st.subheader("👣 Langkah Kerja")
        langkah_list = data_lkpd.get("langkah_kerja", [])
        langkah_text = "\n".join(langkah_list)
        langkah_baru = st.text_area("Langkah Kerja (pisahkan dengan baris baru)", value=langkah_text, height=200)

        # Tabel Hasil Pengamatan
        st.subheader("📊 Tabel Hasil Pengamatan")
        header_lama = data_lkpd.get("tabel_header", [])
        header_baru_list = []
        cols_header = st.columns(len(header_lama))
        for i, col in enumerate(cols_header):
            if i < len(header_lama):
                val = header_lama[i]
            else:
                val = f"Kolom {i+1}"
            header_val = col.text_input(f"Header {i+1}", value=val, key=f"header_{i}")
            header_baru_list.append(header_val)

        # Pertanyaan Analisis Data
        st.subheader("🧠 Pertanyaan Analisis Data dan Diskusi")
        analisis_list = data_lkpd.get("analisis_pertanyaan", [])
        analisis_baru_list = []
        for i, q in enumerate(analisis_list):
            q_baru = st.text_area(f"Pertanyaan {i+1}", value=q, key=f"analisis_q_{i}")
            analisis_baru_list.append(q_baru)

        # Petunjuk Kesimpulan
        st.subheader("🎯 Petunjuk untuk Menulis Kesimpulan")
        kesimpulan_baru = st.text_area("Petunjuk Kesimpulan", value=data_lkpd.get("kesimpulan_petunjuk", ""), height=100)

        # Tombol Simpan
        if st.button("💾 Simpan Seluruh Perubahan LKPD"):
            data_baru = {
                "judul": judul_baru,
                "tujuan": [item.strip() for item in tujuan_baru.split("\n") if item.strip()],
                "dasar_teori": teori_baru,
                "petunjuk": [item.strip() for item in petunjuk_baru.split("\n") if item.strip()],
                "alat_bahan": [item.strip() for item in alat_baru.split("\n") if item.strip()],
                "langkah_kerja": [item.strip() for item in langkah_baru.split("\n") if item.strip()],
                "tabel_header": header_baru_list,
                "analisis_pertanyaan": analisis_baru_list,
                "kunci_jawaban_analisis": data_lkpd.get("kunci_jawaban_analisis", {}),
                "kesimpulan_petunjuk": kesimpulan_baru,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_lkpd(data_baru)
            st.success("✅ Seluruh LKPD berhasil diperbarui!")

    # --- TAB 2: Lihat Hasil Siswa & Kunci Jawaban ---
    with tab_hasil:
        st.subheader("📂 Lihat Hasil LKPD Siswa")
        df_jawaban = muat_jawaban()
        df_siswa = df_jawaban[df_jawaban["role"] == "siswa"]

        if df_siswa.empty:
            st.info("Belum ada siswa yang mengerjakan LKPD.")
        else:
            # Tampilkan daftar siswa yang mengumpulkan
            st.dataframe(df_siswa[["nama", "email", "kelompok", "waktu_kumpul"]].sort_values(by="waktu_kumpul", ascending=False))

            # Detail jawaban siswa tertentu
            st.divider()
            st.subheader("🔍 Lihat Jawaban Lengkap Siswa")
            emails_unik = df_siswa["email"].unique()
            email_pilihan = st.selectbox("Pilih Email Siswa:", ["Pilih..."] + list(emails_unik))

            if email_pilihan != "Pilih...":
                # Ambil jawaban terakhir dari email yang dipilih
                jawaban_siswa = df_siswa[df_siswa["email"] == email_pilihan].iloc[-1]
                st.write(f"**Nama:** {jawaban_siswa['nama']}")
                st.write(f"**Kelompok:** {jawaban_siswa['kelompok']}")
                st.write(f"**Waktu Kumpul:** {jawaban_siswa['waktu_kumpul']}")

                # Tampilkan Tabel Pengamatan
                st.markdown("#### 📊 Tabel Hasil Pengamatan")
                try:
                    tabel_data = json.loads(jawaban_siswa['tabel_pengamatan_json'])
                    df_tabel = pd.DataFrame(tabel_data)
                    st.dataframe(df_tabel)
                except Exception as e:
                    st.error(f"Error memuat tabel: {e}")

                # Tampilkan Analisis Data dan Diskusi
                st.markdown("#### 🧠 Analisis Data dan Diskusi")
                for i, q in enumerate(data_lkpd.get("analisis_pertanyaan", []), 1):
                    st.markdown(f"**{i}. {q}**")
                    jawaban_key = f"analisis_q{i}"
                    st.write(jawaban_siswa.get(jawaban_key, "_Tidak dijawab_"))
                    st.divider()

                # Tampilkan Kesimpulan
                st.markdown("#### 🎯 Kesimpulan")
                st.write(jawaban_siswa.get("kesimpulan", "_Tidak diisi_"))

        # --- KUNCI JAWABAN ANALISIS DATA (RAHASIA UNTUK GURU) ---
        st.divider()
        st.subheader("🔒 Kunci Jawaban Analisis Data LKPD (Hanya untuk Guru)")
        pwd = st.text_input("Masukkan password untuk melihat kunci jawaban:", type="password")
        if pwd == GURU_KUNCI_PASSWORD:
            st.success("✅ Akses kunci jawaban diberikan.")
            kunci = data_lkpd.get("kunci_jawaban_analisis", {})
            st.markdown("#### Kunci Jawaban:")
            for i, q in enumerate(data_lkpd.get("analisis_pertanyaan", []), 1):
                st.markdown(f"**{i}. {q}**")
                kunci_key = f"q{i}"
                st.write(f"**Jawaban Guru:** {kunci.get(kunci_key, '_Belum diisi_')}")
                st.divider()
        elif pwd:
            st.error("❌ Password salah.")

        # Form untuk mengedit kunci jawaban
        st.subheader("✏️ Edit Kunci Jawaban Analisis Data (Guru)")
        kunci_lama = data_lkpd.get("kunci_jawaban_analisis", {})
        kunci_baru = {}
        for i, q in enumerate(data_lkpd.get("analisis_pertanyaan", []), 1):
            kunci_key = f"q{i}"
            kunci_baru[kunci_key] = st.text_area(f"Kunci Jawaban untuk Pertanyaan {i}", value=kunci_lama.get(kunci_key, ""), key=f"kunci_{i}")

        if st.button("💾 Simpan Kunci Jawaban"):
            data_lkpd["kunci_jawaban_analisis"] = kunci_baru
            simpan_lkpd(data_lkpd)
            st.success("✅ Kunci jawaban analisis LKPD berhasil disimpan!")

# === HALAMAN SISWA: MENGERJAKAN LKPD ===
def siswa_page():
    st.header("📝 LKPD: Dinamika Rotasi")

    # Muat data LKPD
    data_lkpd = muat_lkpd()
    if not data_lkpd:
        st.error("LKPD belum diatur oleh guru.")
        return

    st.subheader(data_lkpd.get("judul", "LKPD Dinamika Rotasi"))
    
    # Tampilkan bagian LKPD (tanpa kunci jawaban)
    st.markdown("### 🎯 Tujuan Pembelajaran")
    for i, t in enumerate(data_lkpd.get("tujuan", []), 1):
        st.write(f"{i}. {t}")

    st.markdown("### 📚 Dasar Teori")
    st.write(data_lkpd.get("dasar_teori", ""))

    st.markdown("### 📋 Petunjuk Pengerjaan")
    for i, p in enumerate(data_lkpd.get("petunjuk", []), 1):
        st.write(f"{i}. {p}")

    st.markdown("### 🛠️ Alat dan Bahan")
    for a in data_lkpd.get("alat_bahan", []):
        st.write(f"- {a}")

    st.markdown("### 👣 Langkah Kerja")
    for i, l in enumerate(data_lkpd.get("langkah_kerja", []), 1):
        st.write(f"{i}. {l}")

    st.divider()

    # Formulir Pengisian Jawaban Siswa
    st.subheader("✍️ Isi Jawaban LKPD")

    # Informasi siswa
    nama = st.text_input("Nama Anggota Kelompok:", value=st.session_state.current_user)
    kelompok = st.text_input("Nama Kelompok:")

    # Tabel Hasil Pengamatan
    st.markdown("### 📊 Tabel Hasil Pengamatan")
    header_list = data_lkpd.get("tabel_header", ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"])
    tabel_data = []
    for i in range(3): # Misalnya 3 baris untuk 3 variasi gaya
        cols = st.columns(len(header_list))
        baris_data = {}
        for j, header in enumerate(header_list):
            with cols[j]:
                if j == 0: # Kolom No.
                    st.write(f"**{i+1}**")
                    baris_data[header] = str(i+1)
                else:
                    nilai = st.text_input("", key=f"tabel_{i}_{j}")
                    baris_data[header] = nilai
        tabel_data.append(baris_data)

    # Pertanyaan Analisis Data dan Diskusi
    st.markdown("### 🧠 Analisis Data dan Diskusi")
    jawaban_analisis = {}
    for i, q in enumerate(data_lkpd.get("analisis_pertanyaan", []), 1):
        st.markdown(f"**{i}. {q}**")
        jawaban_key = f"analisis_q{i}"
        jawaban = st.text_area("Jawaban Anda:", key=jawaban_key, height=100)
        jawaban_analisis[jawaban_key] = jawaban

    # Kesimpulan
    st.markdown("### 🎯 Kesimpulan")
    kesimpulan = st.text_area(data_lkpd.get("kesimpulan_petunjuk", "Tulis kesimpulan kelompok Anda:"), height=150)

    # Tombol Simpan
    if st.button("✅ Simpan Jawaban LKPD"):
        if not nama.strip() or not kelompok.strip():
            st.error("Nama dan Kelompok tidak boleh kosong!")
        elif any(not v.strip() for v in jawaban_analisis.values()) or not kesimpulan.strip():
            st.error("Mohon jawab semua pertanyaan dan isi kesimpulan!")
        else:
            jawaban_dict = {
                "nama": nama.strip(),
                "kelompok": kelompok.strip(),
                "tabel_pengamatan": tabel_data,
                "analisis_q1": jawaban_analisis.get("analisis_q1", ""),
                "analisis_q2": jawaban_analisis.get("analisis_q2", ""),
                "analisis_q3": jawaban_analisis.get("analisis_q3", ""),
                "kesimpulan": kesimpulan.strip()
            }
            simpan_jawaban_baru(jawaban_dict)
            st.success("✅ Jawaban LKPD berhasil disimpan!")

# === MAIN APP ===
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "role", "current_user", "current_email"]:
            st.session_state.pop(key, None)
        st.rerun()

    # Tampilkan halaman berdasarkan role
    if st.session_state.role == "guru":
        guru_page()
    elif st.session_state.role == "admin":
        guru_page() # Admin bisa melihat halaman guru
    elif st.session_state.role == "siswa":
        siswa_page()