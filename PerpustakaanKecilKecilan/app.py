from models.buku import Kategori
from models.koleksi_buku import KoleksiBuku
from models.Perpustakaan import Perpustakaan, PerpustakaanError
from models.peminjaman import Peminjaman
from models.Pengguna import Pengguna, PenggunaError

DAFTAR_PENGGUNA = {
    1: Pengguna(1, "Budi", "rahasia123"),
    2: Pengguna(2, "Siti", "passwordsiti"),
}


def login_dari_input():
    """Minta ID dan password, lalu kembalikan objek Pengguna jika berhasil."""
    try:
        id_pengguna = int(input("ID Pengguna: "))
    except ValueError:
        print("ID harus berupa angka.")
        return None
    pengguna = DAFTAR_PENGGUNA.get(id_pengguna)
    if pengguna is None:
        print("Pengguna tidak terdaftar.")
        return None
    try:
        pengguna.login(input("Password: "))
    except PenggunaError as e:
        print(e)
        return None
    print(f"Selamat datang, {pengguna.nama}!")
    return pengguna


def pilih_kategori():
    daftar = list(Kategori)
    for i, k in enumerate(daftar, 1):
        print(f"{i}. {k.label}")
    try:
        nomor = int(input("Pilih nomor kategori: "))
    except ValueError:
        return None
    return daftar[nomor - 1] if 1 <= nomor <= len(daftar) else None


def tampil_data_pengguna(peminjaman, jenis):
    pengguna = peminjaman.pengguna_aktif
    if pengguna is None or not pengguna.sedang_login:
        print("Silakan login dulu (menu 10).")
        return
    data = (pengguna.lihat_riwayat_peminjaman() if jenis == "riwayat"
            else pengguna.lihat_status_peminjaman())
    if not data:
        print("Belum ada data.")
    for d in data:
        print(d)


def main():
    koleksi = KoleksiBuku()
    perpus = Perpustakaan("Perpustakaan Kecil", koleksi)
    peminjaman = Peminjaman(koleksi, fungsi_login=login_dari_input)

    menu = """
===== {nama} =====
1. Daftar buku          6. Kembalikan buku
2. Daftar kategori      7. Perpanjang peminjaman
3. Cari buku            8. Riwayat peminjaman saya
4. Filter kategori      9. Status peminjaman saya
5. Pinjam buku         10. Login / Logout
0. Keluar"""

    while True:
        print(menu.format(nama=perpus.nama_perpustakaan))
        pilihan = input("Pilih menu: ").strip()
        try:
            if pilihan == "1":
                perpus.tampilkanDaftarBuku()
            elif pilihan == "2":
                perpus.tampilkanKategori()
            elif pilihan == "3":
                hasil = perpus.cariBuku(input("Judul (boleh kosong): "),
                                        input("Penulis (boleh kosong): "))
                perpus.tampilkanDaftarBuku(hasil)
            elif pilihan == "4":
                kategori = pilih_kategori()
                if kategori is None:
                    print("Pilihan kategori tidak valid.")
                else:
                    perpus.tampilkanDaftarBuku(perpus.filterKategori(kategori))
            elif pilihan == "5":
                peminjaman.peminjaman()
            elif pilihan == "6":
                peminjaman.kembalikan()
            elif pilihan == "7":
                peminjaman.perpanjang()
            elif pilihan == "8":
                tampil_data_pengguna(peminjaman, "riwayat")
            elif pilihan == "9":
                tampil_data_pengguna(peminjaman, "status")
            elif pilihan == "10":
                aktif = peminjaman.pengguna_aktif
                if aktif is not None and aktif.sedang_login:
                    aktif.logout()
                    peminjaman.pengguna_aktif = None
                    print("Logout berhasil.")
                else:
                    peminjaman.pengguna_aktif = login_dari_input()
            elif pilihan == "0":
                print("Terima kasih.")
                break
            else:
                print("Menu tidak dikenal.")
        except (PenggunaError, PerpustakaanError) as e:
            print(f"Kesalahan: {e}")


if __name__ == "__main__":
    main()
