# 1.Meminta login jika belum memiliki sesi pengguna
# 2.Memilih buku yang ingin dipinjam.
# 3.Memeriksa ketersediaan buku
# 4.Mencatat Tanggal peminjaman & jatuh tempo
# 5.Pengembalian buku
# 6.Memperpanjang masa peminjaman
# 7.Denda keterlambatan & kehilangan

from datetime import datetime, timedelta

LAMA_PINJAM = 7
LAMA_PERPANJANG = 7
MAKS_PERPANJANG = 2
DENDA_PER_HARI = 1000

class Peminjaman:
    def __init__(self, koleksi, pengguna_aktif=None, fungsi_login=None):
        self.koleksi = koleksi
        self.pengguna_aktif = pengguna_aktif
        self.fungsi_login = fungsi_login
        self.log_peminjaman = {}

    # Fitur 1 
    def __pastikan_login(self):
        if self.pengguna_aktif is None:
            print("Anda belum login. Silakan login terlebih dahulu.")
            if self.fungsi_login is not None:
                self.pengguna_aktif = self.fungsi_login()
        return self.pengguna_aktif is not None

    def __input_tanggal(self, teks):
        input_tgl = input(f"{teks} (YYYY-MM-DD) [Enter untuk Hari Ini]: ")
        if input_tgl.strip() == "":
            return datetime.now()
        try:
            return datetime.strptime(input_tgl, "%Y-%m-%d")
        except ValueError:
            print("Format tanggal salah!")
            return None

    # Fitur 2, 3, 4
    def peminjaman(self, item_cari=None):
        if not self.__pastikan_login():
            return

        kode = input("Masukan Kode: ")

        for item in self.koleksi:
            if item.kode == kode:
                if type(item).__name__ == "Majalah":
                    print("Majalah hanya boleh dibaca di Perpustakaan")
                    return
                if item.stok != "tersedia":
                    print(f"Tidak tersedia, status: {item.stok}")
                    return

                tgl_pinjam = self.__input_tanggal("Masukan Tanggal Pinjam")
                if tgl_pinjam is None:
                    print("Peminjaman dibatalkan.")
                    return

                jatuh_tempo = tgl_pinjam + timedelta(days=LAMA_PINJAM)
                self.log_peminjaman[kode] = {
                    "pengguna": self.pengguna_aktif.nama,
                    "tgl_pinjam": tgl_pinjam,
                    "jatuh_tempo": jatuh_tempo,
                    "perpanjang": 0
                }

                item.stok = "Dipinjam"
                print("Peminjaman berhasil")
                print(f"Peminjam      : {self.pengguna_aktif.nama}")
                print(f"Judul         : {item.judul}")
                print(f"Tgl Pinjam    : {tgl_pinjam.strftime('%Y-%m-%d')}")
                print(f"Batas Kembali : {jatuh_tempo.strftime('%Y-%m-%d')} (Maksimal 1 minggu)")
                return

        print("Kode tidak ditemukan")

    # Fitur 6
    def perpanjang(self):
        if not self.__pastikan_login():
            return

        kode = input("Masukan kode yang ingin diperpanjang: ")

        for item in self.koleksi:
            if item.kode == kode:
                if item.stok != "Dipinjam":
                    print("Koleksi ini sedang tidak dipinjam!")
                    return

                data = self.log_peminjaman[kode]
                if data["pengguna"] != self.pengguna_aktif.nama:
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
                return

        print("kode tidak ditemukan")

    # Fitur 5 & 7
    def kembalikan(self, item_cari=None):
        if not self.__pastikan_login():
            return

        kode = input("Masukan kode: ")

        for item in self.koleksi:
            if item.kode == kode:
                if type(item).__name__ == "Majalah":
                    print("Majalah tidak bisa dipinjam, jadi tidak perlu dikembalikan")
                    return
                if item.stok != "Dipinjam":
                    print("koleksi masih berada di perpustakaan / belum dipinjam")
                    return

                data = self.log_peminjaman[kode]
                if data["pengguna"] != self.pengguna_aktif.nama:
                    print("Koleksi ini dipinjam oleh pengguna lain!")
                    return

                status_kondisi = input("Apakah koleksi hilang? (y/n): ").lower()
                if status_kondisi == 'y':
                    print(f"Koleksi hilang. Wajib ganti rugi sesuai harga buku: Rp {item.harga:,}")
                    item.stok = "Hilang"
                    del self.log_peminjaman[kode]
                    return

                tgl_kembali = self.__input_tanggal("Masukan Tanggal Pengembalian")
                if tgl_kembali is None:
                    return

                denda = 0
                if tgl_kembali > data["jatuh_tempo"]:
                    hari_telat = (tgl_kembali - data["jatuh_tempo"]).days
                    denda = hari_telat * DENDA_PER_HARI
                    print(f"Terlambat {hari_telat} hari. Denda keterlambatan: Rp {denda:,}")

                item.stok = "tersedia"
                del self.log_peminjaman[kode]

                print(f"Judul  : {item.judul} berhasil dikembalikan")
                return

        print("kode tidak ditemukan")