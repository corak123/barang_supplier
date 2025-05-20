import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Manajemen Stok Gudang", layout="wide")
st.title("📦 Aplikasi Manajemen Stok Gudang")

menu = st.sidebar.radio("Menu", [
    "Masuk Barang (Supplier)",
    "Masuk ke Gudang",
    "Keluar ke Customer",
    "Update Stock Gudang"
])

# 1. Masuk Barang dari Supplier
if menu == "Masuk Barang (Supplier)":
    st.header("📥 Barang Masuk dari Supplier")
    with st.form("form_supplier"):
        no_sj = st.text_input("No. SJ Supplier")
        so = st.text_input("SO")
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        tgl_sj = st.date_input("Tanggal SJ", value=datetime.today())
        keterangan = st.text_area("Keterangan")

        submitted = st.form_submit_button("Simpan")
        if submitted:
            msg = tambah_masuk_barang_supplier(no_sj, so, nama_barang, jumlah, str(tgl_sj), keterangan)
            st.success(msg)

# 2. Masuk ke Gudang
elif menu == "Masuk ke Gudang":
    st.header("🏠 Barang Masuk ke Gudang")
    with st.form("form_gudang"):
        nama_barang = st.text_input("Nama Barang")
        kode_barang = st.text_input("Kode Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        so = st.text_input("SO")
        sj = st.text_input("No. SJ")
        po = st.text_input("PO")
        tgl_sj = st.date_input("Tanggal SJ", value=datetime.today(), key="tgl_masuk_gudang")
        keterangan = st.text_area("Keterangan")

        submitted = st.form_submit_button("Simpan")
        if submitted:
            msg = tambah_masuk_gudang(nama_barang, kode_barang, jumlah, so, sj, po, str(tgl_sj), keterangan)
            st.success(msg)

# 3. Keluar ke Customer
elif menu == "Keluar ke Customer":
    st.header("📤 Barang Keluar ke Customer")
    with st.form("form_keluar"):
        nama_barang = st.text_input("Nama Barang")
        kode_barang = st.text_input("Kode Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        so = st.text_input("SO")
        sj = st.text_input("No. SJ")
        po = st.text_input("PO")
        tgl_sj = st.date_input("Tanggal SJ", value=datetime.today(), key="tgl_keluar")
        keterangan = st.text_area("Keterangan")

        submitted = st.form_submit_button("Simpan")
        if submitted:
            msg = tambah_keluar_customer(nama_barang, kode_barang, jumlah, so, sj, po, str(tgl_sj), keterangan)
            st.success(msg)

# 4. Update Stock Gudang
elif menu == "Update Stock Gudang":
    st.header("🔄 Update Stock Gudang")
    if st.button("Update Sekarang"):
        msg = update_stock_gudang()
        st.success(msg)
