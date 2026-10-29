/**
 * XMedical Atlas interactivo — selección de objeto, panel exploración, scroll suave.
 *
 * Un hub = un contenedor con [data-atlas-hub] que contiene:
 *   - botones [data-atlas-module]
 *   - un contenedor [data-atlas-explore] con paneles [data-atlas-panel="<id>"]
 *
 * Comportamiento: clic abre el panel del módulo, mueve el foco al panel (para
 * lectores de pantalla), Escape cierra y devuelve el foco al objeto. Los módulos
 * sin panel no abren un contenedor vacío.
 */
(function () {
  "use strict";

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function scrollTo(element) {
    if (!element) return;
    element.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
  }

  function initHub(root) {
    const explore =
      root.querySelector("[data-atlas-explore]") || document.getElementById("xm-atlas-explore");
    if (!explore) return;

    const panels = Array.from(explore.querySelectorAll("[data-atlas-panel]"));
    const objects = Array.from(root.querySelectorAll("[data-atlas-module]"));
    let lastTrigger = null;

    function panelFor(moduleId) {
      return panels.find((panel) => panel.getAttribute("data-atlas-panel") === moduleId) || null;
    }

    function setObjectImage(btn, open) {
      const img = btn.querySelector(".xm-atlas-object__img");
      if (!img) return;
      const src = open
        ? btn.getAttribute("data-atlas-img-open")
        : btn.getAttribute("data-atlas-img-closed");
      if (src) img.src = src;
    }

    function deactivate() {
      objects.forEach((btn) => {
        btn.classList.remove("is-active");
        btn.setAttribute("aria-expanded", "false");
        setObjectImage(btn, false);
      });
    }

    function close(returnFocus) {
      explore.hidden = true;
      panels.forEach((panel) => {
        panel.hidden = true;
      });
      deactivate();
      if (returnFocus && lastTrigger) lastTrigger.focus();
    }

    function showPanel(moduleId, trigger) {
      const panel = panelFor(moduleId);
      if (!panel) return false;

      panels.forEach((item) => {
        item.hidden = item !== panel;
      });
      explore.hidden = false;
      lastTrigger = trigger || null;

      objects.forEach((btn) => {
        const active = btn.getAttribute("data-atlas-module") === moduleId;
        btn.classList.toggle("is-active", active);
        btn.setAttribute("aria-expanded", active ? "true" : "false");
        setObjectImage(btn, active);
      });

      panel.setAttribute("tabindex", "-1");
      panel.focus({ preventScroll: true });
      scrollTo(explore);
      return true;
    }

    objects.forEach((btn) => {
      const moduleId = btn.getAttribute("data-atlas-module");
      btn.setAttribute("aria-expanded", "false");
      btn.addEventListener("click", () => {
        if (moduleId === "flujo_dia") {
          scrollTo(document.querySelector(".xm-hilo"));
          return;
        }
        if (!showPanel(moduleId, btn)) {
          // Módulo declarado sin panel: llevamos al bloque equivalente en vez de
          // abrir un contenedor vacío.
          scrollTo(document.querySelector(".xm-hilo"));
        }
      });
    });

    explore.addEventListener("keydown", (event) => {
      if (event.key === "Escape") close(true);
    });

    const initial = root.getAttribute("data-atlas-initial-module");
    if (initial) showPanel(initial, null);
  }

  document.querySelectorAll("[data-atlas-hub]").forEach(initHub);
})();
