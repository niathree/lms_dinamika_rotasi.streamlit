import streamlit as st
import json
import os
from datetime import datetime

# --- Konfigurasi awal ---
st.set_page_config(
    page_title="Post-test: Dinamika Rotasi",
    layout="wide"
)

# --- File konfigurasi ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

POST_TEST_FILE = os.path.join(DATA_DIR, "post_test.json")
JAWABAN_FILE = os.path.join(DATA_DIR, "post_test_jawaban.csv")

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

# --- Fungsi muat dan simpan data post-test ---
def muat_post_test():
    if os.path.exists(POST_TEST_FILE):
        with open(POST_TEST_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    else:
        # Buat soal default: 3 C3 (7 poin), 7 C4 (11 poin), 1 soal C4 = 13 poin agar total 100
        soal_default = {
            "judul": "Post-test: Dinamika Rotasi",
            "deskripsi": "Uji pemahamanmu tentang Torsi, Momen Inersia, Momentum Sudut, dan Energi Kinetik Rotasi.",
            "soal_list": [
                {
                    "id": 1,
                    "soal": "Sebuah silinder pejal (I = ½MR²) dan sebuah silinder berongga tipis (I = MR²) dengan massa dan jari-jari yang sama dilepaskan dari keadaan diam di puncak bidang miring yang sama. Manakah pernyataan yang benar mengenai gerak keduanya?",
                    "pilihan": ["A. Silinder berongga tiba di dasar lebih dulu karena memiliki momen inersia lebih besar.", "B. Silinder pejal tiba di dasar lebih dulu karena memiliki momen inersia lebih kecil.", "C. Keduanya tiba di dasar secara bersamaan karena massa dan jari-jarinya sama.", "D. Silinder berongga memiliki kecepatan linear akhir yang lebih besar.", "E. Silinder pejal memiliki energi kinetik rotasi yang lebih besar di dasar."],
                    "kunci": "B",
                    "poin": 11, # C4
                    "tingkat": "C4"
                },
                {
                    "id": 2,
                    "soal": "Sebuah roda dengan momen inersia 0,4 kg·m² berputar dengan kecepatan sudut 10 rad/s. Untuk menghentikannya dalam waktu 2 detik, torsi konstan yang harus diberikan adalah...",
                    "pilihan": ["A. 0.5 Nm", "B. 1.0 Nm", "C. 2.0 Nm", "D. 4.0 Nm", "E. 8.0 Nm"],
                    "kunci": "C",
                    "poin": 11, # C4
                    "tingkat": "C4"
                },
                {
                    "id": 3,
                    "soal": "Sebuah roda sepeda berdiameter 0,8 m diberi gaya 25 N secara tegak lurus pada tepinya. Besar torsi yang dihasilkan terhadap porosnya adalah...",
                    "pilihan": ["A. 5 Nm", "B. 10 Nm", "C. 20 Nm", "D. 25 Nm", "E. 40 Nm"],
                    "kunci": "C",
                    "poin": 7, # C3
                    "tingkat": "C3"
                },
                {
                    "id": 4,
                    "soal": "Sebuah kipas angin memiliki momen inersia 0,8 kg·m² dan mengalami torsi sebesar 4 Nm. Percepatan sudut kipas tersebut adalah...",
                    "pilihan": ["A. 0.2 rad/s²", "B. 0.4 rad/s²", "C. 2.0 rad/s²", "D. 5.0 rad/s²", "E. 8.0 rad/s²"],
                    "kunci": "D",
                    "poin": 7, # C3
                    "tingkat": "C3"
                },
                {
                    "id": 5,
                    "soal": "Seorang penari balet sedang berputar dengan lengan terentang. Ketika ia menarik kedua lengannya ke dada, kecepatan putarannya meningkat. Fenomena ini dapat dijelaskan dengan prinsip...",
                    "pilihan": ["A. Hukum II Newton untuk Rotasi.", "B. Kekekalan Energi Mekanik.", "C. Kekekalan Momentum Sudut.", "D. Hukum Kekekalan Energi Kinetik.", "E. Hukum Kekekalan Momen Inersia."],
                    "kunci": "C",
                    "poin": 7, # C3
                    "tingkat": "C3"
                },
                {
                    "id": 6,
                    "soal": "Dua gaya bekerja pada sebuah batang yang dapat berputar di titik poros O. Gaya A = 30 N, diberikan pada jarak 0,5 m dari O dengan sudut 90°. Gaya B = 40 N, diberikan pada jarak 0,4 m dari O dengan sudut 30°. Manakah pernyataan yang benar?",
                    "pilihan": ["A. Torsi dari gaya A dan B sama besar.", "B. Torsi dari gaya B lebih besar karena gayanya lebih besar.", "C. Torsi dari gaya A lebih besar karena menghasilkan torsi maksimum.", "D. Torsi dari gaya B lebih besar karena lengan momennya lebih panjang.", "E. Tidak dapat dibandingkan karena arah gayanya berbeda."],
                    "kunci": "C",
                    "poin": 11, # C4
                    "tingkat": "C4"
                },
                {
                    "id": 7,
                    "soal": "Jika lengan gaya dari sebuah pintu dikurangi menjadi sepertiganya, bagaimana perubahan torsi yang dihasilkan jika gaya yang diberikan tetap?",
                    "pilihan": ["A. Torsi menjadi tiga kali lebih besar.", "B. Torsi menjadi sepertiga dari semula.", "C. Torsi tetap sama.", "D. Torsi menjadi sembilan kali lebih kecil.", "E. Torsi menjadi nol."],
                    "kunci": "B",
                    "poin": 11, # C4
                    "tingkat": "C4"
                },
                {
                    "id": 8,
                    "soal": "Sebuah benda memiliki momen inersia sebesar I dan berotasi dengan kecepatan sudut ω. Jika kecepatan sudutnya diubah menjadi 2ω, bagaimana perubahan energi kinetik rotasinya?",
                    "pilihan": ["A. Menjadi dua kali lipat.", "B. Menjadi empat kali lipat.", "C. Menjadi setengahnya.", "D. Tidak berubah.", "E. Menjadi seperempatnya."],
                    "kunci": "B",
                    "poin": 11, # C4
                    "tingkat": "C4"
                },
                {
                    "id": 9,
                    "soal": "Dua roda identik memiliki massa yang sama, tetapi roda A massanya terkonsentrasi di tepi, sedangkan roda B massanya terkonsentrasi di pusat. Jika keduanya diberi torsi yang sama, roda mana yang lebih cepat mencapai kecepatan sudut tertentu?",
                    "pilihan": ["A. Roda A karena momen inersianya lebih besar.", "B. Roda B karena momen inersianya lebih kecil.", "C. Keduanya sama karena massanya sama.", "D. Roda A karena lebih stabil.", "E. Tidak dapat ditentukan tanpa mengetahui jari-jarinya."],
                    "kunci": "B",
                    "poin": 11, # C4
                    "tingkat": "C4"
                },
                {
                    "id": 10,
                    "soal": "Sebuah benda dikenai torsi sebesar 6 Nm, dengan gaya 20 N yang bekerja pada jarak 0,6 m dari sumbu putar. Berapakah besar sudut θ antara arah gaya dan lengan momen?",
                    "pilihan": ["A. 0°", "B. 30°", "C. 45°", "D. 60°", "E. 90°"],
                    "kunci": "B",
                    "poin": 13, # C4 (untuk mencapai total 100)
                    "tingkat": "C4"
                }
            ],
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(POST_TEST_FILE, "w", encoding='utf-8') as f:
            json.dump(soal_default, f, indent=4, ensure_ascii=False)
        return soal_default

def simpan_post_test(data_baru):
    with open(POST_TEST_FILE, "w", encoding='utf-8') as f:
        json.dump(data_baru, f, indent=4, ensure_ascii=False)

def simpan_jawaban_siswa(email, jawaban_dict, skor_total):
    import pandas as pd
    df = pd.DataFrame([{
        "email": email,
        "timestamp": datetime.now().isoformat(),
        "skor": skor_total,
        **{f"jawaban_{k}": v for k, v in jawaban_dict.items()}
    }])
    if os.path.exists(JAWABAN_FILE):
        df_existing = pd.read_csv(JAWABAN_FILE)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(JAWABAN_FILE, index=False)

def sudah_mengerjakan(email):
    if not os.path.exists(JAWABAN_FILE):
        return False
    import pandas as pd
    df = pd.read_csv(JAWABAN_FILE)
    return not df[df["email"] == email].empty

def get_nilai_siswa(email):
    if not os.path.exists(JAWABAN_FILE):
        return None
    import pandas as pd
    df = pd.read_csv(JAWABAN_FILE)
    row = df[df["email"] == email]
    if not row.empty:
        return row.iloc[0]["skor"]
    return None

# === HALAMAN GURU ===
def guru_page():
    st.header("📝 Edit Soal Post-test")
    data = muat_post_test()

    # Edit soal
    with st.form("form_edit_post_test"):
        judul_baru = st.text_input("Judul Post-test", value=data.get("judul", ""))
        desc_baru = st.text_area("Deskripsi", value=data.get("deskripsi", ""), height=100)

        soal_list_baru = []
        for i, soal in enumerate(data.get("soal_list", [])):
            st.markdown(f"---\n#### Soal {i+1} (Tingkat: {soal.get('tingkat', 'C?')})")
            soal_baru = st.text_area(f"Soal", value=soal.get("soal", ""), key=f"soal_{i}", height=150)
            pilihan_baru = []
            for j, p in enumerate(soal.get("pilihan", [])):
                pilihan_baru.append(st.text_input(f"Pilihan {chr(65+j)}", value=p, key=f"pil_{i}_{j}"))
            kunci_baru = st.selectbox(f"Kunci Jawaban Soal {i+1}", options=["A", "B", "C", "D", "E"], index=["A", "B", "C", "D", "E"].index(soal.get("kunci", "A")), key=f"kunci_{i}")
            # Poin otomatis berdasarkan tingkat kesulitan, kecuali soal ke-10 (index 9) = 13
            poin_default = 7 if soal.get("tingkat") == "C3" else 11
            if i == 9: # Soal ke-10 (index 9) kita atur manual jadi 13
                poin_default = 13
            poin_baru = st.number_input(f"Poin Soal {i+1}", value=soal.get("poin", poin_default), min_value=1, max_value=20, step=1, key=f"poin_{i}")
            # Filter hanya C3 & C4
            tingkat_baru = st.selectbox(f"Tingkat Kesulitan Soal {i+1}", 
                                       options=["C3", "C4"], 
                                       index=["C3", "C4"].index(soal.get("tingkat", "C3")), 
                                       key=f"tingkat_{i}")

            soal_baru_dict = {
                "id": i+1,
                "soal": soal_baru,
                "pilihan": pilihan_baru,
                "kunci": kunci_baru,
                "poin": poin_baru,
                "tingkat": tingkat_baru
            }
            soal_list_baru.append(soal_baru_dict)

        submitted = st.form_submit_button("💾 Simpan Soal Post-test")

    if submitted:
        total_poin_baru = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in soal_list_baru])
        if total_poin_baru != 100:
            st.error(f"⚠️ Total poin soal saat ini adalah {total_poin_baru}. Harap atur ulang agar totalnya menjadi 100.")
        else:
            data_baru = {
                "judul": judul_baru,
                "deskripsi": desc_baru,
                "soal_list": soal_list_baru,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_post_test(data_baru)
            st.success("✅ Soal post-test berhasil disimpan!")

    # Pratinjau soal untuk siswa (dengan kunci jawaban dan poin)
    st.divider()
    st.subheader("👁️ Pratinjau Soal untuk Siswa (dengan Kunci Jawaban)")
    total_poin = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in data.get("soal_list", [])])
    # Hitung jumlah C3 & C4
    c3_count = sum(1 for s in data.get("soal_list", []) if s.get("tingkat") == "C3")
    c4_count = sum(1 for s in data.get("soal_list", []) if s.get("tingkat") == "C4")
    st.info(f"**Jumlah Soal: {c3_count} C3, {c4_count} C4 | Total Poin Maksimal: {total_poin}**")
    for soal in data.get("soal_list", []):
        st.markdown(f"**({soal['poin']} poin - {soal['tingkat']}) {soal['soal']}**")
        for p in soal["pilihan"]:
            st.write(p)
        st.write(f"**Kunci Jawaban: {soal['kunci']}**")
        st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.current_email = ""
        st.rerun()

# === HALAMAN SISWA ===
def siswa_page():
    st.header("📝 Post-test: Dinamika Rotasi")
    data = muat_post_test()

    st.subheader(data.get("judul", "Post-test"))
    st.info(data.get("deskripsi", "Uji pemahamanmu."))

    # Cek apakah sudah mengerjakan
    if sudah_mengerjakan(st.session_state.current_email):
        skor = get_nilai_siswa(st.session_state.current_email)
        st.success(f"✅ Anda sudah mengerjakan post-test ini.")
        total_poin = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in data.get("soal_list", [])])
        st.metric("Nilai Anda", f"{skor}/{total_poin}")
        if skor >= 80:  # >= 80
            st.balloons()
            st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
        elif skor >= 60:  # >= 60
            st.info("👍 Bagus! Anda cukup memahami konsepnya.")
        else:
            st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")
        return

    # Form jawaban
    jawaban_dict = {}
    soal_list = data.get("soal_list", [])
    total_poin = sum([s.get("poin", 7 if s.get("tingkat") == "C3" else 11) for s in soal_list])

    with st.form("form_post_test_siswa"):
        for i, soal in enumerate(soal_list):
            poin_soal = soal.get("poin", 7 if soal.get("tingkat") == "C3" else 11)
            tingkat = soal.get("tingkat", "C?")
            st.markdown(f"**({poin_soal} poin - {tingkat}) {i+1}. {soal['soal']}**")
            for p in soal["pilihan"]:
                st.write(p)
            # Siswa hanya memilih jawaban, tidak melihat kunci
            jawaban = st.radio(f"Pilihan untuk soal {i+1}", options=["A", "B", "C", "D", "E"], key=f"jawaban_{i}", index=None)
            jawaban_dict[i+1] = jawaban

        submitted = st.form_submit_button("✅ Kirim Jawaban")

    if submitted:
        if any(v is None for v in jawaban_dict.values()):
            st.error("⚠️ Mohon jawab semua soal.")
        else:
            # Hitung skor
            skor_total = 0
            for i, soal in enumerate(soal_list):
                id_soal = i + 1
                jawaban_user = jawaban_dict[id_soal]
                if jawaban_user == soal.get("kunci"):
                    skor_total += soal.get("poin", 7 if soal.get("tingkat") == "C3" else 11)

            simpan_jawaban_siswa(st.session_state.current_email, jawaban_dict, skor_total)
            st.success("✅ Jawaban berhasil dikirim!")
            st.metric("Nilai Anda", f"{skor_total}/100")
            if skor_total >= 80:  # >= 80
                st.balloons()
                st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
            elif skor_total >= 60:  # >= 60
                st.info("👍 Bagus! Anda cukup memahami konsepnya.")
            else:
                st.warning("💡 Ayo pelajari lagi materinya kamu pasti bisa!")

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