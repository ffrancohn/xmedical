/**
 * XMedical Atlas interactivo — selección de objeto, panel exploración, scroll suave.
 */
(function () {
  "use strict";

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function initHub(root) {
    const explore = document.getElementById("xm-atlas-explore");
    if (!explore) return;

    const panels = explore.querySelectorAll("[data-atlas-panel]");
    const objects = root.querySelectorAll("[data-atlas-module]");

    function setObjectImage(btn, open) {
      const img = btn.querySelector(".xm-atlas-object__img");
      if (!img) return;
      const src = open ? btn.getAttribute("data-atlas-img-open") : btn.getAttribute("data-atlas-img-closed");
      if (src) img.src = src;
    }

    function showPanel(moduleId) {
      panels.forEach((panel) => {
        const match = panel.getAttribute("data-atlas-panel") === moduleId;
        panel.hidden = !match;
      });
      explore.hidden = false;
      objects.forEach((btn) => {
        const active = btn.getAttribute("data-atlas-module") === moduleId;
        btn.classList.toggle("is-active", active);
        btn.setAttribute("aria-expanded", active ? "true" : "false");
        setObjectImage(btn, active);
      });
      if (!prefersReducedMotion()) {
        explore.scrollIntoView({ behavior: "smooth", block: "start" });
      } else {
        explore.scrollIntoView({ block: "start" });
      }
    }

    objects.forEach((btn) => {
      const moduleId = btn.getAttribute("data-atlas-module");
      btn.setAttribute("aria-expanded", "false");
      btn.addEventListener("click", () => {
        if (moduleId === "flujo_dia") {
          const hilo = document.querySelector(".xm-hilo");
          if (hilo) {
            hilo.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
          }
          return;
        }
        showPanel(moduleId);
      });
    });

    const initial = root.getAttribute("data-atlas-initial-module");
    if (initial) showPanel(initial);
  }

  document.querySelectorAll("[data-atlas-hub]").forEach(initHub);
})();
