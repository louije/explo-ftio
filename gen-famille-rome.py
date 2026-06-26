#!/usr/bin/env python3
"""Generate & inject the "Famille ROME" tab into every ROME documentation page.

The ROME 4.0 referential is split across several distinct APIs. Each ROME doc
page carries a "Famille ROME" tab that situates it among its siblings: every
sibling gets a card with its role + a pairwise contrast against the current page,
and the current page's own card is highlighted.

Single source of truth = APIS + BOUNDARY below. Idempotent and re-runnable:
running it again rebuilds the tab from scratch. To add a FUTURE ROME page, add
it to APIS (+ its BOUNDARY pairs) and to PAGES, then run:  python3 gen-famille-rome.py
"""
import re

D = "/Users/louije/Development/gip/ftio/docs/"

# Display order + per-API role (one self-contained sentence).
APIS = [
    dict(slug="rome-4-0-metiers", title="ROME 4.0 — Métiers", page="rome-4-0-metiers.html", ep="17 endpoints",
         role="Le référentiel navigable : parcourir l'arbre des métiers, rechercher, filtrer par RIASEC / NAF / compétence, et lire les métadonnées d'un métier (ISCO/ESCO, transitions, mobilité)."),
    dict(slug="rome-4-0-fiches-metiers", title="Fiches ROME", page="rome-4-0-fiches-metiers.html", ep="3 endpoints",
         role="La fiche métier assemblée : pour un code ROME, les compétences groupées par enjeu et les savoirs groupés par catégorie."),
    dict(slug="rome-4-0-competences", title="ROME 4.0 — Compétences", page="rome-4-0-competences.html", ep="21 endpoints",
         role="Le référentiel des compétences : chaque compétence avec son type, sa correspondance ESCO, ses macro-compétences et savoirs."),
    dict(slug="rome-4-0-contextes-travail", title="ROME 4.0 — Situations de travail", page="rome-4-0-contextes-travail.html", ep="3 endpoints",
         role="Le référentiel des situations de travail : contextes et conditions d'exercice (horaires, environnement, statuts)."),
    dict(slug="romeo", title="Romeo", page="romeo.html", ep="prédiction · 4 endpoints",
         role="Le moteur de prédiction : à partir d'un texte libre, prédit le code métier ou compétence ROME le plus probable."),
]

# Pairwise boundary, neutral phrasing (reads correctly on either page).
BOUNDARY = {
    frozenset({"rome-4-0-metiers", "rome-4-0-fiches-metiers"}): "Métiers liste quels métiers existent et leurs compétences à plat ; Fiches ROME structure compétences et savoirs (par enjeu et catégorie) pour un métier connu.",
    frozenset({"rome-4-0-metiers", "rome-4-0-competences"}): "Métiers liste les compétences mobilisées par métier ; Compétences décrit chaque compétence en profondeur, indépendamment des métiers.",
    frozenset({"rome-4-0-metiers", "rome-4-0-contextes-travail"}): "Métiers expose les contextes de travail rattachés à un métier ; Situations de travail fournit le référentiel complet des contextes.",
    frozenset({"rome-4-0-metiers", "romeo"}): "Romeo prédit un code à partir de texte libre ; Métiers explore ensuite ce code dans le référentiel.",
    frozenset({"rome-4-0-fiches-metiers", "rome-4-0-competences"}): "Fiches ROME regroupe les compétences d'un métier par enjeu ; Compétences est le référentiel détaillé de chaque compétence.",
    frozenset({"rome-4-0-fiches-metiers", "rome-4-0-contextes-travail"}): "Fiches ROME décrit le contenu d'un métier (compétences, savoirs) ; Situations de travail en décrit les conditions d'exercice.",
    frozenset({"rome-4-0-fiches-metiers", "romeo"}): "Romeo trouve le code métier à partir de texte ; Fiches ROME en donne ensuite la fiche compétences-savoirs.",
    frozenset({"rome-4-0-competences", "rome-4-0-contextes-travail"}): "Compétences = ce que la personne sait faire ; Situations de travail = les conditions dans lesquelles elle l'exerce.",
    frozenset({"rome-4-0-competences", "romeo"}): "Romeo prédit un code compétence à partir de texte ; Compétences en donne le détail.",
    frozenset({"rome-4-0-contextes-travail", "romeo"}): "Romeo mappe du texte vers des codes ROME ; Situations de travail est le référentiel des contextes de travail.",
}

PAGES = [a["slug"] for a in APIS]  # every API that has a doc page

def card(cur, api):
    is_cur = api["slug"] == cur["slug"]
    style = ' style="grid-column:1/-1;border-color:#a7f3d0;background:#f0fdf4;"' if is_cur else ' style="grid-column:1/-1;"'
    count = ("cette page · " + api["ep"]) if is_cur else api["ep"]
    title = api["title"] if is_cur else '<a href="%s">%s</a>' % (api["page"], api["title"])
    body = api["role"]
    if not is_cur:
        b = BOUNDARY[frozenset({cur["slug"], api["slug"]})]
        body += '<br><strong>%s vs %s :</strong> %s' % (cur["title"], api["title"], b)
    return ('    <div class="ref-card voc-card"%s>\n'
            '      <div class="ref-head"><span class="ref-title">%s</span><span class="ref-count">%s</span></div>\n'
            '      <div class="expl">%s</div>\n'
            '    </div>') % (style, title, count, body)

def render(cur_slug):
    cur = next(a for a in APIS if a["slug"] == cur_slug)
    cards = "\n\n".join(card(cur, a) for a in APIS)
    button = "    <button class=\"tb\" onclick=\"setTab('famille')\">Famille ROME</button>"
    view = '''<!-- FAMILLE ROME (généré par gen-famille-rome.py) -->
<div class="view" id="v-famille">

<div class="note" style="margin-bottom:20px;">
  <strong>Le ROME 4.0 est éclaté en plusieurs API.</strong> Aucune n'est une version d'une autre : ce sont des <em>angles</em> différents sur le même référentiel. Savoir laquelle appeler évite de dupliquer des appels.
</div>

<div class="ref-section">
  <h2 class="ref-section-title">
    <span class="rs-dot" style="background:#0d9488;"></span>
    Cette API dans la famille ROME 4.0
    <span class="rs-count">5 API</span>
    <span class="rs-tech">classification ROME 4.0</span>
  </h2>
  <div class="ref-section-intro">
    Le fil conducteur : <strong>Métiers</strong> répond à « quels métiers existent et comment sont-ils reliés ? ». Les autres décrivent en détail un métier, une compétence ou un contexte déjà identifié.
  </div>
  <div class="ref-families">

%s

  </div>
</div>

<div class="note">
  <strong>Quelle API appeler ?</strong> Texte libre à mapper → <strong>Romeo</strong>. Naviguer / rechercher / filtrer des métiers → <strong>Métiers</strong>. Afficher la fiche compétences-savoirs d'un métier → <strong>Fiches ROME</strong>. Détailler une compétence → <strong>Compétences</strong>. Décrire un contexte de travail → <strong>Situations de travail</strong>.
</div>

</div>''' % cards
    return button, view

def view_span(s, vid):
    m = re.search(r'<div class="view[^"]*" id="v-%s">' % re.escape(vid), s)
    if not m:
        return None
    after = m.end(); depth = 1
    for tok in re.finditer(r'<div\b|</div>', s[after:]):
        if tok.group() == '<div':
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return (m.start(), after + tok.end())
    raise AssertionError("unbalanced view: " + vid)

def inject(cur_slug):
    path = D + next(a["page"] for a in APIS if a["slug"] == cur_slug)
    raw = open(path, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    s = raw.decode("utf-8")
    button, view = render(cur_slug)
    button = button.replace("\n", nl); view = view.replace("\n", nl)

    # 1) remove any existing famille button + view (idempotent)
    s = re.sub(r"[ \t]*<button class=\"tb\" onclick=\"setTab\('famille'\)\">.*?</button>\r?\n", "", s)
    span = view_span(s, "famille")
    if span:
        pre, post = s[:span[0]], s[span[1]:]
        pre = re.sub(r"(\s*<!--[^\n]*-->)+\s*$", "", pre)  # strip the view's leading comment(s)
        s = pre + nl + post

    # 2) insert button right after the Modèle tab button
    m = re.search(r"<button class=\"tb active\" onclick=\"setTab\('nested'\)\">.*?</button>", s)
    assert m, "Modèle tab button not found in " + path
    s = s[:m.end()] + nl + button + s[m.end():]

    # 3) insert the famille view right after the Modèle (v-nested) view
    ns = view_span(s, "nested")
    assert ns, "v-nested not found in " + path
    s = s[:ns[1]] + nl + nl + view + s[ns[1]:]

    open(path, "wb").write(s.encode("utf-8"))
    return path

if __name__ == "__main__":
    for slug in PAGES:
        print("injected:", inject(slug))
