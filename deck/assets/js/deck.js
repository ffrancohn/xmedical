/* ============================================================
   XMEDICAL · ATLAS — deck controller
   Navigation, overview, chapters, counters, plan toggle.
   ============================================================ */
(function () {
  "use strict";

  const deck = document.getElementById("deck");
  const stage = document.getElementById("stage");
  const slides = Array.from(document.querySelectorAll(".slide"));
  const total = slides.length;
  const body = document.body;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const params = new URLSearchParams(window.location.search);
  const staticMode = params.get("static") === "1";
  if (staticMode) body.classList.add("is-static");

  let index = 0;
  let locked = false;
  let touchStart = null;

  const els = {
    currentNum: document.getElementById("currentNum"),
    totalNum: document.getElementById("totalNum"),
    currentTitle: document.getElementById("currentTitle"),
    chapterLabel: document.getElementById("chapterLabel"),
    chapterNav: document.getElementById("chapterNav"),
    progressFill: document.getElementById("progressFill"),
    progress: document.querySelector(".progress"),
    prevBtn: document.getElementById("prevBtn"),
    nextBtn: document.getElementById("nextBtn"),
    overview: document.getElementById("overview"),
    overviewGrid: document.getElementById("overviewGrid"),
    overviewBtn: document.getElementById("overviewBtn"),
    overviewClose: document.getElementById("overviewClose"),
    fullscreenBtn: document.getElementById("fullscreenBtn"),
    planStage: document.querySelector(".plan-stage"),
    planButtons: Array.from(document.querySelectorAll("[data-plan-btn]")),
    planHudLabel: document.getElementById("planHudLabel")
  };

  const chapters = [];
  slides.forEach((slide, i) => {
    const key = slide.dataset.chapter || "00";
    const label = slide.dataset.chapterLabel || "Introducción";
    let chapter = chapters.find((c) => c.key === key);
    if (!chapter) {
      chapter = { key, label, first: i, slides: [] };
      chapters.push(chapter);
    }
    chapter.slides.push(i);
  });

  /* ---------- navigation ---------- */
  function goTo(next, opts = {}) {
    next = Math.max(0, Math.min(total - 1, next));
    if (next === index && opts.force !== true) return;
    if (locked && !opts.force) return;

    const previous = index;
    index = next;

    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === index);
      slide.classList.toggle("is-before", i < index);
      slide.setAttribute("aria-hidden", i === index ? "false" : "true");
      if (i === index) {
        slide.removeAttribute("inert");
      } else {
        slide.setAttribute("inert", "");
      }
    });

    const slide = slides[index];
    body.dataset.tone = slide.dataset.tone || "light";
    body.dataset.slide = String(index + 1);

    if (els.currentNum) els.currentNum.textContent = String(index + 1).padStart(2, "0");
    if (els.currentTitle) els.currentTitle.textContent = slide.dataset.title || "";
    if (els.chapterLabel) {
      els.chapterLabel.textContent = `${slide.dataset.chapter || "00"} · ${slide.dataset.chapterLabel || "Introducción"}`;
    }
    if (els.progressFill) els.progressFill.style.width = `${((index + 1) / total) * 100}%`;
    if (els.progress) els.progress.setAttribute("aria-valuenow", Math.round(((index + 1) / total) * 100));

    if (els.prevBtn) els.prevBtn.disabled = index === 0;
    if (els.nextBtn) els.nextBtn.disabled = index === total - 1;

    updateChapterNav();
    runCounters(slide);
    updateHash();

    if (!reduceMotion) {
      body.classList.remove("nav-prev", "nav-next");
      if (index > previous) body.classList.add("nav-next");
      else if (index < previous) body.classList.add("nav-prev");
      window.setTimeout(() => body.classList.remove("nav-prev", "nav-next"), 480);
    }

    // release the lock after the slide transition
    locked = true;
    window.setTimeout(() => { locked = false; }, reduceMotion ? 20 : 420);
  }

  function nextSlide() { goTo(index + 1); }
  function prevSlide() { goTo(index - 1); }

  function updateHash() {
    const id = slides[index] && slides[index].id;
    if (!id) return;
    const url = new URL(window.location.href);
    url.hash = id;
    try {
      history.replaceState(null, "", url);
    } catch (err) {
      window.location.hash = id;
    }
  }

  function slideFromHash() {
    const hash = window.location.hash.replace("#", "");
    if (hash) {
      const found = slides.findIndex((s) => s.id === hash);
      if (found >= 0) return found;
    }
    const params = new URLSearchParams(window.location.search);
    const q = parseInt(params.get("slide"), 10);
    if (!Number.isNaN(q) && q >= 1 && q <= total) return q - 1;
    return 0;
  }

  /* ---------- chapters ---------- */
  function updateChapterNav() {
    if (!els.chapterNav) return;
    const current = chapters.findIndex((c) => c.slides.includes(index));
    Array.from(els.chapterNav.children).forEach((btn, i) => {
      btn.classList.toggle("is-active", i === current);
      btn.setAttribute("aria-current", i === current ? "true" : "false");
    });
  }

  function buildChapterNav() {
    if (!els.chapterNav) return;
    els.chapterNav.innerHTML = "";
    chapters.forEach((chapter) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = `${chapter.key} ${chapter.label}`;
      btn.title = `Ir a ${chapter.label}`;
      btn.addEventListener("click", () => goTo(chapter.first, { force: true }));
      els.chapterNav.appendChild(btn);
    });
    updateChapterNav();
  }

  /* ---------- counters ---------- */
  function runCounters(slide) {
    const counters = slide.querySelectorAll("[data-count]");
    counters.forEach((el) => {
      if (el.dataset.done === "1") return;
      const target = parseInt(el.dataset.count, 10);
      if (Number.isNaN(target)) return;
      el.dataset.done = "1";
      if (reduceMotion || staticMode) {
        el.textContent = String(target);
        return;
      }
      const duration = 850;
      const start = performance.now();
      function tick(now) {
        const p = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = String(Math.round(target * eased));
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = String(target);
      }
      requestAnimationFrame(tick);
    });
  }

  /* ---------- overview ---------- */
  function buildOverview() {
    if (!els.overviewGrid) return;
    els.overviewGrid.innerHTML = "";
    chapters.forEach((chapter) => {
      const section = document.createElement("section");
      section.className = "overview-chapter";
      const h = document.createElement("h3");
      h.textContent = `${chapter.key} · ${chapter.label}`;
      section.appendChild(h);
      const cards = document.createElement("div");
      cards.className = "overview-cards";
      chapter.slides.forEach((i) => {
        const slide = slides[i];
        const card = document.createElement("button");
        card.type = "button";
        card.className = "overview-card";
        card.dataset.slideIndex = String(i);
        card.innerHTML = `
          <span class="overview-card-num">${String(i + 1).padStart(2, "0")}</span>
          <span class="overview-card-title">${slide.dataset.title || slide.id}</span>
          <span class="overview-card-summary">${slide.dataset.summary || ""}</span>
          <span class="overview-card-arrow">→</span>`;
        card.addEventListener("click", () => {
          closeOverview();
          goTo(i, { force: true });
        });
        cards.appendChild(card);
      });
      section.appendChild(cards);
      els.overviewGrid.appendChild(section);
    });
    updateOverviewCurrent();
  }

  function updateOverviewCurrent() {
    if (!els.overviewGrid) return;
    els.overviewGrid.querySelectorAll(".overview-card").forEach((card) => {
      card.classList.toggle("is-current", Number(card.dataset.slideIndex) === index);
    });
  }

  function openOverview() {
    if (!els.overview) return;
    updateOverviewCurrent();
    body.classList.add("overview-open");
    els.overview.setAttribute("aria-hidden", "false");
    const current = els.overviewGrid.querySelector(".overview-card.is-current");
    if (current) current.scrollIntoView({ block: "center", behavior: reduceMotion ? "auto" : "smooth" });
    els.overview.setAttribute("tabindex", "-1");
    window.setTimeout(() => els.overview.focus({ preventScroll: true }), 50);
    if (els.overviewBtn) els.overviewBtn.setAttribute("aria-expanded", "true");
  }

  function closeOverview() {
    if (!body.classList.contains("overview-open")) return;
    body.classList.remove("overview-open");
    if (els.overview) els.overview.setAttribute("aria-hidden", "true");
    if (els.overviewBtn) {
      els.overviewBtn.setAttribute("aria-expanded", "false");
      els.overviewBtn.focus();
    }
  }

  function toggleOverview() {
    if (body.classList.contains("overview-open")) closeOverview();
    else openOverview();
  }

  /* ---------- plan toggle ---------- */
  function setPlanView(view) {
    if (!els.planStage) return;
    els.planStage.dataset.planView = view;
    els.planButtons.forEach((btn) => {
      const active = btn.dataset.planBtn === view;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
    if (els.planHudLabel) {
      els.planHudLabel.textContent = view === "flat"
        ? "Planta · recorrido del paciente · 5 estaciones"
        : "Recorrido del paciente · 5 estaciones";
    }
  }

  /* ---------- fullscreen ---------- */
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      const req = document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
      if (req && req.catch) req.catch(() => {});
    } else if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  }

  /* ---------- events ---------- */
  function bind() {
    if (els.prevBtn) els.prevBtn.addEventListener("click", prevSlide);
    if (els.nextBtn) els.nextBtn.addEventListener("click", nextSlide);
    if (els.overviewBtn) {
      els.overviewBtn.setAttribute("aria-expanded", "false");
      els.overviewBtn.addEventListener("click", toggleOverview);
    }
    if (els.overviewClose) els.overviewClose.addEventListener("click", closeOverview);
    if (els.fullscreenBtn) els.fullscreenBtn.addEventListener("click", toggleFullscreen);

    document.querySelectorAll("[data-goto]").forEach((el) => {
      el.addEventListener("click", (e) => {
        const n = parseInt(el.dataset.goto, 10);
        if (Number.isNaN(n)) return;
        e.preventDefault();
        closeOverview();
        goTo(n - 1, { force: true });
      });
    });

    els.planButtons.forEach((btn) => {
      btn.addEventListener("click", () => setPlanView(btn.dataset.planBtn));
    });

    document.addEventListener("keydown", (e) => {
      const target = e.target;
      const typing = target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable);
      if (typing) return;

      if (e.key === "Escape") {
        if (body.classList.contains("overview-open")) {
          e.preventDefault();
          closeOverview();
        }
        return;
      }
      if (e.key === "g" || e.key === "G") {
        e.preventDefault();
        toggleOverview();
        return;
      }
      if (e.key === "f" || e.key === "F") {
        e.preventDefault();
        toggleFullscreen();
        return;
      }
      if (body.classList.contains("overview-open")) {
        if (e.key === "ArrowDown" || e.key === "ArrowRight") {
          e.preventDefault();
          const cards = Array.from(els.overviewGrid.querySelectorAll(".overview-card"));
          const cur = cards.findIndex((c) => c === document.activeElement);
          const next = cards[Math.min(cards.length - 1, cur + 1)];
          if (next) next.focus();
        } else if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
          e.preventDefault();
          const cards = Array.from(els.overviewGrid.querySelectorAll(".overview-card"));
          const cur = cards.findIndex((c) => c === document.activeElement);
          const prev = cards[Math.max(0, cur - 1)];
          if (prev) prev.focus();
        }
        return;
      }

      if (e.key === "ArrowRight" || e.key === "PageDown" || (e.key === " " && !e.shiftKey)) {
        e.preventDefault();
        nextSlide();
      } else if (e.key === "ArrowLeft" || e.key === "PageUp" || (e.key === " " && e.shiftKey)) {
        e.preventDefault();
        prevSlide();
      } else if (e.key === "Home") {
        e.preventDefault();
        goTo(0, { force: true });
      } else if (e.key === "End") {
        e.preventDefault();
        goTo(total - 1, { force: true });
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        nextSlide();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        prevSlide();
      }
    });

    window.addEventListener("hashchange", () => {
      const found = slideFromHash();
      if (found !== index) goTo(found, { force: true });
    });

    // touch / swipe
    stage.addEventListener("pointerdown", (e) => {
      if (e.pointerType === "mouse") return;
      if (e.target.closest("button,a")) return;
      touchStart = { x: e.clientX, y: e.clientY, t: Date.now() };
    });
    stage.addEventListener("pointerup", (e) => {
      if (!touchStart) return;
      const dx = e.clientX - touchStart.x;
      const dy = e.clientY - touchStart.y;
      const elapsed = Date.now() - touchStart.t;
      touchStart = null;
      if (elapsed > 900) return;
      if (Math.abs(dx) > 52 && Math.abs(dx) > Math.abs(dy) * 1.4) {
        if (dx < 0) nextSlide();
        else prevSlide();
      }
    });
    stage.addEventListener("pointercancel", () => { touchStart = null; });

    // clicking the dim area of the overview closes it
    if (els.overview) {
      els.overview.addEventListener("click", (e) => {
        if (e.target === els.overview || e.target.classList.contains("overview-bg")) closeOverview();
      });
    }
  }

  /* ---------- decorative QR ---------- */
  function buildQR() {
    document.querySelectorAll("[data-qr]").forEach((grid) => {
      const n = 21;
      const cells = Array.from({ length: n * n }, () => false);
      const at = (x, y) => y * n + x;
      const finder = (ox, oy) => {
        for (let y = 0; y < 7; y++) {
          for (let x = 0; x < 7; x++) {
            const edge = x === 0 || y === 0 || x === 6 || y === 6;
            const core = x >= 2 && x <= 4 && y >= 2 && y <= 4;
            cells[at(ox + x, oy + y)] = edge || core;
          }
        }
      };
      finder(0, 0); finder(14, 0); finder(0, 14);
      for (let i = 8; i < 13; i++) {
        cells[at(i, 6)] = i % 2 === 0;
        cells[at(6, i)] = i % 2 === 0;
      }
      // deterministic pseudo-random data modules
      let seed = 7319;
      const rand = () => {
        seed = (seed * 1103515245 + 12345) & 0x7fffffff;
        return seed / 0x7fffffff;
      };
      for (let y = 0; y < n; y++) {
        for (let x = 0; x < n; x++) {
          if ((x < 8 && y < 8) || (x > 13 && y < 8) || (x < 8 && y > 13)) continue;
          if (x === 6 || y === 6) continue;
          cells[at(x, y)] = rand() > 0.52;
        }
      }
      const frag = document.createDocumentFragment();
      cells.forEach((on) => {
        const cell = document.createElement("span");
        cell.className = "qr-cell" + (on ? " on" : "");
        frag.appendChild(cell);
      });
      grid.appendChild(frag);
    });
  }

  /* ---------- init ---------- */
  function init() {
    if (!slides.length) return;
    if (els.totalNum) els.totalNum.textContent = String(total).padStart(2, "0");
    buildChapterNav();
    buildOverview();
    buildQR();
    bind();
    index = slideFromHash();
    slides.forEach((slide, i) => {
      const active = i === index;
      slide.classList.toggle("is-active", active);
      slide.classList.toggle("is-before", i < index);
      slide.setAttribute("aria-hidden", active ? "false" : "true");
      if (!active) slide.setAttribute("inert", "");
    });
    const slide = slides[index];
    body.dataset.tone = slide.dataset.tone || "light";
    body.dataset.slide = String(index + 1);
    if (els.currentNum) els.currentNum.textContent = String(index + 1).padStart(2, "0");
    if (els.currentTitle) els.currentTitle.textContent = slide.dataset.title || "";
    if (els.chapterLabel) els.chapterLabel.textContent = `${slide.dataset.chapter || "00"} · ${slide.dataset.chapterLabel || "Introducción"}`;
    if (els.progressFill) els.progressFill.style.width = `${((index + 1) / total) * 100}%`;
    if (els.progress) els.progress.setAttribute("aria-valuenow", Math.round(((index + 1) / total) * 100));
    if (els.prevBtn) els.prevBtn.disabled = index === 0;
    if (els.nextBtn) els.nextBtn.disabled = index === total - 1;
    updateChapterNav();
    runCounters(slide);
    setPlanView(params.get("plan") === "flat" ? "flat" : "iso");
    if (params.get("overview") === "1") window.setTimeout(openOverview, 80);
    window.setTimeout(() => { body.classList.add("is-ready"); }, 60);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
