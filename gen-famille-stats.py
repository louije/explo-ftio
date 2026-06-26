#!/usr/bin/env python3
"""Generate & inject the "Famille Statistiques" tab into every stats doc page.

The four France Travail statistics APIs share the exact same query engine
(territoire × activité × période × caractéristique, POST indicateur, GET
référentiels). They differ only by which indicators they expose. Each stats doc
page carries a "Famille Statistiques" tab situating it among its siblings, with
a pairwise contrast and the current page highlighted.

Single source of truth = APIS + BOUNDARY. Idempotent / re-runnable. To add a
FUTURE stats page, add it to APIS (+ its BOUNDARY pairs) and run:
    python3 gen-famille-stats.py
"""
import re

D = "/Users/louije/Development/gip/ftio/docs/"

APIS = [
    dict(slug="informations-territoire", title="Informations sur un territoire", short="Informations territoire",
         page="informations-territoire.html", ep="5 indicateurs",
         role="<strong>Comprendre un territoire.</strong> Population (<span class=\"ev\">POP_1</span>), population active (<span class=\"ev\">POP_2</span>), établissements (<span class=\"ev\">ETAB_1</span>), salariés (<span class=\"ev\">SAL_1</span>) et l'indicateur prospectif de dynamisme de l'emploi (<span class=\"ev\">DYN_1</span>). L'angle « contexte socio-économique »."),
    dict(slug="marche-travail", title="Marché du travail", short="Marché du travail",
         page="marche-travail.html", ep="offre & demande",
         role="Demandeurs, offres, embauches, tensions de recrutement et salaires, par métier et territoire. L'angle « marché de l'emploi »."),
    dict(slug="acces-emploi-demandeurs-emploi", title="Accès à l'emploi des demandeurs", short="Accès demandeurs",
         page="acces-emploi-demandeurs-emploi.html", ep="parcours DE",
         role="Le taux et les conditions d'accès (ou de retour) à l'emploi des demandeurs d'emploi. L'angle « devenir des demandeurs »."),
    dict(slug="sortants-formation-acces-emploi", title="Sortants de formation & accès à l'emploi", short="Sortants de formation",
         page="sortants-formation-acces-emploi.html", ep="après formation",
         role="L'accès à l'emploi des personnes à l'issue d'une formation. L'angle « efficacité des formations »."),
]

BOUNDARY = {
    frozenset({"informations-territoire", "marche-travail"}): "Informations territoire décrit le contexte (qui vit et travaille ici) ; Marché du travail décrit le marché de l'emploi (offres, demande, tensions).",
    frozenset({"informations-territoire", "acces-emploi-demandeurs-emploi"}): "L'un photographie la population active du territoire ; l'autre suit le devenir des demandeurs d'emploi.",
    frozenset({"informations-territoire", "sortants-formation-acces-emploi"}): "Même cadre statistique ; ici l'angle est le portrait du territoire, là l'efficacité des formations sur le retour à l'emploi.",
    frozenset({"marche-travail", "acces-emploi-demandeurs-emploi"}): "Marché du travail mesure l'offre et la demande à un instant ; Accès demandeurs suit le retour à l'emploi des personnes dans le temps.",
    frozenset({"marche-travail", "sortants-formation-acces-emploi"}): "Marché du travail couvre tout le marché ; Sortants de formation cible le retour à l'emploi après une formation.",
    frozenset({"acces-emploi-demandeurs-emploi", "sortants-formation-acces-emploi"}): "Accès demandeurs couvre tous les demandeurs ; Sortants de formation se restreint à ceux qui sortent d'une formation.",
}

PAGES = [a["slug"] for a in APIS]

def card(cur, api):
    is_cur = api["slug"] == cur["slug"]
    style = ' style="grid-column:1/-1;border-color:#a7f3d0;background:#f0fdf4;"' if is_cur else ' style="grid-column:1/-1;"'
    count = ("cette page · " + api["ep"]) if is_cur else api["ep"]
    title = api["title"] if is_cur else '<a href="%s">%s</a>' % (api["page"], api["title"])
    body = api["role"]
    if not is_cur:
        b = BOUNDARY[frozenset({cur["slug"], api["slug"]})]
        body += '<br><strong>%s vs %s :</strong> %s' % (cur["short"], api["short"], b)
    return ('    <div class="ref-card voc-card"%s>\n'
            '      <div class="ref-head"><span class="ref-title">%s</span><span class="ref-count">%s</span></div>\n'
            '      <div class="expl">%s</div>\n'
            '    </div>') % (style, title, count, body)

def render(cur_slug):
    cur = next(a for a in APIS if a["slug"] == cur_slug)
    cards = "\n\n".join(card(cur, a) for a in APIS)
    button = "    <button class=\"tb\" onclick=\"setTab('famille')\">Famille Statistiques</button>"
    view = '''<!-- FAMILLE STATISTIQUES (généré par gen-famille-stats.py) -->
<div class="view" id="v-famille">

<div class="note" style="margin-bottom:20px;">
  <strong>Quatre API statistiques, un même moteur.</strong> France Travail expose ses statistiques via plusieurs API qui partagent <em>exactement</em> le même cadre de requête : on <code>POST</code> un indicateur en croisant territoire × activité × période × caractéristique, et les dimensions sont les mêmes référentiels. Ce qui distingue les API, ce sont les <strong>indicateurs</strong> qu'elles exposent.
</div>

<div class="ref-section">
  <h2 class="ref-section-title">
    <span class="rs-dot" style="background:#0d9488;"></span>
    Cette API dans la famille Statistiques
    <span class="rs-count">4 API</span>
    <span class="rs-tech">même cadre territoire × activité × période</span>
  </h2>
  <div class="ref-section-intro">
    Le fil conducteur : même requête, même réponse <code>IndicateurRetour</code>, mêmes référentiels. Choisir l'API revient à choisir <strong>quel angle</strong> on veut sur le territoire ou le métier.
  </div>
  <div class="ref-families">

%s

  </div>
</div>

<div class="note">
  <strong>Quelle API appeler ?</strong> Portrait socio-économique d'un territoire → <strong>Informations sur un territoire</strong>. Offres / demande / tensions / salaires par métier → <strong>Marché du travail</strong>. Devenir des demandeurs d'emploi → <strong>Accès à l'emploi des demandeurs</strong>. Retour à l'emploi après formation → <strong>Sortants de formation</strong>.
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

    s = re.sub(r"[ \t]*<button class=\"tb\" onclick=\"setTab\('famille'\)\">.*?</button>\r?\n", "", s)
    span = view_span(s, "famille")
    if span:
        pre, post = s[:span[0]], s[span[1]:]
        pre = re.sub(r"(\s*<!--[^\n]*-->)+\s*$", "", pre)
        s = pre + nl + post

    m = re.search(r"<button class=\"tb active\" onclick=\"setTab\('nested'\)\">.*?</button>", s)
    assert m, "Modèle tab button not found in " + path
    s = s[:m.end()] + nl + button + s[m.end():]

    ns = view_span(s, "nested")
    assert ns, "v-nested not found in " + path
    s = s[:ns[1]] + nl + nl + view + s[ns[1]:]

    open(path, "wb").write(s.encode("utf-8"))
    return path

if __name__ == "__main__":
    for slug in PAGES:
        print("injected:", inject(slug))
