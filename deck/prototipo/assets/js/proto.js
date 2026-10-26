/* Navegación del prototipo: perfil, pantalla, mapa y avatares. */
(function () {
  "use strict";

  const ORDER = ["superadmin", "admin", "recepcion", "enfermeria", "medico", "especialista", "paciente"];

  const PROFILES = {
    superadmin: {
      label: "Superadministrador", person: "Ana Ruiz", role: "Plataforma", avatar: "superadmin",
      initials: "AR", accent: "gold", portal: false, blurb: "Instituciones, respaldos y auditoría.",
      sections: [{ title: "Plataforma", items: [
        { id: "instituciones", label: "Instituciones", icon: "building" },
        { id: "respaldos", label: "Respaldos", icon: "database" },
        { id: "auditoria", label: "Auditoría", icon: "file" }
      ]}]
    },
    admin: {
      label: "Administrador", person: "Luis Ortega", role: "Clínica Demo", avatar: "admin",
      initials: "LO", accent: "blue", portal: false, blurb: "Operación, auditoría e IA.",
      sections: [
        { title: "Reportes", items: [{ id: "administracion", label: "Administración", icon: "chart" }] },
        { title: "Sistema", items: [
          { id: "auditoria", label: "Auditoría", icon: "file" },
          { id: "ia", label: "Configuración IA", icon: "cpu" }
        ]}
      ]
    },
    recepcion: {
      label: "Recepción", person: "Carmen Díaz", role: "Recepcionista", avatar: "recepcionista",
      initials: "CD", accent: "coral", portal: false, blurb: "Registra, agenda y recibe.",
      sections: [{ title: "Clínica", items: [
        { id: "inicio", label: "Inicio", icon: "home" },
        { id: "pacientes", label: "Pacientes", icon: "users" },
        { id: "citas", label: "Citas", icon: "calendar" }
      ]}]
    },
    enfermeria: {
      label: "Enfermería", person: "Rosa Méndez", role: "Enfermera", avatar: "enfermera",
      initials: "RM", accent: "green", portal: false, blurb: "Signos, triaje y cola.",
      sections: [{ title: "Clínica", items: [
        { id: "inicio", label: "Inicio", icon: "home" },
        { id: "preclinica", label: "Preclínica", icon: "heart" },
        { id: "triaje", label: "Triaje", icon: "activity" }
      ]}]
    },
    medico: {
      label: "Médico general", person: "Elena Vargas", role: "Medicina general", avatar: "medico",
      initials: "EV", accent: "teal", portal: false, blurb: "Agenda, consulta e historia.",
      sections: [{ title: "Clínica", items: [
        { id: "inicio", label: "Inicio", icon: "home" },
        { id: "consulta", label: "Consulta", icon: "stethoscope" },
        { id: "historia", label: "Historia", icon: "file" }
      ]}]
    },
    especialista: {
      label: "Especialista", person: "Martín Salas", role: "Cardiología", avatar: "especialista",
      initials: "MS", accent: "violet", portal: false, blurb: "Referencias y contrarreferencia.",
      sections: [{ title: "Clínica", items: [
        { id: "referencias", label: "Referencias", icon: "share" },
        { id: "agenda", label: "Agenda", icon: "calendar" },
        { id: "contrarreferencia", label: "Contrarreferencia", icon: "file" }
      ]}]
    },
    paciente: {
      label: "Paciente", person: "María José López", role: "Portal del paciente", avatar: "paciente",
      initials: "ML", accent: "sky", portal: true, blurb: "Citas, llegada e historia.",
      sections: [{ title: "Portal", items: [
        { id: "inicio", label: "Inicio", icon: "home" },
        { id: "citas", label: "Mis citas", icon: "calendar" },
        { id: "historia", label: "Historia", icon: "file" }
      ]}]
    }
  };

  const picker = document.getElementById("picker");
  const app = document.getElementById("app");
  const map = document.getElementById("map");
  const nav = document.getElementById("nav");
  const toast = document.getElementById("toast");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let toastTimer = 0;
  let lockHash = false;

  function screensOf(profile) {
    return profile.sections.flatMap((section) => section.items);
  }

  function showToast(text) {
    toast.textContent = text;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
  }

  function loadAvatar(node) {
    const file = node.dataset.file;
    const img = node.querySelector("img");
    const fallback = node.querySelector("[data-fallback]");
    if (!file || !img || !fallback) return;
    const fail = () => {
      img.hidden = true;
      fallback.hidden = false;
    };
    const ok = () => {
      img.hidden = false;
      fallback.hidden = true;
    };
    img.hidden = true;
    fallback.hidden = false;
    img.onload = ok;
    img.onerror = () => {
      if (!img.dataset.triedPng) {
        img.dataset.triedPng = "1";
        img.src = "avatars/" + file + ".png";
      } else fail();
    };
    img.dataset.triedPng = "";
    img.alt = "";
    img.src = "avatars/" + file + ".svg";
  }

  function runCounts(root) {
    root.querySelectorAll("[data-count]").forEach((el) => {
      const target = Number(el.dataset.count);
      if (reduced || !target) {
        el.textContent = String(target);
        return;
      }
      const start = performance.now();
      const tick = (now) => {
        const p = Math.min(1, (now - start) / 700);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = String(Math.round(target * eased));
        if (p < 1) requestAnimationFrame(tick);
      };
      el.textContent = "0";
      requestAnimationFrame(tick);
    });
  }

  function renderNav(profile, screenId) {
    nav.innerHTML = profile.sections.map((section) => {
      const buttons = section.items.map((item) => {
        const active = item.id === screenId ? " is-active" : "";
        return '<button type="button" class="nav-btn' + active + '" data-go="' + item.id + '">' +
          '<svg class="icon" aria-hidden="true"><use href="#i-' + item.icon + '"></use></svg>' +
          item.label + "</button>";
      }).join("");
      return '<div><div class="nav-sec">' + section.title + "</div>" + buttons + "</div>";
    }).join("");
  }

  const FLOW = [
    { id: "agendar", name: "Agendar", staff: "recepcionista", ini: "CD", caption: "Aún no llegan", people: [["CA", "Carlos Andrade"], ["AP", "Andrés Paz"]] },
    { id: "recibir", name: "Recibir", staff: "recepcionista", ini: "CD", caption: "En sala", people: [["ML", "María José López"], ["SG", "Sofía Gil"], ["NR", "Nora Ruiz"], ["HP", "Hugo Peña"]] },
    { id: "medir", name: "Medir", staff: "enfermera", ini: "RM", caption: "En signos", people: [["PR", "Pedro Ramos"], ["JT", "Julia Torres"], ["RG", "Raúl Gómez"]] },
    { id: "atender", name: "Atender", staff: "medico", ini: "EV", caption: "Listos para consulta", people: [["EV", "Elena Vásquez"], ["DS", "Diego Solís"]] },
    { id: "derivar", name: "Derivar", staff: "especialista", ini: "MS", caption: "Hacia especialidad", people: [["LM", "Lucía Méndez"], ["BK", "Bruno Klein"]] }
  ];
  const HILO_VIEW = {
    recepcion: { open: ["agendar", "recibir"], mine: ["agendar", "recibir"] },
    enfermeria: { open: ["medir"], mine: ["medir"] },
    medico: { open: ["atender"], mine: ["atender"] },
    especialista: { open: ["derivar"], mine: ["derivar"] },
    paciente: {
      personal: true,
      open: ["recibir"],
      mine: ["recibir"],
      done: ["agendar"],
      lines: {
        agendar: "Tu cita de las 10:30 ya está agendada.",
        recibir: "Estás aquí. Siguiente: Medir.",
        medir: "Siguiente paso, cuando pases a enfermería.",
        atender: "Consulta con Elena Vargas.",
        derivar: "Solo si te envían a especialidad."
      }
    }
  };

  function facesHtml(people) {
    const shown = people.slice(0, 3);
    const extra = people.length - shown.length;
    return '<div class="faces">' + shown.map(function (person) {
      return '<span class="ini" title="' + person[1] + '">' + person[0] + "</span>";
    }).join("") + (extra ? '<span class="more">+' + extra + "</span>" : "") + "</div>";
  }

  function setStation(hilo, id, open) {
    hilo.querySelectorAll("[data-station]").forEach(function (el) {
      if (el.dataset.station !== id) return;
      el.classList.toggle("is-open", open);
      if (el.classList.contains("station")) el.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function fitHilo(root) {
    const mobile = window.matchMedia("(max-width: 860px)").matches;
    root.querySelectorAll(".hilo").forEach(function (hilo) {
      const stations = Array.from(hilo.querySelectorAll(".station"));
      if (!mobile) {
        stations.forEach(function (station) {
          setStation(hilo, station.dataset.station, station.dataset.default === "open");
        });
        return;
      }
      const preferred = stations.find(function (station) { return station.dataset.default === "open"; }) || stations[0];
      stations.forEach(function (station) {
        setStation(hilo, station.dataset.station, station === preferred);
      });
    });
  }

  function renderHilo(node) {
    const view = HILO_VIEW[node.dataset.hilo];
    if (!view) return;
    node.classList.toggle("hilo-personal", !!view.personal);
    const buttons = FLOW.map(function (station, index) {
      const open = view.open.indexOf(station.id) !== -1;
      const mine = view.mine.indexOf(station.id) !== -1;
      const done = view.done && view.done.indexOf(station.id) !== -1;
      const count = view.personal ? "" : '<span class="station-count">' + station.people.length + " ahora</span>";
      const mark = view.personal
        ? '<span class="station-count">' + (index + 1) + " / 5</span>"
        : '<span class="avatar sm" data-file="' + station.staff + '"><img alt="" hidden><span data-fallback>' + station.ini + "</span></span>";
      return '<button type="button" class="station' + (open ? " is-open" : "") + (mine ? " is-mine" : "") + (done ? " is-done" : "") +
        '" data-station="' + station.id + '" data-default="' + (open ? "open" : "") + '" aria-expanded="' + (open ? "true" : "false") + '">' +
        '<span class="station-top">' + mark + "<span><span class=\"station-name\">" + station.name + "</span>" + count + "</span></span></button>";
    }).join("");
    const panels = FLOW.map(function (station, index) {
      const open = view.open.indexOf(station.id) !== -1 ? " is-open" : "";
      const body = view.personal
        ? (station.id === "recibir"
          ? '<div class="person-row"><div class="avatar sm" data-file="paciente"><img alt="" hidden><span data-fallback>ML</span></div><p class="hilo-caption">' + view.lines[station.id] + "</p></div>"
          : '<p class="hilo-caption">' + view.lines[station.id] + "</p>")
        : '<p class="hilo-caption">' + station.caption + "</p>" + facesHtml(station.people);
      return '<div class="hilo-panel' + open + '" data-station="' + station.id + '" style="--col:' + (index + 1) + '">' + body + "</div>";
    }).join("");
    node.innerHTML = '<p class="kicker hilo-kicker">' + (view.personal ? "Tu lugar en el hilo" : "El hilo de hoy") + "</p>" +
      '<div class="hilo-track">' + buttons + "</div><div class=\"hilo-panels\">" + panels + "</div>";
    node.querySelectorAll(".avatar[data-file]").forEach(loadAvatar);
  }

  function showPicker() {
    app.hidden = true;
    picker.hidden = false;
    map.hidden = true;
    app.classList.remove("nav-open");
    if (location.hash) history.replaceState(null, "", location.pathname + location.search);
    document.title = "XMedical · Prototipo";
  }

  function show(profileId, screenId, fromHash) {
    const profile = PROFILES[profileId];
    if (!profile) {
      showPicker();
      return;
    }
    const items = screensOf(profile);
    const item = items.find((entry) => entry.id === screenId) || items[0];
    const index = items.findIndex((entry) => entry.id === item.id);

    picker.hidden = true;
    app.hidden = false;
    map.hidden = true;
    app.classList.toggle("is-portal", profile.portal);
    app.style.setProperty("--accent", "var(--" + profile.accent + ")");
    app.classList.remove("nav-open");

    document.querySelectorAll(".screen").forEach((screen) => {
      const on = screen.dataset.profile === profileId && screen.dataset.screen === item.id;
      screen.classList.toggle("is-on", on);
    });

    renderNav(profile, item.id);
    document.getElementById("who-name").textContent = profile.person;
    document.getElementById("who-role").textContent = profile.role;
    document.getElementById("side-kicker").textContent = profile.portal ? "Portal" : "Clínica Demo";
    const sessionAvatar = document.getElementById("session-avatar");
    sessionAvatar.dataset.file = profile.avatar;
    sessionAvatar.querySelector("[data-fallback]").textContent = profile.initials;
    loadAvatar(sessionAvatar);

    const active = document.querySelector(".screen.is-on");
    if (active) {
      document.getElementById("crumb-kicker").textContent = active.dataset.kicker || profile.label;
      document.getElementById("crumb-title").textContent = active.dataset.title || item.label;
      active.querySelectorAll(".avatar[data-file]").forEach(loadAvatar);
      runCounts(active);
      fitHilo(active);
      active.parentElement.scrollTop = 0;
    }
    document.getElementById("count").textContent = (index + 1) + " / " + items.length;
    document.title = profile.label + " · " + item.label;

    const nextHash = "#" + profileId + "/" + item.id;
    if (!fromHash && location.hash !== nextHash) {
      lockHash = true;
      location.hash = nextHash;
      lockHash = false;
    }
  }

  function current() {
    const raw = location.hash.replace(/^#/, "");
    const [profileId, screenId] = raw.split("/");
    return { profileId, screenId };
  }

  function step(delta) {
    const { profileId, screenId } = current();
    const profile = PROFILES[profileId];
    if (!profile) return;
    const items = screensOf(profile);
    const index = Math.max(0, items.findIndex((item) => item.id === screenId));
    const next = items[(index + delta + items.length) % items.length];
    show(profileId, next.id);
  }

  function openMap() {
    const { profileId } = current();
    if (!profileId) return;
    const grid = document.getElementById("map-grid");
    grid.innerHTML = ORDER.map((id) => {
      const profile = PROFILES[id];
      const on = id === profileId ? " on" : "";
      return '<button type="button" class="' + on.trim() + '" data-pick="' + id + '"><b>' +
        profile.label + "</b><span>" + profile.blurb + "</span></button>";
    }).join("");
    map.hidden = false;
    grid.querySelector("button").focus();
  }

  document.body.addEventListener("click", (event) => {
    const station = event.target.closest(".station");
    if (station) {
      const hilo = station.closest(".hilo");
      const mobile = window.matchMedia("(max-width: 860px)").matches;
      const single = mobile || hilo.classList.contains("hilo-personal");
      if (single) {
        hilo.querySelectorAll(".station").forEach(function (item) {
          setStation(hilo, item.dataset.station, item === station);
        });
      } else {
        setStation(hilo, station.dataset.station, !station.classList.contains("is-open"));
      }
      return;
    }
    const pick = event.target.closest("[data-pick]");
    if (pick) {
      show(pick.dataset.pick);
      return;
    }
    const go = event.target.closest("[data-go]");
    if (go && current().profileId) {
      show(current().profileId, go.dataset.go);
      return;
    }
    if (event.target.closest("[data-picker]")) {
      showPicker();
      return;
    }
    if (event.target.closest("[data-map]")) {
      openMap();
      return;
    }
    if (event.target.closest("[data-close-map]")) {
      map.hidden = true;
      return;
    }
    if (event.target.closest("[data-menu]")) {
      app.classList.toggle("nav-open");
      return;
    }
    if (event.target.closest("[data-prev]")) step(-1);
    if (event.target.closest("[data-next]")) step(1);
    if (event.target.id === "map") {
      map.hidden = true;
      return;
    }
    const demo = event.target.closest("button");
    if (demo && demo.type === "submit" && !demo.form) {
      showToast("Prototipo visual: esta acción no guarda datos.");
    }
    if (demo && demo.classList.contains("linkish") && !demo.dataset.go) {
      showToast("Prototipo visual: esta acción no guarda datos.");
    }
  });

  document.body.addEventListener("submit", (event) => {
    event.preventDefault();
    showToast("Prototipo visual: esta acción no guarda datos.");
  });

  document.addEventListener("keydown", (event) => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName);
    if (event.key === "Escape") {
      if (!map.hidden) map.hidden = true;
      else if (app.classList.contains("nav-open")) app.classList.remove("nav-open");
      else if (!app.hidden) showPicker();
      return;
    }
    if (typing) return;
    if (event.key === "g" || event.key === "G") {
      if (!app.hidden) openMap();
      return;
    }
    if (event.key === "Home") {
      showPicker();
      return;
    }
    if (app.hidden || !map.hidden) return;
    if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
      event.preventDefault();
      step(1);
    }
    if (event.key === "ArrowLeft" || event.key === "PageUp") {
      event.preventDefault();
      step(-1);
    }
  });

  window.addEventListener("hashchange", () => {
    if (lockHash) return;
    const { profileId, screenId } = current();
    if (!profileId) showPicker();
    else show(profileId, screenId, true);
  });

  document.querySelectorAll("[data-hilo]").forEach(renderHilo);
  window.addEventListener("resize", function () { fitHilo(document); });

  const params = new URLSearchParams(location.search);
  const perfil = params.get("perfil");
  if (perfil && PROFILES[perfil] && !location.hash) {
    location.hash = perfil;
  } else if (!location.hash) {
    showPicker();
  } else {
    const { profileId, screenId } = current();
    show(profileId, screenId, true);
  }
})();
