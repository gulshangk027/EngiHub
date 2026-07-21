/* EngiHub — Global JavaScript */

// ── Theme Toggle ──────────────────────────────────────────────
(function () {
  const html  = document.documentElement;
  const btn   = document.getElementById('themeToggle');
  const icon  = document.getElementById('themeIcon');

  const saved = localStorage.getItem('engihub-theme') || 'dark';
  html.setAttribute('data-theme', saved);
  updateIcon(saved);

  if (btn) {
    btn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('engihub-theme', next);
      updateIcon(next);
    });
  }

  function updateIcon(theme) {
    if (!icon) return;
    icon.className = theme === 'dark' ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
  }
})();

// ── Navbar scroll shadow ───────────────────────────────────────
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNav');
  if (!nav) return;
  nav.classList.toggle('scrolled', window.scrollY > 20);
});

// ── Animate module cards on scroll ────────────────────────────
(function () {
  const cards = document.querySelectorAll('.module-card');
  if (!cards.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  cards.forEach(c => obs.observe(c));
})();

// ── Toast helper ──────────────────────────────────────────────
function showToast(msg, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const id   = 'toast-' + Date.now();
  const html = `
    <div id="${id}" class="toast align-items-center text-bg-${type} border-0 show" role="alert">
      <div class="d-flex">
        <div class="toast-body">${msg}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>`;
  container.insertAdjacentHTML('beforeend', html);
  setTimeout(() => document.getElementById(id)?.remove(), 4000);
}
