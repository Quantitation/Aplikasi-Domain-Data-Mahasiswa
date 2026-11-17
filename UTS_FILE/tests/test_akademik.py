"""Uji sederhana (unittest, standard library). Jalankan: python -m unittest discover tests"""
import unittest

from akademik import analyzer, validator


def mhs(nim, prodi, ipk):
    return {"nim": nim, "nama": "X", "prodi": prodi, "semester": 1, "ipk": ipk}


class TestAnalyzer(unittest.TestCase):
    def test_rekap_normal(self):
        hasil = analyzer.rekap_per_prodi([mhs("1", "A", 3.0), mhs("2", "A", 4.0)])
        self.assertEqual(hasil["A"]["rata_ipk"], 3.5)

    def test_rekap_data_kosong(self):  # edge case
        self.assertEqual(analyzer.rekap_per_prodi([]), {})

    def test_hapus_duplikat(self):
        unik, dup = analyzer.hapus_duplikat([mhs("1", "A", 3.0), mhs("1", "A", 3.0)])
        self.assertEqual((len(unik), len(dup)), (1, 1))

    def test_predikat_batas(self):  # edge case nilai batas
        self.assertEqual(analyzer.tentukan_predikat(3.5), "Cum Laude")
        self.assertEqual(analyzer.tentukan_predikat(1.99), "Perlu Pembinaan")


class TestValidator(unittest.TestCase):
    def test_koma_desimal(self):
        baris = {"nim": "1", "nama": "a", "prodi": "b", "semester": "2", "ipk": "3,5"}
        self.assertEqual(validator.bersihkan_baris(baris)["ipk"], 3.5)

    def test_ipk_di_luar_rentang(self):  # edge case
        baris = {"nim": "1", "nama": "a", "prodi": "b", "semester": "2", "ipk": "4.5"}
        with self.assertRaises(ValueError):
            validator.bersihkan_baris(baris)


if __name__ == "__main__":
    unittest.main()
