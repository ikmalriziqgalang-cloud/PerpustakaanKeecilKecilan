import io
import unittest
from contextlib import redirect_stdout

from models.buku import Kategori
from models.koleksi_buku import KoleksiBuku
from models.perpustakaan import Perpustakaan, PerpustakaanError


class TestPerpustakaan(unittest.TestCase):
    def setUp(self):
        self.koleksi = KoleksiBuku()
        self.perpus = Perpustakaan("Perpustakaan Kecil", self.koleksi)

    def test_nama_perpustakaan(self):
        self.assertEqual(self.perpus.nama_perpustakaan, "Perpustakaan Kecil")

    def test_nama_read_only(self):
        with self.assertRaises(AttributeError):
            self.perpus.nama_perpustakaan = "Lain"

    # ---- cariBuku ----
    def test_cari_by_judul(self):
        hasil = self.perpus.cariBuku(judul="laskar")
        self.assertEqual([b.id_buku for b in hasil], ["NOV-001"])

    def test_cari_by_judul_tidak_peka_huruf_besar(self):
        self.assertEqual(len(self.perpus.cariBuku(judul="LASKAR PELANGI")), 1)

    def test_cari_by_nama_penulis(self):
        hasil = self.perpus.cariBuku(penulis="andrea")
        self.assertEqual(len(hasil), 3)

    def test_cari_by_id_penulis(self):
        self.assertEqual(len(self.perpus.cariBuku(penulis="P02")), 3)

    def test_cari_judul_atau_penulis(self):
        # judul cocok 1 buku (Bumi Manusia, penulis P02), penulis Andrea cocok 3 buku
        hasil = self.perpus.cariBuku(judul="bumi", penulis="andrea")
        self.assertEqual(len(hasil), 4)

    def test_cari_tidak_ketemu(self):
        self.assertEqual(self.perpus.cariBuku(judul="tidak ada judul ini"), [])

    def test_cari_tanpa_kata_kunci(self):
        with self.assertRaises(PerpustakaanError):
            self.perpus.cariBuku()
        with self.assertRaises(PerpustakaanError):
            self.perpus.cariBuku(judul="   ", penulis="  ")

    # ---- filterKategori ----
    def test_filter_kategori(self):
        hasil = self.perpus.filterKategori(Kategori.MAJALAH)
        self.assertEqual(len(hasil), 3)
        self.assertTrue(all(b.kategori == Kategori.MAJALAH for b in hasil))

    def test_filter_kategori_tidak_valid(self):
        for bad in ("Novel", None, 1):
            with self.assertRaises(PerpustakaanError):
                self.perpus.filterKategori(bad)

    # ---- tampilan ----
    def test_tampilkan_kategori(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.perpus.tampilkanKategori()
        teks = out.getvalue()
        self.assertIn("Novel (10 buku)", teks)
        self.assertIn("Majalah (3 buku)", teks)

    def test_tampilkan_daftar_buku_semua(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.perpus.tampilkanDaftarBuku()
        self.assertIn("Total: 33 buku", out.getvalue())

    def test_tampilkan_daftar_buku_hasil_cari(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.perpus.tampilkanDaftarBuku(self.perpus.cariBuku(judul="edensor"))
        self.assertIn("Total: 1 buku", out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
