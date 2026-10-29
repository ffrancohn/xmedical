/**
 * XMedical Atlas — escena isométrica del consultorio.
 *
 * Pinta un SVG axonométrico con estaciones (escritorio, paciente, sala de espera,
 * archivo, pasillo). Cada estación es un <g role="button" tabindex="0"> con su
 * aria-label; al seleccionar, la cámara hace punch-in y se abre el panel.
 * Escape vuelve y devuelve el foco.
 *
 * Datos: JSON embebido por `json_script` en #xm-scene-data (atlas_scene.construir_escena_medico).
 */
(function () {
  "use strict";

  var root = document.getElementById("xm-scene");
  if (!root) return;
  var dataEl = document.getElementById("xm-scene-data");
  if (!dataEl) return;

  var SCENE = JSON.parse(dataEl.textContent);
  var svg = document.getElementById("xm-scene-svg");
  var labelsBox = document.getElementById("xm-scene-labels");
  var panel = document.getElementById("xm-scene-panel");
  var table = document.getElementById("xm-scene-table");

  var byId = {};
  SCENE.estaciones.forEach(function (e) { byId[e.id] = e; });
  var paciente = SCENE.paciente || {};

  /* ---------- proyección ---------- */
  var COS = Math.cos(Math.PI / 6), SIN = 0.5, S = 34;
  function P(x, y, z) { return [(x - y) * COS * S, (x + y) * SIN * S - (z || 0) * S]; }
  function n(v) { return Math.round(v * 100) / 100; }
  function pts(arr) { return arr.map(function (p) { return n(p[0]) + "," + n(p[1]); }).join(" "); }

  var C = {
    floorA: "#f0ece2", grid: "rgba(11,31,38,.09)",
    wallL: "#e6e0d3", wallB: "#eee9de",
    wood: "#c9a27a", woodTop: "#dcbb96", woodDark: "#a9855f",
    steel: "#a3aeb1", steelTop: "#bcc6c8", steelDark: "#8b979a",
    paper: "#fbfaf6", accent: "#0f766e", accentDark: "#0a4f4a",
    screen: "#123039", skin: "#3e5158", shirt: "#5b6f75"
  };

  function quad(list, a, b, c, d, fill, stroke) {
    list.push('<polygon points="' + pts([a, b, c, d]) + '" fill="' + fill + '"' +
      (stroke ? ' stroke="' + stroke + '" stroke-width=".7"' : "") + "/>");
  }
  function flat(list, x, y, z, w, d, fill, stroke) {
    quad(list, P(x, y, z), P(x + w, y, z), P(x + w, y + d, z), P(x, y + d, z), fill, stroke);
  }
  function box(list, x, y, z, w, d, h, col) {
    var top = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)];
    var right = [top[3], top[2], P(x + w, y + d, z), P(x, y + d, z)];
    var left = [top[0], top[3], P(x, y + d, z), P(x, y, z)];
    list.push('<polygon points="' + pts(top) + '" fill="' + col.top + '"/>');
    list.push('<polygon points="' + pts(right) + '" fill="' + col.right + '"/>');
    list.push('<polygon points="' + pts(left) + '" fill="' + col.left + '"/>');
  }
  function person(list, x, y, h, color) {
    var head = P(x, y, h);
    list.push('<circle cx="' + n(head[0]) + '" cy="' + n(head[1]) + '" r="7.5" fill="' + color + '"/>');
    quad(list, P(x - 0.2, y, h - 0.18), P(x + 0.2, y, h - 0.18), P(x + 0.2, y, h - 0.95), P(x - 0.2, y, h - 0.95), color);
  }
  function faceY(list, x, y, z, w, h, fill, stroke) {
    quad(list, P(x, y, z), P(x + w, y, z), P(x + w, y, z + h), P(x, y, z + h), fill, stroke);
  }

  /* ---------- geometría por estación ---------- */
  function geomAgenda() {
    var b = [];
    box(b, 3.5, 8.4, 0, 2.3, 1.15, 1.05, { top: C.woodTop, left: C.wood, right: C.woodDark });
    for (var i = 0; i < 3; i++) flat(b, 3.75 + i * 0.5, 8.6, 1.07, 0.42, 0.55, C.paper, "rgba(11,31,38,.2)");
    box(b, 4.9, 8.55, 1.05, 0.75, 0.12, 0.55, { top: C.screen, left: C.steelDark, right: C.steel });
    box(b, 6.05, 8.85, 0, 0.85, 0.85, 0.45, { top: C.accent, left: C.accentDark, right: "#083f3b" });
    box(b, 6.05, 9.6, 0.45, 0.85, 0.16, 0.95, { top: C.accent, left: C.accentDark, right: "#083f3b" });
    quad(b, P(6.25, 9.35, 0.45), P(6.7, 9.35, 0.45), P(6.7, 9.35, 0.04), P(6.25, 9.35, 0.04), "#e2e8e6");
    person(b, 6.47, 9.25, 1.32, "#0b3b44");
    return { polys: b, anchor: P(4.6, 8.9, 2.15), depth: 8.9 };
  }

  function geomPaciente() {
    var b = [];
    box(b, 3.3, 10.2, 0, 0.9, 0.9, 0.45, { top: "#dcd3c2", left: "#c6bba8", right: "#ab9f8c" });
    box(b, 3.3, 11.0, 0.45, 0.9, 0.16, 0.95, { top: "#dcd3c2", left: "#c6bba8", right: "#ab9f8c" });
    if (paciente.ocupada) {
      quad(b, P(3.5, 10.72, 0.45), P(3.95, 10.72, 0.45), P(3.95, 10.72, 0.04), P(3.5, 10.72, 0.04), "#42585f");
      person(b, 3.72, 10.62, 1.12, "#42585f");
    }
    return { polys: b, anchor: P(3.72, 10.55, 2.1), depth: 10.6 };
  }

  function geomEspera() {
    var b = [];
    box(b, 1.0, 2.85, 0, 3.2, 0.16, 1.0, { top: "#cbb590", left: "#b7a07a", right: "#9c8663" });
    box(b, 1.0, 2.0, 0, 3.2, 0.85, 0.42, { top: "#cbb590", left: "#b7a07a", right: "#9c8663" });
    var total = Math.min(3, Math.max(0, parseInt(paciente.total || 0, 10)));
    for (var i = 0; i < total; i++) {
      var x = 1.5 + i * 0.95;
      var col = i === 0 ? C.skin : C.shirt;
      quad(b, P(x - 0.17, 2.55, 0.42), P(x + 0.17, 2.55, 0.42), P(x + 0.17, 2.55, 0.04), P(x - 0.17, 2.55, 0.04), col);
      person(b, x, 2.55, 1.15, col);
    }
    return { polys: b, anchor: P(2.6, 2.4, 2.0), depth: 2.4 };
  }

  function geomHistoria() {
    var b = [];
    box(b, 0.55, 5.4, 0, 1.35, 1.55, 2.15, { top: C.steelTop, left: C.steel, right: C.steelDark });
    for (var i = 0; i < 3; i++) {
      faceY(b, 0.72, 6.96, 1.62 - i * 0.62, 1.0, 0.5, "#c3ced1", "rgba(11,31,38,.25)");
      quad(b, P(1.1, 6.9, 1.75 - i * 0.62), P(1.35, 6.9, 1.75 - i * 0.62), P(1.35, 6.9, 1.7 - i * 0.62), P(1.1, 6.9, 1.7 - i * 0.62), "#7d8b8f");
    }
    return { polys: b, anchor: P(1.2, 6.3, 3.0), depth: 6.1 };
  }

  function geomPasillo() {
    var b = [];
    quad(b, P(2.6, 0.02, 0.01), P(3.95, 0.02, 0.01), P(3.95, 0.9, 0.01), P(2.6, 0.9, 0.01), "#dfd8c9");
    faceY(b, 2.6, 0.02, 0, 1.35, 2.25, "#0d3138");
    faceY(b, 2.72, 0.05, 0.08, 1.11, 2.05, "#17505b");
    faceY(b, 2.8, 0.07, 1.95, 0.95, 0.12, "#2dd4bf");
    return { polys: b, anchor: P(3.3, 0.3, 2.9), depth: 0.3 };
  }

  var GEOM = { agenda: geomAgenda, espera: geomEspera, historia: geomHistoria };

  /* ---------- montaje ---------- */
  var stations = [];
  Object.keys(GEOM).forEach(function (id) {
    if (!byId[id]) return;
    var g = GEOM[id]();
    g.id = id;
    g.data = byId[id];
    g.bbox = bounds(g.polys.join(""));
    stations.push(g);
  });

  // paciente (sin panel) y pasillo (navegación): sólo si hay datos de espera
  var extra = geomPaciente();
  extra.id = "paciente";
  extra.data = { etiqueta: "Siguiente paciente", aria: paciente.ocupada ? "Siguiente paciente en la silla" : "Silla del paciente vacía", kpis: [], barras: [], acciones: [] };
  extra.bbox = bounds(extra.polys.join(""));
  stations.push(extra);

  var pasillo = geomPasillo();
  pasillo.id = "pasillo";
  pasillo.data = { etiqueta: "Pasillo", aria: "Pasillo hacia recepción y especialidades", kpis: [], barras: [], acciones: [{ texto: "Ir a la agenda", url: (SCENE.urls || {}).citas || "" }] };
  pasillo.bbox = bounds(pasillo.polys.join(""));
  stations.push(pasillo);

  var ordered = stations.slice().sort(function (a, b) { return a.depth - b.depth; });

  var floor = [], walls = [];
  flat(floor, 0, 0, 0, 9, 14, C.floorA);
  for (var i = 0; i <= 9; i++) floor.push('<line x1="' + n(P(i, 0)[0]) + '" y1="' + n(P(i, 0)[1]) + '" x2="' + n(P(i, 14)[0]) + '" y2="' + n(P(i, 14)[1]) + '" stroke="' + C.grid + '"/>');
  for (var j = 0; j <= 14; j++) floor.push('<line x1="' + n(P(0, j)[0]) + '" y1="' + n(P(0, j)[1]) + '" x2="' + n(P(9, j)[0]) + '" y2="' + n(P(9, j)[1]) + '" stroke="' + C.grid + '"/>');
  quad(walls, P(0, 0, 0), P(0, 14, 0), P(0, 14, 3.4), P(0, 0, 3.4), C.wallL);
  quad(walls, P(0, 0, 0), P(9, 0, 0), P(9, 0, 3.4), P(0, 0, 3.4), C.wallB);

  var markup = '<g class="xm-scene-floor">' + floor.join("") + '</g><g class="xm-scene-walls">' + walls.join("") + "</g>";
  ordered.forEach(function (st) {
    markup += '<g class="xm-scene-station" data-station="' + st.id + '" role="button" tabindex="0" aria-label="' +
      (st.data.aria || st.data.etiqueta) + '" aria-controls="xm-scene-panel">' +
      '<g class="xm-scene-halo">' + st.polys.join("") + "</g>" +
      '<g class="xm-scene-body">' + st.polys.join("") + "</g>" +
      '<polygon class="xm-scene-hit" points="' + hit(st.bbox) + '"/></g>';
  });
  svg.innerHTML = markup;
  // el halo reutiliza los polígonos: se le da color y opacidad por CSS
  svg.querySelectorAll(".xm-scene-halo polygon").forEach(function (p) { p.setAttribute("fill", C.accent); p.setAttribute("opacity", ".16"); });

  function bounds(html) {
    var re = /([-\d.]+),([-\d.]+)/g, m, minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    while ((m = re.exec(html))) {
      var x = parseFloat(m[1]), y = parseFloat(m[2]);
      if (x < minX) minX = x; if (y < minY) minY = y;
      if (x > maxX) maxX = x; if (y > maxY) maxY = y;
    }
    return { minX: minX, minY: minY, maxX: maxX, maxY: maxY };
  }
  function hit(b) { var p = 10; return pts([[b.minX - p, b.minY - p], [b.maxX + p, b.minY - p], [b.maxX + p, b.maxY + p], [b.minX - p, b.maxY + p]]); }

  var labelEls = {};
  stations.forEach(function (st) {
    var el = document.createElement("div");
    el.className = "xm-scene-label";
    el.innerHTML = "<b>" + st.data.etiqueta + "</b>";
    el._anchor = st.anchor;
    labelsBox.appendChild(el);
    labelEls[st.id] = el;
  });

  /* ---------- cámara ---------- */
  var world = bounds(svg.innerHTML);
  var view = { x: 0, y: 0, w: 1, h: 1 };
  var raf = null;
  function compact() { return window.matchMedia("(max-width: 900px)").matches; }
  function viewFor(b, pad) {
    pad = pad == null ? (compact() ? 8 : 34) : pad;
    return { x: b.minX - pad, y: b.minY - pad, w: Math.max(b.maxX - b.minX + pad * 2, 240), h: Math.max(b.maxY - b.minY + pad * 2, 180) };
  }
  function homeView() { return viewFor(world); }

  function setCamera(target, animate) {
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!animate || reduce) {
      view = target;
      svg.setAttribute("viewBox", n(view.x) + " " + n(view.y) + " " + n(view.w) + " " + n(view.h));
      placeLabels();
      return;
    }
    var from = { x: view.x, y: view.y, w: view.w, h: view.h }, t0 = performance.now(), dur = 450;
    cancelAnimationFrame(raf);
    (function step(t) {
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      ["x", "y", "w", "h"].forEach(function (key) { view[key] = from[key] + (target[key] - from[key]) * e; });
      svg.setAttribute("viewBox", n(view.x) + " " + n(view.y) + " " + n(view.w) + " " + n(view.h));
      placeLabels();
      if (k < 1) raf = requestAnimationFrame(step);
    })(t0);
  }

  function placeLabels() {
    var vb = svg.viewBox.baseVal, rect = svg.getBoundingClientRect();
    if (!rect.width || !vb.width) return;
    stations.forEach(function (st) {
      var el = labelEls[st.id], a = st.anchor;
      el.style.left = ((a[0] - vb.x) / vb.width) * rect.width + "px";
      el.style.top = ((a[1] - vb.y) / vb.height) * rect.height + "px";
      var inView = a[0] >= vb.x && a[0] <= vb.x + vb.width;
      el.style.display = inView && (!compact() || el.classList.contains("is-visible")) ? "" : "none";
    });
  }

  /* ---------- panel ---------- */
  function renderPanel(st) {
    var d = st.data;
    document.getElementById("xm-scene-kicker").textContent = (SCENE.perfil || "") + (SCENE.especialidad ? " · " + SCENE.especialidad : "");
    document.getElementById("xm-scene-title").textContent = d.etiqueta;
    document.getElementById("xm-scene-lead").textContent = d.lead || "";
    var html = '<div class="xm-scene-kpis">' + (d.kpis || []).map(function (k) {
      return '<div class="xm-scene-kpi"><span>' + k.etiqueta + "</span><strong>" + k.valor + "</strong></div>";
    }).join("") + "</div>";
    html += (d.barras || []).map(function (b) {
      return '<div class="xm-scene-bar"><div class="t"><span>' + b.etiqueta + "</span><span>" + b.valor + "</span></div>" +
        '<div class="track"><span class="fill' + (/^\+/.test(b.etiqueta) ? " warn" : "") + '" style="width:' + b.pct + '%"></span></div></div>';
    }).join("");
    document.getElementById("xm-scene-body").innerHTML = html;
    document.getElementById("xm-scene-actions").innerHTML = (d.acciones || []).map(function (a, i) {
      return a.url ? '<a class="btn btn-sm ' + (i ? "btn-outline" : "btn-primary") + '" href="' + a.url + '">' + a.texto + "</a>" : "";
    }).join("");
  }

  var lastFocus = null;
  function openStation(id, trigger) {
    var st = stations.filter(function (s) { return s.id === id; })[0];
    if (!st) return;
    if (!(st.data.kpis || []).length && !(st.data.acciones || []).length) return; // sin panel propio
    lastFocus = trigger || lastFocus;
    svg.querySelectorAll(".xm-scene-station").forEach(function (el) {
      var on = el.getAttribute("data-station") === id;
      el.classList.toggle("is-hot", on);
      el.setAttribute("aria-expanded", on ? "true" : "false");
      if (labelEls[el.getAttribute("data-station")]) labelEls[el.getAttribute("data-station")].classList.toggle("is-visible", on);
    });
    renderPanel(st);
    panel.hidden = false;
    root.classList.add("is-open");
    setCamera(viewFor(st.bbox, compact() ? 22 : 70), true);
    document.getElementById("xm-scene-title").focus({ preventScroll: true });
  }

  function closeStation(returnFocus) {
    panel.hidden = true;
    root.classList.remove("is-open");
    svg.querySelectorAll(".xm-scene-station").forEach(function (el) {
      el.classList.remove("is-hot");
      el.setAttribute("aria-expanded", "false");
      if (labelEls[el.getAttribute("data-station")]) labelEls[el.getAttribute("data-station")].classList.remove("is-visible");
    });
    setCamera(homeView(), true);
    if (returnFocus && lastFocus) lastFocus.focus();
  }

  svg.addEventListener("click", function (e) {
    var st = e.target.closest(".xm-scene-station");
    if (st) openStation(st.getAttribute("data-station"), st);
  });
  svg.addEventListener("keydown", function (e) {
    var st = e.target.closest(".xm-scene-station");
    if (!st) return;
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openStation(st.getAttribute("data-station"), st); }
  });
  svg.addEventListener("mouseover", function (e) {
    var st = e.target.closest(".xm-scene-station");
    if (st && labelEls[st.getAttribute("data-station")]) { labelEls[st.getAttribute("data-station")].classList.add("is-visible"); placeLabels(); }
  });
  svg.addEventListener("mouseout", function (e) {
    var st = e.target.closest(".xm-scene-station");
    if (st && !st.classList.contains("is-hot") && labelEls[st.getAttribute("data-station")]) {
      labelEls[st.getAttribute("data-station")].classList.remove("is-visible"); placeLabels();
    }
  });
  svg.addEventListener("focusin", function (e) {
    var st = e.target.closest(".xm-scene-station");
    if (st && labelEls[st.getAttribute("data-station")]) { labelEls[st.getAttribute("data-station")].classList.add("is-visible"); placeLabels(); }
  });
  svg.addEventListener("focusout", function (e) {
    var st = e.target.closest(".xm-scene-station");
    if (st && !st.classList.contains("is-hot") && labelEls[st.getAttribute("data-station")]) {
      labelEls[st.getAttribute("data-station")].classList.remove("is-visible"); placeLabels();
    }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) closeStation(true); });
  document.getElementById("xm-scene-close").addEventListener("click", function () { closeStation(true); });

  document.getElementById("xm-scene-toggle").addEventListener("click", function (e) {
    table.hidden = !table.hidden;
    root.classList.toggle("is-table", !table.hidden);
    e.target.textContent = table.hidden ? "Ver como tabla" : "Volver a la escena";
    if (!table.hidden) panel.hidden = true;
  });

  var r = svg.getBoundingClientRect();
  svg.setAttribute("viewBox", "0 0 " + (r.width || 900) + " " + (r.height || 640));
  setCamera(homeView(), false);
  window.addEventListener("resize", function () {
    if (panel.hidden) setCamera(homeView(), false); else placeLabels();
  });
  placeLabels();
})();
