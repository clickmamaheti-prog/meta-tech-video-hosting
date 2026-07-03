import os
import uuid
import secrets
from flask import Flask, request, render_template, url_for, send_from_directory, jsonify, session, redirect
from werkzeug.middleware.proxy_fix import ProxyFix

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

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum is 500MB.'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
