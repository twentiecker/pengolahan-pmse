"""
Modul sederhana untuk mapping COICOP
"""

import pandas as pd

# Data mapping
COICOP_MAP = {
    "1": "01. Food and non-alcoholic beverages",
    "2": "02. Alcoholic beverages, tobacco and narcotics",
    "3": "03. Clothing and footwear",
    "4": "04. Housing, water, electricity, gas and other fuels",
    "5": "05. Furnishings, household equipment and routine household maintenance",
    "6": "06. Health",
    "7": "07. Transport",
    "8": "08. Information and communication",
    "9": "09. Recreation, sport and culture",
    "10": "10. Education services",
    "11.1": "11.1. Food and beverage serving services",
    "11.2": "11.2. Accommodation services",
    "12": "12. Insurance and financial services",
    "13": "13. Personal care, social protection and miscellaneous goods and services",
    "88": "88. Unidentified",
    "99": "99. Non PKRT",
}


def get_coicop(kode):
    """
    Mendapatkan deskripsi COICOP dari kode.

    Args:
        kode: str/int/float - Kode COICOP

    Returns:
        str: Deskripsi COICOP, atau 'Unknown: {kode}' jika tidak ditemukan
    """
    if pd.isna(kode):
        return "Unknown (NaN)"

    kode_str = str(kode).strip()
    return COICOP_MAP.get(kode_str, f"Unknown: {kode}")


def add_coicop_column(df, kolom_kode, nama_kolom_baru="deskripsi_coicop"):
    """
    Menambahkan kolom deskripsi COICOP ke dataframe.

    Args:
        df: DataFrame
        kolom_kode: Nama kolom yang berisi kode COICOP
        nama_kolom_baru: Nama kolom baru untuk hasil mapping

    Returns:
        DataFrame dengan kolom baru
    """
    df_result = df.copy()
    df_result[nama_kolom_baru] = df_result[kolom_kode].apply(get_coicop)
    return df_result
