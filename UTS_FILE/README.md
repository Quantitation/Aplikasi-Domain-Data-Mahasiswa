# Aplikasi Pengolah Data Mahasiswa (Command Line)
## 1. Tujuan, Pengguna, Format Input dan Output

- Masalah: data mahasiswa di bagian akademik sering tidak rapi (NIM ganda, IPK ditulis "3,72", data kosong), sehingga rekap dilakukan manual.
- Tujuan: merekap dan membersihkan data mahasiswa secara otomatis dan konsisten.
- Target pengguna: staf administrasi akademik dan dosen wali.
- Input: file .csv atau .json dengan kolom nim, nama, prodi, semester, ipk (contoh: data/mahasiswa.csv).
- Output: tabel di terminal, atau file .csv/.json melalui opsi --simpan atau pilihan simpan di menu.

## 2. Fitur Utama

- rekap: jumlah, rata-rata, tertinggi, dan terendah IPK per prodi
- cari: pencarian berdasarkan potongan nama atau NIM
- filter: penyaringan berdasarkan prodi dan IPK minimum
- bersihkan: penghapusan duplikat NIM dan data tidak valid

## 3. Struktur Program

```
uas_mahasiswa/
    main.py              titik masuk (tanpa argumen = menu, dengan argumen = perintah)
    README.md
    requirements.txt
    akademik/            package buatan sendiri
        __init__.py
        cli.py           argparse dan alur program (mode perintah)
        menu.py          menu interaktif bergaya tab (mode menu)
        loader.py        membaca CSV/JSON
        validator.py     validasi dan pembersihan data
        analyzer.py      cari, filter, rekap, hapus duplikat
        exporter.py      menyimpan CSV/JSON
    data/                contoh file input
    output/              contoh hasil output dan log pengujian
    tests/               unit test
```

Alur dependensi: main memanggil cli (mode perintah) atau menu (mode menu).
Module menu memakai fungsi dari cli. Module cli memanggil loader, validator, analyzer, lalu exporter.
Module analyzer dan validator tidak melakukan input/output sehingga mudah diuji.

## 4. Cara Menjalankan

Syarat: Python 3.8 atau lebih baru. Tidak ada dependency tambahan.
Buka terminal, masuk ke folder proyek (cd uas_mahasiswa), lalu pilih salah satu mode.

Mode A - Menu interaktif (paling mudah):

```
python main.py
```

Pilih tab dengan mengetik angka lalu Enter:

```
[1.Rekap]  2.Cari   3.Filter   4.Bersihkan   5.Ganti File   0.Keluar
File aktif: data/mahasiswa.csv (15 mahasiswa)
```

Tab 1 sampai 4 menjalankan fitur dan menawarkan penyimpanan hasil. Tab 5 mengganti file data. Tab 0 untuk keluar.

Mode B - Perintah langsung:

```
python main.py rekap data/mahasiswa.csv
python main.py rekap data/mahasiswa.csv --simpan output/rekap_prodi.json
python main.py cari data/mahasiswa.csv siti
python main.py filter data/mahasiswa.csv --prodi "Teknik Informatika" --min-ipk 3.5 --simpan output/filter_ti.csv
python main.py bersihkan data/mahasiswa_kotor.csv --simpan output/kotor_bersih.json
python main.py rekap data/mahasiswa.json
```

Bantuan: python main.py --help

Menjalankan unit test:

```
python -m unittest discover tests -v
```

Catatan: di Windows bila perintah python tidak dikenali, gunakan py. Di Mac/Linux gunakan python3.

## 5. Library dan Dependency

Seluruhnya Python standard library: argparse, csv, json, pathlib, dan unittest.
Tidak ada library pihak ketiga (requirements.txt tidak berisi paket).

## 6. Penanganan Error

- File tidak ditemukan: muncul pesan [ERROR], program tidak crash.
- File kosong, kolom wajib hilang, JSON rusak, atau format tidak didukung: muncul pesan [ERROR] Data bermasalah.
- Baris tidak valid (NIM bukan angka, IPK di luar 0-4, semester di luar 1-14, field kosong): baris dilewati dan muncul [PERINGATAN] beserta nomor datanya.
- Gagal menyimpan (hasil kosong untuk CSV, ekstensi salah, tidak ada izin tulis): muncul pesan [ERROR] Gagal menyimpan.
- Input menu tidak sesuai (angka tab tidak dikenal, IPK bukan angka, kata kunci kosong): muncul pesan error dan menu ditampilkan kembali.

## 7. Referensi

- Frydenberg, M., & Xu, J. (2019). Easy as Py: A first course in Python with a taste of data analytics. Information Systems Education Journal, 17(4), 4-15. https://isedj.org/2019-17/n4/ISEDJv17n4p4.html
- Xu, J., & Frydenberg, M. (2021). Python programming in an IS curriculum: Perceived relevance and outcomes. Information Systems Education Journal, 19(4), 37-54. https://isedj.org/2021-19/n4/ISEDJv19n4p37.html
- Python Software Foundation. (n.d.). csv - CSV file reading and writing. Diakses 16 November 2026, dari https://docs.python.org/3/library/csv.html
- Python Software Foundation. (n.d.). json - JSON encoder and decoder. Diakses 16 November 2026, dari https://docs.python.org/3/library/json.html
- Python Software Foundation. (n.d.). Errors and exceptions. Diakses 16 November 2026, dari https://docs.python.org/3/tutorial/errors.html
- Python Software Foundation. (n.d.). Data structures. Diakses 16 November 2026, dari https://docs.python.org/3/tutorial/datastructures.html

Daftar lengkap dengan pembahasan ada pada lembar jawaban.

## 8. Pernyataan Bantuan AI

Kerangka kode, data contoh, README dibuat dengan bantuan AI.
