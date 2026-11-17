"""Modul exporter: menyimpan hasil ke file CSV/JSON."""
import csv
import json
from pathlib import Path


def simpan(data, path):
    """Simpan list of dict (atau dict) ke file; format ditentukan dari ekstensi."""
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    if file.suffix.lower() == ".json":
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif file.suffix.lower() == ".csv":
        _simpan_csv(data, file)
    else:
        raise ValueError("Output harus berekstensi .csv atau .json")


def _simpan_csv(data, file):
    if isinstance(data, dict):  # rekap: ubah ke list baris
        data = [{"prodi": k, **v} for k, v in data.items()]
    if not data:
        raise ValueError("Tidak ada data untuk disimpan")
    with open(file, "w", newline="", encoding="utf-8") as f:
        penulis = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        penulis.writeheader()
        penulis.writerows(data)
