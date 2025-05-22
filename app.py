import streamlit as st
from datetime import datetime
from sheet_helper import tambah_masuk_barang_supplier, tambah_masuk_gudang, tambah_keluar_customer, update_stock_gudang, get_stock_gudang

st.set_page_config(page_title="Manajemen Stok Gudang", layout="wide")
st.title("📦 Aplikasi Manajemen Stok Gudang")

menu = st.sidebar.selectbox("Menu", [
    "Masuk Barang (Supplier)", "Keluar (Customer)",
    "Stock Gudang"
])

# Masuk Barang: Semua Form Digabung
if menu == "Masuk Barang (Supplier)":
    st.header("📥 Barang Masuk dari Supplier")
    with st.form("form_masuk_barang"):
        st.subheader("🧾 Data dari Supplier")
        no_sj = st.text_input("No. SJ Supplier")
        so_supplier = st.text_input("SO Supplier")
        nama_barang_supplier = st.text_input("Nama Barang (Supplier)")
        jumlah_supplier = st.number_input("Jumlah (Supplier)", min_value=1, step=1)
        tgl_sj_supplier = st.date_input("Tanggal SJ (Supplier)", value=datetime.today())
        ket_supplier = st.text_area("Keterangan (Supplier)")

        st.subheader("🏠 Masuk ke Gudang")
        nama_barang_gudang = st.text_input("Nama Barang (Gudang)")
        kode_barang_gudang = st.text_input("Kode Barang")
        jumlah_gudang = st.number_input("Jumlah (Gudang)", min_value=1, step=1)
        so_gudang = st.text_input("SO Gudang")
        sj_gudang = st.text_input("No. SJ Gudang")
        po_gudang = st.text_input("PO Gudang")
        tgl_sj_gudang = st.date_input("Tanggal SJ (Gudang)", value=datetime.today(), key="tgl_masuk_gudang")
        ket_gudang = st.text_area("Keterangan (Gudang)")

        st.subheader("📤 Keluar ke Customer")
        nama_barang_customer = st.text_input("Nama Barang (Customer)")
        kode_barang_customer = st.text_input("Kode Barang (Customer)")
        jumlah_customer = st.number_input("Jumlah (Customer)", min_value=1, step=1)
        so_customer = st.text_input("SO Customer")
        sj_customer = st.text_input("No. SJ Customer")
        po_customer = st.text_input("PO Customer")
        tgl_sj_customer = st.date_input("Tanggal SJ (Customer)", value=datetime.today(), key="tgl_keluar")
        ket_customer = st.text_area("Keterangan (Customer)")

        submitted = st.form_submit_button("Tambah Masuk Barang")
        if submitted:
            msg1 = tambah_masuk_barang_supplier(no_sj, so_supplier, nama_barang_supplier, jumlah_supplier, str(tgl_sj_supplier), ket_supplier)
            msg2 = tambah_masuk_gudang(nama_barang_gudang, kode_barang_gudang, jumlah_gudang, so_gudang, sj_gudang, po_gudang, str(tgl_sj_gudang), ket_gudang)
            msg3 = tambah_keluar_customer(nama_barang_customer, kode_barang_customer, jumlah_customer, so_customer, sj_customer, po_customer, str(tgl_sj_customer), ket_customer)

            st.success("✅ Data berhasil ditambahkan:")
            st.info(f"- Supplier: {msg1}")
            st.info(f"- Masuk Gudang: {msg2}")
            st.info(f"- Keluar Customer: {msg3}")

elif menu == "Keluar (Customer)":
    st.header("📤 Keluar Barang ke Customer")

    # Step 1: Input awal
    nama_barang = st.text_input("Nama Barang")
    kode_barang = st.text_input("Kode Barang")
    cek_btn = st.button("🔍 Cek Barang di Stok")

    # Step 2: Cek stok
    if cek_btn and kode_barang:
        msg = update_stock_gudang()
        st.success(msg)
        df_stock = get_stock_gudang()
        data_barang = df_stock[df_stock["Kode Barang"] == kode_barang]

        if not data_barang.empty:
            sisa = int(data_barang.iloc[0]["Sisa"])
            st.success(f"✅ Barang ditemukan. Sisa stok: {sisa}")

            # Step 3: Form lanjutan jika stok tersedia
            if sisa > 0:
                with st.form("form_keluar_customer"):
                    jumlah = st.number_input("Jumlah Keluar", min_value=1, max_value=sisa, step=1)
                    so = st.text_input("SO")
                    sj = st.text_input("SJ")
                    po = st.text_input("PO")
                    tgl_sj = st.date_input("Tanggal SJ", datetime.today())
                    keterangan = st.text_area("Keterangan")

                    submitted = st.form_submit_button("Simpan Keluar")
                    if submitted:
                        tgl_sj_str = tgl_sj.strftime("%Y-%m-%d")
                        msg = tambah_keluar_customer(nama_barang, kode_barang, jumlah, so, sj, po, tgl_sj_str, keterangan)
                        if msg.startswith("✅"):
                            st.success(msg)
                        else:
                            st.error(msg)
            else:
                st.warning("⚠️ Stok 0, tidak bisa mengeluarkan barang.")
        else:
            st.error("❌ Barang tidak ditemukan di stock gudang.")


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

