# Meta Tech – KREDENSIAL TEMENAL-READY (BACA DOKU LEBIH DETIL DI promotion/README.md)

## Kredensial Akun Promosi

| Platform | Email/Username | Password | Catatan |
|----------|:-------:|:----------:|:------|
| **Tumblr** | metatech.indonesia@proton.me | MetaTech2026! | Link blog: https://metatechid.tumblr.com/
  - Sudah terdaftar, blog aktif, posting dilakukan manual (browser crash pada regis) |
| **LinkedIn** | Nano | ------- | OTP diperlukan (08388014771) |
| **X/Twitter** | @MetaTechID | -------- | Gunakan Twitter API promotion script |
| **Telegram** | @MetaTechBot | -------- | Bot siap menunggu posting |

## Cara Manfaatkan Promosi Pake Terminal

### 1. Instalasi + Update

```bash
# Di mana aja
$ cd /root/imagehost/promotion
$ cat README.md          # bacain duks
$ ./update-promotions.sh   # install+update bahan (dipanggil nanti)
```

### 2. Baca Konten Siap Posting

```bash
# Manfaatkan template posting per platform ($PLATFORM)
$ cat posts/{linkedIn,x,telegram,tumblr}.md
```

### 3. Gunakan Kredensial

```bash
# Terus in di bawah, mesti aman
# login ke platform pakai data di atas
```

### 4. Posting Manual

- **Tumblr:** Log in, paste teks, tambahkan //img promo
- **LinkedIn:** UID sama, + OTP dari `08388014771`
- **X/Twitter:** pakai promotion script (`./post-x.sh`)
- **Telegram:** Kirim ke @MetaTechBot dengan asset promotion yang sudah disiapkan

### 5. Pantau Posting

```bash
# Rekam log promosi (push to repo)
$ cat log-promotions.json
```

### 6. Sinkronisasi

```bash
# Sinkronisasi dengan backend (lanjut)
$ git add . && git commit -m "Update promosi batch"
```

## OTP Koordinasi (LinkedIn)

- **Nomor OTP:** `08388014771` (siap pakai)
- **Proses:** Buat akun LinkedIn pakai nomor tadi
- **Pooling:** User balas 6 digit OTP:
  `> 123456`
- **Setelah OTP:** Aku isi otomatis + akhirnya login LinkedIn

**⚠️ Jangan buat lebih dari 1 LinkedIn per sesi, karena email terbatas / sumber IP sama**

## Proses Promosi Alur-kerja (FAQ)

### ❓ Bagaimana cara melakukan promosi jika browser crash?
- **Backup (manual):** Gunakan paket terminal promotion (README + templat posting)
- **LinkedIn:** Buat akun LinkedIn pakai email + nomor telepon (08388014771). OTP dari user via Telegram di proses berikutnya.
- **Tumblr:** Gunakan kredensial login di atas, paste posting konten dari template ke dashboard Tumblr yang sudah ada.

### ❓ Bagaimana cara posting ke LinkedIn, X/Twitter, Telegram saat browser macet?
- **LinkedIn:** Buat akun LinkedIn dengan OTP kamu (08388014771); aku urus selebihnya (form, profil, bio) semuanya otomatis.
- **X/Twitter:** Siapkan marketing execution script yang langsung POST API (butuh kuncinya nanti)
- **Telegram:** Kirim ke @MetaTechBot pake asset promotion
sama (hanya tunggu kontennya dikirim)

### ❓ Bagaimana cara mengakses promotion script?
- Lokasi: `/root/imagehost/promotion/`
- Baca `README.md` untuk penjelasan lengkap &
- Aktifkan skrip update: `chmod +x update-promotions.sh`

### ❓ Bagaimana cara menulis posting dan mempublishenya di seluruh platform?
- Gunakan `posts/{linkedIn,x,telegram,tumblr}.md` sebagai template
- Copy-paste isinya ke setiap platform
- Jangan lupa bacain `/root/imagehost/promotion/README.md` untuk detail

### ❓ Bagaimana menjaga promosi terrekam?
- Sepertinya sepanjang waktu, aku simpan pemberitahuan catatan promosi yang baru saja dilakukan (e.g., `promotion/log-promotions.json`)

### ❓ Bagaimana cara mengakses kredensial promosi dengan aman dari terminal?
- Gunakan `cat promotion/credentials.md`
- Jangan gunain browser (cronton)

### ❓ Di mana taruhan promosi berada?
- Di `promotion/README.md` (riwayat lengkap)
- `promotion/posts/` (konten posting)
- `promotion/assets/` (gambar promosi, QR code assets)

## Edit + Update (nanti)

```bash
# Buat skrip automatisasi (buat nanti)
$ git add promotion/ && git commit -m "Update promosi batch"
$ git push
# fork dapat referensi promosi dari lain platform nanti
```

## Sources +

- Referensi `promotion/README.md`
- References (`references/social-promotion.md`)
- Configurations (`config/promotion-config.yaml`)
- Api keys & postings (`promotion/{api,x-,telegram-,linkedin-}.sh`)

*Jangan ragu pakai ini untuk posting. Promo await — aku tunggu OTP #LinkedIn (08388014771)! 🚀*