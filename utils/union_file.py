import pandas as pd
import glob
import os


def union(FOLDER_PATH):
    # ======================================
    # Step 1: Baca semua file CSV ke dalam list of DataFrames
    # ======================================
    all_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))
    # Exclude file gabungan.csv kalau udah ada
    all_files = [f for f in all_files if "gabungan" not in os.path.basename(f)]

    print(f"📁 Ditemukan {len(all_files)} file CSV")
    print("=" * 60)

    df_list = []
    file_info = []

    for file in all_files:
        # Baca file
        df = pd.read_csv(file, sep=";", encoding="utf-8-sig")

        # Simpan info
        file_info.append(
            {
                "nama_file": os.path.basename(file),
                "jumlah_baris": len(df),
                "jumlah_kolom": len(df.columns),
                "df": df,
            }
        )

        df_list.append(df)

        print(
            f"📄 {os.path.basename(file)}: {len(df):,} baris x {len(df.columns)} kolom"
        )

    # ======================================
    # Step 2: Gabung semua DataFrame
    # ======================================
    print("\n" + "=" * 60)
    print("🔄 Menggabungkan semua DataFrame...")

    result = pd.concat(df_list, ignore_index=True)

    print(f"✅ Hasil gabungan: {len(result):,} baris x {len(result.columns)} kolom")

    # ======================================
    # Step 3: Validasi jumlah baris
    # ======================================
    print("\n" + "=" * 60)
    print("🔍 VALIDASI JUMLAH BARIS")
    print("=" * 60)

    # Hitung total baris dari semua file sebelum digabung
    total_baris_asli = sum([info["jumlah_baris"] for info in file_info])
    total_baris_gabungan = len(result)

    print(f"📊 Total baris dari semua file: {total_baris_asli:,}")
    print(f"📊 Total baris setelah digabung: {total_baris_gabungan:,}")
    print(f"📊 Selisih: {total_baris_asli - total_baris_gabungan:,}")

    if total_baris_asli == total_baris_gabungan:
        print("\n✅ SUKSES! Jumlah baris SAMA persis!")
    else:
        print("\n❌ GAGAL! Jumlah baris BERBEDA!")
        print(f"   Ada {total_baris_asli - total_baris_gabungan} baris yang hilang!")

        # ======================================
        # Step 4: Analisis kenapa baris berkurang
        # ======================================
        print("\n" + "=" * 60)
        print("🔎 ANALISIS PENYEBAB BARIS BERKURANG")
        print("=" * 60)

        # Cek setiap file
        for info in file_info:
            df = info["df"]
            nama = info["nama_file"]

            # Cek duplikasi index
            index_dup = df.index.duplicated().sum()
            if index_dup > 0:
                print(f"⚠️ {nama}: Ada {index_dup} index duplikat")

            # Cek baris kosong (semua NaN)
            empty_rows = df.isna().all(axis=1).sum()
            if empty_rows > 0:
                print(f"⚠️ {nama}: Ada {empty_rows} baris kosong total")

            # Cek duplikasi data (semua kolom sama)
            dup_rows = df.duplicated().sum()
            if dup_rows > 0:
                print(f"⚠️ {nama}: Ada {dup_rows} baris duplikat sempurna")

        # Cek duplikasi di hasil gabungan
        print("\n🔍 Cek duplikasi di hasil gabungan:")
        result_duplicates = result.duplicated().sum()
        if result_duplicates > 0:
            print(f"⚠️ Ada {result_duplicates} baris duplikat di hasil gabungan")
            print(f"   (Ini TIDAK mengurangi jumlah baris, hanya info saja)")

        # Cek index duplikat
        if result.index.duplicated().sum() > 0:
            print(f"⚠️ Ada index duplikat di hasil gabungan")

    # ======================================
    # Step 5: Cek struktur kolom
    # ======================================
    print("\n" + "=" * 60)
    print("📋 CEK STRUKTUR KOLOM")
    print("=" * 60)

    # Cek apakah semua file punya kolom yang sama
    kolom_per_file = [set(info["df"].columns) for info in file_info]
    if all(kolom_per_file[0] == kolom for kolom in kolom_per_file):
        print("✅ Semua file punya struktur kolom yang SAMA")
    else:
        print("⚠️ PERINGATAN: Struktur kolom BERBEDA!")
        for info in file_info:
            print(f"\n📄 {info['nama_file']}:")
            print(f"   Kolom: {list(info['df'].columns)}")

    print(f"\n📋 Kolom hasil gabungan: {list(result.columns)}")

    # ======================================
    # Step 6: Tampilkan sample data
    # ======================================
    print("\n" + "=" * 60)
    print("👀 SAMPLE DATA (5 baris pertama)")
    print("=" * 60)
    print(result.head())

    print("\n" + "=" * 60)
    print("📊 STATISTIK DASAR")
    print("=" * 60)
    print(f"Total baris final: {len(result):,}")
    print(f"Total kolom final: {len(result.columns)}")
    print(f"Memory usage: {result.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # ======================================
    # Step 7: Simpan hasil (opsional)
    # ======================================
    result.to_csv(
        os.path.join(FOLDER_PATH, "gabungan.csv"),
        sep=";",
        index=False,
        encoding="utf-8-sig",
    )
    print(f"✅ Disimpan ke: {os.path.join(FOLDER_PATH, 'gabungan.csv')}")
