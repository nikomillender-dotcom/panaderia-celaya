/* Panadería Celaya — Multi-Page Cart & Interaction Engine
   Cart is shared across all pages and between /en and /es via localStorage. */
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

  function toast(msg) {
    var t = $("#toast");
    if (!t) return;
    t.textContent = msg;
    t.classList.add("on");
    clearTimeout(toast.h);
    toast.h = setTimeout(function () { t.classList.remove("on"); }, 1800);
  }

  /* ---------- mobile menu toggle ---------- */
  var navToggle = $("#navToggle"), mobileDrawer = $("#mobileDrawer");
  if (navToggle && mobileDrawer) {
    navToggle.addEventListener("click", function () {
      var isOpen = mobileDrawer.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  /* ---------- cart state ---------- */
  function setQty(id, q) {
    if (!C.items[id]) return;
    if (q <= 0) delete cart[id];
    else cart[id] = Math.min(q, 99);
    save();
    render();
  }
  function count() {
    return Object.keys(cart).reduce(function (a, k) { return a + cart[k]; }, 0);
  }
  function hasCake() {
    return Object.keys(cart).some(function (k) { return C.items[k] && C.items[k].cake; });
  }

  function render() {
    $$(".item").forEach(function (el) {
      var id = el.dataset.id;
      var q = cart[id] || 0;
      el.classList.toggle("in", q > 0);
      var out = $("output", el);
      if (out) out.textContent = q;
    });
    $$(".cart-count").forEach(function (e) { e.textContent = count(); });
    var body = $("#cartLines");
    if (!body) return;
    var ids = Object.keys(cart);
    if (!ids.length) {
      body.innerHTML = '<div class="empty"><div class="big">🧺</div><h3>' + T.emptyT + "</h3><p>" + T.emptyP + "</p></div>";
      var f = $("#orderForm");
      if (f) f.hidden = true;
      return;
    }
    var sub = 0, unk = false, html = "";
    ids.forEach(function (id) {
      var it = C.items[id], q = cart[id];
      if (!it) return;
      if (it.price == null) unk = true;
      else sub += it.price * q;
      html += '<div class="line" data-id="' + id + '"><b>' + esc(it.name) + "</b>" +
        '<span class="step"><button type="button" data-d="-1" aria-label="' + T.less + '">–</button><output>' + q + '</output><button type="button" data-d="1" aria-label="' + T.more + '">+</button></span>' +
        "<small>" + (it.price == null ? T.priceAtPickup : money(it.price) + " × " + q) + "</small></div>";
    });
    html += '<div class="total"><span>' + T.subtotal + "</span><span>" + money(sub) + (unk ? "+" : "") + "</span></div>" +
      '<p class="fine">' + (unk ? T.fineUnknown : T.fineKnown) + "</p>";
    body.innerHTML = html;
    var formEl = $("#orderForm");
    if (formEl) formEl.hidden = false;
    var cakeBox = $("#cakeBox");
    if (cakeBox) cakeBox.classList.toggle("on", hasCake());
    setMinDate();
  }

  /* ---------- pickup date/time ---------- */
  function iso(d) {
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  function setMinDate() {
    var d = new Date();
    if (hasCake()) d.setDate(d.getDate() + 3);
    var el = $("#f-date");
    if (!el) return;
    el.min = iso(d);
    if (!el.value || el.value < el.min) el.value = iso(d);
    var note = $("#cakeNote");
    if (note) note.hidden = !hasCake();
  }

  (function initTimes() {
    var s = $("#f-time");
    if (!s) return;
    for (var h = 6; h <= 20; h++) {
      for (var m = 0; m < 60; m += 30) {
        if (h === 20 && m > 30) continue;
        var hh = h % 12 || 12, ap = h < 12 ? "AM" : "PM";
        var lbl = hh + ":" + (m ? "30" : "00") + " " + ap;
        s.insertAdjacentHTML("beforeend", '<option value="' + lbl + '">' + lbl + "</option>");
      }
    }
    s.value = "10:00 AM";
  })();

  /* ---------- drawer open/close ---------- */
  var dr = $("#drawer"), sc = $("#scrim"), lastFocus;
  function open() {
    lastFocus = document.activeElement;
    if (dr) { dr.classList.add("on"); dr.setAttribute("aria-hidden", "false"); }
    if (sc) sc.classList.add("on");
    document.body.style.overflow = "hidden";
    var closeBtn = $("#drawerClose");
    if (closeBtn) closeBtn.focus();
  }
  function close() {
    if (dr) { dr.classList.remove("on"); dr.setAttribute("aria-hidden", "true"); }
    if (sc) sc.classList.remove("on");
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  $$("[data-open-cart]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      showForm();
      open();
    });
  });

  $$("[data-cake-order]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      if (!cart["tres-leches"] && !cart["birthday"]) {
        setQty("tres-leches", 1);
      }
      showForm();
      open();
    });
  });

  var dClose = $("#drawerClose");
  if (dClose) dClose.addEventListener("click", close);
  if (sc) sc.addEventListener("click", close);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && dr && dr.classList.contains("on")) close();
  });

  /* ---------- item clicks (add / step) ---------- */
  document.addEventListener("click", function (e) {
    var add = e.target.closest(".add");
    var st = e.target.closest(".step button");
    if (add) {
      var itemEl = add.closest(".item");
      if (itemEl) {
        setQty(itemEl.dataset.id, 1);
        toast(T.added);
      }
    } else if (st) {
      var host = st.closest("[data-id]");
      if (host) {
        var current = cart[host.dataset.id] || 0;
        setQty(host.dataset.id, current + (+st.dataset.d));
      }
    }
  });

  /* ---------- order message + submit ---------- */
  function buildMessage(f) {
    var lines = [T.msgHead, ""], sub = 0, unk = false;
    Object.keys(cart).forEach(function (id) {
      var it = C.items[id];
      if (!it) return;
      lines.push("• " + cart[id] + " × " + it.name + (it.price != null ? " (" + money(it.price) + ")" : ""));
      if (it.price == null) unk = true;
      else sub += it.price * cart[id];
    });
    lines.push(
      "",
      T.lblSub + ": " + money(sub) + (unk ? "+ (" + T.priceAtPickup + ")" : ""),
      "",
      T.lblName + ": " + f.name,
      T.lblPhone + ": " + f.phone,
      T.lblPickup + ": " + f.date + " " + f.time
    );
    var cakeInfo = [f.size, f.flavor, f.msg].filter(Boolean).join(" · ");
    if (hasCake() && cakeInfo) lines.push(T.lblCake + ": " + cakeInfo);
    if (f.notes) lines.push(T.lblNotes + ": " + f.notes);
    return lines.join("\n");
  }

  function val() {
    var f = {};
    ["name", "phone", "date", "time", "notes", "size", "flavor", "msg"].forEach(function (k) {
      var el = $("#f-" + k);
      f[k] = el ? (el.value || "").trim() : "";
    });
    var ok = true;
    $$(".err").forEach(function (e) { e.textContent = ""; });
    if (f.name.length < 2) { var en = $("#e-name"); if (en) en.textContent = T.eName; ok = false; }
    if (f.phone.replace(/\D/g, "").length < 10) { var ep = $("#e-phone"); if (ep) ep.textContent = T.ePhone; ok = false; }
    var fd = $("#f-date");
    if (!f.date) { var ed = $("#e-date"); if (ed) ed.textContent = T.eDate; ok = false; }
    if (f.date && fd && f.date < fd.min) { var ed2 = $("#e-date"); if (ed2) ed2.textContent = hasCake() ? T.eCake : T.eDate; ok = false; }
    return ok ? f : null;
  }

  function showForm() {
    var cv = $("#cartView"), dv = $("#doneView");
    if (cv) cv.hidden = false;
    if (dv) dv.hidden = true;
  }

  var ordForm = $("#orderForm");
  if (ordForm) {
    ordForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = val();
      if (!f) {
        var bad = $(".err:not(:empty)");
        if (bad && bad.previousElementSibling) bad.previousElementSibling.focus();
        return;
      }
      var msg = buildMessage(f), tel = C.phoneRaw;
      var dm = $("#doneMsg"); if (dm) dm.textContent = msg;
      var sb = $("#smsBtn"); if (sb) sb.href = "sms:" + tel + "?&body=" + encodeURIComponent(msg);
      var cb = $("#callBtn"); if (cb) cb.href = "tel:" + tel;
      var cv = $("#cartView"); if (cv) cv.hidden = true;
      var dv = $("#doneView"); if (dv) { dv.hidden = false; dv.scrollIntoView(); }
      if (C.endpoint) {
        fetch(C.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({ lang: L, order: msg, contact: f })
        }).then(function (r) {
          if (r.ok) { var sok = $("#sentOk"); if (sok) sok.hidden = false; }
        }).catch(function () {});
      }
    });
  }

  var cpBtn = $("#copyBtn");
  if (cpBtn) {
    cpBtn.addEventListener("click", function () {
      var dm = $("#doneMsg");
      var t = dm ? dm.textContent : "";
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(
        function () { toast(T.copied); },
        function () {
          if (dm) {
            var r = document.createRange();
            r.selectNodeContents(dm);
            getSelection().removeAllRanges();
            getSelection().addRange(r);
          }
          toast(T.copyFail);
        }
      );
    });
  }

  var clrBtn = $("#clearBtn");
  if (clrBtn) {
    clrBtn.addEventListener("click", function () {
      cart = {};
      save();
      render();
      showForm();
      close();
    });
  }

  /* ---------- category filter pills on Menu page ---------- */
  var filterBtns = $$(".filter-btn");
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var targetCat = btn.dataset.cat;
        filterBtns.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        var sections = $$(".cat-section");
        sections.forEach(function (sec) {
          if (targetCat === "all" || sec.id === "cat-" + targetCat) {
            sec.hidden = false;
          } else {
            sec.hidden = true;
          }
        });
        if (targetCat !== "all") {
          var targetEl = $("#cat-" + targetCat);
          if (targetEl) targetEl.scrollIntoView({ behavior: "smooth" });
        }
      });
    });
  }

  /* ---------- open-now status (America/Chicago) ---------- */
  (function initOpenStatus() {
    var p = $("#openPill");
    if (!p) return;
    try {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/Chicago",
        weekday: "short",
        hour: "numeric",
        minute: "numeric",
        hour12: false
      }).formatToParts(new Date()), o = {};
      parts.forEach(function (x) { o[x.type] = x.value; });
      var mins = (+o.hour % 24) * 60 + +o.minute;
      var isOpen = mins >= 360 && mins < 1245; // 6:00 AM to 8:45 PM
      p.classList.toggle("open", isOpen);
      var txt = $(".txt", p);
      if (txt) txt.textContent = isOpen ? T.openNow : T.closedNow;
      var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
      var idx = days.indexOf(o.weekday);
      var rows = $$("#hoursTbl tr");
      if (rows.length && idx !== -1) {
        var row = rows[(idx + 6) % 7];
        if (row) row.classList.add("today");
      }
    } catch (e) {}
  })();

  /* ---------- deep link handling ---------- */
  if (location.hash === "#order") {
    showForm();
    open();
  }
  render();
})();
