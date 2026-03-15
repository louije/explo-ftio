# France Travail API Documentation — Template Reference

Single-page HTML documentation format for France Travail OpenAPI schemas.
Each API gets one HTML file that references the shared `style.css` and `script.js`.

## File structure

```
docs/
  style.css          ← shared stylesheet (all pages)
  script.js          ← shared behaviour (all pages)
  diagnostic-usager.html  ← reference implementation
  {api-slug}.html    ← one file per API
  TEMPLATE.md        ← this file
```

When generating new pages, create `{api-slug}.html` in this folder.
They all share the same `style.css` and `script.js`.

---

## Page skeleton

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{API Title} — Schéma complet</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Instrument+Serif&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">

<header>
  <h1>{Human-readable API name}</h1>
  <div class="sub">{One-line human explanation of what this API does}</div>
  <div class="sub-tech">{Technical name} v{version} — {N} endpoints · {M} schemas</div>
  <div class="endpoint-tag"><strong>Base</strong> {base URL without https://}</div>
</header>

<div class="controls">
  <div class="tab-group">
    <button class="tb active" onclick="setTab('nested')">Modèle</button>
    <button class="tb" onclick="setTab('coverage')">Couverture API</button>
    <button class="tb" onclick="setTab('example')">Exemple</button>
  </div>
</div>

<!-- TAB 1 -->
<div class="view active" id="v-nested"> ... </div>

<!-- TAB 2 -->
<div class="view" id="v-coverage"> ... </div>

<!-- TAB 3 -->
<div class="view" id="v-example"> ... </div>

<footer>
  OpenAPI {spec version} — {API name} v{version} · {base host} · {N} endpoints · {M} schemas
</footer>

</div>
<script src="script.js"></script>
</body>
</html>
```

---

## Tab 1 — Modèle (nested data model)

Shows the response schema as nested, coloured cards.
Each card represents a schema object or array. Cards nest inside each other
to mirror the JSON structure.

### Node anatomy

```html
<div class="n {level-color} [stack]" [id="m-{slug}"]>
  <div class="nh">
    <div class="dot"></div>
    <div class="name">
      {Human name}
      <span class="dto">{jsonField} · {DtoName}</span>   <!-- or just field name -->
    </div>
    <div class="card">
      {Cardinality label}
      <span class="card-tech">{type} · {notation}</span>
    </div>
  </div>
  <div class="nb">
    <div class="fi">
      {Human-readable explanation of what this data means}
      <span class="at">{shared component tag, e.g. "Conseiller tracé"}</span>
      <div class="fi-tech">
        <code>{field1}</code> · <code>{field2}</code> ·
        <span class="ev">{ENUM_VAL_1|ENUM_VAL_2}</span> ·
        <span class="at">@ {ReferencedDto}</span>
      </div>
    </div>
    <!-- nested children go here -->
  </div>
</div>
```

### Cardinality patterns

| Human label      | Tech label        | CSS            | Meaning                |
|------------------|-------------------|----------------|------------------------|
| Unique           | object · 1:1      | (no `.stack`)  | Exactly one object     |
| Exactement 1     | object · 1:1      | (no `.stack`)  | Same, emphasis         |
| Facultatif       | object · 0:1      | (no `.stack`)  | Optional, may be null  |
| 1 ou plusieurs   | array · 1:N       | `.stack`       | Array, at least one    |
| 0 ou plusieurs   | array · 0:N       | `.stack`       | Array, may be empty    |
| 1 ou plus        | array · 1:N       | `.stack`       | Short form (leaf nodes)|

The `.stack` class adds a box-shadow that looks like stacked cards behind
the main card. It uses `--lc` and `--lbg` from the level color class.

### Level color classes

Assign colours based on semantic role, not depth. Available palette:

| Class  | Colour     | Hex     | Typical use                         |
|--------|------------|---------|-------------------------------------|
| `.l0`  | Black      | #1a1a1a | Root response object                |
| `.l1-b`| Orange     | #d97706 | Primary domain (warm / aspirational)|
| `.l1-c`| Red        | #dc2626 | Primary domain (constraints/risk)   |
| `.l1-p`| Purple     | #7c3aed | Primary domain (agency/confidence)  |
| `.l1-n`| Teal       | #0d9488 | Primary domain (digital/skills)     |
| `.l2d` | Deep pink  | #e879a0 | Sub-entity (target/goal)            |
| `.l2t` | Green      | #22c55e | Sub-entity (thematic grouping)      |
| `.l2c` | Amber      | #f59e0b | Sub-entity (constraint list)        |
| `.l3`  | Gray       | #e0ddd6 | Leaf / neutral detail               |
| `.l3b` | Bright green| #86efac| Leaf / strength/positive            |
| `.l3s` | Soft purple| #c4b5fd | Leaf / situation/constat            |
| `.l3o` | Yellow     | #fcd34d | Leaf / objective/action             |

**Choosing colours for a new API:** Use `.l0` for root. Pick distinct `l1-*`
colours for top-level domain sections. Use `l2*` / `l3*` for nesting below.
You don't have to use all classes — pick what makes semantic sense. You can
also add new level classes following the same pattern:

```css
.l1-x{--lc:#HEX;--lbg:#HEX;border-color:var(--lc);background:var(--lbg);}
.l1-x>.nh{background:#HEX;}
.l1-x>.nh .dot{background:#HEX;}
.l1-x>.nh .card{background:rgba(R,G,B,.1);color:#HEX;}
```

### Inline elements

| Class       | Purpose                                           |
|-------------|---------------------------------------------------|
| `.fi`       | Human-readable field description paragraph        |
| `.fi-tech`  | Technical field listing (monospace, dimmer)        |
| `.ev`       | Inline enum value badge — `ENUM_A\|ENUM_B`        |
| `.at`       | Attribute/component tag — `Conseiller tracé`       |
| `code`      | Individual field name in tech listing              |
| `.dto`      | DTO name shown in header after human name          |
| `.card-tech`| Technical cardinality shown after human label      |

### Layout helpers

- `.grid-2` — Two-column grid (stacks on mobile < 840px)
- `.note` — Footnote/legend box below the model

---

## Tab 2 — Couverture API (endpoint + schema inventory)

### Domain + endpoint block

```html
<div class="domain">
  <div class="domain-title">
    {Technical domain name}
    <span class="dt-human">— {Human explanation}</span>
  </div>
  <div style="background:#fff;border:1px solid var(--border);border-radius:8px;overflow:hidden;">
    <div class="ep-row">
      <span class="ep-method m-{get|post|put|delete|patch}">{METHOD}</span>
      <div>
        <span class="ep-desc">{Technical summary}</span>
        <div class="ep-human">{Human one-liner}</div>
        <span class="ep-path">{/path/with/{params}}</span>
      </div>
    </div>
    <!-- more ep-rows -->
  </div>
</div>
```

HTTP method classes: `.m-get` (green), `.m-post` (blue), `.m-put` (amber),
`.m-delete` (red), `.m-patch` (purple).

### Schema chip grid

```html
<div class="schema-grid">
  <div class="schema-chip">
    <span class="sc-dot sc-{read|write|hist|ref|misc}"></span>
    <span class="sc-name">{DtoName}</span>
    <span class="sc-desc">— {short description}</span>
  </div>
</div>
```

Schema categories and dot colours:

| Class      | Colour | Meaning                    |
|------------|--------|----------------------------|
| `.sc-read` | Green  | Read / consultation        |
| `.sc-write`| Blue   | Write / save               |
| `.sc-hist` | Purple | Historisation / audit trail |
| `.sc-ref`  | Amber  | Referential / lookup data  |
| `.sc-misc` | Gray   | Other / utility            |

Add a `.sc-legend` block above the grid to explain the dots.

---

## Tab 3 — Exemple (side-by-side JSON + narrative)

### Layout

```html
<div class="story">
  <strong>{Context heading}</strong> — {Narrative introducing the example data}
</div>

<div class="example-split">
  <div class="panel panel-json" id="panel-json">
    <div class="json-tree">
      <div data-section="s-{name}">{...json...}</div>
      <div data-section="s-{name}">{...json...}</div>
    </div>
  </div>

  <div class="panel panel-human" id="panel-human">
    <div data-section="s-{name}">
      <!-- human cards here -->
    </div>
    <div data-section="s-{name}">
      <!-- human cards here -->
    </div>
  </div>
</div>
```

### JSON syntax highlighting

JSON is hand-authored HTML (not auto-generated) using `<span>` classes
inside a `<div class="json-tree">` with `white-space: pre`:

| Class    | Colour  | Token type  |
|----------|---------|-------------|
| `.jk`    | Purple  | Key name    |
| `.js`    | Green   | String value|
| `.jn`    | Orange  | Number      |
| `.jb`    | Red     | Boolean     |
| `.jnull` | Gray    | null        |
| `.jc`    | Gray    | Comment     |

Example:
```html
<span class="jk">"fieldName"</span>: <span class="js">"value"</span>,
```

### data-section synchronisation

Both the JSON panel and the human panel are divided into `<div>` blocks
with matching `data-section="s-{name}"` attributes. The `s-` prefix is
conventional (for "section").

These enable two behaviours (provided by `script.js`):

1. **Hover highlight** — hovering either side highlights both panels
2. **Click-to-scroll** — clicking one side smooth-scrolls to the matching
   block on the other side, with a flash animation

Choose section boundaries at logical JSON array items or object groups.
Each `data-section` value must appear exactly once in each panel.

### Human narrative cards

```html
<div class="ex-title">
  <span class="ex-ico">{emoji}</span> {Section title}
</div>
<div class="ex-card">
  <h4>{Item title}</h4>
  <p>{Description} <span class="ex-tag tag-{type}">{Label}</span></p>
  <div class="ex-sub">
    <div class="ex-item">
      <strong>{Sub-item}</strong> → <span class="ex-tag tag-{type}">{Status}</span>
    </div>
  </div>
  <div class="ex-agent">{Attribution line}</div>
</div>
```

### Status tag classes

| Class         | Background | Use for                        |
|---------------|------------|--------------------------------|
| `.tag-ok`     | Green      | Positive / point fort          |
| `.tag-non`    | Green      | "Non" (no constraint)          |
| `.tag-besoin` | Yellow     | Need identified                |
| `.tag-moyen`  | Yellow     | Medium impact                  |
| `.tag-nonex`  | Gray       | Not yet explored               |
| `.tag-encours`| Blue       | In progress                    |
| `.tag-oui`    | Red        | "Oui" (constraint present)     |
| `.tag-fort`   | Red        | High impact                    |
| `.tag-faible` | Teal       | Low impact                     |
| `.tag-prio`   | Purple     | Priority                       |

---

## script.js — Behaviours

The script is dependency-free vanilla JS. It provides:

### `setTab(id, updateHash)`
Switches tabs. `id` is one of `'nested'`, `'coverage'`, `'example'`.
Updates `location.hash` via `replaceState` unless `updateHash === false`.

### Hover highlight
Delegated `mouseover`/`mouseout` on `[data-section]` elements.
Adds/removes `.highlight` class on all elements sharing the same
`data-section` value.

### Click-to-scroll
Delegated `click` on `.example-split [data-section]`. Finds the matching
`[data-section]` in the opposite panel (`.panel-json` ↔ `.panel-human`),
calls `scrollIntoView({ behavior: 'smooth', block: 'center' })`, then
triggers a 1.5s flash animation (`.flash` class).

### Hash routing
On `DOMContentLoaded` and `hashchange`, reads `location.hash` and calls
`setTab()` if it matches a tab id. This allows direct linking:
`page.html#coverage`, `page.html#example`.

---

## Generating a new page from an OpenAPI schema

### What you need

1. The OpenAPI JSON file (from `schemas/{api-slug}.json`)
2. Understanding of what the API does (from the schema description and
   endpoint summaries)

### Step-by-step

1. **Read the schema.** Identify:
   - API title, version, base URL (from `info` and `servers`)
   - All paths and their methods/summaries (from `paths`)
   - All schemas and their nesting relationships (from `components.schemas`)
   - Which schemas are responses (read), request bodies (write),
     referential, or historical

2. **Design Tab 1.** Map the main response schema into nested cards:
   - Start with the root response DTO as `.l0`
   - Identify top-level sections and assign `l1-*` colours by semantic role
   - Nest children, choosing `l2*`/`l3*` colours
   - Add `.stack` for any array property
   - Write human names (French, with accents) for each node
   - Write `.fi` descriptions explaining what the data means
   - Write `.fi-tech` blocks listing field names and enum values

3. **Build Tab 2.** List every endpoint grouped by domain:
   - Group endpoints by shared path prefix or logical domain
   - For each endpoint: method badge, tech summary, human one-liner, path
   - List all schemas as chips, categorised by read/write/hist/ref/misc

4. **Create Tab 3.** Build a realistic example:
   - Invent a realistic persona and scenario (French context)
   - Write a mock JSON response using the schema structure
   - Divide into `data-section` blocks at logical boundaries
   - Write matching human narrative cards for each section
   - Ensure section names match between panels

5. **Write the HTML** using the skeleton above. Reference the shared
   `style.css` and `script.js`.

### For simple APIs

Not all APIs need three full tabs. If the API has:
- **1-3 endpoints and few schemas** — Tab 2 may be a simple list
- **No nested response structure** — Tab 1 can be a flat set of cards
- **Trivial responses** — Tab 3 example can be brief

Adapt the depth and detail to what's useful, not to fill space.

---

## Fonts

Three fonts used:

| Font              | Use                              | Source                |
|-------------------|----------------------------------|-----------------------|
| Instrument Serif  | Page title (`h1`)                | Self-hosted (`fonts/`)|
| Source Sans 3     | Body text, human descriptions    | Google Fonts          |
| IBM Plex Mono     | Technical: DTOs, field names, paths, JSON | Google Fonts |

Instrument Serif is loaded via `@font-face` in `style.css` from `../fonts/*.woff2`.

---

## Responsive behaviour

- `.grid-2` stacks to single column below 840px
- `.example-split` stacks to single column below 840px
- Body has `padding: 32px 16px` (works on mobile)
- No fixed widths anywhere
