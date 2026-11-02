/* SHOP.CO template — behaviour. No dependencies. */
(function () {
  "use strict";

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- cart store (localStorage) ---------- */
  var KEY = "shopco_cart_v1";
  var DISCOUNT = 0.2;   // 20% off, as shown in the design
  var DELIVERY = 15;    // flat delivery fee

  var SEED = [
    { id: "gradient-graphic-t-shirt", name: "Gradient Graphic T-shirt", size: "Large", color: "White", price: 145, qty: 1 },
    { id: "checkered-shirt", name: "Checkered Shirt", size: "Medium", color: "Red", price: 180, qty: 1 },
    { id: "skinny-fit-jeans", name: "Skinny Fit Jeans", size: "Large", color: "Blue", price: 240, qty: 1 }
  ];

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw === null) return SEED.slice();           // first visit: show the demo cart from the design
      var v = JSON.parse(raw);
      return Array.isArray(v) ? v : [];
    } catch (e) { return SEED.slice(); }
  }
  function save(items) { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {} }
  function count(items) { return items.reduce(function (n, i) { return n + i.qty; }, 0); }
  function money(n) { return "$" + Math.round(n); }

  function updateBadge() {
    var n = count(load());
    $$("[data-cart-count]").forEach(function (el) { el.textContent = n ? String(n) : ""; el.setAttribute("data-count", n); });
  }

  /* ---------- header / banner ---------- */
  var banner = $("[data-close-banner]");
  if (banner) banner.addEventListener("click", function () { $("#topbar").classList.add("is-hidden"); });

  var menuBtn = $("[data-menu]");
  if (menuBtn) menuBtn.addEventListener("click", function () {
    var open = $("#nav").classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  var searchBtn = $("[data-search-toggle]");
  if (searchBtn) searchBtn.addEventListener("click", function () {
    var h = $("#header"); h.classList.toggle("search-open");
    if (h.classList.contains("search-open")) { var i = $("input[type=search]", h); if (i) i.focus(); }
  });

  /* ---------- newsletter ---------- */
  $$("[data-newsletter]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".news-msg", f), v = f.elements.email.value.trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { msg.textContent = "Please enter a valid email address."; return; }
      msg.textContent = "Thanks for subscribing!"; f.reset();
      // TODO: send `v` to your email provider / backend here.
    });
  });

  /* ---------- home: testimonials slider ---------- */
  var track = $("[data-track]");
  if (track) $$("[data-slide]").forEach(function (b) {
    b.addEventListener("click", function () {
      var card = track.firstElementChild;
      var step = card ? card.getBoundingClientRect().width + 20 : 320;
      track.scrollBy({ left: step * Number(b.getAttribute("data-slide")), behavior: "smooth" });
    });
  });

  /* ---------- category: filters ---------- */
  var filters = $("#filters");
  if (filters) {
    var scrim = $("[data-scrim]");
    function setFilters(open) {
      filters.classList.toggle("open", open);
      scrim.classList.toggle("on", open);
      document.body.style.overflow = open ? "hidden" : "";
    }
    $$("[data-open-filters]").forEach(function (b) { b.addEventListener("click", function () { setFilters(true); }); });
    $$("[data-close-filters],[data-apply-filter]").forEach(function (b) { b.addEventListener("click", function () { setFilters(false); }); });
    scrim.addEventListener("click", function () { setFilters(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setFilters(false); });

    $$(".f-title", filters).forEach(function (b) {
      b.addEventListener("click", function () {
        var g = b.parentElement, closed = g.classList.toggle("closed");
        b.setAttribute("aria-expanded", closed ? "false" : "true");
      });
    });
    // colours: multi select, sizes: single select
    $$(".swatch", filters).forEach(function (s) {
      s.addEventListener("click", function () {
        var on = s.classList.toggle("on"); s.setAttribute("aria-pressed", on ? "true" : "false");
      });
    });
    $$(".chips", filters).forEach(function (wrap) {
      $$(".chip", wrap).forEach(function (c) {
        c.addEventListener("click", function () {
          $$(".chip", wrap).forEach(function (o) { o.classList.remove("on"); o.setAttribute("aria-pressed", "false"); });
          c.classList.add("on"); c.setAttribute("aria-pressed", "true");
        });
      });
    });
    // price range
    var range = $("[data-range]", filters);
    if (range) {
      var ins = $$("input", range), fill = $(".fill", range), minL = $("[data-min]"), maxL = $("[data-max]");
      var draw = function (changed) {
        var a = Number(ins[0].value), b = Number(ins[1].value);
        if (a > b) { if (changed === ins[0]) { ins[0].value = a = b; } else { ins[1].value = b = a; } }
        var max = Number(ins[0].max);
        fill.style.left = (a / max * 100) + "%"; fill.style.width = ((b - a) / max * 100) + "%";
        minL.textContent = "$" + a; maxL.textContent = "$" + b;
      };
      ins.forEach(function (i) { i.addEventListener("input", function () { draw(i); }); });
      draw();
    }
  }
  // sorting (client side demo)
  var sortSel = $("[data-sort]"), grid = $("[data-grid]");
  if (sortSel && grid) {
    var original = $$(".card", grid);
    sortSel.addEventListener("change", function () {
      var cards = original.slice(), v = sortSel.value;
      if (v === "low") cards.sort(function (a, b) { return a.dataset.price - b.dataset.price; });
      if (v === "high") cards.sort(function (a, b) { return b.dataset.price - a.dataset.price; });
      if (v === "rating") cards.sort(function (a, b) { return b.dataset.rating - a.dataset.rating; });
      cards.forEach(function (c) { grid.appendChild(c); });
    });
  }

  /* ---------- product page ---------- */
  var pdp = $("[data-product]");
  if (pdp) {
    var thumbs = $$("[data-thumb]"), main = $("#main-img");
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () {
        thumbs.forEach(function (o) { o.classList.remove("on"); }); t.classList.add("on");
        var im = $("img", t); if (im && main) main.src = im.src;
      });
    });
    var singles = function (sel, attr) {
      $$(sel + " > *", pdp).forEach(function (b, _, all) {
        b.addEventListener("click", function () {
          all.forEach(function (o) { o.classList.remove("on"); o.setAttribute("aria-pressed", "false"); });
          b.classList.add("on"); b.setAttribute("aria-pressed", "true");
        });
      });
    };
    singles("[data-colors]"); singles("[data-sizes]");

    var qv = $("[data-qty-val]"), q = 1;
    $("[data-dec]").addEventListener("click", function () { q = Math.max(1, q - 1); qv.textContent = q; });
    $("[data-inc]").addEventListener("click", function () { q = Math.min(99, q + 1); qv.textContent = q; });

    $("[data-add-to-cart]").addEventListener("click", function () {
      var size = ($("[data-sizes] .on", pdp) || {}).textContent || "Large";
      var colorEl = $("[data-colors] .on", pdp), color = colorEl ? colorEl.getAttribute("data-color") : "Olive";
      var items = load();
      var hit = items.filter(function (i) { return i.id === pdp.dataset.id && i.size === size && i.color === color; })[0];
      if (hit) hit.qty += q; else items.push({ id: pdp.dataset.id, name: pdp.dataset.name, size: size, color: color, price: Number(pdp.dataset.price), qty: q });
      save(items); updateBadge();
      var m = $("[data-add-msg]"); m.textContent = "Added to cart.";
      setTimeout(function () { m.textContent = ""; }, 2500);
    });

    var tabs = $$("[data-tab]");
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        tabs.forEach(function (o) { o.classList.toggle("on", o === t); o.setAttribute("aria-selected", o === t ? "true" : "false"); });
        $$(".tab-panel").forEach(function (p) { p.hidden = p.id !== "tab-" + t.dataset.tab; });
      });
    });
  }

  /* ---------- cart page ---------- */
  var list = $("#cart-items");
  if (list) {
    var icons = {
      trash: '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/></svg>',
      minus: '<svg class="icon-xs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>',
      plus: '<svg class="icon-xs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
    };
    var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&", "<": "<", ">": ">", '"': """, "'": "&#39;" }[c]; }); };
    var items = load();

    var render = function () {
      if (!items.length) {
        list.innerHTML = '<div class="cart-empty"><p>Your cart is empty.</p><p style="margin-top:16px"><a class="btn btn-dark" href="category.html">Continue shopping</a></p></div>';
      } else {
        list.innerHTML = items.map(function (it, i) {
          return '<div class="cart-item" data-i="' + i + '">' +
            '<div class="pic"><img src="assets/img/products/' + esc(it.id) + '.png" alt="' + esc(it.name) + '" onerror="this.remove()"></div>' +
            '<div class="body"><div class="left"><div><h3>' + esc(it.name) + '</h3>' +
            '<div class="meta"><p>Size: <span>' + esc(it.size) + '</span></p><p>Color: <span>' + esc(it.color) + '</span></p></div></div>' +
            '<p class="amount">' + money(it.price) + '</p></div>' +
            '<div class="right"><button class="remove" type="button" aria-label="Remove ' + esc(it.name) + '" data-remove>' + icons.trash + '</button>' +
            '<div class="qty sm"><button type="button" aria-label="Decrease quantity" data-dec>' + icons.minus + '</button><span>' + it.qty + '</span>' +
            '<button type="button" aria-label="Increase quantity" data-inc>' + icons.plus + '</button></div></div></div></div>';
        }).join("");
      }
      totals(); updateBadge();
    };
    var totals = function () {
      var sub = items.reduce(function (n, i) { return n + i.price * i.qty; }, 0);
      var disc = sub * DISCOUNT, fee = items.length ? DELIVERY : 0;
      $("[data-subtotal]").textContent = money(sub);
      $("[data-discount]").textContent = "-" + money(disc);
      $("[data-delivery]").textContent = money(fee);
      $("[data-total]").textContent = money(sub - disc + fee);
    };
    list.addEventListener("click", function (e) {
      var row = e.target.closest(".cart-item"); if (!row) return;
      var i = Number(row.dataset.i);
      if (e.target.closest("[data-remove]")) items.splice(i, 1);
      else if (e.target.closest("[data-inc]")) items[i].qty = Math.min(99, items[i].qty + 1);
      else if (e.target.closest("[data-dec]")) items[i].qty = Math.max(1, items[i].qty - 1);
      else return;
      save(items); render();
    });

    var promo = $("[data-promo]");
    promo.addEventListener("submit", function (e) {
      e.preventDefault();
      var code = promo.elements.code.value.trim(), m = $("[data-promo-msg]");
      m.textContent = code ? "Promo codes aren't connected yet — add your own validation here." : "Enter a promo code first.";
      // TODO: validate `code` with your backend and adjust DISCOUNT / totals().
    });
    $("[data-checkout]").addEventListener("click", function (e) { e.preventDefault(); /* TODO: go to your checkout */ });
    render();
  }

  updateBadge();
})();
