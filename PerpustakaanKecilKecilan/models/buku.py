from enum import Enum


class Kategori(Enum):
    """Jenis koleksi perpustakaan."""

    NOVEL = "Novel"
    JURNAL = "Jurnal"
    KARYA_ILMIAH = "Karya Ilmiah"
    MAJALAH = "Majalah"

    @property
    def label(self):
        return self.value


class Buku:
    """Representasi satu koleksi (buku) di perpustakaan."""

    def __init__(self, id_buku, id_judul, judul, id_penulis, id_penerbit, kategori, harga):
        self._id_buku = id_buku
        self._id_judul = id_judul
        self._judul = judul
        self._id_penulis = id_penulis
        self._id_penerbit = id_penerbit
        self._kategori = kategori
        self._harga = harga          # dalam Rupiah
        self._tersedia = True        # buku baru otomatis tersedia

    # ---------- Properti (hanya baca) ----------

    @property
    def id_buku(self):
        return self._id_buku

    @property
    def id_judul(self):
        return self._id_judul

    @property
    def judul(self):
        return self._judul

    @property
    def id_penulis(self):
        return self._id_penulis

    @property
    def id_penerbit(self):
        return self._id_penerbit

    @property
    def kategori(self):
        return self._kategori

    @property
    def harga(self):
        return self._harga

    @property
    def tersedia(self):
        return self._tersedia

    # ---------- Status ketersediaan ----------

    @property
    def status(self):
        """Teks status untuk ditampilkan ke user."""
        return "Tersedia" if self._tersedia else "Dipinjam"

    @property
    def harga_format(self):
        """Harga dengan format Rupiah, contoh: Rp 85.000"""
        return "Rp " + f"{self._harga:,}".replace(",", ".")

    def pinjam(self):
        """Tandai buku sebagai dipinjam.

        Mengembalikan True jika berhasil, False jika buku sudah dipinjam orang lain.
        """
        if not self._tersedia:
            return False
        self._tersedia = False
        return True

    def kembalikan(self):
        """Tandai buku sebagai tersedia kembali.

        Mengembalikan True jika berhasil, False jika buku memang tidak sedang dipinjam.
        """
        if self._tersedia:
            return False
        self._tersedia = True
        return True

    def __str__(self):
        return (f"[{self._id_buku}] {self._judul} | {self._kategori.label} | "
                f"Penulis: {self._id_penulis} | Penerbit: {self._id_penerbit} | "
                f"{self.harga_format} | {self.status}")