import streamlit as st
import pandas as pd
st.set_page_config(page_title="TorMonitor", page_icon="📊", layout="wide")

#status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Beranda"
if "role" not in st.session_state:
    st.session_state["role"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "success" not in st.session_state:
    st.session_state["success"] = False

#data awal
if "karyawan_data" not in st.session_state:
    # Data awal untuk simulasi database
    data_awal = {
        "Nama": ["Roger Sumatra", "Rudi Capkakitiga", "Siti Stabilizer", "Farhan Kebab", "Cahyo Turu", "Mas Ironi", "Bambang Pasundan", "Si Imut", "Budi Perjuangan", "Rehan Wangsaff"],
        "Password": ["roger123", "rudi123", "siti123", "farhan123", "cahyo123", "masironi123", "bambang123", "siimut123", "budi123", "rehan123"],
        "Pelanggaran Ringan": [0] * 10,
        "Pelanggaran Sedang": [0] * 10,
        "Pelanggaran Berat": [0] * 10,
        "Kredit": [0] * 10,
    }

    df_awal = pd.DataFrame(data_awal)
    df_awal["Kredit"] = (100 + df_awal["Pelanggaran Ringan"] * (-5) + df_awal["Pelanggaran Sedang"] * (-15) + df_awal["Pelanggaran Berat"] * (-30))

    st.session_state["karyawan_data"] = df_awal

def login_form(): #Login
    st.markdown("# TorMonitor 1.0")
    with st.form("login_form"):
        st.markdown("#### Masukkan Username dan Password Anda")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login", key="login_button", type="primary")

        if submit_button: #Verifikasi
            if username == "Rusdi Menghilang" and password == "rusdi123":
                st.session_state["logged_in"] = True
                st.success("Login sukses sebagai manajer!")
                st.session_state["role"] = "manajer"
                st.session_state["username"] = "manajer"
                st.rerun()
            else:
                df_karyawan = st.session_state["karyawan_data"]

                user_match = df_karyawan[df_karyawan["Nama"].str.lower() == username.lower()]

                if not user_match.empty:
                    password_user = user_match["Password"].iloc[0]

                    if password == password_user:
                        st.session_state["logged_in"] = True
                        st.session_state["role"] = "user"
                        st.session_state["username"] = user_match["Nama"].iloc[0] # Nama Karyawan yang login
                        st.success(f"Login sukses sebagai {st.session_state['username']}!")
                        st.rerun()
                    else:
                        st.error("Password salah.")
                else:
                    st.error("Invalid username or password.")

def beranda():
    if st.session_state["role"] == "manajer":
        st.title(f"Selamat Datang, {st.session_state['role'].capitalize()}! 👋")
        st.info("Gunakan navigasi di sebelah kiri untuk melihat fitur aplikasi.")
        st.metric(label="Total Karyawan", value=len(st.session_state['karyawan_data']))
        st.markdown("##### Tugas Manajer:")
        st.write("Anda dapat menginput dan melihat rekapitulasi data kredit karyawan.")

    elif st.session_state["role"] == "user":
        st.title(f"Selamat Datang, {st.session_state['username']}! 👋")
        st.info("Gunakan navigasi di sebelah kiri untuk melihat fitur aplikasi.")
        st.markdown("##### Tugas Karyawan:")
        st.write("Anda dapat mengecek gaji berdasarkan kredit Anda.")
       
def about():
    st.markdown("# Tentang Kami")
    st.markdown("""
        ## Kelompok 2   
        ##### Kelas : K-28         
        ##### Anggota : 
            - M. Iqbal Aufa (16425185)
            - M. Rafi' Putra I. (16425280)
            - M. Nabil Zam Zami (16425310)
            - Rifadzaki Abiyyu A. (16425355)
            - Liya Zafirah K. (16425465)
    """)

    st.header("Tentang TorMonitor")
    st.write("""
        TorMonitor merupakan Aplikasi Monitoring Kinerja Karyawan ini dirancang untuk memberikan transparansi dan perhitungan yang jelas mengenai kedisiplinan dan kinerja non-akademik staf.
""")

    st.subheader("Perhitungan Kinerja (Kredit Skor)")
    st.write("""
        Setiap karyawan memulai dengan **100 Kredit Skor**. Kredit Skor ini berkurang berdasarkan tingkat pelanggaran yang dicatat:
        - **Pelanggaran Ringan:** -5 Poin per kejadian.
        - **Pelanggaran Sedang:** -15 Poin per kejadian.
        - **Pelanggaran Berat:** -30 Poin per kejadian.
    """
)
    st.subheader("Fungsi Utama")
    st.markdown("""
        - **Input Kredit (Manajer):** Manajer dapat memperbarui jumlah pelanggaran karyawan secara *real-time* dan melihat skor kredit otomatis diperbarui.
        - **Rekap Kredit (Semua Pengguna):** Menampilkan tabel dan grafik skor kredit terkini. Karyawan hanya melihat skor mereka sendiri, sedangkan Manajer melihat skor seluruh tim.
        - **Kalkulator Gaji (Semua Pengguna):** Mensimulasikan dampak skor kredit pada gaji bulanan dengan batas potongan maksimum 50%.
    """)

    st.subheader("Pengembang")
    st.write("Aplikasi ini dibuat sebagai simulasi sistem monitoring kinerja.")

def input_kredit():
    st.header("Input Pelanggaran Karyawan")
    st.write("Silakan ubah jumlah pelanggaran Ringan (-5), Sedang (-15), dan Berat (-30) di tabel. Nilai Kredit akan diperbarui otomatis setelah tombol Simpan ditekan.")


    df = st.session_state["karyawan_data"].copy()

    df_edit = st.data_editor(df,
        key = "hitung_kredit",
        column_config={
            "Pelanggaran Ringan": st.column_config.NumberColumn(
                min_value=0,
                max_value=50,
                help="-5 poin per pelanggaran ringan",
            ),
            "Pelanggaran Sedang": st.column_config.NumberColumn(
                min_value=0,
                max_value=30,
                help="-15 poin per pelanggaran sedang",
            ),
            "Pelanggaran Berat": st.column_config.NumberColumn(
                min_value=0,
                max_value=20,
                help="-30 poin per pelanggaran berat",
            ),
            "Kredit": st.column_config.NumberColumn(
                format = "%.0f",
                help = "Jumlah kredit karyawan setelah dikurangi poin pelanggaran",
            ),
        },
        disabled=["Nama", "Kredit"],
        hide_index=False,
    )

    if st.button("Simpan & Hitung Kredit", type="primary", key="hitung_button"):
        try:
            df_edit["Pelanggaran Ringan"] = df_edit["Pelanggaran Ringan"].fillna(0).astype(int)
            df_edit["Pelanggaran Sedang"] = df_edit["Pelanggaran Sedang"].fillna(0).astype(int)
            df_edit["Pelanggaran Berat"] = df_edit["Pelanggaran Berat"].fillna(0).astype(int)

            df_edit["Kredit"] = (100 + df_edit["Pelanggaran Ringan"] * (-5) + df_edit["Pelanggaran Sedang"] * (-15) + df_edit["Pelanggaran Berat"] * (-30))
            st.session_state["karyawan_data"] = df_edit
            st.session_state["success"] = True
            st.rerun()

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    if st.session_state["success"] == True:
        st.success("Data kredit karyawan berhasil diperbarui!")
        st.session_state["success"] = False

def rekap_kredit():
    st.header("Rekapitulasi Kredit Karyawan")
    st.write("Menampilkan rekap kredit karyawan.")

    df_rekap = st.session_state["karyawan_data"].copy()

    st.subheader("Tabel Rekap Kredit Karyawan")
    st.dataframe(df_rekap, use_container_width=True)

    st.subheader("Visualisasi Kredit Karyawan")
    st.bar_chart(df_rekap.set_index("Nama")["Kredit"])

    st.header("Kalkulator Gaji Karyawan")

    gajiAwal = 10000000 # Gaji awal karyawan
    
    # Menampilkan data karyawan untuk referensi
    st.subheader("Skor Kredit Karyawan (Dari Data Saat Ini)")

    karyawan_pilih = st.selectbox("Pilih Karyawan yang Akan Dicek Gajinya:", 
                                  st.session_state['karyawan_data']['Nama'].tolist())
    
    # Ambil skor kredit dari data state
    skor_kredit = st.session_state['karyawan_data'][st.session_state['karyawan_data']['Nama'] == karyawan_pilih]['Kredit'].iloc[0]

    st.metric(label=f"Kredit Skor {karyawan_pilih}", value=skor_kredit)
    
    if st.button("Hitung Gaji Akhir", key="hitung_gaji"):
        # Ambil nilai positif dari skor kredit (contoh: -15 menjadi 15)

        max_potongan = 0.50 #Maksimum Potongan 50%

        persentase_potongan = min((100-skor_kredit) / 100, max_potongan) 
        
        gajiAkhir = gajiAwal * (1 - persentase_potongan)
        
        st.success(f"Karyawan: **{karyawan_pilih}**")
        st.info(f"Skor Kredit: {skor_kredit} | Potongan Gaji: {persentase_potongan * 100:.0f}%")
        st.markdown(f"**Gaji Akhir Karyawan:** <h3 style='color: green;'>Rp {gajiAkhir:,.0f}</h3>", unsafe_allow_html=True)

def cek_gaji():
    st.header("Cek Gaji Karyawan")

    karyawan = st.session_state["username"]
    data = st.session_state["karyawan_data"]

    gajiAwal = 10000000 #Gaji awal karyawan
    gajiAkhir = 0
    kreditSkor = data[data["Nama"] == karyawan]["Kredit"].iloc[0]
    st.metric(label=f"Kredit Skor {karyawan}", value=kreditSkor)

    if st.button("Hitung Gaji Akhir", key="hitung_gaji"):
        # Ambil nilai positif dari kredit skor (contoh: -15 menjadi 15)

        max_potongan = 0.50 # Maksimum Potongan 50%
        persentase_potongan = min((100 - kreditSkor) / 100, max_potongan) 
        
        gajiAkhir = gajiAwal * (1 - persentase_potongan)
        
        st.success(f"Karyawan: **{karyawan}**")
        st.info(f"Kredit Skor: {kreditSkor} | Potongan Gaji: {persentase_potongan * 100:.0f}%")
        st.markdown(f"**Gaji Akhir Karyawan:** <h3 style='color: green;'>Rp {gajiAkhir:,.0f}</h3>", unsafe_allow_html=True)

def main_app():
    #Navigasi
    st.sidebar.title("Navigasi")
    st.sidebar.markdown("Pilih halaman:")
    
    #Tombol menu navigasi per role
    if st.session_state["role"] == "manajer": #Menu untuk manajer
        if st.sidebar.button("Beranda", type="tertiary", use_container_width=True, key="beranda_manajer"):
            st.session_state["current_page"] = "Beranda"
            st.rerun()

        if st.sidebar.button("Input Kredit", type="tertiary", use_container_width=True, key="pantau_rekap"):
            st.session_state["current_page"] = "Input Kredit"
            st.rerun()
        
        if st.sidebar.button("Rekap Kredit", type="tertiary", use_container_width=True, key="cek_gaji"):
            st.session_state["current_page"] = "Rekap Kredit"
            st.rerun()
        
        if st.sidebar.button("Tentang Kami", type="tertiary", use_container_width=True, key="about"):
            st.session_state["current_page"] = "About"
            st.rerun()

    elif st.session_state["role"] == "user": #Menu untuk user
        if st.sidebar.button("Beranda", type="tertiary", use_container_width=True, key="beranda_user"):
            st.session_state["current_page"] = "Beranda"
            st.rerun()

        if st.sidebar.button("Kalkulator Gaji", type="tertiary", use_container_width=True, key="cek_gaji"):
            st.session_state["current_page"] = "Kalkulator Gaji"
            st.rerun()
            
        if st.sidebar.button("Tentang Kami", type="tertiary", use_container_width=True, key="about"):
            st.session_state["current_page"] = "About"
            st.rerun()

    #Tombol Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", type="primary", use_container_width=True, key="logout"):
        st.session_state["logged_in"] = False
        st.session_state["current_page"] = "Beranda" #Reset halaman juga
        st.rerun()
    
    # Memanggil fungsi halaman (mengubah "current_page" sesuai tombol yang ditekan)
    if st.session_state["current_page"] == "Beranda":
        beranda()
    elif st.session_state["current_page"] == "About":
        about()
    elif st.session_state["current_page"] == "Kalkulator Gaji":
        cek_gaji()
    elif st.session_state["current_page"] == "Input Kredit":
        input_kredit()
    elif st.session_state["current_page"] == "Rekap Kredit":
        rekap_kredit()

#Algoritma mengecek sesi login
if not st.session_state["logged_in"]:
    login_form()
else:
    main_app()
