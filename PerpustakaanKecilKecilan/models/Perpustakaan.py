from models.buku import Kategori


class PerpustakaanError(Exception):
    """Kesalahan pada class Perpustakaan."""


class Perpustakaan:
    def __init__(self, nama_perpustakaan, koleksi):
        self._nama_perpustakaan = nama_perpustakaan
        self._koleksi = koleksi          # objek KoleksiBuku (satu sumber data)

    @property
    def nama_perpustakaan(self):
        return self._nama_perpustakaan

    def tampilkanDaftarBuku(self, daftar=None):
        daftar = self._koleksi.get_semua_buku() if daftar is None else daftar
        self._koleksi.tampilkan(daftar)      # sudah berbentuk tabel

    def tampilkanKategori(self):
        print("Kategori buku:")
        for k in Kategori:
            jumlah = len(self._koleksi.cari_by_kategori(k))
            print(f"  - {k.label} ({jumlah} buku)")

    def cariBuku(self, judul="", penulis=""):
        """Cari berdasarkan judul ATAU penulis (tidak peka huruf besar/kecil)."""
        judul, penulis = judul.strip().lower(), penulis.strip().lower()
        if not judul and not penulis:
            raise PerpustakaanError("Isi kata kunci judul atau penulis.")
        hasil = []
        for b in self._koleksi.get_semua_buku():
            nama = self._koleksi.get_nama_penulis(b.id_penulis).lower()
            cocok_judul = judul and judul in b.judul.lower()
            cocok_penulis = penulis and (penulis in nama or penulis == b.id_penulis.lower())
            if cocok_judul or cocok_penulis:
                hasil.append(b)
        return hasil

    def filterKategori(self, kategori):
        if not isinstance(kategori, Kategori):
            raise PerpustakaanError("Kategori tidak valid.")
        return self._koleksi.cari_by_kategori(kategori)
