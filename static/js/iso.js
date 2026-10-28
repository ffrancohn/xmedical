/* ============================================================
   XMEDICAL · ATLAS — isometric scene renderer
   Vanilla JS. Draws SVG scenes from a small geometric DSL.
   ============================================================ */
(function () {
  "use strict";

  const COS = Math.cos(Math.PI / 6);
  const SIN = 0.5;
  const S = 6; // world unit -> svg units
  const T = {
    floor: "#174850",
    floorSide: "#0e3038",
    wallA: "#17434d",
    wallB: "#11353e",
    edge: "rgba(94,234,212,.58)",
    edgeSoft: "rgba(94,234,212,.32)",
    grid: "rgba(94,234,212,.14)",
    ink: "#e2f0ec",
    dim: "rgba(226,240,236,.45)",
    accent: "#5eead4",
    coral: "#e5765d",
    gold: "#e7b85c",
    teal: "#2dd4bf",
    blue: "#71b4d8",
    violet: "#b3a3e9",
    green: "#75c9a4"
  };

  const f = (n) => Number(n.toFixed(2));

  function P(x, y, z = 0) {
    return [(x - y) * COS * S, (x + y) * SIN * S - z * S];
  }

  class Scene {
    constructor() {
      this.body = "";
      this.minX = Infinity;
      this.minY = Infinity;
      this.maxX = -Infinity;
      this.maxY = -Infinity;
    }
    track(x, y) {
      if (x < this.minX) this.minX = x;
      if (y < this.minY) this.minY = y;
      if (x > this.maxX) this.maxX = x;
      if (y > this.maxY) this.maxY = y;
    }
    trackPts(pts) {
      pts.forEach((p) => this.track(p[0], p[1]));
    }
    add(markup) {
      this.body += markup;
      return this;
    }
    poly(pts, fill, opt = {}) {
      const str = pts.map((p) => `${f(p[0])},${f(p[1])}`).join(" ");
      this.trackPts(pts);
      const stroke = opt.stroke || "none";
      const sw = opt.sw == null ? 0.55 : opt.sw;
      const op = opt.opacity == null ? 1 : opt.opacity;
      const cls = opt.cls ? ` class="${opt.cls}"` : "";
      return this.add(
        `<polygon points="${str}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" opacity="${op}"${cls}/>`
      );
    }
    line(a, b, stroke, opt = {}) {
      const pa = P(a[0], a[1], a[2] || 0);
      const pb = P(b[0], b[1], b[2] || 0);
      this.trackPts([pa, pb]);
      const sw = opt.sw == null ? 0.5 : opt.sw;
      const dash = opt.dash ? ` stroke-dasharray="${opt.dash}"` : "";
      const op = opt.opacity == null ? 1 : opt.opacity;
      return this.add(
        `<line x1="${f(pa[0])}" y1="${f(pa[1])}" x2="${f(pb[0])}" y2="${f(pb[1])}" stroke="${stroke}" stroke-width="${sw}" opacity="${op}"${dash} stroke-linecap="round"/>`
      );
    }
    text(x, y, str, opt = {}) {
      const anchor = opt.anchor || "start";
      const size = opt.size || 7;
      const cls = opt.cls || "iso-label";
      const fill = opt.fill ? ` fill="${opt.fill}"` : "";
      const approx = str.length * size * 0.62;
      const left = anchor === "middle" ? x - approx / 2 : anchor === "end" ? x - approx : x;
      this.track(left, y - size);
      this.track(left + approx, y + 2);
      return this.add(
        `<text x="${f(x)}" y="${f(y)}" text-anchor="${anchor}" font-size="${size}" class="${cls}"${fill}>${str}</text>`
      );
    }
    label(x, y, z, title, sub, opt = {}) {
      const p = P(x, y, z);
      const anchor = opt.anchor || "middle";
      const dy = opt.dy || 0;
      const top = p[1] + dy;
      const width = Math.max(title.length * 6.4, (sub || "").length * 3.6);
      const left = anchor === "middle" ? p[0] - width / 2 : p[0] - (anchor === "end" ? width : 0);
      this.track(left, top - 12);
      this.track(left + width, top + 9);
      let s = `<g class="iso-tag">`;
      if (opt.leader !== false) {
        s += `<line class="iso-leader" x1="${f(p[0])}" y1="${f(p[1])}" x2="${f(p[0])}" y2="${f(top + 7)}"/>`;
        s += `<circle cx="${f(p[0])}" cy="${f(p[1])}" r="1.6" fill="${opt.accent || T.coral}"/>`;
      }
      if (opt.num) {
        s += `<rect x="${f(left - 13)}" y="${f(top - 12.6)}" width="9.6" height="9.6" rx="1.7" fill="${opt.accent || T.coral}"/>`;
        s += `<text x="${f(left - 8.2)}" y="${f(top - 5)}" text-anchor="middle" font-size="5.7" fill="#08171d" font-family="IBM Plex Mono,monospace" font-weight="600">${opt.num}</text>`;
      }
      s += `<text x="${f(p[0])}" y="${f(top - 3)}" text-anchor="${anchor}" font-size="${opt.size || 8.8}" class="iso-room-label">${title}</text>`;
      if (sub) {
        s += `<text x="${f(p[0])}" y="${f(top + 7.2)}" text-anchor="${anchor}" font-size="6" class="iso-sub">${sub}</text>`;
      }
      s += `</g>`;
      return this.add(s);
    }
    viewBox(pad = 18) {
      const w = this.maxX - this.minX;
      const h = this.maxY - this.minY;
      return `${f(this.minX - pad)} ${f(this.minY - pad)} ${f(w + pad * 2)} ${f(h + pad * 2)}`;
    }
  }

  /* ---------- primitives ---------- */
  function box(s, o) {
    const { x, y, w, d, h = 0, z = 0 } = o;
    const top = o.top || T.floor;
    const sideA = o.sideA || o.side1 || T.floorSide;
    const sideB = o.sideB || o.side2 || T.wallB;
    const stroke = o.stroke === null ? "none" : o.stroke || T.edgeSoft;
    const sw = o.sw == null ? 0.62 : o.sw;
    const op = o.opacity == null ? 1 : o.opacity;
    const zt = z + h;
    const faceA = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, zt), P(x + w, y, zt)];
    const faceB = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, zt), P(x, y + d, zt)];
    const topFace = [P(x, y, zt), P(x + w, y, zt), P(x + w, y + d, zt), P(x, y + d, zt)];
    s.poly(faceA, sideA, { stroke, sw, opacity: op });
    s.poly(faceB, sideB, { stroke, sw, opacity: op });
    s.poly(topFace, top, { stroke, sw, opacity: op });
    if (o.highlight) {
      const inner = [P(x + 0.8, y + 0.8, zt), P(x + w - 0.8, y + 0.8, zt), P(x + w - 0.8, y + d - 0.8, zt), P(x + 0.8, y + d - 0.8, zt)];
      s.poly(inner, "none", { stroke: o.highlight, sw: 0.5, opacity: 0.8 });
    }
  }

  function slab(s, o) {
    const { x, y, w, d, z = 0, t = 2.4 } = o;
    const top = o.top || T.floor;
    const sideA = o.sideA || T.floorSide;
    const sideB = o.sideB || "#081d23";
    const stroke = o.stroke || T.edgeSoft;
    s.poly([P(x, y, z), P(x + w, y, z), P(x + w, y + d, z), P(x, y + d, z)], top, { stroke, sw: 0.55 });
    s.poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z - t), P(x + w, y, z - t)], sideA, { stroke, sw: 0.45 });
    s.poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z - t), P(x, y + d, z - t)], sideB, { stroke, sw: 0.45 });
  }

  function wallY(s, x, y, w, h, o = {}) {
    const c = o.color || T.wallA;
    const e = o.edge || T.edgeSoft;
    s.poly([P(x, y, 0), P(x + w, y, 0), P(x + w, y, h), P(x, y, h)], c, { stroke: e, sw: 0.55 });
    if (o.trim !== false) {
      s.line([x, y, h], [x + w, y, h], o.trimColor || T.edge, { sw: 0.6 });
    }
    if (o.windows) {
      const count = Math.max(1, Math.floor(w / 7));
      const step = w / count;
      for (let i = 0; i < count; i++) {
        const wx = x + step * i + step * 0.24;
        const ww = step * 0.5;
        s.poly([P(wx, y, h * 0.34), P(wx + ww, y, h * 0.34), P(wx + ww, y, h * 0.78), P(wx, y, h * 0.78)], "rgba(94,234,212,.1)", { stroke: "rgba(94,234,212,.32)", sw: 0.45 });
      }
    }
  }

  function wallX(s, x, y, d, h, o = {}) {
    const c = o.color || T.wallB;
    const e = o.edge || T.edgeSoft;
    s.poly([P(x, y, 0), P(x, y + d, 0), P(x, y + d, h), P(x, y, h)], c, { stroke: e, sw: 0.55 });
    if (o.trim !== false) {
      s.line([x, y, h], [x, y + d, h], o.trimColor || T.edge, { sw: 0.6 });
    }
  }

  function floorGrid(s, x, y, w, d, step = 4.5) {
    for (let i = step; i < w; i += step) {
      s.line([x + i, y, 0.02], [x + i, y + d, 0.02], T.grid, { sw: 0.35 });
    }
    for (let j = step; j < d; j += step) {
      s.line([x, y + j, 0.02], [x + w, y + j, 0.02], T.grid, { sw: 0.35 });
    }
  }

  function room(s, o) {
    const { x, y, w, d, h = 9, label, sub, num, accent } = o;
    slab(s, { x, y, w, d, z: 0, t: o.t || 2.6, top: o.floor || T.floor, sideA: o.sideA, sideB: o.sideB, stroke: o.edge || T.edgeSoft });
    floorGrid(s, x, y, w, d, o.gridStep || 4.2);
    // inner rug / accent path
    if (o.rug !== false) {
      const inset = 2.2;
      s.poly(
        [P(x + inset, y + inset, 0.05), P(x + w - inset, y + inset, 0.05), P(x + w - inset, y + d - inset, 0.05), P(x + inset, y + d - inset, 0.05)],
        o.rugColor || "rgba(94,234,212,.035)",
        { stroke: o.rugStroke || "rgba(94,234,212,.09)", sw: 0.4 }
      );
    }
    wallY(s, x, y, w, h, { color: o.wallA, windows: o.windows, edge: o.wallEdge });
    wallX(s, x, y, d, h, { color: o.wallB, edge: o.wallEdge });
    // corner column
    s.line([x, y, 0], [x, y, h], "rgba(94,234,212,.5)", { sw: 0.8 });
    if (label) {
      s.label(x + w / 2, y + d / 2, h + 8, label, sub, { num, accent: accent || T.coral, size: o.labelSize || 8.2 });
    }
  }

  /* ---------- props ---------- */
  function desk(s, x, y, w = 9, d = 4, z = 0, color = "#24616a") {
    box(s, { x, y, w, d, h: 3, z, top: color, sideA: "#1a4a52", sideB: "#153f47", stroke: "rgba(94,234,212,.34)" });
    // legs
    const lc = "rgba(94,234,212,.24)";
    s.line([x + 0.7, y + 0.7, 0], [x + 0.7, y + 0.7, 3], lc, { sw: 0.4 });
    s.line([x + w - 0.7, y + d - 0.7, 0], [x + w - 0.7, y + d - 0.7, 3], lc, { sw: 0.4 });
  }

  function monitor(s, x, y, z, w = 5.4, color = T.accent, ecg = false) {
    box(s, { x: x + 0.6, y, w: 0.35, d: 0.35, h: 2.4, z, top: "#1c4d55", sideA: "#17434b", sideB: "#12363e", stroke: T.edgeSoft });
    box(s, { x, y, w, d: 0.55, h: 3.2, z: z + 2.4, top: "#0b262e", sideA: "#0b262e", sideB: "#0b262e", stroke: "rgba(94,234,212,.48)" });
    const sp = [P(x + 0.35, y + 0.56, z + 2.6), P(x + w - 0.35, y + 0.56, z + 2.6), P(x + w - 0.35, y + 0.56, z + 5.1), P(x + 0.35, y + 0.56, z + 5.1)];
    s.poly(sp, "rgba(94,234,212,.17)", { stroke: "rgba(94,234,212,.68)", sw: 0.35 });
    if (ecg) {
      const a = P(x + 0.6, y + 0.58, z + 4.2);
      const b = P(x + 1.6, y + 0.58, z + 4.2);
      const c = P(x + 2.2, y + 0.58, z + 4.6);
      const d2 = P(x + 2.8, y + 0.58, z + 3.8);
      const e = P(x + 3.6, y + 0.58, z + 4.2);
      const f2 = P(x + w - 0.6, y + 0.58, z + 4.2);
      s.add(
        `<path d="M${f(a[0])} ${f(a[1])} L${f(b[0])} ${f(b[1])} L${f(c[0])} ${f(c[1])} L${f(d2[0])} ${f(d2[1])} L${f(e[0])} ${f(e[1])} L${f(f2[0])} ${f(f2[1])}" class="iso-ecg"/>`
      );
    }
  }

  function chair(s, x, y, z = 0, color = "#2e7079", face = "y") {
    box(s, { x, y, w: 3.4, d: 3.4, h: 0.7, z: z + 1.5, top: color, sideA: "#164049", sideB: "#11343c", stroke: "rgba(94,234,212,.26)" });
    if (face === "y") {
      box(s, { x, y: y + 2.7, w: 3.4, d: 0.55, h: 3.4, z: z + 0.4, top: color, sideA: "#164049", sideB: "#12343b", stroke: "rgba(94,234,212,.22)" });
    } else {
      box(s, { x: x + 2.7, y, w: 0.55, d: 3.4, h: 3.4, z: z + 0.4, top: color, sideA: "#164049", sideB: "#12343b", stroke: "rgba(94,234,212,.22)" });
    }
    const lc = "rgba(94,234,212,.22)";
    s.line([x + 0.5, y + 0.5, 0], [x + 0.5, y + 0.5, 1.5], lc, { sw: 0.35 });
    s.line([x + 2.9, y + 2.9, 0], [x + 2.9, y + 2.9, 1.5], lc, { sw: 0.35 });
  }

  function bench(s, x, y, w = 12, d = 3, color = "#2a626b") {
    box(s, { x, y, w, d, h: 1.8, z: 0.2, top: color, sideA: "#1f4d55", sideB: "#19434b", stroke: "rgba(94,234,212,.28)" });
    box(s, { x, y: y + d - 0.5, w, d: 0.5, h: 3.4, z: 0, top: color, sideA: "#1f4d55", sideB: "#19434b", stroke: "rgba(94,234,212,.24)" });
  }

  function bed(s, x, y, w = 14, d = 5.6, color = "#2b6b74") {
    box(s, { x, y, w, d, h: 2.2, z: 0, top: color, sideA: "#1d4c54", sideB: "#17434b", stroke: "rgba(94,234,212,.34)" });
    box(s, { x: x + 0.8, y: y + 0.6, w: w - 1.6, d: d - 1.2, h: 1.1, z: 2.2, top: "#3d8087", sideA: "#2f6a72", sideB: "#275e66", stroke: "rgba(94,234,212,.24)" });
    box(s, { x: x + 1.2, y: y + 0.9, w: 3.6, d: d - 1.8, h: 0.8, z: 3.3, top: "#a9d2d0", sideA: "#84b3b3", sideB: "#6f9fa2", stroke: "rgba(226,240,236,.3)" });
  }

  function plant(s, x, y, z = 0, size = 1) {
    box(s, { x, y, w: 2.6 * size, d: 2.6 * size, h: 2.6 * size, z, top: "#2b5a4a", sideA: "#1f463b", sideB: "#193b32", stroke: "rgba(117,201,164,.32)" });
    const p = P(x + 1.3 * size, y + 1.3 * size, z + 2.8 * size);
    s.add(
      `<g opacity=".82"><ellipse cx="${f(p[0])}" cy="${f(p[1] - 6 * size)}" rx="${f(3.4 * size)}" ry="${f(1.5 * size)}" fill="#2f7f5f" transform="rotate(-28 ${f(p[0])} ${f(p[1] - 6 * size)})"/><ellipse cx="${f(p[0] + 2.2 * size)}" cy="${f(p[1] - 3.4 * size)}" rx="${f(3.2 * size)}" ry="${f(1.4 * size)}" fill="#3f9d77" transform="rotate(38 ${f(p[0] + 2.2 * size)} ${f(p[1] - 3.4 * size)})"/><ellipse cx="${f(p[0] - 2.1 * size)}" cy="${f(p[1] - 3 * size)}" rx="${f(2.9 * size)}" ry="${f(1.3 * size)}" fill="#347f64" transform="rotate(28 ${f(p[0] - 2.1 * size)} ${f(p[1] - 3 * size)})"/></g>`
    );
  }

  function person(s, x, y, z = 0, color = T.coral, opts = {}) {
    const p = P(x, y, z);
    const h = opts.h || 15;
    const r = opts.r || 3.1;
    s.track(p[0] - 6, p[1] - h - 3);
    s.track(p[0] + 6, p[1] + 3);
    s.add(
      `<g class="iso-person" opacity="${opts.opacity || 0.95}">` +
        `<ellipse cx="${f(p[0])}" cy="${f(p[1] + 0.5)}" rx="5.4" ry="2.1" fill="rgba(0,0,0,.28)"/>` +
        `<path d="M${f(p[0] - 4.4)} ${f(p[1])} Q${f(p[0] - 4.8)} ${f(p[1] - 9)} ${f(p[0])} ${f(p[1] - 9.6)} Q${f(p[0] + 4.8)} ${f(p[1] - 9)} ${f(p[0] + 4.4)} ${f(p[1])} Z" fill="${color}"/>` +
        `<circle cx="${f(p[0])}" cy="${f(p[1] - 12.4)}" r="${r}" fill="${color}"/>` +
        `<circle cx="${f(p[0])}" cy="${f(p[1] - 12.4)}" r="${r}" fill="none" stroke="rgba(8,23,29,.3)" stroke-width=".6"/>` +
      `</g>`
    );
  }

  function board(s, x, y, z, w = 9, h = 5, accent = T.accent) {
    box(s, { x, y, w, d: 0.6, h, z, top: "#0a2229", sideA: "#0a2229", sideB: "#0a2229", stroke: "rgba(94,234,212,.3)" });
    const pts = [P(x + 0.6, y + 0.62, z + 0.8), P(x + w - 0.6, y + 0.62, z + 0.8), P(x + w - 0.6, y + 0.62, z + h - 0.7), P(x + 0.6, y + 0.62, z + h - 0.7)];
    s.poly(pts, "rgba(94,234,212,.07)", { stroke: "rgba(94,234,212,.35)", sw: 0.35 });
    const base = P(x + w * 0.25, y + 0.64, z + 0.9);
    for (let i = 0; i < 4; i++) {
      const bh = (0.9 + i * 0.75) * (h / 5);
      s.add(`<rect x="${f(base[0] + i * 6)}" y="${f(base[1] - bh * S)}" width="2.4" height="${f(bh * S)}" fill="${accent}" opacity=".55" rx=".5"/>`);
    }
  }

  function counter(s, x, y, w = 12, d = 3.4) {
    box(s, { x, y, w, d, h: 4.2, z: 0, top: "#1d515a", sideA: "#143d45", sideB: "#10343c", stroke: "rgba(94,234,212,.34)" });
    box(s, { x, y: y - 0.8, w, d: 0.8, h: 0.5, z: 4.2, top: "#2c6870", sideA: "#21545c", sideB: "#1b474f", stroke: "rgba(94,234,212,.2)" });
  }

  function shelves(s, x, y, w = 4, d = 9, h = 10) {
    box(s, { x, y, w, d, h, z: 0, top: "#153f47", sideA: "#0f333a", sideB: "#0b2a31", stroke: "rgba(94,234,212,.28)" });
    for (let i = 1; i < 4; i++) {
      s.line([x + 0.4, y + 0.4, (h / 4) * i], [x + w - 0.4, y + d - 0.4, (h / 4) * i], "rgba(94,234,212,.16)", { sw: 0.4 });
    }
  }

  function icon(s, x, y, z, type, color = T.accent) {
    const p = P(x, y, z);
    const c = f(p[0]), cy = f(p[1]);
    s.track(c - 6, cy - 6);
    s.track(c + 6, cy + 6);
    const g = (inner) => `<g transform="translate(${c},${cy})" stroke="${color}" fill="none" stroke-width=".9" stroke-linecap="round" stroke-linejoin="round" opacity=".85">${inner}</g>`;
    let inner = "";
    if (type === "users") inner = `<circle cx="-2.2" cy="-2" r="1.8"/><path d="M-5.4 4c.3-2.2 1.5-3.4 3.2-3.4s2.9 1.2 3.2 3.4"/><path d="M2.2 -3.8a1.9 1.9 0 0 1 0 3.6M3.1 1.1c1.4.2 2.2 1.2 2.4 2.9"/>`;
    else if (type === "calendar") inner = `<rect x="-5" y="-4.2" width="10" height="9" rx="1.2"/><path d="M-5 -1.6H5M-2.8-6v2.4M2.8-6v2.4"/>`;
    else if (type === "heart") inner = `<path d="M0 5.2C-4.8 1.4-6-1.2-4.4-3.2c1.4-1.7 3.4-.8 4.4.8 1-1.6 3-2.5 4.4-.8C6-1.2 4.8 1.4 0 5.2Z"/>`;
    else if (type === "stethoscope") inner = `<path d="M-4.4-5v3.2a3.1 3.1 0 0 0 6.2 0V-5"/><path d="M-1.3 1.4v2a3.7 3.7 0 0 0 7.4 0V1.6"/><circle cx="6.3" cy="0" r="1.5"/>`;
    else if (type === "share") inner = `<circle cx="-4" cy="1" r="1.8"/><circle cx="4" cy="-4" r="1.8"/><circle cx="4" cy="5" r="1.8"/><path d="m-2.2.2 4.6-3M-2.2 1.8l4.6 2.4"/>`;
    else if (type === "qr") inner = `<rect x="-4.8" y="-4.8" width="4" height="4" rx=".4"/><rect x="1" y="-4.8" width="4" height="4" rx=".4"/><rect x="-4.8" y="1" width="4" height="4" rx=".4"/><path d="M1 1h1.6v1.6H1zM4 1h1.2M1 4v1.2M4 4h1.2v1.2"/>`;
    else if (type === "shield") inner = `<path d="M0-6 5-3.8V.4C5 4 2.8 5.8 0 6.6-2.8 5.8-5 4-5 .4v-4.2L0-6Z"/><path d="m-2 1 1.4 1.4L2.6-1"/>`;
    s.add(g(inner));
  }

  /* ---------- shared room compositions ---------- */
  const W = 26, D = 19;

  function clinicRoomReception(s, x, y) {
    room(s, { x, y, w: W, d: D, h: 9.5, label: "Recepción", sub: "", num: "01", accent: T.gold });
    counter(s, x + 3.2, y + 4.2, 12, 3.2);
    monitor(s, x + 5.2, y + 3.7, 4.7, 4.4);
    chair(s, x + 19, y + 8, 0, "#255962", "x");
    person(s, x + 20.6, y + 10.2, 0, T.gold);
    person(s, x + 8.2, y + 9.8, 0, T.teal, { opacity: 0.55 });
    plant(s, x + 2.2, y + 14.6, 0, 0.9);
    s.label(x + W / 2, y + D + 2, 0, "", "", { leader: false, size: 0.1 });
  }

  function clinicRoomWaiting(s, x, y) {
    room(s, { x, y, w: 22, d: D, h: 8, label: "Sala de espera", sub: "", num: "02", accent: T.teal });
    bench(s, x + 2.6, y + 4, 12.5, 2.8);
    bench(s, x + 2.6, y + 8.6, 12.5, 2.8);
    person(s, x + 6, y + 5.5, 0, T.teal, { opacity: 0.7 });
    person(s, x + 11.4, y + 10.2, 0, T.coral, { opacity: 0.8 });
    plant(s, x + 18.3, y + 3.2, 0, 1.15);
    board(s, x + 15.2, y + 0.4, 4.5, 6.2, 4.2, T.teal);
  }

  function clinicRoomPreclinic(s, x, y) {
    room(s, { x, y, w: 22, d: D, h: 9.5, label: "Preclínica", sub: "", num: "03", accent: T.coral });
    bed(s, x + 2.2, y + 4, 13.5, 5.2);
    monitor(s, x + 17.4, y + 4, 0, 3.8, T.coral, true);
    person(s, x + 9, y + 11.4, 0, T.coral);
    person(s, x + 16, y + 12.8, 0, T.teal, { opacity: 0.8 });
    plant(s, x + 2.3, y + 14.8, 0, 0.8);
  }

  function clinicRoomConsult(s, x, y) {
    room(s, { x, y, w: 27, d: 22, h: 10, label: "Consulta", sub: "", num: "04", accent: T.teal });
    desk(s, x + 4, y + 5, 12.5, 4.4, 0, "#1a4b52");
    monitor(s, x + 7.4, y + 4.2, 3, 6.4, T.teal, false);
    chair(s, x + 4.2, y + 11.4, 0, "#255962", "y");
    chair(s, x + 13.2, y + 10.8, 0, "#2a5e66", "y");
    person(s, x + 5.1, y + 12.7, 0, T.teal);
    person(s, x + 14.6, y + 12.2, 0, T.coral);
    bed(s, x + 4.2, y + 16, 13.5, 4.6);
    board(s, x + 18.4, y + 0.5, 4.6, 6, 4.4, T.teal);
    plant(s, x + 24.2, y + 17.2, 0, 0.8);
  }

  function clinicRoomLabs(s, x, y) {
    room(s, { x, y, w: 26, d: 22, h: 8.5, label: "Salida · QR", sub: "", num: "05", accent: T.gold });
    counter(s, x + 3.2, y + 4, 13, 3.4);
    monitor(s, x + 5, y + 3.5, 4.3, 4.2, T.gold);
    shelves(s, x + 19.2, y + 3, 3.6, 9, 9.5);
    person(s, x + 7.6, y + 9.6, 0, T.gold);
    person(s, x + 15.6, y + 12, 0, T.teal, { opacity: 0.75 });
    plant(s, x + 3, y + 17.2, 0, 0.9);
  }

  function clinicRoomReferrals(s, x, y) {
    room(s, { x, y, w: 22, d: 22, h: 8.5, label: "Referencias", sub: "", num: "06", accent: T.violet });
    desk(s, x + 3, y + 4, 10.5, 4);
    monitor(s, x + 4.8, y + 3.4, 3, 5.2, T.violet);
    chair(s, x + 12, y + 4.8, 0, "#3a3560", "x");
    person(s, x + 9, y + 10.4, 0, T.violet);
    board(s, x + 15.4, y + 0.4, 4.4, 7, 4.4, T.violet);
    shelves(s, x + 17.8, y + 14.4, 3.4, 5, 6.5);
  }

  /* ---------- scenes ---------- */
  const scenes = {};

  scenes.hero = (s) => {
    const ox = 0, oy = 0;
    clinicRoomReception(s, ox, oy);
    clinicRoomWaiting(s, ox + 29, oy);
    clinicRoomPreclinic(s, ox + 54, oy);
    clinicRoomConsult(s, ox + 54, oy + 25);
    clinicRoomLabs(s, ox, oy + 25);
    // the cover already carries the narrative: keep the model clean
    s.body = s.body.replace(/<g class="iso-tag">[\s\S]*?<\/g>/g, "");
    // route
    const pts = [
      [11, -3, 0.4], [11, 9, 0.4], [40, 9, 0.4], [63, 9, 0.4], [68, 35, 0.4], [13, 37, 0.4], [11, 49, 0.4]
    ].map((p) => P(p[0], p[1], p[2]));
    const d = `M${pts.map((p) => `${f(p[0])},${f(p[1])}`).join(" L")}`;
    s.add(`<path d="${d}" class="iso-route-base"/><path d="${d}" class="iso-route"/>`);
    const dot = pts[0];
    s.add(`<g opacity=".55"><circle cx="${f(dot[0])}" cy="${f(dot[1])}" r="7" fill="none" stroke="rgba(229,118,93,.35)"/><circle cx="${f(dot[0])}" cy="${f(dot[1])}" r="3" fill="none" stroke="rgba(229,118,93,.3)"/></g>`);
  };

  scenes.clinic = (s) => {
    clinicRoomReception(s, 0, 0);
    clinicRoomWaiting(s, 29, 0);
    clinicRoomPreclinic(s, 54, 0);
    clinicRoomConsult(s, 54, 25);
    clinicRoomLabs(s, 0, 25);
    clinicRoomReferrals(s, 29, 25);
    const pts = [
      [7, -5, 0.6], [7, 8, 0.6], [36, 8, 0.6], [61, 8, 0.6], [67, 33, 0.6], [14, 36, 0.6], [13, 51, 0.6]
    ].map((p) => P(p[0], p[1], p[2]));
    const d = `M${f(pts[0][0])},${f(pts[0][1])} ` + pts.slice(1).map((p) => `L${f(p[0])},${f(p[1])}`).join(" ");
    s.add(`<path d="${d}" class="iso-route-base"/><path d="${d}" class="iso-route"/>`);
    // start pin
    s.add(`<g><circle cx="${f(pts[0][0])}" cy="${f(pts[0][1])}" r="4.2" fill="#e5765d"/><circle cx="${f(pts[0][0])}" cy="${f(pts[0][1])}" r="9" fill="none" stroke="rgba(229,118,93,.35)"/></g>`);
    // exit pin
    const last = pts[pts.length - 1];
    s.add(`<g><circle cx="${f(last[0])}" cy="${f(last[1])}" r="3.2" fill="none" stroke="#5eead4" stroke-width="1"/><path d="M${f(last[0] - 5)} ${f(last[1])}h10M${f(last[0])} ${f(last[1] - 5)}v10" stroke="#5eead4" stroke-width=".7"/></g>`);
  };

  scenes.campus = (s) => {
    const cx = -8, cy = -6;
    const w = 18, d = 11;
    const mods = [
      { x: -38, y: -26, type: "users", title: "Pacientes", sub: "identidad", color: T.gold, n: "01" },
      { x: -8, y: -26, type: "calendar", title: "Citas", sub: "agenda", color: T.teal, n: "02" },
      { x: 22, y: -26, type: "heart", title: "Preclínica", sub: "signos", color: T.coral, n: "03" },
      { x: -38, y: 12, type: "qr", title: "QR", sub: "documentos", color: T.gold, n: "06" },
      { x: -8, y: 12, type: "share", title: "Referencias", sub: "derivación", color: T.violet, n: "05" },
      { x: 22, y: 12, type: "stethoscope", title: "Consulta", sub: "encuentro", color: T.teal, n: "04" }
    ];

    // central light well
    const c = P(cx, cy, 0.1);
    s.add(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="112" ry="56" fill="rgba(45,212,191,.05)"/>`);
    s.add(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="76" ry="38" fill="none" stroke="rgba(94,234,212,.16)" stroke-width=".7" stroke-dasharray="2 5"/>`);
    s.add(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="42" ry="21" fill="none" stroke="rgba(94,234,212,.3)" stroke-width=".8"/>`);

    // links from each module to the HCE core
    mods.forEach((m) => {
      const a = P(cx, cy, 2.2);
      const b = P(m.x + w / 2, m.y + d / 2, 2.2);
      const mx = (a[0] + b[0]) / 2;
      const my = (a[1] + b[1]) / 2 - 24;
      s.add(`<path class="campus-link" d="M${f(a[0])},${f(a[1])} Q${f(mx)},${f(my)} ${f(b[0])},${f(b[1])}" fill="none" stroke="${m.color}" stroke-width=".75" opacity=".36"/>`);
      s.add(`<circle cx="${f(b[0])}" cy="${f(b[1])}" r="2" fill="${m.color}" opacity=".8"/>`);
    });

    function plinth(m) {
      slab(s, { x: m.x, y: m.y, w, d, z: 0, t: 2.4, top: "#123a43", sideA: "#0c2931", sideB: "#092229", stroke: "rgba(94,234,212,.3)" });
      box(s, { x: m.x + 1.5, y: m.y + 1.5, w: w - 3, d: d - 3, h: 4.2, z: 0.1, top: "#1b4d56", sideA: "#143c44", sideB: "#10343c", stroke: "rgba(94,234,212,.28)" });
      box(s, { x: m.x + 2.4, y: m.y + 2.4, w: w - 4.8, d: d - 4.8, h: 0.8, z: 4.3, top: m.color, sideA: m.color, sideB: m.color, stroke: "rgba(8,23,29,.35)", opacity: 0.82 });
      icon(s, m.x + w / 2, m.y + d / 2, 8, m.type, m.color);
      // numbered plaque on the front face
      const b = P(m.x + w / 2, m.y + d + 0.1, 2.2);
      s.track(b[0] - 6, b[1] - 5);
      s.track(b[0] + 6, b[1] + 5);
      s.add(`<g class="campus-plaque"><rect x="${f(b[0] - 8)}" y="${f(b[1] - 6)}" width="16" height="12" rx="2.4" fill="rgba(8,23,29,.92)" stroke="${m.color}" stroke-width=".7"/><text x="${f(b[0])}" y="${f(b[1] + 3.3)}" text-anchor="middle" font-size="7" fill="${m.color}" font-family="IBM Plex Mono,monospace" font-weight="600">${m.n}</text></g>`);
    }

    mods.filter((m) => m.y < cy).forEach(plinth);
    // central spine
    box(s, { x: cx - 3, y: cy - 3, w: 6, d: 6, h: 2.2, z: 0, top: "#1e555e", sideA: "#154149", sideB: "#10343c", stroke: "rgba(94,234,212,.55)" });
    box(s, { x: cx - 1.8, y: cy - 1.8, w: 3.6, d: 3.6, h: 24, z: 2.2, top: "rgba(94,234,212,.32)", sideA: "rgba(45,212,191,.2)", sideB: "rgba(45,212,191,.14)", stroke: "rgba(94,234,212,.72)", opacity: 0.9 });
    const top = P(cx, cy, 28);
    s.add(`<circle cx="${f(top[0])}" cy="${f(top[1])}" r="5" fill="none" stroke="rgba(94,234,212,.65)" stroke-width=".8"/><circle cx="${f(top[0])}" cy="${f(top[1])}" r="10" fill="none" stroke="rgba(94,234,212,.2)" stroke-width=".6"/>`);
    s.add(`<circle cx="${f(top[0])}" cy="${f(top[1])}" r="1.8" fill="${T.accent}"/>`);
    mods.filter((m) => m.y > cy).forEach(plinth);
  };

  scenes.stack = (s) => {
    const layers = [
      { z: 0, w: 62, d: 42, top: "#0e2931", a: "#0a2027", b: "#081b21", label: "Infraestructura", sub: "Apache · Gunicorn · Celery", color: T.gold },
      { z: 13, w: 54, d: 36, top: "#10333c", a: "#0b252c", b: "#092128", label: "Datos", sub: "PostgreSQL 15 · RLS · Redis", color: T.coral },
      { z: 26, w: 46, d: 30, top: "#143c44", a: "#0e2d34", b: "#0b252c", label: "Aplicaciones", sub: "Django · 14 apps · RBAC", color: T.teal },
      { z: 39, w: 38, d: 24, top: "#194a52", a: "#123a42", b: "#0e3037", label: "Canales", sub: "Web · Portal · API JWT", color: T.blue }
    ];
    const x0 = -8, y0 = -8;
    layers.forEach((l, i) => {
      slab(s, { x: x0 - l.w / 2, y: y0 - l.d / 2, w: l.w, d: l.d, z: l.z, t: 3.2, top: l.top, sideA: l.a, sideB: l.b, stroke: "rgba(94,234,212,.32)" });
      // grid panel on top
      const gx = x0 - l.w / 2 + 2, gy = y0 - l.d / 2 + 2;
      for (let k = 6; k < l.w - 4; k += 6) s.line([gx + k, gy, l.z + 0.2], [gx + k, gy + l.d - 4, l.z + 0.2], "rgba(94,234,212,.09)", { sw: 0.35 });
      // label callout at right edge
      const anchor = P(x0 + l.w / 2 + 2, y0, l.z + 1);
      s.add(`<line x1="${f(anchor[0])}" y1="${f(anchor[1])}" x2="${f(anchor[0] + 26)}" y2="${f(anchor[1] - 5)}" stroke="rgba(94,234,212,.25)" stroke-width=".5" stroke-dasharray="2 3"/>`);
      s.add(`<circle cx="${f(anchor[0])}" cy="${f(anchor[1])}" r="2" fill="${l.color}"/>`);
      s.text(anchor[0] + 30, anchor[1] - 1, l.label.toUpperCase(), { size: 8, fill: "rgba(238,250,246,.94)" });
      s.text(anchor[0] + 30, anchor[1] + 7.2, l.sub, { size: 5.8, cls: "iso-sub" });
      // layer number
      s.text(anchor[0] + 30, anchor[1] - 9.4, `0${4 - i}`, { size: 5, cls: "iso-sub" });
    });
    // tenant columns
    const tenants = [
      { x: x0 - 18, y: y0 - 2, c: T.teal, n: "TENANT A" },
      { x: x0 - 2, y: y0 + 10, c: T.gold, n: "TENANT B" },
      { x: x0 + 14, y: y0 + 2, c: T.coral, n: "TENANT C" }
    ];
    tenants.forEach((t, i) => {
      const top = P(t.x, t.y, 53);
      s.line([t.x, t.y, 2], [t.x, t.y, 53], t.c, { sw: 1, dash: "2 3", opacity: 0.65 });
      s.add(`<circle cx="${f(top[0])}" cy="${f(top[1])}" r="2.1" fill="${t.c}"/><circle cx="${f(top[0])}" cy="${f(top[1])}" r="5" fill="none" stroke="${t.c}" stroke-width=".5" opacity=".45"/>`);
      s.text(top[0], top[1] - 9, t.n, { anchor: "middle", size: 5.2, cls: "iso-sub" });
    });
    // shield on data layer
    const sh = P(x0 - 14, y0 + 2, 18);
    s.add(`<g transform="translate(${f(sh[0])},${f(sh[1])})" opacity=".85"><path d="M0-6 5-3.8V.4C5 4 2.8 5.8 0 6.6-2.8 5.8-5 4-5 .4v-4.2L0-6Z" fill="rgba(229,118,93,.12)" stroke="${T.coral}" stroke-width=".8"/><path d="m-2 1 1.4 1.4L2.6-1" fill="none" stroke="${T.coral}" stroke-width=".8"/></g>`);
  };

  /* ---------- role scenes ---------- */
  scenes.superadmin = (s) => {
    // command platform
    slab(s, { x: -30, y: -20, w: 60, d: 44, z: 0, t: 2.6, top: "#123a43", sideA: "#0b2931", sideB: "#082229", stroke: "rgba(94,234,212,.34)" });
    floorGrid(s, -30, -20, 60, 44, 6);
    const c = P(0, 0, 0);
    s.add(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="150" ry="78" fill="none" stroke="rgba(94,234,212,.13)" stroke-width=".8" stroke-dasharray="2 6"/>`);
    s.add(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="105" ry="54" fill="none" stroke="rgba(94,234,212,.18)" stroke-width=".8"/>`);
    s.add(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="62" ry="32" fill="rgba(45,212,191,.06)" stroke="rgba(94,234,212,.25)" stroke-width=".7"/>`);

    const tenants = [
      { x: -28, y: 8, c: T.teal, n: "A" },
      { x: 22, y: 2, c: T.gold, n: "B" },
      { x: 3, y: 28, c: T.coral, n: "C" }
    ];
    tenants.forEach((t) => {
      slab(s, { x: t.x, y: t.y, w: 14, d: 9, z: 0.2, t: 2, top: "#143f47", sideA: "#0d2e36", sideB: "#0a252d", stroke: "rgba(94,234,212,.2)" });
      box(s, { x: t.x + 2, y: t.y + 1.4, w: 10, d: 6.2, h: 4, z: 0.2, top: "#1b4d56", sideA: "#143c44", sideB: "#10343c", stroke: "rgba(94,234,212,.26)" });
      box(s, { x: t.x + 2.4, y: t.y + 1.8, w: 9.2, d: 5.4, h: 0.6, z: 4.2, top: t.c, sideA: t.c, sideB: t.c, stroke: "rgba(8,23,29,.3)", opacity: 0.78 });
      const top = P(t.x + 7, t.y + 4.5, 5.2);
      s.add(`<circle cx="${f(top[0])}" cy="${f(top[1])}" r="1.6" fill="${t.c}"/>`);
    });

    // beacon tower
    box(s, { x: -8, y: -8, w: 16, d: 16, h: 3, z: 0, top: "#1d5059", sideA: "#153e46", sideB: "#11353d", stroke: "rgba(94,234,212,.55)" });
    box(s, { x: -4.4, y: -4.4, w: 8.8, d: 8.8, h: 24, z: 3, top: "rgba(45,212,191,.3)", sideA: "rgba(45,212,191,.18)", sideB: "rgba(45,212,191,.12)", stroke: "rgba(94,234,212,.62)", opacity: 0.92 });
    // tower glazing
    for (let i = 0; i < 4; i++) {
      s.line([-4.4, -4.4 + i * 2.2, 6], [-4.4, -4.4 + i * 2.2, 25], "rgba(94,234,212,.25)", { sw: 0.4 });
    }
    box(s, { x: -9, y: -7, w: 18, d: 14, h: 6, z: 27, top: "#1b5059", sideA: "#123c44", sideB: "#0e3139", stroke: "rgba(94,234,212,.62)" });
    box(s, { x: -9.8, y: -7.8, w: 19.6, d: 15.6, h: 1, z: 33, top: "#2a6b73", sideA: "#1f555e", sideB: "#194850", stroke: "rgba(94,234,212,.4)" });
    // cabin windows
    s.poly([P(-9.05, -4, 28), P(-9.05, 4, 28), P(-9.05, 4, 32), P(-9.05, -4, 32)], "rgba(94,234,212,.2)", { stroke: "rgba(94,234,212,.55)", sw: 0.45 });
    // antenna
    s.line([0, 0, 34], [0, 0, 41], "rgba(94,234,212,.7)", { sw: 0.8 });
    s.add(`<circle cx="${f(P(0, 0, 41)[0])}" cy="${f(P(0, 0, 41)[1])}" r="2.4" fill="${T.accent}"/>`);

    // beams to tenants
    tenants.forEach((t) => {
      const a = P(0, 0, 34);
      const b = P(t.x + 7, t.y + 4, 6);
      const mx = (a[0] + b[0]) / 2;
      const my = Math.min(a[1], b[1]) - 16;
      s.add(`<path d="M${f(a[0])},${f(a[1])} Q${f(mx)},${f(my)} ${f(b[0])},${f(b[1])}" fill="none" stroke="${t.c}" stroke-width=".65" opacity=".4" stroke-dasharray="2 5"/>`);
    });
    person(s, 10, 14, 0, T.gold);
    person(s, -12, 16, 0, T.teal, { opacity: 0.75 });
  };

  scenes.admin = (s) => {
    room(s, { x: 0, y: 0, w: 50, d: 34, h: 10, windows: true, rugColor: "rgba(63,126,166,.05)" });
    board(s, 12, 0.5, 5.5, 17, 7, T.blue);
    // add a second dashboard panel
    board(s, 31, 0.5, 5.5, 6, 5, T.blue);
    desk(s, 14, 10, 18, 5, 0, "#24616a");
    monitor(s, 18, 9.2, 3, 7, T.blue);
    chair(s, 15, 16.4, 0, "#2e7079", "y");
    person(s, 16, 17.8, 0, T.blue);
    chair(s, 27, 16.2, 0, "#2e7079", "y");
    // calendar wall
    box(s, { x: 37, y: 8, w: 8, d: 0.6, h: 6, z: 3.4, top: "#0a2229", sideA: "#0a2229", sideB: "#0a2229", stroke: "rgba(94,234,212,.35)" });
    const cal = P(37.4, 8.7, 4);
    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 3; j++) {
        s.add(`<rect x="${f(cal[0] + i * 8)}" y="${f(cal[1] - j * 7)}" width="5" height="4.4" rx=".6" fill="${j === 2 && i === 2 ? "rgba(229,118,93,.7)" : "rgba(94,234,212,.18)"}"/>`);
      }
    }
    person(s, 40, 15, 0, T.teal, { opacity: 0.8 });
    plant(s, 3.4, 27, 0, 1.15);
  };

  scenes.recepcion = (s) => {
    room(s, { x: 0, y: 0, w: 48, d: 31, h: 9.5, windows: true, rugColor: "rgba(201,154,63,.04)" });
    counter(s, 5, 8.5, 18, 3.6);
    monitor(s, 8.4, 7.9, 4.3, 5.2, T.gold);
    person(s, 14, 14.6, 0, T.gold);
    bench(s, 28, 7, 12.5, 2.8);
    bench(s, 28, 12.6, 12.5, 2.8);
    person(s, 31, 8.6, 0, T.teal, { opacity: 0.8 });
    person(s, 34, 14.2, 0, T.coral, { opacity: 0.8 });
    person(s, 37.6, 15.1, 0, T.teal, { opacity: 0.55 });
    // self check-in kiosk
    box(s, { x: 43, y: 22, w: 3.4, d: 3.4, h: 6, z: 0, top: "#20565e", sideA: "#18434b", sideB: "#13373f", stroke: "rgba(94,234,212,.45)" });
    const ks = P(43.2, 25.6, 4.2);
    s.add(`<rect x="${f(ks[0])}" y="${f(ks[1])}" width="14" height="10" rx="1.5" fill="rgba(94,234,212,.16)" stroke="rgba(94,234,212,.55)" stroke-width=".5"/>`);
    s.add(`<path d="M${f(ks[0] + 3)} ${f(ks[1] + 4)}h8M${f(ks[0] + 3)} ${f(ks[1] + 7)}h5" stroke="#5eead4" stroke-width=".45"/>`);
    plant(s, 2.8, 25, 0, 1.1);
  };

  scenes.enfermeria = (s) => {
    room(s, { x: 0, y: 0, w: 46, d: 32, h: 10, windows: true, rugColor: "rgba(229,118,93,.04)" });
    bed(s, 4.5, 7, 17, 6.2);
    person(s, 12, 18.5, 0, T.coral);
    // vitals cart
    box(s, { x: 26, y: 8.5, w: 6.5, d: 5, h: 4.2, z: 0, top: "#1d5059", sideA: "#153f47", sideB: "#11353d", stroke: "rgba(94,234,212,.34)" });
    monitor(s, 27.4, 9.2, 4.2, 4.2, T.coral, true);
    person(s, 33, 17, 0, T.teal);
    // wall vitals board
    bankVitals(s, 34, 0.5, 5.6);
    plant(s, 2.8, 26, 0, 1);
  };

  function bankVitals(s, x, y, z) {
    box(s, { x, y, w: 9, d: 0.6, h: 5.4, z, top: "#0a2229", sideA: "#0a2229", sideB: "#0a2229", stroke: "rgba(94,234,212,.4)" });
    const p = P(x + 1, y + 0.7, z + 1.2);
    s.add(`<rect x="${f(p[0])}" y="${f(p[1])}" width="34" height="8" rx="1" fill="rgba(94,234,212,.1)"/>`);
    for (let i = 0; i < 4; i++) {
      s.add(`<rect x="${f(p[0])}" y="${f(p[1] + 10 + i * 7)}" width="${f(28 - i * 4)}" height="2.4" rx="1" fill="${i === 0 ? "rgba(229,118,93,.7)" : "rgba(94,234,212,.22)"}"/>`);
    }
  }

  scenes.medico = (s) => {
    room(s, { x: 0, y: 0, w: 50, d: 35, h: 10, windows: true, rugColor: "rgba(45,212,191,.04)" });
    desk(s, 5, 7, 16, 5, 0, "#24616a");
    monitor(s, 9, 6.2, 3, 6.4, T.teal);
    chair(s, 6, 13, 0, "#2e7079", "y");
    chair(s, 15, 13, 0, "#2e7079", "y");
    person(s, 7.2, 14.4, 0, T.teal);
    person(s, 16.4, 14.2, 0, T.coral);
    bed(s, 5, 24.5, 16, 5.4);
    board(s, 31, 0.5, 5.5, 15, 7.4, T.teal);
    // wizard steps on the board
    const b = P(32.2, 1.2, 5.2);
    for (let i = 0; i < 8; i++) {
      s.add(`<rect x="${f(b[0] + i * 9.4)}" y="${f(b[1])}" width="6.4" height="6.4" rx="1" fill="${i < 3 ? "rgba(94,234,212,.6)" : "rgba(94,234,212,.12)"}" stroke="rgba(94,234,212,.35)" stroke-width=".4"/>`);
    }
    shelves(s, 44.5, 20, 2.6, 8, 7.5);
    plant(s, 46, 29, 0, 0.9);
  };

  scenes.especialista = (s) => {
    // level 1 platform
    slab(s, { x: -32, y: 2, w: 26, d: 22, z: 0, t: 2.6, top: "#123a43", sideA: "#0b2931", sideB: "#082229", stroke: "rgba(94,234,212,.32)" });
    floorGrid(s, -32, 2, 26, 22, 4.5);
    room(s, { x: -28, y: 6, w: 18, d: 12, h: 7.5, rug: false, floor: "#174850", gridStep: 4 });
    desk(s, -25, 9, 7, 3.2, 0, "#24616a");
    monitor(s, -23.2, 8.6, 3, 3.4, T.teal);
    person(s, -20, 16, 0, T.teal);
    s.text(P(-19, 12, 10.5)[0], P(-19, 12, 10.5)[1], "NIVEL 1", { anchor: "middle", size: 6.2, cls: "iso-room-label" });

    // level 2 raised platform
    box(s, { x: 8, y: 0, w: 30, d: 24, h: 10, z: 0, top: "#123a43", sideA: "#0b2931", sideB: "#082229", stroke: "rgba(94,234,212,.32)" });
    slab(s, { x: 8, y: 0, w: 30, d: 24, z: 10, t: 1.6, top: "#174850", sideA: "#0e3038", sideB: "#0a252d", stroke: "rgba(94,234,212,.4)" });
    floorGrid(s, 8, 0, 30, 24, 5);
    desk(s, 13, 7, 14, 4.6, 10, "#24616a");
    monitor(s, 16, 6.2, 13, 6, T.violet);
    chair(s, 14, 13.2, 10, "#3a3560", "y");
    person(s, 15.2, 14.4, 10, T.violet);
    person(s, 23.4, 14.2, 10, T.coral);
    plant(s, 33, 18, 10, 0.95);
    s.text(P(23, 12, 16.5)[0], P(23, 12, 16.5)[1], "NIVEL 2", { anchor: "middle", size: 6.2, cls: "iso-room-label" });

    // bridge
    const a = P(-10, 12, 5);
    const b = P(8, 12, 14);
    const mx = (a[0] + b[0]) / 2;
    const my = Math.min(a[1], b[1]) - 34;
    const bridge = `M${f(a[0])},${f(a[1])} Q${f(mx)},${f(my)} ${f(b[0])},${f(b[1])}`;
    s.add(`<path d="${bridge}" fill="none" stroke="rgba(179,163,233,.2)" stroke-width="7" stroke-linecap="round"/>`);
    s.add(`<path id="refBridge" d="${bridge}" fill="none" stroke="rgba(179,163,233,.7)" stroke-width=".9" stroke-dasharray="3 6"/>`);
    s.add(`<g class="iso-envelope"><rect x="-5" y="-3.5" width="10" height="7" rx=".8" fill="#efe9dd" stroke="#e5765d" stroke-width=".6"/><path d="M-5-3 0 1.5 5-3" fill="none" stroke="#e5765d" stroke-width=".6"/><animateMotion dur="7s" repeatCount="indefinite" rotate="auto"><mpath href="#refBridge"/></animateMotion></g>`);
  };

  scenes.paciente = (s) => {
    slab(s, { x: -24, y: -18, w: 48, d: 36, z: 0, t: 2.4, top: "#123a43", sideA: "#0b2931", sideB: "#082229", stroke: "rgba(94,234,212,.32)" });
    floorGrid(s, -24, -18, 48, 36, 5);
    // giant phone / tablet
    box(s, { x: -12, y: -16, w: 22, d: 32, h: 1.6, z: 0.2, top: "#0a2229", sideA: "#071a20", sideB: "#06181d", stroke: "rgba(94,234,212,.55)" });
    box(s, { x: -11, y: -15, w: 20, d: 30, h: 0.23, z: 1.8, top: "#103b44", sideA: "#103b44", sideB: "#103b44", stroke: "rgba(94,234,212,.4)" });
    const screen = { x: -10.4, y: -14.2, w: 18.8, d: 28.4 };
    // header
    s.poly([P(screen.x, screen.y, 2.1), P(screen.x + screen.w, screen.y, 2.1), P(screen.x + screen.w, screen.y + 3.4, 2.1), P(screen.x, screen.y + 3.4, 2.1)], "rgba(45,212,191,.34)", { stroke: "rgba(94,234,212,.6)", sw: 0.4 });
    // next appointment card
    s.poly([P(screen.x + 1.2, screen.y + 5, 2.1), P(screen.x + screen.w - 1.2, screen.y + 5, 2.1), P(screen.x + screen.w - 1.2, screen.y + 12.5, 2.1), P(screen.x + 1.2, screen.y + 12.5, 2.1)], "rgba(94,234,212,.17)", { stroke: "rgba(94,234,212,.65)", sw: 0.45 });
    // appointment accent
    s.poly([P(screen.x + 1.2, screen.y + 5, 2.2), P(screen.x + 2.2, screen.y + 5, 2.2), P(screen.x + 2.2, screen.y + 12.5, 2.2), P(screen.x + 1.2, screen.y + 12.5, 2.2)], "#e5765d", { stroke: "none", sw: 0 });
    // list rows
    for (let i = 0; i < 3; i++) {
      s.poly([P(screen.x + 1.2, screen.y + 15 + i * 3.4, 2.1), P(screen.x + screen.w - 1.2, screen.y + 15 + i * 3.4, 2.1), P(screen.x + screen.w - 1.2, screen.y + 17.2 + i * 3.4, 2.1), P(screen.x + 1.2, screen.y + 17.2 + i * 3.4, 2.1)], "rgba(94,234,212,.13)", { stroke: "rgba(94,234,212,.32)", sw: 0.35 });
    }
    // bottom nav
    s.poly([P(screen.x, screen.y + 27.2, 2.1), P(screen.x + screen.w, screen.y + 27.2, 2.1), P(screen.x + screen.w, screen.y + screen.d - 0.8, 2.1), P(screen.x, screen.y + screen.d - 0.8, 2.1)], "rgba(94,234,212,.18)", { stroke: "rgba(94,234,212,.4)", sw: 0.35 });
    // notification card floating
    const n = P(15, -12, 11);
    s.add(`<g transform="translate(${f(n[0])},${f(n[1])})"><rect x="-24" y="-10" width="48" height="20" rx="3" fill="rgba(8,23,29,.94)" stroke="rgba(94,234,212,.55)" stroke-width=".7"/><circle cx="-16" cy="-2" r="3.2" fill="#e5765d"/><path d="M-16-5.2v3.4M-16 .4v.4" stroke="#08171d" stroke-width=".8"/><text x="-9" y="-1" font-size="7" fill="rgba(238,250,246,.9)" font-family="IBM Plex Mono,monospace">CITA HOY</text><text x="-9" y="6" font-size="5.4" fill="rgba(226,240,236,.5)" font-family="IBM Plex Mono,monospace">10:30 · MEDICINA GENERAL</text></g>`);
    // second floating card: portable history
    const h = P(-19, 18, 9);
    s.add(`<g transform="translate(${f(h[0])},${f(h[1])})"><rect x="-30" y="-10" width="60" height="22" rx="3" fill="rgba(8,23,29,.95)" stroke="rgba(94,234,212,.4)" stroke-width=".7"/><rect x="-23" y="-5" width="11" height="13" rx="1.2" fill="rgba(94,234,212,.14)" stroke="rgba(94,234,212,.5)" stroke-width=".5"/><path d="M-20-1h5M-20 2h5M-20 5h3" stroke="#5eead4" stroke-width=".45"/><text x="-7" y="-1" font-size="6.2" fill="rgba(238,250,246,.9)" font-family="IBM Plex Mono,monospace">HCE · PDF</text><text x="-7" y="6" font-size="5" fill="rgba(226,240,236,.45)" font-family="IBM Plex Mono,monospace">DESCARGAR HISTORIA</text></g>`);
    person(s, 15.5, 14, 0.2, T.sky);
    person(s, -17.5, 16, 0.2, T.teal, { opacity: 0.7 });
    plant(s, 19, 20, 0.2, 1.1);
  };

  function render(name, svg) {
    const s = new Scene();
    try {
      (scenes[name] || scenes.clinic)(s);
    } catch (err) {
      console.error("ISO scene error", name, err);
      s.body = `<text x="0" y="0" fill="#f00" font-size="8">scene error</text>`;
    }
    svg.setAttribute("viewBox", s.viewBox(name === "hero" ? 14 : 20));
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    svg.innerHTML = s.body;
  }

  function init() {
    document.querySelectorAll("svg[data-iso]").forEach((svg) => {
      const name = svg.getAttribute("data-iso");
      render(name, svg);
      svg.dataset.rendered = "1";
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();

  window.XMedicalISO = { render, scenes, P };
})();
