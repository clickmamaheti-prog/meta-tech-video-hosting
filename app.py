import os
import uuid
import secrets
import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template, url_for, send_from_directory, jsonify, session, redirect
from werkzeug.middleware.proxy_fix import ProxyFix

# Load .env file
load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

# Admin config
ADMIN_KEY = os.environ.get('ADMIN_KEY', 'Kosay378%')
app.secret_key = os.environ.get('SECRET_KEY', 'meta-tech-secret-key-2026-fixed-v1')

ALLOWED_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.3gp', '.ogv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Allowed: mp4, webm, mov, avi, mkv, flv, wmv, m4v, 3gp, ogv'}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    unique_name = str(uuid.uuid4()) + ext
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(filepath)

    file_size = os.path.getsize(filepath)
    video_url = url_for('view_video', filename=unique_name, _external=True)
    direct_url = url_for('static', filename=f'uploads/{unique_name}', _external=True)

    return jsonify({
        'success': True,
        'url': video_url,
        'direct_url': direct_url,
        'filename': unique_name,
        'size': format_size(file_size)
    })

@app.route('/v/<filename>')
def view_video(filename):
    safe_name = os.path.basename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
    if not os.path.exists(filepath):
        return render_template('404.html'), 404
    
    file_size = os.path.getsize(filepath)
    ext = os.path.splitext(safe_name)[1].lower()
    mime_map = {
        '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo', '.mkv': 'video/x-matroska', '.flv': 'video/x-flv',
        '.wmv': 'video/x-ms-wmv', '.m4v': 'video/mp4', '.3gp': 'video/3gpp',
        '.ogv': 'video/ogg'
    }

    return render_template('view.html',
        filename=safe_name,
        video_url=url_for('static', filename=f'uploads/{safe_name}', _external=True),
        page_url=url_for('view_video', filename=safe_name, _external=True),
        file_size=format_size(file_size),
        file_type=ext[1:].upper(),
        mime_type=mime_map.get(ext, 'video/mp4')
    )

@app.route('/dl/<filename>')
def download(filename):
    safe_name = os.path.basename(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_name, as_attachment=True)

@app.route('/recent')
def recent():
    files = []
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], f)
        if os.path.isfile(fpath):
            files.append({
                'filename': f,
                'size': os.path.getsize(fpath),
                'mtime': os.path.getmtime(fpath)
            })
    files.sort(key=lambda x: x['mtime'], reverse=True)
    files = files[:50]
    return render_template('recent.html', files=files)

@app.context_processor
def inject_is_admin():
    return {'is_admin': session.get('is_admin', False)}

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_KEY:
            session['is_admin'] = True
            return redirect(request.form.get('next', url_for('recent')))
        return render_template('admin.html', error='Wrong password')
    return render_template('admin.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_video(filename):
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    safe_name = os.path.basename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    os.remove(filepath)
    return jsonify({'success': True, 'message': 'Video deleted'})

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/abuse', methods=['GET', 'POST'])
def abuse():
    submitted = False
    if request.method == 'POST':
        # Log the report
        report_type = request.form.get('type', '')
        content_url = request.form.get('content_url', '')
        description = request.form.get('description', '')
        reporter_name = request.form.get('name', '')
        reporter_email = request.form.get('email', '')
        print(f"[ABUSE REPORT] Type: {report_type} | URL: {content_url} | From: {reporter_name} <{reporter_email}>")
        submitted = True
    return render_template('abuse.html', submitted=submitted)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    submitted = False
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')
        print(f"[CONTACT] From: {name} <{email}> | Subject: {subject} | Message: {message}")
        submitted = True
    return render_template('contact.html', submitted=submitted)

# Initialize Opencode client
def _get_opencode():
    api_key = os.getenv('OPENCODE_API_KEY', 'sk-nRt...WXCQ')
    base_url = os.getenv('OPENCODE_BASE_URL', 'https://opencode.ai/zen/v1')
    return {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}, base_url

_opencode_headers, _opencode_base_url = _get_opencode()

def call_opencode(prompt: str) -> str:
    """Kirim prompt ke Opencode API dan kembalikan jawaban."""
    url = f"{_opencode_base_url}/chat/completions"
    payload = {
        "model": "deepseek-v4-flash-free",
        "messages": [
            {"role": "system", "content": "Kamu adalah asisten AI Meta Tech — platform video hosting GRATIS Indonesia (tagline: Indonesia Bufering). BUKAN Meta/Facebook/Instagram. Jawab SINGKAT, bahasa Indonesia, hanya soal Meta Tech: upload video max 500MB (MP4, WebM, MOV, dll), tanpa akun, dapat link share langsung, gratis selamanya, iklan interstisial sekali per sesi. Jika di luar topik Meta Tech, jawab singkat 'Maaf, aku hanya bisa bantu soal Meta Tech video hosting.'"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.4
    }
    response = requests.post(url, headers=_opencode_headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    msg = result['choices'][0]['message']
    # Handle reasoning models: use reasoning_content if content is empty
    content = msg.get('content', '').strip()
    reasoning = msg.get('reasoning_content', '').strip()
    if not content and reasoning:
        return reasoning
    return content

# AI Chat Assistant - Knowledge base
AI_KNOWLEDGE = {
    'upload': '📤 **Cara Upload Video:**\n\n1. Klik area upload atau tombol "Upload Video"\n2. Pilih video dari komputer (max 500MB)\n3. Tunggu proses upload selesai\n4. Copy link dan bagikan!\n\nFormat: MP4, WebM, MOV, AVI, MKV, FLV, WMV.',
    'limit': '📦 **Batas Upload:**\nMaksimal **500MB** per file. Format: MP4, WebM, MOV, AVI, MKV, FLV, WMV, M4V, 3GP, OGV.',
    'free': '💰 **Meta Tech GRATIS!**\nTidak ada biaya upload, download, atau streaming. Layanan tetap gratis selama ada dukungan pengunjung.',
    'about': '💡 **Apa itu Meta Tech?**\nPlatform video hosting gratis — Indonesia Bufering. Upload, share, dan streaming video dengan mudah. Tanpa akun, langsung dapat link.',
    'share': '🔗 **Bagikan Video:**\nSetelah upload, copy link "Share Link" atau "Direct Link" dan bagikan ke teman/grup/media sosial.',
    'download': '⬇️ **Download Video:**\nBuka halaman video, klik tombol "Download" untuk mengunduh.',
    'contact': '📧 **Hubungi Kami:**\nBuka halaman Contact di footer website atau kirim laporan lewat Report Abuse.',
    'privacy': '🔒 **Privasi & Keamanan:**\nVideo hanya bisa diakses lewat link unik. Kami tidak membagikan data pengguna.',
    'mobile': '📱 **Mobile Friendly:**\nMeta Tech bisa diakses dari HP/tablet. Upload langsung dari galeri atau file manager.',
    'delete': '🗑️ **Hapus Video:**\nHanya admin yang bisa menghapus. Laporkan konten tidak pantas lewat Report Abuse.',
    'browse': '🔍 **Cari Video:**\nKlik "Browse" di header untuk melihat video terbaru yang sudah diupload.',
    'account': '🔑 **Tanpa Akun!**\nMeta Tech tidak pakai sistem akun. Upload langsung dapat link — tidak perlu daftar atau login.',
    'ads': '📢 **Iklan:**\nMeta Tech menggunakan iklan interstisial sekali per sesi untuk mendukung layanan gratis.',
    'speed': '⚡ **Streaming:**\nKecepatan tergantung koneksi internet. Gunakan WiFi/data stabil untuk hasil terbaik.',
}

AI_FALLBACKS = [
    'Hmm, aku belum tahu jawabannya. Coba tanya dengan kata kunci lain, atau hubungi Contact di footer!',
    'Maaf, belum paham. Coba ulangi dengan kalimat berbeda ya!',
    'Wah, belum ada di pengetahuanku. Coba tanya: cara upload, batas file, atau tentang Meta Tech.',
]

def ai_find_answer(query):
    q = query.lower().strip()
    # Map keywords to knowledge keys
    kw_map = {
        'upload': ['upload', 'cara upload', 'unggah', 'video'],
        'limit': ['limit', 'max', 'ukuran', 'size', 'besar', '500mb', '500 mb', 'batas'],
        'free': ['gratis', 'free', 'bayar', 'harga', 'biaya', 'cost', 'price'],
        'about': ['meta tech', 'meta', 'tentang', 'about', 'apa itu', 'fungsi', 'kegunaan', 'ini apa'],
        'share': ['link', 'share', 'bagikan', 'copy link', 'teman', 'url'],
        'download': ['download', 'unduh', 'save', 'simpan', 'download video'],
        'contact': ['kontak', 'contact', 'email', 'bantuan', 'help', 'support', 'hubungi'],
        'privacy': ['privasi', 'privacy', 'data', 'aman', 'security', 'keamanan'],
        'mobile': ['hp', 'mobile', 'android', 'iphone', 'ios', 'handphone'],
        'delete': ['hapus', 'delete', 'remove', 'ilang'],
        'browse': ['browse', 'cari', 'search', 'recent', 'video lain', 'banyak'],
        'account': ['daftar', 'register', 'sign up', 'login', 'akun', 'account'],
        'ads': ['iklan', 'ad', 'ads', 'monetag', 'redirect'],
        'speed': ['lambat', 'cepat', 'speed', 'buffering', 'streaming', 'kecepatan'],
    }
    for key, keywords in kw_map.items():
        for kw in keywords:
            if kw in q or q in kw:
                return AI_KNOWLEDGE.get(key)
    return None

@app.route('/api/chat', methods=['POST'])
def ai_chat():
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({'error': 'No message'}), 400
    message = data['message'].strip()
    if not message:
        return jsonify({'error': 'Empty message'}), 400

    # Try Opencode first, fallback to local knowledge base
    try:
        answer = call_opencode(message)
    except Exception as e:
        # Fallback to AI knowledge base
        answer = ai_find_answer(message)
        if not answer:
            import random
            answer = random.choice(AI_FALLBACKS)

    return jsonify({
        'answer': answer,
        'session_id': data.get('session_id', str(uuid.uuid4()))
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum is 500MB.'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
