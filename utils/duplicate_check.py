import pandas as pd

FILE_NAME = "produk/ref_produk.csv"
# FILE_NAME = "payment/ref_payment.csv"
df = pd.read_csv(FILE_NAME, sep=",", encoding="utf-8")

# FILE_NAME = "hasil_merge_deskripsi.csv"
# FILE_NAME = "master_produk_dengan_coicop.csv"
# df = pd.read_csv(FILE_NAME, sep=";", encoding="utf-8-sig")

# ======================================
# CEK DUPLIKAT DI DF (DESKRIPSI)
# ======================================
print("\n" + "=" * 70)
print("PEMERIKSAAN DUPLIKAT DI DF")
print("=" * 70)

if "deskripsi" in df.columns:
    # Cek duplikat perfect match
    duplikat_mask = df["deskripsi"].duplicated(keep=False)
    duplikat_count = duplikat_mask.sum()
    duplikat_unique = df[duplikat_mask]["deskripsi"].nunique()

    print(f"Total baris: {len(df):,}")
    print(f"Total nilai unik: {df['deskripsi'].nunique():,}")
    print(f"Baris yang duplikat: {duplikat_count:,}")
    print(f"Nilai yang muncul lebih dari 1x: {duplikat_unique:,}")

    if duplikat_count > 0:
        # Tampilkan nilai yang duplikat
        duplikat_values = df[df["deskripsi"].duplicated(keep=False)][
            "deskripsi"
        ].value_counts()
        print(f"\n🔍 Nilai duplikat (perfect match):")
        print(duplikat_values.head(10))

        # Tampilkan contoh duplikat
        print(f"\n📋 Contoh baris duplikat:")
        contoh_duplikat = (
            df[df["deskripsi"].duplicated(keep=False)].sort_values("deskripsi").head(10)
        )
        for idx, row in contoh_duplikat.iterrows():
            print(f"  '{row['deskripsi']}'")

        # Simpan daftar duplikat
        df_duplikat = df[df["deskripsi"].duplicated(keep=False)].sort_values(
            "deskripsi"
        )
        df_duplikat.to_csv(
            "df_duplikat_deskripsi.csv", sep=";", index=False, encoding="utf-8-sig"
        )
        print(f"\n💾 Daftar duplikat disimpan ke 'df_duplikat_deskripsi.csv'")
    else:
        print("✅ TIDAK ADA duplikat di df")
