"""Modul loader: membaca file CSV/JSON menjadi list of dictionary."""
import csv
import json
from pathlib import Path

KOLOM_WAJIB = {"nim", "nama", "prodi", "semester", "ipk"}


class DataError(Exception):
    """Kesalahan format/isi file data (bukan kesalahan program)."""


def baca_file(path):
    """Baca file .csv atau .json, kembalikan list of dict (data mentah).

    Raises:
        FileNotFoundError: file tidak ada.
        DataError: format tidak didukung, file kosong, atau struktur salah.
    """
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    ekstensi = file.suffix.lower()
    if ekstensi == ".csv":
        return _baca_csv(file)
    if ekstensi == ".json":
        return _baca_json(file)
    raise DataError(f"Format '{ekstensi}' tidak didukung (gunakan .csv/.json)")


def _baca_csv(file):
    with open(file, newline="", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        if pembaca.fieldnames is None:
            raise DataError("File CSV kosong (tidak ada header)")
        kurang = KOLOM_WAJIB - set(pembaca.fieldnames)
        if kurang:
            raise DataError(f"Kolom wajib tidak ada: {', '.join(sorted(kurang))}")
        return list(pembaca)


def _baca_json(file):
    with open(file, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as err:
            raise DataError(f"JSON tidak valid: {err}") from err
    if not isinstance(data, list):
        raise DataError("JSON harus berupa list of object")
    return data
