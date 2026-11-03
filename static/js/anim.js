/* MINT RELOCATION — motion layer (scroll reveal, hero fx, truck, ticker, tilt, progress bar) */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover:hover) and (pointer:fine)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- progress bar ---- */
  var bar = document.createElement("div"); bar.className = "scroll-progress"; document.body.appendChild(bar);
  var tk = false;
  function prog() {
    var h = document.documentElement.scrollHeight - innerHeight, y = pageYOffset;
    bar.style.transform = "scaleX(" + (h > 0 ? Math.min(y / h, 1) : 0) + ")"; tk = false;
  }
  addEventListener("scroll", function () { if (!tk) { tk = true; requestAnimationFrame(prog); } }, { passive: true }); prog();

  /* ---- HOME-only extras ---- */
  var hero = $(".hero");
  if (hero) {
    /* highlighter sweep behind the bold headline words */
    var hb = $("h1 b", hero); if (hb) hb.innerHTML = '<span class="hl">' + hb.innerHTML + "</span>";

    /* floating badges on the photo */
    var ph = $(".ph", hero);
    if (ph) {
      ph.insertAdjacentHTML("beforeend",
        '<div class="hchip a"><i>★</i>5+ Years Trusted</div>' +
        '<div class="hchip b"><i>✓</i>Safe Transport</div>' +
        '<div class="hchip c"><i>⏱</i>24/7 Support</div>');
    }

    /* drifting boxes & shapes */
    var fx = document.createElement("div"); fx.className = "hero-fx";
    var S = [
      ["box", "0.5%", "42%", 52, 10, 9, 14], ["box", "47%", "72%", 40, 14, 11, -16], ["box", "90%", "8%", 48, 18, 10, 22],
      ["sq", "40%", "10%", 38, 12, 8, 90], ["sq", "78%", "78%", 54, 8, 12, -60], ["sq", "3%", "74%", 30, 16, 9, 45],
      ["fill", "30%", "86%", 20, 20, 7, 50], ["fill", "58%", "6%", 16, 22, 8, -40], ["fill", "94%", "52%", 24, 14, 10, 80],
      ["dot", "20%", "28%", 14, 24, 6, 0], ["dot", "66%", "92%", 18, 12, 9, 0], ["dot", "50%", "40%", 12, 26, 7, 0]
    ];
    S.forEach(function (a, i) {
      var e = document.createElement("span");
      e.className = "shape " + a[0];
      e.style.cssText = "left:" + a[1] + ";top:" + a[2] + ";--s:" + a[3] + "px;--k:" + a[4] + ";--t:" + a[5] + "s;--r:" + a[6] + "deg;animation-delay:-" + (i * 0.8) + "s";
      fx.appendChild(e);
    });
    hero.insertBefore(fx, hero.firstChild);

    /* mouse: photo tilt + shape parallax */
    if (fine && !reduce) {
      hero.addEventListener("mousemove", function (e) {
        var r = hero.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        fx.style.setProperty("--mx", x.toFixed(3)); fx.style.setProperty("--my", y.toFixed(3));
        $$(".shape", fx).forEach(function (s) { s.style.setProperty("--mx", x.toFixed(3)); s.style.setProperty("--my", y.toFixed(3)); });
        if (ph) { ph.style.transition = "transform .15s ease-out"; ph.style.transform = "perspective(1000px) rotateY(" + (x * 7).toFixed(2) + "deg) rotateX(" + (-y * 7).toFixed(2) + "deg)"; }
      });
      hero.addEventListener("mouseleave", function () {
        if (ph) { ph.style.transition = "transform .8s cubic-bezier(.2,.7,.2,1)"; ph.style.transform = "perspective(1000px) rotateY(0) rotateX(0)"; }
      });
    }

    /* driving truck strip right under the hero */
    var truck =
      '<svg class="truck" viewBox="0 0 280 118" aria-hidden="true">' +
      '<g class="speed"><rect x="-14" y="30" width="26" height="4" rx="2" fill="#1b2024" opacity=".35"/></g>' +
      '<g class="speed s2"><rect x="-22" y="52" width="34" height="4" rx="2" fill="#1b2024" opacity=".35"/></g>' +
      '<g class="speed s3"><rect x="-10" y="72" width="24" height="4" rx="2" fill="#1b2024" opacity=".35"/></g>' +
      '<circle class="puff" cx="12" cy="86" r="7" fill="#9aa0a6"/><circle class="puff p2" cx="12" cy="86" r="7" fill="#9aa0a6"/><circle class="puff p3" cx="12" cy="86" r="7" fill="#9aa0a6"/>' +
      '<rect x="10" y="8" width="176" height="76" rx="4" fill="#ffdc39"/>' +
      '<rect x="10" y="74" width="176" height="10" fill="#e6b800"/>' +
      '<text x="98" y="44" text-anchor="middle" font-family="Biryani,Arial,sans-serif" font-weight="800" font-size="24" fill="#1b2024">MINT</text>' +
      '<text x="98" y="63" text-anchor="middle" font-family="Biryani,Arial,sans-serif" font-weight="700" font-size="10.5" letter-spacing="1.6" fill="#1b2024">RELOCATION PACKERS</text>' +
      '<path d="M192 26h44q9 0 13 8l20 26q4 5 4 11v14H192z" fill="#1b2024"/>' +
      '<path d="M201 35h31q5 0 8 5l12 17h-51z" fill="#cfe9ff"/>' +
      '<rect x="10" y="84" width="260" height="10" fill="#1b2024"/>' +
      '<circle cx="272" cy="72" r="5" fill="#fff6b0"/>' +
      '<g class="wheel"><circle cx="52" cy="98" r="17" fill="#1b2024"/><circle cx="52" cy="98" r="8" fill="#cfd4d8"/><path d="M52 90v16M44 98h16" stroke="#1b2024" stroke-width="2.5"/></g>' +
      '<g class="wheel"><circle cx="128" cy="98" r="17" fill="#1b2024"/><circle cx="128" cy="98" r="8" fill="#cfd4d8"/><path d="M128 90v16M120 98h16" stroke="#1b2024" stroke-width="2.5"/></g>' +
      '<g class="wheel"><circle cx="228" cy="98" r="17" fill="#1b2024"/><circle cx="228" cy="98" r="8" fill="#cfd4d8"/><path d="M228 90v16M220 98h16" stroke="#1b2024" stroke-width="2.5"/></g>' +
      "</svg>";
    var strip = document.createElement("div"); strip.className = "roadstrip"; strip.setAttribute("aria-hidden", "true");
    strip.innerHTML = '<span class="sun"></span><span class="cloud" style="--y:22px;--t:46s"></span><span class="cloud" style="--y:62px;--t:62s;animation-delay:-20s"></span>' +
      '<div class="road"></div><div class="truckwrap">' + truck + "</div>";
    hero.parentNode.insertBefore(strip, hero.nextSibling);

    /* scrolling ticker above the counters */
    var counters = $(".counters");
    if (counters) {
      var items = ["Careful Packing", "Safe Transport", "On-Time Delivery", "Local & Interstate Moves", "24/7 Support", "GST Bill for Claim", "Hyderabad & Across India"];
      var one = items.map(function (t) { return "<span>" + t + "</span>"; }).join("");
      var tkr = document.createElement("div"); tkr.className = "ticker"; tkr.setAttribute("aria-hidden", "true");
      tkr.innerHTML = '<div class="track">' + one + one + one + one + "</div>";
      counters.parentNode.insertBefore(tkr, counters);
    }
  }

  /* ---- scroll reveal ---- */
  function mark(list, opt) {
    list.forEach(function (el, i) {
      if (el.classList.contains("reveal") || el.closest(".hero")) return;
      el.classList.add("reveal");
      if (opt && opt.cls) el.classList.add(opt.cls);
      var step = (opt && opt.stagger) || 0;
      if (step) el.style.setProperty("--d", ((opt.mod ? i % opt.mod : i) * step).toFixed(2) + "s");
    });
  }
  mark($$(".sec .center, .counters .center"));
  $$(".grid").forEach(function (g) { mark($$(":scope > *", g), { stagger: .12, mod: 3, cls: g.closest(".counters") ? "pop" : "" }); });
  $$(".split").forEach(function (s) { var k = $$(":scope > *", s); mark([k[0]], { cls: "left" }); mark([k[1]], { cls: "right" }); });
  $$(".layout").forEach(function (l) { mark($$(":scope > *", l), { stagger: .15 }); });
  mark($$(".feat > div"), { stagger: .12 });
  mark($$(".bar"));
  mark($$(".band .container"), { cls: "pop" });
  mark($$(".footer .cols > *, .footer .contact > *"), { stagger: .12, mod: 3 });
  $$(".tick").forEach(function (u) { mark($$(":scope > li", u), { stagger: .08, cls: "left" }); });
  mark($$(".side .card"), { stagger: .12 });

  function done(el) {
    /* hand control back to the page's own hover transitions once revealed */
    var d = parseFloat(el.style.getPropertyValue("--d")) || 0;
    setTimeout(function () { el.classList.remove("reveal", "in", "left", "right", "pop"); el.style.removeProperty("--d"); }, (d + 1) * 1000);
  }
  var els = $$(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); done(e.target); } });
    }, { threshold: .12, rootMargin: "0px 0px -6% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.remove("reveal"); }); }
})();
