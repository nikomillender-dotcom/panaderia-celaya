/* Panadería Celaya — cart, ordering, open-now badge. Cart is shared between /en and /es via localStorage. */
(function () {
  "use strict";
  var C = window.CELAYA, T = C.t, L = C.lang, KEY = "celaya_cart_v1";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var cart = {};
  try { cart = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { cart = {}; }
  var money = function (n) { return "$" + n.toFixed(2); };
  var save = function () { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  function toast(msg) { var t = $("#toast"); t.textContent = msg; t.classList.add("on"); clearTimeout(toast.h); toast.h = setTimeout(function () { t.classList.remove("on"); }, 1800); }

  /* ---------- cart state ---------- */
  function setQty(id, q) { if (!C.items[id]) return; if (q <= 0) delete cart[id]; else cart[id] = Math.min(q, 99); save(); render(); }
  function count() { return Object.keys(cart).reduce(function (a, k) { return a + cart[k]; }, 0); }
  function hasCake() { return Object.keys(cart).some(function (k) { return C.items[k] && C.items[k].cake; }); }

  function render() {
    $$(".item").forEach(function (el) {
      var q = cart[el.dataset.id] || 0; el.classList.toggle("in", q > 0); $("output", el).textContent = q;
    });
    $$(".cart-count").forEach(function (e) { e.textContent = count(); });
    var body = $("#cartLines"), ids = Object.keys(cart);
    if (!ids.length) {
      body.innerHTML = '<div class="empty"><div class="big">🧺</div><h3>' + T.emptyT + "</h3><p>" + T.emptyP + "</p></div>";
      $("#orderForm").hidden = true; return;
    }
    var sub = 0, unk = false, html = "";
    ids.forEach(function (id) {
      var it = C.items[id], q = cart[id];
      if (it.price == null) unk = true; else sub += it.price * q;
      html += '<div class="line" data-id="' + id + '"><b>' + esc(it.name) + "</b>" +
        '<span class="step"><button type="button" data-d="-1" aria-label="' + T.less + '">–</button><output>' + q + '</output><button type="button" data-d="1" aria-label="' + T.more + '">+</button></span>' +
        "<small>" + (it.price == null ? T.priceAtPickup : money(it.price) + " × " + q) + "</small></div>";
    });
    html += '<div class="total"><span>' + T.subtotal + "</span><span>" + money(sub) + (unk ? "+" : "") + "</span></div>" +
      '<p class="fine">' + (unk ? T.fineUnknown : T.fineKnown) + "</p>";
    body.innerHTML = html;
    $("#orderForm").hidden = false;
    $("#cakeBox").classList.toggle("on", hasCake());
    setMinDate();
  }

  /* ---------- pickup date/time ---------- */
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function setMinDate() {
    var d = new Date(); if (hasCake()) d.setDate(d.getDate() + 3);
    var el = $("#f-date"); el.min = iso(d); if (!el.value || el.value < el.min) el.value = iso(d);
    $("#cakeNote").hidden = !hasCake();
  }
  (function times() {
    var s = $("#f-time"), h, m, lbl;
    for (h = 6; h <= 20; h++) for (m = 0; m < 60; m += 30) {
      if (h === 20 && m > 30) continue;
      var hh = h % 12 || 12, ap = h < 12 ? "AM" : "PM"; lbl = hh + ":" + (m ? "30" : "00") + " " + ap;
      s.insertAdjacentHTML("beforeend", '<option value="' + lbl + '">' + lbl + "</option>");
    }
    s.value = "10:00 AM";
  })();

  /* ---------- drawer ---------- */
  var dr = $("#drawer"), sc = $("#scrim"), lastFocus;
  function open() { lastFocus = document.activeElement; dr.classList.add("on"); sc.classList.add("on"); dr.setAttribute("aria-hidden", "false"); document.body.style.overflow = "hidden"; $("#drawerClose").focus(); }
  function close() { dr.classList.remove("on"); sc.classList.remove("on"); dr.setAttribute("aria-hidden", "true"); document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
  $$("[data-open-cart]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); showForm(); open(); }); });
  $("#drawerClose").addEventListener("click", close); sc.addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && dr.classList.contains("on")) close(); });

  document.addEventListener("click", function (e) {
    var add = e.target.closest(".add"), st = e.target.closest(".step button");
    if (add) { var id = add.closest(".item").dataset.id; setQty(id, 1); toast(T.added); }
    else if (st) { var host = st.closest("[data-id]"); setQty(host.dataset.id, (cart[host.dataset.id] || 0) + (+st.dataset.d)); }
  });

  /* ---------- order message + submit ---------- */
  function buildMessage(f) {
    var lines = [T.msgHead, ""], sub = 0, unk = false;
    Object.keys(cart).forEach(function (id) {
      var it = C.items[id]; lines.push("• " + cart[id] + " × " + it.name + (it.price != null ? " (" + money(it.price) + ")" : ""));
      if (it.price == null) unk = true; else sub += it.price * cart[id];
    });
    lines.push("", T.lblSub + ": " + money(sub) + (unk ? "+ (" + T.priceAtPickup + ")" : ""), "",
      T.lblName + ": " + f.name, T.lblPhone + ": " + f.phone, T.lblPickup + ": " + f.date + " " + f.time);
    var cakeInfo = [f.size, f.flavor, f.msg].filter(Boolean).join(" · ");
    if (hasCake() && cakeInfo) lines.push(T.lblCake + ": " + cakeInfo);
    if (f.notes) lines.push(T.lblNotes + ": " + f.notes);
    return lines.join("\n");
  }
  function val() {
    var f = {}; ["name", "phone", "date", "time", "notes", "size", "flavor", "msg"].forEach(function (k) { f[k] = ($("#f-" + k).value || "").trim(); });
    var ok = true;
    $$(".err").forEach(function (e) { e.textContent = ""; });
    if (f.name.length < 2) { $("#e-name").textContent = T.eName; ok = false; }
    if (f.phone.replace(/\D/g, "").length < 10) { $("#e-phone").textContent = T.ePhone; ok = false; }
    if (!f.date) { $("#e-date").textContent = T.eDate; ok = false; }
    if (f.date && f.date < $("#f-date").min) { $("#e-date").textContent = hasCake() ? T.eCake : T.eDate; ok = false; }
    return ok ? f : null;
  }
  function showForm() { $("#cartView").hidden = false; $("#doneView").hidden = true; }
  $("#orderForm").addEventListener("submit", function (e) {
    e.preventDefault(); var f = val(); if (!f) { var bad = $(".err:not(:empty)"); if (bad) bad.previousElementSibling.focus(); return; }
    var msg = buildMessage(f), tel = C.phoneRaw;
    $("#doneMsg").textContent = msg;
    $("#smsBtn").href = "sms:" + tel + "?&body=" + encodeURIComponent(msg);
    $("#callBtn").href = "tel:" + tel;
    $("#cartView").hidden = true; $("#doneView").hidden = false; $("#doneView").scrollIntoView();
    if (C.endpoint) { fetch(C.endpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ lang: L, order: msg, contact: f }) }).then(function (r) { if (r.ok) { $("#sentOk").hidden = false; } }).catch(function () {}); }
  });
  $("#copyBtn").addEventListener("click", function () {
    var t = $("#doneMsg").textContent;
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { toast(T.copied); }, function () { var r = document.createRange(); r.selectNodeContents($("#doneMsg")); getSelection().removeAllRanges(); getSelection().addRange(r); toast(T.copyFail); });
  });
  $("#clearBtn").addEventListener("click", function () { cart = {}; save(); render(); showForm(); close(); });

  /* ---------- menu chips (scroll-spy) ---------- */
  var chips = $$(".chip");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) chips.forEach(function (c) { c.classList.toggle("on", c.getAttribute("href") === "#" + en.target.id); }); });
    }, { rootMargin: "-30% 0px -60% 0px" });
    $$(".cat").forEach(function (c) { io.observe(c); });
  }

  /* ---------- open-now (America/Chicago) ---------- */
  (function () {
    var p = $("#openPill"); if (!p) return;
    try {
      var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/Chicago", weekday: "short", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date()), o = {};
      parts.forEach(function (x) { o[x.type] = x.value; });
      var mins = (+o.hour % 24) * 60 + +o.minute, open = mins >= 360 && mins < 1245;
      p.classList.toggle("open", open); $(".txt", p).textContent = open ? T.openNow : T.closedNow;
      var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], idx = days.indexOf(o.weekday), row = $$("#hoursTbl tr")[(idx + 6) % 7]; if (row) row.classList.add("today");
    } catch (e) {}
  })();

  /* ---------- hash deep link: #order opens cart ---------- */
  if (location.hash === "#order") { showForm(); open(); }
  render();
})();
