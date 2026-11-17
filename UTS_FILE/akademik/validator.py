"""Modul validator: membersihkan dan memeriksa data mentah (defensive programming)."""


def bersihkan_baris(baris):
    """Validasi satu baris data, kembalikan dict bersih.

    Raises:
        ValueError: bila ada field yang kosong atau di luar rentang.
    """
    nim = str(baris.get("nim") or "").strip()
    nama = str(baris.get("nama") or "").strip().title()
    prodi = str(baris.get("prodi") or "").strip().title()
    if not nim.isdigit():
        raise ValueError(f"NIM harus angka, ditemukan '{nim}'")
    if not nama or not prodi:
        raise ValueError("Nama/prodi tidak boleh kosong")
    try:
        semester = int(baris.get("semester"))
        ipk = float(str(baris.get("ipk")).replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Semester/IPK bukan angka") from None
    if not 1 <= semester <= 14:
        raise ValueError(f"Semester {semester} di luar rentang 1-14")
    if not 0.0 <= ipk <= 4.0:
        raise ValueError(f"IPK {ipk} di luar rentang 0.00-4.00")
    return {"nim": nim, "nama": nama, "prodi": prodi, "semester": semester, "ipk": ipk}


def validasi_semua(data_mentah):
    """Kembalikan (data_valid, daftar_pesan_error)."""
    valid, error = [], []
    for nomor, baris in enumerate(data_mentah, start=1):
        try:
            valid.append(bersihkan_baris(baris))
        except (ValueError, AttributeError) as err:
            error.append(f"Data ke-{nomor}: {err}")
    return valid, error
