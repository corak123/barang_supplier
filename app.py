import streamlit as st
from datetime import datetime
from sheet_helper import tambah_masuk_barang_supplier, tambah_masuk_gudang, tambah_keluar_customer, update_stock_gudang, get_stock_gudang

st.set_page_config(page_title="Manajemen Stok Gudang", layout="wide")
if "reset_form" not in st.session_state:
    st.session_state["reset_form"] = False

st.title("📦 Aplikasi Manajemen Stok Gudang")

menu = st.sidebar.selectbox("Menu", [
    "Masuk Barang (Supplier)", "Keluar (Customer)",
    "Stock Gudang"
])

# Masuk Barang: Semua Form Digabung
if menu == "Masuk Barang (Supplier)":
    st.header("📥 Barang Masuk dari Supplier")

    # Reset semua field kalau flag reset_form True
    if st.session_state["reset_form"]:
        for key in list(st.session_state.keys()):
            if key not in ["reset_form", "menu"]:  # Jangan reset menu dan flag sendiri
                del st.session_state[key]
        st.session_state["reset_form"] = False
        st.rerun()

    with st.form("form_masuk_barang"):
        st.subheader("🧾 Data dari Supplier")
        no_sj = st.text_input("No. SJ Supplier", key="no_sj")
        so_supplier = st.text_input("SO Supplier", key="so_supplier")
        nama_barang_supplier = st.text_input("Nama Barang (Supplier)", key="nama_barang_supplier")
        jumlah_supplier = st.number_input("Jumlah (Supplier)", min_value=0, step=1, key="jumlah_supplier")
        tgl_sj_supplier = st.date_input("Tanggal SJ (Supplier)", value=datetime.today(), key="tgl_sj_supplier")
        ket_supplier = st.text_area("Keterangan (Supplier)", key="ket_supplier")

        st.subheader("🏠 Masuk ke Gudang")
        #nama_barang_gudang = st.text_input("Nama Barang (Gudang)", key="nama_barang_gudang")
        #kode_barang_gudang = st.text_input("Kode Barang", key="kode_barang_gudang")
        kode_barang_gudang = str(st.text_input("Kode Barang", key="kode_barang_gudang"))
        jumlah_gudang = st.number_input("Jumlah (Gudang)", min_value=0, step=1, key="jumlah_gudang")
        so_gudang = st.text_input("SO Gudang", key="so_gudang")
        sj_gudang = st.text_input("No. SJ Gudang", key="sj_gudang")
        po_gudang = st.text_input("PO Gudang", key="po_gudang")
        tgl_sj_gudang = st.date_input("Tanggal SJ (Gudang)", value=datetime.today(), key="tgl_masuk_gudang")
        ket_gudang = st.text_area("Keterangan (Gudang)", key="ket_gudang")

        st.subheader("📤 Keluar ke Customer")
        #nama_barang_customer = st.text_input("Nama Barang (Customer)", key="nama_barang_customer")
        #kode_barang_customer = st.text_input("Kode Barang (Customer)", key="kode_barang_customer")
        jumlah_customer = st.number_input("Jumlah (Customer)", min_value=0, step=1, key="jumlah_customer")
        so_customer = st.text_input("SO Customer", key="so_customer")
        sj_customer = st.text_input("No. SJ Customer", key="sj_customer")
        po_customer = st.text_input("PO Customer", key="po_customer")
        tgl_sj_customer = st.date_input("Tanggal SJ (Customer)", value=datetime.today(), key="tgl_keluar")
        ket_customer = st.text_area("Keterangan (Customer)", key="ket_customer")

        submitted = st.form_submit_button("Tambah Masuk Barang")
        if submitted:
            msg1 = tambah_masuk_barang_supplier(no_sj, so_supplier, nama_barang_supplier, jumlah_supplier, str(tgl_sj_supplier), ket_supplier)
            msg2 = tambah_masuk_gudang(nama_barang_supplier, kode_barang_gudang, jumlah_gudang, so_gudang, sj_gudang, po_gudang, str(tgl_sj_gudang), ket_gudang)
            msg3 = tambah_keluar_customer(nama_barang_supplier, kode_barang_gudang, jumlah_customer, so_customer, sj_customer, po_customer, str(tgl_sj_customer), ket_customer)

            st.success("✅ Data berhasil ditambahkan:")
            st.info(f"- Supplier: {msg1}")
            st.info(f"- Masuk Gudang: {msg2}")
            st.info(f"- Keluar Customer: {msg3}")
            st.session_state["reset_form"] = True
            st.rerun()

elif menu == "Keluar (Customer)":
    st.header("📤 Keluar Barang ke Customer")

    # Inisialisasi session state
    if "cek_barang_done" not in st.session_state:
        st.session_state.cek_barang_done = False
    if "stok_sisa" not in st.session_state:
        st.session_state.stok_sisa = 0
    if "nama_barang_checked" not in st.session_state:
        st.session_state.nama_barang_checked = ""
    if "kode_barang_checked" not in st.session_state:
        st.session_state.kode_barang_checked = ""

    # Step 1: Input nama dan kode barang
    nama_barang = st.text_input("Nama Barang", value=st.session_state.nama_barang_checked)
    kode_barang = st.text_input("Kode Barang", value=st.session_state.kode_barang_checked)

    if st.button("🔍 Cek Barang di Stok"):
        update_msg = update_stock_gudang()
        #st.info(f"🔄 {update_msg}")

        df_stock = get_stock_gudang()
        data_barang = df_stock[df_stock["Kode Barang"] == kode_barang]

        if not data_barang.empty:
            sisa = int(data_barang.iloc[0]["Sisa"])
            st.session_state.stok_sisa = sisa
            st.session_state.cek_barang_done = True
            st.session_state.nama_barang_checked = nama_barang
            st.session_state.kode_barang_checked = kode_barang
            st.success(f"✅ Barang ditemukan. Sisa stok: {sisa}")
        else:
            st.session_state.cek_barang_done = False
            st.error("❌ Barang tidak ditemukan di stock gudang.")

    # Step 2: Jika sudah dicek dan stok tersedia, tampilkan form
    if st.session_state.cek_barang_done and st.session_state.stok_sisa > 0:
        with st.form("form_keluar_customer"):
            jumlah = st.number_input("Jumlah Keluar", min_value=1, max_value=st.session_state.stok_sisa, step=1)
            so = st.text_input("SO")
            sj = st.text_input("SJ")
            po = st.text_input("PO")
            tgl_sj = st.date_input("Tanggal SJ", datetime.today())
            keterangan = st.text_area("Keterangan")

            submitted = st.form_submit_button("Simpan Keluar")
            if submitted:
                tgl_sj_str = tgl_sj.strftime("%Y-%m-%d")
                msg = tambah_keluar_customer(
                    st.session_state.nama_barang_checked,
                    st.session_state.kode_barang_checked,
                    jumlah, so, sj, po, tgl_sj_str, keterangan
                )
                if msg.startswith("✅"):
                    st.success(msg)
                    # Reset session state agar form tidak muncul lagi
                    st.session_state.clear()  # 🔄 Clear semua session state agar form kosong
                    st.rerun()
                    st.session_state.cek_barang_done = False
                else:
                    st.error(msg)


# Update Stock Gudang
elif menu == "Stock Gudang":
    st.header("🔄 Stock Gudang")
    
    if st.button("Update Sekarang"):
        msg = update_stock_gudang()
        st.success(msg)
        st.rerun()  # reload halaman agar data terbaru langsung tampil
    
    # Tampilkan tabel stock (baik setelah reload maupun saat pertama kali buka)
    df_stock = get_stock_gudang()
    if not df_stock.empty:
        st.dataframe(df_stock)
    else:
        st.info("Data stock gudang kosong atau gagal dimuat.")

