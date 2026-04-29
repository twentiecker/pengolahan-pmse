import pandas as pd
import os
from math import ceil

# =========================
# CONFIG
# =========================
input_file = (
    "output/240426/deskripsi_payment_yang_perlu_ditambahkan.csv"  # file csv sumber
)
output_folder = "payment/hasil_split"  # folder output
rows_per_file = 200  # jumlah baris tiap file

# =========================
# BUAT FOLDER OUTPUT
# =========================
os.makedirs(output_folder, exist_ok=True)

# =========================
# BACA CSV
# =========================
df = pd.read_csv(input_file, sep=";", encoding="utf-8")

total_rows = len(df)
total_files = ceil(total_rows / rows_per_file)

print(f"Total baris : {total_rows}")
print(f"Total file  : {total_files}")

# =========================
# PECAH FILE
# =========================
for i in range(total_files):
    start = i * rows_per_file
    end = start + rows_per_file

    chunk = df.iloc[start:end]

    output_file = os.path.join(output_folder, f"split_{i+1}.csv")

    chunk.to_csv(output_file, index=False)

    print(f"Saved: {output_file} ({len(chunk)} baris)")

print("Selesai bro 🚀")
