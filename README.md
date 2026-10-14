# Project Kripto – Kelompok 3

Proyek mata kuliah Kriptografi yang mengimplementasikan **Hill Cipher**, yaitu cipher substitusi poligrafik berbasis aljabar linear (perkalian matriks modulo 26).

> **Mata Kuliah:** Kriptografi — Teknik Informatika, Universitas Dian Nuswantoro (UDINUS)
> **Kelompok:** 3

---

## Daftar Isi

- [Project Kripto – Kelompok 3](#project-kripto--kelompok-3)
  - [Daftar Isi](#daftar-isi)
  - [Tentang Proyek](#tentang-proyek)
  - [Cara Kerja Hill Cipher](#cara-kerja-hill-cipher)
  - [Fitur](#fitur)
  - [Struktur Proyek](#struktur-proyek)
  - [Memulai](#memulai)
    - [Instalasi](#instalasi)
  - [Cara Penggunaan](#cara-penggunaan)
  - [Contoh](#contoh)
  - [Catatan Keamanan](#catatan-keamanan)
---

## Tentang Proyek

Proyek ini mendemonstrasikan proses enkripsi dan dekripsi menggunakan Hill Cipher dengan matriks kunci berukuran `n × n`. Tujuannya adalah memahami bagaimana aljabar matriks, aritmetika modular, dan invers modular diterapkan pada kriptografi klasik.

## Cara Kerja Hill Cipher

Plaintext dipecah menjadi blok berisi `n` huruf (A=0 ... Z=25). Setiap blok menjadi vektor `P`, dan kunci berupa matriks `K` berukuran `n × n`.

```
Enkripsi:  C = K · P    (mod 26)
Dekripsi:  P = K⁻¹ · C  (mod 26)
```

**Syarat kunci:** `K` harus memiliki invers modulo 26, yaitu `gcd(det(K), 26) = 1`.

Jika panjang teks bukan kelipatan `n`, teks ditambah padding (default: `X`).

## Fitur

- Enkripsi dan dekripsi teks dengan matriks kunci kustom
- Validasi kunci (determinan harus koprima dengan 26)
- Perhitungan invers matriks modular
- Padding(Tambahan) otomatis

## Struktur Proyek

```
Project-Kripto-Kel-3/
├── main.py
├── contoh_Key.txt
└── README.md
```

## Memulai

### Instalasi

```bash
sudo apt install python3 python3-pip python3-venv (install python sesuai OS)
git clone https://github.com/Devjack404/Project-Kripto-Kel-3.git
cd Project-Kripto-Kel-3
```

## Cara Penggunaan

```bash
# python main.py
```

## Contoh

| Item | Nilai |
|---|---|
| Kunci (3×3) | `[[6, 24, 1], [13, 16, 10], [20, 17, 15]]` |
| Plaintext | `ACT` |
| Ciphertext | `POH` |

## Catatan Keamanan

Hill Cipher bersifat **linear**, sehingga rentan terhadap known-plaintext attack: dengan `n` pasang blok plaintext dan ciphertext yang diketahui, penyerang dapat memulihkan kunci melalui `K = C · P⁻¹ (mod 26)`. Matriks kunci yang lebih besar hanya menaikkan biaya serangan, tetapi tidak menghilangkan kelemahan ini. Proyek ini dibuat untuk **tujuan edukasi** dan tidak boleh digunakan untuk melindungi data sungguhan.