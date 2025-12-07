import streamlit as st
import pandas as pd
import os

FILE_NAME = "pengeluaran.csv"

# -------------------------------------------------------
# 1. CEK FILE
# -------------------------------------------------------
def prepare_csv():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["ID", "Tanggal", "Kategori", "Jumlah", "Catatan"])
        df.to_csv(FILE_NAME, index=False)

def load_data():
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False)


# -------------------------------------------------------
# APP STREAMLIT
# -------------------------------------------------------
def app():
    st.title("Aplikasi Pelacak Pengeluaran")

    prepare_csv()
    df = load_data()

    menu = st.sidebar.selectbox("Menu", ["Tambah Data", "Lihat Data", "Hapus Data"])

    # ---------------- TAMBAH DATA ----------------
    if menu == "Tambah Data":
        st.subheader("Tambah Pengeluaran Baru")

        tanggal = st.date_input("Tanggal")
        kategori = st.text_input("Kategori")
        jumlah = st.number_input("Jumlah (Rp)", min_value=0.0, step=500.0)
        catatan = st.text_area("Catatan")

        if st.button("🚀 Simpan Data"):
            new_id = 1 if df.empty else df["ID"].max() + 1

            df.loc[len(df)] = [
                new_id,
                str(tanggal),
                kategori,
                jumlah,
                catatan
            ]

            save_data(df)
            st.success("Data berhasil ditambahkan!")

    # ---------------- LIHAT DATA ----------------
    elif menu == "Lihat Data":
        st.subheader("Daftar Pengeluaran")
        if df.empty:
            st.info("Belum ada data.")
        else:
            st.dataframe(df)

    # ---------------- HAPUS DATA ----------------
    elif menu == "Hapus Data":
        st.subheader("🗑 Hapus Pengeluaran")

        if df.empty:
            st.info("Tidak ada data yang bisa dihapus.")
        else:
            pilih_id = st.selectbox("Pilih ID yang akan dihapus:", df["ID"])

            if st.button("Hapus"):
                df = df[df["ID"] != pilih_id]
                save_data(df)
                st.success("Data berhasil dihapus!")


# RUN
if __name__ == "__main__":
    app()
