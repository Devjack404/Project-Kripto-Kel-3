import math

def huruf_ke_angka(huruf):
    return ord(huruf.upper()) - ord('A')

def angka_ke_huruf(angka):
    return chr((angka % 26) + ord('A'))

def invers_modulo(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def get_submatriks(M, i, j):
    return [row[:j] + row[j+1:] for idx, row in enumerate(M) if idx != i]

def determinan_matriks(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    
    det = 0
    for c in range(n):
        sub = get_submatriks(M, 0, c)
        det += ((-1) ** c) * M[0][c] * determinan_matriks(sub)
    return det % 26

# --- GATE INPUT KUNCI DENGAN VALIDASI DET GENAP & KELIPATAN 13 ---
def input_kunci_dinamis():
    while True:
        raw_input_kunci = input("Masukkan elemen matriks kunci normal (pisahkan dengan spasi, misal: 1 0 2 4 4 3 5 7 6): ")
        try:
            raw_kunci = list(map(int, raw_input_kunci.split()))
        except ValueError:
            print("[Error] Input harus berupa angka-angka yang dipisahkan spasi!\n")
            continue
            
        jumlah_elemen = len(raw_kunci)
        n = math.isqrt(jumlah_elemen)
        
        # 1. Cek Matriks Bujur Sangkar
        if n * n != jumlah_elemen or n == 0:
            print(f"[Error] Jumlah angka ({jumlah_elemen}) tidak membentuk matriks bujur sangkar (contoh: 4 angka untuk 2x2, 9 angka untuk 3x3)!\n")
            continue
            
        kunci = [raw_kunci[i * n:(i + 1) * n] for i in range(n)]
        det = determinan_matriks(kunci)
        
        # 2. Gate Validasi Determinan
        if det % 2 == 0:
            print(f"[Kunci Ditolak] Determinan (det = {det}) bernilai GENAP! Kunci ini tidak memiliki invers mod 26. Coba kunci lain.\n")
            continue
        if det % 13 == 0:
            print(f"[Kunci Ditolak] Determinan (det = {det}) merupakan KELIPATAN 13! Kunci ini tidak memiliki invers mod 26. Coba kunci lain.\n")
            continue
        if math.gcd(det, 26) != 1:
            print(f"[Kunci Ditolak] Determinan (det = {det}) tidak relatif prima dengan 26. Coba kunci lain.\n")
            continue
            
        print(f"\n> Ukuran kunci terdeteksi: {n}x{n}")
        print("Matriks Kunci (K):")
        for baris in kunci:
            print(f"  {baris}")
        print(f"  (det = {det} -> KUNCI VALID!)\n")
        return kunci

# --- PROSES MENCARI K⁻¹ (RINGKAS & TERSTRUKTUR) ---
def invers_matriks_dengan_proses(K):
    n = len(K)
    print("\n--- PROSES MENCARI K⁻¹ ---")
    
    # Langkah 1: Determinan
    det = determinan_matriks(K)
    print(f"1. Determinan (det):")
    print(f"   det(K) = {det} (mod 26)")
    
    # Langkah 2: Mencari x untuk det⁻¹
    print(f"\n2. Mencari Nilai x (det⁻¹):")
    print(f"   Persamaan: ({det} · x) mod 26 = 1")
    
    det_inv = None
    for x in range(1, 26):
        if (det * x) % 26 == 1:
            det_inv = x
            print(f"   Uji x = {x}: ({det} · {x}) = {det*x} ≡ 1 (mod 26) [SESUAI]")
            break
            
    if det_inv is None:
        raise ValueError(f"Determinan {det} tidak memilik invers modular!")
        
    print(f"   -> det⁻¹ = {det_inv}")
    
    # Langkah 3: Perhitungan Matriks Adjugate & K⁻¹
    print(f"\n3. Perhitungan Matriks hingga menjadi K⁻¹:")
    adjugate = []
    for i in range(n):
        adj_row = []
        for j in range(n):
            sub = get_submatriks(K, i, j)
            sub_det = determinan_matriks(sub)
            cofactor = ((-1) ** (i + j)) * sub_det
            adj_row.append(cofactor % 26)
        adjugate.append(adj_row)
        
    adjugate_transposed = [[adjugate[j][i] for j in range(n)] for i in range(n)]
    print("   • Matriks Adjugate:")
    for row in adjugate_transposed:
        print(f"     {row}")
        
    K_inv = [[(det_inv * adjugate_transposed[i][j]) % 26 for j in range(n)] for i in range(n)]
    print(f"   • Perkalian Adjugate × det⁻¹ ({det_inv}) mod 26:")
    for row in K_inv:
        print(f"     {row}")
        
    print("   -> Matriks K⁻¹ Berhasil Ditemukan!")
    print("---------------------------\n")
    return K_inv

def proses_enkripsi(plaintext, K):
    n = len(K)
    plaintext_bersih = "".join(h for h in plaintext.upper() if h.isalpha())
    
    print(f"\n--- PROSES ENKRIPSI ---")
    print(f"Plaintext awal: {plaintext}")
    print(f"Plaintext bersih: {plaintext_bersih}")
    
    while len(plaintext_bersih) % n != 0:
        plaintext_bersih += 'X'
    print(f"Plaintext setelah padding ('X'): {plaintext_bersih}\n")
    
    ciphertext = ""
    block_idx = 1
    for i in range(0, len(plaintext_bersih), n):
        blok_teks = plaintext_bersih[i:i+n]
        print(f"Blok {block_idx} -> \"{blok_teks}\":")
        
        vektor = []
        for char in blok_teks:
            val = huruf_ke_angka(char)
            vektor.append(val)
            print(f"  • {char} -> {val}")
            
        print(f"  Vektor P = {vektor}")
        print("  Perhitungan per baris matriks:")
        
        hasil_angka = []
        for r in range(n):
            komponen_rumus = []
            jumlah_total = 0
            for c in range(n):
                coeff = K[r][c]
                vec_val = vektor[c]
                komponen_rumus.append(f"({coeff} · {vec_val})")
                jumlah_total += coeff * vec_val
            
            rumus_str = " + ".join(komponen_rumus)
            hasil_mod = jumlah_total % 26
            hasil_angka.append(hasil_mod)
            print(f"    Baris {r+1}: {rumus_str} = {jumlah_total} ≡ {hasil_mod} (mod 26)")
            
        blok_cipher = "".join(angka_ke_huruf(num) for num in hasil_angka)
        print(f"  Hasil angka: {hasil_angka} -> Huruf Cipher: {blok_cipher}\n")
        ciphertext += blok_cipher
        block_idx += 1
        
    print(f"Ciphertext akhir: {ciphertext}")
    print("-----------------------\n")

def proses_dekripsi(ciphertext, K):
    n = len(K)
    ciphertext_bersih = "".join(h for h in ciphertext.upper() if h.isalpha())
    
    print(f"\n--- PROSES DEKRIPSI ---")
    print(f"Ciphertext awal: {ciphertext}")
    print(f"Ciphertext bersih: {ciphertext_bersih}")
    
    try:
        K_inv = invers_matriks_dengan_proses(K)
    except ValueError as e:
        print(f"Error pada Kunci: {e}")
        return

    plaintext = ""
    block_idx = 1
    for i in range(0, len(ciphertext_bersih), n):
        blok_teks = ciphertext_bersih[i:i+n]
        print(f"Blok {block_idx} -> Cipher \"{blok_teks}\":")
        
        vektor = []
        for char in blok_teks:
            val = huruf_ke_angka(char)
            vektor.append(val)
            print(f"  • {char} -> {val}")
            
        print(f"  Vektor C = {vektor}")
        print("  Perhitungan dekripsi per baris matriks K⁻¹:")
        
        hasil_angka = []
        for r in range(n):
            komponen_rumus = []
            jumlah_total = 0
            for c in range(n):
                coeff = K_inv[r][c]
                vec_val = vektor[c]
                komponen_rumus.append(f"({coeff} · {vec_val})")
                jumlah_total += coeff * vec_val
            
            rumus_str = " + ".join(komponen_rumus)
            hasil_mod = jumlah_total % 26
            hasil_angka.append(hasil_mod)
            print(f"    Baris {r+1}: {rumus_str} = {jumlah_total} ≡ {hasil_mod} (mod 26)")
            
        blok_plain = "".join(angka_ke_huruf(num) for num in hasil_angka)
        print(f"  Hasil angka: {hasil_angka} -> Huruf Plaintext: {blok_plain}\n")
        plaintext += blok_plain
        block_idx += 1
        
    print(f"Plaintext hasil dekripsi: {plaintext}")
    print("------------------------\n")

def main():
    while True:
        print("=======================================")
        print("      PROGRAM UTAMA HILL CIPHER        ")
        print("=======================================")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("0. Keluar")
        
        pilihan = input("Pilih menu (0/1/2): ")
        
        if pilihan == '0':
            print("Terima kasih telah menggunakan program ini. Sampai jumpa!")
            break
            
        elif pilihan == '1':
            print("\n--- MENU ENKRIPSI ---")
            try:
                kunci = input_kunci_dinamis()
                plaintext = input("Masukkan Plaintext: ")
                proses_enkripsi(plaintext, kunci)
            except Exception as e:
                print(f"[Terjadi Kesalahan]: {e}\n")
                
        elif pilihan == '2':
            print("\n--- MENU DEKRIPSI ---")
            try:
                kunci = input_kunci_dinamis()
                ciphertext = input("Masukkan Ciphertext: ")
                proses_dekripsi(ciphertext, kunci)
            except Exception as e:
                print(f"[Terjadi Kesalahan]: {e}\n")
                
        else:
            print("Pilihan tidak valid. Silakan pilih 0, 1, atau 2.\n")

if __name__ == "__main__":
    main()