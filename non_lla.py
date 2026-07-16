import pandas as pd
import os

LLA_FILE_1 = "data/050526/lla_2025_202605051134.csv"
LLA_FILE_2 = "data/050526/lla_2026_202605051138.csv"

NON_LLA_FILE_1 = "data/050526/non_lla_2025_202605051140.csv"
NON_LLA_FILE_2 = "data/050526/non_lla_2026_202605051141.csv"

OUTPUT_FOLDER = "output/050526"

# ######################################
# NON LLA
# ######################################

# ======================================
# Step 1: Baca dan gabung file
# ======================================
# Baca dua file CSV
df1 = pd.read_csv(
    NON_LLA_FILE_1,
    sep=";",
    encoding="utf-8",
)
df2 = pd.read_csv(
    NON_LLA_FILE_2,
    sep=";",
    encoding="utf-8",
)

# Append (gabung baris)
df_gabung = pd.concat([df1, df2], ignore_index=True)
print(df_gabung)

# ======================================
# Step 2: Hapus duplikat
# ======================================
df_bersih = df_gabung.drop_duplicates(
    subset=["assignment_id", "tahun", "triwulan", "pid", "B3AR1Stot"]
).copy()

print(f"Sebelum hapus duplikat: {len(df_gabung)} baris")
print(f"Setelah hapus duplikat: {len(df_bersih)} baris")


# ======================================
# Step 3a: Lihat value mencurigakan di B3AR1S31 sebelum replace
# ======================================
# Lihat value unik di kolom B3AR1S31
print("Value unik di kolom B3AR1S31:")
print(df_bersih["B3AR1S31"].unique())

# Lihat juga jumlah kemunculan setiap value
print("\nJumlah kemunculan setiap value:")
print(df_bersih["B3AR1S31"].value_counts())

# Lihat beberapa sample baris dengan value tertentu
print("\nSample baris dengan value 478118377000000:")
print(df_bersih[df_bersih["B3AR1S31"] == 478118377000000].head())

print("\nSample baris dengan value 471746057000000:")
print(df_bersih[df_bersih["B3AR1S31"] == 471746057000000].head())

# ======================================
# Step 3b: Replace value
# ======================================
df_bersih.loc[:, "B3AR1S31"] = df_bersih["B3AR1S31"].replace(478118377000000, 478118377)
df_bersih.loc[:, "B3AR1S31"] = df_bersih["B3AR1S31"].replace(471746057000000, 471746057)

mask = (
    (df_bersih["pid"] == 18)
    & (df_bersih["triwulan"] == 1)
    & (df_bersih["tahun"] == 2026)
)
cols = [
    "B3AR1S00",
    "B3AR1S11",
    "B3AR1S12",
    "B3AR1S13",
    "B3AR1S14",
    "B3AR1S15",
    "B3AR1S16",
    "B3AR1S17",
    "B3AR1S18",
    "B3AR1S19",
    "B3AR1S21",
    "B3AR1S31",
    "B3AR1S32",
    "B3AR1S33",
    "B3AR1S34",
    "B3AR1S35",
    "B3AR1S36",
    "B3AR1S51",
    "B3AR1S52",
    "B3AR1S53",
    "B3AR1S61",
    "B3AR1S62",
    "B3AR1S63",
    "B3AR1S64",
    "B3AR1S65",
    "B3AR1S71",
    "B3AR1S72",
    "B3AR1S73",
    "B3AR1S74",
    "B3AR1S75",
    "B3AR1S76",
    "B3AR1S81",
    "B3AR1S82",
    "B3AR1S91",
    "B3AR1S94",
]
df_bersih.loc[mask, cols] = df_bersih.loc[mask, cols] / 100

# ======================================
# Step 3c: Lihat hasil setelah replace
# ======================================
print("\n=== SETELAH REPLACE ===")
print("Value unik di kolom B3AR1S31:")
print(df_bersih["B3AR1S31"].unique())

# Lihat beberapa sample baris dengan value tertentu
print("\nSample baris dengan value 478118377:")
print(df_bersih[df_bersih["B3AR1S31"] == 478118377].head())

print("\nSample baris dengan value 471746057:")
print(df_bersih[df_bersih["B3AR1S31"] == 471746057].head())

# ======================================
# Step 4a: Cek nilai null/NA di kolom-kolom tersebut
# ======================================
# Daftar kolom yang akan direplace null -> 0
kolom_null_to_zero = [
    "B3AR1S00",
    "B3AR1S11",
    "B3AR1S12",
    "B3AR1S13",
    "B3AR1S14",
    "B3AR1S15",
    "B3AR1S16",
    "B3AR1S17",
    "B3AR1S18",
    "B3AR1S19",
    "B3AR1S21",
    "B3AR1S31",
    "B3AR1S32",
    "B3AR1S33",
    "B3AR1S34",
    "B3AR1S35",
    "B3AR1S36",
    "B3AR1S51",
    "B3AR1S52",
    "B3AR1S53",
    "B3AR1S61",
    "B3AR1S62",
    "B3AR1S63",
    "B3AR1S64",
    "B3AR1S65",
    "B3AR1S71",
    "B3AR1S72",
    "B3AR1S73",
    "B3AR1S74",
    "B3AR1S75",
    "B3AR1S76",
    "B3AR1S81",
    "B3AR1S82",
    "B3AR1S91",
    "B3AR1S94",
]

# 1. Cek jumlah NA per kolom
print("=== JUMLAH NA PER KOLOM ===")
na_count = df_bersih[kolom_null_to_zero].isna().sum()
print(na_count[na_count > 0])  # Tampilkan hanya kolom yang punya NA

# 2. Cek apakah yang muncul bukan cuma NA tapi juga string 'null' atau 'NULL'
print("\n=== CEK VALUE UNIK DI BEBERAPA KOLOM (sample) ===")
for col in kolom_null_to_zero[:5]:  # Cek 5 kolom pertama dulu
    unique_vals = df_bersih[col].dropna().unique()
    print(f"\nKolom {col}:")
    print(f"  - Ada {df_bersih[col].isna().sum()} nilai NA")
    print(f"  - Ada {len(unique_vals)} nilai unik (non-NA)")
    if len(unique_vals) < 20:  # Kalau dikit, tampilkan
        print(f"  - Contoh nilai: {unique_vals[:10]}")

# 3. Cek tipe data kolom
print("\n=== TIPE DATA KOLOM ===")
print(df_bersih[kolom_null_to_zero].dtypes.value_counts())

# 4. Cek apakah ada string 'null' atau '' (string kosong)
print("\n=== CEK STRING 'null' ATAU KOSONG ===")
for col in kolom_null_to_zero[:10]:
    if df_bersih[col].dtype == "object":  # Kalau tipe string
        has_null_string = (df_bersih[col] == "null").any()
        has_empty_string = (df_bersih[col] == "").any()
        if has_null_string or has_empty_string:
            print(
                f"{col}: null_string={has_null_string}, empty_string={has_empty_string}"
            )

# ======================================
# Step 4b: Replace null/NA dengan 0 (sesuai M code)
# ======================================
# Replace semua NaN/Null di kolom tersebut menjadi 0
df_bersih.loc[:, kolom_null_to_zero] = df_bersih[kolom_null_to_zero].fillna(0)

# Atau pakai replace (lebih eksplisit seperti di M):
# from numpy import nan
# df_bersih[kolom_null_to_zero] = df_bersih[kolom_null_to_zero].replace([nan, None, 'null', ''], 0)

print("\n=== SETELAH REPLACE ===")
print(f"Jumlah NA setelah replace: {df_bersih[kolom_null_to_zero].isna().sum().sum()}")

# ======================================
# Step 5: Buat kolom total (penjumlahan)
# ======================================
# Daftar kolom yang akan dijumlahkan (sama seperti step 4)
kolom_total = [
    "B3AR1S00",
    "B3AR1S11",
    "B3AR1S12",
    "B3AR1S13",
    "B3AR1S14",
    "B3AR1S15",
    "B3AR1S16",
    "B3AR1S17",
    "B3AR1S18",
    "B3AR1S19",
    "B3AR1S21",
    "B3AR1S31",
    "B3AR1S32",
    "B3AR1S33",
    "B3AR1S34",
    "B3AR1S35",
    "B3AR1S36",
    "B3AR1S51",
    "B3AR1S52",
    "B3AR1S53",
    "B3AR1S61",
    "B3AR1S62",
    "B3AR1S63",
    "B3AR1S64",
    "B3AR1S65",
    "B3AR1S71",
    "B3AR1S72",
    "B3AR1S73",
    "B3AR1S74",
    "B3AR1S75",
    "B3AR1S76",
    "B3AR1S81",
    "B3AR1S82",
    "B3AR1S91",
    "B3AR1S94",
]

# Buat kolom baru dengan menjumlahkan semua kolom di atas
df_bersih.loc[:, "B3AR1Stotal"] = df_bersih[kolom_total].sum(axis=1)

# Cek hasil
print("=== KOLOM BARU B3AR1Stotal ===")
print(df_bersih[["B3AR1Stotal"]].head(10))
print(
    f"\nStatistik: Min={df_bersih['B3AR1Stotal'].min()}, Max={df_bersih['B3AR1Stotal'].max()}, Mean={df_bersih['B3AR1Stotal'].mean():.2f}"
)


# =========================================================
# STEP 6: Group per pid dan tahun untuk cek panel
# =========================================================

print("=== STEP 6: MEMBUAT KOLOM PANEL ===")

# 6a: Group by pid dan tahun, kumpulkan triwulan unik
grouped = df_bersih.groupby(["pid", "tahun"])["triwulan"].unique().reset_index()
grouped.columns = ["pid", "tahun", "triwulan_list"]


# 6b: Fungsi cek triwulan
def check_triwulan(triwulan_list, required_tw):
    triwulan_str = [str(tw) for tw in triwulan_list]
    required_str = [str(tw) for tw in required_tw]
    return all(tw in triwulan_str for tw in required_str)


# 6c: Panel dalam satu tahun (2025)
grouped["is_panel_25Q1_25Q2"] = grouped.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["triwulan_list"], [1, 2])
        else "No"
    ),
    axis=1,
)

grouped["is_panel_25Q2_25Q3"] = grouped.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["triwulan_list"], [2, 3])
        else "No"
    ),
    axis=1,
)

grouped["is_panel_25Q3_25Q4"] = grouped.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["triwulan_list"], [3, 4])
        else "No"
    ),
    axis=1,
)

grouped["is_panel_25Q1_25Q4"] = grouped.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["triwulan_list"], [1, 2, 3, 4])
        else "No"
    ),
    axis=1,
)

# 6d: Gabungkan panel per (pid, tahun) ke df_bersih
df_bersih = df_bersih.merge(
    grouped[
        [
            "pid",
            "tahun",
            "is_panel_25Q1_25Q2",
            "is_panel_25Q2_25Q3",
            "is_panel_25Q3_25Q4",
            "is_panel_25Q1_25Q4",
        ]
    ],
    on=["pid", "tahun"],
    how="left",
)

# =========================================================
# Panel lintas tahun (per pid, tanpa tahun)
# =========================================================

# 6e.1: Panel 2025 Q4 & 2026 Q1
panel_25Q4_26Q1 = (
    df_bersih.groupby("pid")
    .apply(
        lambda g: pd.Series(
            {
                "has_2025Q4": 4 in g[g["tahun"] == 2025]["triwulan"].values,
                "has_2026Q1": 1 in g[g["tahun"] == 2026]["triwulan"].values,
            }
        ),
        include_groups=False,
    )
    .reset_index()
)

panel_25Q4_26Q1["is_panel_25Q4_26Q1"] = panel_25Q4_26Q1.apply(
    lambda row: "Yes" if row["has_2025Q4"] and row["has_2026Q1"] else "No", axis=1
)

df_bersih = df_bersih.merge(
    panel_25Q4_26Q1[["pid", "is_panel_25Q4_26Q1"]], on="pid", how="left"
)

# 6e.2: Panel 2025 Q1 & 2026 Q1 (YANG KAMU MINTA)
panel_25Q1_26Q1 = (
    df_bersih.groupby("pid")
    .apply(
        lambda g: pd.Series(
            {
                "has_2025Q1": 1 in g[g["tahun"] == 2025]["triwulan"].values,
                "has_2026Q1": 1 in g[g["tahun"] == 2026]["triwulan"].values,
            }
        ),
        include_groups=False,
    )
    .reset_index()
)

panel_25Q1_26Q1["is_panel_25Q1_26Q1"] = panel_25Q1_26Q1.apply(
    lambda row: "Yes" if row["has_2025Q1"] and row["has_2026Q1"] else "No", axis=1
)

df_bersih = df_bersih.merge(
    panel_25Q1_26Q1[["pid", "is_panel_25Q1_26Q1"]], on="pid", how="left"
)

# 6e.4: Panel 2025 Q1 & 2025 Q4 & 2026 Q1
panel_25Q1_25Q4_26Q1 = (
    df_bersih.groupby("pid")
    .apply(
        lambda g: pd.Series(
            {
                "has_2025Q1": 1 in g[g["tahun"] == 2025]["triwulan"].values,
                "has_2025Q4": 4 in g[g["tahun"] == 2025]["triwulan"].values,
                "has_2026Q1": 1 in g[g["tahun"] == 2026]["triwulan"].values,
            }
        ),
        include_groups=False,
    )
    .reset_index()
)

panel_25Q1_25Q4_26Q1["is_panel_25Q1_25Q4_26Q1"] = panel_25Q1_25Q4_26Q1.apply(
    lambda row: (
        "Yes"
        if (row["has_2025Q1"] and row["has_2025Q4"] and row["has_2026Q1"])
        else "No"
    ),
    axis=1,
)

df_bersih = df_bersih.merge(
    panel_25Q1_25Q4_26Q1[["pid", "is_panel_25Q1_25Q4_26Q1"]], on="pid", how="left"
)

# 6f: Isi nilai null dengan "No" untuk semua kolom panel
panel_cols = [
    "is_panel_25Q1_25Q2",
    "is_panel_25Q2_25Q3",
    "is_panel_25Q3_25Q4",
    "is_panel_25Q1_25Q4",
    "is_panel_25Q4_26Q1",
    "is_panel_25Q1_26Q1",
    "is_panel_25Q1_25Q4_26Q1",
]

for col in panel_cols:
    if col in df_bersih.columns:
        df_bersih[col] = df_bersih[col].fillna("No")

# =========================================================
# HASIL AKHIR
# =========================================================

print("=== HASIL STEP 6 ===")
print(f"Total baris setelah merge: {len(df_bersih)}")
print(f"Total kolom: {len(df_bersih.columns)}")
print("\nSample kolom panel:")
print(
    df_bersih[
        [
            "pid",
            "tahun",
            "triwulan",
            "is_panel_25Q1_25Q2",
            "is_panel_25Q2_25Q3",
            "is_panel_25Q3_25Q4",
            "is_panel_25Q1_25Q4",
            "is_panel_25Q4_26Q1",
            "is_panel_25Q1_26Q1",
            "is_panel_25Q1_25Q4_26Q1",
        ]
    ].head(10)
)

# Cek distribusi status panel untuk tahun 2025
print("\n=== DISTRIBUSI STATUS PANEL (tahun 2025) ===")
df_2025 = df_bersih[df_bersih["tahun"] == 2025]
print(f"Q1&Q2: {df_2025['is_panel_25Q1_25Q2'].value_counts().to_dict()}")
print(f"Q2&Q3: {df_2025['is_panel_25Q2_25Q3'].value_counts().to_dict()}")
print(f"Q3&Q4: {df_2025['is_panel_25Q3_25Q4'].value_counts().to_dict()}")
print(f"Q1-Q4: {df_2025['is_panel_25Q1_25Q4'].value_counts().to_dict()}")


# Cek pid yang memiliki panel 2025Q4 & 2026Q1
print("\n=== PID dengan panel 2025Q4 & 2026Q1 ===")
sample_pid = panel_25Q4_26Q1[panel_25Q4_26Q1["is_panel_25Q4_26Q1"] == "Yes"][
    "pid"
].head(10)
print(sample_pid)

# Verifikasi manual untuk pid pertama
if len(sample_pid) > 0:
    pid_cek = sample_pid.iloc[5]
    print(f"\nVerifikasi untuk pid {pid_cek}:")
    print(
        df_bersih[df_bersih["pid"] == pid_cek][["tahun", "triwulan"]]
        .drop_duplicates()
        .sort_values(["tahun", "triwulan"])
    )

# Cek pid yang memiliki panel 2025Q1 & 2026Q1
print("\n=== PID dengan panel 2025Q1 & 2026Q1 ===")
sample_pid = panel_25Q1_26Q1[panel_25Q1_26Q1["is_panel_25Q1_26Q1"] == "Yes"][
    "pid"
].head(10)
print(sample_pid)

# Verifikasi manual untuk pid pertama
if len(sample_pid) > 0:
    pid_cek = sample_pid.iloc[5]
    print(f"\nVerifikasi untuk pid {pid_cek}:")
    print(
        df_bersih[df_bersih["pid"] == pid_cek][["tahun", "triwulan"]]
        .drop_duplicates()
        .sort_values(["tahun", "triwulan"])
    )

# ######################################
# LLA
# ######################################

# ======================================
# Step 7: Baca dan gabung file
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
print(df_gabung_lla)


# ======================================
# Step 8: Tambah kolom is_exist_lla_nonlla
# ======================================

# Tambahkan kolom baru dengan nilai konstan "Yes"
df_gabung_lla["is_exist_lla_nonlla"] = "Yes"

# Cek hasil
print("\n=== SETELAH STEP 8 ===")
print(f"Total baris: {len(df_gabung_lla)}")
print(f"Total kolom: {len(df_gabung_lla.columns)}")
print("\nSample kolom baru:")
print(df_gabung_lla[["is_exist_lla_nonlla"]].head(10))
print(
    f"\nDistribusi nilai: {df_gabung_lla['is_exist_lla_nonlla'].value_counts().to_dict()}"
)


# ======================================
# Step 9: Hapus duplikat berdasarkan assignment_id
# ======================================

# Cek jumlah sebelum hapus duplikat
print(f"Jumlah baris sebelum hapus duplikat: {len(df_gabung_lla)}")

# Hapus duplikat berdasarkan assignment_id saja
# keep='first' artinya mempertahankan baris pertama yang muncul (default)
df_bersih_lla = df_gabung_lla.drop_duplicates(
    subset=["assignment_id"], keep="first"
).copy()

print(f"Jumlah baris setelah hapus duplikat: {len(df_bersih_lla)}")
print(f"Jumlah duplikat yang dihapus: {len(df_gabung_lla) - len(df_bersih_lla)}")

# Cek hasil
print("\n=== SAMPLE DATA SETELAH HAPUS DUPILKAT ===")
print(df_bersih_lla.head(10))


# ######################################
# GABUNG NON LLA DAN LLA
# ######################################

# ======================================
# Step 10: Merge non_lla dengan lla (Left Join)
# ======================================

# Left join: df_bersih (non_lla) sebagai tabel utama
df_final = df_bersih.merge(
    df_bersih_lla[
        ["assignment_id", "is_exist_lla_nonlla"]
    ],  # ambil kolom yang diperlukan saja
    on="assignment_id",
    how="left",  # Left Outer Join
)

print(df_final)

# Cek hasil
print("=== HASIL MERGE ===")
print(f"Total baris non_lla (sebelum merge): {len(df_bersih)}")
print(f"Total baris lla: {len(df_bersih_lla)}")
print(f"Total baris final (setelah merge): {len(df_final)}")

# Cek jumlah yang match
match_count = df_final["is_exist_lla_nonlla"].notna().sum()
print(f"Jumlah baris yang match dengan lla: {match_count}")
print(f"Jumlah baris yang tidak match (NULL): {len(df_final) - match_count}")

# Cek sample hasil
print("\n=== SAMPLE HASIL MERGE ===")
print(df_final[["assignment_id", "is_exist_lla_nonlla"]].head(10))

# Cek distribusi is_exist_lla_nonlla
print("\n=== DISTRIBUSI is_exist_lla_nonlla ===")
print(df_final["is_exist_lla_nonlla"].value_counts(dropna=False))

# ======================================
# Step 11: Replace null menjadi "No"
# ======================================

# Cek nilai sebelum replace
print("=== SEBELUM REPLACE ===")
print(
    f"Jumlah null di is_exist_lla_nonlla: {df_final['is_exist_lla_nonlla'].isna().sum()}"
)
print(
    f"Distribusi nilai: {df_final['is_exist_lla_nonlla'].value_counts(dropna=False).to_dict()}"
)

# Replace null/NaN dengan "No"
df_final["is_exist_lla_nonlla"] = df_final["is_exist_lla_nonlla"].fillna("No")

# Cek setelah replace
print("\n=== SETELAH REPLACE ===")
print(
    f"Jumlah null di is_exist_lla_nonlla: {df_final['is_exist_lla_nonlla'].isna().sum()}"
)
print(f"Distribusi nilai: {df_final['is_exist_lla_nonlla'].value_counts().to_dict()}")

# Cek sample
print("\n=== SAMPLE HASIL ===")
print(df_final[["assignment_id", "is_exist_lla_nonlla"]].head(10))


# ======================================
# Step 12: Group dan cek panel untuk LLA
# ======================================

# 12a: Filter hanya yang is_exist_lla_nonlla = "Yes"
df_lla_exist = df_final[df_final["is_exist_lla_nonlla"] == "Yes"].copy()

# 12b: Group by pid dan tahun, kumpulkan triwulan unik
grouped_lla = df_lla_exist.groupby(["pid", "tahun"])["triwulan"].unique().reset_index()
grouped_lla.columns = ["pid", "tahun", "filtered_triwulan"]


# 12c: Fungsi cek triwulan
def check_triwulan(triwulan_list, required_tw):
    triwulan_str = [str(tw) for tw in triwulan_list]
    required_str = [str(tw) for tw in required_tw]
    return all(tw in triwulan_str for tw in required_str)


# 12d: Tambahkan kolom status panel (hanya untuk tahun 2025)
# Panel dalam satu tahun (2025)
grouped_lla["is_exist_25Q1_25Q2"] = grouped_lla.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["filtered_triwulan"], [1, 2])
        else "No"
    ),
    axis=1,
)

grouped_lla["is_exist_25Q2_25Q3"] = grouped_lla.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["filtered_triwulan"], [2, 3])
        else "No"
    ),
    axis=1,
)

grouped_lla["is_exist_25Q3_25Q4"] = grouped_lla.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025 and check_triwulan(row["filtered_triwulan"], [3, 4])
        else "No"
    ),
    axis=1,
)

grouped_lla["is_exist_25Q1_25Q4"] = grouped_lla.apply(
    lambda row: (
        "Yes"
        if row["tahun"] == 2025
        and check_triwulan(row["filtered_triwulan"], [1, 2, 3, 4])
        else "No"
    ),
    axis=1,
)

# ======================================
# 12e: Panel lintas tahun (beda tahun)
# ======================================

df_lla_cross = df_final[df_final["is_exist_lla_nonlla"] == "Yes"].copy()

# 12e.1: Panel lintas tahun (2025 Q4 & 2026 Q1)
grouped_lla_cross_q4 = (
    df_lla_cross.groupby("pid")
    .apply(
        lambda g: pd.Series(
            {
                "has_2025Q4": 4 in g[g["tahun"] == 2025]["triwulan"].values,
                "has_2026Q1": 1 in g[g["tahun"] == 2026]["triwulan"].values,
            }
        ),
        include_groups=False,
    )
    .reset_index()
)

grouped_lla_cross_q4["is_exist_25Q4_26Q1"] = grouped_lla_cross_q4.apply(
    lambda row: "Yes" if row["has_2025Q4"] and row["has_2026Q1"] else "No", axis=1
)

# 12e.2: Panel lintas tahun (2025 Q1 & 2026 Q1) - PERBAIKAN: pake variabel berbeda
grouped_lla_cross_q1 = (
    df_lla_cross.groupby("pid")
    .apply(
        lambda g: pd.Series(
            {
                "has_2025Q1": 1 in g[g["tahun"] == 2025]["triwulan"].values,
                "has_2026Q1": 1 in g[g["tahun"] == 2026]["triwulan"].values,
            }
        ),
        include_groups=False,
    )
    .reset_index()
)

grouped_lla_cross_q1["is_exist_25Q1_26Q1"] = grouped_lla_cross_q1.apply(
    lambda row: "Yes" if row["has_2025Q1"] and row["has_2026Q1"] else "No", axis=1
)

# Gabungkan kedua hasil lintas tahun
grouped_lla_cross = grouped_lla_cross_q4.merge(
    grouped_lla_cross_q1[["pid", "is_exist_25Q1_26Q1"]], on="pid", how="outer"
)

# ======================================
# 12f: Gabungkan semua panel ke df_final
# ======================================

# Pertama, gabungkan panel yang per (pid, tahun)
df_final = df_final.merge(
    grouped_lla[
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

# Kedua, gabungkan panel lintas tahun (per pid saja)
df_final = df_final.merge(
    grouped_lla_cross[["pid", "is_exist_25Q4_26Q1", "is_exist_25Q1_26Q1"]],
    on="pid",
    how="left",
)

# 12g: Isi nilai yang null dengan "No"
panel_cols = [
    "is_exist_25Q1_25Q2",
    "is_exist_25Q2_25Q3",
    "is_exist_25Q3_25Q4",
    "is_exist_25Q1_25Q4",
    "is_exist_25Q4_26Q1",
    "is_exist_25Q1_26Q1",
]

for col in panel_cols:
    df_final[col] = df_final[col].fillna("No")

# ======================================
# HASIL AKHIR
# ======================================
print("=== STEP 12 SELESAI ===")
print(f"Total baris df_final: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")

print("\n=== DISTRIBUSI STATUS PANEL LLA ===")
print(f"is_exist_25Q1_25Q2 (Yes): {(df_final['is_exist_25Q1_25Q2'] == 'Yes').sum()}")
print(f"is_exist_25Q2_25Q3 (Yes): {(df_final['is_exist_25Q2_25Q3'] == 'Yes').sum()}")
print(f"is_exist_25Q3_25Q4 (Yes): {(df_final['is_exist_25Q3_25Q4'] == 'Yes').sum()}")
print(f"is_exist_25Q1_25Q4 (Yes): {(df_final['is_exist_25Q1_25Q4'] == 'Yes').sum()}")
print(f"is_exist_25Q4_26Q1 (Yes): {(df_final['is_exist_25Q4_26Q1'] == 'Yes').sum()}")
print(f"is_exist_25Q1_26Q1 (Yes): {(df_final['is_exist_25Q1_26Q1'] == 'Yes').sum()}")

# ======================================
# Step 13: Replace null -> 0 dan buat kolom total untuk B4DR1 & B4DR2
# ======================================

# Daftar kolom B4DR1
kolom_b4dr1 = [
    "B4DR1S00",
    "B4DR1S11",
    "B4DR1S12",
    "B4DR1S13",
    "B4DR1S14",
    "B4DR1S15",
    "B4DR1S16",
    "B4DR1S17",
    "B4DR1S18",
    "B4DR1S19",
    "B4DR1S21",
    "B4DR1S31",
    "B4DR1S32",
    "B4DR1S33",
    "B4DR1S34",
    "B4DR1S35",
    "B4DR1S36",
    "B4DR1S51",
    "B4DR1S52",
    "B4DR1S53",
    "B4DR1S61",
    "B4DR1S62",
    "B4DR1S63",
    "B4DR1S64",
    "B4DR1S65",
    "B4DR1S71",
    "B4DR1S72",
    "B4DR1S73",
    "B4DR1S74",
    "B4DR1S75",
    "B4DR1S76",
    "B4DR1S81",
    "B4DR1S82",
    "B4DR1S91",
    "B4DR1S94",
]

# Daftar kolom B4DR2
kolom_b4dr2 = [
    "B4DR2S00",
    "B4DR2S11",
    "B4DR2S12",
    "B4DR2S13",
    "B4DR2S14",
    "B4DR2S15",
    "B4DR2S16",
    "B4DR2S17",
    "B4DR2S18",
    "B4DR2S19",
    "B4DR2S21",
    "B4DR2S31",
    "B4DR2S32",
    "B4DR2S33",
    "B4DR2S34",
    "B4DR2S35",
    "B4DR2S36",
    "B4DR2S51",
    "B4DR2S52",
    "B4DR2S53",
    "B4DR2S61",
    "B4DR2S62",
    "B4DR2S63",
    "B4DR2S64",
    "B4DR2S65",
    "B4DR2S71",
    "B4DR2S72",
    "B4DR2S73",
    "B4DR2S74",
    "B4DR2S75",
    "B4DR2S76",
    "B4DR2S81",
    "B4DR2S82",
    "B4DR2S91",
    "B4DR2S94",
]

# 13a: Replace null/NA dengan 0 untuk B4DR1
print("=== SEBELUM REPLACE B4DR1 ===")
na_b4dr1 = df_final[kolom_b4dr1].isna().sum().sum()
print(f"Total NA di kolom B4DR1: {na_b4dr1}")

df_final.loc[:, kolom_b4dr1] = df_final[kolom_b4dr1].fillna(0)

# 13b: Replace null/NA dengan 0 untuk B4DR2
print("\n=== SEBELUM REPLACE B4DR2 ===")
na_b4dr2 = df_final[kolom_b4dr2].isna().sum().sum()
print(f"Total NA di kolom B4DR2: {na_b4dr2}")

df_final.loc[:, kolom_b4dr2] = df_final[kolom_b4dr2].fillna(0)

# 13c: Buat kolom total B4DR1Stotal
df_final["B4DR1Stotal"] = df_final[kolom_b4dr1].sum(axis=1)

# 13d: Buat kolom total B4DR2Stotal
df_final["B4DR2Stotal"] = df_final[kolom_b4dr2].sum(axis=1)

# Cek hasil
print("\n=== HASIL STEP 13 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B4DR1Stotal, B4DR2Stotal")

print("\n=== STATISTIK B4DR1Stotal ===")
print(f"Min: {df_final['B4DR1Stotal'].min()}")
print(f"Max: {df_final['B4DR1Stotal'].max()}")
print(f"Mean: {df_final['B4DR1Stotal'].mean():.2f}")

print("\n=== STATISTIK B4DR2Stotal ===")
print(f"Min: {df_final['B4DR2Stotal'].min()}")
print(f"Max: {df_final['B4DR2Stotal'].max()}")
print(f"Mean: {df_final['B4DR2Stotal'].mean():.2f}")

# Sample hasil
print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B4DR1Stotal", "B4DR2Stotal"]
print(df_final[sample_cols].head(10))

# ======================================
# Step 14: Bersihkan B4ER1 (hapus .0, konversi ke int, replace null, total)
# ======================================

# Daftar kolom B4ER1
kolom_b4er1 = [
    "B4ER1S00",
    "B4ER1S11",
    "B4ER1S12",
    "B4ER1S13",
    "B4ER1S14",
    "B4ER1S15",
    "B4ER1S16",
    "B4ER1S17",
    "B4ER1S18",
    "B4ER1S19",
    "B4ER1S21",
    "B4ER1S31",
    "B4ER1S32",
    "B4ER1S33",
    "B4ER1S34",
    "B4ER1S35",
    "B4ER1S36",
    "B4ER1S51",
    "B4ER1S52",
    "B4ER1S53",
    "B4ER1S61",
    "B4ER1S62",
    "B4ER1S63",
    "B4ER1S64",
    "B4ER1S65",
    "B4ER1S71",
    "B4ER1S72",
    "B4ER1S73",
    "B4ER1S74",
    "B4ER1S75",
    "B4ER1S76",
    "B4ER1S81",
    "B4ER1S82",
    "B4ER1S91",
    "B4ER1S94",
]

# 14a: Cek tipe data sebelum proses
print("=== SEBELUM PROSES ===")
print(f"Jumlah kolom B4ER1: {len(kolom_b4er1)}")
print(f"Sample tipe data: {df_final[kolom_b4er1[0]].dtype}")

# 14b: Replace string ".0" dengan "" (hanya untuk kolom yang masih string)
for col in kolom_b4er1:
    if df_final[col].dtype == "object":  # Jika tipe string/object
        df_final.loc[:, col] = (
            df_final[col].astype(str).str.replace(".0", "", regex=False)
        )

# 14c: Konversi ke integer (Int64, bisa handle null)
for col in kolom_b4er1:
    df_final.loc[:, col] = pd.to_numeric(df_final[col], errors="coerce")

# 14d: Replace null/NA dengan 0
print("\n=== REPLACE NULL -> 0 ===")
na_before = df_final[kolom_b4er1].isna().sum().sum()
print(f"Total NA sebelum replace: {na_before}")

df_final.loc[:, kolom_b4er1] = df_final[kolom_b4er1].fillna(0)

na_after = df_final[kolom_b4er1].isna().sum().sum()
print(f"Total NA setelah replace: {na_after}")

# 14e: Buat kolom total B4ER1Stotal
df_final["B4ER1Stotal"] = df_final[kolom_b4er1].sum(axis=1)

# Cek hasil
print("\n=== HASIL STEP 14 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B4ER1Stotal")

print("\n=== STATISTIK B4ER1Stotal ===")
print(f"Min: {df_final['B4ER1Stotal'].min()}")
print(f"Max: {df_final['B4ER1Stotal'].max()}")
print(f"Mean: {df_final['B4ER1Stotal'].mean():.2f}")

print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B4ER1Stotal"] + kolom_b4er1[:3]
print(df_final[sample_cols].head(10))

# ======================================
# Step 15: Bersihkan B4ER2 (hapus .0, konversi ke int, replace null, total)
# ======================================

# Daftar kolom B4ER2
kolom_b4er2 = [
    "B4ER2S00",
    "B4ER2S11",
    "B4ER2S12",
    "B4ER2S13",
    "B4ER2S14",
    "B4ER2S15",
    "B4ER2S16",
    "B4ER2S17",
    "B4ER2S18",
    "B4ER2S19",
    "B4ER2S21",
    "B4ER2S31",
    "B4ER2S32",
    "B4ER2S33",
    "B4ER2S34",
    "B4ER2S35",
    "B4ER2S36",
    "B4ER2S51",
    "B4ER2S52",
    "B4ER2S53",
    "B4ER2S61",
    "B4ER2S62",
    "B4ER2S63",
    "B4ER2S64",
    "B4ER2S65",
    "B4ER2S71",
    "B4ER2S72",
    "B4ER2S73",
    "B4ER2S74",
    "B4ER2S75",
    "B4ER2S76",
    "B4ER2S81",
    "B4ER2S82",
    "B4ER2S91",
    "B4ER2S94",
]

# 15a: Cek sebelum proses
print("=== STEP 15: PROSES B4ER2 ===")
print(f"Jumlah kolom B4ER2: {len(kolom_b4er2)}")

# Cek apakah kolom-kolom ini ada di dataframe
cols_exist = [col for col in kolom_b4er2 if col in df_final.columns]
cols_missing = [col for col in kolom_b4er2 if col not in df_final.columns]
print(f"Kolom yang ada: {len(cols_exist)}")
if cols_missing:
    print(f"Peringatan: kolom tidak ditemukan - {cols_missing[:5]}...")

# 15b: Replace string ".0" dengan "" (hanya untuk kolom string)
for col in cols_exist:
    if df_final[col].dtype == "object":  # Jika tipe string/object
        df_final.loc[:, col] = (
            df_final[col].astype(str).str.replace(".0", "", regex=False)
        )

# 15c: Konversi ke integer (Int64, bisa handle null)
for col in cols_exist:
    df_final.loc[:, col] = pd.to_numeric(df_final[col], errors="coerce")

# 15d: Replace null/NA dengan 0
na_before = df_final[cols_exist].isna().sum().sum()
print(f"\nTotal NA sebelum replace: {na_before}")

df_final.loc[:, cols_exist] = df_final[cols_exist].fillna(0)

na_after = df_final[cols_exist].isna().sum().sum()
print(f"Total NA setelah replace: {na_after}")

# 15e: Buat kolom total B4ER2Stotal
df_final["B4ER2Stotal"] = df_final[cols_exist].sum(axis=1)

# Cek hasil
print("\n=== HASIL STEP 15 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B4ER2Stotal")

print("\n=== STATISTIK B4ER2Stotal ===")
print(f"Min: {df_final['B4ER2Stotal'].min()}")
print(f"Max: {df_final['B4ER2Stotal'].max()}")
print(f"Mean: {df_final['B4ER2Stotal'].mean():.2f}")

print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B4ER2Stotal"] + cols_exist[:3]
print(df_final[sample_cols].head(10))


# ======================================
# Step 16: Bersihkan B4ER3 (hapus .0, konversi ke int, replace null, total)
# ======================================

# Daftar kolom B4ER3
kolom_b4er3 = [
    "B4ER3S00",
    "B4ER3S11",
    "B4ER3S12",
    "B4ER3S13",
    "B4ER3S14",
    "B4ER3S15",
    "B4ER3S16",
    "B4ER3S17",
    "B4ER3S18",
    "B4ER3S19",
    "B4ER3S21",
    "B4ER3S31",
    "B4ER3S32",
    "B4ER3S33",
    "B4ER3S34",
    "B4ER3S35",
    "B4ER3S36",
    "B4ER3S51",
    "B4ER3S52",
    "B4ER3S53",
    "B4ER3S61",
    "B4ER3S62",
    "B4ER3S63",
    "B4ER3S64",
    "B4ER3S65",
    "B4ER3S71",
    "B4ER3S72",
    "B4ER3S73",
    "B4ER3S74",
    "B4ER3S75",
    "B4ER3S76",
    "B4ER3S81",
    "B4ER3S82",
    "B4ER3S91",
    "B4ER3S94",
]

# 16a: Cek sebelum proses
print("=== STEP 16: PROSES B4ER3 ===")
print(f"Jumlah kolom B4ER3: {len(kolom_b4er3)}")

# Cek apakah kolom-kolom ini ada di dataframe
cols_exist = [col for col in kolom_b4er3 if col in df_final.columns]
cols_missing = [col for col in kolom_b4er3 if col not in df_final.columns]
print(f"Kolom yang ada: {len(cols_exist)}")
if cols_missing:
    print(f"Peringatan: kolom tidak ditemukan - {cols_missing[:5]}...")

# 16b: Replace string ".0" dengan "" (hanya untuk kolom string)
for col in cols_exist:
    if df_final[col].dtype == "object":  # Jika tipe string/object
        df_final.loc[:, col] = (
            df_final[col].astype(str).str.replace(".0", "", regex=False)
        )

# 16c: Konversi ke integer (Int64, bisa handle null)
for col in cols_exist:
    df_final.loc[:, col] = pd.to_numeric(df_final[col], errors="coerce")

# 16d: Replace null/NA dengan 0
na_before = df_final[cols_exist].isna().sum().sum()
print(f"\nTotal NA sebelum replace: {na_before}")

df_final.loc[:, cols_exist] = df_final[cols_exist].fillna(0)

na_after = df_final[cols_exist].isna().sum().sum()
print(f"Total NA setelah replace: {na_after}")

# 16e: Buat kolom total B4ER3Stotal
df_final["B4ER3Stotal"] = df_final[cols_exist].sum(axis=1)

# Cek hasil
print("\n=== HASIL STEP 16 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B4ER3Stotal")

print("\n=== STATISTIK B4ER3Stotal ===")
print(f"Min: {df_final['B4ER3Stotal'].min()}")
print(f"Max: {df_final['B4ER3Stotal'].max()}")
print(f"Mean: {df_final['B4ER3Stotal'].mean():.2f}")

# Cek distribusi (berapa banyak yang totalnya 0)
zero_count = (df_final["B4ER3Stotal"] == 0).sum()
print(
    f"\nJumlah baris dengan B4ER3Stotal = 0: {zero_count} ({zero_count/len(df_final)*100:.1f}%)"
)

print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B4ER3Stotal"] + cols_exist[:3]
print(df_final[sample_cols].head(10))

# ======================================
# Step 17: Bersihkan B4ER4 (hapus .0, konversi ke int, replace null, total)
# ======================================

# Daftar kolom B4ER4
kolom_b4er4 = [
    "B4ER4S00",
    "B4ER4S11",
    "B4ER4S12",
    "B4ER4S13",
    "B4ER4S14",
    "B4ER4S15",
    "B4ER4S16",
    "B4ER4S17",
    "B4ER4S18",
    "B4ER4S19",
    "B4ER4S21",
    "B4ER4S31",
    "B4ER4S32",
    "B4ER4S33",
    "B4ER4S34",
    "B4ER4S35",
    "B4ER4S36",
    "B4ER4S51",
    "B4ER4S52",
    "B4ER4S53",
    "B4ER4S61",
    "B4ER4S62",
    "B4ER4S63",
    "B4ER4S64",
    "B4ER4S65",
    "B4ER4S71",
    "B4ER4S72",
    "B4ER4S73",
    "B4ER4S74",
    "B4ER4S75",
    "B4ER4S76",
    "B4ER4S81",
    "B4ER4S82",
    "B4ER4S91",
    "B4ER4S94",
]

# 17a: Cek sebelum proses
print("=== STEP 17: PROSES B4ER4 ===")
print(f"Jumlah kolom B4ER4: {len(kolom_b4er4)}")

# Cek apakah kolom-kolom ini ada di dataframe
cols_exist = [col for col in kolom_b4er4 if col in df_final.columns]
cols_missing = [col for col in kolom_b4er4 if col not in df_final.columns]
print(f"Kolom yang ada: {len(cols_exist)}")
if cols_missing:
    print(f"Peringatan: kolom tidak ditemukan - {cols_missing[:5]}...")

# 17b: Replace string ".0" dengan "" (hanya untuk kolom string)
for col in cols_exist:
    if df_final[col].dtype == "object":  # Jika tipe string/object
        df_final.loc[:, col] = (
            df_final[col].astype(str).str.replace(".0", "", regex=False)
        )

# 17c: Konversi ke integer (Int64, bisa handle null)
for col in cols_exist:
    df_final.loc[:, col] = pd.to_numeric(df_final[col], errors="coerce")

# 17d: Replace null/NA dengan 0
na_before = df_final[cols_exist].isna().sum().sum()
print(f"\nTotal NA sebelum replace: {na_before}")

df_final.loc[:, cols_exist] = df_final[cols_exist].fillna(0)

na_after = df_final[cols_exist].isna().sum().sum()
print(f"Total NA setelah replace: {na_after}")

# 17e: Buat kolom total B4ER4Stotal
df_final["B4ER4Stotal"] = df_final[cols_exist].sum(axis=1)

# Cek hasil
print("\n=== HASIL STEP 17 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B4ER4Stotal")

print("\n=== STATISTIK B4ER4Stotal ===")
print(f"Min: {df_final['B4ER4Stotal'].min()}")
print(f"Max: {df_final['B4ER4Stotal'].max()}")
print(f"Mean: {df_final['B4ER4Stotal'].mean():.2f}")

# Cek distribusi (berapa banyak yang totalnya 0)
zero_count = (df_final["B4ER4Stotal"] == 0).sum()
print(
    f"\nJumlah baris dengan B4ER4Stotal = 0: {zero_count} ({zero_count/len(df_final)*100:.1f}%)"
)

print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B4ER4Stotal"] + cols_exist[:3]
print(df_final[sample_cols].head(10))

# ======================================
# Step 18: Replace null -> 0 dan buat kolom total untuk B3BR1
# ======================================

# Daftar kolom B3BR1
kolom_b3br1 = [
    "B3BR1S00",
    "B3BR1S11",
    "B3BR1S12",
    "B3BR1S13",
    "B3BR1S14",
    "B3BR1S15",
    "B3BR1S16",
    "B3BR1S17",
    "B3BR1S18",
    "B3BR1S19",
    "B3BR1S21",
    "B3BR1S31",
    "B3BR1S32",
    "B3BR1S33",
    "B3BR1S34",
    "B3BR1S35",
    "B3BR1S36",
    "B3BR1S51",
    "B3BR1S52",
    "B3BR1S53",
    "B3BR1S61",
    "B3BR1S62",
    "B3BR1S63",
    "B3BR1S64",
    "B3BR1S65",
    "B3BR1S71",
    "B3BR1S72",
    "B3BR1S73",
    "B3BR1S74",
    "B3BR1S75",
    "B3BR1S76",
    "B3BR1S81",
    "B3BR1S82",
    "B3BR1S91",
    "B3BR1S94",
]

# 18a: Cek sebelum proses
print("=== STEP 18: PROSES B3BR1 ===")
print(f"Jumlah kolom B3BR1: {len(kolom_b3br1)}")

# Cek apakah kolom-kolom ini ada di dataframe
cols_exist = [col for col in kolom_b3br1 if col in df_final.columns]
cols_missing = [col for col in kolom_b3br1 if col not in df_final.columns]
print(f"Kolom yang ada: {len(cols_exist)}")
if cols_missing:
    print(f"Peringatan: kolom tidak ditemukan - {cols_missing[:5]}...")

# 18b: Cek tipe data dan NA sebelum replace
print("\n=== SEBELUM REPLACE ===")
print(
    f"Sample tipe data kolom pertama: {df_final[cols_exist[0]].dtype if cols_exist else 'N/A'}"
)
na_before = df_final[cols_exist].isna().sum().sum()
print(f"Total NA sebelum replace: {na_before}")

# 18c: Replace null/NA dengan 0
df_final.loc[:, cols_exist] = df_final[cols_exist].fillna(0)

# 18d: Buat kolom total B3BR1Stotal
df_final["B3BR1Stotal"] = df_final[cols_exist].sum(axis=1)

# Cek hasil
print("\n=== HASIL STEP 18 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B3BR1Stotal")

print("\n=== STATISTIK B3BR1Stotal ===")
print(f"Min: {df_final['B3BR1Stotal'].min()}")
print(f"Max: {df_final['B3BR1Stotal'].max()}")
print(f"Mean: {df_final['B3BR1Stotal'].mean():.2f}")

# Cek distribusi (berapa banyak yang totalnya 0)
zero_count = (df_final["B3BR1Stotal"] == 0).sum()
print(
    f"\nJumlah baris dengan B3BR1Stotal = 0: {zero_count} ({zero_count/len(df_final)*100:.1f}%)"
)

print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B3BR1Stotal"] + cols_exist[:3]
print(df_final[sample_cols].head(10))

# ======================================
# Step 19: Buat kolom total untuk B4BR1 dan B4BR2
# ======================================

# Daftar kolom B4BR1
kolom_b4br1 = [
    "B4BR1S00",
    "B4BR1S11",
    "B4BR1S12",
    "B4BR1S13",
    "B4BR1S14",
    "B4BR1S15",
    "B4BR1S16",
    "B4BR1S17",
    "B4BR1S18",
    "B4BR1S19",
    "B4BR1S21",
    "B4BR1S31",
    "B4BR1S32",
    "B4BR1S33",
    "B4BR1S34",
    "B4BR1S35",
    "B4BR1S36",
    "B4BR1S51",
    "B4BR1S52",
    "B4BR1S53",
    "B4BR1S61",
    "B4BR1S62",
    "B4BR1S63",
    "B4BR1S64",
    "B4BR1S65",
    "B4BR1S71",
    "B4BR1S72",
    "B4BR1S73",
    "B4BR1S74",
    "B4BR1S75",
    "B4BR1S76",
    "B4BR1S81",
    "B4BR1S82",
    "B4BR1S91",
    "B4BR1S94",
]

# Daftar kolom B4BR2
kolom_b4br2 = [
    "B4BR2S00",
    "B4BR2S11",
    "B4BR2S12",
    "B4BR2S13",
    "B4BR2S14",
    "B4BR2S15",
    "B4BR2S16",
    "B4BR2S17",
    "B4BR2S18",
    "B4BR2S19",
    "B4BR2S21",
    "B4BR2S31",
    "B4BR2S32",
    "B4BR2S33",
    "B4BR2S34",
    "B4BR2S35",
    "B4BR2S36",
    "B4BR2S51",
    "B4BR2S52",
    "B4BR2S53",
    "B4BR2S61",
    "B4BR2S62",
    "B4BR2S63",
    "B4BR2S64",
    "B4BR2S65",
    "B4BR2S71",
    "B4BR2S72",
    "B4BR2S73",
    "B4BR2S74",
    "B4BR2S75",
    "B4BR2S76",
    "B4BR2S81",
    "B4BR2S82",
    "B4BR2S91",
    "B4BR2S94",
]

# 19a: Proses B4BR1
print("=== STEP 19: PROSES B4BR1 & B4BR2 ===")

# Cek kolom B4BR1 yang ada
cols_b4br1_exist = [col for col in kolom_b4br1 if col in df_final.columns]
print(f"B4BR1 - Kolom yang ada: {len(cols_b4br1_exist)} / {len(kolom_b4br1)}")

if cols_b4br1_exist:
    # Cek NA sebelum (untuk safety)
    na_before = df_final[cols_b4br1_exist].isna().sum().sum()
    if na_before > 0:
        print(f"  Peringatan: Ada {na_before} nilai NA di B4BR1, akan diisi 0")
        df_final.loc[:, cols_b4br1_exist] = df_final[cols_b4br1_exist].fillna(0)

    # Buat kolom total
    df_final["B4BR1Stotal"] = df_final[cols_b4br1_exist].sum(axis=1)
    print(
        f"  B4BR1Stotal - Range: {df_final['B4BR1Stotal'].min()} - {df_final['B4BR1Stotal'].max()}"
    )

# 19b: Proses B4BR2
cols_b4br2_exist = [col for col in kolom_b4br2 if col in df_final.columns]
print(f"\nB4BR2 - Kolom yang ada: {len(cols_b4br2_exist)} / {len(kolom_b4br2)}")

if cols_b4br2_exist:
    # Cek NA sebelum (untuk safety)
    na_before = df_final[cols_b4br2_exist].isna().sum().sum()
    if na_before > 0:
        print(f"  Peringatan: Ada {na_before} nilai NA di B4BR2, akan diisi 0")
        df_final.loc[:, cols_b4br2_exist] = df_final[cols_b4br2_exist].fillna(0)

    # Buat kolom total
    df_final["B4BR2Stotal"] = df_final[cols_b4br2_exist].sum(axis=1)
    print(
        f"  B4BR2Stotal - Range: {df_final['B4BR2Stotal'].min()} - {df_final['B4BR2Stotal'].max()}"
    )

# Cek hasil akhir
print("\n=== HASIL STEP 19 ===")
print(f"Total baris: {len(df_final)}")
print(f"Total kolom: {len(df_final.columns)}")
print(f"Kolom baru: B4BR1Stotal, B4BR2Stotal")

print("\n=== SAMPLE DATA ===")
sample_cols = ["assignment_id", "B4BR1Stotal", "B4BR2Stotal"]
if "B4BR1Stotal" in df_final.columns and "B4BR2Stotal" in df_final.columns:
    print(df_final[sample_cols].head(10))

# ======================================
# Step 20: Bersihkan B4CR1 (hapus .0, konversi ke int, replace null, total)
# ======================================

# Daftar kolom B4CR1
kolom_b4cr1 = [
    "B4CR1S00",
    "B4CR1S11",
    "B4CR1S12",
    "B4CR1S13",
    "B4CR1S14",
    "B4CR1S15",
    "B4CR1S16",
    "B4CR1S17",
    "B4CR1S18",
    "B4CR1S19",
    "B4CR1S21",
    "B4CR1S31",
    "B4CR1S32",
    "B4CR1S33",
    "B4CR1S34",
    "B4CR1S35",
    "B4CR1S36",
    "B4CR1S51",
    "B4CR1S52",
    "B4CR1S53",
    "B4CR1S61",
    "B4CR1S62",
    "B4CR1S63",
    "B4CR1S64",
    "B4CR1S65",
    "B4CR1S71",
    "B4CR1S72",
    "B4CR1S73",
    "B4CR1S74",
    "B4CR1S75",
    "B4CR1S76",
    "B4CR1S81",
    "B4CR1S82",
    "B4CR1S91",
    "B4CR1S94",
]

# 20a: Cek sebelum proses
print("=== STEP 20: PROSES B4CR1 ===")
print(f"Jumlah kolom B4CR1: {len(kolom_b4cr1)}")

# Cek apakah kolom-kolom ini ada di dataframe
cols_exist = [col for col in kolom_b4cr1 if col in df_final.columns]
cols_missing = [col for col in kolom_b4cr1 if col not in df_final.columns]
print(f"Kolom yang ada: {len(cols_exist)}")
if cols_missing:
    print(f"Peringatan: kolom tidak ditemukan - {cols_missing[:5]}...")

if cols_exist:
    # 20b: Replace string ".0" dengan "" (hanya untuk kolom string)
    for col in cols_exist:
        if df_final[col].dtype == "object":  # Jika tipe string/object
            df_final.loc[:, col] = (
                df_final[col].astype(str).str.replace(".0", "", regex=False)
            )

    # 20c: Konversi ke integer (Int64, bisa handle null)
    for col in cols_exist:
        df_final.loc[:, col] = pd.to_numeric(df_final[col], errors="coerce")

    # 20d: Replace null/NA dengan 0
    na_before = df_final[cols_exist].isna().sum().sum()
    print(f"\nTotal NA sebelum replace: {na_before}")

    df_final.loc[:, cols_exist] = df_final[cols_exist].fillna(0)

    # 20e: Buat kolom total B4CR1Stotal
    df_final["B4CR1Stotal"] = df_final[cols_exist].sum(axis=1)

    # Cek hasil
    print("\n=== HASIL STEP 20 ===")
    print(f"Total baris: {len(df_final)}")
    print(f"Total kolom: {len(df_final.columns)}")
    print(f"Kolom baru: B4CR1Stotal")

    print("\n=== STATISTIK B4CR1Stotal ===")
    print(f"Min: {df_final['B4CR1Stotal'].min()}")
    print(f"Max: {df_final['B4CR1Stotal'].max()}")
    print(f"Mean: {df_final['B4CR1Stotal'].mean():.2f}")

    # Cek distribusi (berapa banyak yang totalnya 0)
    zero_count = (df_final["B4CR1Stotal"] == 0).sum()
    print(
        f"\nJumlah baris dengan B4CR1Stotal = 0: {zero_count} ({zero_count/len(df_final)*100:.1f}%)"
    )

    print("\n=== SAMPLE DATA ===")
    sample_cols = ["assignment_id", "B4CR1Stotal"] + cols_exist[:3]
    print(df_final[sample_cols].head(10))
else:
    print("Tidak ada kolom B4CR1 yang ditemukan, proses dilewati.")

# ======================================
# Step 21: Bersihkan B4CR2 (hapus .0, konversi ke int, replace null, total)
# ======================================

# Daftar kolom B4CR2
kolom_b4cr2 = [
    "B4CR2S00",
    "B4CR2S11",
    "B4CR2S12",
    "B4CR2S13",
    "B4CR2S14",
    "B4CR2S15",
    "B4CR2S16",
    "B4CR2S17",
    "B4CR2S18",
    "B4CR2S19",
    "B4CR2S21",
    "B4CR2S31",
    "B4CR2S32",
    "B4CR2S33",
    "B4CR2S34",
    "B4CR2S35",
    "B4CR2S36",
    "B4CR2S51",
    "B4CR2S52",
    "B4CR2S53",
    "B4CR2S61",
    "B4CR2S62",
    "B4CR2S63",
    "B4CR2S64",
    "B4CR2S65",
    "B4CR2S71",
    "B4CR2S72",
    "B4CR2S73",
    "B4CR2S74",
    "B4CR2S75",
    "B4CR2S76",
    "B4CR2S81",
    "B4CR2S82",
    "B4CR2S91",
    "B4CR2S94",
]

# 21a: Cek sebelum proses
print("=== STEP 21: PROSES B4CR2 (FINAL) ===")
print(f"Jumlah kolom B4CR2: {len(kolom_b4cr2)}")

# Cek apakah kolom-kolom ini ada di dataframe
cols_exist = [col for col in kolom_b4cr2 if col in df_final.columns]
cols_missing = [col for col in kolom_b4cr2 if col not in df_final.columns]
print(f"Kolom yang ada: {len(cols_exist)}")
if cols_missing:
    print(f"Peringatan: kolom tidak ditemukan - {cols_missing[:5]}...")

if cols_exist:
    # 21b: Replace string ".0" dengan "" (hanya untuk kolom string)
    for col in cols_exist:
        if df_final[col].dtype == "object":
            df_final.loc[:, col] = (
                df_final[col].astype(str).str.replace(".0", "", regex=False)
            )

    # 21c: Konversi ke integer
    for col in cols_exist:
        df_final.loc[:, col] = pd.to_numeric(df_final[col], errors="coerce")

    # 21d: Replace null/NA dengan 0
    na_before = df_final[cols_exist].isna().sum().sum()
    print(f"\nTotal NA sebelum replace: {na_before}")

    df_final.loc[:, cols_exist] = df_final[cols_exist].fillna(0)

    # 21e: Buat kolom total B4CR2Stotal
    df_final["B4CR2Stotal"] = df_final[cols_exist].sum(axis=1)

    # Cek hasil
    print("\n=== HASIL STEP 21 ===")
    print(f"Total baris: {len(df_final)}")
    print(f"Total kolom: {len(df_final.columns)}")
    print(f"Kolom baru: B4CR2Stotal")

    print("\n=== STATISTIK B4CR2Stotal ===")
    print(f"Min: {df_final['B4CR2Stotal'].min()}")
    print(f"Max: {df_final['B4CR2Stotal'].max()}")
    print(f"Mean: {df_final['B4CR2Stotal'].mean():.2f}")

    zero_count = (df_final["B4CR2Stotal"] == 0).sum()
    print(
        f"\nJumlah baris dengan B4CR2Stotal = 0: {zero_count} ({zero_count/len(df_final)*100:.1f}%)"
    )
else:
    print("Tidak ada kolom B4CR2 yang ditemukan, proses dilewati.")

# ======================================
# Step 22: Kolom Agregasi Regional untuk B3AR1 dan B3BR1
# ======================================

print("=== STEP 22: MEMBUAT KOLOM REGIONAL ===")

# ----------------------------------------------------------------------
# B3AR1 - Regional
# ----------------------------------------------------------------------

# Sumatra_B3AR1
df_final["Sumatra_B3AR1"] = (
    df_final["B3AR1S11"]
    + df_final["B3AR1S12"]
    + df_final["B3AR1S13"]
    + df_final["B3AR1S14"]
    + df_final["B3AR1S15"]
    + df_final["B3AR1S16"]
    + df_final["B3AR1S17"]
    + df_final["B3AR1S18"]
    + df_final["B3AR1S19"]
    + df_final["B3AR1S21"]
)

# Jawa_B3AR1
df_final["Jawa_B3AR1"] = (
    df_final["B3AR1S31"]
    + df_final["B3AR1S32"]
    + df_final["B3AR1S33"]
    + df_final["B3AR1S34"]
    + df_final["B3AR1S35"]
    + df_final["B3AR1S36"]
)

# Bali-Nusra_B3AR1
df_final["Bali-Nusra_B3AR1"] = (
    df_final["B3AR1S51"] + df_final["B3AR1S52"] + df_final["B3AR1S53"]
)

# Kalimantan_B3AR1
df_final["Kalimantan_B3AR1"] = (
    df_final["B3AR1S61"]
    + df_final["B3AR1S62"]
    + df_final["B3AR1S63"]
    + df_final["B3AR1S64"]
    + df_final["B3AR1S65"]
)

# Sulawesi_B3AR1
df_final["Sulawesi_B3AR1"] = (
    df_final["B3AR1S71"]
    + df_final["B3AR1S72"]
    + df_final["B3AR1S73"]
    + df_final["B3AR1S74"]
    + df_final["B3AR1S75"]
    + df_final["B3AR1S76"]
)

# Maluku-Papua_B3AR1
df_final["Maluku-Papua_B3AR1"] = (
    df_final["B3AR1S81"]
    + df_final["B3AR1S82"]
    + df_final["B3AR1S91"]
    + df_final["B3AR1S94"]
)

# ----------------------------------------------------------------------
# B3BR1 - Regional
# ----------------------------------------------------------------------

# Sumatra_B3BR1
df_final["Sumatra_B3BR1"] = (
    df_final["B3BR1S11"]
    + df_final["B3BR1S12"]
    + df_final["B3BR1S13"]
    + df_final["B3BR1S14"]
    + df_final["B3BR1S15"]
    + df_final["B3BR1S16"]
    + df_final["B3BR1S17"]
    + df_final["B3BR1S18"]
    + df_final["B3BR1S19"]
    + df_final["B3BR1S21"]
)

# Jawa_B3BR1
df_final["Jawa_B3BR1"] = (
    df_final["B3BR1S31"]
    + df_final["B3BR1S32"]
    + df_final["B3BR1S33"]
    + df_final["B3BR1S34"]
    + df_final["B3BR1S35"]
    + df_final["B3BR1S36"]
)

# Bali-Nusra_B3BR1
df_final["Bali-Nusra_B3BR1"] = (
    df_final["B3BR1S51"] + df_final["B3BR1S52"] + df_final["B3BR1S53"]
)

# Kalimantan_B3BR1
df_final["Kalimantan_B3BR1"] = (
    df_final["B3BR1S61"]
    + df_final["B3BR1S62"]
    + df_final["B3BR1S63"]
    + df_final["B3BR1S64"]
    + df_final["B3BR1S65"]
)

# Sulawesi_B3BR1
df_final["Sulawesi_B3BR1"] = (
    df_final["B3BR1S71"]
    + df_final["B3BR1S72"]
    + df_final["B3BR1S73"]
    + df_final["B3BR1S74"]
    + df_final["B3BR1S75"]
    + df_final["B3BR1S76"]
)

# Maluku-Papua_B3BR1
df_final["Maluku-Papua_B3BR1"] = (
    df_final["B3BR1S81"]
    + df_final["B3BR1S82"]
    + df_final["B3BR1S91"]
    + df_final["B3BR1S94"]
)

print("✅ 12 kolom regional berhasil dibuat (6 untuk B3AR1 + 6 untuk B3BR1)")

# Cek statistik kolom regional
print("\n=== STATISTIK KOLOM REGIONAL B3AR1 ===")
regional_cols_b3ar1 = [
    "Sumatra_B3AR1",
    "Jawa_B3AR1",
    "Bali-Nusra_B3AR1",
    "Kalimantan_B3AR1",
    "Sulawesi_B3AR1",
    "Maluku-Papua_B3AR1",
]

for col in regional_cols_b3ar1:
    if col in df_final.columns:
        zero_count = (df_final[col] == 0).sum()
        print(f"{col:20} | Zero: {zero_count:8} | Total: {df_final[col].sum():15.0f}")

print("\n=== STATISTIK KOLOM REGIONAL B3BR1 ===")
regional_cols_b3br1 = [
    "Sumatra_B3BR1",
    "Jawa_B3BR1",
    "Bali-Nusra_B3BR1",
    "Kalimantan_B3BR1",
    "Sulawesi_B3BR1",
    "Maluku-Papua_B3BR1",
]

for col in regional_cols_b3br1:
    if col in df_final.columns:
        zero_count = (df_final[col] == 0).sum()
        print(f"{col:20} | Zero: {zero_count:8} | Total: {df_final[col].sum():15.0f}")

# Verifikasi total regional = total keseluruhan
if "B3AR1Stotal" in df_final.columns:
    total_regional_b3ar1 = df_final[regional_cols_b3ar1].sum(axis=1)
    match = (total_regional_b3ar1 == df_final["B3AR1Stotal"]).all()
    print(f"\nVerifikasi B3AR1: Total regional = Total keseluruhan? {match}")

if "B3BR1Stotal" in df_final.columns:
    total_regional_b3br1 = df_final[regional_cols_b3br1].sum(axis=1)
    match = (total_regional_b3br1 == df_final["B3BR1Stotal"]).all()
    print(f"Verifikasi B3BR1: Total regional = Total keseluruhan? {match}")


# Update final summary dengan kolom regional
print("\n" + "=" * 60)
print("=== FINAL SUMMARY - SEMUA KOLOM (termasuk regional) ===")
print("=" * 60)

all_total_columns = [
    # Existing totals
    "B3AR1Stotal",
    "B4DR1Stotal",
    "B4DR2Stotal",
    "B4ER1Stotal",
    "B4ER2Stotal",
    "B4ER3Stotal",
    "B4ER4Stotal",
    "B3BR1Stotal",
    "B4BR1Stotal",
    "B4BR2Stotal",
    "B4CR1Stotal",
    "B4CR2Stotal",
    # Regional B3AR1
    "Sumatra_B3AR1",
    "Jawa_B3AR1",
    "Bali-Nusra_B3AR1",
    "Kalimantan_B3AR1",
    "Sulawesi_B3AR1",
    "Maluku-Papua_B3AR1",
    # Regional B3BR1
    "Sumatra_B3BR1",
    "Jawa_B3BR1",
    "Bali-Nusra_B3BR1",
    "Kalimantan_B3BR1",
    "Sulawesi_B3BR1",
    "Maluku-Papua_B3BR1",
]

print(f"\n{'Kolom':<25} {'Zero Values':<15} {'Range'}")
print("-" * 60)

for col in all_total_columns:
    if col in df_final.columns:
        zero_count = (df_final[col] == 0).sum()
        min_val = df_final[col].min()
        max_val = df_final[col].max()
        print(
            f"{col:<25} {zero_count:>10} ({zero_count/len(df_final)*100:>5.1f}%)   {min_val:>10.0f} - {max_val:>10.0f}"
        )
    else:
        print(f"{col:<25} {'TIDAK DITEMUKAN'}")

print("=" * 60)
print(f"Total baris final: {len(df_final)}")
print(f"Total kolom final: {len(df_final.columns)}")
print("=" * 60)

# EXPORT KE CSV
df_final.to_csv(
    os.path.join(OUTPUT_FOLDER, "df_final.csv"),
    sep=";",
    index=False,
    encoding="utf-8-sig",
)
print("✅ File CSV telah disimpan: df_final.csv")


# ======================================
# Step 23: Investigasi model_bisnis yang tidak konsisten per pid
# ======================================

print("=== STEP 23: CEK KONSISTENSI MODEL BISNIS PER PID ===")

# 23a: Cek apakah kolom model_bisnis dan model_bisnis_id ada
model_cols = ["model_bisnis", "model_bisnis_id"]
available_cols = [col for col in model_cols if col in df_final.columns]

if not available_cols:
    print(
        "❌ Kolom 'model_bisnis' atau 'model_bisnis_id' tidak ditemukan di dataframe!"
    )
    print(f"Kolom yang tersedia: {df_final.columns.tolist()}")
else:
    print(f"✅ Kolom ditemukan: {available_cols}")

    # 23b: Group by pid, cek berapa nilai unik model_bisnis per pid
    print("\n=== CEK PER PID ===")

    # Hitung jumlah nilai unik model_bisnis per pid
    unique_models_per_pid = (
        df_final.groupby("pid")["model_bisnis"].nunique().reset_index()
    )
    unique_models_per_pid.columns = ["pid", "jumlah_model_unik"]

    # Filter pid yang punya lebih dari 1 model_bisnis (tidak konsisten)
    inconsistent_pids = unique_models_per_pid[
        unique_models_per_pid["jumlah_model_unik"] > 1
    ]

    print(f"Total PID unik: {len(unique_models_per_pid)}")
    print(
        f"PID dengan model_bisnis TIDAK KONSISTEN (lebih dari 1): {len(inconsistent_pids)}"
    )

    if len(inconsistent_pids) > 0:
        print(f"\nDaftar PID yang tidak konsisten (sample 10):")
        print(inconsistent_pids.head(10))

        # 23c: Tampilkan detail untuk PID yang tidak konsisten
        print("\n=== DETAIL PID YANG TIDAK KONSISTEN ===")
        for pid in inconsistent_pids["pid"].head(5):  # Ambil 5 sample
            print(f"\n--- PID: {pid} ---")
            detail = df_final[df_final["pid"] == pid][
                ["pid", "tahun", "triwulan", "model_bisnis", "model_bisnis_id"]
            ]
            print(detail.to_string(index=False))
    else:
        print("✅ Semua PID memiliki model_bisnis yang konsisten!")

    # 23d: Tampilkan distribusi model_bisnis
    print("\n=== DISTRIBUSI MODEL BISNIS ===")
    print(df_final["model_bisnis"].value_counts())

    # 23e: Buat list khusus untuk PID yang bermasalah
    if len(inconsistent_pids) > 0:
        # Buat dataframe khusus untuk PID yang tidak konsisten
        df_inconsistent = df_final[
            df_final["pid"].isin(inconsistent_pids["pid"])
        ].copy()

        # Urutkan berdasarkan pid, tahun, triwulan
        df_inconsistent = df_inconsistent.sort_values(["pid", "tahun", "triwulan"])

        print(f"\n=== DATA PID BERMASALAH (TOTAL {len(df_inconsistent)} BARIS) ===")
        print(
            df_inconsistent[
                ["pid", "tahun", "triwulan", "model_bisnis", "model_bisnis_id"]
            ].head(20)
        )

        # 23f: Simpan ke CSV untuk analisa lebih lanjut
        df_inconsistent.to_csv(
            os.path.join(OUTPUT_FOLDER, "pid_model_bisnis_inconsistent.csv"),
            sep=";",
            index=False,
            encoding="utf-8-sig",
        )
        print(
            "\n✅ File 'pid_model_bisnis_inconsistent.csv' telah disimpan untuk analisa lanjutan"
        )

        # 23g: Ringkasan per pid (model bisnis apa saja yang muncul)
        print("\n=== RINGKASAN PER PID BERMASALAH ===")
        summary = (
            df_inconsistent.groupby("pid")["model_bisnis"]
            .apply(lambda x: x.unique().tolist())
            .reset_index()
        )
        summary.columns = ["pid", "model_bisnis_yang_muncul"]
        print(summary.to_string(index=False))

# ======================================
# Step 24: Backfill dengan data terakhir (FLEKSIBEL)
# ======================================

print("=== STEP 24: BACKFILL DENGAN DATA TERAKHIR (FLEKSIBEL) ===")

if "model_bisnis" in df_final.columns and "model_bisnis_id" in df_final.columns:

    # 24a: Urutkan dan ambil data terakhir per pid (berdasarkan tahun dan triwulan tertinggi)
    df_sorted = df_final.sort_values(["pid", "tahun", "triwulan"])

    # Ambil nilai terakhir untuk setiap pid
    last_model = (
        df_sorted.groupby("pid")[["model_bisnis", "model_bisnis_id"]]
        .last()
        .reset_index()
    )
    last_model.columns = ["pid", "model_bisnis_last", "model_bisnis_id_last"]

    # 24b: Cek dari tahun/triwulan berapa data terakhir diambil
    last_tw = df_sorted.groupby("pid")[["tahun", "triwulan"]].last().reset_index()
    last_tw.columns = ["pid", "tahun_last", "triwulan_last"]

    # Gabungkan info
    last_model = last_model.merge(last_tw, on="pid", how="left")

    print("\n📊 INFORMASI DATA TERAKHIR PER PID:")
    print(f"  - Rata-rata tahun terakhir: {last_model['tahun_last'].mean():.0f}")
    print(f"  - Distribusi triwulan terakhir:")
    print(last_model["triwulan_last"].value_counts().sort_index())

    # Tampilkan sample PID dengan tahun terakhir yang berbeda
    print("\n📋 SAMPLE PID dengan tahun terakhir:")
    print(last_model.head(10).to_string(index=False))

    # 24c: Backfill data lama dengan nilai terakhir
    df_final = df_final.merge(
        last_model[["pid", "model_bisnis_last", "model_bisnis_id_last"]],
        on="pid",
        how="left",
    )

    # Simpan nilai asli
    df_final["model_bisnis_asli"] = df_final["model_bisnis"]
    df_final["model_bisnis_id_asli"] = df_final["model_bisnis_id"]

    # Replace dengan nilai terakhir
    df_final["model_bisnis"] = df_final["model_bisnis_last"]
    df_final["model_bisnis_id"] = df_final["model_bisnis_id_last"]

    # 24d: Hitung perubahan
    changes_model = (df_final["model_bisnis_asli"] != df_final["model_bisnis"]).sum()
    changes_id = (df_final["model_bisnis_id_asli"] != df_final["model_bisnis_id"]).sum()

    print(f"\n📊 PERUBAHAN SETELAH BACKFILL:")
    print(
        f"  - Model_bisnis berubah: {changes_model} baris ({changes_model/len(df_final)*100:.1f}%)"
    )
    print(
        f"  - Model_bisnis_id berubah: {changes_id} baris ({changes_id/len(df_final)*100:.1f}%)"
    )

    # 24e: Hapus kolom temporary
    df_final = df_final.drop(columns=["model_bisnis_last", "model_bisnis_id_last"])

    print(
        "\n✅ Backfill selesai! Data terakhir per PID yang digunakan adalah data dengan (tahun, triwulan) tertinggi."
    )

else:
    print("❌ Kolom model_bisnis atau model_bisnis_id tidak ditemukan!")

# ======================================
# Step 25b (atau step terpisah): Cek assignment_id ganda dalam satu (pid, tahun, triwulan)
# ======================================

# ======================================
# CEK ANOMALI: PID, TAHUN, TRIWULAN SAMA TAPI ASSIGNMENT_ID BERBEDA
# ======================================

print("=== CEK ANOMALI: ASSIGNMENT_ID GANDA PER (PID, TAHUN, TRIWULAN) ===")

# Definisikan kolom kunci
group_columns = ["pid", "tahun", "triwulan"]

# Cek apakah kolom yang diperlukan ada
missing_cols = [
    col for col in group_columns + ["assignment_id"] if col not in df_final.columns
]

if missing_cols:
    print(f"❌ Kolom tidak ditemukan: {missing_cols}")
else:
    # 1. Group by pid, tahun, triwulan, hitung unique assignment_id
    grouped = df_final.groupby(group_columns)["assignment_id"].nunique().reset_index()
    grouped.columns = group_columns + ["jumlah_assignment_id"]

    # 2. Filter yang punya lebih dari 1 assignment_id
    anomaly = grouped[grouped["jumlah_assignment_id"] > 1].copy()

    print(f"\n📊 STATISTIK:")
    print(f"  - Total kombinasi (pid, tahun, triwulan): {len(grouped):,}")
    print(
        f"  - Kombinasi dengan NORMAL (1 assignment_id): {len(grouped) - len(anomaly):,}"
    )
    print(f"  - Kombinasi dengan ANOMALI (>1 assignment_id): {len(anomaly):,}")

    if len(anomaly) > 0:
        print(f"\n⚠️ DITEMUKAN {len(anomaly)} KOMBINASI YANG BERMASALAH!")

        # 3. Tampilkan daftar anomaly
        print("\n📋 DAFTAR KOMBINASI BERMASALAH (10 pertama):")
        print(anomaly.head(10).to_string(index=False))

        # 4. Untuk setiap anomaly, tampilkan detail assignment_id yang berbeda
        print("\n📋 DETAIL ASSIGNMENT_ID PER KOMBINASI BERMASALAH (sample 3):")

        for i, (_, row) in enumerate(anomaly.head(3).iterrows()):
            pid = row["pid"]
            tahun = row["tahun"]
            triwulan = row["triwulan"]

            # Ambil data untuk kombinasi ini
            detail = df_final[
                (df_final["pid"] == pid)
                & (df_final["tahun"] == tahun)
                & (df_final["triwulan"] == triwulan)
            ]

            print(f"\n{'='*70}")
            print(f"ANOMALI #{i+1}")
            print(f"{'='*70}")
            print(f"  PID: {pid}")
            print(f"  Tahun: {tahun}")
            print(f"  Triwulan: {triwulan}")
            print(f"  Jumlah assignment_id unik: {row['jumlah_assignment_id']}")
            print(f"\n  DAFTAR ASSIGNMENT_ID DAN DATA TERKAIT:")

            # Tampilkan assignment_id dan beberapa kolom penting
            show_cols = ["assignment_id", "model_bisnis", "model_bisnis_id"]
            if "B3AR1Stotal" in detail.columns:
                show_cols.append("B3AR1Stotal")
            if "is_exist_lla_nonlla" in detail.columns:
                show_cols.append("is_exist_lla_nonlla")

            print(detail[show_cols].to_string(index=False))

        # 5. Export anomaly ke CSV
        output_file = os.path.join(OUTPUT_FOLDER, "anomaly_pid_tahun_triwulan.csv")
        anomaly.to_csv(output_file, sep=";", index=False, encoding="utf-8-sig")
        print(f"\n💾 Daftar kombinasi bermasalah disimpan ke: {output_file}")

        # 6. Export detail semua baris yang bermasalah
        anomaly_keys = anomaly[group_columns].copy()
        df_anomaly_full = df_final.merge(anomaly_keys, on=group_columns, how="inner")
        detail_file = os.path.join(OUTPUT_FOLDER, "anomaly_full_detail.csv")
        df_anomaly_full.to_csv(detail_file, sep=";", index=False, encoding="utf-8-sig")
        print(f"💾 Detail lengkap semua baris bermasalah disimpan ke: {detail_file}")

        # 7. Tampilkan rekomendasi
        print("\n💡 REKOMENDASI:")
        print(
            "  - Ini indikasi data tidak konsisten: satu perusahaan (pid) di triwulan yang sama"
        )
        print("    memiliki lebih dari satu assignment_id.")
        print("  - Perlu investigasi lebih lanjut dari sumber data.")
        print(
            "  - Opsi cleaning: pilih salah satu assignment_id berdasarkan kriteria tertentu"
        )
        print(
            "    (misal: pilih yang memiliki nilai total terbesar, atau pilih yang terakhir)"
        )

        # 8. Opsi: Tampilkan statistik assignment_id apa saja yang bentrok
        print("\n📊 STATISTIK ASSIGNMENT_ID YANG BENTROK:")
        assignment_stats = (
            df_anomaly_full.groupby("assignment_id").size().sort_values(ascending=False)
        )
        print(assignment_stats.head(10).to_string())

    else:
        print(
            "\n✅ TIDAK ADA ANOMALI! Setiap kombinasi (pid, tahun, triwulan) hanya memiliki 1 assignment_id."
        )

# ======================================
# Step 26: Cleaning Anomali (pid, tahun, triwulan) dengan date_modified terbaru
# ======================================

print(
    "=== STEP 26: CLEANING ANOMALI - PERTAHANKAN DATA DENGAN DATE_MODIFIED TERBARU ==="
)

# Definisikan kolom kunci
group_columns = ["pid", "tahun", "triwulan"]

# Cek apakah kolom date_modified ada
if "date_modified" not in df_final.columns:
    print("❌ Kolom 'date_modified' tidak ditemukan!")
    print(f"Kolom yang tersedia: {df_final.columns.tolist()}")

    # Coba cari kolom yang mirip dengan date_modified
    similar_cols = [
        col
        for col in df_final.columns
        if "date" in col.lower() or "modified" in col.lower() or "update" in col.lower()
    ]
    if similar_cols:
        print(f"\n💡 Kolom yang mungkin mirip: {similar_cols}")
        print("Silakan sesuaikan nama kolom yang benar.")
else:

    # 26a: Identifikasi kombinasi yang bermasalah (punya >1 assignment_id)
    grouped = df_final.groupby(group_columns)["assignment_id"].nunique().reset_index()
    problematic_groups = grouped[grouped["assignment_id"] > 1][group_columns].copy()

    print(f"\n📊 IDENTIFIKASI KOMBINASI BERMASALAH:")
    print(f"  - Total kombinasi (pid, tahun, triwulan): {len(grouped):,}")
    print(f"  - Kombinasi BERMASALAH (>1 assignment_id): {len(problematic_groups):,}")

    if len(problematic_groups) == 0:
        print("\n✅ TIDAK ADA KOMBINASI BERMASALAH! Tidak perlu cleaning.")
    else:
        print(f"\n⚠️ Ditemukan {len(problematic_groups)} kombinasi bermasalah!")

        # 26b: Tampilkan sample kombinasi bermasalah
        print("\n📋 SAMPLE KOMBINASI BERMASALAH (10 pertama):")
        print(problematic_groups.head(10).to_string(index=False))

        # 26c: Simpan data sebelum cleaning untuk backup
        df_before_clean = df_final.copy()
        print(f"\n💾 Backup data sebelum cleaning disimpan ke memory (df_before_clean)")

        # 26d: Untuk setiap kombinasi bermasalah, pilih baris dengan date_modified terbaru
        rows_to_keep = []
        rows_to_remove = []

        for _, group_key in problematic_groups.iterrows():
            pid = group_key["pid"]
            tahun = group_key["tahun"]
            triwulan = group_key["triwulan"]

            # Ambil semua baris untuk kombinasi ini
            mask = (
                (df_final["pid"] == pid)
                & (df_final["tahun"] == tahun)
                & (df_final["triwulan"] == triwulan)
            )
            group_data = df_final[mask].copy()

            # Pastikan date_modified dalam format datetime
            if group_data["date_modified"].dtype == "object":
                group_data["date_modified"] = pd.to_datetime(
                    group_data["date_modified"], errors="coerce"
                )

            # Cari baris dengan date_modified terbaru
            latest_idx = group_data["date_modified"].idxmax()
            latest_row = group_data.loc[latest_idx]

            # Baris yang dipertahankan
            rows_to_keep.append(latest_idx)

            # Baris yang akan dihapus (selain yang terbaru)
            other_indices = group_data.index[group_data.index != latest_idx].tolist()
            rows_to_remove.extend(other_indices)

        print(f"\n📊 HASIL SELEKSI:")
        print(
            f"  - Baris yang DIPERTAHANKAN (date_modified terbaru): {len(rows_to_keep)}"
        )
        print(f"  - Baris yang akan DIHAPUS: {len(rows_to_remove)}")

        # 26e: Tampilkan sample perbandingan (sebelum vs sesudah dipilih)
        print("\n📋 SAMPLE PERBANDINGAN (3 kombinasi pertama):")
        for i, (_, group_key) in enumerate(problematic_groups.head(3).iterrows()):
            if i >= 3:
                break
            pid = group_key["pid"]
            tahun = group_key["tahun"]
            triwulan = group_key["triwulan"]

            mask = (
                (df_final["pid"] == pid)
                & (df_final["tahun"] == tahun)
                & (df_final["triwulan"] == triwulan)
            )
            group_data = df_final[mask].copy()

            if group_data["date_modified"].dtype == "object":
                group_data["date_modified"] = pd.to_datetime(
                    group_data["date_modified"], errors="coerce"
                )

            print(f"\n{'='*60}")
            print(f"KOMBINASI #{i+1}: PID={pid}, Tahun={tahun}, Triwulan={triwulan}")
            print(f"{'='*60}")
            print(
                group_data[
                    ["assignment_id", "date_modified", "model_bisnis"]
                ].to_string(index=False)
            )

            # Tampilkan yang dipilih
            latest = group_data.loc[group_data["date_modified"].idxmax()]
            print(
                f"\n✅ YANG DIPERTAHANKAN: assignment_id={latest['assignment_id']}, date_modified={latest['date_modified']}"
            )

        # 26f: Hapus baris yang tidak diinginkan
        df_final = df_final.drop(index=rows_to_remove).reset_index(drop=True)

        # 26g: Verifikasi hasil cleaning
        print("\n=== VERIFIKASI HASIL CLEANING ===")

        # Cek apakah masih ada kombinasi bermasalah
        grouped_after = (
            df_final.groupby(group_columns)["assignment_id"].nunique().reset_index()
        )
        problematic_after = grouped_after[grouped_after["assignment_id"] > 1]

        print(f"\n📊 SETELAH CLEANING:")
        print(f"  - Total baris sebelum: {len(df_before_clean):,}")
        print(f"  - Total baris setelah: {len(df_final):,}")
        print(f"  - Baris yang dihapus: {len(df_before_clean) - len(df_final):,}")
        print(f"  - Kombinasi bermasalah yang tersisa: {len(problematic_after)}")

        if len(problematic_after) == 0:
            print("\n✅ CLEANING SUKSES! Semua anomali telah diatasi.")
        else:
            print(f"\n⚠️ Masih ada {len(problematic_after)} kombinasi bermasalah!")
            print(problematic_after.head().to_string(index=False))

        # 26h: Export log perubahan
        log_file = os.path.join(OUTPUT_FOLDER, "cleaning_anomaly_log.csv")
        log_data = []
        for idx in rows_to_remove:
            row = df_before_clean.loc[idx]
            log_data.append(
                {
                    "pid": row["pid"],
                    "tahun": row["tahun"],
                    "triwulan": row["triwulan"],
                    "assignment_id_removed": row["assignment_id"],
                    "date_modified_removed": row["date_modified"],
                }
            )

        if log_data:
            df_log = pd.DataFrame(log_data)
            df_log.to_csv(log_file, sep=";", index=False, encoding="utf-8-sig")
            print(f"\n💾 Log baris yang dihapus disimpan ke: {log_file}")

# EXPORT KE CSV
df_final.to_csv(
    os.path.join(OUTPUT_FOLDER, "df_final_clean.csv"),
    sep=";",
    index=False,
    encoding="utf-8-sig",
)
print("✅ File CSV telah disimpan: df_final_clean.csv")

# ======================================
# CEK DUPLIKAT BERDASARKAN PID, TAHUN, TRIWULAN, ASSIGNMENT_ID
# ======================================

print("=== CEK DUPLIKAT DATA ===")

# Definisikan kolom kunci untuk cek duplikat
key_columns = ["pid", "tahun", "triwulan", "assignment_id"]

# 1. Cek apakah kolom-kolom kunci ada
missing_keys = [col for col in key_columns if col not in df_final.columns]

if missing_keys:
    print(f"❌ Kolom kunci tidak ditemukan: {missing_keys}")
    print(f"Kolom yang tersedia: {df_final.columns.tolist()}")
else:
    # 2. Cek duplikat berdasarkan key_columns
    duplicates_mask = df_final.duplicated(subset=key_columns, keep=False)
    df_duplicates = df_final[duplicates_mask].copy()

    # 3. Hitung statistik
    total_duplicate_rows = len(df_duplicates)
    duplicate_groups = (
        df_duplicates.groupby(key_columns).size().reset_index(name="count")
    )
    num_duplicate_groups = len(duplicate_groups)

    print(f"\n📊 STATISTIK DUPLIKAT:")
    print(f"  - Total baris dalam dataframe: {len(df_final):,}")
    print(f"  - Baris yang terindikasi duplikat: {total_duplicate_rows:,}")
    print(f"  - Jumlah grup duplikat (kombinasi yang sama): {num_duplicate_groups}")

    if num_duplicate_groups > 0:
        print(f"\n⚠️ DITEMUKAN {num_duplicate_groups} KOMBINASI DUPLIKAT!")

        # 4. Tampilkan grup duplikat dengan jumlahnya
        print("\n📋 DAFTAR GRUP DUPLIKAT (10 grup teratas):")
        print(
            duplicate_groups.sort_values("count", ascending=False)
            .head(10)
            .to_string(index=False)
        )

        # 5. Tampilkan detail baris duplikat (sample)
        print("\n📋 DETAIL BARIS DUPLIKAT (20 baris pertama):")
        cols_to_show = (
            key_columns
            + ["model_bisnis"]
            + [
                col
                for col in ["B3AR1Stotal", "B4DR1Stotal"]
                if col in df_duplicates.columns
            ]
        )
        print(df_duplicates[cols_to_show].head(20).to_string(index=False))

        # 6. Untuk setiap grup duplikat, tampilkan semua barisnya (sample 3 grup)
        print("\n📋 DETAIL LENGKAP PER GRUP DUPLIKAT (3 grup pertama):")
        for i, (idx, group) in enumerate(df_duplicates.groupby(key_columns)):
            if i >= 3:
                break
            print(f"\n--- GRUP DUPLIKAT {i+1} ---")
            print(f"  PID: {group['pid'].iloc[0]}")
            print(f"  Tahun: {group['tahun'].iloc[0]}")
            print(f"  Triwulan: {group['triwulan'].iloc[0]}")
            print(f"  Assignment ID: {group['assignment_id'].iloc[0]}")
            print(f"  Jumlah duplikat: {len(group)} baris")
            print(f"\n  Data:")
            print(
                group[
                    ["pid", "tahun", "triwulan", "assignment_id", "model_bisnis"]
                    + (["B3AR1Stotal"] if "B3AR1Stotal" in group.columns else [])
                ].to_string(index=False)
            )

        # 7. Export duplikat ke CSV
        output_file = os.path.join(OUTPUT_FOLDER, "duplicate_records.csv")
        df_duplicates.to_csv(output_file, sep=";", index=False, encoding="utf-8-sig")
        print(f"\n💾 File duplikat disimpan ke: {output_file}")

        # 8. Export grup duplikat (ringkasan)
        summary_file = os.path.join(OUTPUT_FOLDER, "duplicate_groups_summary.csv")
        duplicate_groups.to_csv(
            summary_file, sep=";", index=False, encoding="utf-8-sig"
        )
        print(f"💾 Ringkasan grup duplikat disimpan ke: {summary_file}")

    else:
        print("\n✅ TIDAK ADA DUPLIKAT! Data sudah bersih.")


# ======================================
# Step 25: Hapus Duplikat Berdasarkan pid, tahun, triwulan, assignment_id
# ======================================

print("=== STEP 25: MENGHAPUS DUPLIKAT ===")

# Definisikan kolom kunci
key_columns = ["pid", "tahun", "triwulan", "assignment_id"]

# Cek apakah kolom kunci ada
missing_keys = [col for col in key_columns if col not in df_final.columns]

if missing_keys:
    print(f"❌ Kolom kunci tidak ditemukan: {missing_keys}")
else:
    # 25a: Catat jumlah sebelum hapus duplikat
    before_count = len(df_final)
    print(f"\n📊 SEBELUM HAPUS DUPLIKAT:")
    print(f"  - Total baris: {before_count:,}")

    # 25b: Cek berapa banyak duplikat yang akan dihapus
    duplicate_count = df_final.duplicated(subset=key_columns, keep=False).sum()
    print(f"  - Baris yang terindikasi duplikat: {duplicate_count:,}")

    # 25c: Hapus duplikat
    # keep='last' → mempertahankan data yang TERAKHIR muncul (berdasarkan urutan dataframe)
    # keep='first' → mempertahankan data yang PERTAMA muncul
    # keep=False → hapus semua duplikat (termasuk yang pertama)

    df_final = df_final.drop_duplicates(subset=key_columns, keep="last")

    # 25d: Catat jumlah setelah hapus duplikat
    after_count = len(df_final)
    removed_count = before_count - after_count

    print(f"\n📊 SETELAH HAPUS DUPLIKAT:")
    print(f"  - Total baris: {after_count:,}")
    print(f"  - Baris yang dihapus: {removed_count:,}")

    # 25e: Verifikasi tidak ada duplikat tersisa
    remaining_duplicates = df_final.duplicated(subset=key_columns).sum()
    if remaining_duplicates == 0:
        print(f"\n✅ BERHASIL! Tidak ada duplikat tersisa.")
    else:
        print(
            f"\n⚠️ Masih ada {remaining_duplicates} baris duplikat, perlu dicek ulang."
        )

    print("\n💡 INFORMASI:")
    print("  - keep='last' → Mempertahankan data TERAKHIR (urutan kemunculan)")
    print("  - Jika ingin mempertahankan data PERTAMA, gunakan keep='first'")

# EXPORT KE CSV
df_final.to_csv(
    os.path.join(OUTPUT_FOLDER, "df_final_clean_count.csv"),
    sep=";",
    index=False,
    encoding="utf-8-sig",
)
print("✅ File CSV telah disimpan: df_final_clean_count.csv")
