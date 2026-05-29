const typeMap = { pdf: 'pdf', docx: 'docx', xlsx: 'xlsx', csv: 'csv', txt: 'txt' };
const iconMap = { pdf: 'ti-file-type-pdf', docx: 'ti-file-type-doc', xlsx: 'ti-file-type-xls', csv: 'ti-table', txt: 'ti-file-text' };
function getExt(n) { return n.split('.').pop().toLowerCase(); }

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 140) + 'px';
}
function updateCount(el) {
    document.getElementById('char-count').textContent = el.value.length + ' / 2000';
}
function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); document.getElementById('query-form').submit(); }
}
function useSuggestion(text) {
    const ta = document.getElementById('query-input');
    ta.value = text; autoResize(ta); updateCount(ta); ta.focus();
}

function togglePanel() {
    document.getElementById('right-panel').classList.toggle('collapsed');
}

function dragOver(e) {
    e.preventDefault();
    document.getElementById('drop-zone').classList.add('drag-over');
}
function dragLeave() {
    document.getElementById('drop-zone').classList.remove('drag-over');
}
function dropFiles(e) {
    e.preventDefault(); dragLeave();
    addToList(e.dataTransfer.files);
}

function addToList(files) {
    const list = document.getElementById('file-list');
    const empty = document.getElementById('empty-files');
    if (empty) empty.remove();
    Array.from(files).forEach(f => {
        const ext = getExt(f.name);
        const t = typeMap[ext] || 'txt';
        const ic = iconMap[t] || 'ti-file';
        const size = f.size > 1048576 ? (f.size / 1048576).toFixed(1) + ' MB' : Math.round(f.size / 1024) + ' KB';
        const div = document.createElement('div');
        div.className = 'f-item';
        div.innerHTML = `
        <div class="f-icon ${t}"><i class="ti ${ic}"></i></div>
        <div class="f-info">
          <div class="f-name">${f.name}</div>
          <div class="f-meta">${size}</div>
        </div>
        <i class="ti ti-trash f-del" onclick="this.closest('.f-item').remove()"></i>
      `;
        list.appendChild(div);
    });
}

function addChips(files) {
    const c = document.getElementById('file-chips');
    Array.from(files).forEach(f => {
        const ext = getExt(f.name);
        const ic = iconMap[typeMap[ext] || 'txt'] || 'ti-file';
        const chip = document.createElement('div');
        chip.className = 'chip';
        chip.innerHTML = `<i class="ti ${ic}"></i>${f.name}<span class="rm" onclick="this.closest('.chip').remove()">✕</span>`;
        c.appendChild(chip);
    });
}

function handleQuerySubmit(e) {
    const val = document.getElementById('query-input').value.trim();
    if (!val) { e.preventDefault(); return; }
    const ca = document.getElementById('chat-area');
    const es = document.getElementById('empty-state');
    if (es) es.style.display = 'none';
    const um = document.createElement('div');
    um.className = 'msg user';
    um.innerHTML = `<div class="msg-avatar user">You</div><div><div class="msg-bubble">${escHtml(val)}</div><div class="msg-meta">Just now</div></div>`;
    ca.appendChild(um);
    const tm = document.createElement('div');
    tm.className = 'msg ai'; tm.id = 'thinking-msg';
    tm.innerHTML = `<div class="msg-avatar ai">SD</div><div class="thinking-dots"><span></span><span></span><span></span></div>`;
    ca.appendChild(tm);
    ca.scrollTop = ca.scrollHeight;
}
function escHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

window.addEventListener('DOMContentLoaded', () => {
    const ca = document.getElementById('chat-area');
    ca.scrollTop = ca.scrollHeight;
});


// login page

function togglePw() {
    const inp = document.getElementById('password');
    const icon = document.getElementById('toggle-pw');
    if (inp.type === 'password') {
        inp.type = 'text';
        icon.classList.replace('ti-eye', 'ti-eye-off');
    } else {
        inp.type = 'password';
        icon.classList.replace('ti-eye-off', 'ti-eye');
    }
}


// signup page


function togglePw() {
    const inp = document.getElementById('password');
    const icon = document.getElementById('toggle-pw');
    if (inp.type === 'password') {
        inp.type = 'text';
        icon.classList.replace('ti-eye', 'ti-eye-off');
    } else {
        inp.type = 'password';
        icon.classList.replace('ti-eye-off', 'ti-eye');
    }
}

function checkStrength(val) {
    const bar = document.getElementById('pw-bar');
    const label = document.getElementById('pw-label');
    if (!val) {
        bar.style.width = '0%'; bar.style.background = 'var(--text3)';
        label.style.color = 'var(--text3)'; label.textContent = 'Enter a password';
        return;
    }
    let score = 0;
    if (val.length >= 8) score++;
    if (/[A-Z]/.test(val)) score++;
    if (/[0-9]/.test(val)) score++;
    if (/[^A-Za-z0-9]/.test(val)) score++;
    const levels = [
        { w: '20%', color: '#f87171', text: 'Weak' },
        { w: '45%', color: '#fbbf24', text: 'Fair' },
        { w: '70%', color: '#60a5fa', text: 'Good' },
        { w: '100%', color: '#4ade80', text: 'Strong' },
    ];
    const l = levels[score - 1] || levels[0];
    bar.style.width = l.w;
    bar.style.background = l.color;
    label.style.color = l.color;
    label.textContent = l.text;
}