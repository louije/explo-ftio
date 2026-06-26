#!/usr/bin/env python3
"""Inject a "Famille" tab (always the LAST tab) into every API doc page.

The tab situates the API within its catalogue family (the 9 groups) and links to
its siblings — navigation help on every page. For the families whose APIs are
*alternatives* (ROME, Statistiques) it keeps the pairwise "X vs Y" contrasts; for
the *sequential* Parcours d'accompagnement it shows the journey order; for the
rest it lists the siblings with a one-line role.

Source of truth: catalogue-data.js (grouping, titles, versions, stars) + the
ROLES / BOUNDARY / ORDER tables below. Idempotent / re-runnable:
    python3 gen-famille.py
"""
import json, re, html
from collections import defaultdict

ROOT = "/Users/louije/Development/gip/ftio/"
D = ROOT + "docs/"

cat = open(ROOT + "catalogue-data.js", encoding="utf-8").read()
CATA = json.loads(cat.split("const CATALOGUE = ", 1)[1].rstrip().rstrip(";"))
APIS = {a["slug"]: a for a in CATA["apis"]}
GROUPS = {g["id"]: g for g in CATA["groups"]}
MEMBERS = defaultdict(list)
for a in CATA["apis"]:
    MEMBERS[a["group"]].append(a["slug"])

# One-line role for members of "rich" families (others derive it from the catalogue description).
ROLES = {
    # ROME
    "rome-4-0-metiers": "Le référentiel navigable : parcourir l'arbre des métiers, rechercher, filtrer par RIASEC / NAF / compétence, et lire les métadonnées d'un métier (ISCO/ESCO, transitions, mobilité).",
    "rome-4-0-fiches-metiers": "La fiche métier assemblée : pour un code ROME, les compétences groupées par enjeu et les savoirs groupés par catégorie.",
    "rome-4-0-competences": "Le référentiel des compétences : chaque compétence avec son type, sa correspondance ESCO, ses macro-compétences et savoirs.",
    "rome-4-0-contextes-travail": "Le référentiel des situations de travail : contextes et conditions d'exercice (horaires, environnement, statuts).",
    "romeo": "Le moteur de prédiction : à partir d'un texte libre, prédit le code métier ou compétence ROME le plus probable.",
    # Statistiques
    "informations-territoire": "Comprendre un territoire : population, population active, établissements, salariés et dynamisme de l'emploi. L'angle « contexte socio-économique ».",
    "marche-travail": "Demandeurs, offres, embauches, tensions de recrutement et salaires, par métier et territoire. L'angle « marché de l'emploi ».",
    "acces-emploi-demandeurs-emploi": "Le taux et les conditions d'accès (ou de retour) à l'emploi des demandeurs d'emploi. L'angle « devenir des demandeurs ».",
    "sortants-formation-acces-emploi": "L'accès à l'emploi des personnes à l'issue d'une formation. L'angle « efficacité des formations ».",
    # Parcours d'accompagnement (séquence)
    "orientation-usager": "Oriente l'usager vers un parcours (social, socio-professionnel, professionnel) et un organisme référent — le point de départ.",
    "contrat-engagement": "Formalise les engagements réciproques usager / organisme : lire, signer ou refuser le contrat d'engagement.",
    "rendez-vous-partenaires": "Crée et gère les rendez-vous de l'usager — la cadence des rencontres de l'accompagnement.",
    "declaration-demarche": "Déclare et suit les démarches concrètes de retour à l'emploi (pourquoi / quoi / comment).",
    "gestion-sanctions-rsa": "Gère les manquements et conséquences de sanction en cas de non-respect des engagements (RSA).",
}

SHORT = {
    "rome-4-0-metiers": "Métiers", "rome-4-0-fiches-metiers": "Fiches ROME",
    "rome-4-0-competences": "Compétences", "rome-4-0-contextes-travail": "Situations de travail", "romeo": "Romeo",
    "informations-territoire": "Informations territoire", "marche-travail": "Marché du travail",
    "acces-emploi-demandeurs-emploi": "Accès demandeurs", "sortants-formation-acces-emploi": "Sortants de formation",
}

# Pairwise contrasts, only for families whose APIs are alternatives.
BOUNDARY = {
    "rome": {
        frozenset({"rome-4-0-metiers","rome-4-0-fiches-metiers"}): "Métiers liste quels métiers existent et leurs compétences à plat ; Fiches ROME structure compétences et savoirs (par enjeu et catégorie) pour un métier connu.",
        frozenset({"rome-4-0-metiers","rome-4-0-competences"}): "Métiers liste les compétences mobilisées par métier ; Compétences décrit chaque compétence en profondeur.",
        frozenset({"rome-4-0-metiers","rome-4-0-contextes-travail"}): "Métiers expose les contextes de travail d'un métier ; Situations de travail fournit le référentiel complet des contextes.",
        frozenset({"rome-4-0-metiers","romeo"}): "Romeo prédit un code à partir de texte libre ; Métiers explore ensuite ce code dans le référentiel.",
        frozenset({"rome-4-0-fiches-metiers","rome-4-0-competences"}): "Fiches ROME regroupe les compétences d'un métier par enjeu ; Compétences est le référentiel détaillé de chaque compétence.",
        frozenset({"rome-4-0-fiches-metiers","rome-4-0-contextes-travail"}): "Fiches ROME décrit le contenu d'un métier ; Situations de travail en décrit les conditions d'exercice.",
        frozenset({"rome-4-0-fiches-metiers","romeo"}): "Romeo trouve le code métier à partir de texte ; Fiches ROME en donne ensuite la fiche compétences-savoirs.",
        frozenset({"rome-4-0-competences","rome-4-0-contextes-travail"}): "Compétences = ce que la personne sait faire ; Situations de travail = les conditions dans lesquelles elle l'exerce.",
        frozenset({"rome-4-0-competences","romeo"}): "Romeo prédit un code compétence à partir de texte ; Compétences en donne le détail.",
        frozenset({"rome-4-0-contextes-travail","romeo"}): "Romeo mappe du texte vers des codes ROME ; Situations de travail est le référentiel des contextes de travail.",
    },
    "stats": {
        frozenset({"informations-territoire","marche-travail"}): "Informations territoire décrit le contexte (qui vit et travaille ici) ; Marché du travail décrit le marché de l'emploi (offres, demande, tensions).",
        frozenset({"informations-territoire","acces-emploi-demandeurs-emploi"}): "L'un photographie la population active du territoire ; l'autre suit le devenir des demandeurs d'emploi.",
        frozenset({"informations-territoire","sortants-formation-acces-emploi"}): "Même cadre statistique ; ici l'angle est le portrait du territoire, là l'efficacité des formations.",
        frozenset({"marche-travail","acces-emploi-demandeurs-emploi"}): "Marché du travail mesure l'offre et la demande à un instant ; Accès demandeurs suit le retour à l'emploi dans le temps.",
        frozenset({"marche-travail","sortants-formation-acces-emploi"}): "Marché du travail couvre tout le marché ; Sortants de formation cible le retour à l'emploi après une formation.",
        frozenset({"acces-emploi-demandeurs-emploi","sortants-formation-acces-emploi"}): "Accès demandeurs couvre tous les demandeurs ; Sortants de formation se restreint à ceux qui sortent d'une formation.",
    },
}

# Sequential families get a fixed journey order (others sort by title).
ORDER = {
    "parcours": ["orientation-usager","contrat-engagement","rendez-vous-partenaires","declaration-demarche","gestion-sanctions-rsa"],
}

INTRO = {
    "rome": "Toutes décrivent le référentiel ROME 4.0 sous un angle différent ; chaque carte précise ce qui la distingue.",
    "stats": "Toutes partagent le même moteur statistique (territoire × activité × période) ; chaque carte précise son angle.",
    "parcours": "Les étapes de l'accompagnement « loi pour le plein emploi », dans l'ordre du parcours.",
}
INTRO_DEFAULT = "Les autres API du même domaine — pour passer de l'une à l'autre."

def esc(t): return html.escape(t or "", quote=False)

def role_for(slug):
    if slug in ROLES:
        return ROLES[slug]
    d = (APIS[slug].get("description") or "").strip()
    if len(d) > 150:
        d = d[:150].rsplit(" ", 1)[0] + "…"
    return esc(d)

def ordered_members(gid):
    ms = list(MEMBERS[gid])
    if gid in ORDER:
        return [s for s in ORDER[gid] if s in ms] + [s for s in ms if s not in ORDER[gid]]
    return sorted(ms, key=lambda s: APIS[s]["title"].lower())

def card(gid, current, slug):
    a = APIS[slug]
    is_cur = slug == current
    style = ' style="grid-column:1/-1;border-color:#a7f3d0;background:#f0fdf4;"' if is_cur else ' style="grid-column:1/-1;"'
    star = ' ★' if a.get("starred") else ""
    if is_cur:
        title = esc(a["title"]) + star
        count = "cette page"
    else:
        title = '<a href="%s.html">%s</a>%s' % (slug, esc(a["title"]), star)
        count = "v" + esc(a["version"]) + ('  <span class="at">nouveau</span>' if a.get("isNew") else "")
    body = role_for(slug)
    if not is_cur and gid in BOUNDARY:
        b = BOUNDARY[gid].get(frozenset({current, slug}))
        if b:
            body += '<br><strong>%s vs %s :</strong> %s' % (SHORT.get(current, APIS[current]["title"]), SHORT.get(slug, a["title"]), b)
    return ('    <div class="ref-card voc-card"%s>\n'
            '      <div class="ref-head"><span class="ref-title">%s</span><span class="ref-count">%s</span></div>\n'
            '      <div class="expl">%s</div>\n'
            '    </div>') % (style, title, count, body)

def render(current):
    g = GROUPS[APIS[current]["group"]]
    gid = g["id"]
    members = ordered_members(gid)
    cards = "\n\n".join(card(gid, current, s) for s in members)
    intro_parts = [esc(g["description"])]
    if gid in INTRO:
        intro_parts.append(INTRO[gid])
    intro_html = " ".join(intro_parts) + ' <a href="../index.html">Voir toutes les familles</a> dans le catalogue.'
    view = '''<!-- FAMILLE (généré par gen-famille.py) -->
<div class="view" id="v-famille">

<div class="ref-section">
  <h2 class="ref-section-title">
    <span class="rs-dot" style="background:#0d9488;"></span>
    La famille %s
    <span class="rs-count">%d API</span>
    <span class="rs-tech">navigation</span>
  </h2>
  <div class="ref-section-intro">%s</div>
  <div class="ref-families">

%s

  </div>
</div>

</div>''' % (esc(g["label"]), len(members), intro_html, cards)
    button = "    <button class=\"tb\" onclick=\"setTab('famille')\">Famille</button>"
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

def inject(current):
    path = D + current + ".html"
    raw = open(path, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    s = raw.decode("utf-8")
    button, view = render(current)
    button = button.replace("\n", nl); view = view.replace("\n", nl)

    # remove any existing Famille button + view (idempotent)
    s = re.sub(r"[ \t]*<button class=\"tb\" onclick=\"setTab\('famille'\)\">.*?</button>\r?\n", "", s)
    sp = view_span(s, "famille")
    if sp:
        pre, post = s[:sp[0]], s[sp[1]:]
        pre = re.sub(r"(\s*<!--[^\n]*-->)+\s*$", "", pre)
        s = pre + nl + post

    # insert button as the LAST tab in the tab-group
    m = re.search(r'<div class="tab-group">', s)
    assert m, "tab-group not found in " + path
    close = s.index("</div>", m.end())
    line_start = s.rfind(nl, m.end(), close) + len(nl)
    s = s[:line_start] + button + nl + s[line_start:]

    # insert the view as the LAST view, just before <footer>
    f = s.index("<footer")
    fline = s.rfind(nl, 0, f) + len(nl)
    s = s[:fline] + view + nl + nl + s[fline:]

    open(path, "wb").write(s.encode("utf-8"))
    return path

if __name__ == "__main__":
    for slug in APIS:
        inject(slug)
    print("Famille tab injected into %d pages" % len(APIS))
