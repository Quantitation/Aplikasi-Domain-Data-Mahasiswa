"""Modul analyzer: logika pengolahan data (fungsi murni, tanpa input/output)."""


def hapus_duplikat(data):
    """Hapus duplikat berdasarkan NIM memakai set. Return (unik, duplikat)."""
    sudah_ada = set()
    unik, duplikat = [], []
    for mhs in data:
        if mhs["nim"] in sudah_ada:
            duplikat.append(mhs)
        else:
            sudah_ada.add(mhs["nim"])
            unik.append(mhs)
    return unik, duplikat


def cari(data, kata_kunci):
    """Cari mahasiswa berdasarkan potongan nama atau NIM."""
    kunci = kata_kunci.strip().lower()
    return [m for m in data if kunci in m["nama"].lower() or kunci in m["nim"]]


def filter_data(data, prodi=None, min_ipk=0.0):
    """Saring data berdasarkan prodi (opsional) dan IPK minimum."""
    return [
        m for m in data
        if m["ipk"] >= min_ipk and (prodi is None or m["prodi"].lower() == prodi.lower())
    ]


def tentukan_predikat(ipk):
    """Tentukan predikat berdasarkan IPK."""
    if ipk >= 3.5:
        return "Cum Laude"
    elif ipk >= 3.0:
        return "Baik"
    elif ipk >= 2.0:
        return "Cukup"
    return "Perlu Pembinaan"


def tambah_predikat(data):
    """Tambahkan kolom predikat pada setiap mahasiswa."""
    return [{**m, "predikat": tentukan_predikat(m["ipk"])} for m in data]


def daftar_prodi(data):
    """Kumpulan prodi unik (set comprehension), terurut."""
    return sorted({m["prodi"] for m in data})


def rekap_per_prodi(data):
    """Kelompokkan IPK per prodi lalu hitung jumlah, rata-rata, tertinggi, terendah."""
    kelompok = {}
    for m in data:
        kelompok.setdefault(m["prodi"], []).append(m["ipk"])
    return {
        prodi: {
            "jumlah": len(nilai),
            "rata_ipk": round(sum(nilai) / len(nilai), 2),
            "tertinggi": max(nilai),
            "terendah": min(nilai),
        }
        for prodi, nilai in kelompok.items()
    }
