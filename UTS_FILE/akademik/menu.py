"""Modul menu: antarmuka interaktif bergaya tab/daftar menu (dipakai bila program dijalankan tanpa argumen)."""
from . import analyzer, cli, exporter, loader

FILE_AWAL = "data/mahasiswa.csv"
TAB = [("1", "Rekap"), ("2", "Cari"), ("3", "Filter"), ("4", "Bersihkan"), ("5", "Ganti File"), ("0", "Keluar")]


def tanya(pesan, default=""):
    """Baca input pengguna. Return None bila input habis (EOF)."""
    try:
        jawab = input(pesan).strip()
    except EOFError:
        return None
    return jawab or default


def cetak_tab(status, aktif):
    """Tampilkan baris 'tab' menu; tab yang sedang dipilih diberi kurung siku."""
    tab = " ".join(f"[{k}.{n}]" if k == aktif else f" {k}.{n} " for k, n in TAB)
    print("\n" + "=" * 72)
    print(tab)
    print(f"File aktif: {status['file']} ({len(status['data'])} mahasiswa)")
    print("=" * 72)


def muat(path):
    """Muat file lewat pipeline cli.muat_data. Return list data, atau None bila gagal."""
    try:
        data, laporan = cli.muat_data(path)
    except FileNotFoundError as err:
        print(f"[ERROR] {err}")
        return None
    except loader.DataError as err:
        print(f"[ERROR] Data bermasalah: {err}")
        return None
    cli.cetak_laporan(laporan)
    return data


def tawarkan_simpan(hasil):
    """Tanya apakah hasil ingin disimpan ke file CSV/JSON."""
    if not hasil:
        return
    path = tanya("Simpan hasil? Ketik nama file .csv/.json (Enter = lewati): ")
    if not path:
        return
    try:
        exporter.simpan(hasil, path)
        print(f"[OK] Hasil disimpan ke {path}")
    except (PermissionError, ValueError) as err:
        print(f"[ERROR] Gagal menyimpan: {err}")


def baca_ipk():
    """Baca IPK minimum dari pengguna. Return float, atau None bila input salah."""
    teks = (tanya("IPK minimum 0-4 (Enter = 0): ", "0") or "0").replace(",", ".")
    try:
        nilai = float(teks)
    except ValueError:
        print("[ERROR] IPK harus berupa angka")
        return None
    if not 0.0 <= nilai <= 4.0:
        print("[ERROR] IPK harus di antara 0 dan 4")
        return None
    return nilai


def menu_rekap(status):
    hasil = analyzer.rekap_per_prodi(status["data"])
    cli.cetak_rekap(hasil)
    tawarkan_simpan(hasil)


def menu_cari(status):
    kata = tanya("Kata kunci (nama atau NIM): ")
    if not kata:
        print("[ERROR] Kata kunci tidak boleh kosong")
        return
    hasil = analyzer.cari(status["data"], kata)
    cli.cetak_tabel(hasil)
    tawarkan_simpan(hasil)


def menu_filter(status):
    print("Prodi tersedia:", ", ".join(analyzer.daftar_prodi(status["data"])) or "-")
    prodi = tanya("Nama prodi (Enter = semua prodi): ") or None
    min_ipk = baca_ipk()
    if min_ipk is None:
        return
    hasil = analyzer.filter_data(status["data"], prodi, min_ipk)
    cli.cetak_tabel(hasil)
    tawarkan_simpan(hasil)


def menu_bersihkan(status):
    print(f"[INFO] Data bersih (tanpa duplikat & data tidak valid): {len(status['data'])} baris")
    tawarkan_simpan(status["data"])


def menu_ganti_file(status):
    path = tanya("Path file .csv/.json: ")
    if not path:
        print("[ERROR] Path tidak boleh kosong")
        return
    data = muat(path)
    if data is not None: 
        status["file"], status["data"] = path, data


AKSI = {"1": menu_rekap, "2": menu_cari, "3": menu_filter, "4": menu_bersihkan, "5": menu_ganti_file}


def _loop():
    print("=== Aplikasi Pengolah Data Mahasiswa ===")
    status = {"file": FILE_AWAL, "data": muat(FILE_AWAL) or []}
    if not status["data"]:
        print("Gunakan tab 5 (Ganti File) untuk memilih file data.")
    aktif = "1"
    while True:
        cetak_tab(status, aktif)
        pilihan = tanya("Pilih tab (angka): ")
        if pilihan is None or pilihan == "0":
            break
        if pilihan not in AKSI:
            print("[ERROR] Pilihan tidak dikenal, masukkan angka 0-5")
            continue
        aktif = pilihan
        cetak_tab(status, aktif)
        AKSI[pilihan](status)


def main():
    """Titik masuk mode menu. Return 0."""
    try:
        _loop()
    except KeyboardInterrupt:
        print()
    print("Sampai jumpa!")
    return 0
