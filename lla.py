import pandas as pd
import os

LLA_FILE_1 = "data/050526/lla_2025_202605051134.csv"
LLA_FILE_2 = "data/050526/lla_2026_202605051138.csv"

NON_LLA_FILE_1 = "data/050526/non_lla_2025_202605051140.csv"
NON_LLA_FILE_2 = "data/050526/non_lla_2026_202605051141.csv"

OUTPUT_FOLDER = "output/050526"


# ######################################
# LLA
# ######################################

# ======================================
# Step 1: Baca dan gabung file
# ======================================
# Baca dua file CSV
df1_lla = pd.read_csv(
    LLA_FILE_1,
    sep=";",
    encoding="utf-8",
)
df2_lla = pd.read_csv(
    LLA_FILE_2,
    sep=";",
    encoding="utf-8",
)

# Append (gabung baris)
df_gabung_lla = pd.concat([df1_lla, df2_lla], ignore_index=True)
print("Sample data awal:")
print(df_gabung_lla.head(10))
print("\nInfo tipe data:")
print(df_gabung_lla.dtypes)


# ======================================
# Step 2: Cek nilai sebelum replace
# ======================================
print("\n" + "=" * 50)
print("PENGECEKAN NILAI SEBELUM REPLACE")
print("=" * 50)

# Cek nilai 478118376000000
nilai1 = 478118376000000
cek1 = df_gabung_lla["input_data"] == nilai1
jumlah1 = cek1.sum()

print(f"\nNilai yang dicari: {nilai1}")
print(f"Jumlah baris dengan nilai {nilai1}: {jumlah1}")
if jumlah1 > 0:
    print(f"Index baris yang mengandung nilai {nilai1}:")
    print(df_gabung_lla[cek1].index.tolist())
    print("\nSample data yang mengandung nilai tersebut:")
    print(df_gabung_lla[cek1])

# Cek nilai 471746056000000
nilai2 = 471746056000000
cek2 = df_gabung_lla["input_data"] == nilai2
jumlah2 = cek2.sum()

print(f"\nNilai yang dicari: {nilai2}")
print(f"Jumlah baris dengan nilai {nilai2}: {jumlah2}")
if jumlah2 > 0:
    print(f"Index baris yang mengandung nilai {nilai2}:")
    print(df_gabung_lla[cek2].index.tolist())
    print("\nSample data yang mengandung nilai tersebut:")
    print(df_gabung_lla[cek2])


# ======================================
# Step 3: Replace Value (hanya jika ada)
# ======================================
print("\n" + "=" * 50)
print("PROSES REPLACE")
print("=" * 50)

if jumlah1 > 0:
    df_gabung_lla.loc[:, "input_data"] = df_gabung_lla["input_data"].replace(
        478118376000000, 478118376
    )
    print(f"✓ Sudah replace {jumlah1} baris nilai {478118376000000} -> {478118376}")
else:
    print(f"⚠ Nilai {478118376000000} tidak ditemukan, skip replace")

if jumlah2 > 0:
    df_gabung_lla.loc[:, "input_data"] = df_gabung_lla["input_data"].replace(
        471746056000000, 471746056
    )
    print(f"✓ Sudah replace {jumlah2} baris nilai {471746056000000} -> {471746056}")
else:
    print(f"⚠ Nilai {471746056000000} tidak ditemukan, skip replace")


# ======================================
# Step 4: Verifikasi hasil replace
# ======================================
print("\n" + "=" * 50)
print("VERIFIKASI HASIL REPLACE")
print("=" * 50)

if jumlah1 > 0:
    cek1_setelah = (df_gabung_lla["input_data"] == 478118376).sum()
    print(f"Jumlah nilai {478118376} setelah replace: {cek1_setelah}")

if jumlah2 > 0:
    cek2_setelah = (df_gabung_lla["input_data"] == 471746056).sum()
    print(f"Jumlah nilai {471746056} setelah replace: {cek2_setelah}")

print("\nSample data setelah replace:")
print(df_gabung_lla.head(10))


# ======================================
# Step 5: Baca file ref_produk
# ======================================
REF_PRODUK_FILE = "produk/ref_produk.csv"
# Baca dua file CSV
df_ref_produk = pd.read_csv(
    REF_PRODUK_FILE,
    sep=",",
    encoding="utf-8",
)

print("\n" + "=" * 50)
print("DATA REF_PRODUK")
print("=" * 50)
print("Sample data ref_produk:")
print(df_ref_produk.head(10))
print("\nInfo tipe data ref_produk:")
print(df_ref_produk.dtypes)


# ======================================
# Step 6: Merge (Left Outer Join) dengan ref_produk
# ======================================
print("\n" + "=" * 50)
print("PROSES LEFT OUTER JOIN")
print("=" * 50)

# Cek duplikasi di ref_produk sebelum join
print("\nCek duplikasi di df_ref_produk berdasarkan 'deskripsi':")
jumlah_duplikat = df_ref_produk.duplicated(subset=["deskripsi"]).sum()
print(f"Jumlah baris duplikat di ref_produk: {jumlah_duplikat}")

if jumlah_duplikat > 0:
    print("\n⚠ PERINGATAN: Ada duplikasi deskripsi di ref_produk!")
    print("Sample duplikasi:")
    duplikat_check = df_ref_produk[
        df_ref_produk.duplicated(subset=["deskripsi"], keep=False)
    ]
    print(duplikat_check.sort_values("deskripsi").head(10))

    # Opsional: Ambil yang pertama saja untuk setiap deskripsi
    print("\n>>> Menghilangkan duplikasi di ref_produk (keep='first')")
    df_ref_produk_unique = df_ref_produk.drop_duplicates(
        subset=["deskripsi"], keep="first"
    )
    print(
        f"Jumlah baris setelah drop duplikat: {len(df_ref_produk_unique)} vs sebelumnya {len(df_ref_produk)}"
    )
else:
    df_ref_produk_unique = df_ref_produk
    print("✓ Tidak ada duplikasi di ref_produk")

# Left Outer Join berdasarkan kolom "deskripsi" dengan match perfect
print(
    "\nMelakukan LEFT OUTER JOIN (perfect match termasuk spasi, huruf besar/kecil)..."
)
df_merged = df_gabung_lla.merge(
    df_ref_produk_unique,
    on="deskripsi",  # Kolom yang di-join (perfect match)
    how="left",  # Left Outer Join
    suffixes=("", "_ref"),  # Untuk membedakan kolom dengan nama sama (jika ada)
)

print(f"\nJumlah baris sebelum join: {len(df_gabung_lla)}")
print(f"Jumlah baris setelah join: {len(df_merged)}")
print(f"Jumlah kolom setelah join: {len(df_merged.columns)}")

# Verifikasi jumlah baris tetap sama
if len(df_merged) == len(df_gabung_lla):
    print("\n✓ SUKSES! Jumlah baris tetap sama seperti df_gabung_lla")
else:
    print(
        f"\n⚠ PERINGATAN! Jumlah baris berubah dari {len(df_gabung_lla)} menjadi {len(df_merged)}"
    )

# Cek hasil join (lihat kolom dari ref_produk)
print("\nKolom baru dari ref_produk:")
ref_columns = [col for col in df_merged.columns if col not in df_gabung_lla.columns]
print(ref_columns)

print("\nSample data setelah join (5 baris pertama):")
print(df_merged.head(5))

# Cek apakah ada data yang tidak match (null values di kolom ref_produk)
print("\nCek data yang tidak match (null values dari hasil join):")
if ref_columns:
    null_count = df_merged[ref_columns[0]].isna().sum() if ref_columns else 0
    print(f"Jumlah baris yang tidak match (null di kolom ref): {null_count}")
    persentase_null = (null_count / len(df_merged)) * 100
    print(f"Persentase tidak match: {persentase_null:.2f}%")

    if null_count > 0:
        print("\nSample 'deskripsi' yang tidak match (5 baris):")
        tidak_match = df_merged[df_merged[ref_columns[0]].isna()]
        print(tidak_match[["deskripsi"]].head(5))

# Cek match perfect (termasuk spasi, huruf besar/kecil)
print("\n" + "=" * 50)
print("VERIFIKASI PERFECT MATCH")
print("=" * 50)
print("Contoh 5 nilai 'deskripsi' dari df_gabung_lla:")
print(df_gabung_lla["deskripsi"].head(5))
print("\nContoh 5 nilai 'deskripsi' dari df_ref_produk_unique:")
print(df_ref_produk_unique["deskripsi"].head(5))


# ======================================
# Step 7: Baca file ref_payment
# ======================================
REF_PAYMENT_FILE = "payment/ref_payment.csv"
# Baca dua file CSV
df_ref_payment = pd.read_csv(
    REF_PAYMENT_FILE,
    sep=",",
    encoding="utf-8",
)

print("\n" + "=" * 50)
print("DATA REF_PAYMENT")
print("=" * 50)
print("Sample data ref_payment:")
print(df_ref_payment.head(10))
print("\nInfo tipe data ref_payment:")
print(df_ref_payment.dtypes)


# ======================================
# Step 8: Merge (Left Outer Join) dengan ref_payment
# ======================================
print("\n" + "=" * 50)
print("PROSES LEFT OUTER JOIN DENGAN REF_PAYMENT")
print("=" * 50)

# Cek duplikasi di ref_payment sebelum join
print("\nCek duplikasi di df_ref_payment berdasarkan 'deskripsi':")
jumlah_duplikat_payment = df_ref_payment.duplicated(subset=["deskripsi"]).sum()
print(f"Jumlah baris duplikat di ref_payment: {jumlah_duplikat_payment}")

if jumlah_duplikat_payment > 0:
    print("\n⚠ PERINGATAN: Ada duplikasi deskripsi di ref_payment!")
    print("Sample duplikasi:")
    duplikat_check_payment = df_ref_payment[
        df_ref_payment.duplicated(subset=["deskripsi"], keep=False)
    ]
    print(duplikat_check_payment.sort_values("deskripsi").head(10))

    # Ambil yang pertama saja untuk setiap deskripsi
    print("\n>>> Menghilangkan duplikasi di ref_payment (keep='first')")
    df_ref_payment_unique = df_ref_payment.drop_duplicates(
        subset=["deskripsi"], keep="first"
    )
    print(
        f"Jumlah baris setelah drop duplikat: {len(df_ref_payment_unique)} vs sebelumnya {len(df_ref_payment)}"
    )
else:
    df_ref_payment_unique = df_ref_payment
    print("✓ Tidak ada duplikasi di ref_payment")

# Left Outer Join berdasarkan kolom "deskripsi"
print("\nMelakukan LEFT OUTER JOIN dengan ref_payment...")
df_merged = df_merged.merge(
    df_ref_payment_unique,
    on="deskripsi",  # Kolom yang di-join (perfect match)
    how="left",  # Left Outer Join
)

print(f"\nJumlah baris setelah join dengan ref_payment: {len(df_merged)}")
print(f"Jumlah kolom setelah join: {len(df_merged.columns)}")

# Verifikasi jumlah baris tetap sama
if len(df_merged) == len(df_gabung_lla):
    print("\n✓ SUKSES! Jumlah baris tetap sama seperti df_gabung_lla")
else:
    print(
        f"\n⚠ PERINGATAN! Jumlah baris berubah dari {len(df_gabung_lla)} menjadi {len(df_merged)}"
    )

# Cek hasil join (lihat kolom baru dari ref_payment)
print("\nKolom baru dari ref_payment:")
ref_payment_columns = [
    col
    for col in df_merged.columns
    if col not in df_gabung_lla.columns and col != "deskripsi"
]
print(ref_payment_columns)

print("\nSample data setelah join dengan ref_payment (5 baris pertama):")
print(df_merged.head(5))

# Cek apakah ada data yang tidak match (null values)
print("\nCek data yang tidak match dengan ref_payment:")
if ref_payment_columns:
    null_count_payment = df_merged[ref_payment_columns[3]].isna().sum()
    print(
        f"Jumlah baris yang tidak match (null di kolom ref_payment): {null_count_payment}"
    )
    persentase_null_payment = (null_count_payment / len(df_merged)) * 100
    print(f"Persentase tidak match: {persentase_null_payment:.2f}%")

    if null_count_payment > 0:
        print("\nSample 'deskripsi' yang tidak match dengan ref_payment (5 baris):")
        tidak_match_payment = df_merged[df_merged[ref_payment_columns[3]].isna()]
        print(tidak_match_payment[["deskripsi"]].head(5))

# ======================================
# Tampilkan ringkasan semua kolom setelah join
# ======================================
print("\n" + "=" * 50)
print("RINGKASAN SEMUA KOLOM SETELAH JOIN")
print("=" * 50)
print(f"Total kolom: {len(df_merged.columns)}")
print("\nDaftar semua kolom:")
for i, col in enumerate(df_merged.columns, 1):
    print(f"{i}. {col}")

print("\nSample final data (5 baris):")
print(df_merged.head(5))


# ======================================
# Step 9: Tambah kolom flag untuk kata "tot"
# ======================================
print("\n" + "=" * 50)
print("PROSES ADD COLUMN tot_flag")
print("=" * 50)

# Cek apakah kolom 'variabel' ada
if "variabel" in df_merged.columns:
    # Tambah kolom tot_flag (case-insensitive, cek apakah mengandung "tot")
    df_merged["tot_flag"] = (
        df_merged["variabel"].astype(str).str.lower().str.contains("tot", na=False)
    )

    print(f"✓ Berhasil menambahkan kolom 'tot_flag'")
    print(f"Tipe data kolom 'tot_flag': {df_merged['tot_flag'].dtypes}")

    # Tampilkan statistik flag
    print(f"\nStatistik tot_flag:")
    print(f"True  (mengandung 'tot'): {df_merged['tot_flag'].sum():,} baris")
    print(f"False (tidak mengandung 'tot'): {(~df_merged['tot_flag']).sum():,} baris")

    # Sample hasil
    print("\nSample data (10 baris pertama):")
    print(df_merged[["variabel", "tot_flag"]].head(10))

    # Contoh baris yang mengandung 'tot'
    print("\nSample baris yang mengandung 'tot' (5 baris):")
    print(df_merged[df_merged["tot_flag"] == True][["variabel", "tot_flag"]].head(5))
else:
    print(f"⚠ PERINGATAN: Kolom 'variabel' tidak ditemukan dalam dataframe!")
    print(f"Kolom yang tersedia: {df_merged.columns.tolist()}")


# ======================================
# Step 9a: Ekstrak deskripsi yang belum ada di ref_produk
# ======================================
print("\n" + "=" * 50)
print("EKSTRAK DESKRIPSI YANG BELUM ADA DI REF_PRODUK")
print("=" * 50)

# Daftar datakey yang diinginkan untuk ref_produk
target_datakeys_produk = [
    "B3AR2",
    "B3AR3",
    "B3AR6",
    "B3AR7",
    "B3BR2",
    "B3BR3",
    "B3BR6",
    "B3BR7",
    "B4BR3",
    "B4BR4",
    "B4DR3",
    "B4DR4",
    "B4DR5",
]

# Filter data yang belum match (null di kolom ref_produk)
if ref_columns:
    df_not_match_produk = df_merged[df_merged[ref_columns[0]].isna()].copy()
    print(
        f"Total data yang tidak match di ref_produk: {len(df_not_match_produk):,} baris"
    )

    # Filter berdasarkan datakey yang diinginkan
    df_filter_datakey_produk = df_not_match_produk[
        df_not_match_produk["datakey"].isin(target_datakeys_produk)
    ].copy()
    print(
        f"Data dengan datakey yang ditargetkan: {len(df_filter_datakey_produk):,} baris"
    )

    # Filter berdasarkan flag_tot = False
    if "tot_flag" in df_filter_datakey_produk.columns:
        df_final_extract_produk = df_filter_datakey_produk[
            df_filter_datakey_produk["tot_flag"] == False
        ].copy()
        print(f"Data dengan tot_flag = False: {len(df_final_extract_produk):,} baris")

        # Ambil kolom yang diperlukan
        extract_columns = ["deskripsi", "datakey", "variabel", "tot_flag"]
        available_columns = [
            col for col in extract_columns if col in df_final_extract_produk.columns
        ]

        # Buat dataframe hasil ekstrak
        df_extracted_deskripsi_produk = df_final_extract_produk[
            available_columns
        ].copy()

        # Hapus duplikasi deskripsi
        df_extracted_deskripsi_produk_unique = (
            df_extracted_deskripsi_produk.drop_duplicates(subset=["deskripsi"])
        )

        # Tampilkan hasil
        print("\n" + "=" * 50)
        print("HASIL EKSTRAK DESKRIPSI - REF_PRODUK")
        print("=" * 50)
        print(
            f"Jumlah deskripsi unik yang diekstrak: {len(df_extracted_deskripsi_produk_unique):,}"
        )
        print(
            f"Jumlah total baris (termasuk duplikat): {len(df_extracted_deskripsi_produk):,}"
        )

        print("\nSample hasil ekstrak (10 baris pertama):")
        print(df_extracted_deskripsi_produk.head(10))

        # Tampilkan statistik per datakey
        print("\nStatistik per datakey (ref_produk):")
        stat_datakey_produk = df_extracted_deskripsi_produk["datakey"].value_counts()
        for key, count in stat_datakey_produk.items():
            print(f"  {key}: {count:,} baris")

        # Tampilkan daftar deskripsi unik
        print("\nDaftar deskripsi unik yang perlu ditambahkan ke ref_produk:")
        print(
            df_extracted_deskripsi_produk_unique[["deskripsi", "datakey"]].to_string(
                index=False
            )
        )

        # Export ke CSV
        df_extracted_deskripsi_produk_unique.to_csv(
            os.path.join(OUTPUT_FOLDER, "deskripsi_produk_yang_perlu_ditambahkan.csv"),
            sep=";",
            index=False,
            encoding="utf-8-sig",
        )
        print(
            f"\n✓ Hasil ekstrak ref_produk disimpan ke '{OUTPUT_FOLDER}/deskripsi_produk_yang_perlu_ditambahkan.csv'"
        )

    else:
        print("⚠ PERINGATAN: Kolom 'tot_flag' tidak ditemukan untuk ref_produk!")
else:
    print("⚠ Tidak ada kolom ref_produk yang bisa dijadikan indikator match!")

# ======================================
# Step 9b: Ekstrak deskripsi yang belum ada di ref_payment
# ======================================
print("\n" + "=" * 50)
print("EKSTRAK DESKRIPSI YANG BELUM ADA DI REF_PAYMENT")
print("=" * 50)

# Daftar datakey yang diinginkan untuk ref_payment
target_datakeys_payment = ["B3AR4", "B3BR4", "B4BR5"]

# Filter data yang belum match (null di kolom ref_payment)
if ref_payment_columns:
    df_not_match_payment = df_merged[df_merged[ref_payment_columns[3]].isna()].copy()
    print(
        f"Total data yang tidak match di ref_payment: {len(df_not_match_payment):,} baris"
    )

    # Filter berdasarkan datakey yang diinginkan
    df_filter_datakey_payment = df_not_match_payment[
        df_not_match_payment["datakey"].isin(target_datakeys_payment)
    ].copy()
    print(
        f"Data dengan datakey yang ditargetkan: {len(df_filter_datakey_payment):,} baris"
    )

    # Filter berdasarkan flag_tot = False
    if "tot_flag" in df_filter_datakey_payment.columns:
        df_final_extract_payment = df_filter_datakey_payment[
            df_filter_datakey_payment["tot_flag"] == False
        ].copy()
        print(f"Data dengan tot_flag = False: {len(df_final_extract_payment):,} baris")

        # Ambil kolom yang diperlukan
        extract_columns = ["deskripsi", "datakey", "variabel", "tot_flag"]
        available_columns = [
            col for col in extract_columns if col in df_final_extract_payment.columns
        ]

        # Buat dataframe hasil ekstrak
        df_extracted_deskripsi_payment = df_final_extract_payment[
            available_columns
        ].copy()

        # Hapus duplikasi deskripsi
        df_extracted_deskripsi_payment_unique = (
            df_extracted_deskripsi_payment.drop_duplicates(subset=["deskripsi"])
        )

        # Tampilkan hasil
        print("\n" + "=" * 50)
        print("HASIL EKSTRAK DESKRIPSI - REF_PAYMENT")
        print("=" * 50)
        print(
            f"Jumlah deskripsi unik yang diekstrak: {len(df_extracted_deskripsi_payment_unique):,}"
        )
        print(
            f"Jumlah total baris (termasuk duplikat): {len(df_extracted_deskripsi_payment):,}"
        )

        print("\nSample hasil ekstrak (10 baris pertama):")
        print(df_extracted_deskripsi_payment.head(10))

        # Tampilkan statistik per datakey
        print("\nStatistik per datakey (ref_payment):")
        stat_datakey_payment = df_extracted_deskripsi_payment["datakey"].value_counts()
        for key, count in stat_datakey_payment.items():
            print(f"  {key}: {count:,} baris")

        # Tampilkan daftar deskripsi unik
        print("\nDaftar deskripsi unik yang perlu ditambahkan ke ref_payment:")
        print(
            df_extracted_deskripsi_payment_unique[["deskripsi", "datakey"]].to_string(
                index=False
            )
        )

        # Export ke CSV
        df_extracted_deskripsi_payment_unique.to_csv(
            os.path.join(OUTPUT_FOLDER, "deskripsi_payment_yang_perlu_ditambahkan.csv"),
            sep=";",
            index=False,
            encoding="utf-8-sig",
        )
        print(
            f"\n✓ Hasil ekstrak ref_payment disimpan ke '{OUTPUT_FOLDER}/deskripsi_payment_yang_perlu_ditambahkan.csv'"
        )

    else:
        print("⚠ PERINGATAN: Kolom 'tot_flag' tidak ditemukan untuk ref_payment!")
else:
    print("⚠ Tidak ada kolom ref_payment yang bisa dijadikan indikator match!")


# # ======================================
# # Step 9b: Ekstrak deskripsi yang belum ada di ref_payment
# # ======================================
# print("\n" + "=" * 50)
# print("EKSTRAK DESKRIPSI YANG BELUM ADA DI REF_PAYMENT")
# print("=" * 50)

# # Daftar datakey yang diinginkan untuk ref_payment
# target_datakeys_payment = ["B3AR4", "B3BR4", "B4BR5"]

# # Cek kolom dari ref_payment (biasanya ada suffix atau langsung 'klasifikasi')
# # Sesuaikan dengan hasil merge ref_payment sebelumnya
# payment_columns = [
#     col
#     for col in df_merged.columns
#     if col not in df_gabung_lla.columns and col not in ["deskripsi"]
# ]
# payment_indicator_col = None

# # Cari kolom indikator dari ref_payment (misalnya 'klasifikasi')
# for col in payment_columns:
#     if col not in ["deskripsi"]:
#         payment_indicator_col = col
#         break

# if payment_indicator_col:
#     df_not_match_payment = df_merged[df_merged[payment_indicator_col].isna()].copy()
#     print(
#         f"Total data yang tidak match di ref_payment: {len(df_not_match_payment):,} baris"
#     )

#     # Filter berdasarkan datakey yang diinginkan
#     df_filter_datakey_payment = df_not_match_payment[
#         df_not_match_payment["datakey"].isin(target_datakeys_payment)
#     ].copy()
#     print(
#         f"Data dengan datakey yang ditargetkan: {len(df_filter_datakey_payment):,} baris"
#     )

#     # Filter berdasarkan flag_tot = False
#     if "tot_flag" in df_filter_datakey_payment.columns:
#         df_final_extract_payment = df_filter_datakey_payment[
#             df_filter_datakey_payment["tot_flag"] == False
#         ].copy()
#         print(f"Data dengan tot_flag = False: {len(df_final_extract_payment):,} baris")

#         # Ambil kolom yang diperlukan
#         extract_columns = ["deskripsi", "datakey", "variabel", "tot_flag"]
#         available_columns = [
#             col for col in extract_columns if col in df_final_extract_payment.columns
#         ]

#         # Buat dataframe hasil ekstrak
#         df_extracted_deskripsi_payment = df_final_extract_payment[
#             available_columns
#         ].copy()

#         # Hapus duplikasi deskripsi
#         df_extracted_deskripsi_payment_unique = (
#             df_extracted_deskripsi_payment.drop_duplicates(subset=["deskripsi"])
#         )

#         # Tampilkan hasil
#         print("\n" + "=" * 50)
#         print("HASIL EKSTRAK DESKRIPSI - REF_PAYMENT")
#         print("=" * 50)
#         print(
#             f"Jumlah deskripsi unik yang diekstrak: {len(df_extracted_deskripsi_payment_unique):,}"
#         )
#         print(
#             f"Jumlah total baris (termasuk duplikat): {len(df_extracted_deskripsi_payment):,}"
#         )

#         print("\nSample hasil ekstrak (10 baris pertama):")
#         print(df_extracted_deskripsi_payment.head(10))

#         # Tampilkan statistik per datakey
#         print("\nStatistik per datakey (ref_payment):")
#         stat_datakey_payment = df_extracted_deskripsi_payment["datakey"].value_counts()
#         for key, count in stat_datakey_payment.items():
#             print(f"  {key}: {count:,} baris")

#         # Tampilkan daftar deskripsi unik
#         print("\nDaftar deskripsi unik yang perlu ditambahkan ke ref_payment:")
#         print(
#             df_extracted_deskripsi_payment_unique[["deskripsi", "datakey"]].to_string(
#                 index=False
#             )
#         )

#         # Export ke CSV
#         df_extracted_deskripsi_payment_unique.to_csv(
#             os.path.join(OUTPUT_FOLDER, "deskripsi_payment_yang_perlu_ditambahkan.csv"),
#             sep=";",
#             index=False,
#             encoding="utf-8-sig",
#         )
#         print(
#             f"\n✓ Hasil ekstrak ref_payment disimpan ke '{OUTPUT_FOLDER}/deskripsi_payment_yang_perlu_ditambahkan.csv'"
#         )

#     else:
#         print("⚠ PERINGATAN: Kolom 'tot_flag' tidak ditemukan untuk ref_payment!")
# else:
#     print("⚠ Tidak ada kolom ref_payment yang bisa dijadikan indikator match!")

# ======================================
# Tampilkan ringkasan kedua ekstrak
# ======================================
print("\n" + "=" * 50)
print("RINGKASAN EKSTRAK DESKRIPSI")
print("=" * 50)
print(
    f"REF_PRODUK - Jumlah deskripsi unik: {len(df_extracted_deskripsi_produk_unique) if 'df_extracted_deskripsi_produk_unique' in locals() else 0}"
)
print(
    f"REF_PAYMENT - Jumlah deskripsi unik: {len(df_extracted_deskripsi_payment_unique) if 'df_extracted_deskripsi_payment_unique' in locals() else 0}"
)


# ======================================
# Step 10: Group per pid dan tahun untuk daftar triwulan unik
# ======================================
print("\n" + "=" * 50)
print("PROSES MEMBUAT STATUS PANEL")
print("=" * 50)

# Pastikan kolom triwulan ada dan dalam format yang benar
if (
    "triwulan" in df_merged.columns
    and "pid" in df_merged.columns
    and "tahun" in df_merged.columns
):

    # Group by pid dan tahun, kumpulkan triwulan unik dalam bentuk list
    df_group = df_merged.groupby(["pid", "tahun"])["triwulan"].unique().reset_index()
    df_group.columns = ["pid", "tahun", "triwulan_list"]

    # Konversi triwulan ke string untuk memudahkan pengecekan
    df_group["triwulan_list_str"] = df_group["triwulan_list"].apply(
        lambda x: [str(int(item)) for item in x if pd.notna(item)]
    )

    print(f"Jumlah unik kombinasi pid-tahun: {len(df_group)}")
    print("\nSample hasil grouping:")
    print(df_group.head(10))

    # ======================================
    # Step 11: Tambahkan status untuk berbagai kombinasi triwulan
    # ======================================

    # Function untuk cek apakah triwulan tertentu ada dalam list
    def check_tw(tw_list, required_tw):
        """Cek apakah semua required_tw ada dalam tw_list"""
        return all(tw in tw_list for tw in required_tw)

    # 1. is_panel_25Q1_25Q2 (tahun 2025 dan memiliki TW 1 & 2)
    df_group["is_panel_25Q1_25Q2"] = df_group.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025 and check_tw(row["triwulan_list_str"], ["1", "2"])
            else "No"
        ),
        axis=1,
    )

    # 2. is_panel_25Q2_25Q3 (tahun 2025 dan memiliki TW 2 & 3)
    df_group["is_panel_25Q2_25Q3"] = df_group.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025 and check_tw(row["triwulan_list_str"], ["2", "3"])
            else "No"
        ),
        axis=1,
    )

    # 3. is_panel_25Q3_25Q4 (tahun 2025 dan memiliki TW 3 & 4)
    df_group["is_panel_25Q3_25Q4"] = df_group.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025 and check_tw(row["triwulan_list_str"], ["3", "4"])
            else "No"
        ),
        axis=1,
    )

    # 4. is_panel_25Q1-25Q4 (tahun 2025 dan memiliki TW 1,2,3,4 lengkap)
    df_group["is_panel_25Q1-25Q4"] = df_group.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025
            and check_tw(row["triwulan_list_str"], ["1", "2", "3", "4"])
            else "No"
        ),
        axis=1,
    )

    # ======================================
    # Step 12: Status panel lintas tahun
    # ======================================
    print("\n" + "=" * 50)
    print("PROSES STATUS PANEL LINTAS TAHUN")
    print("=" * 50)

    # Buat dataframe untuk cek per pid (tanpa tahun)
    # Cek apakah pid memiliki 2025Q4
    df_2025Q4 = df_merged[(df_merged["tahun"] == 2025) & (df_merged["triwulan"] == 4)][
        ["pid"]
    ].drop_duplicates()
    df_2025Q4["has_2025Q4"] = True

    # Cek apakah pid memiliki 2026Q1
    df_2026Q1 = df_merged[(df_merged["tahun"] == 2026) & (df_merged["triwulan"] == 1)][
        ["pid"]
    ].drop_duplicates()
    df_2026Q1["has_2026Q1"] = True

    # Cek apakah pid memiliki 2025Q1
    df_2025Q1 = df_merged[(df_merged["tahun"] == 2025) & (df_merged["triwulan"] == 1)][
        ["pid"]
    ].drop_duplicates()
    df_2025Q1["has_2025Q1"] = True

    # Gabungkan semua pengecekan
    df_panel_check = df_merged[["pid"]].drop_duplicates()
    df_panel_check = df_panel_check.merge(df_2025Q1, on="pid", how="left")
    df_panel_check = df_panel_check.merge(df_2025Q4, on="pid", how="left")
    df_panel_check = df_panel_check.merge(df_2026Q1, on="pid", how="left")

    # Isi NaN dengan False
    df_panel_check["has_2025Q1"] = df_panel_check["has_2025Q1"].fillna(False)
    df_panel_check["has_2025Q4"] = df_panel_check["has_2025Q4"].fillna(False)
    df_panel_check["has_2026Q1"] = df_panel_check["has_2026Q1"].fillna(False)

    # Hitung kondisi 2025Q4 dan 2026Q1
    df_panel_check["is_panel_25Q4_26Q1"] = (
        df_panel_check["has_2025Q4"] & df_panel_check["has_2026Q1"]
    )

    # Hitung kondisi 2025Q1 dan 2026Q1 (PANEL BARU)
    df_panel_check["is_panel_25Q1_26Q1"] = (
        df_panel_check["has_2025Q1"] & df_panel_check["has_2026Q1"]
    )

    # Hitung kondisi 2025Q1, 2025Q4, dan 2026Q1
    df_panel_check["is_panel_25Q1_25Q4_26Q1"] = (
        df_panel_check["has_2025Q1"]
        & df_panel_check["has_2025Q4"]
        & df_panel_check["has_2026Q1"]
    )

    # Convert ke Yes/No
    df_panel_check["is_panel_25Q4_26Q1"] = df_panel_check["is_panel_25Q4_26Q1"].apply(
        lambda x: "Yes" if x else "No"
    )
    df_panel_check["is_panel_25Q1_26Q1"] = df_panel_check["is_panel_25Q1_26Q1"].apply(
        lambda x: "Yes" if x else "No"
    )
    df_panel_check["is_panel_25Q1_25Q4_26Q1"] = df_panel_check[
        "is_panel_25Q1_25Q4_26Q1"
    ].apply(lambda x: "Yes" if x else "No")

    print(f"Jumlah pid yang memiliki 2025Q4: {df_panel_check['has_2025Q4'].sum():,}")
    print(f"Jumlah pid yang memiliki 2026Q1: {df_panel_check['has_2026Q1'].sum():,}")
    print(f"Jumlah pid yang memiliki 2025Q1: {df_panel_check['has_2025Q1'].sum():,}")
    print(
        f"Jumlah pid dengan is_panel_25Q4_26Q1 = Yes: {(df_panel_check['is_panel_25Q4_26Q1'] == 'Yes').sum():,}"
    )
    print(
        f"Jumlah pid dengan is_panel_25Q1_26Q1 = Yes: {(df_panel_check['is_panel_25Q1_26Q1'] == 'Yes').sum():,}"
    )
    print(
        f"Jumlah pid dengan is_panel_25Q1_25Q4_26Q1 = Yes: {(df_panel_check['is_panel_25Q1_25Q4_26Q1'] == 'Yes').sum():,}"
    )

    # ======================================
    # Step 13: Gabungkan status ke data asal
    # ======================================
    print("\n" + "=" * 50)
    print("GABUNGKAN STATUS KE DATA ASAL")
    print("=" * 50)

    # Gabungkan status dari df_group ke df_merged (based on pid dan tahun)
    df_merged = df_merged.merge(
        df_group[
            [
                "pid",
                "tahun",
                "is_panel_25Q1_25Q2",
                "is_panel_25Q2_25Q3",
                "is_panel_25Q3_25Q4",
                "is_panel_25Q1-25Q4",
            ]
        ],
        on=["pid", "tahun"],
        how="left",
    )

    # Gabungkan status lintas tahun (based on pid saja)
    df_merged = df_merged.merge(
        df_panel_check[
            [
                "pid",
                "is_panel_25Q4_26Q1",
                "is_panel_25Q1_26Q1",
                "is_panel_25Q1_25Q4_26Q1",
            ]
        ],
        on="pid",
        how="left",
    )

    # Fill NaN untuk status yang tidak ada (karena left join)
    status_columns = [
        "is_panel_25Q1_25Q2",
        "is_panel_25Q2_25Q3",
        "is_panel_25Q3_25Q4",
        "is_panel_25Q1-25Q4",
        "is_panel_25Q4_26Q1",
        "is_panel_25Q1_26Q1",
        "is_panel_25Q1_25Q4_26Q1",
    ]
    for col in status_columns:
        df_merged[col] = df_merged[col].fillna("No")

    # ======================================
    # Step 14: Verifikasi hasil
    # ======================================
    print("\n" + "=" * 50)
    print("VERIFIKASI STATUS PANEL")
    print("=" * 50)

    # Tampilkan statistik untuk tahun 2025
    df_2025 = df_merged[df_merged["tahun"] == 2025]
    print("\nStatistik untuk tahun 2025:")
    print(f"Total data 2025: {len(df_2025):,} baris")
    print(
        f"is_panel_25Q1_25Q2  (TW 1&2) - Yes: {(df_2025['is_panel_25Q1_25Q2'] == 'Yes').sum():,}"
    )
    print(
        f"is_panel_25Q2_25Q3  (TW 2&3) - Yes: {(df_2025['is_panel_25Q2_25Q3'] == 'Yes').sum():,}"
    )
    print(
        f"is_panel_25Q3_25Q4  (TW 3&4) - Yes: {(df_2025['is_panel_25Q3_25Q4'] == 'Yes').sum():,}"
    )
    print(
        f"is_panel_25Q1-25Q4 (TW 1-4) - Yes: {(df_2025['is_panel_25Q1-25Q4'] == 'Yes').sum():,}"
    )

    print("\nStatistik lintas tahun (berlaku untuk semua data):")
    print(
        f"is_panel_25Q4_26Q1 (2025Q4 & 2026Q1) - Yes: {(df_merged['is_panel_25Q4_26Q1'] == 'Yes').sum():,}"
    )
    print(
        f"is_panel_25Q1_26Q1 (2025Q1 & 2026Q1) - Yes: {(df_merged['is_panel_25Q1_26Q1'] == 'Yes').sum():,}"
    )
    print(
        f"is_panel_25Q1_25Q4_26Q1 (2025Q1, 2025Q4, 2026Q1) - Yes: {(df_merged['is_panel_25Q1_25Q4_26Q1'] == 'Yes').sum():,}"
    )

    # Sample hasil
    print("\nSample data dengan status panel (5 baris pertama untuk tahun 2025):")
    sample_columns = [
        "pid",
        "tahun",
        "triwulan",
        "is_panel_25Q1_25Q2",
        "is_panel_25Q2_25Q3",
        "is_panel_25Q3_25Q4",
        "is_panel_25Q1-25Q4",
        "is_panel_25Q4_26Q1",
        "is_panel_25Q1_26Q1",
        "is_panel_25Q1_25Q4_26Q1",
    ]
    print(
        df_merged[df_merged["tahun"] == 2025][sample_columns]
        .drop_duplicates(subset=["pid", "tahun"])
        .head(10)
    )

    print("\nSample pid yang memiliki is_panel_25Q4_26Q1 = Yes:")
    sample_panel_25q4_26q1 = (
        df_merged[df_merged["is_panel_25Q4_26Q1"] == "Yes"][
            ["pid", "tahun", "triwulan"]
        ]
        .drop_duplicates()
        .head(10)
    )
    print(sample_panel_25q4_26q1)

    print("\nSample pid yang memiliki is_panel_25Q1_26Q1 = Yes:")
    sample_panel_25q1_26q1 = (
        df_merged[df_merged["is_panel_25Q1_26Q1"] == "Yes"][
            ["pid", "tahun", "triwulan"]
        ]
        .drop_duplicates()
        .head(10)
    )
    print(sample_panel_25q1_26q1)

else:
    print("⚠ PERINGATAN: Kolom yang diperlukan tidak lengkap!")
    print(f"Kolom yang ada: {df_merged.columns.tolist()}")
    print("Diperlukan kolom: 'pid', 'tahun', 'triwulan'")


# ######################################
# NON LLA
# ######################################

# ======================================
# Step 15: Baca dan gabung file NON LLA
# ======================================
# Baca dua file CSV
df1_non_lla = pd.read_csv(
    NON_LLA_FILE_1,
    sep=";",
    encoding="utf-8",
)
df2_non_lla = pd.read_csv(
    NON_LLA_FILE_2,
    sep=";",
    encoding="utf-8",
)

# Append (gabung baris)
df_gabung_non_lla = pd.concat([df1_non_lla, df2_non_lla], ignore_index=True)
print("Sample data non_lla awal:")
print(df_gabung_non_lla.head(10))
print("\nInfo tipe data:")
print(df_gabung_non_lla.dtypes)


# ======================================
# Step 16: Hapus duplikat
# ======================================
df_bersih = df_gabung_non_lla.drop_duplicates(subset=["assignment_id"]).copy()

print(f"Sebelum hapus duplikat: {len(df_gabung_non_lla)} baris")
print(f"Setelah hapus duplikat: {len(df_bersih)} baris")


# ======================================
# Step 17: Tambah kolom is_exist_lla_nonlla
# ======================================

# Tambahkan kolom baru dengan nilai konstan "Yes"
df_bersih["is_exist_lla_nonlla"] = "Yes"

# Cek hasil
print("\n=== SETELAH STEP 8 ===")
print(f"Total baris: {len(df_bersih)}")
print(f"Total kolom: {len(df_bersih.columns)}")
print("\nSample kolom baru:")
print(df_bersih[["is_exist_lla_nonlla"]].head(10))
print(
    f"\nDistribusi nilai: {df_bersih['is_exist_lla_nonlla'].value_counts().to_dict()}"
)


# ======================================
# Step 18: Merge LLA dengan NON LLA (Left Outer Join) - hanya ambil kolom is_exist_lla_nonlla
# ======================================
print("\n" + "=" * 50)
print("PROSES MERGE LLA DENGAN NON LLA")
print("=" * 50)

# Cek apakah kolom assignment_id ada di kedua dataframe
if "assignment_id" in df_merged.columns and "assignment_id" in df_bersih.columns:

    # Cek tipe data assignment_id
    print("\nCek tipe data assignment_id:")
    print(f"Tipe data di df_merged: {df_merged['assignment_id'].dtypes}")
    print(f"Tipe data di df_bersih: {df_bersih['assignment_id'].dtypes}")

    # Pastikan tipe data sama (konversi ke string)
    df_merged["assignment_id"] = df_merged["assignment_id"].astype(str)
    df_bersih["assignment_id"] = df_bersih["assignment_id"].astype(str)

    # Cek duplikasi assignment_id di df_bersih (harusnya sudah dihapus di step 16)
    duplikat_non_lla = df_bersih["assignment_id"].duplicated().sum()
    print(f"\nJumlah duplikat assignment_id di df_bersih: {duplikat_non_lla}")

    # Cek nilai unik
    print(
        f"\nJumlah unique assignment_id di df_merged: {df_merged['assignment_id'].nunique():,}"
    )
    print(
        f"Jumlah unique assignment_id di df_bersih: {df_bersih['assignment_id'].nunique():,}"
    )

    # Ambil hanya kolom yang diperlukan dari df_bersih
    df_non_lla_selected = df_bersih[["assignment_id", "is_exist_lla_nonlla"]].copy()

    # Left Outer Join (hanya ambil kolom is_exist_lla_nonlla)
    print("\nMelakukan LEFT OUTER JOIN (hanya ambil is_exist_lla_nonlla)...")
    df_final = df_merged.merge(
        df_non_lla_selected,
        on="assignment_id",  # Kolom join
        how="left",  # Left Outer Join
    )

    print(f"\nJumlah baris sebelum join: {len(df_merged):,}")
    print(f"Jumlah baris setelah join: {len(df_final):,}")
    print(f"Jumlah kolom setelah join: {len(df_final.columns)}")

    # Verifikasi jumlah baris tetap sama
    if len(df_final) == len(df_merged):
        print("\n✓ SUKSES! Jumlah baris tetap sama seperti df_merged")
    else:
        print(f"\n⚠ PERINGATAN! Jumlah baris berubah!")

    # Cek apakah ada data yang match
    if "is_exist_lla_nonlla" in df_final.columns:
        match_count = df_final["is_exist_lla_nonlla"].notna().sum()
        non_match_count = df_final["is_exist_lla_nonlla"].isna().sum()

        print(f"\nStatistik match dengan non_lla:")
        print(
            f"Match (ada di non_lla): {match_count:,} baris ({match_count/len(df_final)*100:.2f}%)"
        )
        print(
            f"Tidak match (tidak ada di non_lla): {non_match_count:,} baris ({non_match_count/len(df_final)*100:.2f}%)"
        )

        # Isi NaN dengan "No" untuk kolom is_exist_lla_nonlla
        df_final["is_exist_lla_nonlla"] = df_final["is_exist_lla_nonlla"].fillna("No")
        print(f"\n✓ Kolom 'is_exist_lla_nonlla' sudah diisi:")
        print(f"   - Yes: {(df_final['is_exist_lla_nonlla'] == 'Yes').sum():,} baris")
        print(f"   - No:  {(df_final['is_exist_lla_nonlla'] == 'No').sum():,} baris")

    # Sample hasil
    print("\nSample hasil merge (10 baris pertama):")
    print(df_final[["assignment_id", "is_exist_lla_nonlla"]].head(10))

    # Cek perbandingan sebelum dan sesudah
    print("\nContoh assignment_id yang match (Yes):")
    match_sample = (
        df_final[df_final["is_exist_lla_nonlla"] == "Yes"]["assignment_id"]
        .head(5)
        .tolist()
    )
    print(match_sample)

    print("\nContoh assignment_id yang tidak match (No):")
    non_match_sample = (
        df_final[df_final["is_exist_lla_nonlla"] == "No"]["assignment_id"]
        .head(5)
        .tolist()
    )
    print(non_match_sample)

else:
    print("⚠ PERINGATAN: Kolom 'assignment_id' tidak ditemukan!")
    if "assignment_id" not in df_merged.columns:
        print(f"Kolom di df_merged: {df_merged.columns.tolist()[:10]}...")
    if "assignment_id" not in df_bersih.columns:
        print(f"Kolom di df_bersih: {df_bersih.columns.tolist()[:10]}...")

# ======================================
# Tampilkan ringkasan final
# ======================================
print("\n" + "=" * 50)
print("RINGKASAN FINAL DATAFRAME")
print("=" * 50)
print(f"Total baris: {len(df_final):,}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom yang tersedia: {df_final.columns.tolist()}")
print(f"\nMemory usage: {df_final.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


# ======================================
# Step 19: Group berdasarkan pid dan tahun untuk non_lla yang is_exist = "Yes"
# ======================================
print("\n" + "=" * 50)
print("PROSES MEMBUAT STATUS EXIST PANEL")
print("=" * 50)

# Pastikan kolom yang diperlukan ada
if all(
    col in df_final.columns
    for col in ["pid", "tahun", "triwulan", "is_exist_lla_nonlla"]
):

    # Filter data yang is_exist_lla_nonlla = "Yes"
    df_exist = df_final[df_final["is_exist_lla_nonlla"] == "Yes"].copy()
    print(f"Jumlah data dengan is_exist_lla_nonlla = 'Yes': {len(df_exist):,} baris")

    # Group by pid dan tahun, kumpulkan triwulan unik
    df_group_exist = (
        df_exist.groupby(["pid", "tahun"])["triwulan"].unique().reset_index()
    )
    df_group_exist.columns = ["pid", "tahun", "filtered_triwulan"]

    # Konversi triwulan ke string untuk memudahkan pengecekan
    df_group_exist["filtered_triwulan_str"] = df_group_exist["filtered_triwulan"].apply(
        lambda x: [str(int(item)) for item in x if pd.notna(item)]
    )

    print(f"\nJumlah unik kombinasi pid-tahun dengan exist data: {len(df_group_exist)}")
    print("\nSample hasil grouping:")
    print(df_group_exist.head(10))

    # ======================================
    # Step 20: Tambahkan status untuk berbagai kombinasi triwulan
    # ======================================
    print("\n" + "=" * 50)
    print("PROSES MENAMBAHKAN STATUS EXIST PANEL")
    print("=" * 50)

    def check_tw(tw_list, required_tw):
        """Cek apakah semua required_tw ada dalam tw_list"""
        return all(tw in tw_list for tw in required_tw)

    # 1. is_exist_25Q1_25Q2 (tahun 2025 dan memiliki TW 1 & 2)
    df_group_exist["is_exist_25Q1_25Q2"] = df_group_exist.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025
            and check_tw(row["filtered_triwulan_str"], ["1", "2"])
            else "No"
        ),
        axis=1,
    )

    # 2. is_exist_25Q2_25Q3 (tahun 2025 dan memiliki TW 2 & 3)
    df_group_exist["is_exist_25Q2_25Q3"] = df_group_exist.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025
            and check_tw(row["filtered_triwulan_str"], ["2", "3"])
            else "No"
        ),
        axis=1,
    )

    # 3. is_exist_25Q3_25Q4 (tahun 2025 dan memiliki TW 3 & 4)
    df_group_exist["is_exist_25Q3_25Q4"] = df_group_exist.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025
            and check_tw(row["filtered_triwulan_str"], ["3", "4"])
            else "No"
        ),
        axis=1,
    )

    # 4. is_exist_25Q1_25Q4 (tahun 2025 dan memiliki TW 1,2,3,4 lengkap)
    df_group_exist["is_exist_25Q1_25Q4"] = df_group_exist.apply(
        lambda row: (
            "Yes"
            if row["tahun"] == 2025
            and check_tw(row["filtered_triwulan_str"], ["1", "2", "3", "4"])
            else "No"
        ),
        axis=1,
    )

    # ======================================
    # Step 21: Status exist lintas tahun (2025Q4 & 2026Q1)
    # ======================================
    print("\n" + "=" * 50)
    print("PROSES STATUS EXIST PANEL LINTAS TAHUN")
    print("=" * 50)

    # Buat dataframe untuk cek per pid (tanpa tahun) berdasarkan data exist
    # Cek apakah pid memiliki 2025Q4 dengan is_exist = "Yes"
    df_exist_2025Q4 = df_exist[
        (df_exist["tahun"] == 2025) & (df_exist["triwulan"] == 4)
    ][["pid"]].drop_duplicates()
    df_exist_2025Q4["has_exist_2025Q4"] = True

    # Cek apakah pid memiliki 2026Q1 dengan is_exist = "Yes"
    df_exist_2026Q1 = df_exist[
        (df_exist["tahun"] == 2026) & (df_exist["triwulan"] == 1)
    ][["pid"]].drop_duplicates()
    df_exist_2026Q1["has_exist_2026Q1"] = True

    # Cek apakah pid memiliki 2025Q1 dengan is_exist = "Yes"
    df_exist_2025Q1 = df_exist[
        (df_exist["tahun"] == 2025) & (df_exist["triwulan"] == 1)
    ][["pid"]].drop_duplicates()
    df_exist_2025Q1["has_exist_2025Q1"] = True

    # Gabungkan semua pengecekan
    df_exist_panel_check = df_final[["pid"]].drop_duplicates()
    df_exist_panel_check = df_exist_panel_check.merge(
        df_exist_2025Q1, on="pid", how="left"
    )
    df_exist_panel_check = df_exist_panel_check.merge(
        df_exist_2025Q4, on="pid", how="left"
    )
    df_exist_panel_check = df_exist_panel_check.merge(
        df_exist_2026Q1, on="pid", how="left"
    )

    # Isi NaN dengan False
    df_exist_panel_check["has_exist_2025Q1"] = df_exist_panel_check[
        "has_exist_2025Q1"
    ].fillna(False)
    df_exist_panel_check["has_exist_2025Q4"] = df_exist_panel_check[
        "has_exist_2025Q4"
    ].fillna(False)
    df_exist_panel_check["has_exist_2026Q1"] = df_exist_panel_check[
        "has_exist_2026Q1"
    ].fillna(False)

    # Hitung kondisi 2025Q4 dan 2026Q1
    df_exist_panel_check["is_exist_25Q4_26Q1"] = (
        df_exist_panel_check["has_exist_2025Q4"]
        & df_exist_panel_check["has_exist_2026Q1"]
    )

    # Hitung kondisi 2025Q1, 2025Q4, dan 2026Q1
    df_exist_panel_check["is_exist_25Q1_25Q4_26Q1"] = (
        df_exist_panel_check["has_exist_2025Q1"]
        & df_exist_panel_check["has_exist_2025Q4"]
        & df_exist_panel_check["has_exist_2026Q1"]
    )

    # Convert ke Yes/No
    df_exist_panel_check["is_exist_25Q4_26Q1"] = df_exist_panel_check[
        "is_exist_25Q4_26Q1"
    ].apply(lambda x: "Yes" if x else "No")
    df_exist_panel_check["is_exist_25Q1_25Q4_26Q1"] = df_exist_panel_check[
        "is_exist_25Q1_25Q4_26Q1"
    ].apply(lambda x: "Yes" if x else "No")

    print(f"\nStatistik exist panel:")
    print(
        f"Jumlah pid dengan exist 2025Q1: {df_exist_panel_check['has_exist_2025Q1'].sum():,}"
    )
    print(
        f"Jumlah pid dengan exist 2025Q4: {df_exist_panel_check['has_exist_2025Q4'].sum():,}"
    )
    print(
        f"Jumlah pid dengan exist 2026Q1: {df_exist_panel_check['has_exist_2026Q1'].sum():,}"
    )
    print(
        f"Jumlah pid dengan is_exist_25Q4_26Q1 = Yes: {(df_exist_panel_check['is_exist_25Q4_26Q1'] == 'Yes').sum():,}"
    )
    print(
        f"Jumlah pid dengan is_exist_25Q1_25Q4_26Q1 = Yes: {(df_exist_panel_check['is_exist_25Q1_25Q4_26Q1'] == 'Yes').sum():,}"
    )

    # ======================================
    # Step 22: Gabungkan status ke data asal
    # ======================================
    print("\n" + "=" * 50)
    print("GABUNGKAN STATUS EXIST KE DATA ASAL")
    print("=" * 50)

    # Gabungkan status dari df_group_exist ke df_final (based on pid dan tahun)
    # Hanya untuk tahun 2025 saja karena status untuk 2025
    df_final = df_final.merge(
        df_group_exist[
            [
                "pid",
                "tahun",
                "is_exist_25Q1_25Q2",
                "is_exist_25Q2_25Q3",
                "is_exist_25Q3_25Q4",
                "is_exist_25Q1_25Q4",
            ]
        ],
        on=["pid", "tahun"],
        how="left",
    )

    # Gabungkan status lintas tahun (based on pid saja)
    df_final = df_final.merge(
        df_exist_panel_check[["pid", "is_exist_25Q4_26Q1", "is_exist_25Q1_25Q4_26Q1"]],
        on="pid",
        how="left",
    )

    # Fill NaN untuk status yang tidak ada (karena left join)
    exist_status_columns = [
        "is_exist_25Q1_25Q2",
        "is_exist_25Q2_25Q3",
        "is_exist_25Q3_25Q4",
        "is_exist_25Q1_25Q4",
        "is_exist_25Q4_26Q1",
        "is_exist_25Q1_25Q4_26Q1",
    ]

    for col in exist_status_columns:
        df_final[col] = df_final[col].fillna("No")

    # ======================================
    # Step 23: Verifikasi hasil
    # ======================================
    print("\n" + "=" * 50)
    print("VERIFIKASI STATUS EXIST PANEL")
    print("=" * 50)

    # Tampilkan statistik untuk tahun 2025
    df_final_2025 = df_final[df_final["tahun"] == 2025]
    print("\nStatistik exist panel untuk tahun 2025:")
    print(f"Total data 2025: {len(df_final_2025):,} baris")
    print(
        f"is_exist_25Q1_25Q2  (TW 1&2) - Yes: {(df_final_2025['is_exist_25Q1_25Q2'] == 'Yes').sum():,}"
    )
    print(
        f"is_exist_25Q2_25Q3  (TW 2&3) - Yes: {(df_final_2025['is_exist_25Q2_25Q3'] == 'Yes').sum():,}"
    )
    print(
        f"is_exist_25Q3_25Q4  (TW 3&4) - Yes: {(df_final_2025['is_exist_25Q3_25Q4'] == 'Yes').sum():,}"
    )
    print(
        f"is_exist_25Q1_25Q4 (TW 1-4) - Yes: {(df_final_2025['is_exist_25Q1_25Q4'] == 'Yes').sum():,}"
    )

    print("\nStatistik exist panel lintas tahun (berlaku untuk semua data):")
    print(
        f"is_exist_25Q4_26Q1 (2025Q4 & 2026Q1) - Yes: {(df_final['is_exist_25Q4_26Q1'] == 'Yes').sum():,}"
    )
    print(
        f"is_exist_25Q1_25Q4_26Q1 (2025Q1, 2025Q4, 2026Q1) - Yes: {(df_final['is_exist_25Q1_25Q4_26Q1'] == 'Yes').sum():,}"
    )

    # Sample hasil
    print(
        "\nSample data dengan status exist panel (10 baris pertama untuk tahun 2025):"
    )
    sample_columns = [
        "pid",
        "tahun",
        "triwulan",
        "is_exist_lla_nonlla",
        "is_exist_25Q1_25Q2",
        "is_exist_25Q2_25Q3",
        "is_exist_25Q3_25Q4",
        "is_exist_25Q1_25Q4",
        "is_exist_25Q4_26Q1",
        "is_exist_25Q1_25Q4_26Q1",
    ]
    print(
        df_final[df_final["tahun"] == 2025][sample_columns]
        .drop_duplicates(subset=["pid", "tahun"])
        .head(10)
    )

    print("\nSample pid yang memiliki is_exist_25Q4_26Q1 = Yes:")
    sample_exist_panel = (
        df_final[df_final["is_exist_25Q4_26Q1"] == "Yes"][
            ["pid", "tahun", "triwulan", "is_exist_lla_nonlla"]
        ]
        .drop_duplicates()
        .head(10)
    )
    print(sample_exist_panel)

else:
    print("⚠ PERINGATAN: Kolom yang diperlukan tidak lengkap!")
    print(f"Kolom yang ada di df_final: {df_final.columns.tolist()}")
    print("Diperlukan kolom: 'pid', 'tahun', 'triwulan', 'is_exist_lla_nonlla'")

# ======================================
# Tampilkan ringkasan final semua kolom
# ======================================
print("\n" + "=" * 50)
print("RINGKASAN FINAL SEMUA KOLOM")
print("=" * 50)
print(f"Total baris: {len(df_final):,}")
print(f"Total kolom: {len(df_final.columns)}")
print("\nDaftar semua kolom yang tersedia:")
for i, col in enumerate(df_final.columns, 1):
    print(f"{i}. {col}")


# ======================================
# FINAL CHECK SEBELUM SAVE KE CSV
# ======================================
print("\n" + "=" * 80)
print(" " * 20 + "FINAL CHECK DATAFRAME")
print("=" * 80)

# ======================================
# 1. Informasi Dasar
# ======================================
print("\n📊 INFORMASI DASAR:")
print("-" * 50)
print(f"✓ Total baris: {len(df_final):,}")
print(f"✓ Total kolom: {len(df_final.columns):,}")
print(f"✓ Memory usage: {df_final.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ======================================
# 2. Cek Missing Values per Kolom
# ======================================
print("\n🔍 CEK MISSING VALUES (per kolom):")
print("-" * 50)

missing_summary = df_final.isnull().sum()
missing_percent = (missing_summary / len(df_final)) * 100
missing_df = pd.DataFrame(
    {"Missing Values": missing_summary, "Percentage (%)": missing_percent}
)
missing_df = missing_df[missing_df["Missing Values"] > 0].sort_values(
    "Missing Values", ascending=False
)

if len(missing_df) > 0:
    print(f"Terdapat {len(missing_df)} kolom dengan missing values:")
    print(missing_df.head(20))
else:
    print("✓ Tidak ada missing values di semua kolom!")

# ======================================
# 3. Cek Duplikasi
# ======================================
print("\n🔍 CEK DUPLIKASI:")
print("-" * 50)

# Cek duplikasi berdasarkan assignment_id
if "assignment_id" in df_final.columns:
    duplicate_assignments = df_final["assignment_id"].duplicated().sum()
    print(f"✓ Duplikasi berdasarkan 'assignment_id': {duplicate_assignments:,} baris")

    if duplicate_assignments > 0:
        print("⚠ PERINGATAN: Ada duplikasi assignment_id! Sample:")
        dup_samples = (
            df_final[df_final["assignment_id"].duplicated(keep=False)]
            .sort_values("assignment_id")
            .head(10)
        )
        print(dup_samples[["assignment_id", "pid", "tahun", "triwulan"]])

# Cek duplikasi keseluruhan baris
duplicate_rows = df_final.duplicated().sum()
print(f"✓ Duplikasi keseluruhan baris: {duplicate_rows:,} baris")

# ======================================
# 4. Cek Tipe Data
# ======================================
print("\n📋 CEK TIPE DATA:")
print("-" * 50)

dtype_summary = df_final.dtypes.value_counts()
for dtype, count in dtype_summary.items():
    print(f"✓ {dtype}: {count} kolom")

# Tampilkan kolom dengan tipe object (biasanya string)
object_cols = df_final.select_dtypes(include=["object"]).columns.tolist()
if object_cols:
    print(f"\nKolom dengan tipe object (string): {len(object_cols)} kolom")
    print(f"  Sample: {object_cols[:10]}")

# ======================================
# 5. Statistik Kolom Penting untuk Pivot
# ======================================
print("\n📈 STATISTIK KOLOM PENTING UNTUK PIVOT:")
print("-" * 50)

# Kolom-kolom penting yang biasanya dipakai untuk pivot
key_columns = [
    "tahun",
    "triwulan",
    "pid",
    "datakey",
    "tot_flag",
    "is_exist_lla_nonlla",
    "is_panel_25Q1_25Q2",
    "is_panel_25Q2_25Q3",
    "is_panel_25Q3_25Q4",
    "is_panel_25Q1-25Q4",
    "is_panel_25Q4_26Q1",
    "is_exist_25Q1_25Q2",
    "is_exist_25Q2_25Q3",
    "is_exist_25Q3_25Q4",
    "is_exist_25Q1_25Q4",
    "is_exist_25Q4_26Q1",
]

for col in key_columns:
    if col in df_final.columns:
        unique_count = df_final[col].nunique()
        print(f"\n✓ {col}:")
        print(f"  - Unique values: {unique_count:,}")

        # Tampilkan value counts untuk kolom dengan unique sedikit
        if unique_count <= 10:
            value_counts = df_final[col].value_counts()
            for val, cnt in value_counts.items():
                print(f"  - {val}: {cnt:,} ({cnt/len(df_final)*100:.1f}%)")

# ======================================
# 6. Statistik Flag / Boolean Columns
# ======================================
print("\n🚩 STATISTIK FLAG COLUMNS (Yes/No):")
print("-" * 50)

flag_columns = [col for col in df_final.columns if col.startswith(("is_", "tot_flag"))]
for col in flag_columns:
    if col in df_final.columns:
        yes_count = (
            (df_final[col] == "Yes").sum()
            if df_final[col].dtype == "object"
            else df_final[col].sum()
        )
        no_count = (
            (df_final[col] == "No").sum()
            if df_final[col].dtype == "object"
            else (
                (~df_final[col].astype(bool)).sum()
                if df_final[col].dtype == "bool"
                else 0
            )
        )
        total = len(df_final)

        print(f"\n✓ {col}:")
        print(f"  - Yes: {yes_count:,} ({yes_count/total*100:.1f}%)")
        print(f"  - No:  {no_count:,} ({no_count/total*100:.1f}%)")

# ======================================
# 7. Cek Data per Tahun dan Triwulan
# ======================================
print("\n📅 DISTRIBUSI DATA PER TAHUN & TRIWULAN:")
print("-" * 50)

if "tahun" in df_final.columns and "triwulan" in df_final.columns:
    # Per tahun
    tahun_dist = df_final["tahun"].value_counts().sort_index()
    print("\nPer Tahun:")
    for tahun, count in tahun_dist.items():
        print(f"  {tahun}: {count:,} baris ({count/len(df_final)*100:.1f}%)")

    # Per triwulan
    triwulan_dist = df_final["triwulan"].value_counts().sort_index()
    print("\nPer Triwulan:")
    for triwulan, count in triwulan_dist.items():
        print(f"  Q{triwulan}: {count:,} baris ({count/len(df_final)*100:.1f}%)")

    # Cross tab tahun vs triwulan
    print("\nCross Tab Tahun vs Triwulan:")
    cross_tab = pd.crosstab(df_final["tahun"], df_final["triwulan"])
    print(cross_tab)

# ======================================
# 8. Cek Data untuk Pivot (Nilai Numerik)
# ======================================
print("\n💰 STATISTIK KOLOM NUMERIK (jika ada untuk agregasi):")
print("-" * 50)

numeric_cols = df_final.select_dtypes(include=["float64", "int64"]).columns.tolist()
if numeric_cols:
    # Hanya tampilkan 10 kolom numerik pertama
    for col in numeric_cols[:10]:
        print(f"\n✓ {col}:")
        print(f"  - Min: {df_final[col].min():,.2f}")
        print(f"  - Max: {df_final[col].max():,.2f}")
        print(f"  - Mean: {df_final[col].mean():,.2f}")
        print(f"  - Sum: {df_final[col].sum():,.2f}")
else:
    print("✓ Tidak ada kolom numerik untuk agregasi")

# ======================================
# 9. Sample Data untuk Review
# ======================================
print("\n👀 SAMPLE DATA (10 baris pertama untuk preview):")
print("-" * 50)

# Pilih kolom penting untuk ditampilkan
preview_columns = [
    "assignment_id",
    "pid",
    "tahun",
    "triwulan",
    "datakey",
    "tot_flag",
    "is_exist_lla_nonlla",
    "is_panel_25Q1_25Q2",
    "is_panel_25Q4_26Q1",
    "is_exist_25Q4_26Q1",
]

available_preview = [col for col in preview_columns if col in df_final.columns]
print(df_final[available_preview].head(10))

# ======================================
# 10. Validasi Data untuk Pivot Excel
# ======================================
print("\n✅ VALIDASI KESIAPAN DATA UNTUK PIVOT EXCEL:")
print("-" * 50)

validation_passed = True

# Cek 1: Apakah ada kolom yang bisa dijadikan row/column?
pivot_keys = ["tahun", "triwulan", "pid", "datakey"]
missing_keys = [key for key in pivot_keys if key not in df_final.columns]
if missing_keys:
    print(f"⚠ PERINGATAN: Kolom untuk pivot tidak lengkap! Missing: {missing_keys}")
    validation_passed = False
else:
    print("✓ Kolom untuk row/column pivot tersedia (tahun, triwulan, pid, datakey)")

# Cek 2: Apakah ada nilai untuk diagregasi?
if numeric_cols:
    print(f"✓ Kolom numerik untuk agregasi tersedia ({len(numeric_cols)} kolom)")
else:
    print("⚠ PERINGATAN: Tidak ada kolom numerik untuk agregasi (sum, count, average)")

# Cek 3: Apakah ada flag/filter columns?
if flag_columns:
    print(f"✓ Flag/filter columns tersedia ({len(flag_columns)} kolom)")
else:
    print("⚠ PERINGATAN: Tidak ada flag/filter columns")

# Cek 4: Data size
if len(df_final) < 1000000:
    print(f"✓ Data size reasonable ({len(df_final):,} baris) untuk Excel")
else:
    print(f"⚠ Data size besar ({len(df_final):,} baris), Excel mungkin lambat")

if validation_passed:
    print("\n🎉 DATA SIAP DISAVE DAN DIPIVOT DI EXCEL!")
else:
    print("\n⚠ PERHATIAN: Ada beberapa hal yang perlu diperbaiki sebelum pivot")

# ======================================
# 11. Save to CSV
# ======================================
print("\n" + "=" * 80)
print(" " * 25 + "SAVE TO CSV")
print("=" * 80)

# Buat output folder jika belum ada
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Nama file output dengan timestamp
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(OUTPUT_FOLDER, f"df_final_lla_{timestamp}.csv")

print(f"\n💾 Menyimpan data ke: {output_file}")
print(f"   Total baris: {len(df_final):,}")
print(f"   Total kolom: {len(df_final.columns):,}")

# Save ke CSV dengan separator ; untuk Excel Indonesia
df_final.to_csv(
    output_file,
    sep=";",
    encoding="utf-8-sig",  # utf-8-sig agar Excel bisa baca dengan benar
    index=False,
)

print(f"\n✅ FILE BERHASIL DISAVE!")
print(f"   📁 Lokasi: {output_file}")
print(f"   📊 Size: {os.path.getsize(output_file) / 1024**2:.2f} MB")

# ======================================
# 12. Ringkasan Final
# ======================================
print("\n" + "=" * 80)
print(" " * 25 + "RINGKASAN FINAL")
print("=" * 80)

print(f"""
📋 SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Total Baris           : {len(df_final):,}
  • Total Kolom           : {len(df_final.columns):,}
  • Total Missing Values  : {df_final.isnull().sum().sum():,}
  • Total Duplikasi       : {duplicate_rows:,}
  • Flag Columns          : {len(flag_columns)} kolom
  • Numeric Columns       : {len(numeric_cols)} kolom
  • Output File Size      : {os.path.getsize(output_file) / 1024**2:.2f} MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 REKOMENDASI UNTUK PIVOT EXCEL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Filter rows     : Gunakan kolom 'tahun' dan 'triwulan'
  2. Rows/Columns    : 'pid', 'datakey', 'deskripsi'
  3. Values          : Kolom numerik (jika ada) atau gunakan COUNT
  4. Filters         : Flag columns (is_*, tot_flag)

💡 TIPS:
  • Gunakan ';' sebagai separator karena file disave dengan encoding UTF-8-BOM
  • Buka di Excel: Data → From Text/CSV → Pilih file → Separator ';' → Load
  • Untuk data besar (>1jt baris), pertimbangkan menggunakan Power Pivot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("🎉 PROSES SELESAI! File siap untuk dipivot di Excel! 👍")
