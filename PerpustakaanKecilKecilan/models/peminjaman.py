from datetime import datetime, timedelta
from models.buku import Kategori

LAMA_PINJAM = 7
LAMA_PERPANJANG = 7
MAKS_PERPANJANG = 2
DENDA_PER_HARI = 9000


class Peminjaman:
    def __init__(self, koleksi, pengguna_aktif=None, fungsi_login=None):
        self.koleksi = koleksi
        self.pengguna_aktif = pengguna_aktif
        self.fungsi_login = fungsi_login
        self.log_peminjaman = {}
        self._nomor = 0

    # Fitur 1
    def __pastikan_login(self):
        if self.pengguna_aktif is None or not self.pengguna_aktif.sedang_login:
            print("Anda belum login. Silakan login terlebih dahulu.")
            if self.fungsi_login is not None:
                self.pengguna_aktif = self.fungsi_login()
        return self.pengguna_aktif is not None and self.pengguna_aktif.sedang_login

    def __input_tanggal(self, teks):
        input_tgl = input(f"{teks} (YYYY-MM-DD) [Enter untuk Hari Ini]: ")
        if input_tgl.strip() == "":
            return datetime.now()
        try:
            return datetime.strptime(input_tgl.strip(), "%Y-%m-%d")
        except ValueError:
            print("Format tanggal salah!")
            return None

    # Fitur 2, 3, 4
    def peminjaman(self):
        if not self.__pastikan_login():
            return

        kode = input("Masukan Kode Buku: ")
        item = self.koleksi.cari_by_id_buku(kode)
        if item is None:
            print("Kode tidak ditemukan")
            return
        if item.kategori == Kategori.MAJALAH:
            print("Majalah hanya boleh dibaca di Perpustakaan")
            return
        if not item.tersedia:
            print(f"Tidak tersedia, status: {item.status}")
            return

        tgl_pinjam = self.__input_tanggal("Masukan Tanggal Pinjam")
        if tgl_pinjam is None:
            print("Peminjaman dibatalkan.")
            return

        jatuh_tempo = tgl_pinjam + timedelta(days=LAMA_PINJAM)
        self._nomor += 1
        catatan = {
            "id_peminjaman": f"PJM-{self._nomor:03d}",
            "id_buku": item.id_buku,
            "judul": item.judul,
            "id_pengguna": self.pengguna_aktif.id_pengguna,
            "tgl_pinjam": tgl_pinjam,
            "jatuh_tempo": jatuh_tempo,
            "perpanjang": 0,
            "status_peminjaman": "DIPINJAM",
            "denda": 0,
        }
        item.pinjam()
        self.log_peminjaman[item.id_buku] = catatan
        self.pengguna_aktif.tambah_peminjaman(catatan)

        print("Peminjaman berhasil")
        print(f"Peminjam      : {self.pengguna_aktif.nama}")
        print(f"Judul         : {item.judul}")
        print(f"Tgl Pinjam    : {tgl_pinjam.strftime('%Y-%m-%d')}")
        print(f"Batas Kembali : {jatuh_tempo.strftime('%Y-%m-%d')} (Maksimal 1 minggu)")

    # Fitur 6
    def perpanjang(self):
        if not self.__pastikan_login():
            return

        kode = input("Masukan kode yang ingin diperpanjang: ")
        item = self.koleksi.cari_by_id_buku(kode)
        if item is None:
            print("Kode tidak ditemukan")
            return

        data = self.log_peminjaman.get(item.id_buku)
        if data is None:
            print("Koleksi ini sedang tidak dipinjam!")
            return
        if data["id_pengguna"] != self.pengguna_aktif.id_pengguna:
            print("Koleksi ini dipinjam oleh pengguna lain!")
            return

        tgl_sekarang = self.__input_tanggal("Masukan Tanggal Hari Ini")
        if tgl_sekarang is None:
            return
        if tgl_sekarang > data["jatuh_tempo"]:
            hari = (tgl_sekarang - data["jatuh_tempo"]).days
            print(f"Sudah lewat jatuh tempo {hari} hari. Tidak bisa diperpanjang, silakan kembalikan.")
            return
        if data["perpanjang"] >= MAKS_PERPANJANG:
            print(f"Batas perpanjangan ({MAKS_PERPANJANG}x) sudah tercapai!")
            return

        data["jatuh_tempo"] += timedelta(days=LAMA_PERPANJANG)
        data["perpanjang"] += 1
        print(f"Perpanjangan berhasil ({data['perpanjang']}/{MAKS_PERPANJANG}). "
              f"Batas baru pengembalian: {data['jatuh_tempo'].strftime('%Y-%m-%d')}")

    # Fitur 5 & 7
    def kembalikan(self):
        if not self.__pastikan_login():
            return

        kode = input("Masukan kode: ")
        item = self.koleksi.cari_by_id_buku(kode)
        if item is None:
            print("Kode tidak ditemukan")
            return
        if item.kategori == Kategori.MAJALAH:
            print("Majalah tidak bisa dipinjam, jadi tidak perlu dikembalikan")
            return

        data = self.log_peminjaman.get(item.id_buku)
        if data is None:
            print("Koleksi masih berada di perpustakaan / belum dipinjam")
            return
        if data["id_pengguna"] != self.pengguna_aktif.id_pengguna:
            print("Koleksi ini dipinjam oleh pengguna lain!")
            return

        hilang = input("Apakah koleksi hilang? (y/n): ").strip().lower()
        if hilang == "y":
            data["denda"] = item.harga
            data["status_peminjaman"] = "HILANG"
            del self.log_peminjaman[item.id_buku]
            # buku sengaja TIDAK dikembalikan ke status tersedia karena hilang
            print(f"Koleksi hilang. Wajib ganti rugi sesuai harga buku: {item.harga_format}")
            return

        tgl_kembali = self.__input_tanggal("Masukan Tanggal Pengembalian")
        if tgl_kembali is None:
            return

        if tgl_kembali > data["jatuh_tempo"]:
            hari_telat = (tgl_kembali - data["jatuh_tempo"]).days
            data["denda"] = hari_telat * DENDA_PER_HARI
            print(f"Terlambat {hari_telat} hari. Denda keterlambatan: Rp {data['denda']:,}")

        item.kembalikan()
        data["status_peminjaman"] = "DIKEMBALIKAN"
        del self.log_peminjaman[item.id_buku]
        print(f"Judul  : {item.judul} berhasil dikembalikan")
