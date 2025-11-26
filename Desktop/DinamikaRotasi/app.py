import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# === KONFIGURASI ===
PRETEST_SOAL_FILE = "pretest_soal.json"
PRETEST_SISWA_FILE = "pretest_siswa.csv"

# Inisialisasi file jika belum ada
if not os.path.exists(PRETEST_SOAL_FILE):
    # Teks default soal diambil dari permintaan Anda
    default_soal = {
        "pertemuan_1": [
            "Pernahkah kamu membuka pintu? Di bagian mana lebih mudah mendorongnya: dekat engsel atau di gagang pintu? Mengapa menurutmu?",
            "Jika kamu menggunakan kunci inggris untuk membuka baut, apakah lebih mudah memegang ujungnya atau dekat baut? Jelaskan!",
            "Bayangkan dua roda sepeda: satu polos, satu dipasangi beban di pinggirnya. Roda mana yang menurutmu lebih sulit diputar dari keadaan diam? Mengapa?",
            "Menurutmu, apa yang membuat suatu benda “sulit” atau “mudah” berputar?"
        ],
        "pertemuan_2": [
            "Pernah lihat penari balet atau pesenam berputar? Saat mereka menarik tangan ke badan, putarannya jadi lebih cepat atau lambat? Menurutmu, kenapa?",
            "Jika sebuah roda sepeda sedang berputar bebas di udara (tanpa gesekan), apakah putarannya akan berhenti sendiri? Mengapa?",
            "Apa perbedaan antara gerak lurus (translasi) dan gerak berputar (rotasi)? Berikan satu contoh benda yang mengalami kedua jenis gerak tersebut sekaligus (misalnya roda yang menggelinding).",
            "Bisakah suatu benda berputar semakin cepat tanpa didorong lagi? Jika ya, dalam situasi apa?"
        ],
        "waktu_update": ""
    }
    with open(PRETEST_SOAL_FILE, "w") as f:
        json.dump(default_soal, f)

if not os.path.exists(PRETEST_SISWA_FILE):
    pd.DataFrame(columns=["email", "nama", "kelompok", "pertemuan", "jawaban", "waktu_submit", "role"]).to_csv(PRETEST_SISWA_FILE, index=False)

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
    st.title("🔐 Login Pre-test")
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

# === HALAMAN GURU: EDIT SOAL & LIHAT PENGERJAAN SISWA ===
def guru_page():
    st.header("📝 Edit & Pantau Pre-test")

    # Muat soal dari file
    with open(PRETEST_SOAL_FILE, "r") as f:
        soal_data = json.load(f)

    # Form untuk mengedit soal Pertemuan 1 (dengan teks default dari permintaan Anda)
    st.subheader("Edit Soal Pre-test Pertemuan 1")
    soal_p1 = []
    for i, s in enumerate(soal_data.get("pertemuan_1", [
            "Pernahkah kamu membuka pintu? Di bagian mana lebih mudah mendorongnya: dekat engsel atau di gagang pintu? Mengapa menurutmu?",
            "Jika kamu menggunakan kunci inggris untuk membuka baut, apakah lebih mudah memegang ujungnya atau dekat baut? Jelaskan!",
            "Bayangkan dua roda sepeda: satu polos, satu dipasangi beban di pinggirnya. Roda mana yang menurutmu lebih sulit diputar dari keadaan diam? Mengapa?",
            "Menurutmu, apa yang membuat suatu benda “sulit” atau “mudah” berputar?"
        ])):
        q = st.text_area(f"Soal {i+1} Pertemuan 1", value=s, key=f"p1_{i}")
        soal_p1.append(q)

    # Form untuk mengedit soal Pertemuan 2 (dengan teks default dari permintaan Anda)
    st.subheader("Edit Soal Pre-test Pertemuan 2")
    soal_p2 = []
    for i, s in enumerate(soal_data.get("pertemuan_2", [
            "Pernah lihat penari balet atau pesenam berputar? Saat mereka menarik tangan ke badan, putarannya jadi lebih cepat atau lambat? Menurutmu, kenapa?",
            "Jika sebuah roda sepeda sedang berputar bebas di udara (tanpa gesekan), apakah putarannya akan berhenti sendiri? Mengapa?",
            "Apa perbedaan antara gerak lurus (translasi) dan gerak berputar (rotasi)? Berikan satu contoh benda yang mengalami kedua jenis gerak tersebut sekaligus (misalnya roda yang menggelinding).",
            "Bisakah suatu benda berputar semakin cepat tanpa didorong lagi? Jika ya, dalam situasi apa?"
        ])):
        q = st.text_area(f"Soal {i+1} Pertemuan 2", value=s, key=f"p2_{i}")
        soal_p2.append(q)

    if st.button("Simpan Soal Pre-test"):
        data_baru = {
            "pertemuan_1": soal_p1,
            "pertemuan_2": soal_p2,
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(PRETEST_SOAL_FILE, "w") as f:
            json.dump(data_baru, f)
        st.success("✅ Soal Pre-test berhasil disimpan dan **disimpan secara permanen**!")

    st.divider()
    # --- LIHAT PENGERJAAN SISWA ---
    st.subheader("📋 Daftar Siswa yang Mengerjakan Pre-test")

    df_siswa = pd.read_csv(PRETEST_SISWA_FILE)
    df_siswa = df_siswa[df_siswa["role"] == "siswa"] # Filter hanya data siswa

    if df_siswa.empty:
        st.info("Belum ada siswa yang mengerjakan pre-test.")
    else:
        # Tampilkan data siapa saja yang sudah submit
        df_summary = df_siswa.groupby(["email", "nama", "kelompok", "pertemuan"]).agg({
            "waktu_submit": "max"
        }).reset_index()

        st.dataframe(df_summary)

        # Opsi untuk melihat jawaban lengkap siswa tertentu
        st.subheader("🔍 Lihat Jawaban Siswa")
        emails_unik = df_siswa["email"].unique()
        email_pilihan = st.selectbox("Pilih Email Siswa:", ["Pilih..."] + list(emails_unik))

        if email_pilihan != "Pilih...":
            df_pilihan = df_siswa[df_siswa["email"] == email_pilihan]
            for _, row in df_pilihan.iterrows():
                st.write(f"**Nama:** {row['nama']}")
                st.write(f"**Kelompok:** {row['kelompok']}")
                st.write(f"**Pertemuan:** {row['pertemuan']}")
                st.write(f"**Waktu Submit:** {row['waktu_submit']}")
                st.write("**Jawaban:**")
                # Jawaban disimpan dalam format JSON string
                try:
                    jawaban_dict = json.loads(row['jawaban'])
                    for idx, (soal, jawaban) in enumerate(jawaban_dict.items(), 1):
                        st.write(f"**Soal {idx}:** {soal}")
                        st.write(f"**Jawaban:** {jawaban}")
                        st.divider()
                except json.JSONDecodeError:
                    st.error("Format jawaban rusak.")


# === HALAMAN SISWA: PILIH PERTEMUAN & KERJAKAN SOAL ===
def siswa_page():
    st.header("📝 Pre-test: Dinamika Rotasi")

    # Muat soal dari file
    if os.path.exists(PRETEST_SOAL_FILE):
        with open(PRETEST_SOAL_FILE, "r") as f:
            soal_data = json.load(f)
    else:
        st.error("Soal pre-test belum diatur oleh guru.")
        return

    # Pilih pertemuan
    pertemuan = st.selectbox("Pilih Pertemuan:", ["Pertemuan 1", "Pertemuan 2"])

    if pertemuan == "Pertemuan 1":
        petunjuk = """
        **Halo, Sobat Fisika !**
        Sebelum memulai pembelajaran hari ini, kamu diminta menjawab beberapa pertanyaan berikut berdasarkan pengalaman atau dugaanmu sendiri.
        🔹 Jawabanmu tidak dinilai, tetapi akan membantu guru memahami pemikiran awalmu.
        🔹 Jawablah dengan jujur dan sejujurnya — gunakan kata-katamu sendiri!
        🔹 Tidak ada jawaban salah !
        Setelah menjawab, kamu akan menonton video apersepsi dan melakukan eksplorasi melalui simulasi interaktif untuk memperdalam pemahamanmu.
        Selamat bereksplorasi! 
        """
        soal_list = soal_data.get("pertemuan_1", [])
    else: # Pertemuan 2
        petunjuk = """
        **Halo, Sobat Fisika!**
        Sebelum memulai pembelajaran hari ini, coba jawab pertanyaan berikut berdasarkan intuisi atau pengalaman sehari-harimu.
        🔹 Jawabanmu hanya untuk memicu rasa ingin tahu — tidak ada yang dinilai benar atau salah.
        🔹 Tulislah jawabanmu sejujurnya. 
        Setelah ini, kamu akan menjelajahi konsep-konsep menarik melalui simulasi virtual dan diskusi kelompok.
        Yuk, mulai eksplorasi !
        """
        soal_list = soal_data.get("pertemuan_2", [])

    st.info(petunjuk)
    st.divider()

    # Formulir untuk mengisi nama dan kelompok (opsional)
    nama = st.text_input("Nama Anggota Kelompok (Kamu)", value=st.session_state.current_user)
    kelompok = st.text_input("Nama Kelompok (Opsional)")

    # Form jawaban
    jawaban_dict = {}
    st.subheader("Jawaban Pre-test")
    for i, soal in enumerate(soal_list):
        jawaban = st.text_area(f"{i+1}. {soal}", key=f"jawab_{i}")
        jawaban_dict[soal] = jawaban

    # Tombol submit
    if st.button(f"Kirim Jawaban Pre-test {pertemuan}"):
        # Cek apakah nama diisi
        if not nama.strip():
            st.error("Mohon isi nama kamu terlebih dahulu.")
        else:
            # Cek apakah semua soal diisi (opsional)
            semua_terisi = all(jawaban.strip() for jawaban in jawaban_dict.values())
            if semua_terisi:
                # Simpan jawaban ke file CSV
                df_siswa = pd.read_csv(PRETEST_SISWA_FILE)
                new_entry = pd.DataFrame([{
                    "email": st.session_state.current_email,
                    "nama": nama.strip(),
                    "kelompok": kelompok.strip() if kelompok.strip() else "Tidak disebutkan",
                    "pertemuan": pertemuan,
                    "jawaban": json.dumps(jawaban_dict), # Simpan sebagai string JSON
                    "waktu_submit": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }])
                df_siswa = pd.concat([df_siswa, new_entry], ignore_index=True)
                df_siswa.to_csv(PRETEST_SISWA_FILE, index=False)
                st.success(f"✅ Jawaban Pre-test {pertemuan} berhasil disimpan.")
            else:
                st.error("Mohon isi semua pertanyaan terlebih dahulu.")


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