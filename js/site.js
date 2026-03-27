'use strict';

/* ============================================================
   1. NAV — transparent → solid on scroll
   ============================================================ */
(function () {
  var nav = document.getElementById('site-nav');
  if (!nav) return;
  function onScroll() { nav.classList.toggle('scrolled', window.scrollY > 40); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}());

/* ============================================================
   2. MOBILE NAV
   ============================================================ */
(function () {
  var btn = document.querySelector('.nav-toggle');
  var mob = document.querySelector('.mobile-nav');
  if (!btn || !mob) return;

  btn.addEventListener('click', function () {
    var open = btn.classList.toggle('open');
    mob.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  mob.addEventListener('click', function (e) {
    if (e.target === mob || e.target.tagName === 'A') {
      btn.classList.remove('open');
      mob.classList.remove('open');
      document.body.style.overflow = '';
    }
  });
}());

/* ============================================================
   3. SCROLL REVEAL (IntersectionObserver)
   ============================================================ */
(function () {
  var els = document.querySelectorAll('.reveal');
  if (!els.length || !window.IntersectionObserver) {
    els.forEach(function (el) { el.classList.add('visible'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  els.forEach(function (el) { io.observe(el); });
}());

/* ============================================================
   4. CATALOG — ACCORDION
   ============================================================ */
(function () {
  document.querySelectorAll('.product-item-header').forEach(function (header) {
    header.addEventListener('click', function () {
      header.closest('.product-item').classList.toggle('open');
    });
  });
}());

/* ============================================================
   5. CATALOG — SEARCH & FILTER
   ============================================================ */
(function () {
  var searchEl = document.getElementById('catalog-search');
  var catBtns  = document.querySelectorAll('.catalog-category-btn');
  var items    = document.querySelectorAll('.product-item[data-category]');
  if (!items.length) return;

  var currentCat = 'all';

  function filter() {
    var q = searchEl ? searchEl.value.toLowerCase().trim() : '';
    items.forEach(function (item) {
      var cat   = item.dataset.category || '';
      var text  = item.textContent.toLowerCase();
      var show  = (currentCat === 'all' || cat === currentCat) && (!q || text.includes(q));
      item.style.display = show ? '' : 'none';
    });
  }

  if (searchEl) searchEl.addEventListener('input', filter);

  catBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      catBtns.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      currentCat = btn.dataset.category || 'all';
      filter();
    });
  });
}());

/* ============================================================
   6. TESTIMONIALS — SCROLL NAV
   ============================================================ */
(function () {
  var track = document.querySelector('.testimonials-track');
  var prev  = document.getElementById('t-prev');
  var next  = document.getElementById('t-next');
  if (!track || !prev || !next) return;

  var cardW = function () {
    var c = track.querySelector('.testimonial-card');
    return c ? c.offsetWidth + 20 : 320;
  };

  prev.addEventListener('click', function () { track.scrollBy({ left: -cardW(), behavior: 'smooth' }); });
  next.addEventListener('click', function () { track.scrollBy({ left:  cardW(), behavior: 'smooth' }); });
}());

/* ============================================================
   7. WHATSAPP FLOATING BUTTON
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelector('.whatsapp-float')) return;
  var phone = '918925883227';
  var msg   = 'Hi Genoasis, I would like to inquire about your water treatment products.';
  var el = document.createElement('div');
  el.className = 'whatsapp-float';
  el.innerHTML = '<a href="https://wa.me/' + phone + '?text=' + encodeURIComponent(msg) + '" target="_blank" rel="noopener" title="Chat on WhatsApp"><i class="fab fa-whatsapp"></i><span>Chat with us</span></a>';
  document.body.appendChild(el);
});

/* ============================================================
   8. CONTACT FORM (Web3Forms)
   ============================================================ */
(function () {
  var form   = document.getElementById('contact-form');
  var status = document.getElementById('form-status');
  if (!form) return;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    var btn = form.querySelector('[type=submit]');
    btn.disabled = true;
    btn.textContent = 'Sending…';
    if (status) { status.className = 'form-status'; }

    try {
      var res  = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: new FormData(form) });
      var data = await res.json();
      if (data.success) {
        if (status) { status.textContent = 'Thank you! We\'ll get back to you shortly.'; status.className = 'form-status form-status--success visible'; }
        form.reset();
      } else { throw new Error(); }
    } catch (_) {
      if (status) { status.textContent = 'Something went wrong. Please email us at info@genoasis.com'; status.className = 'form-status form-status--error visible'; }
    } finally {
      btn.disabled = false;
      btn.textContent = 'Send Message';
    }
  });
}());
