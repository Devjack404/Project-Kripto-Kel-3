import math

# ==============================================================================
# 1. FUNGSI KONVERSI KARAKTER & ANGKA
# ==============================================================================

def huruf_ke_angka(huruf):
    """
    Fungsi: Mengubah satu karakter huruf (A-Z) menjadi representasi angka (0-25).
    
    Alur Kerja:
    1. huruf.upper() memastikan huruf selalu berupa huruf kapital (misal 'a' menjadi 'A').
    2. ord() mengambil nilai kode ASCII dari karakter tersebut.
       - Nilai ASCII 'A' adalah 65, 'B' adalah 66, ..., 'Z' adalah 90.
    3. Nilai ASCII huruf dikurangi dengan ASCII 'A' (65):
       - 'A' -> 65 - 65 = 0
       - 'B' -> 66 - 65 = 1
       - 'Z' -> 90 - 65 = 25
    """
    return ord(huruf.upper()) - ord('A')


def angka_ke_huruf(angka):
    """
    Fungsi: Mengubah nilai angka (0-25) kembali menjadi karakter huruf kapital (A-Z).
    
    Alur Kerja:
    1. angka % 26: Melakukan operasi modulo 26 agar nilai angka selalu berada 
       dalam rentang alfabet 0 sampai 25 (mencegah overflow jika nilainya >= 26).
    2. Menambahkan hasil modulo dengan nilai ASCII 'A' (65).
    3. chr(): Mengonversi angka kode ASCII kembali menjadi bentuk karakter string.
       - 0 -> chr(0 + 65) = 'A'
       - 1 -> chr(1 + 65) = 'B'
       - 25 -> chr(25 + 65) = 'Z'
    """
    return chr((angka % 26) + ord('A'))


# ==============================================================================
# 2. FUNGSI MATEMATIKA & OPERASI MATRIKS
# ==============================================================================

def invers_modulo(a, m=26):
    """
    Fungsi: Mencari nilai invers perkalian modular dari bilangan 'a' modulo 'm' (default m = 26).
    Invers modular adalah bilangan bulat 'x' sedemikian sehingga: (a * x) mod m == 1.
    
    Alur Kerja:
    1. a = a % m: Menyederhanakan nilai 'a' ke dalam rentang 0 hingga m-1.
    2. Looping nilai x dari 1 hingga m-1 (metode brute-force/pencarian langsung).
    3. Jika ditemukan nilai x yang memenuhi persamaan (a * x) % m == 1, 
       maka nilai x tersebut adalah invers modularnya dan langsung dikembalikan.
    4. Jika hingga perulangan selesai tidak ditemukan, kembalikan None (tidak punya invers).
    """
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def get_submatriks(M, i, j):
    """
    Fungsi: Menghasilkan sub-matriks baru dari matriks M dengan cara menghapus
    baris ke-i dan kolom ke-j. Fungsi ini digunakan untuk menghitung minor kofaktor.
    
    Alur Kerja:
    1. enumerate(M) menelusuri setiap baris beserta indeksnya (idx).
    2. Kondisi 'if idx != i': Melewati/mengabaikan baris ke-i yang ingin dihapus.
    3. Pada baris yang terpilih, kolom ke-j dihapus dengan slicing list:
       - row[:j]: Mengambil elemen-elemen sebelum kolom j.
       - row[j+1:]: Mengambil elemen-elemen setelah kolom j.
       - row[:j] + row[j+1:]: Menggabungkan keduanya (elemen kolom j terbuang).
    4. Mengembalikan matriks baru berukuran (n-1) x (n-1).
    """
    return [row[:j] + row[j+1:] for idx, row in enumerate(M) if idx != i]


# --- FUNGSI MENCETAK MATRIKS AGAR RAPI & SEJAJAR ---
def cetak_matriks(M, indent="  "):
    """
    Fungsi: Mencetak tampilan matriks ke terminal dengan format yang rapi dan sejajar.
    
    Alur Kerja:
    1. Cek apakah matriks M kosong. Jika kosong, fungsi langsung berhenti.
    2. Menghitung panjang karakter terpanjang dari setiap angka di dalam matriks
       menggunakan len(str(val)), agar semua kolom memiliki lebar yang sama.
    3. Menetapkan batas minimal lebar kolom = 2 karakter agar angka 1 digit tetap rapi.
    4. Looping setiap baris, meratakan angka dengan format f"{val:{max_len}d}",
       lalu mencetak baris dengan kurung siku [ ... ] sesuai indentasi.
    """
    if not M:
        return
    # Menentukan lebar kolom maksimum agar seragam & rapi
    max_len = max(len(str(val)) for row in M for val in row)
    max_len = max(max_len, 2)  # Minimal 2 karakter agar 1 digit terformat rapi
    for row in M:
        row_str = " ".join(f"{val:{max_len}d}" for val in row)
        print(f"{indent}[ {row_str} ]")


def hitung_determinan_sederhana(M):
    """
    Fungsi: Menghitung nilai determinan matriks persegi secara rekursif murni tanpa menampilkan proses.
    Fungsi ini dipakai secara internal ketika menghitung determinan sub-matriks pada kofaktor.
    
    Alur Kerja:
    1. Ambil ukuran matriks n (jumlah baris/kolom).
    2. Kasus dasar rekursi:
       - Jika n == 1: Determinan adalah nilai elemen tunggal itu sendiri M[0][0].
       - Jika n == 2: Gunakan rumus perkalian silang: (M[0][0] * M[1][1]) - (M[0][1] * M[1][0]).
    3. Jika n > 2: Gunakan metode Ekspansi Kofaktor pada baris pertama (baris 0):
       - Looping setiap kolom c dari 0 sampai n-1.
       - Hitung tanda selang-seling: ((-1) ** c).
       - Kalikan tanda dengan elemen baris pertama M[0][c] dan determinan sub-matriksnya
         secara rekursif: hitung_determinan_sederhana(get_submatriks(M, 0, c)).
       - Jumlahkan semua suku kofaktor ke variabel d dan kembalikan hasilnya.
    """
    n = len(M)
    if n == 1: return M[0][0]
    if n == 2: return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    d = 0
    for c in range(n):
        d += ((-1) ** c) * M[0][c] * hitung_determinan_sederhana(get_submatriks(M, 0, c))
    return d


# --- HITUNG DETERMINAN DENGAN PENJABARAN RANGKAIAN PROSES ---
def hitung_determinan_dengan_proses(K):
    """
    Fungsi: Menghitung determinan matriks kunci K sekaligus menampilkan penjabaran
    setiap langkah perhitungannya secara detail ke layar agar pengguna dapat memahaminya.
    
    Alur Kerja:
    1. Mendeteksi dimensi matriks kunci K (n x n):
       a. Jika n == 2 (Matriks 2x2):
          - Ambil elemen a, b, c, d.
          - Hitung diagonal utama (a * d) dan diagonal samping (b * c).
          - Hitung determinan asli: det_raw = (a * d) - (b * c).
          - Hitung determinan modulo 26: det_mod = det_raw % 26.
          - Cetak langkah-langkahnya ke layar.
       b. Jika n == 3 (Matriks 3x3):
          - Menggunakan Metode Sarrus (duplikasi 2 kolom pertama di sebelah kanan).
          - Hitung 3 perkalian diagonal utama (positif): (a*e*i), (b*f*g), (c*d*h).
          - Hitung 3 perkalian diagonal samping (negatif): (c*e*g), (a*f*h), (b*d*i).
          - Hitung determinan asli: det_raw = total_positif - total_negatif.
          - Hitung determinan modulo 26: det_mod = det_raw % 26.
          - Cetak rincian perkalian dan penjumlahannya ke layar.
       c. Jika n > 3:
          - Karena metode Sarrus hanya berlaku untuk 3x3, gunakan Ekspansi Kofaktor Baris Pertama.
          - Looping setiap elemen di baris ke-1, ambil sub-matriksnya, hitung determinan sub-matriks,
            dan terapkan tanda (+ / -).
          - Jumlahkan seluruh suku untuk memperoleh det_raw dan det_mod.
    2. Mengembalikan pasangan nilai (det_raw, det_mod).
    """
    n = len(K)
    print("\n--- PROSES PERHITUNGAN DETERMINAN KEY ---")
    
    # Kasus Matriks Ordo 2x2
    if n == 2:
        a, b = K[0][0], K[0][1]
        c, d = K[1][0], K[1][1]
        
        # Perhitungan perkalian diagonal
        p1 = a * d
        p2 = b * c
        det_raw = p1 - p2
        det_mod = det_raw % 26
        
        # Tampilkan langkah perhitungan ke layar
        print("Bentuk Matriks K (2x2):")
        cetak_matriks(K, indent="  ")
        print("\nRumus Determinan 2x2: det(K) = (a · d) - (b · c)")
        print(f"1. Diagonal Utama   (a · d) : {a} · {d} = {p1}")
        print(f"2. Diagonal Samping (b · c) : {b} · {c} = {p2}")
        print(f"3. Pengurangan              : {p1} - {p2} = {det_raw}")
        print(f"4. Modulo 26                : {det_raw} mod 26 = {det_mod}")
        return det_raw, det_mod
        
    # Kasus Matriks Ordo 3x3
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
        
        # Diagonal utama (arah kiri-atas ke kanan-bawah bernilai positif)
        p1, p2, p3 = a * e * i, b * f * g, c * d * h
        total_positif = p1 + p2 + p3
        
        print("1. Perkalian Diagonal Utama (Positif / Ditambah):")
        print(f"   • Diagonal 1 : ({a} · {e} · {i}) = {p1}")
        print(f"   • Diagonal 2 : ({b} · {f} · {g}) = {p2}")
        print(f"   • Diagonal 3 : ({c} · {d} · {h}) = {p3}")
        print(f"   • Total Positif = {p1} + {p2} + {p3} = {total_positif}\n")
        
        # Diagonal samping (arah kanan-atas ke kiri-bawah bernilai negatif)
        n1, n2, n3 = c * e * g, a * f * h, b * d * i
        total_negatif = n1 + n2 + n3
        
        print("2. Perkalian Diagonal Samping (Negatif / Dikurangi):")
        print(f"   • Diagonal 1 : ({c} · {e} · {g}) = {n1}")
        print(f"   • Diagonal 2 : ({a} · {f} · {h}) = {n2}")
        print(f"   • Diagonal 3 : ({b} · {d} · {i}) = {n3}")
        print(f"   • Total Negatif = {n1} + {n2} + {n3} = {total_negatif}\n")
        
        # Pengurangan total positif dengan total negatif
        det_raw = total_positif - total_negatif
        det_mod = det_raw % 26
        
        print("3. Pengurangan Total Positif - Total Negatif:")
        print(f"   det(K) = {total_positif} - {total_negatif} = {det_raw}")
        print(f"   det(K) mod 26 = {det_raw} mod 26 = {det_mod}")
        return det_raw, det_mod
        
    # Kasus Matriks Ordo Lebih Besar dari 3x3 (> 3x3)
    else:
        print(f"Bentuk Matriks K ({n}x{n}):")
        cetak_matriks(K, indent="  ")
        print(f"\n[Catatan Matematika] Untuk matriks {n}x{n} (> 3x3), Metode Sarrus tidak berlaku.")
        print("Penjabaran menggunakan Metode Ekspansi Kofaktor Baris Ke-1:")
        
        det_raw = 0
        rincian_suku = []
        # Uraikan berdasarkan elemen-elemen baris ke-1 (indeks baris 0)
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
    """
    Fungsi: Menganalisis penyebab mengapa kunci ditolak dan memberikan saran perbaikan konkret.
    Kunci Hill Cipher wajib memiliki determinan yang relatif prima dengan 26 (gcd(det, 26) == 1).
    
    Alur Kerja:
    1. Periksa nilai det_mod (determinan modulo 26):
       - Jika det_mod == 0: Matriks singular (tidak punya invers matriks).
         Saran: Ubah angka diagonal utama agar hasil ad != bc.
       - Jika det_mod genap: Memiliki faktor pembagi 2 (faktor persekutuan dengan 26).
         Saran: Ubah salah satu angka agar determinan bernilai ganjil.
       - Jika det_mod kelipatan 13: Memiliki faktor pembagi 13 (faktor persekutuan dengan 26).
         Saran: Ubah nilai elemen matriks agar tidak kelipatan 13.
       - Kasus lain: Mengingatkan pengguna untuk mengganti salah satu angka pada matriks.
    2. Menampilkan saran tersebut ke layar agar pengguna dapat memperbaiki input kuncinya.
    """
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


def cek_kunci_trivial(K):
    """
    Fungsi: Mendeteksi apakah matriks kunci K bersifat 'trivial', yaitu kunci yang secara
    matematis valid (punya invers mod 26) NAMUN menghasilkan Ciphertext == Plaintext,
    sehingga enkripsi tidak memberikan keamanan apapun.

    Kasus Trivial yang Dideteksi:
    - Matriks Identitas (I): Seluruh elemen diagonal bernilai 1 (mod 26) dan
      semua elemen di luar diagonal bernilai 0 (mod 26).
    - Mengapa berbahaya: Rumus enkripsi Hill Cipher adalah C = K·P mod 26.
      Jika K ≡ I (mod 26), maka C = I·P = P, artinya Ciphertext = Plaintext.
      Kunci tidak mengacak teks sama sekali!

    Alur Kerja:
    1. Dapatkan ukuran matriks n.
    2. Periksa setiap elemen K[i][j] terhadap nilai yang diharapkan pada matriks identitas:
       - Jika i == j (diagonal): nilai harus 1 (mod 26).
       - Jika i != j (luar diagonal): nilai harus 0 (mod 26).
    3. Jika semua elemen memenuhi kondisi di atas → kembalikan True (kunci trivial).
    4. Jika ada satu saja elemen yang tidak memenuhi → kembalikan False (kunci aman).
    """
    n = len(K)
    for i in range(n):
        for j in range(n):
            # Nilai yang diharapkan: 1 jika diagonal, 0 jika bukan diagonal
            expected = 1 if i == j else 0
            # Bandingkan nilai aktual (mod 26) dengan nilai matriks identitas
            if K[i][j] % 26 != expected:
                return False  # Setidaknya satu elemen berbeda → bukan identitas
    return True  # Semua elemen cocok → matriks identitas (trivial)


# --- PROSES MENCARI K⁻¹ DENGAN RINCIAN ADJOIN SEPENUHNYA ---
def hitung_k_invers_dengan_proses(K, det_mod):
    """
    Fungsi: Menghitung matriks invers kunci (K⁻¹) dalam aritmatika modulo 26
    serta menampilkan seluruh prosesnya secara bertahap ke layar.
    
    Rumus: K⁻¹ = (det(K)⁻¹ * Adjoin(K)) mod 26
    
    Alur Kerja:
    1. Langkah 1: Tampilkan determinan kunci mod 26 (det_mod).
    2. Langkah 2: Cari invers perkalian modular determinan (det⁻¹), yaitu bilangan x (1-25)
       sehingga (det_mod * x) mod 26 == 1.
    3. Langkah 3a & 3b: Hitung Matriks Kofaktor (C):
       - Untuk setiap elemen baris i dan kolom j, ambil sub-matriksnya dengan get_submatriks(K, i, j).
       - Hitung determinan sub-matriks tersebut.
       - Terapkan tanda selang-seling (-1)^(i+j).
       - Simpan nilai kofaktor C_ij yang sudah di-modulo 26.
    4. Langkah 3c: Bentuk Matriks Adjugate / Adjoin (adj(K)):
       - Melakukan Transpose pada matriks kofaktor C (menukar posisi baris menjadi kolom: adj[i][j] = C[j][i]).
    5. Langkah 4: Kalikan setiap elemen matriks Adjoin dengan det⁻¹ lalu modulo 26:
       - K⁻¹[i][j] = (adj[i][j] * det⁻¹) mod 26.
    6. Cetak matriks K⁻¹ akhir yang berhasil didapatkan dan kembalikan matriks tersebut.
    """
    n = len(K)
    print("\n--- PROSES MENCARI KEY INVERS (K⁻¹) ---")
    
    # 1. Menampilkan determinan
    print(f"1. Determinan Kunci (mod 26): {det_mod}")
    
    # 2. Mencari nilai invers determinan (det⁻¹)
    print("\n2. Mencari Nilai x untuk det⁻¹ (sehingga det · x ≡ 1 mod 26):")
    det_inv = None
    for x in range(1, 26):
        if (det_mod * x) % 26 == 1:
            det_inv = x
            print(f"   • Uji x = {x}: ({det_mod} · {x}) = {det_mod * x} ≡ 1 (mod 26) [BERHASIL]")
            break
            
    print(f"   -> Maka det⁻¹ = {det_inv}")
    
    # 3. Menghitung Matriks Kofaktor & Adjoin
    print("\n3. Membentuk Matriks Kofaktor & Adjugate:")
    print("   a. Perhitungan Kofaktor C_ij = (-1)^(i+j) · det(M_ij) mod 26:")
    
    cofactor_matrix = []
    for i in range(n):
        cof_row = []
        for j in range(n):
            # Ambil sub-matriks tanpa baris i dan kolom j
            sub = get_submatriks(K, i, j)
            sub_det_raw = hitung_determinan_sederhana(sub)
            # Tanda kofaktor: jika (i+j) genap bertanda +, jika ganjil bertanda -
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
    
    # Adjugate adalah Transpose dari matriks kofaktor (baris ditukar dengan kolom)
    adjugate = [[cofactor_matrix[j][i] for j in range(n)] for i in range(n)]
    print("\n   c. Matriks Adjugate (adj(K) = Transpose dari C):")
    cetak_matriks(adjugate, indent="      ")
    
    # 4. Perkalian Adjugate dengan det⁻¹ modulo 26
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
    """
    Fungsi: Mengatur alur penerimaan input matriks kunci dari pengguna,
    memvalidasi kelayakan kunci secara matematis, dan menghitung matriks inversnya.
    
    Alur Kerja:
    1. Menampilkan panduan dan tips syarat kunci yang valid untuk Hill Cipher:
       - Harus berukuran persegi (misal 4 angka untuk 2x2, 9 angka untuk 3x3).
       - Determinan tidak boleh 0, tidak genap, dan bukan kelipatan 13.
       - FPB/gcd(determinan, 26) harus sama dengan 1.
       - Bukan matriks identitas (trivial key).
    2. Melakukan perulangan input (while True) hingga kunci yang valid dimasukkan:
       a. Membaca teks masukan dan mengonversinya menjadi list angka integer.
       b. Menghitung ukuran matriks n menggunakan math.isqrt() (akar kuadrat integer).
       c. Memastikan jumlah angka pas membentuk matriks bujur sangkar (n * n == jumlah_elemen).
       d. Mengubah list 1 dimensi menjadi list 2 dimensi (matriks n x n).
       e. Menghitung determinan kunci melalui fungsi hitung_determinan_dengan_proses().
       f. Validasi kelayakan determinan (mod 26):
          - Jika tidak valid, panggil fungsi berikan_saran_perbaikan() dan minta input ulang.
          - Jika valid, lanjutkan ke validasi berikutnya.
       g. Validasi kunci trivial menggunakan cek_kunci_trivial():
          - Jika kunci adalah matriks identitas (mod 26), tampilkan peringatan detail dan saran,
            lalu minta input ulang.
       h. Jika semua validasi lolos, hitung K⁻¹ dan kembalikan pasangan (kunci, k_inv).
    """
    print("=" * 60)
    print("           INPUT KUNCI / KEY HILL CIPHER              ")
    print("=" * 60)
    print("📌 TIPS & TRICK MEMILIH KUNCI VALID:")
    print(" 1. Masukkan elemen angka dipisahkan spasi (misal 4 angka untuk 2x2, 9 angka untuk 3x3).")
    print(" 2. Pastikan determinan TIDAK 0 (matriks tidak boleh singular).")
    print(" 3. Pastikan determinan TIDAK GENAP dan BUKAN KELIPATAN 13.")
    print(" 4. Contoh Kunci 2x2 Valid : 3 3 2 5  (det = 9)")
    print(" 5. Contoh Kunci 3x3 Valid : 1 0 2 4 4 3 5 7 6  (det = 19)")
    print(" 6. HINDARI Matriks Identitas (diagonal serba 1, lainnya 0) → ciphertext = plaintext!")
    print("=" * 60 + "\n")
    
    while True:
        raw_input_kunci = input("Masukkan elemen matriks kunci (misal: 1 0 2 4 4 3 5 7 6): ")
        # Validasi 1: Input harus dapat dikonversi menjadi integer
        try:
            raw_kunci = list(map(int, raw_input_kunci.split()))
        except ValueError:
            print("[Error] Input harus berupa angka-angka yang dipisahkan spasi!\n")
            continue
            
        jumlah_elemen = len(raw_kunci)
        n = math.isqrt(jumlah_elemen)
        
        # Validasi 2: Jumlah elemen harus membentuk matriks persegi (n x n)
        if n * n != jumlah_elemen or n == 0:
            print(f"[Error] Jumlah angka ({jumlah_elemen}) tidak membentuk matriks bujur sangkar (contoh: 4 angka untuk 2x2, 9 angka untuk 3x3)!\n")
            continue
            
        # Mengubah list 1D menjadi matriks 2D berukuran n x n
        kunci = [raw_kunci[i * n:(i + 1) * n] for i in range(n)]
        
        # Hitung determinan dengan rincian proses
        det_raw, det_mod = hitung_determinan_dengan_proses(kunci)
        
        # Validasi 3: Determinan harus relatif prima dengan 26 (memiliki invers modulo 26)
        if det_mod == 0 or det_mod % 2 == 0 or det_mod % 13 == 0 or math.gcd(det_mod, 26) != 1:
            print(f"\n❌ [KUNCI DITOLAK] Determinan mod 26 = {det_mod} TIDAK VALID!")
            berikan_saran_perbaikan(kunci, det_mod)
            print("Silakan input ulang kunci yang baru.\n" + "-" * 50)
            continue

        # Validasi 4: Cek apakah kunci bersifat trivial (matriks identitas mod 26)
        # Kunci trivial menyebabkan K·P = P → Ciphertext = Plaintext (tidak ada enkripsi)
        if cek_kunci_trivial(kunci):
            n_size = len(kunci)
            print(f"\n⚠️  [PERINGATAN KUNCI TRIVIAL] Kunci yang Anda masukkan adalah Matriks Identitas {n_size}x{n_size}!")
            print("=" * 60)
            print("📌 PENJELASAN MASALAH:")
            print(f"   Matriks Identitas {n_size}x{n_size} memang memiliki determinan = 1 (valid secara matematis),")
            print("   TETAPI ketika digunakan sebagai kunci Hill Cipher, rumus enkripsi menjadi:")
            print("     C = K · P mod 26")
            print(f"     C = I · P mod 26  ← Karena K = I (Matriks Identitas)")
            print("     C = P              ← Hasilnya: Ciphertext = Plaintext!")
            print("   Artinya: Teks Anda TIDAK DIENKRIPSI sama sekali — teks asli langsung terlihat.")
            print("   Kunci ini TIDAK AMAN dan tidak boleh digunakan dalam kriptografi.")
            print("="*60)
            print("💡 SARAN PERBAIKAN:")
            print("   Pilih kunci yang elemennya tidak membentuk matriks identitas.")
            print("   Contoh kunci yang aman dan valid:")
            print("   • 2x2 : 3 3 2 5     (det mod 26 = 9)")
            print("   • 3x3 : 1 0 2 4 4 3 5 7 6  (det mod 26 = 19)")
            print("   • 4x4 : 1 2 1 0 0 1 2 1 1 0 1 2 2 1 0 1  (det mod 26 = 3)")
            print("   Pastikan tidak ada baris/kolom yang saling merupakan kelipatan satu sama lain.")
            print("-" * 60)
            print("Silakan input ulang kunci yang baru.\n" + "-" * 50)
            continue
            
        print(f"\n✓ [KUNCI VALID] Determinan mod 26 = {det_mod} memiliki invers modular!")
        
        # Hitung K⁻¹ dengan rincian proses
        k_inv = hitung_k_invers_dengan_proses(kunci, det_mod)
        return kunci, k_inv


# ==============================================================================
# 3. FUNGSI ENKRIPSI & DEKRIPSI
# ==============================================================================

def proses_enkripsi(plaintext, K):
    """
    Fungsi: Melakukan proses enkripsi teks terang (Plaintext) menjadi teks tersandi (Ciphertext)
    menggunakan algoritma Hill Cipher dengan matriks kunci K.
    
    Rumus Matematis: C = (K · P) mod 26
    
    Alur Kerja:
    1. Pembersihan Teks:
       - Mengambil hanya karakter huruf alfabet (h.isalpha()) dan mengubahnya ke huruf besar (h.upper()).
       - Menghilangkan spasi, angka, dan tanda baca.
    2. Padding (Penambahan Karakter):
       - Matriks kunci berukuran n x n membutuhkan input teks dengan kelipatan n.
       - Jika panjang teks belum kelipatan n (len % n != 0), tambahkan karakter 'X' di akhir teks.
    3. Enkripsi Blok demi Blok:
       - Memotong teks menjadi potongan-potongan blok sepanjang n karakter.
       - Konversi huruf pada setiap blok menjadi vektor angka menggunakan huruf_ke_angka().
       - Perkalian Matriks: Setiap baris matriks K dikalikan dengan vektor angka teks,
         dijumlahkan, lalu dihitung modulo 26.
       - Konversi angka hasil modulo kembali menjadi huruf menggunakan angka_ke_huruf().
       - Gabungkan hasil huruf setiap blok ke dalam variabel ciphertext.
    4. Menampilkan rincian perhitungan per blok dan hasil akhir Ciphertext ke layar.
    """
    n = len(K)
    # Bersihkan teks hanya mengambil alfabet dan kapital
    plaintext_bersih = "".join(h for h in plaintext.upper() if h.isalpha())
    
    print(f"\n--- PROSES ENKRIPSI ---")
    print(f"Plaintext awal  : {plaintext}")
    print(f"Plaintext bersih: {plaintext_bersih}")
    
    # Tambahkan padding 'X' jika panjang teks tidak habis dibagi ukuran matriks n
    while len(plaintext_bersih) % n != 0:
        plaintext_bersih += 'X'
    print(f"Plaintext dengan padding ('X'): {plaintext_bersih}\n")
    
    ciphertext = ""
    block_idx = 1
    # Loop per blok sepanjang n karakter
    for i in range(0, len(plaintext_bersih), n):
        blok_teks = plaintext_bersih[i:i+n]
        print(f"Blok {block_idx} -> \"{blok_teks}\":")
        
        # Konversi karakter blok menjadi vektor angka
        vektor = []
        for char in blok_teks:
            val = huruf_ke_angka(char)
            vektor.append(val)
            print(f"  • {char} -> {val}")
            
        print(f"  Vektor P = {vektor}")
        print("  Perhitungan per baris matriks K:")
        
        # Perkalian baris matriks kunci K dengan vektor kolom teks P
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
            
        # Konversi angka hasil perkalian kembali menjadi karakter huruf
        blok_cipher = "".join(angka_ke_huruf(num) for num in hasil_angka)
        print(f"  Hasil angka: {hasil_angka} -> Huruf Cipher: {blok_cipher}\n")
        ciphertext += blok_cipher
        block_idx += 1
        
    print(f"Ciphertext akhir: {ciphertext}")
    print("-----------------------\n")


def proses_dekripsi(ciphertext, K_inv):
    """
    Fungsi: Melakukan proses dekripsi teks tersandi (Ciphertext) kembali menjadi teks terang (Plaintext)
    menggunakan algoritma Hill Cipher dengan matriks kunci invers K⁻¹.
    
    Rumus Matematis: P = (K⁻¹ · C) mod 26
    
    Alur Kerja:
    1. Pembersihan Teks:
       - Mengambil hanya karakter huruf alfabet kapital dan membuang karakter lain.
    2. Dekripsi Blok demi Blok:
       - Memotong ciphertext menjadi potongan-potongan blok sepanjang n karakter (ukuran ordo K⁻¹).
       - Konversi huruf pada setiap blok menjadi vektor angka menggunakan huruf_ke_angka().
       - Perkalian Matriks: Setiap baris matriks kunci invers K⁻¹ dikalikan dengan vektor angka ciphertext,
         dijumlahkan, lalu dihitung modulo 26.
       - Konversi angka hasil modulo kembali menjadi huruf menggunakan angka_ke_huruf().
       - Gabungkan hasil huruf setiap blok ke dalam variabel plaintext.
    3. Menampilkan rincian perhitungan per blok dan hasil akhir Plaintext ke layar.
    """
    n = len(K_inv)
    # Bersihkan ciphertext hanya mengambil alfabet kapital
    ciphertext_bersih = "".join(h for h in ciphertext.upper() if h.isalpha())
    
    print(f"\n--- PROSES DEKRIPSI ---")
    print(f"Ciphertext awal  : {ciphertext}")
    print(f"Ciphertext bersih: {ciphertext_bersih}\n")
    
    plaintext = ""
    block_idx = 1
    # Loop per blok sepanjang n karakter
    for i in range(0, len(ciphertext_bersih), n):
        blok_teks = ciphertext_bersih[i:i+n]
        print(f"Blok {block_idx} -> Cipher \"{blok_teks}\":")
        
        # Konversi karakter blok menjadi vektor angka
        vektor = []
        for char in blok_teks:
            val = huruf_ke_angka(char)
            vektor.append(val)
            print(f"  • {char} -> {val}")
            
        print(f"  Vektor C = {vektor}")
        print("  Perhitungan per baris matriks K⁻¹:")
        
        # Perkalian baris matriks kunci invers K⁻¹ dengan vektor ciphertext C
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
            
        # Konversi angka hasil perkalian kembali menjadi karakter huruf plaintext
        blok_plain = "".join(angka_ke_huruf(num) for num in hasil_angka)
        print(f"  Hasil angka: {hasil_angka} -> Huruf Plaintext: {blok_plain}\n")
        plaintext += blok_plain
        block_idx += 1
        
    print(f"Plaintext hasil dekripsi: {plaintext}")
    print("------------------------\n")


# ==============================================================================
# 4. FUNGSI UTAMA (MAIN MENU & ENTRY POINT)
# ==============================================================================

def main():
    """
    Fungsi: Titik masuk utama (entry point) program aplikasi Hill Cipher interaktif.
    
    Alur Kerja:
    1. Memulai program dengan memanggil alur_input_kunci_awal() untuk mendapatkan
       matriks kunci K dan matriks invers K⁻¹ yang valid dari pengguna.
    2. Menjalankan perulangan interaktif (while True) yang menampilkan menu utama:
       - Menampilkan status matriks kunci aktif (K) dan inversnya (K⁻¹).
       - Menampilkan 4 pilihan menu:
         1. Enkripsi: Menerima input plaintext lalu memanggil proses_enkripsi().
         2. Dekripsi: Menerima input ciphertext lalu memanggil proses_dekripsi().
         3. Ganti Kunci: Memanggil kembali alur_input_kunci_awal() untuk mengganti kunci aktif.
         4. Keluar: Menghentikan perulangan (break) dan menutup program.
       - Menangani masukan menu yang tidak valid jika pengguna memasukkan selain 1-4.
    """
    # Tahap awal: Input kunci dan hitung inversnya
    kunci, k_inv = alur_input_kunci_awal()
    
    # Perulangan Menu Utama
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
        
        # Pilihan 1: Enkripsi teks
        if pilihan == '1':
            teks = input("\nMasukkan Plaintext: ")
            proses_enkripsi(teks, kunci)
            input("Tekan [Enter] untuk kembali ke Menu Utama...")
            print()
            
        # Pilihan 2: Dekripsi teks
        elif pilihan == '2':
            teks = input("\nMasukkan Ciphertext: ")
            proses_dekripsi(teks, k_inv)
            input("Tekan [Enter] untuk kembali ke Menu Utama...")
            print()
            
        # Pilihan 3: Ganti kunci matriks
        elif pilihan == '3':
            print("\n--- GANTI KUNCI BARU ---")
            kunci, k_inv = alur_input_kunci_awal()
            
        # Pilihan 4: Keluar dari program
        elif pilihan == '4':
            print("\nTerima kasih telah menggunakan program Hill Cipher. Sampai jumpa!")
            break
            
        # Validasi pilihan menu selain 1, 2, 3, 4
        else:
            print("\nPilihan tidak valid! Silakan pilih angka 1, 2, 3, atau 4.\n")


# Titik eksekusi saat file dijalankan langsung melalui perintah terminal/IDE
if __name__ == "__main__":
    main()