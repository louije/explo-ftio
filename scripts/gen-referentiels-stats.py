#!/usr/bin/env python3
"""Generate & inject the "Référentiels" tab into every stats doc page.

The four France Travail statistics APIs share the Smart Emploi referential
(maille territoriale) but each exposes its own indicators, activity types and
nomenclatures. This builds a deep Référentiels tab per page: shared territory
mailles + per-API crossing dimensions + an "Indicateurs & requêtes possibles"
matrix (required/optional criteria per indicator).

Single source of truth = SHARED_MAILLES + PER_API below. Idempotent. To add a
FUTURE stats page, add an entry to PER_API and run:  python3 gen-referentiels-stats.py
"""
import re, os

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/docs/"

# Shared across all four APIs (Smart Emploi territory referential).
SHARED_MAILLES = [
    ("NAT", "National"),
    ("REG", "Région"),
    ("DEP", "Département"),
    ("BASSIN", "Bassin d'emploi France Travail"),
    ("EPCI", "Intercommunalité"),
    ("CLPE", "Comité local pour l'emploi"),
]

PER_API = {
    "informations-territoire": {
        "page": "informations-territoire.html",
        "activites": [("ROME", "Métier (code ROME)"), ("NAF88", "Secteur d'activité (NAF 88)"),
                      ("CUMUL", "Agrégation — cumul toutes activités"), ("MOYENNE", "Agrégation — moyenne toutes activités")],
        "periodes": [("ANNEE", "Donnée annuelle"), ("TRIMESTRE", "Donnée trimestrielle")],
        "nomenclatures": [],
        "indicators": [
            ("POP_1", "Population totale", "stat-population", "territoire", "périodes, caractéristiques", "Seul indicateur sans activité obligatoire."),
            ("POP_2", "Population active", "stat-population-active", "territoire, activité", "périodes, caractéristiques", ""),
            ("ETAB_1", "Établissements", "stat-etablissements", "territoire, activité", "périodes, caractéristiques", ""),
            ("SAL_1", "Salariés", "stat-salaries", "territoire, activité", "périodes", "Pas de ventilation par caractéristique."),
            ("DYN_1", "Dynamique de l'emploi", "stat-dynamique-emploi", "territoire, activité", "périodes", "Indicateur prospectif propre à France Travail."),
        ],
    },
    "marche-travail": {
        "page": "marche-travail.html",
        "activites": [("ROME", "Métier (code ROME)"), ("NAF", "Secteur (NAF)"), ("COMP", "Compétence")],
        "periodes": [("TRIMESTRE", "Donnée trimestrielle"), ("ANNEE", "Donnée annuelle")],
        "nomenclatures": [("CATCAND", "Catégorie de candidat (A, B, C…)"), ("ORIGINEOFF", "Origine de l'offre"),
                          ("TYPE_TENSION", "Type de tension"), ("DUREEEMP", "Durée d'emploi"), ("CATCANDxDUREEEMP", "Catégorie × durée d'emploi")],
        "indicators": [
            ("DE_1", "Demandeurs inscrits", "stat-demandeurs", "territoire, activité", "catégorie de candidat, périodes, caractéristiques", ""),
            ("DE_5", "Nouveaux inscrits", "stat-demandeurs-entrant", "territoire, activité", "périodes, caractéristiques", "Entrées du trimestre et sur 12 mois."),
            ("OFF_1", "Offres enregistrées", "stat-offres", "territoire, activité", "origine de l'offre, périodes", ""),
            ("EMB_1", "Embauches", "stat-embauches", "territoire, activité", "catégorie de candidat, périodes", ""),
            ("PERSP_2", "Tensions de recrutement", "stat-perspective-employeur", "territoire, activité", "périodes", "Difficultés de recrutement par métier."),
            ("DYN_1", "Dynamique de l'emploi", "stat-dynamique-emploi", "territoire, activité", "périodes", "Indicateur prospectif."),
            ("SAL_3", "Salaires en poste", "salaire-rome-fap (GET)", "territoire, ROME", "—", "Endpoint GET par chemin, pas un POST de critères."),
        ],
    },
    "acces-emploi-demandeurs-emploi": {
        "page": "acces-emploi-demandeurs-emploi.html",
        "activites": [("ROME", "Métier recherché (code ROME)")],
        "periodes": [("TRIMESTRE", "Donnée trimestrielle")],
        "nomenclatures": [("DUREEEMP", "Durée d'emploi / délai d'accès")],
        "indicators": [
            ("ACC_1", "Accès à l'emploi à 6 mois", "stat-acces-emploi", "territoire, activité", "délai d'accès, périodes, caractéristiques", "Demandeurs catégories A et B, par métier recherché."),
        ],
    },
    "sortants-formation-acces-emploi": {
        "page": "sortants-formation-acces-emploi.html",
        "activites": [("ROME", "Métier recherché (code ROME)"), ("FORM14", "Domaine de formation (nomenclature FORM14)")],
        "periodes": [("TRIMESTRE", "Donnée trimestrielle")],
        "nomenclatures": [("ACCESEMP", "Accès à l'emploi")],
        "indicators": [
            ("ACC_2", "Accès à l'emploi à 6 mois (sortants de formation)", "stat-acces-emploi-sorties-formation", "territoire, activité", "délai d'accès, périodes, caractéristiques", ""),
            ("DE_3", "Demandeurs sortants de formation", "stat-demandeurs-sorties-formation", "territoire, activité", "périodes, caractéristiques", "Par type de formation et métier recherché."),
        ],
    },
}

PAGES = list(PER_API)

def voc_card(title, items, tech):
    lis = "\n".join('        <li><span class="voc-code">%s</span> %s</li>' % (c, l) for c, l in items)
    return ('    <div class="ref-card voc-card">\n'
            '      <div class="ref-head"><span class="ref-title">%s</span><span class="ref-count">%d</span></div>\n'
            '      <ul class="ref-list voc-list">\n%s\n      </ul>\n'
            '      <div class="voc-tech">%s</div>\n'
            '    </div>') % (title, len(items), lis, tech)

def indicator_card(code, label, ep, oblig, fac, note):
    body = ('<code>%s</code> — <strong>Obligatoire :</strong> %s. <strong>Facultatif :</strong> %s.' % (ep, oblig, fac))
    if note:
        body += ' <em>%s</em>' % note
    return ('    <div class="ref-card voc-card" style="grid-column:1/-1;">\n'
            '      <div class="ref-head"><span class="ref-title">%s</span><span class="ref-count"><span class="ev">%s</span></span></div>\n'
            '      <div class="expl">%s</div>\n'
            '    </div>') % (label, code, body)

def render(slug):
    a = PER_API[slug]
    maille = voc_card("Niveaux disponibles", SHARED_MAILLES,
                      "Codes attestés : <code>NAT</code>, <code>REG</code>, <code>DEP</code>. Les libellés des mailles fines sont confirmés ; leurs codes exacts et leur disponibilité par indicateur sont servis par <code>GET /referentiel/type-territoires</code> et <code>details-indicateurs</code>.")
    dim_cards = [
        voc_card("Type d'activité", a["activites"], "<code>codeTypeActivite</code> — liste complète et combinaisons valides via <code>details-indicateurs</code>."),
        voc_card("Type de période", a["periodes"], "<code>codeTypePeriode</code> — <code>dernierePeriode=true</code> pour la plus récente, sinon <code>listeCodePeriode</code>."),
    ]
    if a["nomenclatures"]:
        dim_cards.append(voc_card("Nomenclatures", a["nomenclatures"], "<code>codeTypeNomenclature</code> — axes de découpage propres à certains indicateurs."))
    indicators = "\n\n".join(indicator_card(*ind) for ind in a["indicators"])

    button = "    <button class=\"tb\" onclick=\"setTab('ref')\">Référentiels</button>"
    view = '''<!-- RÉFÉRENTIELS (généré par gen-referentiels-stats.py) -->
<div class="view" id="v-ref">

<div class="note" style="margin-bottom:20px;">
  Toutes les dimensions de requête viennent du <strong>Référentiel Smart Emploi</strong>, consultable via les endpoints <code>GET /referentiel/*</code>. Les valeurs ci-dessous sont les principales ; la liste <em>complète et à jour</em>, ainsi que les combinaisons réellement autorisées <strong>pour chaque indicateur</strong>, sont données par <code>GET /referentiel/details-indicateurs</code> (le catalogue des indicateurs).
</div>

<div class="ref-section">
  <h2 class="ref-section-title">
    <span class="rs-dot" style="background:#0d9488;"></span>
    Maille territoriale
    <span class="rs-count">6 niveaux</span>
    <span class="rs-tech"><code>codeTypeTerritoire</code> · référentiel <code>type-territoires</code></span>
  </h2>
  <div class="ref-section-intro">
    Le niveau géographique de l'analyse, du plus large au plus fin. Les mailles fines (bassin, EPCI, CLPE) sont au cœur du pilotage territorial de la loi pour le plein emploi.
  </div>
  <div class="ref-families">
%s
  </div>
</div>

<div class="ref-section">
  <h2 class="ref-section-title">
    <span class="rs-dot" style="background:#d97706;"></span>
    Dimensions de croisement
    <span class="rs-count">%d</span>
    <span class="rs-tech"><code>codeTypeActivite</code> · <code>codeTypePeriode</code>%s</span>
  </h2>
  <div class="ref-section-intro">
    Les axes que l'on croise avec le territoire : <strong>sur quoi</strong> porte la statistique (activité), à <strong>quel pas de temps</strong> (période)%s.
  </div>
  <div class="ref-families">
%s
  </div>
</div>

<div class="ref-section">
  <h2 class="ref-section-title">
    <span class="rs-dot" style="background:#7c3aed;"></span>
    Indicateurs &amp; requêtes possibles
    <span class="rs-count">%d</span>
    <span class="rs-tech">un appel par indicateur</span>
  </h2>
  <div class="ref-section-intro">
    Chaque indicateur accepte un jeu de critères précis. <strong>Territoire</strong> est toujours obligatoire ; les autres critères varient — le catalogue <code>details-indicateurs</code> fait foi.
  </div>
  <div class="ref-families">

%s

  </div>
</div>

</div>''' % (
        maille,
        len(dim_cards),
        " · <code>codeTypeNomenclature</code>" if a["nomenclatures"] else "",
        ", et selon quels découpages (nomenclatures)" if a["nomenclatures"] else "",
        "\n".join(dim_cards),
        len(a["indicators"]),
        indicators,
    )
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

def inject(slug):
    path = D + PER_API[slug]["page"]
    raw = open(path, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    s = raw.decode("utf-8")
    button, view = render(slug)
    button = button.replace("\n", nl); view = view.replace("\n", nl)

    # remove existing Référentiels button + view (idempotent)
    s = re.sub(r"[ \t]*<button class=\"tb\" onclick=\"setTab\('ref'\)\">.*?</button>\r?\n", "", s)
    span = view_span(s, "ref")
    if span:
        pre, post = s[:span[0]], s[span[1]:]
        pre = re.sub(r"(\s*<!--[^\n]*-->)+\s*$", "", pre)
        s = pre + nl + post

    # insert button right after the Modèle tab (stable position, independent of Famille)
    m = re.search(r"<button class=\"tb active\" onclick=\"setTab\('nested'\)\">.*?</button>", s)
    assert m, "Modèle button not found in " + path
    s = s[:m.end()] + nl + button + s[m.end():]

    # insert the Référentiels view right after the Modèle (v-nested) view
    ns = view_span(s, "nested")
    assert ns, "v-nested not found in " + path
    s = s[:ns[1]] + nl + nl + view + s[ns[1]:]

    s = re.sub(r"(\r?\n){3,}", nl + nl, s)  # collapse accumulated blank lines (idempotency)
    open(path, "wb").write(s.encode("utf-8"))
    return path

if __name__ == "__main__":
    for slug in PAGES:
        print("injected:", inject(slug))
