import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- Konfigurasi awal ---
st.set_page_config(
    page_title="Pre-test Fisika: Dinamika Rotasi",
    layout="wide"
)

# --- File konfigurasi ---
SOAL_FILE = "pre_test_soal.json"
JAWABAN_FILE = "pre_test_jawaban.csv"

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

# === Fungsi bantu ===
def init_soal_default():
    default = {
        "judul": "Pre-test Fisika: Dinamika Rotasi",
        "deskripsi": "Jawablah pertanyaan berikut dengan jelas dan singkat.",
        "soal_list": [
            {
                "id": "s1",
                "teks": "Jelaskan pengertian momen gaya (torsi) dan tuliskan rumusnya. Jelaskan pula makna fisis dari masing-masing variabel dalam rumus tersebut.",
                "kunci": "Momen gaya (torsi) adalah ukuran kecenderungan suatu gaya untuk memutar benda terhadap suatu poros. Rumus: τ = r × F = rF sin θ. r adalah lengan momen, F adalah gaya, θ adalah sudut antara r dan F.",
                "rubrik": {
                    "3": "Menjelaskan torsi, menyebutkan rumus, dan menjelaskan makna masing-masing variabel.",
                    "2": "Menjelaskan torsi dan rumus, tetapi kurang menjelaskan makna variabel.",
                    "1": "Menjelaskan torsi saja atau menyebut rumus tanpa penjelasan.",
                    "0": "Tidak menjawab atau jawaban salah."
                }
            },
            {
                "id": "s2",
                "teks": "Apa yang dimaksud dengan momen inersia? Jelaskan perbedaannya dengan massa dalam gerak translasi.",
                "kunci": "Momen inersia adalah ukuran kelembaman benda terhadap perubahan gerak rotasi. Ia berperan dalam gerak rotasi seperti massa dalam gerak translasi. Semakin besar momen inersia, semakin sulit benda diputar.",
                "rubrik": {
                    "3": "Menjelaskan definisi dan peran momen inersia serta perbedaannya dengan massa.",
                    "2": "Menjelaskan definisi dan menyebutkan perbedaannya, tetapi kurang lengkap.",
                    "1": "Menjelaskan definisi saja.",
                    "0": "Tidak menjawab atau jawaban salah."
                }
            },
            {
                "id": "s3",
                "teks": "Tuliskan rumus momentum sudut dan jelaskan hukum kekekalan momentum sudut. Berikan contoh penerapannya dalam kehidupan sehari-hari.",
                "kunci": "L = Iω. Hukum kekekalan momentum sudut menyatakan bahwa jika torsi luar nol, maka momentum sudut tetap. Contoh: pemain es skating memutar tubuhnya dengan mengurangi jari-jari (I berkurang, ω bertambah).",
                "rubrik": {
                    "3": "Menuliskan rumus, menjelaskan hukum, dan memberikan contoh penerapan.",
                    "2": "Menuliskan rumus dan menjelaskan hukum, tetapi tanpa contoh.",
                    "1": "Menuliskan rumus saja.",
                    "0": "Tidak menjawab atau jawaban salah."
                }
            },
            {
                "id": "s4",
                "teks": "Jelaskan perbedaan antara energi kinetik translasi dan energi kinetik rotasi. Tuliskan rumus masing-masing.",
                "kunci": "Energi kinetik translasi adalah energi akibat gerak lurus (EK = 1/2 mv²). Energi kinetik rotasi adalah energi akibat gerak putar (EK = 1/2 Iω²).",
                "rubrik": {
                    "3": "Menjelaskan perbedaan dan menuliskan kedua rumus dengan benar.",
                    "2": "Menjelaskan perbedaan tetapi hanya menuliskan satu rumus.",
                    "1": "Menjelaskan perbedaan tanpa rumus.",
                    "0": "Tidak menjawab atau jawaban salah."
                }
            },
            {
                "id": "s5",
                "teks": "Sebuah silinder pejal dengan massa M dan jari-jari R menggelinding tanpa slip. Jika kecepatan sudutnya ω, hitung energi kinetik total silinder tersebut.",
                "kunci": "EK_total = EK_translasi + EK_rotasi = 1/2 Mv² + 1/2 Iω². Karena v = ωR dan I = 1/2 MR², maka EK_total = 1/2 M(ωR)² + 1/2 (1/2 MR²)ω² = 3/4 Mω²R².",
                "rubrik": {
                    "3": "Menyebutkan rumus total EK, substitusi v = ωR, dan I, lalu menghitung dengan benar.",
                    "2": "Menyebutkan rumus EK total dan substitusi v dan I, tetapi salah perhitungan.",
                    "1": "Menyebutkan rumus EK translasi dan rotasi saja.",
                    "0": "Tidak menjawab atau jawaban salah."
                }
            }
        ]
    }
    with open(SOAL_FILE, "w") as f:
        json.dump(default, f, indent=4)

def muat_soal():
    if not os.path.exists(SOAL_FILE):
        init_soal_default()
    with open(SOAL_FILE, "r") as f:
        return json.load(f)

def simpan_soal(data):
    with open(SOAL_FILE, "w") as f:
        json.dump(data, f, indent=4)

def simpan_jawaban(email, judul, jawaban_dict, skor_total):
    df = pd.DataFrame([{
        "email": email,
        "judul": judul,
        "timestamp": datetime.now().isoformat(),
        "skor": skor_total,
        **{f"jawaban_{k}": v for k, v in jawaban_dict.items()}
    }])
    if os.path.exists(JAWABAN_FILE):
        df_existing = pd.read_csv(JAWABAN_FILE)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(JAWABAN_FILE, index=False)

def sudah_mengerjakan(email, judul):
    if not os.path.exists(JAWABAN_FILE):
        return False
    df = pd.read_csv(JAWABAN_FILE)
    return not df[(df["email"] == email) & (df["judul"] == judul)].empty

def get_nilai_siswa(email, judul):
    if not os.path.exists(JAWABAN_FILE):
        return None
    df = pd.read_csv(JAWABAN_FILE)
    row = df[(df["email"] == email) & (df["judul"] == judul)]
    if not row.empty:
        return row.iloc[0]["skor"]
    return None

# === HALAMAN GURU ===
def guru_page():
    st.title("Dashboard Guru: Pre-test Fisika")
    data = muat_soal()

    tab1, tab2 = st.tabs(["Edit Soal", "Lihat Hasil Siswa"])

    # --- Tab 1: Edit Soal + Kunci Jawaban + Rubrik ---
    with tab1:
        st.subheader("Edit Soal Pre-test")
        judul = st.text_input("Judul", data.get("judul", ""))
        deskripsi = st.text_area("Deskripsi", data.get("deskripsi", ""))

        soal_list = data.get("soal_list", [])
        updated_soal = []
        for i, soal in enumerate(soal_list):
            st.markdown(f"#### Soal {i+1}")
            teks = st.text_area(f"Teks Soal {i+1}", soal["teks"], key=f"teks_{i}")
            kunci = st.text_area(f"Kunci Jawaban", soal["kunci"], key=f"kunci_{i}")

            st.markdown("**Rubrik Penilaian**")
            rubrik = soal["rubrik"]
            rubrik_3 = st.text_input("Skor 3", rubrik.get("3", ""), key=f"r3_{i}")
            rubrik_2 = st.text_input("Skor 2", rubrik.get("2", ""), key=f"r2_{i}")
            rubrik_1 = st.text_input("Skor 1", rubrik.get("1", ""), key=f"r1_{i}")
            rubrik_0 = st.text_input("Skor 0", rubrik.get("0", ""), key=f"r0_{i}")

            updated_soal.append({
                "id": soal["id"],
                "teks": teks,
                "kunci": kunci,
                "rubrik": {"3": rubrik_3, "2": rubrik_2, "1": rubrik_1, "0": rubrik_0}
            })

        if st.button("Simpan Perubahan"):
            data["judul"] = judul
            data["deskripsi"] = deskripsi
            data["soal_list"] = updated_soal
            simpan_soal(data)
            st.success("Soal berhasil diperbarui!")

    # --- Tab 2: Lihat Hasil Siswa ---
    with tab2:
        st.subheader("Hasil Pre-test Siswa")
        if os.path.exists(JAWABAN_FILE):
            df = pd.read_csv(JAWABAN_FILE)
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("Belum ada siswa yang mengerjakan.")
        else:
            st.info("Belum ada data jawaban.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.current_email = ""
        st.rerun()

# === HALAMAN SISWA ===
def siswa_page():
    st.title("Pre-test: Dinamika Rotasi")
    data = muat_soal()

    judul = data.get("judul", "")
    deskripsi = data.get("deskripsi", "")

    st.subheader(judul)
    st.info(deskripsi)

    email = st.session_state.current_email

    # Cek apakah sudah mengerjakan
    if sudah_mengerjakan(email, judul):
        skor = get_nilai_siswa(email, judul)
        st.success(f"Anda sudah mengerjakan pre-test ini.")
        st.metric("Nilai Anda", f"{skor}/15")
        if skor >= 12:
            st.balloons()
            st.info("Luar biasa! Pemahaman Anda sangat baik.")
        elif skor >= 8:
            st.info("Bagus! Anda cukup memahami konsepnya.")
        else:
            st.warning("Ayo pelajari lagi materinya—kamu pasti bisa!")
        return

    # Form jawaban
    soal_list = data.get("soal_list", [])
    jawaban_dict = {}
    with st.form("form_pretest_siswa"):
        for i, soal in enumerate(soal_list):
            st.markdown(f"#### {i+1}. {soal['teks']}")
            jawaban = st.text_area(f"Jawaban {i+1}", key=soal["id"], height=120)
            jawaban_dict[soal["id"]] = jawaban

        submitted = st.form_submit_button("Kirim & Lihat Nilai")

        if submitted:
            if any(not v.strip() for v in jawaban_dict.values()):
                st.error("Mohon isi semua jawaban.")
            else:
                # Skor sementara: 3 per soal (asumsi otomatis = skor maksimal untuk demo)
                skor_total = 15  # 5 soal x 3

                simpan_jawaban(email, judul, jawaban_dict, skor_total)
                st.success("Jawaban dikirim!")
                st.metric("Nilai Anda", f"{skor_total}/15")
                if skor_total >= 12:
                    st.balloons()
                    st.info("Luar biasa! Pemahaman Anda sangat baik.")
                elif skor_total >= 8:
                    st.info("Bagus! Anda cukup memahami konsepnya.")
                else:
                    st.warning("Ayo pelajari lagi materinya—kamu pasti bisa!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.current_email = ""
        st.rerun()

# === MAIN ===
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "guru":
        guru_page()
    elif st.session_state.role == "siswa":
        siswa_page()
    else:
        st.error("Role tidak dikenali.")