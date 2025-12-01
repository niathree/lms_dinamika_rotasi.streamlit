import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import uuid
import streamlit.components.v1 as components
from supabase import create_client, Client

# --- KONFIGURASI AWAL (Harus di awal sekali) ---
st.set_page_config(
    page_title="LMS Dinamika Rotasi (Supabase)",
    layout="wide"
)

# --- Setup Supabase Client ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- KONSTANTA ---
ADMIN_PASSWORD = "admin123"
GURU_PASSWORD = "guru123"
UPLOAD_FOLDER = "uploaded_media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- FILE KONFIGURASI (tidak digunakan lagi karena sekarang pakai Supabase) ---
# FILES = {...} # Baris ini dihapus

# File untuk menyimpan waktu terakhir update elemen (untuk notifikasi) - tetap menggunakan file lokal untuk sementara
NOTIFIKASI_FILE = "notifikasi_update.json"

# Inisialisasi file notifikasi jika belum ada
if not os.path.exists(NOTIFIKASI_FILE):
    default_notif = {
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
        "Hasil Penilaian": ""
    }
    with open(NOTIFIKASI_FILE, "w") as f:
        json.dump(default_notif, f)

# Session state untuk login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_email" not in st.session_state:
    st.session_state.current_email = ""

if "hadir" not in st.session_state:
    st.session_state.hadir = False

if "last_access" not in st.session_state:
    st.session_state.last_access = {}

# === FUNGSI LOGIN ===
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
                    st.session_state.hadir = True # Guru otomatis hadir
                    st.rerun()
                else:
                    st.error("❌ Password salah!")
        elif email == "admin@dinamikarotasi.sch.id": # Ganti dengan email admin Anda
            password = st.text_input("🔑 Password Admin", type="password", key="pwd_admin_input")
            if st.button("Login sebagai Admin", key="login_admin_btn"):
                if password == "admin123":
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
            if st.button("Login sebagai Siswa", key="login_siswa_btn"):
                st.session_state.role = "siswa"
                st.session_state.current_user = email.split("@")[0].title()
                st.session_state.current_email = email
                st.session_state.logged_in = True
                st.session_state.hadir = False # Siswa harus daftar hadir
                st.rerun()

# === FUNGSI PEMBANTU (Menggunakan Supabase) ===
def check_hadir():
    """Cek apakah siswa sudah daftar hadir."""
    if not st.session_state.get("hadir", False):
        st.warning("🔒 Silakan daftar hadir terlebih dahulu.")
        st.stop()

def muat_data_supabase(table_name, key_column=None, key_value=None):
    """Muat data dari tabel Supabase."""
    try:
        query = supabase.table(table_name).select("*")
        if key_column and key_value is not None:
            query = query.eq(key_column, key_value)
        response = query.execute()
        if response.data:
            if key_column: # Jika query berdasarkan kunci, kembalikan satu item
                # Konversi string JSON ke objek Python jika kolom 'data_json' ada
                if 'data_json' in response.data[0]:
                    import json
                    response.data[0]["data_json"] = json.loads(response.data[0]["data_json"])
                return response.data[0]
            else: # Jika query semua data, kembalikan list
                # Konversi string JSON ke objek Python jika kolom 'data_json' ada
                for item in response.data:
                    if 'data_json' in item:
                        import json
                        item["data_json"] = json.loads(item["data_json"])
                return response.data
        else:
            if key_column:
                return None # Tidak ditemukan
            else:
                return [] # Tidak ada data
    except Exception as e:
        st.error(f"Gagal memuat data dari {table_name}: {e}")
        return None

def simpan_data_supabase(table_name, data_baru, upsert=True):
    """Simpan data ke tabel Supabase."""
    try:
        # Konversi objek Python ke string JSON jika kolom 'data_json' ada
        data_to_save = data_baru.copy()
        if 'data_json' in data_to_save:
            import json
            data_to_save["data_json"] = json.dumps(data_to_save["data_json"], ensure_ascii=False)
        if upsert:
            # Gunakan upsert: insert jika tidak ada, update jika kunci utama (primary key) sudah ada
            # Untuk tabel konfigurasi, kita gunakan kunci 'kunci'
            if table_name == "konfigurasi":
                supabase.table(table_name).upsert(data_to_save).execute()
            else:
                # Untuk tabel lain, kita biasanya insert
                supabase.table(table_name).insert(data_to_save).execute()
        else:
            supabase.table(table_name).insert(data_to_save).execute()
    except Exception as e:
        st.error(f"Gagal menyimpan data ke {table_name}: {e}")

def periksa_notifikasi(item_key):
    """Cek apakah ada notifikasi baru untuk item tertentu."""
    # Muat waktu update dari file lokal (masih menggunakan file untuk notifikasi)
    with open(NOTIFIKASI_FILE, "r") as f:
        notif_data = json.load(f)
    waktu_update = notif_data.get(item_key)
    if not waktu_update:
        return False
    waktu_update_obj = datetime.strptime(waktu_update, "%Y-%m-%d %H:%M:%S")
    # Ambil waktu akses terakhir dari session state
    waktu_akses_terakhir = st.session_state.last_access.get(item_key)
    if not waktu_akses_terakhir:
        return True # Belum pernah diakses, tampilkan notifikasi
    waktu_akses_obj = datetime.strptime(waktu_akses_terakhir, "%Y-%m-%d %H:%M:%S")
    return waktu_update_obj > waktu_akses_obj

def reset_notifikasi(item_key):
    """Reset notifikasi setelah siswa membuka item."""
    st.session_state.last_access[item_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def update_notifikasi(item_key):
    """Fungsi helper untuk memperbarui waktu notifikasi di file lokal."""
    with open(NOTIFIKASI_FILE, "r") as f:
        notif = json.load(f)
    notif[item_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTIFIKASI_FILE, "w") as f:
        json.dump(notif, f)

# === MODUL DAFTAR HADIR ===
def daftar_hadir():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: DAFTAR HADIR ---
        st.header("📋 Daftar Hadir Siswa")
        df_raw = muat_data_supabase("data_hadir")
        if df_raw is not None:
            df = pd.DataFrame(df_raw)
            df_siswa = df[df["role"] == "siswa"]
            st.dataframe(df_siswa[["nama", "email", "status", "waktu"]].sort_values(by="waktu", ascending=False))
        else:
            st.info("Belum ada data kehadiran siswa.")
    else: # Siswa
        # --- DASBOR SISWA: DAFTAR HADIR ---
        st.header("📝 Daftar Hadir")
        nama = st.text_input("Nama Lengkap", value=st.session_state.current_user)
        status = st.radio("Status Kehadiran", ["Hadir", "Tidak Hadir"])
        if st.button("✅ Simpan Kehadiran"):
            if not nama.strip():
                st.error("Nama tidak boleh kosong!")
            else:
                new_entry = {
                    "email": st.session_state.current_email,
                    "nama": nama.strip(),
                    "status": status,
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }
                simpan_data_supabase("data_hadir", new_entry, upsert=False) # Insert
                st.session_state.hadir = (status == "Hadir")
                st.success(f"✅ Terima kasih, **{nama}**! Status kehadiran Anda: **{status}**.")

# === MODUL VIDEO APREPSI ===
def video_apersepsi():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: VIDEO APREPSI ---
        st.header("🎥 Upload & Edit Video Apersepsi")
        video_data = muat_data_supabase("konfigurasi", "kunci", "video_info")
        if not video_data:
            video_data = {"kunci": "video_info", "data_json": {}, "waktu_update": ""}
            # Buat default
            default_video_data = {
                "judul": "Video Apersepsi: Dinamika Rotasi",
                "deskripsi": "Halo, Sobat Fisika! Sebelum memulai pembelajaran hari ini, kamu diminta menonton video apersepsi berikut untuk memicu rasa ingin tahumu tentang fenomena rotasi di sekitar kita.",
                "file_video": "",
                "waktu_update": ""
            }
            simpan_data_supabase("konfigurasi", {
                "kunci": "video_info",
                "data_json": default_video_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            video_data = default_video_data
        else:
            video_data = video_data.get("data_json", {})

        with st.form("form_video_apresiasi"):
            judul_baru = st.text_input("Judul Video", value=video_data.get("judul", ""))
            desc_baru = st.text_area("Deskripsi Video", value=video_data.get("deskripsi", ""), height=150)
            vid = st.file_uploader("Upload video (MP4)", type=["mp4"])
            submitted = st.form_submit_button("💾 Simpan Video & Deskripsi")

            if submitted:
                if vid is not None:
                    # Simpan video dengan nama unik
                    unique_filename = f"{uuid.uuid4().hex}_{vid.name}"
                    video_path_simpan = os.path.join(UPLOAD_FOLDER, unique_filename)
                    with open(video_path_simpan, "wb") as f:
                        f.write(vid.read())
                    video_data["file_video"] = unique_filename
                video_data["judul"] = judul_baru
                video_data["deskripsi"] = desc_baru
                video_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data_supabase("konfigurasi", {
                    "kunci": "video_info",
                    "data_json": video_data,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Video Apersepsi")
                st.success("✅ Video apersepsi & deskripsi berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Video Apersepsi untuk Siswa")
        st.write(f"**{video_data.get('judul', 'Video Apersepsi')}**")
        st.info(video_data.get("deskripsi", ""))
        if video_data.get("file_video"):
            video_path = os.path.join(UPLOAD_FOLDER, video_data["file_video"])
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.warning("📁 File video belum ditemukan.")
        else:
            st.info("📁 Video belum diupload oleh guru.")

    else: # Siswa
        # --- DASBOR SISWA: VIDEO APREPSI ---
        st.header("🎥 Video Apersepsi")
        check_hadir()
        video_data_raw = muat_data_supabase("konfigurasi", "kunci", "video_info")
        if not video_data_raw:
            st.error("Video apersepsi belum diatur oleh guru.")
            st.stop()
        video_data = video_data_raw.get("data_json", {})
        st.write(f"**{video_data.get('judul', 'Video Apersepsi')}**")
        st.info(video_data.get("deskripsi", ""))
        if video_data.get("file_video"):
            video_path = os.path.join(UPLOAD_FOLDER, video_data["file_video"])
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.warning("📁 File video belum ditemukan.")
        else:
            st.info("📁 Video belum diupload oleh guru.")
        reset_notifikasi("Video Apersepsi")

# === MODUL PRE-TEST (gunakan kode baru yang disimpan ke Supabase) ===
def pre_test():
    import streamlit as st
    import pandas as pd
    import json
    import os
    from datetime import datetime

    # Konstanta
    SUPABASE_TABLE_PRE_TEST_SOAL = "konfigurasi"
    SUPABASE_TABLE_PRE_TEST_JAWABAN = "hasil_nilai"

    def muat_soal():
        # Ambil dari tabel konfigurasi dengan kunci 'pre_test_soal'
        data_raw = muat_data_supabase(SUPABASE_TABLE_PRE_TEST_SOAL, "kunci", "pre_test_soal")
        if not data_raw:
            # Buat data default jika tidak ada
            default_data = {
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
                    # Tambahkan soal-soal lainnya sesuai kebutuhan
                ]
            }
            simpan_data_supabase(SUPABASE_TABLE_PRE_TEST_SOAL, {
                "kunci": "pre_test_soal",
                "data_json": default_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return default_data
        return data_raw.get("data_json", {})

    def simpan_soal(data_baru):
        simpan_data_supabase(SUPABASE_TABLE_PRE_TEST_SOAL, {
            "kunci": "pre_test_soal",
            "data_json": data_baru,
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Update notifikasi
        update_notifikasi("Pre-test")

    def simpan_jawaban_siswa(email, nama, judul, jawaban_dict, skor_total):
        jawaban_json_str = json.dumps(jawaban_dict)
        new_entry = {
            "email": email,
            "nama": nama,
            "jenis_penilaian": "Pre-test",
            "jawaban_json": jawaban_json_str,
            "nilai": skor_total,
            "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": "siswa"
        }
        simpan_data_supabase(SUPABASE_TABLE_PRE_TEST_JAWABAN, new_entry, upsert=False)

    def sudah_mengerjakan(email):
        # Cek di tabel hasil_nilai untuk jenis_penilaian = 'Pre-test'
        try:
            response = supabase.table(SUPABASE_TABLE_PRE_TEST_JAWABAN).select("id").eq("email", email).eq("jenis_penilaian", "Pre-test").execute()
            return len(response.data) > 0
        except Exception:
            return False

    def get_nilai_siswa(email):
        # Ambil nilai dari tabel hasil_nilai untuk jenis_penilaian = 'Pre-test'
        try:
            response = supabase.table(SUPABASE_TABLE_PRE_TEST_JAWABAN).select("nilai").eq("email", email).eq("jenis_penilaian", "Pre-test").execute()
            if response.data:
                return response.data[0]["nilai"]
            return None
        except Exception:
            return None

    # --- Halaman Guru Pre-test ---
    def guru_page():
        st.header("🧑‍🏫 Dashboard Guru: Pre-test Fisika")
        data = muat_soal()

        tab1, tab2 = st.tabs(["Edit Soal", "Lihat Hasil Siswa"])

        # --- Tab 1: Edit Soal + Kunci Jawaban + Rubrik ---
        with tab1:
            st.subheader("📝 Edit Soal Pre-test")
            judul = st.text_input("Judul", value=data.get("judul", ""))
            deskripsi = st.text_area("Deskripsi", value=data.get("deskripsi", ""), height=100)

            soal_list = data.get("soal_list", [])
            updated_soal = []
            for i, soal in enumerate(soal_list):
                st.markdown(f"#### Soal {i+1}")
                teks = st.text_area(f"Teks Soal {i+1}", soal["teks"], key=f"teks_{i}", height=150)
                kunci = st.text_area(f"Kunci Jawaban", soal["kunci"], key=f"kunci_{i}", height=100)

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

            if st.button("💾 Simpan Perubahan"):
                data["judul"] = judul
                data["deskripsi"] = deskripsi
                data["soal_list"] = updated_soal
                simpan_soal(data)
                st.success("✅ Soal berhasil diperbarui!")

        # --- Tab 2: Lihat Hasil Siswa ---
        with tab2:
            st.subheader("📊 Hasil Pre-test Siswa")
            try:
                response = supabase.table(SUPABASE_TABLE_PRE_TEST_JAWABAN).select("*").eq("jenis_penilaian", "Pre-test").execute()
                if response.data:
                    df = pd.DataFrame(response.data)
                    st.dataframe(df[["nama", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
                else:
                    st.info("Belum ada siswa yang mengerjakan.")
            except Exception as e:
                st.error(f"Gagal mengambil data hasil: {e}")
                st.info("Belum ada data jawaban.")

    # --- Halaman Siswa Pre-test ---
    def siswa_page():
        st.header("⚙️ Pre-test: Dinamika Rotasi")
        data = muat_soal()

        judul = data.get("judul", "")
        deskripsi = data.get("deskripsi", "")

        st.subheader(judul)
        st.info(deskripsi)

        email = st.session_state.current_email
        nama = st.session_state.current_user

        # Cek apakah sudah mengerjakan
        if sudah_mengerjakan(email):
            skor = get_nilai_siswa(email)
            st.success(f"✅ Anda sudah mengerjakan pre-test ini.")
            st.metric("Nilai Anda", f"{skor}/15")
            if skor >= 12:
                st.balloons()
                st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
            elif skor >= 8:
                st.info("👍 Bagus! Anda cukup memahami konsepnya.")
            else:
                st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")
            return

        # Form jawaban
        soal_list = data.get("soal_list", [])
        jawaban_dict = {}
        with st.form("form_pretest_siswa"):
            for i, soal in enumerate(soal_list):
                st.markdown(f"#### {i+1}. {soal['teks']}")
                jawaban = st.text_area(f"Jawaban {i+1}", key=soal["id"], height=120)
                jawaban_dict[soal["id"]] = jawaban

            submitted = st.form_submit_button("✅ Kirim & Lihat Nilai")

            if submitted:
                if any(not v.strip() for v in jawaban_dict.values()):
                    st.error("⚠️ Mohon isi semua jawaban.")
                else:
                    # Skor sementara: 3 per soal (asumsi otomatis = skor maksimal untuk demo)
                    skor_total = 15  # 5 soal x 3

                    simpan_jawaban_siswa(email, nama, judul, jawaban_dict, skor_total)
                    st.success("✅ Jawaban dikirim!")
                    st.metric("Nilai Anda", f"{skor_total}/15")
                    if skor_total >= 12:
                        st.balloons()
                        st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
                    elif skor_total >= 8:
                        st.info("👍 Bagus! Anda cukup memahami konsepnya.")
                    else:
                        st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")

    # --- Main Pre-test ---
    if st.session_state.role == "guru":
        guru_page()
    else:
        siswa_page()

# === MODUL DESKRIPSI MATERI ===
def deskripsi_materi():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: DESKRIPSI MATERI ---
        st.header("📚 Edit Deskripsi Materi")
        deskripsi_data_raw = muat_data_supabase("konfigurasi", "kunci", "deskripsi_materi")
        if not deskripsi_data_raw:
            deskripsi_data = {}
            # Buat default
            default_deskripsi_data = {
                "judul": "Deskripsi Materi: Dinamika Rotasi",
                "capaian_pembelajaran": "... (isi capaian pembelajaran) ...",
                "tujuan_pembelajaran": ["... (isi tujuan pembelajaran 1) ...", "... (isi tujuan pembelajaran 2) ..."]
            }
            simpan_data_supabase("konfigurasi", {
                "kunci": "deskripsi_materi",
                "data_json": default_deskripsi_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            deskripsi_data = default_deskripsi_data
        else:
            deskripsi_data = deskripsi_data_raw.get("data_json", {})

        with st.form("form_edit_deskripsi"):
            judul_baru = st.text_input("Judul Deskripsi Materi", value=deskripsi_data.get("judul", ""))
            cp_baru = st.text_area("Capaian Pembelajaran (Fase F)", value=deskripsi_data.get("capaian_pembelajaran", ""), height=200)
            tp_list = deskripsi_data.get("tujuan_pembelajaran", [])
            tp_text = "\n".join(tp_list)
            tp_baru = st.text_area("Tujuan Pembelajaran (pisahkan dengan baris baru)", value=tp_text, height=150)
            submitted = st.form_submit_button("💾 Simpan Deskripsi Materi")

            if submitted:
                tp_list_baru = [item.strip() for item in tp_baru.split("\n") if item.strip()]
                data_baru = {
                    "judul": judul_baru,
                    "capaian_pembelajaran": cp_baru,
                    "tujuan_pembelajaran": tp_list_baru
                }
                simpan_data_supabase("konfigurasi", {
                    "kunci": "deskripsi_materi",
                    "data_json": data_baru,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Deskripsi Materi")
                st.success("✅ Deskripsi materi berhasil disimpan!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Deskripsi Materi untuk Siswa")
        st.write(f"**{deskripsi_data.get('judul', 'Deskripsi Materi')}**")
        st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
        st.write(deskripsi_data.get("capaian_pembelajaran", ""))
        st.markdown("### 📌 Tujuan Pembelajaran")
        for i, tp in enumerate(deskripsi_data.get("tujuan_pembelajaran", []), 1):
            st.write(f"{i}. {tp}")

    else: # Siswa
        # --- DASBOR SISWA: DESKRIPSI MATERI ---
        st.header("📚 Deskripsi Materi: Dinamika Rotasi")
        check_hadir()
        deskripsi_data_raw = muat_data_supabase("konfigurasi", "kunci", "deskripsi_materi")
        if not deskripsi_data_raw:
            st.error("Deskripsi materi belum diatur oleh guru.")
            st.stop()
        deskripsi_data = deskripsi_data_raw.get("data_json", {})
        st.write(f"**{deskripsi_data.get('judul', 'Deskripsi Materi')}**")
        st.markdown("### 🎯 Capaian Pembelajaran (Fase F)")
        st.write(deskripsi_data.get("capaian_pembelajaran", ""))
        st.markdown("### 📌 Tujuan Pembelajaran")
        for i, tp in enumerate(deskripsi_data.get("tujuan_pembelajaran", []), 1):
            st.write(f"{i}. {tp}")
        reset_notifikasi("Deskripsi Materi")

# === MODUL MEDIA PEMBELAJARAN ===
def media_pembelajaran():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: MEDIA PEMBELAJARAN ---
        st.header("📚 Upload & Edit Media Pembelajaran")
        media_data_raw = muat_data_supabase("konfigurasi", "kunci", "media_pembelajaran")
        if not media_data_raw:
            media_data = {}
            # Buat default
            default_media_data = {
                "judul": "Media Pembelajaran: Dinamika Rotasi",
                "deskripsi": "Berikut adalah media pembelajaran tambahan untuk memperdalam pemahaman Anda tentang Dinamika Rotasi.",
                "pertemuan_1": {
                    "judul": "Pertemuan 1",
                    "deskripsi": "Bahan ajar untuk Pertemuan 1",
                    "bahan_ajar": "### DINAMIKA ROTASI\n...",
                    "videos": [],
                    "images": []
                },
                "pertemuan_2": {
                    "judul": "Pertemuan 2",
                    "deskripsi": "Bahan ajar untuk Pertemuan 2",
                    "bahan_ajar": "### GERAK TRANSLASI vs GERAK ROTASI\n...",
                    "videos": [],
                    "images": []
                },
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data_supabase("konfigurasi", {
                "kunci": "media_pembelajaran",
                "data_json": default_media_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            media_data = default_media_data
        else:
            media_data = media_data_raw.get("data_json", {})

        tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

        # --- Pertemuan 1 ---
        with tab1:
            st.subheader("📅 Upload & Edit Media Pembelajaran - Pertemuan 1")
            p1_data = media_data.get("pertemuan_1", {})
            # Judul dan Deskripsi
            judul_p1 = st.text_input("Judul Pertemuan 1", value=p1_data.get("judul", ""))
            desc_p1 = st.text_area("Deskripsi Bahan Ajar", value=p1_data.get("deskripsi", ""), height=100)
            # Bahan Ajar (ditulis langsung)
            bahan_ajar_p1 = st.text_area("📝 Bahan Ajar Pertemuan 1 (Ditulis Langsung)", value=p1_data.get("bahan_ajar", ""), height=300)
            # Upload video & gambar tambahan
            st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 1")
            new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p1")
            new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p1")
            if st.button("➕ Tambahkan Video/Gambar Pertemuan 1"):
                if new_video_url:
                    # Validasi sederhana untuk URL embed
                    if "youtube.com/embed/" in new_video_url:
                        p1_data.setdefault("videos", []).append({
                            "judul": f"Video {len(p1_data.get('videos', [])) + 1}",
                            "url": new_video_url,
                            "sumber": "YouTube/Guru"
                        })
                        st.success("✅ Video berhasil ditambahkan!")
                    else:
                        st.error("Harap gunakan URL 'embed' YouTube yang valid. Contoh: https://www.youtube.com/embed/VIDEO_ID")
                if new_image_url:
                    p1_data.setdefault("images", []).append({
                        "judul": f"Gambar {len(p1_data.get('images', [])) + 1}",
                        "url": new_image_url,
                        "sumber": "Guru"
                    })
                    st.success("✅ Gambar berhasil ditambahkan!")
                media_data["pertemuan_1"] = p1_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data_supabase("konfigurasi", {
                    "kunci": "media_pembelajaran",
                    "data_json": media_data,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Media Pembelajaran")
                st.rerun()

            # Tombol Simpan
            if st.button("💾 Simpan Media Pembelajaran Pertemuan 1"):
                p1_data["judul"] = judul_p1
                p1_data["deskripsi"] = desc_p1
                p1_data["bahan_ajar"] = bahan_ajar_p1
                media_data["pertemuan_1"] = p1_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data_supabase("konfigurasi", {
                    "kunci": "media_pembelajaran",
                    "data_json": media_data,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Media Pembelajaran")
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

        # --- Pertemuan 2 ---
        with tab2:
            st.subheader("📅 Upload & Edit Media Pembelajaran - Pertemuan 2")
            p2_data = media_data.get("pertemuan_2", {})
            # Judul dan Deskripsi
            judul_p2 = st.text_input("Judul Pertemuan 2", value=p2_data.get("judul", ""))
            desc_p2 = st.text_area("Deskripsi Bahan Ajar", value=p2_data.get("deskripsi", ""), height=100)
            # Bahan Ajar (ditulis langsung)
            bahan_ajar_p2 = st.text_area("📝 Bahan Ajar Pertemuan 2 (Ditulis Langsung)", value=p2_data.get("bahan_ajar", ""), height=300)
            # Upload video & gambar tambahan
            st.subheader("🖼️ Upload Video & Gambar Tambahan - Pertemuan 2")
            new_video_url = st.text_input("URL Video YouTube (Embed)", key="new_video_p2")
            new_image_url = st.text_input("URL Gambar (Harus dihosting online)", key="new_image_p2")
            if st.button("➕ Tambahkan Video/Gambar Pertemuan 2"):
                if new_video_url:
                    # Validasi sederhana untuk URL embed
                    if "youtube.com/embed/" in new_video_url:
                        p2_data.setdefault("videos", []).append({
                            "judul": f"Video {len(p2_data.get('videos', [])) + 1}",
                            "url": new_video_url,
                            "sumber": "YouTube/Guru"
                        })
                        st.success("✅ Video berhasil ditambahkan!")
                    else:
                        st.error("Harap gunakan URL 'embed' YouTube yang valid. Contoh: https://www.youtube.com/embed/VIDEO_ID")
                if new_image_url:
                    p2_data.setdefault("images", []).append({
                        "judul": f"Gambar {len(p2_data.get('images', [])) + 1}",
                        "url": new_image_url,
                        "sumber": "Guru"
                    })
                    st.success("✅ Gambar berhasil ditambahkan!")
                media_data["pertemuan_2"] = p2_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data_supabase("konfigurasi", {
                    "kunci": "media_pembelajaran",
                    "data_json": media_data,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Media Pembelajaran")
                st.rerun()

            # Tombol Simpan
            if st.button("💾 Simpan Media Pembelajaran Pertemuan 2"):
                p2_data["judul"] = judul_p2
                p2_data["deskripsi"] = desc_p2
                p2_data["bahan_ajar"] = bahan_ajar_p2
                media_data["pertemuan_2"] = p2_data
                media_data["waktu_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                simpan_data_supabase("konfigurasi", {
                    "kunci": "media_pembelajaran",
                    "data_json": media_data,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Media Pembelajaran")
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

    else: # Siswa
        # --- DASBOR SISWA: MEDIA PEMBELAJARAN ---
        st.header("📚 Media Pembelajaran: Dinamika Rotasi")
        check_hadir()
        media_data_raw = muat_data_supabase("konfigurasi", "kunci", "media_pembelajaran")
        if not media_data_raw:
            st.error("Media pembelajaran belum diatur oleh guru.")
            st.stop()
        media_data = media_data_raw.get("data_json", {})
        st.write(f"**{media_data.get('judul', 'Media Pembelajaran')}**")
        st.info(media_data.get("deskripsi", ""))
        tab1, tab2 = st.tabs(["📅 Pertemuan 1", "📅 Pertemuan 2"])

        # --- Pertemuan 1 ---
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

        # --- Pertemuan 2 ---
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

        reset_notifikasi("Media Pembelajaran")

# === MODUL SIMULASI VIRTUAL (gunakan kode baru yang disimpan ke Supabase) ===
def simulasi_virtual():
    import streamlit as st
    import streamlit.components.v1 as components
    import json
    import os
    from datetime import datetime

    SUPABASE_TABLE_SIMULASI_VIRTUAL = "konfigurasi"

    def muat_simulasi():
        data_raw = muat_data_supabase(SUPABASE_TABLE_SIMULASI_VIRTUAL, "kunci", "simulasi_virtual")
        if not data_raw:
            default_data = {
                "judul": "Simulasi Virtual: Dinamika Rotasi",
                "deskripsi": "Eksplorasi konsep Torsi, Momen Inersia, dan Momentum Sudut secara interaktif dengan simulasi PhET!",
                "petunjuk_penggunaan": "... (isi petunjuk penggunaan) ...",
                "simulasi_list": [
                    {
                        "judul": "⚖️ Torque (Torsi) - PhET",
                        "url": "https://phet.colorado.edu/sims/cheerpj/rotation/latest/rotation.html?simulation=torque",
                        "sumber": "PhET Colorado",
                        "petunjuk": "... (isi petunjuk khusus simulasi) ..."
                    }
                ],
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data_supabase(SUPABASE_TABLE_SIMULASI_VIRTUAL, {
                "kunci": "simulasi_virtual",
                "data_json": default_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return default_data
        return data_raw.get("data_json", {})

    def simpan_simulasi(data_baru):
        simpan_data_supabase(SUPABASE_TABLE_SIMULASI_VIRTUAL, {
            "kunci": "simulasi_virtual",
            "data_json": data_baru,
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Update notifikasi
        update_notifikasi("Simulasi Virtual")

    # --- Halaman Guru Simulasi ---
    def guru_page():
        st.header("🧪 Edit Simulasi Virtual")
        simulasi_data = muat_simulasi()

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
            simpan_simulasi(data_baru)
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
            # Coba embed simulasi
            try:
                components.iframe(sim["url"], height=600, scrolling=True)
            except Exception:
                st.warning(f"Simulasi tidak dapat dimuat langsung. [Klik di sini untuk membuka di tab baru]({sim['url']})")

    # --- Halaman Siswa Simulasi ---
    def siswa_page():
        st.header("🧪 Simulasi Virtual: Dinamika Rotasi")
        simulasi_data = muat_simulasi()

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
            # Coba embed simulasi
            try:
                components.iframe(simulasi["url"], height=600, scrolling=True)
            except Exception:
                st.error(f"Simulasi '{simulasi['judul']}' tidak dapat dimuat langsung di halaman ini.")
                st.link_button(f"🔗 Buka Simulasi", simulasi["url"])
                st.info("💡 **Catatan:** Simulasi akan terbuka di tab baru browser Anda.")

    # --- Main Simulasi ---
    if st.session_state.role == "guru":
        guru_page()
    else:
        siswa_page()

# === MODUL LKPD ===
def lkpd():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: LKPD ---
        st.header("📄 Edit LKPD")
        lkpd_data_raw = muat_data_supabase("konfigurasi", "kunci", "lkpd")
        if not lkpd_data_raw:
            lkpd_data = {}
            # Buat default
            default_lkpd_data = {
                "judul": "LKPD: Dinamika Rotasi - Analisis Torsi dan Durasi Putaran Gasing",
                "deskripsi": "... (isi deskripsi LKPD) ...",
                "tujuan": ["... (isi tujuan LKPD 1) ...", "... (isi tujuan LKPD 2) ..."],
                "materi": "... (isi dasar teori) ...",
                "petunjuk": ["... (isi petunjuk 1) ...", "... (isi petunjuk 2) ..."],
                "alat_bahan": ["... (isi alat bahan 1) ...", "... (isi alat bahan 2) ..."],
                "langkah_kerja": ["... (isi langkah kerja 1) ...", "... (isi langkah kerja 2) ..."],
                "tabel_header": ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"],
                "analisis_pertanyaan": ["... (isi pertanyaan analisis 1) ...", "... (isi pertanyaan analisis 2) ..."],
                "kesimpulan_petunjuk": "... (isi petunjuk kesimpulan) ...",
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data_supabase("konfigurasi", {
                "kunci": "lkpd",
                "data_json": default_lkpd_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            lkpd_data = default_lkpd_data
        else:
            lkpd_data = lkpd_data_raw.get("data_json", {})

        with st.form("form_edit_lkpd"):
            judul_baru = st.text_input("Judul LKPD", value=lkpd_data.get("judul", ""))
            desc_baru = st.text_area("Deskripsi LKPD", value=lkpd_data.get("deskripsi", ""), height=100)
            st.subheader("🎯 Tujuan Pembelajaran")
            tujuan_list = lkpd_data.get("tujuan", [])
            tujuan_text = "\n".join(tujuan_list)
            tujuan_baru = st.text_area("Tujuan (pisahkan dengan baris baru)", value=tujuan_text, height=150)
            st.subheader("📚 Dasar Teori")
            teori_baru = st.text_area("Dasar Teori", value=lkpd_data.get("materi", ""), height=200)
            st.subheader("📋 Petunjuk Pengerjaan")
            petunjuk_list = lkpd_data.get("petunjuk", [])
            petunjuk_text = "\n".join(petunjuk_list)
            petunjuk_baru = st.text_area("Petunjuk (pisahkan dengan baris baru)", value=petunjuk_text, height=150)
            st.subheader("🛠️ Alat dan Bahan")
            alat_list = lkpd_data.get("alat_bahan", [])
            alat_text = "\n".join(alat_list)
            alat_baru = st.text_area("Alat dan Bahan (pisahkan dengan baris baru)", value=alat_text, height=150)
            st.subheader("👣 Langkah Kerja")
            langkah_list = lkpd_data.get("langkah_kerja", [])
            langkah_text = "\n".join(langkah_list)
            langkah_baru = st.text_area("Langkah Kerja (pisahkan dengan baris baru)", value=langkah_text, height=200)
            st.subheader("📊 Tabel Hasil Pengamatan")
            header_lama = lkpd_data.get("tabel_header", [])
            header_baru_list = []
            cols_header = st.columns(len(header_lama))
            for i, col in enumerate(cols_header):
                if i < len(header_lama):
                    val = header_lama[i]
                else:
                    val = f"Kolom {i+1}"
                header_val = col.text_input(f"Header {i+1}", value=val, key=f"header_{i}")
                header_baru_list.append(header_val)
            st.subheader("🧠 Pertanyaan Analisis Data dan Diskusi")
            analisis_list = lkpd_data.get("analisis_pertanyaan", [])
            analisis_baru_list = []
            for i, q in enumerate(analisis_list):
                q_baru = st.text_area(f"Pertanyaan {i+1}", value=q, key=f"analisis_q_{i}")
                analisis_baru_list.append(q_baru)
            st.subheader("🎯 Petunjuk untuk Menulis Kesimpulan")
            kesimpulan_baru = st.text_area("Petunjuk Kesimpulan", value=lkpd_data.get("kesimpulan_petunjuk", ""), height=100)
            submitted = st.form_submit_button("💾 Simpan Seluruh Perubahan LKPD")

            if submitted:
                data_baru = {
                    "judul": judul_baru,
                    "deskripsi": desc_baru,
                    "tujuan": [item.strip() for item in tujuan_baru.split("\n") if item.strip()],
                    "materi": teori_baru,
                    "petunjuk": [item.strip() for item in petunjuk_baru.split("\n") if item.strip()],
                    "alat_bahan": [item.strip() for item in alat_baru.split("\n") if item.strip()],
                    "langkah_kerja": [item.strip() for item in langkah_baru.split("\n") if item.strip()],
                    "tabel_header": header_baru_list,
                    "analisis_pertanyaan": analisis_baru_list,
                    "kesimpulan_petunjuk": kesimpulan_baru,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                simpan_data_supabase("konfigurasi", {
                    "kunci": "lkpd",
                    "data_json": data_baru,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("LKPD")
                st.success("✅ Seluruh LKPD berhasil diperbarui!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau LKPD untuk Siswa")
        st.write(f"**{lkpd_data.get('judul', 'LKPD')}**")
        st.info(lkpd_data.get("deskripsi", ""))
        st.markdown("### 🎯 Tujuan Pembelajaran")
        for i, t in enumerate(lkpd_data.get("tujuan", []), 1):
            st.write(f"{i}. {t}")
        st.markdown("### 📚 Dasar Teori")
        st.write(lkpd_data.get("materi", ""))
        st.markdown("### 📋 Petunjuk Pengerjaan")
        for i, p in enumerate(lkpd_data.get("petunjuk", []), 1):
            st.write(f"{i}. {p}")
        st.markdown("### 🛠️ Alat dan Bahan")
        for a in lkpd_data.get("alat_bahan", []):
            st.write(f"- {a}")
        st.markdown("### 👣 Langkah Kerja")
        for i, l in enumerate(lkpd_data.get("langkah_kerja", []), 1):
            st.write(f"{i}. {l}")
        st.markdown("### 📊 Tabel Hasil Pengamatan")
        header_list = lkpd_data.get("tabel_header", ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"])
        st.table([header_list] + [["", "", "", "", ""]] * 3)
        st.markdown("### 🧠 Pertanyaan Analisis Data dan Diskusi")
        for i, q in enumerate(lkpd_data.get("analisis_pertanyaan", []), 1):
            st.markdown(f"**{i}. {q}**")
        st.markdown("### 🎯 Kesimpulan")
        st.write(lkpd_data.get("kesimpulan_petunjuk", ""))

    else: # Siswa
        # --- DASBOR SISWA: LKPD ---
        st.header("📄 LKPD: Dinamika Rotasi")
        check_hadir()
        lkpd_data_raw = muat_data_supabase("konfigurasi", "kunci", "lkpd")
        if not lkpd_data_raw:
            st.error("LKPD belum diatur oleh guru.")
            st.stop()
        lkpd_data = lkpd_data_raw.get("data_json", {})
        st.write(f"**{lkpd_data.get('judul', 'LKPD')}**")
        st.info(lkpd_data.get("deskripsi", ""))
        st.markdown("### 🎯 Tujuan Pembelajaran")
        for i, t in enumerate(lkpd_data.get("tujuan", []), 1):
            st.write(f"{i}. {t}")
        st.markdown("### 📚 Dasar Teori")
        st.write(lkpd_data.get("materi", ""))
        st.markdown("### 📋 Petunjuk Pengerjaan")
        for i, p in enumerate(lkpd_data.get("petunjuk", []), 1):
            st.write(f"{i}. {p}")
        st.markdown("### 🛠️ Alat dan Bahan")
        for a in lkpd_data.get("alat_bahan", []):
            st.write(f"- {a}")
        st.markdown("### 👣 Langkah Kerja")
        for i, l in enumerate(lkpd_data.get("langkah_kerja", []), 1):
            st.write(f"{i}. {l}")
        st.markdown("### 📊 Tabel Hasil Pengamatan")
        header_list = lkpd_data.get("tabel_header", ["No.", "Gaya Tarikan", "Panjang Tali/ Lengan (cm)", "Waktu Putar (s)", "Torsi Relatif"])
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
        st.markdown("### 🧠 Analisis Data dan Diskusi")
        jawaban_analisis = {}
        for i, q in enumerate(lkpd_data.get("analisis_pertanyaan", []), 1):
            st.markdown(f"**{i}. {q}**")
            jawaban = st.text_area("Jawaban Anda:", key=f"analisis_q{i}", height=100)
            jawaban_analisis[f"analisis_q{i}"] = jawaban
        st.markdown("### 🎯 Kesimpulan")
        kesimpulan = st.text_area(lkpd_data.get("kesimpulan_petunjuk", "Tulis kesimpulan kelompok Anda:"), height=150)
        if st.button("✅ Simpan Jawaban LKPD"):
            if any(not v.strip() for v in jawaban_analisis.values()) or not kesimpulan.strip():
                st.error("⚠️ Mohon jawab semua pertanyaan dan isi kesimpulan!")
            else:
                df_nilai = muat_data_supabase("hasil_nilai") # Ambil data nilai dari Supabase
                if df_nilai is None:
                    df_nilai = [] # Jika belum ada data, buat list kosong
                jawaban_lkpd = {
                    "tabel": str(tabel_data),
                    "analisis": str(jawaban_analisis),
                    "kesimpulan": kesimpulan.strip()
                }
                jawaban_json_str = json.dumps(jawaban_lkpd)
                new_entry = {
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "jenis_penilaian": "LKPD",
                    "jawaban_json": jawaban_json_str,
                    "nilai": 0, # Nilai akan diisi oleh guru
                    "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }
                # Simpan ke Supabase
                simpan_data_supabase("hasil_nilai", new_entry, upsert=False)
                st.success("✅ Jawaban LKPD berhasil disimpan!")
        reset_notifikasi("LKPD")

# === MODUL REFLEKSI SISWA ===
def refleksi_siswa():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: REFLEKSI SISWA ---
        st.header("💭 Edit Refleksi Siswa")
        refleksi_data_raw = muat_data_supabase("konfigurasi", "kunci", "refleksi")
        if not refleksi_data_raw:
            refleksi_data = {}
            # Buat default
            default_refleksi_data = {
                "judul": "Refleksi Pembelajaran: Dinamika Rotasi",
                "deskripsi": "... (isi deskripsi refleksi) ...",
                "pertanyaan_list": [
                    {"id": "r1", "teks": "Bagaimana perasaan Anda setelah mempelajari materi pada pertemuan ini?"},
                    {"id": "r2", "teks": "Materi apa yang belum Anda pahami pada pembelajaran ini?"},
                    # Tambahkan pertanyaan lainnya
                ],
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data_supabase("konfigurasi", {
                "kunci": "refleksi",
                "data_json": default_refleksi_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            refleksi_data = default_refleksi_data
        else:
            refleksi_data = refleksi_data_raw.get("data_json", {})

        with st.form("form_edit_refleksi"):
            judul_baru = st.text_input("Judul Refleksi", value=refleksi_data.get("judul", ""))
            desc_baru = st.text_area("Deskripsi Refleksi", value=refleksi_data.get("deskripsi", ""), height=150)
            st.subheader("📝 Pertanyaan Refleksi")
            pertanyaan_list = refleksi_data.get("pertanyaan_list", [])
            pertanyaan_baru_list = []
            for i, q in enumerate(pertanyaan_list):
                q_baru = st.text_area(f"Pertanyaan {i+1}", value=q.get("teks", ""), key=f"refleksi_q_{i}")
                pertanyaan_baru_list.append({"id": q.get("id", f"r{i+1}"), "teks": q_baru})
            submitted = st.form_submit_button("💾 Simpan Refleksi Siswa")

            if submitted:
                data_baru = {
                    "judul": judul_baru,
                    "deskripsi": desc_baru,
                    "pertanyaan_list": pertanyaan_baru_list
                }
                simpan_data_supabase("konfigurasi", {
                    "kunci": "refleksi",
                    "data_json": data_baru,
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update notifikasi
                update_notifikasi("Refleksi Siswa")
                st.success("✅ Refleksi siswa berhasil diperbarui!")

        # Tampilkan pratinjau
        st.divider()
        st.subheader("👁️‍🗨️ Pratinjau Refleksi untuk Siswa")
        st.write(f"**{refleksi_data.get('judul', 'Refleksi Siswa')}**")
        st.info(refleksi_data.get("deskripsi", ""))
        for i, q in enumerate(refleksi_data.get("pertanyaan_list", []), 1):
            st.markdown(f"#### {i}. {q['teks']}")

    else: # Siswa
        # --- DASBOR SISWA: REFLEKSI SISWA ---
        st.header("💭 Refleksi Pembelajaran")
        check_hadir()
        refleksi_data_raw = muat_data_supabase("konfigurasi", "kunci", "refleksi")
        if not refleksi_data_raw:
            st.error("Refleksi belum diatur oleh guru.")
            st.stop()
        refleksi_data = refleksi_data_raw.get("data_json", {})
        st.write(f"**{refleksi_data.get('judul', 'Refleksi Siswa')}**")
        st.info(refleksi_data.get("deskripsi", ""))
        jawaban_refleksi = {}
        for i, q in enumerate(refleksi_data.get("pertanyaan_list", []), 1):
            st.markdown(f"#### {i}. {q['teks']}")
            jawaban = st.text_area("Jawaban Anda:", key=q["id"], height=100)
            jawaban_refleksi[q["id"]] = jawaban
        if st.button("✅ Kirim Refleksi"):
            if any(not v.strip() for v in jawaban_refleksi.values()):
                st.error("⚠️ Mohon jawab semua pertanyaan.")
            else:
                # Simpan ke Supabase
                df_nilai = muat_data_supabase("hasil_nilai")
                if df_nilai is None:
                    df_nilai = []
                jawaban_json_str = json.dumps(jawaban_refleksi)
                new_entry = {
                    "email": st.session_state.current_email,
                    "nama": st.session_state.current_user,
                    "jenis_penilaian": "Refleksi",
                    "jawaban_json": jawaban_json_str,
                    "nilai": 0, # Refleksi tidak dinilai
                    "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": "siswa"
                }
                simpan_data_supabase("hasil_nilai", new_entry, upsert=False)
                st.success("✅ Refleksi berhasil dikirim!")
        reset_notifikasi("Refleksi Siswa")

# === MODUL POST-TEST (gunakan kode baru yang disimpan ke Supabase) ===
def post_test():
    import streamlit as st
    import json
    import os
    from datetime import datetime

    SUPABASE_TABLE_POST_TEST = "konfigurasi"
    SUPABASE_TABLE_POST_TEST_JAWABAN = "hasil_nilai"

    def muat_post_test():
        data_raw = muat_data_supabase(SUPABASE_TABLE_POST_TEST, "kunci", "post_test")
        if not data_raw:
            # Buat soal default: 3 C3 (7 poin), 7 C4 (11 poin), 1 soal C4 = 13 poin agar total 100
            default_data = {
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
                    # Tambahkan soal-soal lainnya sesuai kebutuhan
                ],
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            simpan_data_supabase(SUPABASE_TABLE_POST_TEST, {
                "kunci": "post_test",
                "data_json": default_data,
                "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return default_data
        return data_raw.get("data_json", {})

    def simpan_post_test(data_baru):
        simpan_data_supabase(SUPABASE_TABLE_POST_TEST, {
            "kunci": "post_test",
            "data_json": data_baru,
            "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Update notifikasi
        update_notifikasi("Post-test")

    def simpan_jawaban_siswa(email, nama, jawaban_dict, skor_total):
        jawaban_json_str = json.dumps(jawaban_dict)
        new_entry = {
            "email": email,
            "nama": nama,
            "jenis_penilaian": "Post-test",
            "jawaban_json": jawaban_json_str,
            "nilai": skor_total,
            "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": "siswa"
        }
        simpan_data_supabase(SUPABASE_TABLE_POST_TEST_JAWABAN, new_entry, upsert=False)

    def sudah_mengerjakan(email):
        try:
            response = supabase.table(SUPABASE_TABLE_POST_TEST_JAWABAN).select("id").eq("email", email).eq("jenis_penilaian", "Post-test").execute()
            return len(response.data) > 0
        except Exception:
            return False

    def get_nilai_siswa(email):
        try:
            response = supabase.table(SUPABASE_TABLE_POST_TEST_JAWABAN).select("nilai").eq("email", email).eq("jenis_penilaian", "Post-test").execute()
            if response.data:
                return response.data[0]["nilai"]
            return None
        except Exception:
            return None

    # --- Halaman Guru Post-test ---
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

    # --- Halaman Siswa Post-test ---
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

                simpan_jawaban_siswa(st.session_state.current_email, st.session_state.current_user, jawaban_dict, skor_total)
                st.success("✅ Jawaban berhasil dikirim!")
                st.metric("Nilai Anda", f"{skor_total}/100")
                if skor_total >= 80:  # >= 80
                    st.balloons()
                    st.info("🎉 Luar biasa! Pemahaman Anda sangat baik.")
                elif skor_total >= 60:  # >= 60
                    st.info("👍 Bagus! Anda cukup memahami konsepnya.")
                else:
                    st.warning("💡 Ayo pelajari lagi materinya—kamu pasti bisa!")

    # --- Main Post-test ---
    if st.session_state.role == "guru":
        guru_page()
    else:
        siswa_page()

# === MODUL FORUM DISKUSI (gunakan kode baru yang disimpan ke Supabase) ===
def forum_diskusi():
    import streamlit as st
    import json
    import os
    from datetime import datetime

    SUPABASE_TABLE_FORUM = "forum_diskusi"

    def muat_forum():
        # Ambil semua data dari tabel forum_diskusi
        try:
            response = supabase.table(SUPABASE_TABLE_FORUM).select("*").order("waktu", desc=False).execute()
            if response.data:
                # Bangun struktur pohon dari flat list
                all_posts = response.data
                topik_list = [item for item in all_posts if item["parent_id"] is None or pd.isna(item["parent_id"])]
                for topik in topik_list:
                    topik["komentar"] = [k for k in all_posts if k["parent_id"] == topik["id"]]
                    for komentar in topik["komentar"]:
                        komentar["balasan"] = [b for b in all_posts if b["parent_id"] == komentar["id"]]
                return {"topik": topik_list}
            else:
                return {"topik": []}
        except Exception as e:
            st.error(f"Gagal memuat forum: {e}")
            return {"topik": []}

    def simpan_topik_baru(author, pesan):
        new_entry = {
            "parent_id": None, # Topik utama
            "author": author,
            "pesan": pesan,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": "siswa" # Asumsikan siswa yang membuat topik
        }
        try:
            supabase.table(SUPABASE_TABLE_FORUM).insert(new_entry).execute()
            # Update notifikasi
            update_notifikasi("Forum Diskusi")
        except Exception as e:
            st.error(f"Gagal menyimpan topik baru: {e}")

    def simpan_komentar(parent_id, author, pesan):
        new_entry = {
            "parent_id": parent_id,
            "author": author,
            "pesan": pesan,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": "siswa"
        }
        try:
            supabase.table(SUPABASE_TABLE_FORUM).insert(new_entry).execute()
            # Update notifikasi
            update_notifikasi("Forum Diskusi")
        except Exception as e:
            st.error(f"Gagal menyimpan komentar: {e}")

    # --- Halaman Forum ---
    st.header("💬 Forum Diskusi: Dinamika Rotasi")
    forum_data = muat_forum()

    # --- Form untuk membuat topik baru ---
    st.subheader("📝 Buat Topik Baru")
    with st.form("form_topik_baru"):
        isi_topik = st.text_area("Tulis topik diskusi Anda...")
        kirim_topik = st.form_submit_button("Kirim Topik")

        if kirim_topik:
            if isi_topik.strip():
                simpan_topik_baru(st.session_state.current_user, isi_topik.strip())
                st.success("✅ Topik berhasil dibuat!")
                st.rerun()
            else:
                st.error("❌ Isi topik tidak boleh kosong.")

    # --- Tampilkan daftar topik ---
    st.subheader("📋 Daftar Topik")
    if not forum_data["topik"]:
        st.info("Belum ada topik diskusi. Jadilah yang pertama untuk memulai!")
    else:
        for topik in forum_data["topik"]:
            st.markdown(f"### {topik['pesan']}")
            st.caption(f"Oleh: {topik['author']} | {topik['waktu']}")

            # Form komentar
            with st.form(f"form_komentar_{topik['id']}"):
                isi_komentar = st.text_area(f"Tambahkan komentar untuk topik ini", key=f"isi_komen_{topik['id']}")
                kirim_komentar = st.form_submit_button(f"Kirim Komentar")

                if kirim_komentar:
                    if isi_komentar.strip():
                        simpan_komentar(topik['id'], st.session_state.current_user, isi_komentar.strip())
                        st.success("✅ Komentar berhasil dikirim!")
                        st.rerun()
                    else:
                        st.error("❌ Komentar tidak boleh kosong.")

            # Tampilkan komentar
            for komentar in topik.get("komentar", []):
                st.markdown(f"**{komentar['author']}** - {komentar['waktu']}")
                st.write(komentar['pesan'])

                # Form balasan
                with st.form(f"form_balasan_{topik['id']}_{komentar['id']}"):
                    isi_balasan = st.text_area(f"Balas komentar ini", key=f"isi_balas_{topik['id']}_{komentar['id']}")
                    kirim_balasan = st.form_submit_button(f"Kirim Balasan")

                    if kirim_balasan:
                        if isi_balasan.strip():
                            simpan_komentar(komentar['id'], st.session_state.current_user, isi_balasan.strip())
                            st.success("✅ Balasan berhasil dikirim!")
                            st.rerun()
                        else:
                            st.error("❌ Balasan tidak boleh kosong.")

                # Tampilkan balasan
                df_all = muat_data_supabase(SUPABASE_TABLE_FORUM) # Ambil ulang data untuk menampilkan balasan
                if df_all:
                    balasan_list = [b for b in df_all if b["parent_id"] == komentar["id"]]
                    for balasan in balasan_list:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;└ **{balasan['author']}** - {balasan['waktu']}")
                        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;└ {balasan['pesan']}")

            st.divider()
    reset_notifikasi("Forum Diskusi")

# === MODUL HASIL PENILAIAN ===
def hasil_penilaian():
    if st.session_state.role in ["guru", "admin"]:
        # --- DASBOR GURU: HASIL PENILAIAN ---
        st.header("📊 Hasil Penilaian Siswa")
        try:
            response = supabase.table("hasil_nilai").select("*").execute()
            if response.data:
                df = pd.DataFrame(response.data)
                df_siswa = df[df["role"] == "siswa"]
                st.dataframe(df_siswa[["nama", "jenis_penilaian", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
            else:
                st.info("Belum ada data penilaian.")
        except Exception as e:
            st.error(f"Gagal mengambil data penilaian: {e}")
            st.info("Belum ada data penilaian.")

    else: # Siswa
        # --- DASBOR SISWA: HASIL PENILAIAN ---
        st.header("📊 Hasil Penilaian Anda")
        check_hadir()
        try:
            response = supabase.table("hasil_nilai").select("*").eq("email", st.session_state.current_email).eq("role", "siswa").execute()
            if response.data:
                df_siswa = pd.DataFrame(response.data)
                st.dataframe(df_siswa[["jenis_penilaian", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
            else:
                st.info("Anda belum mengerjakan penilaian.")
        except Exception as e:
            st.error(f"Gagal mengambil data penilaian Anda: {e}")
            st.info("Belum ada data penilaian.")
        reset_notifikasi("Hasil Penilaian")

# === MENU UTAMA ===
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.write(f"👤 **{st.session_state.current_user} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "role", "current_user", "current_email", "hadir", "last_access"]:
            st.session_state.pop(key, None)
        st.rerun()

    # Urutan menu
    menu_options = [
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

    # Tampilkan notifikasi di sidebar untuk siswa
    if st.session_state.role == "siswa":
        st.sidebar.divider()
        st.sidebar.subheader("🔔 Notifikasi")
        # Periksa notifikasi untuk item yang diminta
        items_to_check = ["Pre-test", "Media Pembelajaran", "Simulasi Virtual", "LKPD", "Post-test", "Forum Diskusi", "Hasil Penilaian"]
        for menu_item in items_to_check:
            if periksa_notifikasi(menu_item):
                st.sidebar.warning(f"Ada pembaruan di **{menu_item}**!")

    # Menu navigasi berdasarkan role
    if st.session_state.role in ["guru", "admin"]:
        menu = st.sidebar.selectbox("Navigasi Guru/Admin", menu_options)
    else: # Siswa
        menu = st.sidebar.selectbox("Navigasi Siswa", menu_options)

    # Tampilkan halaman berdasarkan menu dan role
    if menu == "Daftar Hadir":
        daftar_hadir()
    elif menu == "Video Apersepsi":
        video_apersepsi()
    elif menu == "Pre-test":
        pre_test()
    elif menu == "Deskripsi Materi":
        deskripsi_materi()
    elif menu == "Media Pembelajaran":
        media_pembelajaran()
    elif menu == "Simulasi Virtual":
        simulasi_virtual()
    elif menu == "LKPD":
        lkpd()
    elif menu == "Refleksi Siswa":
        refleksi_siswa()
    elif menu == "Post-test":
        post_test()
    elif menu == "Forum Diskusi":
        forum_diskusi()
    elif menu == "Hasil Penilaian":
        hasil_penilaian()

    # Tombol Logout
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "role", "current_user", "current_email", "hadir", "last_access"]:
            st.session_state.pop(key, None)
        st.rerun()