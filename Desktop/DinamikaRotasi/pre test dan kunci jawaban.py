    elif menu == "Pre-test":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: PRE-TEST ---
            st.header("🧠 Kelola Pre-test")
            tab1, tab2, tab3 = st.tabs(["📅 Edit Soal", "🔑 Kunci Jawaban & Rubrik", "📊 Hasil Pre-test"])
            
            # --- Tab 1: Edit Soal ---
            with tab1:
                st.subheader("Pertemuan 1")
                data_p1 = muat_data("pre_test_p1")
                if not data_p1:
                    st.error("Soal pre-test pertemuan 1 belum diatur.")
                    st.stop()
                with st.form("form_edit_pre_p1"):
                    judul_baru = st.text_input("Judul Pre-test", value=data_p1.get("judul", ""))
                    desc_baru = st.text_area("Deskripsi Pre-test", value=data_p1.get("deskripsi", ""), height=150)
                    soal_list = data_p1.get("soal_list", [])
                    soal_baru_list = []
                    for i, soal in enumerate(soal_list):
                        teks_baru = st.text_area(f"Soal {i+1}", value=soal.get("teks", ""), key=f"pre_p1_soal_{i}")
                        soal_baru_list.append({"id": soal.get("id", f"p1_q{i+1}"), "teks": teks_baru})
                    submitted_p1 = st.form_submit_button("💾 Simpan Soal Pre-test Pertemuan 1")
                if submitted_p1:
                    data_baru = {
                        "judul": judul_baru,
                        "deskripsi": desc_baru,
                        "soal_list": soal_baru_list,
                        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    simpan_data("pre_test_p1", data_baru)
                    # Update notifikasi
                    with open(NOTIFIKASI_FILE, "r") as f:
                        notif = json.load(f)
                    notif["Pre-test"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(NOTIFIKASI_FILE, "w") as f:
                        json.dump(notif, f)
                    st.success("✅ Soal pre-test pertemuan 1 berhasil disimpan!")

                st.divider()
                st.subheader("Pertemuan 2")
                data_p2 = muat_data("pre_test_p2")
                if not data_p2:
                    st.error("Soal pre-test pertemuan 2 belum diatur.")
                    st.stop()
                with st.form("form_edit_pre_p2"):
                    judul_baru = st.text_input("Judul Pre-test", value=data_p2.get("judul", ""))
                    desc_baru = st.text_area("Deskripsi Pre-test", value=data_p2.get("deskripsi", ""), height=150)
                    soal_list = data_p2.get("soal_list", [])
                    soal_baru_list = []
                    for i, soal in enumerate(soal_list):
                        teks_baru = st.text_area(f"Soal {i+1}", value=soal.get("teks", ""), key=f"pre_p2_soal_{i}")
                        soal_baru_list.append({"id": soal.get("id", f"p2_q{i+1}"), "teks": teks_baru})
                    submitted_p2 = st.form_submit_button("💾 Simpan Soal Pre-test Pertemuan 2")
                if submitted_p2:
                    data_baru = {
                        "judul": judul_baru,
                        "deskripsi": desc_baru,
                        "soal_list": soal_baru_list,
                        "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    simpan_data("pre_test_p2", data_baru)
                    # Update notifikasi
                    with open(NOTIFIKASI_FILE, "r") as f:
                        notif = json.load(f)
                    notif["Pre-test"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(NOTIFIKASI_FILE, "w") as f:
                        json.dump(notif, f)
                    st.success("✅ Soal pre-test pertemuan 2 berhasil disimpan!")

            # --- Tab 2: Kunci Jawaban & Rubrik ---
            with tab2:
                st.subheader("Rubrik Penilaian Pre-test")
                st.info("Setiap jawaban yang sesuai dengan kunci jawaban akan mendapatkan skor **3**. Skor maksimal adalah **12**.")
                
                st.subheader("Pertemuan 1")
                kunci_p1 = muat_data("kunci_pre_test_p1")
                if not kunci_p1:
                    soal_list_p1 = muat_data("pre_test_p1").get("soal_list", [])
                    kunci_p1 = {soal["id"]: "" for soal in soal_list_p1}
                
                with st.form("form_edit_kunci_p1"):
                    for soal_id in kunci_p1.keys():
                        kunci_p1[soal_id] = st.text_area(f"Kunci Jawaban untuk {soal_id}", value=kunci_p1[soal_id], key=f"kunci_p1_{soal_id}")
                    submit_kunci_p1 = st.form_submit_button("💾 Simpan Kunci Jawaban Pertemuan 1")
                if submit_kunci_p1:
                    simpan_data("kunci_pre_test_p1", kunci_p1)
                    st.success("✅ Kunci jawaban pertemuan 1 berhasil disimpan!")

                st.divider()
                st.subheader("Pertemuan 2")
                kunci_p2 = muat_data("kunci_pre_test_p2")
                if not kunci_p2:
                    soal_list_p2 = muat_data("pre_test_p2").get("soal_list", [])
                    kunci_p2 = {soal["id"]: "" for soal in soal_list_p2}
                
                with st.form("form_edit_kunci_p2"):
                    for soal_id in kunci_p2.keys():
                        kunci_p2[soal_id] = st.text_area(f"Kunci Jawaban untuk {soal_id}", value=kunci_p2[soal_id], key=f"kunci_p2_{soal_id}")
                    submit_kunci_p2 = st.form_submit_button("💾 Simpan Kunci Jawaban Pertemuan 2")
                if submit_kunci_p2:
                    simpan_data("kunci_pre_test_p2", kunci_p2)
                    st.success("✅ Kunci jawaban pertemuan 2 berhasil disimpan!")

            # --- Tab 3: Hasil Pre-test ---
            with tab3:
                st.subheader("Daftar Nilai Pre-test")
                df_nilai = muat_data("hasil_nilai")
                if df_nilai is not None and not df_nilai.empty:
                    df_pretest = df_nilai[df_nilai["jenis_penilaian"].str.contains("Pre-test", na=False)]
                    if not df_pretest.empty:
                        st.dataframe(df_pretest[["nama", "email", "jenis_penilaian", "nilai", "waktu_kerja"]].sort_values(by="waktu_kerja", ascending=False))
                    else:
                        st.info("Belum ada siswa yang mengerjakan Pre-test.")
                else:
                    st.info("Belum ada data penilaian.")

        else: # Siswa
            # --- DASBOR SISWA: PRE-TEST ---
            st.header("🧠 Pre-test: Dinamika Rotasi")
            check_hadir()
            # Pilih pertemuan
            pertemuan = st.selectbox("Pilih Pertemuan:", ["Pertemuan 1", "Pertemuan 2"], key="pilih_pertemuan_pre")
            if pertemuan == "Pertemuan 1":
                data = muat_data("pre_test_p1")
                jenis_penilaian = "Pre-test 1"
                kunci_jawaban = muat_data("kunci_pre_test_p1") or {}
            else:
                data = muat_data("pre_test_p2")
                jenis_penilaian = "Pre-test 2"
                kunci_jawaban = muat_data("kunci_pre_test_p2") or {}

            if not data:
                st.error(f"Soal pre-test {pertemuan} belum diatur oleh guru.")
                st.stop()

            st.write(f"**{data.get('judul', f'Pre-test {pertemuan}')}**")
            st.info(data.get("deskripsi", ""))
            jawaban_dict = {}
            soal_list = data.get("soal_list", [])
            with st.form(f"form_pre_test_{pertemuan.lower().replace(' ', '_')}"):
                for i, soal in enumerate(soal_list):
                    st.markdown(f"#### {i+1}. {soal['teks']}")
                    jawaban = st.text_area("Jawaban Anda:", key=soal["id"], height=100)
                    jawaban_dict[soal["id"]] = jawaban
                submitted = st.form_submit_button(f"✅ Kirim Jawaban Pre-test {pertemuan}")
                if submitted:
                    if any(not v.strip() for v in jawaban_dict.values()):
                        st.error("⚠️ Mohon jawab semua pertanyaan.")
                    else:
                        # --- PENILAIAN OTOMATIS ---
                        nilai_total = 0
                        for soal_id, jawaban_siswa in jawaban_dict.items():
                            kunci = kunci_jawaban.get(soal_id, "").strip().lower()
                            jawaban = jawaban_siswa.strip().lower()
                            # Penilaian sederhana: cek keberadaan kata kunci dari kunci jawaban di jawaban siswa
                            if kunci and all(kata in jawaban for kata in kunci.split()):
                                nilai_total += 3 # Skor penuh jika sesuai
                            # Jika tidak sesuai atau kunci tidak ada, skor = 0 untuk soal tersebut
                        
                        # Simpan jawaban dan nilai ke file CSV
                        df = muat_data("hasil_nilai")
                        jawaban_json_str = json.dumps(jawaban_dict)
                        new_entry = pd.DataFrame([{
                            "email": st.session_state.current_email,
                            "nama": st.session_state.current_user,
                            "jenis_penilaian": jenis_penilaian,
                            "jawaban_json": jawaban_json_str,
                            "nilai": nilai_total,
                            "waktu_kerja": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "role": "siswa"
                        }])
                        df = pd.concat([df, new_entry], ignore_index=True)
                        simpan_data("hasil_nilai", df)
                        
                        # Tampilkan hasil langsung
                        st.success(f"✅ Jawaban pre-test {pertemuan} berhasil dikirim!")
                        st.subheader("📊 Hasil Penilaian Anda")
                        st.metric("Nilai Total", f"{nilai_total}/12")
                        
                        # Berikan feedback berdasarkan nilai
                        if nilai_total == 12:
                            st.balloons()
                            st.success("🎉 Luar biasa! Pemahaman awal Anda sangat baik!")
                        elif nilai_total >= 6:
                            st.info("👍 Bagus! Pemahaman awal Anda cukup baik. Lanjutkan belajar!")
                        else:
                            st.warning("📚 Pemahaman awal Anda perlu ditingkatkan. Jangan khawatir, mari kita pelajari bersama!")
            reset_notifikasi("Pre-test")