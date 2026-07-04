/**
 * Meta Tech AI Assistant Widget
 * Floating chat widget with AI-powered Q&A
 */
(function() {
  'use strict';

  let isOpen = false;
  let sessionId = null;
  let messageCount = 0;

  // Knowledge base for common questions
  const knowledgeBase = [
    { keywords: ['upload', 'cara upload', 'upload video', 'how to upload'], answer: '📤 **Cara Upload Video:**\n\n1. Klik area upload atau tombol "Upload Video"\n2. Pilih video dari komputer (max 500MB)\n3. Tunggu proses upload selesai\n4. Copy link dan bagikan!\n\nFormat: MP4, WebM, MOV, AVI, MKV, FLV, WMV' },
    { keywords: ['max', 'ukuran', 'size', 'limit', 'besar', '500'], answer: '📦 **Batas Upload:**\nMaksimal **500MB** per file. Format video yang didukung: MP4, WebM, MOV, AVI, MKV, FLV, WMV, M4V, 3GP, OGV.' },
    { keywords: ['gratis', 'free', 'free', 'bayar', 'harga', 'biaya', 'price', 'cost', 'premium'], answer: '💰 **Meta Tech GRATIS!**\nLayanan video hosting ini gratis untuk semua pengguna. Tidak ada biaya upload, download, atau streaming. Tetap gratis selama ada dukungan pengunjung.' },
    { keywords: ['link', 'share', 'bagikan', 'share link', 'copy link', 'teman'], answer: '🔗 **Bagikan Video:**\nSetelah upload, kamu akan langsung dapat link. Copy link "Share Link" atau "Direct Link" dan bagikan ke teman, grup, atau media sosial.' },
    { keywords: ['download', 'unduh', 'save', 'simpan'], answer: '⬇️ **Download Video:**\nBuka halaman video, klik tombol "Download". Video akan terunduh langsung.' },
    { keywords: ['hapus', 'delete', 'remove', 'ilang'], answer: '🗑️ **Hapus Video:**\nHanya admin yang bisa menghapus video. Jika ada konten tidak pantas, laporkan lewat halaman Report Abuse.' },
    { keywords: ['kontak', 'contact', 'email', 'hubungi', 'bantuan', 'help', 'support'], answer: '📧 **Hubungi Kami:**\nBuka halaman Contact di footer website untuk mengirim pesan. Tersedia juga Report Abuse untuk laporan konten.' },
    { keywords: ['privasi', 'privacy', 'data', 'aman', 'security', 'keamanan'], answer: '🔒 **Privasi & Keamanan:**\nVideo yang kamu upload hanya bisa diakses lewat link unik. Kami tidak membagikan data pengguna. Baca kebijakan privasi di footer website.' },
    { keywords: ['lama', 'duration', 'lama upload', 'lama proses'], answer: '⏱️ **Lama Upload:**\nTergantung ukuran file dan kecepatan internet kamu. Koneksi stabil disarankan untuk file besar (100MB+).' },
    { keywords: ['salah', 'error', 'gagal', 'fail', 'failed', 'not working', 'tidak bisa', 'masalah'], answer: '❌ **Troubleshooting:**\nPastikan: (1) Format video didukung, (2) Ukuran file di bawah 500MB, (3) Koneksi internet stabil. Coba refresh halaman dan upload ulang. Jika masih bermasalah, hubungi Contact.' },
    { keywords: ['browser', 'hp', 'mobile', 'android', 'iphone', 'ios', 'handphone'], answer: '📱 **Mobile Friendly:**\nMeta Tech bisa diakses dari HP/tablet. Upload langsung dari galeri atau file manager.' },
    { keywords: ['meta tech', 'meta', 'tentang', 'about', 'apa itu', 'fungsi', 'kegunaan'], answer: '💡 **Apa itu Meta Tech?**\nMeta Tech adalah platform video hosting gratis — Indonesia Bufering. Upload, share, dan streaming video dengan mudah. Tanpa akun, tanpa ribet, langsung dapat link.' },
    { keywords: ['banyak', 'banyak video', 'cari', 'search', 'video lain', 'recent', 'browse'], answer: '🔍 **Cari Video:**\nKlik "Browse" di header untuk melihat video terbaru yang sudah diupload.' },
    { keywords: ['daftar', 'register', 'sign up', 'login', 'akun', 'account'], answer: '🔑 **Tanpa Akun!**\nMeta Tech tidak pakai sistem akun. Upload langsung dapat link — tidak perlu daftar atau login.' },
    { keywords: ['404', 'not found', 'hilang', 'tidak ada'], answer: '🔗 **Link Tidak Aktif?**\nMungkin video sudah dihapus oleh admin karena melanggar aturan. Gunakan Report Abuse jika perlu.' },
    { keywords: ['monetag', 'iklan', 'ad', 'redirect', 'ads', 'interstitial'], answer: '📢 **Iklan:**\nMeta Tech menggunakan iklan interstisial untuk mendukung layanan gratis. Setiap pengunjung baru akan diarahkan ke iklan satu kali per sesi. Dukunganmu membantu layanan tetap gratis!' },
    { keywords: ['kecepatan', 'cepat', 'lambat', 'slow', 'speed', 'buffering', 'streaming'], answer: '⚡ **Streaming:**\nKecepatan streaming tergantung koneksi internet. Untuk pengalaman terbaik, gunakan koneksi WiFi/data stabil.' },
  ];

  function createWidget() {
    const container = document.createElement('div');
    container.id = 'aiWidgetContainer';
    container.innerHTML = `
      <style>
        @media (max-width: 480px) {
          #aiWidgetContainer .ai-widget-trigger { bottom: 16px; right: 16px; padding: 10px 16px; }
          #aiWidgetContainer .ai-widget-panel { bottom: 72px; right: 12px; left: 12px; width: auto; height: 60vh; }
        }
      </style>
      <div class="ai-widget-trigger" id="aiWidgetTrigger" role="button" tabindex="0" aria-label="Tanya AI Assistant">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          <line x1="9" y1="10" x2="15" y2="10"/>
          <line x1="12" y1="7" x2="12" y2="13"/>
        </svg>
        <span>Tanya AI</span>
      </div>

      <div class="ai-widget-panel" id="aiWidgetPanel">
        <div class="ai-widget-header">
          <div class="ai-widget-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2a4 4 0 0 1 4 4v2a4 4 0 0 1-8 0V6a4 4 0 0 1 4-4z"/>
              <path d="M5 17v-1a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v1"/>
              <circle cx="12" cy="6" r="4"/>
            </svg>
          </div>
          <div class="ai-widget-header-info">
            <h3>Meta Tech AI</h3>
            <p>Online — Siap bantu kamu</p>
          </div>
          <button class="ai-widget-close" id="aiWidgetClose" aria-label="Tutup">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="ai-widget-messages" id="aiMessages">
          <div class="ai-msg bot">
            <div class="msg-content">👋 Halo! Aku asisten AI Meta Tech. Tanya apa aja tentang platform ini ya!</div>
            <div class="msg-time">Sekarang</div>
          </div>
        </div>

        <div class="ai-quick-replies" id="aiQuickReplies">
          <button class="ai-quick-chip" data-msg="Cara upload video">📤 Upload</button>
          <button class="ai-quick-chip" data-msg="Apa itu Meta Tech?">💡 Tentang</button>
          <button class="ai-quick-chip" data-msg="Batas ukuran file">📦 Limit</button>
          <button class="ai-quick-chip" data-msg="Gratis atau bayar?">💰 Gratis</button>
        </div>

        <div class="ai-widget-input">
          <input type="text" id="aiChatInput" placeholder="Ketik pesan..." maxlength="500" autocomplete="off">
          <button id="aiSendBtn" aria-label="Kirim">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>

        <div class="ai-widget-footer">
          <span>Powered by Meta Tech AI</span>
        </div>
      </div>
    `;
    document.body.appendChild(container);
    bindEvents();
  }

  function bindEvents() {
    const trigger = document.getElementById('aiWidgetTrigger');
    const panel = document.getElementById('aiWidgetPanel');
    const closeBtn = document.getElementById('aiWidgetClose');
    const input = document.getElementById('aiChatInput');
    const sendBtn = document.getElementById('aiSendBtn');
    const messages = document.getElementById('aiMessages');
    const chips = document.querySelectorAll('.ai-quick-chip');

    trigger.addEventListener('click', togglePanel);
    trigger.addEventListener('keydown', function(e) { if (e.key === 'Enter') togglePanel(); });
    closeBtn.addEventListener('click', closePanel);
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    input.addEventListener('input', function() {
      sendBtn.disabled = !this.value.trim();
    });

    chips.forEach(function(chip) {
      chip.addEventListener('click', function() {
        input.value = this.getAttribute('data-msg');
        sendMessage();
      });
    });
  }

  function togglePanel() {
    if (isOpen) closePanel();
    else openPanel();
  }

  function openPanel() {
    isOpen = true;
    const panel = document.getElementById('aiWidgetPanel');
    panel.classList.add('open');
    document.getElementById('aiChatInput').focus();
    scrollToBottom();
  }

  function closePanel() {
    isOpen = false;
    document.getElementById('aiWidgetPanel').classList.remove('open');
  }

  function scrollToBottom() {
    const msgs = document.getElementById('aiMessages');
    msgs.scrollTop = msgs.scrollHeight;
  }

  function addMessage(text, isUser) {
    const msgs = document.getElementById('aiMessages');
    const now = new Date();
    const time = now.getHours().toString().padStart(2,'0') + ':' + now.getMinutes().toString().padStart(2,'0');
    const div = document.createElement('div');
    div.className = 'ai-msg ' + (isUser ? 'user' : 'bot');
    div.innerHTML = '<div class="msg-content">' + text + '</div><div class="msg-time">' + time + '</div>';
    msgs.appendChild(div);
    messageCount++;
    scrollToBottom();
  }

  function showTyping() {
    const msgs = document.getElementById('aiMessages');
    const div = document.createElement('div');
    div.className = 'ai-msg bot typing';
    div.id = 'typingIndicator';
    div.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    msgs.appendChild(div);
    scrollToBottom();
  }

  function hideTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
  }

  function findAnswer(query) {
    const q = query.toLowerCase().trim();
    // Check knowledge base
    for (const item of knowledgeBase) {
      for (const kw of item.keywords) {
        if (q.includes(kw) || kw.includes(q)) {
          return item.answer;
        }
      }
    }
    return null;
  }

  function getFallbackAnswer() {
    const fallbacks = [
      'Hmm, aku belum tahu jawabannya. Coba tanya dengan kata kunci lain ya! Atau bisa cek halaman Contact untuk bantuan lebih lanjut.',
      'Maaf, aku belum paham pertanyaannya. Coba ulangi dengan kalimat yang berbeda, atau langsung hubungi kami lewat Contact di footer.',
      'Wah, belum ada di pengetahuanku nih. Coba tanya yang lain! Contoh: cara upload, batas file, atau link share.',
    ];
    return fallbacks[Math.floor(Math.random() * fallbacks.length)];
  }

  function processMessage(userMsg) {
    const answer = findAnswer(userMsg);
    if (answer) return answer;
    return getFallbackAnswer();
  }

  async function sendMessage() {
    const input = document.getElementById('aiChatInput');
    const sendBtn = document.getElementById('aiSendBtn');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    sendBtn.disabled = true;
    addMessage(escapeHtml(text), true);
    showTyping();

    // Try API first, fallback to local
    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId })
      });
      const data = await resp.json();
      hideTyping();
      if (data.answer) {
        sessionId = data.session_id;
        addMessage(data.answer, false);
      } else {
        addMessage(processMessage(text), false);
      }
    } catch (e) {
      hideTyping();
      addMessage(processMessage(text), false);
    }

    sendBtn.disabled = false;
    document.getElementById('aiChatInput').focus();
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }
})();
