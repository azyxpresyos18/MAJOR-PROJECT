/* ============================================================
   Demo-District — main.js
   Full frontend JS: transitions, toasts, modals, validation,
   mobile nav, loading states, auto-refresh
   ============================================================ */

/* ── PAGE FADE TRANSITION ───────────────────────────────────── */
(function () {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.22s ease';
  window.addEventListener('load', () => {
    requestAnimationFrame(() => requestAnimationFrame(() => {
      document.body.style.opacity = '1';
    }));
  });

  function fadeOut(cb) {
    document.body.style.transition = 'opacity 0.18s ease';
    document.body.style.opacity = '0';
    setTimeout(cb, 180);
  }

  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href || href === '#' || /^https?:/.test(href) || href.startsWith('mailto') || a.target === '_blank') return;
    e.preventDefault();
    fadeOut(() => { window.location.href = href; });
  });
})();


/* ── TOAST NOTIFICATIONS ────────────────────────────────────── */
const Toast = (function () {
  let container;

  function getContainer() {
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = `
        position: fixed; bottom: 24px; right: 24px;
        display: flex; flex-direction: column; gap: 10px;
        z-index: 9999; pointer-events: none;
      `;
      document.body.appendChild(container);
    }
    return container;
  }

  function show(message, type = 'success', duration = 3500) {
    const colors = {
      success: { bg: '#D1FAE5', border: '#6EE7B7', text: '#065F46', icon: '✅' },
      error:   { bg: '#FEE2E2', border: '#FCA5A5', text: '#991B1B', icon: '❌' },
      info:    { bg: '#DBEAFE', border: '#93C5FD', text: '#1E40AF', icon: 'ℹ️' },
      warning: { bg: '#FEF3C7', border: '#FCD34D', text: '#92400E', icon: '⚠️' },
    };
    const c = colors[type] || colors.success;

    const toast = document.createElement('div');
    toast.style.cssText = `
      background: ${c.bg}; border: 1.5px solid ${c.border}; color: ${c.text};
      padding: 12px 18px; border-radius: 10px; font-size: 0.88rem; font-weight: 600;
      font-family: 'Barlow Condensed', sans-serif; letter-spacing: 0.5px;
      display: flex; align-items: center; gap: 8px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.12);
      pointer-events: all; cursor: pointer;
      opacity: 0; transform: translateY(10px);
      transition: opacity 0.2s ease, transform 0.2s ease;
      max-width: 320px;
    `;
    toast.innerHTML = `<span>${c.icon}</span><span>${message}</span>`;
    toast.addEventListener('click', () => removeToast(toast));
    getContainer().appendChild(toast);

    requestAnimationFrame(() => requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
    }));

    setTimeout(() => removeToast(toast), duration);
    return toast;
  }

  function removeToast(toast) {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 220);
  }

  return { show };
})();


/* ── CONFIRM MODAL ──────────────────────────────────────────── */
const Modal = (function () {
  function confirm(message, onConfirm, danger = true) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
      position: fixed; inset: 0; background: rgba(0,0,0,0.5);
      z-index: 10000; display: flex; align-items: center; justify-content: center;
      opacity: 0; transition: opacity 0.15s ease;
    `;

    const box = document.createElement('div');
    box.style.cssText = `
      background: #fff; border-radius: 14px; padding: 28px 28px 22px;
      max-width: 360px; width: 90%; box-shadow: 0 16px 48px rgba(0,0,0,0.2);
      transform: scale(0.95); transition: transform 0.15s ease;
      font-family: 'Barlow', sans-serif;
    `;

    const dangerColor = danger ? '#DC2626' : '#1e3a8a';
    box.innerHTML = `
      <div style="font-size:2rem;margin-bottom:12px;">${danger ? '🗑️' : '❓'}</div>
      <div style="font-family:'Oswald',sans-serif;font-size:1.1rem;font-weight:700;letter-spacing:1px;margin-bottom:8px;color:#0f1923;">
        ${danger ? 'CONFIRM DELETE' : 'CONFIRM ACTION'}
      </div>
      <p style="font-size:0.88rem;color:#555;line-height:1.5;margin-bottom:20px;">${message}</p>
      <div style="display:flex;gap:10px;justify-content:flex-end;">
        <button id="modal-cancel" style="
          padding:9px 20px;border:1.5px solid #e4e6ea;border-radius:7px;
          background:#fff;font-family:'Barlow Condensed',sans-serif;
          font-weight:700;font-size:0.9rem;cursor:pointer;">
          Cancel
        </button>
        <button id="modal-confirm" style="
          padding:9px 20px;border:none;border-radius:7px;
          background:${dangerColor};color:#fff;
          font-family:'Barlow Condensed',sans-serif;
          font-weight:700;font-size:0.9rem;cursor:pointer;letter-spacing:0.5px;">
          ${danger ? 'DELETE' : 'CONFIRM'}
        </button>
      </div>
    `;

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    requestAnimationFrame(() => requestAnimationFrame(() => {
      overlay.style.opacity = '1';
      box.style.transform = 'scale(1)';
    }));

    function close() {
      overlay.style.opacity = '0';
      box.style.transform = 'scale(0.95)';
      setTimeout(() => overlay.remove(), 150);
    }

    box.querySelector('#modal-cancel').addEventListener('click', close);
    overlay.addEventListener('click', e => { if (e.target === overlay) close(); });
    box.querySelector('#modal-confirm').addEventListener('click', () => {
      close();
      onConfirm();
    });
  }

  return { confirm };
})();


/* ── LOADING SPINNER ────────────────────────────────────────── */
const Loader = (function () {
  let el;

  function show() {
    el = document.createElement('div');
    el.style.cssText = `
      position: fixed; inset: 0; background: rgba(255,255,255,0.6);
      z-index: 9998; display: flex; align-items: center; justify-content: center;
    `;
    el.innerHTML = `
      <div style="
        width: 42px; height: 42px; border: 4px solid #e4e6ea;
        border-top-color: #F5A800; border-radius: 50%;
        animation: spin 0.7s linear infinite;
      "></div>
    `;
    if (!document.querySelector('#spin-style')) {
      const style = document.createElement('style');
      style.id = 'spin-style';
      style.textContent = '@keyframes spin { to { transform: rotate(360deg); } }';
      document.head.appendChild(style);
    }
    document.body.appendChild(el);
  }

  function hide() {
    if (el) { el.remove(); el = null; }
  }

  return { show, hide };
})();


/* ── MOBILE NAV ─────────────────────────────────────────────── */
(function () {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const nav = header.querySelector('.main-nav');
  if (!nav) return;

  const burger = document.createElement('button');
  burger.innerHTML = '☰';
  burger.setAttribute('aria-label', 'Toggle menu');
  burger.style.cssText = `
    display: none; background: none; border: none;
    font-size: 1.4rem; color: #0f1923; cursor: pointer;
    padding: 4px 8px; border-radius: 6px;
  `;

  header.appendChild(burger);

  const style = document.createElement('style');
  style.textContent = `
    @media (max-width: 768px) {
      .main-nav {
        display: none !important; flex-direction: column;
        position: absolute; top: 62px; left: 0; right: 0;
        background: #F5A800; padding: 12px 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 99;
      }
      .main-nav.open { display: flex !important; }
      .burger-btn { display: block !important; }
    }
  `;
  document.head.appendChild(style);
  burger.classList.add('burger-btn');

  burger.addEventListener('click', () => {
    nav.classList.toggle('open');
  });

  document.addEventListener('click', e => {
    if (!header.contains(e.target)) nav.classList.remove('open');
  });
})();


/* ── AUTO-DISMISS DJANGO MESSAGES ───────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.msg').forEach(msg => {
    const type = msg.classList.contains('msg-error') ? 'error' : 'success';
    Toast.show(msg.textContent.trim(), type);
    msg.remove();
  });
});


/* ── FORM VALIDATION ────────────────────────────────────────── */
(function () {
  document.addEventListener('submit', e => {
    const form = e.target;
    if (!form.dataset.validate) return;

    let valid = true;
    form.querySelectorAll('[required]').forEach(field => {
      field.style.borderColor = '';
      if (!field.value.trim()) {
        field.style.borderColor = '#DC2626';
        field.style.transition = 'border-color 0.2s';
        valid = false;
      }
    });

    if (!valid) {
      e.preventDefault();
      Toast.show('Please fill in all required fields.', 'error');
      form.querySelector('[required]:not([value])') &&
        form.querySelector('[required]').focus();
    }
  });

  // Clear red border on input
  document.addEventListener('input', e => {
    if (e.target.style.borderColor === 'rgb(220, 38, 38)') {
      e.target.style.borderColor = '';
    }
  });
})();


/* ── SCHEDULE STATUS UPDATE (replaces inline JS) ────────────── */
window.cycleStatus = async function (id, current) {
  const ORDER = ['pending', 'confirmed', 'ongoing', 'completed', 'cancelled'];
  const next = ORDER[(ORDER.indexOf(current) + 1) % ORDER.length];
  const labels = { pending:'Pending', confirmed:'Confirmed', ongoing:'Ongoing', completed:'Completed', cancelled:'Cancelled' };

  Loader.show();
  try {
    const res = await fetch(`/api/schedule/${id}/status/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ status: next })
    });
    if (res.ok) {
      Toast.show(`Status updated to ${labels[next]}`, 'success');
      setTimeout(() => location.reload(), 900);
    } else {
      Toast.show('Failed to update status.', 'error');
    }
  } catch {
    Toast.show('Network error. Try again.', 'error');
  } finally {
    Loader.hide();
  }
};


/* ── SCHEDULE DELETE (replaces inline JS) ───────────────────── */
window.delSched = function (id) {
  Modal.confirm(
    'This schedule will be permanently deleted. This cannot be undone.',
    async () => {
      Loader.show();
      try {
        const res = await fetch(`/api/schedule/${id}/delete/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        if (res.ok) {
          const row = document.getElementById(`srow-${id}`) || document.getElementById(`row-${id}`);
          if (row) {
            row.style.transition = 'opacity 0.3s, transform 0.3s';
            row.style.opacity = '0';
            row.style.transform = 'translateX(20px)';
            setTimeout(() => row.remove(), 300);
          }
          Toast.show('Schedule deleted successfully.', 'success');
        } else {
          Toast.show('Failed to delete. Try again.', 'error');
        }
      } catch {
        Toast.show('Network error. Try again.', 'error');
      } finally {
        Loader.hide();
      }
    }
  );
};

/* Keep old name working too */
window.deleteRow = window.delSched;


/* ── SCHEDULE FORM TOGGLE ───────────────────────────────────── */
window.toggleForm = function () {
  const form = document.getElementById('scheduleForm');
  if (!form) return;
  const opening = form.style.display === 'none' || form.style.display === '';
  if (opening) {
    form.style.display = 'block';
    form.style.opacity = '0';
    form.style.transform = 'translateY(-8px)';
    form.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
    requestAnimationFrame(() => requestAnimationFrame(() => {
      form.style.opacity = '1';
      form.style.transform = 'translateY(0)';
    }));
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    form.style.opacity = '0';
    form.style.transform = 'translateY(-8px)';
    setTimeout(() => { form.style.display = 'none'; }, 200);
  }
};


/* ── PRODUCT FILTER BY CLIENT ───────────────────────────────── */
window.filterProducts = function (clientId) {
  const sel = document.getElementById('productSelect');
  if (!sel) return;
  [...sel.options].forEach(o => {
    if (!o.value) return;
    o.style.display = (!clientId || o.dataset.client === clientId) ? '' : 'none';
  });
  sel.value = '';
};


/* ── CHANGE STATUS (departmentalize page) ───────────────────── */
window.changeStatus = window.cycleStatus;


/* ── ACTIVE NAV HIGHLIGHT ───────────────────────────────────── */
(function () {
  const path = window.location.pathname;
  document.querySelectorAll('.main-nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href && path.startsWith(href) && href !== '/') {
      a.classList.add('active');
    }
  });
})();


/* ── UTILITY: get CSRF cookie ───────────────────────────────── */
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : '';
}


/* ── TABLE ROW HOVER EFFECT ─────────────────────────────────── */
(function () {
  document.querySelectorAll('.data-table tbody tr').forEach(row => {
    row.style.transition = 'background 0.12s';
  });
})();


/* ── SUMMARY CARD COUNT-UP ANIMATION ────────────────────────── */
(function () {
  function countUp(el) {
    const target = parseInt(el.textContent, 10);
    if (isNaN(target) || target === 0) return;
    let current = 0;
    const step = Math.ceil(target / 20);
    const interval = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(interval);
    }, 30);
  }

  document.querySelectorAll('.stat-num, .s-num, .summary-num').forEach(el => {
    countUp(el);
  });
})();
