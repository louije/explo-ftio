/* ── France Travail API Catalogue ──
   Vanilla JS — no dependencies.
   Reads the CATALOGUE global from catalogue-data.js.
*/

var state = { query: "", group: "all", auths: new Set(), view: "cards" };

var AUTH_LABELS = { peconnect: "PE Connect", agent: "Agent", public: "Public" };

// ── Normalisation for search ──

function normalize(str) {
  return str.toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ").trim();
}

// Build search corpus for each API (once, on init)
var searchCorpus = {};

function buildCorpus() {
  CATALOGUE.apis.forEach(function(api) {
    var parts = [
      api.title, api.description, api.slug, api.baseUrl, api.groupLabel,
      AUTH_LABELS[api.auth] || "",
    ];
    api.endpoints.forEach(function(ep) {
      parts.push(ep.summary, ep.path);
    });
    api.schemas.forEach(function(s) { parts.push(s); });
    if (api.concepts) api.concepts.forEach(function(c) { parts.push(c); });
    searchCorpus[api.slug] = normalize(parts.join(" "));
  });
}

// ── Rendering ──

function escapeHtml(str) {
  var div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function renderCards() {
  var grid = document.getElementById("api-grid");
  var html = "";
  CATALOGUE.apis.forEach(function(api) {
    var authLabel = AUTH_LABELS[api.auth] || api.auth;
    var hasExploration = api.hasDocPage && api.concepts && api.concepts.length > 0;
    var docPath = "docs/" + api.slug + ".html";

    // Detail content depends on whether an exploration page exists
    var detailInner = "";
    if (hasExploration) {
      // Concept chips (no endpoint/schema lists)
      var conceptHtml = "";
      api.concepts.forEach(function(c) {
        conceptHtml += '<span class="cat-concept">' + escapeHtml(c) + '</span>';
      });
      detailInner =
        '<div class="cat-detail-section">' +
          '<div class="cat-detail-concepts">' + conceptHtml + '</div>' +
        '</div>';
    } else {
      // Full endpoint/schema list for APIs without exploration
      var epHtml = "";
      api.endpoints.forEach(function(ep) {
        epHtml += '<div class="cat-detail-ep">' +
          '<span class="ep-method m-' + ep.method.toLowerCase() + '">' + ep.method + '</span>' +
          '<span class="cat-ep-path">' + escapeHtml(ep.path) + '</span>' +
          '<span class="cat-ep-summary">' + escapeHtml(ep.summary) + '</span>' +
          '</div>';
      });
      var schemaHtml = "";
      api.schemas.forEach(function(s) {
        schemaHtml += '<span class="schema-chip-mini">' + escapeHtml(s) + '</span>';
      });
      detailInner =
        '<div class="cat-detail-section">' +
          '<div class="cat-detail-title">Endpoints</div>' +
          epHtml +
        '</div>' +
        '<div class="cat-detail-section">' +
          '<div class="cat-detail-title">Schémas</div>' +
          '<div class="cat-detail-schemas">' + schemaHtml + '</div>' +
        '</div>';
    }

    // Bottom links
    var linksHtml = '';
    if (hasExploration) {
      linksHtml += '<a href="' + docPath + '" class="cat-link">Exploration</a>';
    }
    if (api.pageId) {
      linksHtml += '<a href="https://francetravail.io/data/api/' + api.slug + '?tabgroup-api=documentation" class="cat-link cat-link-ext" target="_blank" rel="noopener">francetravail.io</a>';
    }
    linksHtml += '<a href="schemas/' + api.slug + '.json" class="cat-link">OpenAPI JSON</a>';

    // Title: link with arrow when exploration exists, plain text otherwise
    var titleHtml = hasExploration
      ? '<a href="' + docPath + '" class="cat-card-title cat-card-title-link">' + escapeHtml(api.title) + ' \u2192</a>'
      : '<div class="cat-card-title">' + escapeHtml(api.title) + '</div>';

    html += '<div class="cat-card" data-slug="' + api.slug + '" data-group="' + api.group + '" data-auth="' + api.auth + '">' +
      '<div class="cat-card-head">' +
        titleHtml +
        '<div class="cat-card-version">v' + escapeHtml(api.version) + '</div>' +
      '</div>' +
      '<div class="cat-card-desc">' + escapeHtml(api.description) + '</div>' +
      '<div class="cat-card-stats">' +
        '<span class="cat-stat">' + api.endpointCount + ' endpoint' + (api.endpointCount > 1 ? 's' : '') + '</span>' +
        '<span class="cat-stat">' + api.schemaCount + ' schéma' + (api.schemaCount > 1 ? 's' : '') + '</span>' +
      '</div>' +
      '<div class="cat-card-tags">' +
        '<span class="cat-tag cat-tag-' + api.auth + '">' + authLabel + '</span>' +
        '<span class="cat-tag cat-tag-group">' + escapeHtml(api.groupLabel) + '</span>' +
      '</div>' +
      '<div class="cat-card-base">' + escapeHtml(api.baseUrl) + '</div>' +
      '<div class="cat-card-detail">' +
        detailInner +
        '<div class="cat-card-links">' + linksHtml + '</div>' +
      '</div>' +
    '</div>';
  });
  grid.innerHTML = html;
}

function renderCross() {
  var container = document.getElementById("v-cross");
  var html = "";
  CATALOGUE.crossConcepts.forEach(function(concept) {
    var chipsHtml = "";
    concept.apis.forEach(function(slug) {
      var api = CATALOGUE.apis.find(function(a) { return a.slug === slug; });
      var label = api ? api.title : slug;
      chipsHtml += '<button class="cross-api-link" data-slug="' + slug + '">' + escapeHtml(label) + '</button>';
    });
    html += '<div class="cross-concept">' +
      '<div class="cross-head">' +
        '<div class="cross-name">' + escapeHtml(concept.name) + '</div>' +
        (concept.collision ? '<span class="cross-collision">Collision de schémas</span>' : '') +
        '<span class="cross-count">' + concept.apis.length + ' APIs</span>' +
      '</div>' +
      '<div class="cross-apis">' + chipsHtml + '</div>' +
    '</div>';
  });
  container.innerHTML = html;
}

function renderFilters() {
  var container = document.getElementById("filters");
  var html = '<button class="cat-filter active" data-filter="all">Tout <span class="cat-count">' + CATALOGUE.apis.length + '</span></button>';

  CATALOGUE.groups.forEach(function(g) {
    var count = CATALOGUE.apis.filter(function(a) { return a.group === g.id; }).length;
    html += '<button class="cat-filter" data-filter="' + g.id + '">' + escapeHtml(g.label) + ' <span class="cat-count">' + count + '</span></button>';
  });

  html += '<span class="cat-filter-sep"></span>';
  ["peconnect", "agent", "public"].forEach(function(auth) {
    html += '<button class="cat-filter cat-filter-auth" data-auth="' + auth + '">' + AUTH_LABELS[auth] + '</button>';
  });

  container.innerHTML = html;
}

// ── Filtering ──

function matchesSearch(api) {
  if (!state.query) return true;
  var corpus = searchCorpus[api.slug];
  var tokens = normalize(state.query).split(" ");
  for (var i = 0; i < tokens.length; i++) {
    if (tokens[i] && corpus.indexOf(tokens[i]) === -1) return false;
  }
  return true;
}

function applyFilters() {
  var visible = 0;
  var cards = document.querySelectorAll(".cat-card");
  cards.forEach(function(card) {
    var slug = card.getAttribute("data-slug");
    var group = card.getAttribute("data-group");
    var auth = card.getAttribute("data-auth");
    var api = CATALOGUE.apis.find(function(a) { return a.slug === slug; });

    var show = true;
    if (state.group !== "all" && group !== state.group) show = false;
    if (state.auths.size > 0 && !state.auths.has(auth)) show = false;
    if (show && !matchesSearch(api)) show = false;

    if (show) {
      card.removeAttribute("hidden");
      visible++;
    } else {
      card.setAttribute("hidden", "");
    }
  });

  // Update counter
  document.getElementById("search-meta").textContent = visible + " API" + (visible > 1 ? "s" : "");

  // Empty state
  var grid = document.getElementById("api-grid");
  var empty = grid.querySelector(".cat-empty");
  if (visible === 0 && !empty) {
    grid.insertAdjacentHTML("beforeend", '<div class="cat-empty">Aucune API ne correspond à cette recherche.</div>');
  } else if (visible > 0 && empty) {
    empty.remove();
  }

  highlightMatches();
}

// ── Search highlighting ──

function clearHighlights() {
  document.querySelectorAll(".cat-card mark").forEach(function(mark) {
    var parent = mark.parentNode;
    parent.replaceChild(document.createTextNode(mark.textContent), mark);
    parent.normalize();
  });
}

function highlightInElement(el, tokens) {
  if (!tokens.length) return;
  var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
  var textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);

  textNodes.forEach(function(node) {
    var text = node.textContent;
    var normalized = normalize(text);
    var hasMatch = tokens.some(function(t) { return normalized.indexOf(t) !== -1; });
    if (!hasMatch) return;

    // Build regex from tokens
    var pattern = tokens.map(function(t) {
      return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }).join("|");
    var regex = new RegExp("(" + pattern + ")", "gi");
    var parts = text.split(regex);
    if (parts.length <= 1) return;

    var frag = document.createDocumentFragment();
    parts.forEach(function(part) {
      if (regex.test(part)) {
        var mark = document.createElement("mark");
        mark.textContent = part;
        frag.appendChild(mark);
      } else {
        frag.appendChild(document.createTextNode(part));
      }
      regex.lastIndex = 0;
    });
    node.parentNode.replaceChild(frag, node);
  });
}

function highlightMatches() {
  clearHighlights();
  if (!state.query) return;
  var tokens = normalize(state.query).split(" ").filter(Boolean);
  document.querySelectorAll(".cat-card:not([hidden])").forEach(function(card) {
    highlightInElement(card.querySelector(".cat-card-title"), tokens);
    highlightInElement(card.querySelector(".cat-card-desc"), tokens);
  });
}

// ── Event bindings ──

function bindSearch() {
  var input = document.getElementById("search");
  var timer;
  input.addEventListener("input", function() {
    clearTimeout(timer);
    timer = setTimeout(function() {
      state.query = input.value;
      applyFilters();
      updateHash();
    }, 120);
  });
}

function bindFilters() {
  document.getElementById("filters").addEventListener("click", function(e) {
    var btn = e.target.closest(".cat-filter");
    if (!btn) return;

    if (btn.hasAttribute("data-auth")) {
      // Auth filter: additive toggle
      var auth = btn.getAttribute("data-auth");
      if (state.auths.has(auth)) {
        state.auths.delete(auth);
        btn.classList.remove("active");
      } else {
        state.auths.add(auth);
        btn.classList.add("active");
      }
    } else {
      // Group filter: exclusive toggle
      var filter = btn.getAttribute("data-filter");
      state.group = filter;
      document.querySelectorAll(".cat-filter:not(.cat-filter-auth)").forEach(function(b) {
        b.classList.toggle("active", b.getAttribute("data-filter") === filter);
      });
    }
    applyFilters();
    updateHash();
  });
}

function bindCrossLinks() {
  document.getElementById("v-cross").addEventListener("click", function(e) {
    var btn = e.target.closest(".cross-api-link");
    if (!btn) return;
    var slug = btn.getAttribute("data-slug");
    // Switch to cards view
    setView("cards");
    // Clear filters to show all
    state.group = "all";
    state.auths.clear();
    state.query = slug;
    document.getElementById("search").value = slug;
    document.querySelectorAll(".cat-filter").forEach(function(b) {
      b.classList.toggle("active", b.getAttribute("data-filter") === "all");
    });
    document.querySelectorAll(".cat-filter-auth").forEach(function(b) {
      b.classList.remove("active");
    });
    applyFilters();
    // Scroll to the card
    var card = document.querySelector('.cat-card[data-slug="' + slug + '"]');
    if (card) {
      card.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    updateHash();
  });
}

// ── View switching ──

function setView(id) {
  document.querySelectorAll(".view").forEach(function(v) { v.classList.remove("active"); });
  document.getElementById("v-" + id).classList.add("active");
  document.querySelectorAll(".tab-group .tb").forEach(function(b, i) {
    b.classList.toggle("active", (id === "cards" && i === 0) || (id === "cross" && i === 1));
  });
  // Hide search + filters when on cross view
  var controls = document.getElementById("cards-controls");
  if (controls) controls.style.display = (id === "cards") ? "" : "none";
  state.view = id;
  updateHash();
}

// ── Hash routing ──

function updateHash() {
  var parts = [];
  if (state.view !== "cards") parts.push("view=" + state.view);
  if (state.group !== "all") parts.push("group=" + state.group);
  if (state.auths.size) parts.push("auth=" + Array.from(state.auths).join(","));
  if (state.query) parts.push("q=" + encodeURIComponent(state.query));
  var hash = parts.length ? "#" + parts.join("&") : "";
  history.replaceState(null, "", hash || location.pathname);
}

function resolveHash() {
  var hash = location.hash.replace("#", "");
  if (!hash) return;

  var params = {};
  hash.split("&").forEach(function(pair) {
    var kv = pair.split("=");
    params[kv[0]] = decodeURIComponent(kv[1] || "");
  });

  if (params.view) state.view = params.view;
  if (params.group) state.group = params.group;
  if (params.auth) {
    params.auth.split(",").forEach(function(a) { state.auths.add(a); });
  }
  if (params.q) {
    state.query = params.q;
    document.getElementById("search").value = params.q;
  }

  // Apply view
  if (state.view !== "cards") setView(state.view);

  // Apply group filter UI
  document.querySelectorAll(".cat-filter:not(.cat-filter-auth)").forEach(function(b) {
    b.classList.toggle("active", b.getAttribute("data-filter") === state.group);
  });

  // Apply auth filter UI
  document.querySelectorAll(".cat-filter-auth").forEach(function(b) {
    b.classList.toggle("active", state.auths.has(b.getAttribute("data-auth")));
  });

  applyFilters();
}

// ── Stats ──

function renderStats() {
  var totalEndpoints = 0, totalSchemas = 0;
  CATALOGUE.apis.forEach(function(api) {
    totalEndpoints += api.endpointCount;
    totalSchemas += api.schemaCount;
  });
  document.getElementById("total-endpoints").textContent = totalEndpoints;
  document.getElementById("total-schemas").textContent = totalSchemas;
}

// ── Init ──

function init() {
  buildCorpus();
  renderStats();
  renderFilters();
  renderCards();
  renderCross();
  bindSearch();
  bindFilters();
  bindCrossLinks();
  resolveHash();
}

document.addEventListener("DOMContentLoaded", init);
window.addEventListener("hashchange", function() {
  state = { query: "", group: "all", auths: new Set(), view: "cards" };
  resolveHash();
});
