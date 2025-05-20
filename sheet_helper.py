import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Setup credentials
secrets = st.secrets["google_service_account"]
creds = Credentials.from_service_account_info(secrets, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])
client = gspread.authorize(creds)

# Load sheets
SPREADSHEET_NAME = "stock_gudang_2"
sheet = client.open(SPREADSHEET_NAME)

masuk_barang_sheet = sheet.worksheet("masuk_barang_supplier")
masuk_gudang_sheet = sheet.worksheet("masuk_gudang")
keluar_sheet = sheet.worksheet("keluar")
stock_sheet = sheet.worksheet("stock_gudang")

# Fungsi: Tambah Masuk Barang Supplier
def tambah_masuk_barang_supplier(no_sj, so, nama_barang, jumlah, tgl_sj, keterangan):
    try:
        masuk_barang_sheet.append_row([
            no_sj, so, nama_barang, jumlah, tgl_sj, keterangan
        ])
        return "✅ Data barang masuk berhasil disimpan."
    except Exception as e:
        return f"❌ Gagal menyimpan data: {e}"

# Fungsi: Tambah Masuk Gudang
def tambah_masuk_gudang(nama_barang, kode_barang, jumlah, so, sj, po, tgl_sj, keterangan):
    try:
        masuk_gudang_sheet.append_row([
            nama_barang, kode_barang, jumlah, so, sj, po, tgl_sj, keterangan
        ])
        return "✅ Barang berhasil dimasukkan ke gudang."
    except Exception as e:
        return f"❌ Gagal simpan ke gudang: {e}"

# Fungsi: Tambah Keluar ke Customer
def tambah_keluar_customer(nama_barang, kode_barang, jumlah, so, sj, po, tgl_sj, keterangan):
    try:
        keluar_sheet.append_row([
            nama_barang, kode_barang, jumlah, so, sj, po, tgl_sj, keterangan
        ])
        return "✅ Barang berhasil dikeluarkan ke customer."
    except Exception as e:
        return f"❌ Gagal simpan data keluar: {e}"

# Fungsi: Update Stock Gudang
def update_stock_gudang():
    try:
        masuk_data = masuk_gudang_sheet.get_all_records()
        keluar_data = keluar_sheet.get_all_records()

        stock = {}

        # Proses barang masuk
        for row in masuk_data:
            kode = row["Kode Barang"]
            nama = row["Nama Barang"]
            jumlah = int(row["Jumlah"])
            if kode not in stock:
                stock[kode] = {"nama": nama, "masuk": 0, "keluar": 0}
            stock[kode]["masuk"] += jumlah

        # Proses barang keluar
        for row in keluar_data:
            kode = row["Kode Barang"]
            jumlah = int(row["Jumlah"])
            if kode in stock:
                stock[kode]["keluar"] += jumlah

        # Tulis ke sheet stock
        stock_sheet.clear()
        stock_sheet.append_row(["Kode Barang", "Nama Barang", "Total Masuk", "Total Keluar", "Sisa"])
        for kode, info in stock.items():
            sisa = info["masuk"] - info["keluar"]
            stock_sheet.append_row([kode, info["nama"], info["masuk"], info["keluar"], sisa])
        return "✅ Stock berhasil diupdate."
    except Exception as e:
        return f"❌ Gagal update stock: {e}"
