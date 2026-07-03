# Meta Tech Video Hosting

Platform video hosting premium. Built with Flask + Gunicorn.

## Fitur
- Upload & share video tanpa akun
- Preview video player
- Admin panel (hapus video)
- Monetag interstitial ads
- Cloudflare Tunnel

## Setup
```bash
pip install flask gunicorn
cd /root/imagehost
gunicorn -w 4 -b 0.0.0.0:80 app:app
```

## Konfigurasi
- `ADMIN_KEY` — password admin (default: admin123%)
- `SECRET_KEY` — session signing key

## Lisensi
MIT
