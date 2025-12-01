    elif menu == "Simulasi Virtual":
        if st.session_state.role in ["guru", "admin"]:
            # --- DASBOR GURU: SIMULASI VIRTUAL ---
            st.header("🧪 Edit Simulasi Virtual")
            simulasi_data = muat_data("simulasi_virtual")
            if not simulasi_data:
                st.error("Simulasi virtual belum diatur.")
                st.stop()
            with st.form("form_edit_simulasi"):
                judul_baru = st.text_input("Judul Simulasi Virtual", value=simulasi_data.get("judul", ""))
                desc_baru = st.text_area("Deskripsi", value=simulasi_data.get("deskripsi", ""), height=100)
                petunjuk_baru = st.text_area("Petunjuk Penggunaan (Markdown)", value=simulasi_data.get("petunjuk_penggunaan", ""), height=300)
                # Simulasi List (hanya 1 item untuk Torque)
                simulasi_list = simulasi_data.get("simulasi_list", [])
                if simulasi_list:
                    simulasi = simulasi_list[0] # Hanya ambil simulasi pertama (Torque)
                    st.markdown("#### ⚖️ Simulasi PhET: Torque")
                    judul_sim_baru = st.text_input(f"Judul Simulasi", value=simulasi.get("judul", ""), key=f"sim_judul_0")
                    url_sim_baru = st.text_input(f"URL Simulasi", value=simulasi.get("url", ""), key=f"sim_url_0")
                    sumber_sim_baru = st.text_input(f"Sumber Simulasi", value=simulasi.get("sumber", ""), key=f"sim_sumber_0")
                    simulasi_baru = {
                        "judul": judul_sim_baru,
                        "url": url_sim_baru,
                        "sumber": sumber_sim_baru
                    }
                else:
                    st.error("Simulasi Torque belum diatur.")
                    st.stop()
                submitted = st.form_submit_button("💾 Simpan Simulasi Virtual")
            if submitted:
                data_baru = {
                    "judul": judul_baru,
                    "deskripsi": desc_baru,
                    "petunjuk_penggunaan": petunjuk_baru,
                    "simulasi_list": [simulasi_baru],
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                simpan_data("simulasi_virtual", data_baru)
                # Update notifikasi
                with open(NOTIFIKASI_FILE, "r") as f:
                    notif = json.load(f)
                notif["Simulasi Virtual"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(NOTIFIKASI_FILE, "w") as f:
                    json.dump(notif, f)
                st.success("✅ Simulasi virtual berhasil disimpan!")
            # Tampilkan pratinjau
            st.divider()
            st.subheader("👁️‍🗨️ Pratinjau Simulasi Virtual untuk Siswa")
            st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
            st.info(simulasi_data.get("deskripsi", ""))
            st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))
            for i, sim in enumerate(simulasi_data.get("simulasi_list", []), 1):
                st.markdown(f"#### {i}. {sim['judul']}")
                st.link_button("🔗 Buka Simulasi", sim["url"])

        else: # Siswa
            # --- DASBOR SISWA: SIMULASI VIRTUAL ---
            st.header("🧪 Simulasi Virtual: Dinamika Rotasi")
            check_hadir()
            simulasi_data = muat_data("simulasi_virtual")
            if not simulasi_data:
                st.error("Simulasi virtual belum diatur oleh guru.")
                st.stop()
            st.write(f"**{simulasi_data.get('judul', 'Simulasi Virtual')}**")
            st.info(simulasi_data.get("deskripsi", ""))
            st.markdown(simulasi_data.get("petunjuk_penggunaan", ""))
            simulasi_list = simulasi_data.get("simulasi_list", [])
            if simulasi_list:
                simulasi = simulasi_list[0] # Ambil simulasi pertama (Torque)
                st.markdown(f"#### {simulasi['judul']}")
                st.caption(f"Sumber: {simulasi['sumber']}")
                st.link_button("🔗 Buka Simulasi PhET: Torque", simulasi["url"])
                st.info("💡 **Catatan:** Simulasi akan terbuka di tab baru browser Anda.")
            else:
                st.warning("📁 Simulasi PhET Torque belum diatur oleh guru.")
            reset_notifikasi("Simulasi Virtual")

            elif key == "simulasi_virtual":
                default_data = {
                    "judul": "Simulasi Virtual: Dinamika Rotasi - Torsi (Torque)",
                    "deskripsi": "Eksplorasi konsep Torsi dan Dinamika Rotasi secara interaktif dengan simulasi PhET 'Torque'!",
                    "petunjuk_penggunaan": """📘 **Petunjuk Penggunaan Simulasi PhET: Torque**
💡 Simulasi ini akan membantu Anda memahami hubungan antara gaya, lengan gaya, torsi, momen inersia, dan percepatan sudut.
**Ikuti langkah-langkah berikut untuk menggunakan simulasi:**
1.  **Buka PhET Simulasi**:
    Klik tautan berikut untuk membuka simulasi:  
    🔗 [https://phet.colorado.edu/sims/cheerpj/rotation/latest/rotation.html?simulation=torque](https://phet.colorado.edu/sims/cheerpj/rotation/latest/rotation.html?simulation=torque)
2.  **Pilih Tab "Torque"**:
    Setelah simulasi terbuka, pastikan Anda berada di tab **"Torque"**.
3.  **Eksplorasi Variabel**:
    - **Force**: Atur besar gaya yang diberikan ke roda.
    - **Brake Force**: Aktifkan atau nonaktifkan gaya rem untuk menghentikan putaran.
    - **Applied Force Location**: Geser titik aplikasi gaya untuk mengubah lengan momen (jarak dari pusat).
    - **Mass of the ladybug**: Ubah massa kutu untuk melihat pengaruhnya terhadap momen inersia.
4.  **Amati Perubahan**:
    - Perhatikan bagaimana perubahan gaya dan lengan gaya memengaruhi **Torsi** yang dihasilkan.
    - Amati hubungan antara torsi, momen inersia, dan **Percepatan Sudut** pada grafik.
5.  **Jawab Pertanyaan**:
    - Apa yang terjadi pada percepatan sudut jika gaya diberikan lebih jauh dari pusat?
    - Bagaimana pengaruh massa kutu terhadap percepatan sudut?
    - Jika torsi yang diberikan konstan, bagaimana kecepatan sudut berubah seiring waktu?
> 🎯 **Tujuan**: Memahami prinsip Hukum II Newton untuk Rotasi (τ = Iα) dan faktor-faktor yang memengaruhi torsi dan percepatan sudut.
""",
                    "simulasi_list": [
                        {"judul": "⚖️ Torque (Torsi) - PhET", "url": "https://phet.colorado.edu/sims/cheerpj/rotation/latest/rotation.html?simulation=torque", "sumber": "PhET Colorado"}
                    ],
                    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                with open(file_path, "w", encoding='utf-8') as f:
                    json.dump(default_data, f, indent=4, ensure_ascii=False)