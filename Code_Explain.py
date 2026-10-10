import math


# ============================================================
# FUNGSI PENDUKUNG HILL CIPHER
# ============================================================

# Mengubah satu huruf menjadi angka:
# A = 0, B = 1, C = 2, ..., Z = 25.
def huruf_ke_angka(huruf):
    return ord(huruf.upper()) - ord('A')


# Mengubah angka menjadi huruf.
# Modulo 26 menjaga angka tetap berada pada rentang 0 sampai 25.
def angka_ke_huruf(angka):
    return chr((angka % 26) + ord('A'))


# Mencari invers modular dari a terhadap modulo m (default 26).
# Invers adalah x yang memenuhi (a * x) % m == 1.
# Jika tidak ditemukan, fungsi mengembalikan None.
def invers_modulo(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# Mengambil submatriks dengan menghapus baris ke-i dan kolom ke-j.
# Fungsi ini digunakan saat menghitung minor dan kofaktor matriks.
def get_submatriks(M, i, j):
    return [row[:j] + row[j+1:] for idx, row in enumerate(M) if idx != i]


# Menghitung determinan matriks dalam modulo 26.
# Untuk matriks 1x1, determinan adalah elemen tunggalnya.
# Untuk matriks 2x2, digunakan rumus ad - bc.
# Untuk ukuran lebih besar, digunakan ekspansi kofaktor pada baris pertama.
def determinan_matriks(M):
    n = len(M)

    if n == 1:
        return M[0][0]

    if n == 2:
        return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26

    det = 0
    for c in range(n):
        # Hapus baris pertama dan kolom c untuk membentuk submatriks.
        sub = get_submatriks(M, 0, c)
        # Tanda ekspansi kofaktor bergantian positif dan negatif.
        det += ((-1) ** c) * M[0][c] * determinan_matriks(sub)

    return det % 26


# ============================================================
# INPUT DAN VALIDASI MATRIKS KUNCI
# ============================================================

# Meminta elemen matriks kunci dari pengguna.
# Input akan terus diulang sampai kunci memenuhi syarat.
def input_kunci_dinamis():
    while True:
        raw_input_kunci = input("Masukkan elemen matriks kunci normal (pisahkan dengan spasi, misal: 1 0 2 4 4 3 5 7 6): ")
        try:
            # Pisahkan input berdasarkan spasi lalu ubah setiap elemen menjadi integer.
            raw_kunci = list(map(int, raw_input_kunci.split()))
        except ValueError:
            # Jika ada input yang bukan angka, tampilkan pesan dan minta input ulang.
            print("[Error] Input harus berupa angka-angka yang dipisahkan spasi!\n")
            continue

        jumlah_elemen = len(raw_kunci)
        # Akar kuadrat bulat dipakai sebagai kandidat ukuran sisi matriks.
        n = math.isqrt(jumlah_elemen)

        # 1. Pastikan jumlah elemen membentuk matriks bujur sangkar.
        if n * n != jumlah_elemen or n == 0:
            print(f"[Error] Jumlah angka ({jumlah_elemen}) tidak membentuk matriks bujur sangkar (contoh: 4 angka untuk 2x2, 9 angka untuk 3x3)!\n")
            continue

        # Susun daftar angka menjadi matriks berukuran n x n.
        kunci = [raw_kunci[i * n:(i + 1) * n] for i in range(n)]
        det = determinan_matriks(kunci)

        # 2. Validasi determinan.
        # Determinan tidak boleh genap karena akan memiliki faktor 2 dengan 26.
        if det % 2 == 0:
            print(f"[Kunci Ditolak] Determinan (det = {det}) bernilai GENAP! Kunci ini tidak memiliki invers mod 26. Coba kunci lain.\n")
            continue

        # Determinan juga tidak boleh merupakan kelipatan 13.
        if det % 13 == 0:
            print(f"[Kunci Ditolak] Determinan (det = {det}) merupakan KELIPATAN 13! Kunci ini tidak memiliki invers mod 26. Coba kunci lain.\n")
            continue

        # Pemeriksaan umum: determinan harus relatif prima dengan 26.
        if math.gcd(det, 26) != 1:
            print(f"[Kunci Ditolak] Determinan (det = {det}) tidak relatif prima dengan 26. Coba kunci lain.\n")
            continue

        # Tampilkan matriks dan informasikan bahwa kunci lolos validasi.
        print(f"\n> Ukuran kunci terdeteksi: {n}x{n}")
        print("Matriks Kunci (K):")
        for baris in kunci:
            print(f"  {baris}")
        print(f"  (det = {det} -> KUNCI VALID!)\n")
        return kunci


# ============================================================
# MENCARI INVERS MATRIKS KUNCI
# ============================================================

# Menghitung invers matriks K modulo 26.
# Invers dibutuhkan pada proses dekripsi untuk mengembalikan ciphertext.
def invers_matriks_dengan_proses(K):
    n = len(K)

    print("\n--- PROSES MENCARI K⁻¹ ---")

    # Langkah 1: hitung determinan matriks kunci.
    det = determinan_matriks(K)
    print(f"1. Determinan (det):")
    print(f"   det(K) = {det} (mod 26)")

    # Langkah 2: cari invers modular determinan.
    # Cari x yang membuat (det * x) mod 26 sama dengan 1.
    print(f"\n2. Mencari Nilai x (det⁻¹):")
    print(f"   Persamaan: ({det} · x) mod 26 = 1")
    det_inv = None
    for x in range(1, 26):
        if (det * x) % 26 == 1:
            det_inv = x
            print(f"   Uji x = {x}: ({det} · {x}) = {det*x} ≡ 1 (mod 26) [SESUAI]")
            break

    # Jika invers determinan tidak ditemukan, proses tidak bisa dilanjutkan.
    if det_inv is None:
        raise ValueError(f"Determinan {det} tidak memilik invers modular!")

    print(f"   -> det⁻¹ = {det_inv}")

    # Langkah 3: hitung matriks kofaktor.
    print(f"\n3. Perhitungan Matriks hingga menjadi K⁻¹:")
    adjugate = []
    for i in range(n):
        adj_row = []
        for j in range(n):
            # Minor diperoleh dari determinan submatriks.
            sub = get_submatriks(K, i, j)
            sub_det = determinan_matriks(sub)
            # Kofaktor memakai tanda (-1)^(i+j).
            cofactor = ((-1) ** (i + j)) * sub_det
            adj_row.append(cofactor % 26)
        adjugate.append(adj_row)

    # Transposisi matriks kofaktor menghasilkan matriks adjugate.
    adjugate_transposed = [[adjugate[j][i] for j in range(n)] for i in range(n)]
    print("   • Matriks Adjugate:")
    for row in adjugate_transposed:
        print(f"     {row}")

    # Rumus invers: K^-1 = det(K)^-1 * adjugate(K) mod 26.
    K_inv = [[(det_inv * adjugate_transposed[i][j]) % 26 for j in range(n)] for i in range(n)]
    print(f"   • Perkalian Adjugate × det⁻¹ ({det_inv}) mod 26:")
    for row in K_inv:
        print(f"     {row}")

    print("   -> Matriks K⁻¹ Berhasil Ditemukan!")
    print("---------------------------\n")
    return K_inv


# ============================================================
# PROSES ENKRIPSI
# ============================================================

# Mengubah plaintext (pesan asli) menjadi ciphertext (pesan tersandi).
def proses_enkripsi(plaintext, K):
    # Ukuran matriks menentukan banyak huruf dalam setiap blok.
    n = len(K)

    # Ubah teks menjadi kapital dan sisakan hanya karakter yang dianggap huruf.
    plaintext_bersih = "".join(h for h in plaintext.upper() if h.isalpha())

    print(f"\n--- PROSES ENKRIPSI ---")
    print(f"Plaintext awal: {plaintext}")
    print(f"Plaintext bersih: {plaintext_bersih}")

    # Tambahkan X jika panjang teks belum habis dibagi ukuran blok.
    while len(plaintext_bersih) % n != 0:
        plaintext_bersih += 'X'
    print(f"Plaintext setelah padding ('X'): {plaintext_bersih}\n")

    ciphertext = ""
    block_idx = 1

    # Proses teks per blok sepanjang n karakter.
    for i in range(0, len(plaintext_bersih), n):
        blok_teks = plaintext_bersih[i:i+n]
        print(f"Blok {block_idx} -> \"{blok_teks}\":")

        # Konversi setiap huruf pada blok menjadi angka 0 sampai 25.
        vektor = []
        for char in blok_teks:
            val = huruf_ke_angka(char)
            vektor.append(val)
            print(f"  • {char} -> {val}")
        print(f"  Vektor P = {vektor}")

        print("  Perhitungan per baris matriks:")
        hasil_angka = []

        # Kalikan setiap baris matriks kunci dengan vektor plaintext.
        for r in range(n):
            komponen_rumus = []
            jumlah_total = 0
            for c in range(n):
                coeff = K[r][c]
                vec_val = vektor[c]
                komponen_rumus.append(f"({coeff} · {vec_val})")
                jumlah_total += coeff * vec_val

            # Modulo 26 mengubah hasil ke rentang angka alfabet.
            rumus_str = " + ".join(komponen_rumus)
            hasil_mod = jumlah_total % 26
            hasil_angka.append(hasil_mod)
            print(f"    Baris {r+1}: {rumus_str} = {jumlah_total} ≡ {hasil_mod} (mod 26)")

        # Ubah angka hasil enkripsi menjadi huruf ciphertext.
        blok_cipher = "".join(angka_ke_huruf(num) for num in hasil_angka)
        print(f"  Hasil angka: {hasil_angka} -> Huruf Cipher: {blok_cipher}\n")

        # Gabungkan blok hasil ke ciphertext akhir.
        ciphertext += blok_cipher
        block_idx += 1

    print(f"Ciphertext akhir: {ciphertext}")
    print("-----------------------\n")


# ============================================================
# PROSES DEKRIPSI
# ============================================================

# Mengubah ciphertext kembali menjadi plaintext menggunakan invers kunci.
def proses_dekripsi(ciphertext, K):
    n = len(K)

    # Bersihkan ciphertext dengan cara yang sama seperti plaintext.
    ciphertext_bersih = "".join(h for h in ciphertext.upper() if h.isalpha())

    print(f"\n--- PROSES DEKRIPSI ---")
    print(f"Ciphertext awal: {ciphertext}")
    print(f"Ciphertext bersih: {ciphertext_bersih}")

    # Cari invers matriks kunci terlebih dahulu.
    try:
        K_inv = invers_matriks_dengan_proses(K)
    except ValueError as e:
        # Jika invers tidak dapat dihitung, tampilkan error dan hentikan fungsi ini.
        print(f"Error pada Kunci: {e}")
        return

    plaintext = ""
    block_idx = 1

    # Bagi ciphertext menjadi blok-blok sesuai ukuran matriks.
    for i in range(0, len(ciphertext_bersih), n):
        blok_teks = ciphertext_bersih[i:i+n]
        print(f"Blok {block_idx} -> Cipher \"{blok_teks}\":")

        # Konversi huruf ciphertext menjadi vektor angka.
        vektor = []
        for char in blok_teks:
            val = huruf_ke_angka(char)
            vektor.append(val)
            print(f"  • {char} -> {val}")
        print(f"  Vektor C = {vektor}")

        print("  Perhitungan dekripsi per baris matriks K⁻¹:")
        hasil_angka = []

        # Kalikan setiap baris invers kunci dengan vektor ciphertext.
        for r in range(n):
            komponen_rumus = []
            jumlah_total = 0
            for c in range(n):
                coeff = K_inv[r][c]
                vec_val = vektor[c]
                komponen_rumus.append(f"({coeff} · {vec_val})")
                jumlah_total += coeff * vec_val

            # Ambil modulo 26 agar hasil dapat dikonversi kembali menjadi huruf.
            rumus_str = " + ".join(komponen_rumus)
            hasil_mod = jumlah_total % 26
            hasil_angka.append(hasil_mod)
            print(f"    Baris {r+1}: {rumus_str} = {jumlah_total} ≡ {hasil_mod} (mod 26)")

        # Konversi angka hasil dekripsi menjadi huruf plaintext.
        blok_plain = "".join(angka_ke_huruf(num) for num in hasil_angka)
        print(f"  Hasil angka: {hasil_angka} -> Huruf Plaintext: {blok_plain}\n")

        # Gabungkan blok plaintext.
        plaintext += blok_plain
        block_idx += 1

    print(f"Plaintext hasil dekripsi: {plaintext}")
    print("------------------------\n")


# ============================================================
# MENU UTAMA PROGRAM
# ============================================================

# Mengatur pilihan pengguna dan memanggil fungsi yang sesuai.
def main():
    while True:
        print("=======================================")
        print("      PROGRAM UTAMA HILL CIPHER        ")
        print("=======================================")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("0. Keluar")

        # Baca pilihan menu dari pengguna.
        pilihan = input("Pilih menu (0/1/2): ")

        if pilihan == '0':
            # Hentikan perulangan dan akhiri program.
            print("Terima kasih telah menggunakan program ini. Sampai jumpa!")
            break

        elif pilihan == '1':
            # Alur enkripsi: input kunci -> input plaintext -> proses enkripsi.
            print("\n--- MENU ENKRIPSI ---")
            try:
                kunci = input_kunci_dinamis()
                plaintext = input("Masukkan Plaintext: ")
                proses_enkripsi(plaintext, kunci)
            except Exception as e:
                # Tampilkan pesan jika terjadi kesalahan selama proses enkripsi.
                print(f"[Terjadi Kesalahan]: {e}\n")

        elif pilihan == '2':
            # Alur dekripsi: input kunci -> input ciphertext -> proses dekripsi.
            print("\n--- MENU DEKRIPSI ---")
            try:
                kunci = input_kunci_dinamis()
                ciphertext = input("Masukkan Ciphertext: ")
                proses_dekripsi(ciphertext, kunci)
            except Exception as e:
                # Tampilkan pesan jika terjadi kesalahan selama proses dekripsi.
                print(f"[Terjadi Kesalahan]: {e}\n")

        else:
            # Jika pilihan bukan 0, 1, atau 2, tampilkan pesan kesalahan.
            print("Pilihan tidak valid. Silakan pilih 0, 1, atau 2.\n")


# Jalankan menu utama hanya jika file ini dijalankan secara langsung.
if __name__ == "__main__":
    main()