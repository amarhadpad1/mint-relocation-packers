(function () {
  "use strict";
  var D = window.SITE || {};
  var root = document.body.getAttribute("data-root") || "";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var mobile = function () { return window.matchMedia("(max-width:1279px)").matches; };

  /* ---------- mobile menu + dropdowns ---------- */
  var tog = $(".menu-toggle");
  if (tog) tog.addEventListener("click", function () {
    var on = document.body.classList.toggle("nav-open");
    tog.setAttribute("aria-expanded", on);
  });
  $$(".nav li.has-sub > a").forEach(function (a) {
    a.addEventListener("click", function (e) {
      var li = a.parentNode, dummy = a.getAttribute("href") === "#";
      if (mobile()) {
        /* first tap opens the sub-menu, second tap follows the link */
        if (!li.classList.contains("open")) { e.preventDefault(); closeSiblings(li); li.classList.add("open"); return; }
        if (dummy) { e.preventDefault(); li.classList.remove("open"); }
      } else if (dummy) { e.preventDefault(); }
    });
  });
  function closeSiblings(li) { $$(":scope > li.open", li.parentNode).forEach(function (s) { if (s !== li) s.classList.remove("open"); }); }
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav") && !e.target.closest(".menu-toggle")) {
      $$(".nav li.open").forEach(function (l) { l.classList.remove("open"); });
      document.body.classList.remove("nav-open");
    }
  });
  /* ---------- sticky header ---------- */
  var hdr = $(".site-header"), ph = document.createElement("div");
  if (hdr) { hdr.parentNode.insertBefore(ph, hdr.nextSibling); }
  var topH = hdr ? hdr.offsetHeight : 0;
  function onScroll() {
    var y = window.pageYOffset;
    if (hdr) {
      var stuck = y > (hdr.offsetTop > 0 ? hdr.offsetTop : 150) && y > 150;
      hdr.classList.toggle("stuck", stuck);
      ph.style.height = stuck ? topH + "px" : "0";
    }
    var t = $(".totop"); if (t) t.classList.toggle("on", y > 400);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  var tt = $(".totop"); if (tt) tt.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- search ---------- */
  var ov = $(".search-ov"), si = ov && $("input", ov), sl = ov && $("ul", ov);
  function openS() { ov.classList.add("on"); si.value = ""; render(""); setTimeout(function () { si.focus(); }, 50); }
  function closeS() { ov.classList.remove("on"); }
  function render(q) {
    q = q.toLowerCase().trim();
    var list = (D.pages || []).filter(function (p) { return !q || p[0].toLowerCase().indexOf(q) > -1; }).slice(0, 30);
    sl.innerHTML = list.length ? list.map(function (p) { return '<li><a href="' + root + p[1] + '">' + p[0] + "</a></li>"; }).join("") : '<li class="none">No page found. Try "packers", "Madhapur" or "bill".</li>';
  }
  $$(".search-btn").forEach(function (b) { b.addEventListener("click", openS); });
  if (ov) {
    $(".x", ov).addEventListener("click", closeS);
    si.addEventListener("input", function () { render(si.value); });
    si.addEventListener("keydown", function (e) { if (e.key === "Enter") { var a = $("a", sl); if (a) location.href = a.href; } });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeS(); });
  }

  /* ---------- counters + bars ---------- */
  function animate(el) {
    var to = +el.getAttribute("data-to"), t0 = null;
    (function step(t) { if (!t0) t0 = t; var p = Math.min((t - t0) / 1600, 1); el.textContent = Math.round(to * p); if (p < 1) requestAnimationFrame(step); })(performance.now());
  }
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      if (e.target.hasAttribute("data-to")) animate(e.target);
      if (e.target.classList.contains("f")) e.target.style.width = e.target.getAttribute("data-w") + "%";
      io.unobserve(e.target);
    });
  }, { threshold: .4 }) : null;
  $$("[data-to]").forEach(function (el) { io ? io.observe(el) : (el.textContent = el.getAttribute("data-to")); });
  $$(".bar .f").forEach(function (el) { io ? io.observe(el) : (el.style.width = el.getAttribute("data-w") + "%"); });

  /* ---------- quote forms ---------- */
  function val(f, n) { var e = f.elements[n]; return e ? e.value.trim() : ""; }
  function setErr(f, n, msg) { var e = $('[data-err="' + n + '"]', f); if (e) e.textContent = msg || ""; }
  $$("form[data-quote]").forEach(function (f) {
    var sel = f.elements.branch;
    var qs = new URLSearchParams(location.search);
    if (sel && qs.get("branch")) sel.value = qs.get("branch");
    if (f.elements.service && qs.get("service")) f.elements.service.value = qs.get("service");
    var d = f.elements.date; if (d) { var t = new Date(); d.min = new Date(t.getTime() - t.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); }
    function build() {
      var b = (D.branches || {})[sel ? sel.value : "beeramguda"] || { name: "Head Office", phone: D.hq };
      var lines = ["Hello Mint Relocation Packers, I would like a free quote.", "",
        "Name: " + val(f, "name"), "Phone: " + val(f, "phone")];
      if (val(f, "email")) lines.push("Email: " + val(f, "email"));
      lines.push("Service: " + (val(f, "service") || "Not sure yet"), "Moving from: " + val(f, "from"), "Moving to: " + val(f, "to"),
        "Moving date: " + (val(f, "date") || "Not decided"));
      if (val(f, "message")) lines.push("Message: " + val(f, "message"));
      lines.push("", "Branch: " + b.name);
      return { text: lines.join("\n"), branch: b };
    }
    function check() {
      var ok = true;
      setErr(f, "name"); setErr(f, "phone"); setErr(f, "from"); setErr(f, "to");
      if (val(f, "name").length < 2) { setErr(f, "name", "Please enter your name."); ok = false; }
      if (!/^[0-9+\-\s()]{10,15}$/.test(val(f, "phone"))) { setErr(f, "phone", "Enter a valid phone number."); ok = false; }
      if (!val(f, "from")) { setErr(f, "from", "Where are you moving from?"); ok = false; }
      if (!val(f, "to")) { setErr(f, "to", "Where are you moving to?"); ok = false; }
      return ok;
    }
    function done(msg) { var o = $(".ok", f); if (o) { o.innerHTML = msg; o.classList.add("on"); o.scrollIntoView({ block: "nearest", behavior: "smooth" }); } }
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!check()) return;
      var b = build();
      window.open("https://wa.me/91" + b.branch.phone + "?text=" + encodeURIComponent(b.text), "_blank");
      done("<b>Thank you!</b> WhatsApp has opened with your details for <b>" + b.branch.name + "</b>. Press send to finish. Prefer a call? <a href=\"tel:+91" + b.branch.phone + "\"><b>" + b.branch.phone + "</b></a>");
    });
    var em = $("[data-email]", f);
    if (em) em.addEventListener("click", function () {
      if (!check()) return;
      var b = build();
      location.href = "mailto:" + D.email + "?subject=" + encodeURIComponent("Free quote request - " + val(f, "name")) + "&body=" + encodeURIComponent(b.text);
      done("Your email app has opened with the details. Press send to finish.");
    });
  });

  /* ---------- newsletter ---------- */
  $$("form.subscribe").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = f.elements.email.value.trim();
      var m = $(".sub-msg", f.parentNode);
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { m.textContent = "Please enter a valid email address."; return; }
      m.textContent = "Thanks! Your email app will open to confirm your subscription.";
      location.href = "mailto:" + D.email + "?subject=" + encodeURIComponent("Newsletter subscription") + "&body=" + encodeURIComponent("Please add " + v + " to your newsletter.");
    });
  });

  /* ---------- blog ---------- */
  $$(".chip").forEach(function (c) {
    c.addEventListener("click", function () {
      $$(".chip").forEach(function (x) { x.classList.remove("on"); }); c.classList.add("on");
      var cat = c.getAttribute("data-cat");
      $$(".post").forEach(function (p) { p.style.display = (cat === "all" || p.getAttribute("data-cat") === cat) ? "" : "none"; });
    });
  });
  $$(".post button").forEach(function (b) {
    b.addEventListener("click", function () { var p = b.closest(".post"); p.classList.toggle("open"); b.textContent = p.classList.contains("open") ? "Show less" : "Read more"; });
  });
  if (location.hash && $(".chip[data-cat]")) {
    var h = decodeURIComponent(location.hash.slice(1)).replace(/-/g, " ").toLowerCase();
    $$(".chip").forEach(function (c) { if (c.getAttribute("data-cat").toLowerCase() === h) c.click(); });
  }
})();
