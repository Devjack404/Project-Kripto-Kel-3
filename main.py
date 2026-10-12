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

# --- FUNGSI MENCETAK MATRIKS AGAR RAPI & SEJAJAR ---
def cetak_matriks(M, indent="  "):
    if not M:
        return
    # Menentukan lebar kolom maksimum agar seragam & rapi
    max_len = max(len(str(val)) for row in M for val in row)
    max_len = max(max_len, 2)  # Minimal 2 karakter agar 1 digit terformat rapi
    for row in M:
        row_str = " ".join(f"{val:{max_len}d}" for val in row)
        print(f"{indent}[ {row_str} ]")

def hitung_determinan_sederhana(M):
    n = len(M)
    if n == 1: return M[0][0]
    if n == 2: return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    d = 0
    for c in range(n):
        d += ((-1) ** c) * M[0][c] * hitung_determinan_sederhana(get_submatriks(M, 0, c))
    return d

# --- HITUNG DETERMINAN DENGAN PENJABARAN RANGKAIAN PROSES ---
def hitung_determinan_dengan_proses(K):
    n = len(K)
    print("\n--- PROSES PERHITUNGAN DETERMINAN KEY ---")
    
    if n == 2:
        a, b = K[0][0], K[0][1]
        c, d = K[1][0], K[1][1]
        
        p1 = a * d
        p2 = b * c
        det_raw = p1 - p2
        det_mod = det_raw % 26
        
        print("Bentuk Matriks K (2x2):")
        cetak_matriks(K, indent="  ")
        print("\nRumus Determinan 2x2: det(K) = (a · d) - (b · c)")
        print(f"1. Diagonal Utama   (a · d) : {a} · {d} = {p1}")
        print(f"2. Diagonal Samping (b · c) : {b} · {c} = {p2}")
        print(f"3. Pengurangan              : {p1} - {p2} = {det_raw}")
        print(f"4. Modulo 26                : {det_raw} mod 26 = {det_mod}")
        return det_raw, det_mod
        
    elif n == 3:
        a, b, c = K[0][0], K[0][1], K[0][2]
        d, e, f = K[1][0], K[1][1], K[1][2]
        g, h, i = K[2][0], K[2][1], K[2][2]
        
        print("Bentuk Matriks K (3x3):")
        cetak_matriks(K, indent="  ")
        print("\nMenggunakan Metode Sarrus (Perkalian Diagonal):")
        print("Tambahkan 2 kolom pertama di sebelah kanan:")
        print(f"  [ {a:2d} {b:2d} {c:2d}  | {a:2d} {b:2d} ]")
        print(f"  [ {d:2d} {e:2d} {f:2d}  | {d:2d} {e:2d} ]")
        print(f"  [ {g:2d} {h:2d} {i:2d}  | {g:2d} {h:2d} ]\n")
        
        p1, p2, p3 = a * e * i, b * f * g, c * d * h
        total_positif = p1 + p2 + p3
        
        print("1. Perkalian Diagonal Utama (Positif / Ditambah):")
        print(f"   • Diagonal 1 : ({a} · {e} · {i}) = {p1}")
        print(f"   • Diagonal 2 : ({b} · {f} · {g}) = {p2}")
        print(f"   • Diagonal 3 : ({c} · {d} · {h}) = {p3}")
        print(f"   • Total Positif = {p1} + {p2} + {p3} = {total_positif}\n")
        
        n1, n2, n3 = c * e * g, a * f * h, b * d * i
        total_negatif = n1 + n2 + n3
        
        print("2. Perkalian Diagonal Samping (Negatif / Dikurangi):")
        print(f"   • Diagonal 1 : ({c} · {e} · {g}) = {n1}")
        print(f"   • Diagonal 2 : ({a} · {f} · {h}) = {n2}")
        print(f"   • Diagonal 3 : ({b} · {d} · {i}) = {n3}")
        print(f"   • Total Negatif = {n1} + {n2} + {n3} = {total_negatif}\n")
        
        det_raw = total_positif - total_negatif
        det_mod = det_raw % 26
        
        print("3. Pengurangan Total Positif - Total Negatif:")
        print(f"   det(K) = {total_positif} - {total_negatif} = {det_raw}")
        print(f"   det(K) mod 26 = {det_raw} mod 26 = {det_mod}")
        return det_raw, det_mod
        
    else:
        print(f"Bentuk Matriks K ({n}x{n}):")
        cetak_matriks(K, indent="  ")
        print(f"\n[Catatan Matematika] Untuk matriks {n}x{n} (> 3x3), Metode Sarrus tidak berlaku.")
        print("Penjabaran menggunakan Metode Ekspansi Kofaktor Baris Ke-1:")
        
        det_raw = 0
        rincian_suku = []
        for c in range(n):
            sub = get_submatriks(K, 0, c)
            sub_det = hitung_determinan_sederhana(sub)
            tanda = 1 if c % 2 == 0 else -1
            tanda_str = "+" if tanda == 1 else "-"
            suku = tanda * K[0][c] * sub_det
            det_raw += suku
            
            print(f"\n• Suku ke-{c+1} [{tanda_str} K[0][{c}] · det(sub-matriks {n-1}x{n-1})]:")
            print(f"  - Elemen K[0][{c}] = {K[0][c]}")
            print(f"  - Sub-matriks {n-1}x{n-1}:")
            cetak_matriks(sub, indent="      ")
            print(f"  - det(sub-matriks {n-1}x{n-1}) = {sub_det}")
            print(f"  - Hasil Suku ke-{c+1} = {tanda_str}({K[0][c]} · {sub_det}) = {suku}")
            rincian_suku.append(f"({suku})")
            
        det_mod = det_raw % 26
        print(f"\nTotal Penjumlahan Suku-suku Ekspansi Kofaktor:")
        print(f"  det(K) = {' + '.join(rincian_suku)} = {det_raw}")
        print(f"  det(K) mod 26 = {det_raw} mod 26 = {det_mod}")
        return det_raw, det_mod

def berikan_saran_perbaikan(K, det_mod):
    print("\n[SARAN PERBAIKAN DARI SISTEM]")
    if det_mod == 0:
        print("• Determinan bernilai 0 (Matriks Singular).")
        print("  Saran: Ubah salah satu angka diagonal utama agar ad ≠ bc.")
    elif det_mod % 2 == 0:
        print(f"• Determinan ({det_mod}) bernilai GENAP.")
        print("  Saran: Ubah salah satu elemen pada baris pertama menjadi ganjil/genap agar hasil det(K) menjadi ganjil.")
    elif det_mod % 13 == 0:
        print(f"• Determinan ({det_mod}) merupakan KELIPATAN 13.")
        print("  Saran: Ubah salah satu nilai pada baris terakhir agar determinan tidak habis dibagi 13.")
    else:
        print(f"• Determinan ({det_mod}) memiliki faktor persekutuan dengan 26.")
        print("  Saran: Ganti salah satu angka pada matriks dengan angka lain.")

# --- PROSES MENCARI K⁻¹ DENGAN RINCIAN ADJOIN SEPENUHNYA ---
def hitung_k_invers_dengan_proses(K, det_mod):
    n = len(K)
    print("\n--- PROSES MENCARI KEY INVERS (K⁻¹) ---")
    
    print(f"1. Determinan Kunci (mod 26): {det_mod}")
    
    print("\n2. Mencari Nilai x untuk det⁻¹ (sehingga det · x ≡ 1 mod 26):")
    det_inv = None
    for x in range(1, 26):
        if (det_mod * x) % 26 == 1:
            det_inv = x
            print(f"   • Uji x = {x}: ({det_mod} · {x}) = {det_mod * x} ≡ 1 (mod 26) [BERHASIL]")
            break
            
    print(f"   -> Maka det⁻¹ = {det_inv}")
    
    print("\n3. Membentuk Matriks Kofaktor & Adjugate:")
    print("   a. Perhitungan Kofaktor C_ij = (-1)^(i+j) · det(M_ij) mod 26:")
    
    cofactor_matrix = []
    for i in range(n):
        cof_row = []
        for j in range(n):
            sub = get_submatriks(K, i, j)
            sub_det_raw = hitung_determinan_sederhana(sub)
            tanda = 1 if (i + j) % 2 == 0 else -1
            tanda_str = "+" if tanda == 1 else "-"
            
            raw_cofactor = tanda * sub_det_raw
            mod_cofactor = raw_cofactor % 26
            cof_row.append(mod_cofactor)
            
            print(f"      • C_{i+1}{j+1} = ({tanda_str}1) · det(Sub_{i+1}{j+1})")
            print(f"        Sub_{i+1}{j+1}:")
            cetak_matriks(sub, indent="          ")
            print(f"        det = {sub_det_raw}")
            print(f"        C_{i+1}{j+1} = {tanda_str}({sub_det_raw}) = {raw_cofactor} ≡ {mod_cofactor} (mod 26)")
        cofactor_matrix.append(cof_row)
        
    print("\n   b. Matriks Kofaktor (C):")
    cetak_matriks(cofactor_matrix, indent="      ")
    
    adjugate = [[cofactor_matrix[j][i] for j in range(n)] for i in range(n)]
    print("\n   c. Matriks Adjugate (adj(K) = Transpose dari C):")
    cetak_matriks(adjugate, indent="      ")
    
    print(f"\n4. Perkalian Adjugate × det⁻¹ ({det_inv}) mod 26:")
    K_inv = []
    for i in range(n):
        inv_row = []
        for j in range(n):
            val_adj = adjugate[i][j]
            prod = val_adj * det_inv
            prod_mod = prod % 26
            inv_row.append(prod_mod)
            print(f"   • K⁻¹[{i+1}][{j+1}] = ({val_adj} · {det_inv}) = {prod} ≡ {prod_mod} (mod 26)")
        K_inv.append(inv_row)
        
    print("\n   Matriks K⁻¹ Akhir:")
    cetak_matriks(K_inv, indent="     ")
    
    print("\n✓ MATRIKS K⁻¹ BERHASIL DITEMUKAN!")
    print("---------------------------------------\n")
    return K_inv

def alur_input_kunci_awal():
    print("=" * 60)
    print("           INPUT KUNCI / KEY HILL CIPHER              ")
    print("=" * 60)
    print("📌 TIPS & TRICK MEMILIH KUNCI VALID:")
    print(" 1. Masukkan elemen angka dipisahkan spasi (misal 4 angka untuk 2x2, 9 angka untuk 3x3).")
    print(" 2. Pastikan determinan TIDAK 0 (matriks tidak boleh singular).")
    print(" 3. Pastikan determinan TIDAK GENAP dan BUKAN KELIPATAN 13.")
    print(" 4. Contoh Kunci 2x2 Valid : 3 3 2 5  (det = 9)")
    print(" 5. Contoh Kunci 3x3 Valid : 1 0 2 4 4 3 5 7 6  (det = 19)")
    print("=" * 60 + "\n")
    
    while True:
        raw_input_kunci = input("Masukkan elemen matriks kunci (misal: 1 0 2 4 4 3 5 7 6): ")
        try:
            raw_kunci = list(map(int, raw_input_kunci.split()))
        except ValueError:
            print("[Error] Input harus berupa angka-angka yang dipisahkan spasi!\n")
            continue
            
        jumlah_elemen = len(raw_kunci)
        n = math.isqrt(jumlah_elemen)
        
        if n * n != jumlah_elemen or n == 0:
            print(f"[Error] Jumlah angka ({jumlah_elemen}) tidak membentuk matriks bujur sangkar (contoh: 4 angka untuk 2x2, 9 angka untuk 3x3)!\n")
            continue
            
        kunci = [raw_kunci[i * n:(i + 1) * n] for i in range(n)]
        
        # Hitung determinan dengan rincian
        det_raw, det_mod = hitung_determinan_dengan_proses(kunci)
        
        # Validasi Determinan
        if det_mod == 0 or det_mod % 2 == 0 or det_mod % 13 == 0 or math.gcd(det_mod, 26) != 1:
            print(f"\n❌ [KUNCI DITOLAK] Determinan mod 26 = {det_mod} TIDAK VALID!")
            berikan_saran_perbaikan(kunci, det_mod)
            print("Silakan input ulang kunci yang baru.\n" + "-" * 50)
            continue
            
        print(f"\n✓ [KUNCI VALID] Determinan mod 26 = {det_mod} memiliki invers modular!")
        
        # Hitung K⁻¹ dengan proses
        k_inv = hitung_k_invers_dengan_proses(kunci, det_mod)
        return kunci, k_inv

def proses_enkripsi(plaintext, K):
    n = len(K)
    plaintext_bersih = "".join(h for h in plaintext.upper() if h.isalpha())
    
    print(f"\n--- PROSES ENKRIPSI ---")
    print(f"Plaintext awal  : {plaintext}")
    print(f"Plaintext bersih: {plaintext_bersih}")
    
    while len(plaintext_bersih) % n != 0:
        plaintext_bersih += 'X'
    print(f"Plaintext dengan padding ('X'): {plaintext_bersih}\n")
    
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
        print("  Perhitungan per baris matriks K:")
        
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

def proses_dekripsi(ciphertext, K_inv):
    n = len(K_inv)
    ciphertext_bersih = "".join(h for h in ciphertext.upper() if h.isalpha())
    
    print(f"\n--- PROSES DEKRIPSI ---")
    print(f"Ciphertext awal  : {ciphertext}")
    print(f"Ciphertext bersih: {ciphertext_bersih}\n")
    
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
        print("  Perhitungan per baris matriks K⁻¹:")
        
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
    kunci, k_inv = alur_input_kunci_awal()
    
    while True:
        n = len(kunci)
        print("=" * 50)
        print("                MENU UTAMA HILL CIPHER            ")
        print("=" * 50)
        print(f" [ TAMPILAN KUNCI AKTIF ({n}x{n}) ]")
        print(" Matriks Kunci Normal (K):")
        cetak_matriks(kunci, indent="   ")
        print(" Matriks Kunci Invers (K⁻¹):")
        cetak_matriks(k_inv, indent="   ")
        print("-" * 50)
        print(" 1. Enkripsi")
        print(" 2. Dekripsi")
        print(" 3. Ganti Kunci")
        print(" 4. Keluar")
        print("=" * 50)
        
        pilihan = input("Pilih menu (1-4): ")
        
        if pilihan == '1':
            teks = input("\nMasukkan Plaintext: ")
            proses_enkripsi(teks, kunci)
            input("Tekan [Enter] untuk kembali ke Menu Utama...")
            print()
            
        elif pilihan == '2':
            teks = input("\nMasukkan Ciphertext: ")
            proses_dekripsi(teks, k_inv)
            input("Tekan [Enter] untuk kembali ke Menu Utama...")
            print()
            
        elif pilihan == '3':
            print("\n--- GANTI KUNCI BARU ---")
            kunci, k_inv = alur_input_kunci_awal()
            
        elif pilihan == '4':
            print("\nTerima kasih telah menggunakan program Hill Cipher. Sampai jumpa!")
            break
            
        else:
            print("\nPilihan tidak valid! Silakan pilih angka 1, 2, 3, atau 4.\n")

if __name__ == "__main__":
    main()