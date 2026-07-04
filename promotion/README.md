# Meta Tech — Paket Promosi Terminal-Ready

Paket HTML/files siap pakai untuk posting manual ke platform sosial media dari terminal (Twitter/X, LinkedIn, Telegram, WhatsApp, copy-paste).

## Status Promosi Meta Tech saat ini

| Platform | Status | Kredensial | Catatan |
|----------|:-------:|:----------:|--------|
| Website | ✅ Sudah Live | https://id.methatech.eu.org/ | AI chat + Monetag v3 aktif |
| Tumblr (blog) | ✅ Aktif | metatech.indonesia@proton.me / MetaTech2026! | Lihat https://metatechid.tumblr.com/ |
| LinkedIn | ❌ Menunggu OTP | 08388014771 (backup) | Kirim 6 digit OTP |
| X/Twitter | ⏳ Siap | username: @metatechid | Pakai promotion script |
| Telegram | ⏳ Siap | @MetaTechBot | Pakai promotion script |

## Konten yang bisa disinangkan (copy-paste siap pakai)

### Judul Posting
**🔥 Meta Tech — Premium Video Hosting | Indonesia Bufering**

### Narasi Body (Indonesia)
```
Meta Tech hadir di Indonesia! Platform video hosting premium.

Fitur:
✅ Upload cepat tanpa ribet
✅ Player ringan & responsif  
✅ Gratis & tanpa login
✅ Langsung dapat link share

Lihat demo sekarang:
https://id.methatech.eu.org/

#MetaTech #VideoHosting #IndonesiaBufering
```

### Teks Pendek untuk Twitter/X (280 char)
"🎥 Meta Tech — Upload video cepat & gratis! Ganti platform percayaanmu, pemerasan, dan lag. Mainkan ulang di mana saja dengan AI+Monetag. #MetaTech #Indonesia"

### Teks untuk LinkedIn
"Melihat banyak creator lokal kesulitan upload & streaming video. Saya membangun Meta Tech untuk memberikan video hosting yang bersih, cepat & gratis dengan satu klik: upload → dapatkan link → semua lancar. AI chat + Monetag terintegrasi di situs 🙏\n\n#VideoHosting #StartupIndonesia #Entrepreneur"

### Thumbnail Promosi (dihasilkan via AI)
Semua posting menyertakan gambar hero yang disediakan akun promotion directory (lihat assets/meta-promotion.png).

## Cara Memakai Paket Promosi (via Terminal)

### 1. Persiapan

```bash
# navigation
$ cd /root/imagehost/promotion
$ cat README.md          # lihat konten yang siap diposting
$ ls -la assets/       # assets (gambar + QR)
```

### 2. Terima kredensial sosial media

**Tumblr:** 
- Login: `metatech.indonesia@proton.me`
- Password: `MetaTech2026!`
- Blog URL: `https://metatechid.tumblr.com`

**LinkedIn:** prompt untuk OTP (08388014771)
- OTP masuk? Kirim 6 digit sekarang!

**X/Twitter / Telegram:** bakal dilacak nanti.

### 3. Posting Manual (copy-paste)

#### LinkedIn (di browser)
- Buka https://www.linkedin.com/feed/
- Paste judul & narasi > Post
- Tambahkan assets/meta-promotion.png (drag & drop atau attach)

#### X/Twitter (via terminal dengan `curl`)
```bash
# • install API key setup terlebih dulu (lihat references/x-api.md)
# • salin promotion-templates/x-post.txt
# • paste ke terminal editing
```

#### Telegram (bot)
- Gunakan image & deskripsi yang disediakan di ini.
- Kirim ke @MetaTechBot (prompt nanti).

#### WhatsApp
- Kirim ke grup WA (nomor promosi), paste teks promosi + QR link ke website.

### 4. Simpan Hasil

Copy posting URL setelah setiap platform di `promotion/log.json` untuk tracked.

```json
{
  "tumblr": "https://metatechid.tumblr.com/post/...",
  "linkedin": "...",
  "x": "...",
  "telegram": "...
}
```

## Asset yang dihasilkan

| File | Konten |
|------|:------:|
| assets/meta-promotion.png | Hero promosi (1320x628, logo M, tagline) |
| assets/qr-website.png | QR code yang mengarah ke https://id.methatech.eu.org/ |
| promotion/available-safelinks.json | Tombol cepat (Tanya AI, Monetag, Upload)

![Meta Tech Promotion](/promotion/assets/meta-promotion.png)

## Catatan Cepat saat Posting

- Selalu cantumkan **#MetaTech** & **#IndonesiaBufering**
- Tambahkan link ke AI widget di website di setiap posting
- Gunakan teks propa sosial media campaign hari ini
- Pantau tampilan seluler (responsif)
- Input URL gambar GG --> QR code yang halus

## Pitfalls & Solusi

| Issue | Solusi |
|------|--------|
| UTM link rusak / Google Analytics | Gunakan `/utma=1` di URL (placeholder) |
| Image bukan centang di LinkedIn | Kompres PNG > 200KB, RGBA solid |
| OTP LinkedIn tidak diterima | Kirim ulang ke 08388014771 (Prompt nanti) |

## Licensing

Semua konten promosi adalah kekayaan intelektual Meta Tech. Tidak ada batasan penggunaan di platform sosial media manapun. Tag wajib: Meta Tech, Indonesia Bufering, #MetaTech.

---

*Paket ini selalu up-to-date. Klik `promotion/update-promotions.sh` (nanti) untuk memberi pembaruan.*

---
**Created:** hari ini
**Updated:** selalu
**Brand:** Meta Tech | Indonesia Bufering