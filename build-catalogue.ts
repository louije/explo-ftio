/**
 * build-catalogue.ts — Extracts metadata from OpenAPI schemas
 * Run: bun run build-catalogue.ts
 * Output: catalogue-data.js
 */

import { readdir } from "node:fs/promises";
import { join } from "node:path";

const SCHEMAS_DIR = join(import.meta.dir, "schemas");
const OUT_FILE = join(import.meta.dir, "catalogue-data.js");

// ── Hardcoded mappings (from INDEX.md + CATALOGUE.md) ──

const PAGE_IDS: Record<string, number> = {
  "offres-emploi": 84,
  "sortants-formation-acces-emploi": 231,
  "rechercher-usager": 465,
  "conclusions-entretiens": 515,
  "experiences-professionnelles": 116,
  "metiers-recherches-projets-evolution": 452,
  "referentiel-agences": 107,
  "rome-4-0-fiches-metiers": 272,
  "romeo": 366,
  "marche-travail": 233,
  "acces-emploi-demandeurs-emploi": 234,
  "france-travail-connect": 51,
  "coordonnees": 92,
  "formations-professionnelles": 93,
  "metiers-recherches": 115,
  "evenements-france-travail": 103,
  "rome-4-0-competences": 270,
  "rome-4-0-contextes-travail": 271,
  "jcmo-controle-offre": 279,
  "statut": 135,
  "date-naissance": 99,
  "ajout-competence": 320,
  "informations-administratives-usager": 449,
  "statut-usager": 466,
  "diagnostic-usager": 477,
  "gestion-sanctions-rsa": 497,
  "rendez-vous-partenaires": 416,
  "synthese-pages-employeurs": 561,
  "prestation-partenaire": 260,
  "orientation-usager": 0,
};

const GROUPS: Record<string, [string, string]> = {
  "france-travail-connect":              ["usager-pe", "PE Connect"],
  "coordonnees":                         ["usager-pe", "PE Connect"],
  "date-naissance":                      ["usager-pe", "PE Connect"],
  "statut":                              ["usager-pe", "PE Connect"],
  "experiences-professionnelles":        ["usager-pe", "PE Connect"],
  "formations-professionnelles":         ["usager-pe", "PE Connect"],
  "metiers-recherches":                  ["usager-pe", "PE Connect"],
  "ajout-competence":                    ["usager-pe", "PE Connect"],
  "rechercher-usager":                   ["usager-agent", "Dossier usager"],
  "informations-administratives-usager": ["usager-agent", "Dossier usager"],
  "statut-usager":                       ["usager-agent", "Dossier usager"],
  "conclusions-entretiens":              ["usager-agent", "Dossier usager"],
  "diagnostic-usager":                   ["usager-agent", "Dossier usager"],
  "metiers-recherches-projets-evolution":["usager-agent", "Dossier usager"],
  "rendez-vous-partenaires":             ["usager-agent", "Dossier usager"],
  "orientation-usager":                   ["usager-agent", "Dossier usager"],
  "gestion-sanctions-rsa":               ["partenaire", "Gestion partenaire"],
  "prestation-partenaire":               ["partenaire", "Gestion partenaire"],
  "offres-emploi":                       ["offres", "Offres d'emploi"],
  "jcmo-controle-offre":                 ["offres", "Offres d'emploi"],
  "synthese-pages-employeurs":           ["offres", "Offres d'emploi"],
  "rome-4-0-fiches-metiers":             ["rome", "ROME 4.0"],
  "rome-4-0-competences":                ["rome", "ROME 4.0"],
  "rome-4-0-contextes-travail":          ["rome", "ROME 4.0"],
  "romeo":                               ["rome", "ROME 4.0"],
  "marche-travail":                      ["stats", "Statistiques"],
  "acces-emploi-demandeurs-emploi":      ["stats", "Statistiques"],
  "sortants-formation-acces-emploi":     ["stats", "Statistiques"],
  "referentiel-agences":                 ["standalone", "Services"],
  "evenements-france-travail":           ["standalone", "Services"],
};

// Auth overrides for schemas without securitySchemes
const AUTH_OVERRIDES: Record<string, string> = {
  "rechercher-usager": "agent",
  "diagnostic-usager": "agent",
  "conclusions-entretiens": "agent",
  "informations-administratives-usager": "agent",
  "metiers-recherches-projets-evolution": "agent",
  "rendez-vous-partenaires": "agent",
  "statut-usager": "agent",
};

const CROSS_CONCEPTS = [
  { name: "Usager / Individu", apis: ["france-travail-connect","coordonnees","informations-administratives-usager","rechercher-usager","gestion-sanctions-rsa","prestation-partenaire","date-naissance","statut-usager"], collision: true },
  { name: "Code ROME", apis: ["rome-4-0-fiches-metiers","rome-4-0-competences","romeo","offres-emploi","metiers-recherches","metiers-recherches-projets-evolution","diagnostic-usager","evenements-france-travail","prestation-partenaire","rome-4-0-contextes-travail"], collision: false },
  { name: "Compétence", apis: ["rome-4-0-competences","rome-4-0-fiches-metiers","romeo","offres-emploi","ajout-competence"], collision: true },
  { name: "Adresse", apis: ["coordonnees","informations-administratives-usager","referentiel-agences","offres-emploi","metiers-recherches-projets-evolution","evenements-france-travail","synthese-pages-employeurs","prestation-partenaire","rendez-vous-partenaires"], collision: true },
  { name: "Agent / Conseiller", apis: ["diagnostic-usager","conclusions-entretiens","rechercher-usager","rendez-vous-partenaires","prestation-partenaire"], collision: false },
  { name: "Contrat", apis: ["metiers-recherches-projets-evolution","metiers-recherches","offres-emploi","statut-usager"], collision: false },
  { name: "Agence / Structure", apis: ["referentiel-agences","conclusions-entretiens","diagnostic-usager","rendez-vous-partenaires","prestation-partenaire"], collision: false },
  { name: "Rendez-vous", apis: ["rendez-vous-partenaires","conclusions-entretiens","prestation-partenaire"], collision: false },
  { name: "Statut", apis: ["statut","statut-usager","diagnostic-usager","prestation-partenaire"], collision: true },
  { name: "Salaire", apis: ["offres-emploi","metiers-recherches-projets-evolution","metiers-recherches","marche-travail"], collision: true },
  { name: "Permis", apis: ["formations-professionnelles","offres-emploi","diagnostic-usager"], collision: true },
  { name: "Formation", apis: ["formations-professionnelles","offres-emploi","evenements-france-travail"], collision: true },
];

const DOC_CONCEPTS: Record<string, string[]> = {
  "diagnostic-usager": [
    "Projets professionnels et besoins",
    "Contraintes personnelles",
    "Confiance et capacité à agir",
    "Maîtrise du numérique",
  ],
  "rechercher-usager": [
    "Identification de l'agent",
    "Recherche par NIR + date de naissance",
    "Recherche par numéro France Travail",
  ],
  "conclusions-entretiens": [
    "Entretien — type et date",
    "Modalité de contact",
    "Conseiller et agence",
  ],
  "statut-usager": [
    "Statut d'inscription",
    "Durée d'inscription",
    "Motif et catégorie",
    "Situation et clôture",
  ],
  "informations-administratives-usager": [
    "État civil",
    "Adresses",
    "Coordonnées de contact",
  ],
  "metiers-recherches-projets-evolution": [
    "Métier ciblé",
    "Conditions souhaitées",
    "Mobilité géographique",
    "Projet entrepreneurial",
  ],
  "rendez-vous-partenaires": [
    "Lecture — agenda complet",
    "Écriture — RDV du partenaire",
  ],
  "gestion-sanctions-rsa": [
    "Manquement — fait reproché",
    "Conséquences de sanction",
    "Événements de traitement",
  ],
  "prestation-partenaire": [
    "Candidatures",
    "Sessions et programmation",
    "Commandes",
    "Rendez-vous et présence",
    "Résultats et livrables",
  ],
  "orientation-usager": [
    "Calcul d'orientation",
    "Décision d'orientation",
    "Parcours et structure",
    "Critères sociaux et professionnels",
  ],
  "referentiel-agences": [
    "Identité et type",
    "Adresse et localisation",
    "Horaires d'ouverture",
  ],
  "evenements-france-travail": [
    "Salons en ligne",
    "Événements emploi",
    "Publics et objectifs",
  ],
  "coordonnees": [
    "Identité",
    "Adresse postale",
    "Contact",
  ],
  "date-naissance": [
    "Date de naissance",
  ],
  "statut": [
    "Code statut",
    "Libellé statut",
  ],
  "experiences-professionnelles": [
    "Intitulé et entreprise",
    "Période et durée",
    "Lieu et contexte",
  ],
  "formations-professionnelles": [
    "Intitulé et diplôme",
    "Niveau et domaine",
    "Permis",
  ],
  "france-travail-connect": [
    "Identité",
    "Contact",
    "Identifiants techniques",
  ],
  "ajout-competence": [
    "Compétences ROME à enregistrer",
    "Réponse partielle (206)",
  ],
  "metiers-recherches": [
    "Métier ROME et appellation",
    "Contrats et temps de travail",
    "Mobilité géographique",
    "Salaire souhaité",
  ],
  "rome-4-0-competences": [
    "Compétence et ESCO",
    "Macro-compétence et objectif",
    "Catégorie de savoirs",
  ],
  "rome-4-0-contextes-travail": [
    "Conditions de travail",
    "Horaires et déplacements",
    "Statut et publics",
  ],
  "rome-4-0-fiches-metiers": [
    "Métier",
    "Groupes de compétences",
    "Groupes de savoirs",
  ],
  "romeo": [
    "Prédiction métier",
    "Prédiction compétence",
    "Feedback de performance",
  ],
  "marche-travail": [
    "Indicateurs statistiques",
    "Ventilation par caractéristique",
    "Référentiels territoire et activité",
  ],
  "sortants-formation-acces-emploi": [
    "Accès emploi post-formation",
    "Ventilation par caractéristique",
    "Référentiels territoire et activité",
  ],
  "acces-emploi-demandeurs-emploi": [
    "Accès emploi demandeurs",
    "Ventilation par caractéristique",
    "Référentiels territoire et activité",
  ],
  "offres-emploi": [
    "Offre d'emploi",
    "Entreprise et lieu",
    "Salaire et conditions",
    "Expérience et compétences",
  ],
  "jcmo-controle-offre": [
    "Critères de contrôle",
    "Alertes de légalité",
  ],
  "synthese-pages-employeurs": [
    "Pages employeur",
    "Entête et identification",
    "Établissements",
  ],
};

// Starred APIs — appear first on the catalogue when no filter is active
const STARRED: string[] = [
  "diagnostic-usager",
  "orientation-usager",
  "rendez-vous-partenaires",
  "prestation-partenaire",
];

const GROUP_DEFS = [
  { id: "usager-agent", label: "Dossier usager", description: "APIs agent pour accéder au dossier complet d'un demandeur d'emploi" },
  { id: "usager-pe", label: "PE Connect", description: "APIs usager via France Travail Connect (OAuth individu)" },
  { id: "offres", label: "Offres d'emploi", description: "Recherche d'offres, contrôle, pages employeur" },
  { id: "rome", label: "ROME 4.0", description: "Classification des métiers et compétences" },
  { id: "stats", label: "Statistiques", description: "Indicateurs marché du travail, accès emploi, formation" },
  { id: "partenaire", label: "Gestion partenaire", description: "Prestations sous-traitées, sanctions RSA" },
  { id: "standalone", label: "Services", description: "Référentiels et événements" },
];

// ── Helpers ──

function stripMarkdown(text: string): string {
  return text
    .replace(/\r\n/g, "\n")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")   // [text](url) → text
    .replace(/\*\*([^*]+)\*\*/g, "$1")          // **bold** → bold
    .replace(/\*([^*]+)\*/g, "$1")              // *italic* → italic
    .replace(/`([^`]+)`/g, "$1")                // `code` → code
    .replace(/#+\s*/g, "")                       // # headings
    .replace(/\n{2,}/g, " ")
    .replace(/\n/g, " ")
    .trim();
}

function truncate(text: string, max: number): string {
  if (text.length <= max) return text;
  return text.slice(0, max).replace(/\s+\S*$/, "") + "…";
}

function detectAuth(schema: any, slug: string): string {
  if (AUTH_OVERRIDES[slug]) return AUTH_OVERRIDES[slug];

  const schemes = schema.components?.securitySchemes || {};
  const keys = Object.keys(schemes);
  const values = JSON.stringify(schemes);

  if (values.includes("individu")) return "peconnect";
  if (keys.some(k => k.includes("agent")) || values.includes("/agent")) return "agent";
  // partenaire realm = client credentials, no user context → "public"
  return "public";
}

// ── Main ──

async function main() {
  const files = (await readdir(SCHEMAS_DIR)).filter(f => f.endsWith(".json")).sort();
  const apis = [];

  for (const file of files) {
    const slug = file.replace(".json", "");
    const raw = await Bun.file(join(SCHEMAS_DIR, file)).text();
    const schema = JSON.parse(raw);

    const info = schema.info || {};
    const paths = schema.paths || {};
    const schemas = Object.keys(schema.components?.schemas || {});

    // Extract endpoints
    const endpoints: { method: string; path: string; summary: string }[] = [];
    for (const [path, methods] of Object.entries(paths) as [string, any][]) {
      for (const method of ["get", "post", "put", "delete", "patch"]) {
        if (methods[method]) {
          endpoints.push({
            method: method.toUpperCase(),
            path,
            summary: methods[method].summary || methods[method].operationId || "",
          });
        }
      }
    }

    // Check for doc page
    const docFile = Bun.file(join(import.meta.dir, "docs", `${slug}.html`));
    const hasDocPage = await docFile.exists();

    const group = GROUPS[slug] || ["standalone", "Services"];

    apis.push({
      slug,
      title: info.title || slug,
      version: info.version || "?",
      description: truncate(stripMarkdown(info.description || ""), 300),
      baseUrl: (schema.servers?.[0]?.url || "").replace("https://", ""),
      auth: detectAuth(schema, slug),
      endpointCount: endpoints.length,
      schemaCount: schemas.length,
      group: group[0],
      groupLabel: group[1],
      endpoints,
      schemas,
      pageId: PAGE_IDS[slug] || null,
      hasDocPage,
      concepts: DOC_CONCEPTS[slug] || [],
      starred: STARRED.includes(slug),
    });
  }

  // Sort by group order, then by title
  const groupOrder = GROUP_DEFS.map(g => g.id);
  apis.sort((a, b) => {
    const ga = groupOrder.indexOf(a.group);
    const gb = groupOrder.indexOf(b.group);
    if (ga !== gb) return ga - gb;
    return a.title.localeCompare(b.title, "fr");
  });

  const output = `// Auto-generated by build-catalogue.ts — do not edit
const CATALOGUE = ${JSON.stringify({ apis, groups: GROUP_DEFS, crossConcepts: CROSS_CONCEPTS, starred: STARRED }, null, 2)};
`;

  await Bun.write(OUT_FILE, output);
  console.log(`✓ ${apis.length} APIs → catalogue-data.js (${(output.length / 1024).toFixed(1)} KB)`);
}

main();
