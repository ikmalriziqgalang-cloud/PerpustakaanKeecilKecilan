from models.buku import Buku, Kategori

DATA_NOVEL = [
    ("NOV-001", "J001", "Laskar Pelangi",        "P01", "PB01", 89000),
    ("NOV-002", "J002", "Sang Pemimpi",          "P01", "PB01", 85000),
    ("NOV-003", "J003", "Edensor",               "P01", "PB01", 92000),
    ("NOV-004", "J004", "Bumi Manusia",          "P02", "PB02", 110000),
    ("NOV-005", "J005", "Anak Semua Bangsa",     "P02", "PB02", 105000),
    ("NOV-006", "J006", "Jejak Langkah",         "P02", "PB02", 115000),
    ("NOV-007", "J007", "Laut Bercerita",        "P03", "PB03", 98000),
    ("NOV-008", "J008", "Negeri 5 Menara",       "P04", "PB03", 79000),
    ("NOV-009", "J009", "Ranah 3 Warna",         "P04", "PB03", 82000),
    ("NOV-010", "J010", "Ronggeng Dukuh Paruk", "P05", "PB04", 75000),
]

DATA_JURNAL = [
    ("JUR-001", "J011", "Jurnal Sistem Informasi Modern Vol. 1",     "P06", "PB05", 45000),
    ("JUR-002", "J012", "Jurnal Sistem Informasi Modern Vol. 2",     "P06", "PB05", 45000),
    ("JUR-003", "J013", "Jurnal Rekayasa Perangkat Lunak Vol. 1",    "P07", "PB05", 50000),
    ("JUR-004", "J014", "Jurnal Rekayasa Perangkat Lunak Vol. 2",    "P07", "PB05", 50000),
    ("JUR-005", "J015", "Jurnal Kecerdasan Buatan Indonesia Vol. 1", "P08", "PB06", 55000),
    ("JUR-006", "J016", "Jurnal Pendidikan dan Pembelajaran Vol. 1", "P09", "PB06", 40000),
    ("JUR-007", "J017", "Jurnal Ekonomi dan Bisnis Digital Vol. 1",  "P09", "PB06", 42000),
    ("JUR-008", "J018", "Jurnal Ilmu Kesehatan Masyarakat Vol. 1",   "P10", "PB05", 48000),
    ("JUR-009", "J019", "Jurnal Teknik Sipil dan Lingkungan Vol. 1", "P10", "PB05", 47000),
    ("JUR-010", "J020", "Jurnal Bahasa dan Sastra Nusantara Vol. 1", "P08", "PB06", 38000),
]

DATA_KARYA_ILMIAH = [
    ("KIL-001", "J021", "Analisis Sentimen Twitter dengan Naive Bayes",  "P11", "PB07", 30000),
    ("KIL-002", "J022", "Sistem Informasi Perpustakaan Berbasis Web",    "P12", "PB07", 35000),
    ("KIL-003", "J023", "Pengaruh Motivasi Belajar terhadap Prestasi",   "P13", "PB07", 28000),
    ("KIL-004", "J024", "Segmentasi Pelanggan dengan K-Means",           "P11", "PB07", 32000),
    ("KIL-005", "J025", "Efektivitas Pembelajaran Daring Mahasiswa",     "P13", "PB08", 27000),
    ("KIL-006", "J026", "Penerapan IoT pada Pertanian Cerdas",           "P14", "PB08", 38000),
    ("KIL-007", "J027", "Kualitas Air Sungai di Jawa Tengah",            "P15", "PB08", 33000),
    ("KIL-008", "J028", "Media Sosial dan Perilaku Konsumtif Remaja",    "P16", "PB07", 29000),
    ("KIL-009", "J029", "Optimasi Rute Distribusi Algoritma Genetika",   "P14", "PB08", 36000),
    ("KIL-010", "J030", "Aplikasi Mobile Pembelajaran Bahasa Inggris",   "P12", "PB07", 34000),
]

DATA_MAJALAH = [
    ("MAJ-001", "J031", "Majalah Teknologi Terkini Edisi 1", "P17", "PB09", 25000),
    ("MAJ-002", "J032", "Majalah Sains Populer Edisi 1",     "P17", "PB09", 27000),
    ("MAJ-003", "J033", "Majalah Kuliner Nusantara Edisi 1", "P18", "PB09", 30000),
]

# Pemetaan ID penulis -> nama (supaya pencarian by nama penulis bisa jalan)
NAMA_PENULIS = {
    "P01": "Andrea Hirata",
    "P02": "Pramoedya Ananta Toer",
    "P03": "Leila S. Chudori",
    "P04": "A. Fuadi",
    "P05": "Ahmad Tohari",
}

# Dikosongkan: buku yang "sedang dipinjam" harus tercatat lewat class Peminjaman
CONTOH_DIPINJAM = []

FORMAT_BARIS = "{:<8} {:<8} {:<46} {:<10} {:<11} {:<13} {:>11} {:<9}"
GARIS = "-" * 123


class KoleksiBuku:
    """Menyimpan seluruh buku perpustakaan serta menyediakan pencarian dan tampilan daftar."""

    def __init__(self):
        self._daftar_buku = []
        self._isi_data_awal()


    def _isi_data_awal(self):
        for kategori, data in ((Kategori.NOVEL, DATA_NOVEL),
                               (Kategori.JURNAL, DATA_JURNAL),
                               (Kategori.KARYA_ILMIAH, DATA_KARYA_ILMIAH),
                               (Kategori.MAJALAH, DATA_MAJALAH)):
            for id_buku, id_judul, judul, id_penulis, id_penerbit, harga in data:
                self._daftar_buku.append(
                    Buku(id_buku, id_judul, judul, id_penulis, id_penerbit, kategori, harga))

        for id_buku in CONTOH_DIPINJAM:
            self.cari_by_id_buku(id_buku).pinjam()

    def get_nama_penulis(self, id_penulis):
        """Ambil nama penulis dari ID. Jika tidak ada di pemetaan, kembalikan ID-nya."""
        return NAMA_PENULIS.get(id_penulis, id_penulis)

    def cari_by_id_buku(self, id_buku):
        """Cari satu buku berdasarkan ID Buku (unik). Mengembalikan None jika tidak ada."""
        kunci = id_buku.strip().lower()
        for buku in self._daftar_buku:
            if buku.id_buku.lower() == kunci:
                return buku
        return None

    def cari_by_id_judul(self, id_judul):
        """Cari buku berdasarkan ID Judul."""
        kunci = id_judul.strip().lower()
        return [b for b in self._daftar_buku if b.id_judul.lower() == kunci]

    def cari_by_id_penulis(self, id_penulis):
        """Cari semua buku milik satu penulis berdasarkan ID Penulis."""
        kunci = id_penulis.strip().lower()
        return [b for b in self._daftar_buku if b.id_penulis.lower() == kunci]

    def cari_by_id_penerbit(self, id_penerbit):
        """Cari semua buku dari satu penerbit berdasarkan ID Penerbit."""
        kunci = id_penerbit.strip().lower()
        return [b for b in self._daftar_buku if b.id_penerbit.lower() == kunci]

    def cari_by_kategori(self, kategori):
        """Cari semua buku dalam satu kategori (untuk fitur pencarian kategori)."""
        return [b for b in self._daftar_buku if b.kategori == kategori]


    def get_semua_buku(self):
        return list(self._daftar_buku)

    def get_buku_tersedia(self):
        """Hanya buku yang saat ini tersedia untuk dipinjam."""
        return [b for b in self._daftar_buku if b.tersedia]


    def tampilkan(self, daftar):
        """Tampilkan daftar buku dalam bentuk tabel, lengkap dengan status ketersediaan."""
        if not daftar:
            print("Buku tidak ditemukan.")
            return
        print(GARIS)
        print(FORMAT_BARIS.format("ID Buku", "ID Judul", "Judul", "ID Penulis",
                                  "ID Penerbit", "Kategori", "Harga", "Status"))
        print(GARIS)
        for b in daftar:
            print(FORMAT_BARIS.format(b.id_buku, b.id_judul, b.judul, b.id_penulis,
                                      b.id_penerbit, b.kategori.label,
                                      b.harga_format, b.status))
        print(GARIS)
        print(f"Total: {len(daftar)} buku")
