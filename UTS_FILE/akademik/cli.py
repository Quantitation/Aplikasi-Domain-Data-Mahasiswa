"""Modul cli: antarmuka command line, menghubungkan loader -> validator -> analyzer -> exporter."""
import argparse

from . import analyzer, exporter, loader, validator


def muat_data(path):
    """Baca + validasi + hapus duplikat. Return (data_unik, laporan dict)."""
    mentah = loader.baca_file(path)
    valid, error = validator.validasi_semua(mentah)
    unik, duplikat = analyzer.hapus_duplikat(valid)
    laporan = {"dibaca": len(mentah), "valid": len(valid), "unik": len(unik),
               "duplikat": len(duplikat), "error": error}
    return unik, laporan


def cetak_laporan(laporan):
    print(f"[INFO] Dibaca: {laporan['dibaca']} | Valid: {laporan['valid']} | "
          f"Duplikat dibuang: {laporan['duplikat']} | Dipakai: {laporan['unik']}")
    for pesan in laporan["error"]:
        print(f"[PERINGATAN] {pesan}")


def cetak_tabel(data):
    if not data:
        print("(Tidak ada data yang cocok)")
        return
    print(f"{'NIM':<9}{'Nama':<18}{'Prodi':<20}{'Smt':<5}{'IPK':<6}Predikat")
    print("-" * 72)
    for m in analyzer.tambah_predikat(data):
        print(f"{m['nim']:<9}{m['nama']:<18}{m['prodi']:<20}{m['semester']:<5}"
              f"{m['ipk']:<6.2f}{m['predikat']}")


def cetak_rekap(rekap):
    if not rekap:
        print("(Tidak ada data untuk direkap)")
        return
    print(f"{'Prodi':<20}{'Jumlah':<8}{'Rata IPK':<10}{'Max':<6}Min")
    print("-" * 50)
    for prodi, r in sorted(rekap.items()):
        print(f"{prodi:<20}{r['jumlah']:<8}{r['rata_ipk']:<10.2f}{r['tertinggi']:<6.2f}{r['terendah']:.2f}")


def buat_parser():
    parser = argparse.ArgumentParser(description="Pengolah data mahasiswa (CSV/JSON)")
    sub = parser.add_subparsers(dest="perintah", required=True)

    def tambah(nama, bantuan):
        p = sub.add_parser(nama, help=bantuan)
        p.add_argument("file", help="file input .csv atau .json")
        p.add_argument("--simpan", help="simpan hasil ke file .csv/.json")
        return p

    tambah("rekap", "rekap jumlah & rata-rata IPK per prodi")
    tambah("cari", "cari berdasarkan nama/NIM").add_argument("kata_kunci")
    p_filter = tambah("filter", "saring berdasarkan prodi / IPK minimum")
    p_filter.add_argument("--prodi")
    p_filter.add_argument("--min-ipk", type=float, default=0.0)
    tambah("bersihkan", "buang duplikat & data tidak valid")
    return parser


def jalankan(args):
    """Jalankan perintah, kembalikan hasil yang siap ditampilkan/disimpan."""
    data, laporan = muat_data(args.file)
    cetak_laporan(laporan)
    if args.perintah == "rekap":
        hasil = analyzer.rekap_per_prodi(data)
        cetak_rekap(hasil)
    elif args.perintah == "cari":
        hasil = analyzer.cari(data, args.kata_kunci)
        cetak_tabel(hasil)
    elif args.perintah == "filter":
        hasil = analyzer.filter_data(data, args.prodi, args.min_ipk)
        cetak_tabel(hasil)
    else:  # bersihkan
        hasil = data
        print(f"[INFO] Data bersih: {len(hasil)} baris")
    return hasil


def main(argv=None):
    """Titik masuk program. Return 0 bila sukses, 1 bila gagal."""
    args = buat_parser().parse_args(argv)
    try:
        hasil = jalankan(args)
        if args.simpan:
            exporter.simpan(hasil, args.simpan)
            print(f"[OK] Hasil disimpan ke {args.simpan}")
        return 0
    except FileNotFoundError as err:
        print(f"[ERROR] {err}")
    except loader.DataError as err:
        print(f"[ERROR] Data bermasalah: {err}")
    except (PermissionError, ValueError) as err:
        print(f"[ERROR] Gagal menyimpan/memproses: {err}")
    return 1
