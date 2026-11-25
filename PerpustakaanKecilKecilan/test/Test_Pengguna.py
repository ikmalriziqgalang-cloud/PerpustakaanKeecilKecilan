import unittest
from datetime import datetime, timedelta

from Pengguna import (
    Pengguna, PenggunaError, DataTidakValidError,
    LoginGagalError, AkunTerkunciError, BelumLoginError,
)


class PeminjamanPalsu:
    def __init__(self, id_peminjaman, status_peminjaman):
        self.id_peminjaman = id_peminjaman
        self.status_peminjaman = status_peminjaman


class TestPengguna(unittest.TestCase):
    def setUp(self):
        self.user = Pengguna(1, "Budi", "rahasia123")
        self.t0 = datetime(2026, 11, 24, 10, 0, 0)

    def test_buat_pengguna_valid(self):
        self.assertEqual(self.user.id_pengguna, 1)
        self.assertEqual(self.user.nama, "Budi")
        self.assertFalse(self.user.sedang_login)

    def test_id_tidak_valid(self):
        for bad in (0, -5, "1", None):
            with self.assertRaises(DataTidakValidError):
                Pengguna(bad, "Budi", "rahasia123")

    def test_nama_kosong(self):
        with self.assertRaises(DataTidakValidError):
            Pengguna(1, "   ", "rahasia123")

    def test_password_terlalu_pendek(self):
        with self.assertRaises(DataTidakValidError):
            Pengguna(1, "Budi", "123")

    def test_setter_nama(self):
        self.user.nama = "  Andi "
        self.assertEqual(self.user.nama, "Andi")
        with self.assertRaises(DataTidakValidError):
            self.user.nama = ""

    def test_id_read_only(self):
        with self.assertRaises(AttributeError):
            self.user.id_pengguna = 99

    def test_login_berhasil(self):
        self.assertTrue(self.user.login("rahasia123", self.t0))
        self.assertTrue(self.user.sedang_login)

    def test_login_password_salah(self):
        with self.assertRaises(LoginGagalError):
            self.user.login("salah", self.t0)
        self.assertFalse(self.user.sedang_login)

    def test_tiga_kali_gagal_terkunci(self):
        for _ in range(2):
            with self.assertRaises(LoginGagalError):
                self.user.login("salah", self.t0)
        with self.assertRaises(AkunTerkunciError):
            self.user.login("salah", self.t0)
        with self.assertRaises(AkunTerkunciError):
            self.user.login("rahasia123", self.t0 + timedelta(minutes=30))

    def test_kunci_terbuka_setelah_1_jam(self):
        for _ in range(3):
            with self.assertRaises(PenggunaError):
                self.user.login("salah", self.t0)
        self.assertTrue(self.user.login("rahasia123", self.t0 + timedelta(hours=1, seconds=1)))

    def test_gagal_login_direset_setelah_sukses(self):
        with self.assertRaises(LoginGagalError):
            self.user.login("salah", self.t0)
        self.user.login("rahasia123", self.t0)
        self.user.logout()
        with self.assertRaises(LoginGagalError):
            self.user.login("salah", self.t0)

    def test_logout(self):
        self.user.login("rahasia123", self.t0)
        self.user.logout()
        self.assertFalse(self.user.sedang_login)

    def test_logout_tanpa_login(self):
        with self.assertRaises(BelumLoginError):
            self.user.logout()

    def test_riwayat_butuh_login(self):
        with self.assertRaises(BelumLoginError):
            self.user.lihat_riwayat_peminjaman()
        with self.assertRaises(BelumLoginError):
            self.user.lihat_status_peminjaman()

    def test_riwayat_dan_status(self):
        self.user.login("rahasia123", self.t0)
        self.user.tambah_peminjaman(PeminjamanPalsu(1, "DIKEMBALIKAN"))
        self.user.tambah_peminjaman(PeminjamanPalsu(2, "DIPINJAM"))
        self.user.tambah_peminjaman(PeminjamanPalsu(3, "TERLAMBAT"))

        self.assertEqual(len(self.user.lihat_riwayat_peminjaman()), 3)
        status = self.user.lihat_status_peminjaman()
        self.assertEqual(
            status,
            [{"id": 2, "status": "DIPINJAM"}, {"id": 3, "status": "TERLAMBAT"}],
        )

    def test_riwayat_adalah_salinan(self):
        self.user.login("rahasia123", self.t0)
        self.user.tambah_peminjaman(PeminjamanPalsu(1, "DIPINJAM"))
        self.user.lihat_riwayat_peminjaman().clear()
        self.assertEqual(len(self.user.lihat_riwayat_peminjaman()), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)