# =====================================================================
class Perpustakaan:
    def __init__(self, nama_perpustakaan):
        self._nama_perpustakaan = nama_perpustakaan
        self._daftar_buku = []                     # collection: list objek Buku

    @property
    def nama_perpustakaan(self):
        return self._nama_perpustakaan

    def tambahBuku(self, buku):
        """Dipakai untuk memasukkan data awal (seed data)."""
        if any(b.id_buku == buku.id_buku for b in self._daftar_buku):
            raise PerpustakaanError(f"ID buku {buku.id_buku} sudah ada.")
        self._daftar_buku.append(buku)

    def ambilBuku(self, id_buku):
        for b in self._daftar_buku:
            if b.id_buku == id_buku:
                return b
        raise PerpustakaanError(f"Buku dengan ID {id_buku} tidak ditemukan.")

    def tampilkanDaftarBuku(self, daftar=None):
        daftar = self._daftar_buku if daftar is None else daftar
        if not daftar:
            print("Tidak ada buku yang cocok.")
        for b in daftar:
            print(b.tampilkanDetail())

    def tampilkanKategori(self):
        print("Kategori buku:")
        for k in KategoriBuku:
            jumlah = sum(1 for b in self._daftar_buku if b.kategori == k)
            print(f"  - {k.value} ({jumlah} buku)")

    def cariBuku(self, judul="", penulis=""):
        """Cari berdasarkan judul ATAU penulis (tidak peka huruf besar/kecil)."""
        judul, penulis = judul.strip().lower(), penulis.strip().lower()
        if not judul and not penulis:
            raise PerpustakaanError("Isi kata kunci judul atau penulis.")
        return [b for b in self._daftar_buku
                if (judul and judul in b.judul.lower())
                or (penulis and penulis in b.penulis.lower())]

    def filterKategori(self, kategori):
        if not isinstance(kategori, KategoriBuku):
            raise PerpustakaanError("Kategori tidak valid.")
        return [b for b in self._daftar_buku if b.kategori == kategori]
# =====================================================================