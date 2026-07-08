const currentYear = document.querySelector("#current-year");

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

document.documentElement.classList.add("fw-js");

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function tagSpHeroEnters() {
  document.querySelectorAll(".sp-hero .container").forEach((container) => {
    const eyebrow = container.querySelector(".eyebrow");
    const h1 = container.querySelector("h1");
    const lead = container.querySelector("p:not(.eyebrow)");
    if (eyebrow && !eyebrow.hasAttribute("data-fw-enter")) {
      eyebrow.setAttribute("data-fw-enter", "left");
      eyebrow.setAttribute("data-fw-enter-immediate", "true");
    }
    if (h1 && !h1.hasAttribute("data-fw-enter")) {
      h1.setAttribute("data-fw-enter", "left");
      h1.setAttribute("data-fw-enter-immediate", "true");
      h1.style.setProperty("--fw-enter-delay", "80ms");
    }
    if (lead && !lead.hasAttribute("data-fw-enter")) {
      lead.setAttribute("data-fw-enter", "left");
      lead.setAttribute("data-fw-enter-immediate", "true");
      lead.style.setProperty("--fw-enter-delay", "160ms");
    }
  });
}

function initEnterAnimations() {
  tagSpHeroEnters();
  const items = document.querySelectorAll("[data-fw-enter]");
  if (prefersReducedMotion()) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  document.querySelectorAll('[data-fw-enter-immediate="true"]').forEach((el) => {
    el.classList.add("is-visible");
  });
  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        activeObserver.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -10% 0px", threshold: 0.12 },
  );
  document
    .querySelectorAll('[data-fw-enter]:not([data-fw-enter-immediate="true"]):not(.is-visible)')
    .forEach((el) => observer.observe(el));
}

initEnterAnimations();

(function initContactCutout() {
  const section = document.querySelector(".contact-section");
  if (!section || !section.querySelector(".contact-cutout")) return;

  if (prefersReducedMotion()) {
    section.classList.add("contact-ready");
    return;
  }

  if (!("IntersectionObserver" in window)) {
    section.classList.add("contact-ready");
    return;
  }

  const observer = new IntersectionObserver(
    (entries, activeObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        section.classList.add("contact-ready");
        activeObserver.unobserve(section);
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
  );
  observer.observe(section);
})();

// ---- Formspree AJAX submission ----
function currentUtmParams() {
  const params = new URLSearchParams(window.location.search);
  const keys = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];
  return keys.reduce((acc, key) => {
    acc[key] = params.get(key) || "";
    return acc;
  }, {});
}

function setHiddenValue(form, name, value) {
  const field = form.querySelector(`input[type="hidden"][name="${name}"]`);
  if (field) field.value = value || "";
}

function populateLeadAttribution(form) {
  const utms = currentUtmParams();
  setHiddenValue(form, "page_url", window.location.href);
  setHiddenValue(form, "page_title", document.title);
  setHiddenValue(form, "referrer", document.referrer);
  Object.entries(utms).forEach(([key, value]) => setHiddenValue(form, key, value));
}

function trackConversionEvent(eventName, params = {}) {
  if (typeof gtag !== "function") return;
  gtag("event", eventName, {
    page_location: window.location.href,
    page_title: document.title,
    ...params,
  });
}

function validateEstimateForm(form) {
  const gotcha = form.querySelector('input[name="_gotcha"]');
  if (gotcha && gotcha.value.trim()) {
    return "bot";
  }

  form.querySelectorAll("input:not([type='hidden']), textarea, select").forEach((field) => {
    if (typeof field.value === "string") {
      field.value = field.value.trim();
    }
    field.setCustomValidity("");
  });

  const name = form.querySelector('input[name="name"]');
  if (name && name.value.length < 2) {
    name.setCustomValidity("Please enter your name.");
    name.reportValidity();
    return false;
  }

  const phone = form.querySelector('input[name="phone"]');
  if (phone) {
    const digits = phone.value.replace(/\D/g, "");
    if (digits.length < 10) {
      phone.setCustomValidity("Please enter a valid 10-digit phone number.");
      phone.reportValidity();
      return false;
    }
  }

  const service = form.querySelector('select[name="service"]');
  if (service && !service.value.trim()) {
    service.setCustomValidity("Please select a service.");
    service.reportValidity();
    return false;
  }

  const message = form.querySelector('textarea[name="message"]');
  if (message && message.value.length < 5) {
    message.setCustomValidity("Please describe what you need (at least a few words).");
    message.reportValidity();
    return false;
  }

  if (!form.checkValidity()) {
    form.reportValidity();
    return false;
  }

  return true;
}

function bindEstimateForm(form) {
  if (!form || form.dataset.bound === "true") return;
  if (form.dataset.formMode === "email" || form.action.startsWith("mailto:")) return;
  // FormSubmit uses a normal browser POST so the first submission can trigger activation email delivery.
  if (form.dataset.formMode === "formsubmit") return;
  const success =
    document.getElementById(`${form.id}-success`) ||
    form.parentElement.querySelector(".form-success");
  if (!success) return;

  form.dataset.bound = "true";
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const validation = validateEstimateForm(form);
    if (validation === "bot") {
      form.hidden = true;
      success.hidden = false;
      return;
    }
    if (!validation) return;

    const submitBtn = form.querySelector("[type='submit']");
    const originalText = submitBtn.textContent;

    populateLeadAttribution(form);
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });

      let data = null;
      try {
        data = await res.json();
      } catch {
        data = null;
      }

      if (res.ok) {
        submitBtn.textContent = "Sent!";
        trackConversionEvent("generate_lead", {
          event_category: "form",
          event_label: form.id || "estimate_form",
          form_id: form.id || "",
          service: (form.querySelector('[name="service"]') && form.querySelector('[name="service"]').value) || "",
          form_page: (form.querySelector('[name="page"]') && form.querySelector('[name="page"]').value) || "",
        });
        setTimeout(() => {
          form.hidden = true;
          success.hidden = false;
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        }, 1800);
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        const msg =
          (data && (data.error || data.message)) ||
          "Something went wrong. Please email tyler@faithworksclearing.com directly.";
        alert(msg);
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      alert("Could not send. Please email tyler@faithworksclearing.com directly.");
    }
  });
}

document.querySelectorAll(".contact-form").forEach(bindEstimateForm);

document.querySelectorAll('a[href^="tel:"]').forEach((link) => {
  link.addEventListener("click", () => {
    trackConversionEvent("phone_click", {
      event_category: "contact",
      event_label: link.getAttribute("href"),
      link_text: link.textContent.trim().replace(/\s+/g, " "),
      cta_location: link.closest("header")
        ? "header"
        : link.closest("footer")
          ? "footer"
          : link.closest("aside")
            ? "sidebar"
            : "body",
    });
  });
});

// ---- Nav mega menus (desktop flyout + mobile accordion) ----
(function initNavMegaMenus() {
  function closeDesktopBranches(menu, except) {
    if (!menu) return;
    menu.querySelectorAll(".fw-services-mega__item--branch.subnav-open").forEach((item) => {
      if (item === except) return;
      item.classList.remove("subnav-open");
      const btn = item.querySelector(".subnav-toggle");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  function closeAllDesktopDropdowns(exceptWrap) {
    document.querySelectorAll(".nav-dropdown-wrap").forEach((wrap) => {
      if (wrap === exceptWrap) return;
      const dropdownBtn = wrap.querySelector(".nav-dropdown-btn");
      const dropdownMenu = wrap.querySelector(".nav-dropdown-menu");
      if (dropdownBtn) dropdownBtn.setAttribute("aria-expanded", "false");
      closeDesktopBranches(dropdownMenu);
    });
  }

  document.querySelectorAll(".nav-dropdown-wrap").forEach((wrap) => {
    const dropdownBtn = wrap.querySelector(".nav-dropdown-btn");
    const dropdownMenu = wrap.querySelector(".nav-dropdown-menu");
    if (!dropdownBtn || !dropdownMenu) return;

    dropdownMenu.querySelectorAll(".fw-services-mega__item--branch .subnav-toggle").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const item = btn.closest(".fw-services-mega__item--branch");
        if (!item) return;
        const opening = !item.classList.contains("subnav-open");
        closeDesktopBranches(dropdownMenu, opening ? item : null);
        item.classList.toggle("subnav-open", opening);
        btn.setAttribute("aria-expanded", String(opening));
      });
    });

    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const expanded = dropdownBtn.getAttribute("aria-expanded") === "true";
      closeAllDesktopDropdowns(expanded ? wrap : null);
      dropdownBtn.setAttribute("aria-expanded", String(!expanded));
      if (expanded) closeDesktopBranches(dropdownMenu);
    });

    dropdownMenu.addEventListener("click", (e) => e.stopPropagation());
  });

  document.addEventListener("click", () => {
    closeAllDesktopDropdowns();
    document.querySelectorAll(".nav-dropdown-wrap .nav-dropdown-btn").forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
    });
  });

  function resetMobileBranches() {
    document.querySelectorAll(".fw-mm-item--branch.fw-mm-item--open").forEach((item) => {
      item.classList.remove("fw-mm-item--open");
      const btn = item.querySelector(".fw-mm-trigger");
      const submenu = item.querySelector(".fw-mm-submenu");
      if (btn) btn.setAttribute("aria-expanded", "false");
      if (submenu) submenu.hidden = true;
    });
  }

  document.querySelectorAll(".fw-mm-item--branch > .fw-mm-trigger").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const item = btn.closest(".fw-mm-item--branch");
      const submenu = document.getElementById(btn.getAttribute("aria-controls"));
      if (!item) return;
      const opening = !item.classList.contains("fw-mm-item--open");
      const parent = item.parentElement;
      if (parent) {
        parent.querySelectorAll(":scope > .fw-mm-item--branch.fw-mm-item--open").forEach((other) => {
          if (other === item) return;
          other.classList.remove("fw-mm-item--open");
          const otherBtn = other.querySelector(".fw-mm-trigger");
          const otherSub = other.querySelector(".fw-mm-submenu");
          if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
          if (otherSub) otherSub.hidden = true;
        });
      }
      item.classList.toggle("fw-mm-item--open", opening);
      btn.setAttribute("aria-expanded", String(opening));
      if (submenu) submenu.hidden = !opening;
    });
  });

  window.resetFaithWorksMobileSubmenus = resetMobileBranches;
})();

// ---- FAQ accordion ----
document.querySelectorAll('.faq-question').forEach((btn) => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    const answer   = document.getElementById(btn.getAttribute('aria-controls'));

    // Close all others
    document.querySelectorAll('.faq-question').forEach((otherBtn) => {
      const otherAnswer = document.getElementById(otherBtn.getAttribute('aria-controls'));
      otherBtn.setAttribute('aria-expanded', 'false');
      if (otherAnswer) {
        otherAnswer.setAttribute('aria-hidden', 'true');
        otherAnswer.setAttribute('inert', '');
      }
    });

    // Toggle clicked
    btn.setAttribute('aria-expanded', String(!expanded));
    if (answer) {
      answer.setAttribute('aria-hidden', String(expanded));
      if (expanded) { answer.setAttribute('inert', ''); } else { answer.removeAttribute('inert'); }
    }
  });
});

// ---- Hamburger mobile nav ----
const hamburgerBtn     = document.getElementById('hamburger-btn');
const mobileNav        = document.getElementById('mobile-nav');
const navOverlay       = document.getElementById('nav-overlay');
const mobileNavClose   = document.getElementById('mobile-nav-close');

function openMobileNav() {
  mobileNav.classList.add('is-open');
  navOverlay.classList.add('is-open');
  hamburgerBtn.classList.add('is-open');
  hamburgerBtn.setAttribute('aria-expanded', 'true');
  mobileNav.setAttribute('aria-hidden', 'false');
  mobileNav.removeAttribute('inert');
  document.body.style.overflow = 'hidden';
}

function closeMobileNav() {
  mobileNav.classList.remove('is-open');
  navOverlay.classList.remove('is-open');
  hamburgerBtn.classList.remove('is-open');
  hamburgerBtn.setAttribute('aria-expanded', 'false');
  mobileNav.setAttribute('aria-hidden', 'true');
  mobileNav.setAttribute('inert', '');
  document.body.style.overflow = '';
  if (typeof window.resetFaithWorksMobileSubmenus === "function") {
    window.resetFaithWorksMobileSubmenus();
  }
  document.querySelectorAll(".mobile-services-toggle.is-open").forEach((toggle) => {
    toggle.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    const sub = document.getElementById(toggle.getAttribute("aria-controls"));
    if (sub) sub.classList.remove("is-open");
  });
}

if (hamburgerBtn) {
  hamburgerBtn.addEventListener('click', () => {
    hamburgerBtn.classList.contains('is-open') ? closeMobileNav() : openMobileNav();
  });
}
if (mobileNavClose) mobileNavClose.addEventListener('click', closeMobileNav);
if (navOverlay)     navOverlay.addEventListener('click', closeMobileNav);

// Close mobile nav when a link is tapped
if (mobileNav) {
  mobileNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMobileNav);
  });
}

// Close mobile nav on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('is-open')) {
    closeMobileNav();
  }
});

// Mobile drawer sub-menus (Service Menu + Service Areas)
document.querySelectorAll(".mobile-services-toggle").forEach((toggle) => {
  const subId = toggle.getAttribute("aria-controls");
  const sub = subId ? document.getElementById(subId) : null;
  if (!sub) return;
  toggle.addEventListener("click", () => {
    const open = toggle.classList.toggle("is-open");
    sub.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
  });
});
// ---- Reviews carousel (Knight Logics-style) ----
(function initFaithWorksReviews() {
  const track = document.getElementById("fw-review-track");
  const dotsWrap = document.getElementById("fw-review-dots");
  const prev = document.getElementById("fw-review-prev");
  const next = document.getElementById("fw-review-next");
  if (!track || !dotsWrap || !prev || !next) return;

  const cards = Array.from(track.children);
  if (!cards.length) return;

  let index = 0;
  let cardWidth = 0;
  const gap = 18;

  function perView() {
    if (window.innerWidth < 720) return 1;
    if (window.innerWidth < 1060) return 2;
    return 3;
  }

  function pageCount() {
    return Math.max(1, Math.ceil(cards.length / perView()));
  }

  function renderDots() {
    dotsWrap.innerHTML = "";
    for (let i = 0; i < pageCount(); i += 1) {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "fw-review-dot" + (i === index ? " is-active" : "");
      dot.setAttribute("aria-label", "Go to review set " + (i + 1));
      dot.addEventListener("click", () => {
        index = i;
        update();
      });
      dotsWrap.appendChild(dot);
    }
  }

  function measureCards() {
    cardWidth = cards[0] ? cards[0].offsetWidth : 0;
  }

  function update() {
    const pages = pageCount();
    index = Math.max(0, Math.min(index, pages - 1));
    const offset = index * (cardWidth + gap) * perView();
    track.style.transform = "translateX(" + -offset + "px)";
    Array.from(dotsWrap.children).forEach((dot, dotIndex) => {
      dot.classList.toggle("is-active", dotIndex === index);
    });
    prev.disabled = index === 0;
    next.disabled = index === pages - 1;
  }

  function onResize() {
    measureCards();
    renderDots();
    update();
  }

  prev.addEventListener("click", () => {
    index -= 1;
    update();
  });
  next.addEventListener("click", () => {
    index += 1;
    update();
  });
  window.addEventListener("resize", onResize);
  if (typeof ResizeObserver !== "undefined" && cards[0]) {
    new ResizeObserver(onResize).observe(cards[0]);
  }

  requestAnimationFrame(() => {
    measureCards();
    renderDots();
    update();
  });
})();

// ---- Homepage hero panels + parallax ----
function initHeroPanels() {
  document.querySelectorAll(".hero-panels").forEach((panels) => {
    const hero = panels.closest(".hero");
    if (!hero || hero.dataset.panelsInit) return;
    hero.dataset.panelsInit = "1";
    requestAnimationFrame(() => hero.classList.add("hero-panels-ready"));
  });
}

(function initHomeHeroParallax() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const hero = document.querySelector("body.home-landing .hero");
  if (!hero) return;

  const layers = hero.querySelectorAll(".hero-panels, .hero-cutout-wrap, .hero-overlay");
  if (!layers.length) return;

  let ticking = false;

  function update() {
    ticking = false;
    const heroTop = hero.offsetTop;
    const heroHeight = hero.offsetHeight;
    const offset = Math.max(0, window.scrollY - heroTop);
    const shift = Math.min(offset * 0.4, heroHeight);

    layers.forEach((layer) => {
      layer.style.setProperty("--st-hero-shift", `${Math.round(shift)}px`);
    });
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  initHeroPanels();
  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });

  window.setTimeout(() => {
    hero.querySelectorAll(".hero-panel").forEach((panel) => {
      const opacity = window.getComputedStyle(panel).opacity;
      if (opacity === "0") {
        panel.style.opacity = "1";
        panel.style.transform = "none";
      }
    });
    const cutout = hero.querySelector(".hero-cutout");
    if (cutout && window.getComputedStyle(cutout).opacity === "0") {
      cutout.style.opacity = "1";
      cutout.style.transform = "none";
    }
  }, 1600);
})();


// ---- Homepage follow banner entrance ----
(function initHomeStripEntrance() {
  if (!document.body.classList.contains("home-landing")) return;

  const shell = document.querySelector(".hero-follow-banner__shell.strip-slide");
  if (!shell) return;

  const reveal = () => {
    shell.classList.add("is-visible");
  };

  if (prefersReducedMotion()) {
    reveal();
    return;
  }

  const start = () => window.setTimeout(reveal, 1700);
  const hero = document.querySelector(".hero");

  if (hero?.classList.contains("hero-panels-ready")) {
    start();
    return;
  }

  if (!hero) {
    start();
    return;
  }

  const observer = new MutationObserver(() => {
    if (!hero.classList.contains("hero-panels-ready")) return;
    observer.disconnect();
    start();
  });

  observer.observe(hero, { attributes: true, attributeFilter: ["class"] });
})();

// ---- Legacy single-image hero parallax ----
(function initHeroParallax() {
  const hero = document.querySelector(".hero");
  const bg = hero && hero.querySelector(".hero-bg__img, .hero-bg img");
  if (!hero || !bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  let restTop = 0;
  let headerHeight = 0;
  let ticking = false;
  const rate = 0.45;

  function measureHeader() {
    const header = document.querySelector(".site-header");
    headerHeight = header ? header.offsetHeight : 0;
  }

  function update() {
    ticking = false;
    const rect = hero.getBoundingClientRect();
    if (window.scrollY < 2) {
      restTop = headerHeight || rect.top;
    }
    const shift = -(rect.top - restTop) * rate;
    bg.style.setProperty("--hero-shift", Math.round(shift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  function init() {
    measureHeader();
    requestAnimationFrame(queue);
  }

  window.addEventListener("load", init, { once: true });
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", () => {
    measureHeader();
    queue();
  }, { passive: true });
})();





































// ---- Band parallax (process + scope) ----
(function initBandParallax() {
  const sections = document.querySelectorAll(".process-section--parallax, .scope-section--parallax");
  if (!sections.length) return;
  if (prefersReducedMotion()) return;

  let ticking = false;
  const state = new Map();

  function measureSection(section) {
    const overscanRatio = Number(section.dataset.parallaxOverscan) || 0.38;
    state.set(section, {
      bgImg: section.querySelector(".process-bg__img, .scope-bg__img"),
      rate: Number(section.dataset.parallaxRate) || 0.78,
      maxShift: section.offsetHeight * overscanRatio,
    });
  }

  function clampShift(shift, limit) {
    return Math.round(Math.max(-limit, Math.min(limit, shift)));
  }

  function update() {
    ticking = false;
    const anchor = window.innerHeight * 0.5;
    sections.forEach((section) => {
      const info = state.get(section);
      if (!info || !info.bgImg) return;
      const rect = section.getBoundingClientRect();
      const shift = -(rect.top - anchor) * info.rate;
      info.bgImg.style.setProperty("--fw-band-shift", clampShift(shift, info.maxShift) + "px");
    });
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  function init() {
    sections.forEach(measureSection);
    requestAnimationFrame(queue);
  }

  window.addEventListener("load", init, { once: true });
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", () => {
    sections.forEach(measureSection);
    queue();
  }, { passive: true });
})();
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
// ---- Band parallax (process + scope) ----
