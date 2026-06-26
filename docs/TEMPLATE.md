# France Travail API Documentation — Template Reference

Single-page HTML documentation for each France Travail OpenAPI schema. One HTML
file per API, all sharing `style.css` and `script.js`.

The goal is **human-first explanation**, not raw spec dumping: say what the data
*means* and when to use the API, and keep the technical detail legible but
secondary.

## File structure

```
docs/
  style.css               ← shared stylesheet (all pages)
  script.js               ← shared behaviour (tabs, version toggle, example sync, hash)
  {api-slug}.html         ← one file per API (slug = schemas/{slug}.json)
  diagnostic-usager.html  ← a good full reference implementation
  TEMPLATE.md             ← this file
../scripts/
  gen-famille.py          ← injects the "Famille" tab (see "Generated tabs")
  gen-referentiels-stats.py
../build-catalogue.ts     ← schemas/*.json → catalogue-data.js (the home page data)
```

Create `{slug}.html` by hand (Modèle / Référentiels / Couverture / Exemple, plus
optional disambiguation). The **Famille** tab is generated — don't write it.

---

## Tabs

A page has these tabs, in this order. Only Modèle, Couverture and Exemple are
mandatory.

| Tab | id | Purpose | Authored? |
|-----|----|---------|-----------|
| **Modèle** | `nested` | The response data model, as nested coloured cards | by hand |
| *Disambiguation* | e.g. `versions`, `vs`, `profil` | Optional: distinguish this API from a close sibling | by hand |
| **Référentiels** | `ref` | Enums / vocabularies / coded values the API uses | by hand |
| **Couverture API** | `coverage` | Endpoint + schema inventory | by hand |
| **Exemple** | `example` | Realistic request/response, JSON ↔ narrative | by hand |
| **Famille** | `famille` | Navigation to the API's catalogue family | **generated** |

Tabs are generic: each `.tb` button has `onclick="setTab('xxx')"` and the matching
view is `<div class="view" id="v-xxx">`. The first view carries `active`.

### Page skeleton

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Nom humain} — Schéma complet</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container" id="doc">

<a href="../index.html" class="back-link">← Catalogue</a>

<header>
  <h1>{Nom humain}</h1>
  <div class="sub">{Une phrase : ce que fait l'API, pour qui}</div>
  <div class="sub-tech">{Titre technique} v{version} — {N} endpoints · {M} schémas</div>
  <div class="endpoint-tag"><strong>Base</strong> {base sans https://}</div>
</header>

<div class="controls">
  <div class="tab-group">
    <button class="tb active" onclick="setTab('nested')">Modèle</button>
    <button class="tb" onclick="setTab('ref')">Référentiels</button>
    <button class="tb" onclick="setTab('coverage')">Couverture API</button>
    <button class="tb" onclick="setTab('example')">Exemple</button>
    <!-- the Famille tab is appended by scripts/gen-famille.py -->
  </div>
</div>

<div class="view active" id="v-nested"> … </div>
<div class="view" id="v-ref"> … </div>
<div class="view" id="v-coverage"> … </div>
<div class="view" id="v-example"> … </div>

<footer>
  OpenAPI {spec} — {Titre} v{version} · {host} · {N} endpoints · {M} schémas
</footer>

</div>
<script src="script.js"></script>
</body>
</html>
```

`id="doc"` on the container is required by the version toggle (below); harmless
otherwise.

---

## Token styling — concepts vs values vs examples

This is the core convention. Four visual roles, each meaning something precise —
think syntax highlighting. Get this right and a reader can tell at a glance what
is part of the contract and what is just an illustration.

| Role | Markup | Looks like | Use for |
|------|--------|------------|---------|
| **Field / property name** | `<code>champ</code>` (inside `.fi`/`.fi-tech`) | bold solid mono chip | the contract's identifiers — `siret`, `codePourquoi` |
| **Enum keyword** | `<span class="ev">VAL</span>` | green mono chip | a value from a defined set — `PED`, `RIASEC`, `SIGNE` |
| **Illustrative example** | `<span class="eg">ex. …</span>` | *italic, non-mono, muted* | a made-up sample — *ex. Employé de commerce* |
| **Schema / type** | `.dto`, `.card-tech`, `<span class="at">@ Dto</span>` | small muted mono | DTO names, cardinality, type references |

Rule of thumb: a value the API actually defines (an `enum`) → `.ev`. A value you
invented to illustrate → `.eg`. Don't dress an example up as a keyword.

---

## Tab — Modèle (nested data model)

Response schema as nested, coloured cards mirroring the JSON structure.

```html
<div class="n {level-color} [stack]" id="m-{slug}">
  <div class="nh"><div class="dot"></div>
    <div class="name">{Nom humain} <span class="dto">{champ · Dto}</span></div>
    <div class="card">{Cardinalité} <span class="card-tech">{type · 1:1}</span></div>
  </div>
  <div class="nb">
    <div class="fi">{Ce que la donnée veut dire}
      <div class="fi-tech"><code>{champ1}</code> · <code>{champ2}</code> ·
        <span class="ev">ENUM_A</span> · <span class="at">@ Dto</span></div>
    </div>
    <!-- nested children -->
  </div>
</div>
```

### Cardinality

| Human | Tech | CSS |
|-------|------|-----|
| Unique / Facultatif | object · 1:1 / 0:1 | (no `.stack`) |
| 0 ou plusieurs / 1 ou plusieurs | array · 0:N / 1:N | `.stack` |

`.stack` draws the "stacked cards" shadow (arrays). When a `.fi` text node is
directly followed by nested `.n` boxes, they get a gap automatically.

### Level colours

Assign by **semantic role**, not depth. `.l0` root (black). Top-level domains:
`.l1-b` orange, `.l1-c` red, `.l1-p` purple, `.l1-n` teal. Sub-entities/leaves:
`.l2d` pink, `.l2t` green, `.l2c` amber, `.l3` gray, `.l3b/.l3s/.l3o` light
green/purple/yellow. Pick what reads well; you can add `.l1-x` following the same
pattern.

---

## Tab — Référentiels (vocabularies & coded values)

For the enums / coded values the API relies on. Skip the tab if the API has none.

```html
<div class="view" id="v-ref">
  <div class="note" style="margin-bottom:20px;">{contexte : d'où viennent ces valeurs}</div>

  <div class="ref-section">
    <h2 class="ref-section-title">
      <span class="rs-dot" style="background:#0d9488;"></span>
      {Titre de section}
      <span class="rs-count">{N} valeurs</span>
      <span class="rs-tech">schéma <code>{Dto.champ}</code></span>
    </h2>
    <div class="ref-section-intro">{Toujours une phrase ici — un titre ne doit jamais toucher la boîte qui suit.}</div>
    <div class="ref-families">
      <div class="ref-card voc-card">
        <div class="ref-head"><span class="ref-title">{Sous-titre}</span><span class="ref-count">{N}</span></div>
        <ul class="ref-list voc-list">
          <li><span class="voc-code">CODE</span> Libellé lisible</li>
        </ul>
        <div class="voc-tech"><code>champ</code> — précision technique.</div>
      </div>
    </div>
  </div>
</div>
```

- `.ref-families` is a responsive card grid. `.voc-list` rows wrap cleanly when a
  `.voc-code` is long.
- **Always put a `.ref-section-intro` between a `.ref-section-title` and the cards** —
  the title has a bottom border and must not sit flush against the next box.

---

## Tab — Disambiguation (optional)

When an API is easily confused with a sibling (a v1/v2 pair, two APIs on the same
data, a family member), add a tab that spells out the difference. Reuse the
`.ref-section` structure, and lead each comparison with prominent prose:

```html
<div class="expl">{L'explication, en clair — c'est le point de la page.}</div>
```

`.expl` is body-weight readable text (concepts in `<code>`), unlike the small dim
`.voc-tech`. Put the explanation **first**; field-name boxes are reference below.
For a highlighted "current" card use `style="border-color:#a7f3d0;background:#f0fdf4;"`.

Examples in the repo: orientation-usager (`versions` tab, with the version toggle),
experiences-declarees-employeur (`sources`), competences-professionnelles (`profil`),
la-bonne-boite (`vs`).

---

## Version toggle (one page, several API versions)

When two versions coexist (e.g. Orientation Usager v1 & v2), keep one page with a
header toggle instead of two pages. Wrap each version's per-tab content in a
`.verblock`:

```html
<header>
  <h1>{Nom}</h1>
  <div class="ver-toggle">
    <button class="vb" onclick="setVersion('v1')">v1.0</button>
    <button class="vb active" onclick="setVersion('v2')">v2.0</button>
  </div>
  <div class="sub">…</div>
  <div class="verblock ver-v1"><div class="sub-tech">… v1 …</div> …</div>
  <div class="verblock ver-v2"><div class="sub-tech">… v2 …</div> …</div>
</header>

<div class="view active" id="v-nested">
  <div class="verblock ver-v1"> … modèle v1 … </div>
  <div class="verblock ver-v2"> … modèle v2 … </div>
</div>
```

`setVersion()` flips `#doc[data-version]`; CSS shows only the active `.verblock`.
A version-agnostic `v1 → v2` tab (no `.verblock`) explains what changed.

**Gotcha:** every `data-section` and `id` must be unique on the page, so suffix
them per version (`s-calcul-v1` / `s-calcul-v2`, `m-root-v1` / `m-root-v2`).

---

## Tab — Couverture API

Endpoints grouped by domain, then a schema chip grid.

```html
<div class="domain">
  <div class="domain-title">{Domaine} <span class="dt-human">— {explication}</span></div>
  <div style="background:#fff;border:1px solid var(--border);border-radius:8px;overflow:hidden;">
    <div class="ep-row"><span class="ep-method m-get">GET</span><div>
      <span class="ep-desc">{résumé technique}</span>
      <div class="ep-human">{une ligne humaine}</div>
      <span class="ep-path">{/chemin}</span></div></div>
  </div>
</div>

<div class="schema-grid">
  <div class="schema-chip"><span class="sc-dot sc-read"></span><span class="sc-name">Dto</span> <span class="sc-desc">— …</span></div>
</div>
```

Methods: `.m-get .m-post .m-put .m-delete .m-patch`. Schema dots: `.sc-read`
(green), `.sc-write` (blue), `.sc-ref` (amber), `.sc-hist` (purple), `.sc-misc`
(gray) — add a `.sc-legend` above the grid.

For a list of filter params, prefer a chip list over a `·`-separated run:

```html
<div class="note"><strong>Filtres</strong>
  <div class="chips"><code>dep</code><code>proxycom</code></div></div>
```

`code` inside a `.note` is styled (readable chip); `.chips` lays them out as a
wrapping row.

---

## Tab — Exemple (JSON + narrative, synced)

Two panels sharing `data-section` values; hovering or clicking one highlights /
scrolls the other (handled by `script.js`).

```html
<div class="story"><strong>{Titre}</strong> — {persona + scénario réaliste}</div>
<div class="example-split">
  <div class="panel panel-json" id="panel-json">
    <div class="json-tree"><div data-section="s-x"> …json… </div></div>
  </div>
  <div class="panel panel-human" id="panel-human">
    <div data-section="s-x"> …cartes narratives… </div>
  </div>
</div>
```

JSON is hand-written HTML inside `white-space: pre`: `.jk` key, `.js` string,
`.jn` number, `.jb` boolean, `.jnull` null, `.jc` comment.

Narrative cards: `.ex-title` + `.ex-ico`, `.ex-card` (`h4` + `p`), `.ex-sub` /
`.ex-item`, `.ex-agent` (attribution). Status tags `.ex-tag tag-*` (below).

Each `data-section` value must appear exactly once per panel (suffix per version
on version-toggle pages). Flag any invented values as illustrative.

---

## Inline & tag reference

| Class | Use |
|-------|-----|
| `.fi` / `.fi-tech` | human field description / technical field listing |
| `code` | field name (concept) — bold solid chip in `.fi` |
| `.ev` | enum keyword — green mono chip |
| `.eg` | illustrative example — italic non-mono muted |
| `.dto` / `.card-tech` / `.at` | DTO name / cardinality / `@ reference` |
| `.expl` | prominent explanation prose (disambiguation, comparisons) |
| `.note` | callout box (`.note code` and `.chips` styled inside) |

Status tags (Exemple): `.tag-ok` / `.tag-non` green, `.tag-besoin` / `.tag-moyen`
yellow, `.tag-oui` / `.tag-fort` red, `.tag-faible` teal, `.tag-prio` purple,
`.tag-encours` blue, `.tag-nonex` gray. **Valence-free yes/no:** `.tag-actif`
(blue "applies") / `.tag-inactif` (gray "doesn't") — use these for factual flags
where red/green would wrongly imply good/bad.

---

## script.js behaviours

- `setTab(id)` — switch tabs; updates `#id` hash.
- `setVersion(ver)` — flip the v1/v2 toggle (no-op on pages without it).
- Example sync — hover highlight + click-to-scroll across `[data-section]`.
- Hash routing — `page.html#coverage` opens that tab on load.

Dependency-free vanilla JS; shared by every page.

---

## Generated tabs — do not hand-author

`../scripts/gen-famille.py` injects the **Famille** tab (always last) on every
page: it situates the API in its catalogue family with links to siblings, reusing
`catalogue-data.js` for grouping/titles/versions. `gen-referentiels-stats.py`
maintains the shared Référentiels tab across the four statistics pages.

Both are **idempotent** — re-run any time. Order matters: they read
`catalogue-data.js`, so regenerate it first:

```
bun run build-catalogue.ts          # schemas → catalogue-data.js
python3 scripts/gen-referentiels-stats.py
python3 scripts/gen-famille.py
```

(`build-catalogue.ts` is TypeScript/Bun; the generators are Python — historical
drift, may be unified later. The deployed site is fully static: `make deploy` just
syncs the files.)

---

## Generating a new page — checklist

1. Read `schemas/{slug}.json`: title, version, base, paths, schemas, which are
   read/write/referential.
2. **Modèle** — map the main response to nested cards; colour by role; write human
   `.fi` text; list fields in `.fi-tech` with `code` / `.ev` / `.eg` correctly.
3. **Référentiels** — one section per enum family (skip if none); always an intro.
4. **Disambiguation** — only if the API is confusable with a sibling.
5. **Couverture** — endpoints by domain + schema chips.
6. **Exemple** — a realistic persona; synced JSON ↔ narrative; mark invented data.
7. Add a `DOC_CONCEPTS[slug]` entry in `build-catalogue.ts` (card concept chips),
   plus group/title overrides if needed; `bun run build-catalogue.ts`.
8. Run the generators (above) to add the Famille tab.

Adapt depth to the API: a 1-endpoint API needs far less than diagnostic-usager.

---

## Fonts & responsive

Instrument Serif (h1, self-hosted), Source Sans 3 (body), IBM Plex Mono
(technical). No fixed widths; `.grid-2` and `.example-split` stack below 840px.
