from datetime import datetime, timedelta


class PenggunaError(Exception):
    pass


class DataTidakValidError(PenggunaError):
    pass


class LoginGagalError(PenggunaError):
    pass


class AkunTerkunciError(PenggunaError):
    pass


class BelumLoginError(PenggunaError):
    pass


class Pengguna:
    MAKS_GAGAL = 3
    DURASI_KUNCI = timedelta(hours=1)

    def __init__(self, id_pengguna, nama, password):
        if not isinstance(id_pengguna, int) or isinstance(id_pengguna, bool) or id_pengguna <= 0:
            raise DataTidakValidError("ID harus bilangan bulat positif.")
        if not password or len(password) < 6:
            raise DataTidakValidError("Password minimal 6 karakter.")

        self._id_pengguna = id_pengguna
        self.nama = nama
        self._password = password
        self._sedang_login = False
        self._gagal_login = 0
        self._terkunci_sampai = None
        self._daftar_peminjaman = []

    @property
    def id_pengguna(self):
        return self._id_pengguna

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str) or not nilai.strip():
            raise DataTidakValidError("Nama tidak boleh kosong.")
        self._nama = nilai.strip()

    @property
    def sedang_login(self):
        return self._sedang_login

    def login(self, password, waktu=None):
        waktu = waktu or datetime.now()

        if self._terkunci_sampai is not None:
            if waktu < self._terkunci_sampai:
                raise AkunTerkunciError("Akun terkunci, coba lagi nanti.")
            self._terkunci_sampai = None
            self._gagal_login = 0

        if password == self._password:
            self._gagal_login = 0
            self._sedang_login = True
            return True

        self._gagal_login += 1
        if self._gagal_login >= self.MAKS_GAGAL:
            self._terkunci_sampai = waktu + self.DURASI_KUNCI
            raise AkunTerkunciError("3x gagal login, akun terkunci 1 jam.")
        sisa = self.MAKS_GAGAL - self._gagal_login
        raise LoginGagalError(f"Password salah. Sisa percobaan: {sisa}")

    def logout(self):
        self._wajib_login()
        self._sedang_login = False

    def tambah_peminjaman(self, peminjaman):
        self._wajib_login()
        self._daftar_peminjaman.append(peminjaman)

    def lihat_riwayat_peminjaman(self):
        self._wajib_login()
        return list(self._daftar_peminjaman)

    def lihat_status_peminjaman(self):
        self._wajib_login()
        return [
            {"id": p.id_peminjaman, "status": p.status_peminjaman}
            for p in self._daftar_peminjaman
            if p.status_peminjaman != "DIKEMBALIKAN"
        ]

    def _wajib_login(self):
        if not self._sedang_login:
            raise BelumLoginError("Silakan login terlebih dahulu.")