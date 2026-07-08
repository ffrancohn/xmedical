(function () {
  const form = document.getElementById("consulta-wizard-form");
  if (!form) return;

  const config = form.dataset;
  const indicator = document.getElementById("autosave-indicator");
  const autosaveEnabled = config.autosaveEnabled === "true";
  const autosaveUrl = config.autosaveUrl;
  const step = config.step;
  let saving = false;

  function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : "";
  }

  function setIndicator(state, message) {
    if (!indicator) return;
    indicator.dataset.state = state;
    indicator.textContent = message;
    indicator.className = "text-sm";
    if (state === "saved") indicator.classList.add("text-success");
    if (state === "saving") indicator.classList.add("text-info");
    if (state === "error") indicator.classList.add("text-error");
    if (state === "idle") indicator.classList.add("opacity-70");
  }

  async function autosave() {
    if (!autosaveEnabled || !autosaveUrl || saving) return;
    saving = true;
    setIndicator("saving", "Guardando borrador...");
    const body = new FormData(form);
    body.set("step", step);
    try {
      const response = await fetch(autosaveUrl, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        body,
      });
      const data = await response.json();
      if (!response.ok || !data.ok) {
        throw new Error(data.error || "Error de autosave");
      }
      setIndicator("saved", "Borrador guardado " + new Date().toLocaleTimeString());
    } catch (error) {
      setIndicator("error", "No se pudo guardar el borrador");
      console.error(error);
    } finally {
      saving = false;
    }
  }

  if (autosaveEnabled) {
    setIndicator("idle", "Autosave activo cada 30 s");
    setInterval(autosave, 30000);
  }

  form.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      form.requestSubmit();
    }
  });

  const suggestBtn = document.getElementById("btn-sugerir-diagnostico");
  const suggestBox = document.getElementById("ia-sugerencias");
  const suggestUrl = config.suggestUrl;

  if (suggestBtn && suggestBox && suggestUrl) {
    suggestBtn.addEventListener("click", async () => {
      suggestBtn.disabled = true;
      suggestBox.innerHTML = '<p class="text-sm opacity-70">Consultando sugerencias...</p>';
      try {
        const response = await fetch(suggestUrl, {
          method: "POST",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
        });
        const data = await response.json();
        if (!response.ok || !data.ok) {
          throw new Error(data.error || "IA no disponible");
        }
        if (!data.sugerencias.length) {
          suggestBox.innerHTML = '<p class="alert alert-warning">Sin sugerencias para los datos actuales.</p>';
          return;
        }
        suggestBox.innerHTML =
          `<p class="text-sm text-warning mb-2">${data.disclaimer}</p>` +
          data.sugerencias
            .map(
              (item, index) => `
              <div class="border rounded-box p-3 mb-2">
                <p class="font-semibold">${item.codigo} - ${item.nombre}</p>
                ${item.justificacion ? `<p class="text-sm opacity-80">${item.justificacion}</p>` : ""}
                <button type="button" class="btn btn-sm btn-outline mt-2 ia-usar-sugerencia"
                  data-code="${item.codigo}" data-name="${item.nombre}" data-index="${index}">
                  Usar esta sugerencia
                </button>
              </div>`
            )
            .join("");

        suggestBox.querySelectorAll(".ia-usar-sugerencia").forEach((button) => {
          button.addEventListener("click", () => {
            const codigo = button.dataset.code;
            const nombre = button.dataset.name;
            const confirmar = window.confirm(
              `¿Confirmar sugerencia IA?\n\n${codigo} - ${nombre}\n\nEsto es solo apoyo clinico; usted es responsable del diagnostico final.`
            );
            if (!confirmar) return;
            const codeInput = document.getElementById("id_codigo_cie10");
            const nameInput = document.getElementById("id_nombre");
            if (codeInput) codeInput.value = codigo;
            if (nameInput) nameInput.value = nombre;
            setIndicator("saved", "Sugerencia IA aplicada (pendiente de guardar)");
          });
        });
      } catch (error) {
        suggestBox.innerHTML = `<p class="alert alert-error">${error.message}</p>`;
      } finally {
        suggestBtn.disabled = false;
      }
    });
  }
})();
