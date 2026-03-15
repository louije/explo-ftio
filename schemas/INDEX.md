# France Travail API Schemas — Index & Cross-Reference

29 OpenAPI schemas from francetravail.io. This document indexes every API,
lists shared concepts, and flags where the same real-world thing is modelled
differently across schemas.

---

## 1. API inventory

### Usager-facing data APIs (via PE Connect OAuth — user token)

| # | File | API | Endpoints | Schemas | Domain |
|---|------|-----|-----------|---------|--------|
| 1 | france-travail-connect.json | France Travail Connect v1 | 1 | 1 | Identity |
| 2 | coordonnees.json | Coordonnées v1 | 1 | 1 | Contact info |
| 3 | date-naissance.json | Date de Naissance v1 | 1 | 1 | Identity |
| 4 | statut.json | Statut v1 | 1 | 1 | Registration |
| 5 | experiences-professionnelles.json | Expériences Professionnelles v1 | 1 | 1 | Career history |
| 6 | formations-professionnelles.json | Formations Professionnelles v1 | 2 | 2 | Education |
| 7 | metiers-recherches.json | PE Connect Métiers Recherchés v1 | 1 | 12 | Job search preferences |
| 8 | ajout-competence.json | Ajout de Compétence v1 | 1 | 0 | Skills management |

### Agent-facing data APIs (via jeton usager — client credentials)

| # | File | API | Endpoints | Schemas | Domain |
|---|------|-----|-----------|---------|--------|
| 9 | rechercher-usager.json | Rechercher Usager v2 | 2 | 7 | User lookup (produces jeton) |
| 10 | informations-administratives-usager.json | Infos Administratives v1 | 1 | 6 | Identity + address |
| 11 | statut-usager.json | Statut Usager v2 | 1 | 2 | Registration (detailed) |
| 12 | conclusions-entretiens.json | Conclusions Entretiens v1 | 1 | 1 | Interview records |
| 13 | diagnostic-usager.json | Diagnostic Usager v4 | 25 | 49 | Socio-professional diagnostic |
| 14 | metiers-recherches-projets-evolution.json | Métiers Recherchés v2 | 2 | 16 | Job search + career projects |
| 15 | rendez-vous-partenaires.json | Rendez-vous Partenaire v1 | 4 | 9 | Partner appointments |
| 16 | gestion-sanctions-rsa.json | Sanctions RSA v1 | 3+ | 17 | RSA sanctions |

### Job offer & employer APIs

| # | File | API | Endpoints | Schemas | Domain |
|---|------|-----|-----------|---------|--------|
| 17 | offres-emploi.json | Offres d'emploi v2 | 18 | 17 | Job offers + referentials |
| 18 | jcmo-controle-offre.json | JCMO v1 | 1 | 4 | Job offer legality check |
| 19 | synthese-pages-employeurs.json | Synthèse Pages Employeurs v1 | 4 | 16 | Employer branding pages |

### ROME reference APIs

| # | File | API | Endpoints | Schemas | Domain |
|---|------|-----|-----------|---------|--------|
| 20 | rome-4-0-fiches-metiers.json | ROME Fiches Métiers v1 | 3 | 10 | Job description sheets |
| 21 | rome-4-0-competences.json | ROME Compétences v1 | 21 | 12 | Competency tree |
| 22 | rome-4-0-contextes-travail.json | ROME Contextes Travail v1 | 3 | 2 | Work context categories |
| 23 | romeo.json | Romeo v2 | 4 | 14 | AI ROME matching |

### Statistical APIs (shared framework)

| # | File | API | Endpoints | Schemas | Domain |
|---|------|-----|-----------|---------|--------|
| 24 | marche-travail.json | Marché du travail v1 | 24 | 30+ | Labour market stats |
| 25 | acces-emploi-demandeurs-emploi.json | Accès Emploi DE v1 | 22 | 30+ | Employment access stats |
| 26 | sortants-formation-acces-emploi.json | Sortants Formation v1 | 20+ | 30+ | Training exit stats |

### Other APIs

| # | File | API | Endpoints | Schemas | Domain |
|---|------|-----|-----------|---------|--------|
| 27 | referentiel-agences.json | Référentiel Agences v1 | 2 | 1 | Agency directory |
| 28 | evenements-france-travail.json | Événements Emploi v1 | 5 | 6 | Employment events/salons |
| 29 | prestation-partenaire.json | Prestations Sous-traitées v1 | 8+ | 20+ | Outsourced services |

---

## 2. Authentication patterns

Two distinct realms, plus public APIs:

### PE Connect (individu realm — user is the job seeker)

The job seeker authenticates via OAuth2 authorization code flow.
APIs 1–8 use this pattern. Each gets an individual access token with
specific scopes.

### Client Credentials + jeton usager (agent realm — user is a counsellor)

The partner system authenticates via client credentials. To access a
specific job seeker's data, the system first calls **Rechercher Usager**
(API #9) with the person's NIR or numéro France Travail, and receives
a `jetonUsager` — an encrypted, volatile, day-lived token. This token is
then passed as a header (`ft-jeton-usager`) to all subsequent calls.

APIs 9–16 use this pattern. Most also require `pa-nom-agent`,
`pa-prenom-agent`, `pa-identifiant-agent` headers identifying the
counsellor making the request.

### Public / open scope

APIs 17, 20–28 are accessible with client credentials alone (no user
context needed). The ROME APIs and statistical APIs are essentially
public reference data.

---

## 3. Cross-cutting concepts

### A. Usager / Individu — the job seeker

The same person appears across many APIs, but is modelled differently each time.

| API | Schema/Field | Key properties | Notes |
|-----|-------------|----------------|-------|
| france-travail-connect | `UserInfo` | sub (uuid), gender, family_name, given_name, email | OIDC-style, English field names |
| coordonnees | `Coordonnees` | nom, prenom, email, telephone1/2, adresse1–4, codePostal, codeINSEE | Flat object, French names |
| informations-admin | `UsagerResource` | numeroFranceTravail + nested EtatCivilResource, AdresseResource[], EmailResource[], TelephoneResource[] | Structured, with arrays for multiple addresses |
| informations-admin | `EtatCivilResource` | civilite, nom, prenom, nomCorrespondance, prenomCorrespondance, dateNaissance, nir | Most complete identity |
| date-naissance | `DateDeNaissance` | dateDeNaissance (ISO 8601) | Single field |
| rechercher-usager | `ResultatDTO` | jetonUsager, numeroFranceTravail, topIdentiteCertifiee | Lookup result, not profile |
| gestion-sanctions-rsa | `Individu` | numeroFranceTravail only | Minimal |
| prestation-partenaire | `Individu` | nom, prenom, numeroFranceTravail, civilite, codeAssedic, codeBNI, idGide, identifiantRCU, telephone, commune, mail | Most fields, includes legacy IDs |

**Type conflicts:**
- `civilite`: string "M"/"Mme"/"Mx" (rendez-vous), "1"/"3" (prestation), English "male"/"female" (FT Connect)
- `nom`/`prenom`: appear as separate fields everywhere except `libelleAgent` in conclusions-entretiens (single concatenated string "DUBOIS JEAN")
- `email`: single string (most APIs) vs. array of `EmailResource` (infos-admin) vs. nullable confirmed email (FT Connect)
- `telephone`: single string, vs. telephone1/telephone2 (coordonnees), vs. telephone + telephoneMobile (prestation)
- `adresse`: wildly different structures across APIs (see section F below)

### B. Agent / Conseiller — the counsellor

| API | Representation | Properties | Notes |
|-----|---------------|------------|-------|
| diagnostic-usager | `AgentDto` object | nom, prenom, structure, type | Richest model, embedded in every modified entity |
| conclusions-entretiens | Flat strings | codeAgent, libelleAgent ("DUBOIS JEAN") | No structured object |
| rechercher-usager | HTTP headers | pa-nom-agent, pa-prenom-agent, pa-identifiant-agent | Not in response at all |
| rendez-vous-partenaires | `Interlocuteur` object | civilite, nom, prenom, organisme, service, email, telephone | Contact-oriented (not agent identity) |
| prestation-partenaire | String matricules | agentCreateur, agentModificateur, agentPrescripteur | Just ID strings, no name |

**Type conflicts:**
- diagnostic-usager models the agent as a structured **object** attached to every data point
- conclusions-entretiens uses **flat fields** on the parent entity
- prestation-partenaire uses **opaque matricule strings** only
- In headers, agent info is always three separate strings — never a structured object

### C. Code ROME / Métier / Appellation — occupational classification

The ROME (Répertoire Opérationnel des Métiers) is the backbone of the
employment ecosystem. It appears in virtually every API, but at different
levels of granularity.

| API | Fields/Schema | Level | Notes |
|-----|--------------|-------|-------|
| rome-4-0-fiches-metiers | `FicheMetier` > `Metier` {code, libelle} | Full ROME sheet | Canonical source |
| rome-4-0-competences | `Competence` hierarchy | Skills tree | Cross-referenced to ROME |
| rome-4-0-contextes-travail | `ContexteTravail` {code, libelle, categorie} | Work context categories | Linked to ROME jobs |
| romeo | `AppellationRome` {codeAppellation, libelleAppellation, codeRome, libelleRome} | AI-predicted | Mapping free text → ROME |
| offres-emploi | `romeCode` + `romeLibelle` + `appellationlibelle` | Flat strings on Offre | No separate Rome object |
| offres-emploi | `Referentiel` via /referentiel/metiers, /referentiel/appellations | Code/libelle pairs | Lookup tables |
| metiers-recherches-projets-evolution | `rome` {code, libellé} + `appellation` {code, libelle} | Separate objects | Note: `libellé` with accent (typo in schema) |
| metiers-recherches (PE Connect) | `Rome` {code, libelle} + `Appellation` {code, libelle} | Separate objects | Same structure, different schema names |
| diagnostic-usager | `DiagnosticIndividuDto` | codeRome, codeAppellation, nomMetier | Flat fields on diagnostic entity |
| evenements-france-travail | `codesRome` array of strings | Just codes, no labels | On event objects |
| prestation-partenaire | `codeRome` string | Single code | On candidature |

**Type conflicts:**
- rome/appellation: sometimes separate objects, sometimes flat strings, sometimes just codes
- `libellé` vs `libelle` (accent typo in metiers-recherches-projets-evolution)
- ROME code format is consistent (letter + 4 digits, e.g. "K1302") across all APIs

### D. Compétence — skill/competency

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| rome-4-0-competences | `Competence` base type | code, libelle, type, transitionEcologique, transitionNumerique | Polymorphic: CompetenceDetaillee, MacroSavoirFaire, MacroSavoirEtreProfessionnel, Savoir |
| rome-4-0-competences | `DomaineCompetence` > `Enjeu` > `Objectif` > `MacroCompetence` | Full tree hierarchy | With RIASEC codes, maturité, ESCO mapping |
| rome-4-0-fiches-metiers | Same types via $ref | Same as above | Consumed by fiches |
| romeo | `CompetenceRome` | libelleCompetence, codeCompetence, typeCompetence, scorePrediction | AI-predicted match |
| offres-emploi | `Competence` | code, libelle, exigence (E/S) | Flat, exigence-oriented — **completely different schema** |
| ajout-competence | (inline, no schema) | Endpoint only | Writes to portefeuille de compétences |

**Type conflicts:**
- rome-4-0-competences `Competence` is a rich polymorphic type with inheritance
- offres-emploi `Competence` is a flat {code, libelle, exigence} — **same name, different structure**
- diagnostic-usager has `BesoinIndividuDto` which is conceptually different (a "need" vs a "skill") but plays a similar role in assessment

### E. Contrat / Type de contrat — employment contract

| API | Schema | Values | Notes |
|-----|--------|--------|-------|
| metiers-recherches-projets-evolution | `typeContrat` | code enum: CDI, CDD, DIN, MIS, SAI, LIB, CCE, FS, E2, PS | Full object with code/libelle/libelleLong |
| metiers-recherches (PE Connect) | `TypeContrat` | Same enum | Same structure |
| offres-emploi | `typeContrat` string + referential | "CDD", "CDI" etc. | Flat string on Offre + /referentiel/typesContrats |
| statut-usager | `m_categ_inscription_code/lib` | "1"–"5" for inscription categories | **Different concept**: registration category, not contract type |

### F. Adresse / Lieu / Localisation — address & location

This is the most fragmented concept. Every API that handles addresses
uses a different structure.

| API | Schema | Format |
|-----|--------|--------|
| coordonnees | `Coordonnees` | adresse1–4 (4 lines), codePostal, codeINSEE, libelleCommune, codePays |
| informations-admin | `AdresseResource` | complementAdresse, complementDestinataire, complementDistribution, libelleCommune, codePostal, codeInseeCommune, libellePays, numeroTypeLibelleVoie |
| referentiel-agences | `adressePrincipale` | ligne3–6 (postal norm), bureauDistributeur, communeImplantation, gpsLat, gpsLon |
| offres-emploi | `LieuTravail` | libelle ("74 - ANNECY"), latitude, longitude, codePostal, commune (INSEE) |
| offres-emploi | `Commune` | code (INSEE), libelle, codePostal, codeDepartement |
| metiers-recherches-projets | `lieu` | code, Libelle, type (1=Pays, 2=Continent, 3=Région, 4=Département, 5=Commune) |
| evenements-france-travail | (inline) | ville, codePostal, codeInsee, longitude, latitude |
| synthese-pages-employeurs | `Adresse` | complementAdresse, numeroVoie, extensionNumeroVoie, libelleVoie, codePostal, libelleDistributionPostale |
| prestation-partenaire | `Adresse` | adresseLigne1–4, codeInsee, codePostal, ville, villePostale, identifiantAurore, typeLieu |
| rendez-vous-partenaires | `AdresseRDVU` | adresseLibre (freeform name), libelleAdresse (freeform address) |

**Key observations:**
- No two APIs share the same address schema
- Some use structured fields (numéro, voie, code postal), others use line-based (ligne1–4 or adresse1–4)
- GPS coordinates are present in: referentiel-agences (gpsLat/gpsLon), offres-emploi (latitude/longitude), evenements (latitude/longitude)
- Code INSEE commune appears as: `codeINSEE`, `codeInseeCommune`, `codeInsee`, `commune`, `communeImplantation`, `communeInsee` — same data, 6 different field names

### G. Agence / Structure / Organisme — agency or organisation

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| referentiel-agences | `Agence` | code (Aurore), codeSafir, libelle, type, adresse, horaires, zoneCompetences | Canonical source, very detailed |
| conclusions-entretiens | Flat strings | codeAgence, libelleAgence | Simple |
| diagnostic-usager | `AgentDto.structure` | string | Freeform |
| rendez-vous-partenaires | `Organisme` | code (enum: IND/FT/CD/DCD/ML/CE), idStructure, libelleStructure | Network partner types |
| prestation-partenaire | Various | siteGestionnaire, siteRattachement (SAFIR codes) | Legacy naming |

**Organisme.code enum (rendez-vous) maps the employment network:**
- IND = Indépendant
- FT = France Travail
- CD = Conseil Départemental
- DCD = Délégataire du Conseil Départemental
- ML = Mission Locale
- CE = Cap Emploi

### H. Rendez-vous / Entretien — appointments & interviews

| API | Schema | Key properties | Notes |
|-----|--------|----------------|-------|
| rendez-vous-partenaires | `RendezVousPartenaire` | date, modaliteContact (VISIO/TELEPHONE/PHYSIQUE), motif (AUT/ACC/ORI), statut (PRIS/EFFECTUE/MODIFIE/ABSENT/ANNULE) | CRUD operations |
| rendez-vous-partenaires | `RendezVousUsager` | Same + estEnConflit, historiqueEvenementList, dateAnnulation, motifAnnulation | Read-only aggregated view |
| conclusions-entretiens | `ConclusionEntretienPartenaireDetailsDto` | dateEntretien, typeEntretien (21 enum values), codeModaliteContact (8 enum values), commentaire | Read-only history |
| prestation-partenaire | `RendezVous` | Embedded in Session/Commande | Different context (outsourced service delivery) |

**Modalité de contact — same concept, different enums:**
- rendez-vous: VISIO, TELEPHONE, PHYSIQUE (3 values)
- conclusions-entretiens: B, C, F, I, R, T, V, W (8 values — more granular: distinguishes visioguichet from visioconference, adds collectif, courriel, bilan en ligne)

### I. Statut du demandeur — job seeker registration status

| API | Schema | Type | Values |
|-----|--------|------|--------|
| statut | `StatutResponse.codeStatutIndividu` | string enum | "0" (non DE), "1" (DE) — **binary** |
| statut-usager | `Contrat.m_statut` | string enum | "Identifié", "Inscrit", "Cessé", "Radié" — **4-state lifecycle** |
| diagnostic-usager | `DiagnosticIndividuDto.statut` | string enum | "EN_COURS", "ARCHIVE", "SUPPRIME" — **project status, not person status** |
| prestation-partenaire | `Candidature.statut` | string enum | TR, AN, AT, SS, EC, EA — **candidature processing status** |

These are four entirely different status enums about four different things
(person registration, detailed registration lifecycle, diagnostic project
state, and service candidature processing).

### J. Salaire — salary

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| offres-emploi | `Salaire` | libelle ("Mensuel de 1923.00 Euros sur 12 mois"), commentaire, complement1, complement2, listeComplements[] | Descriptive, text-oriented |
| metiers-recherches-projets-evolution | `salaire` | libelle (enum: Annuel/Mensuel/Cachet/Horaire/Autre), remuneration (double) | Structured, numeric |
| metiers-recherches (PE Connect) | `Salaire` | remuneration (double), libelle, code | Structured |
| marche-travail | Via statistical indicators | valeurPrincipaleMontant (double) | Aggregate statistics only |

### K. Permis — driving license

| API | Type | Values/Structure |
|-----|------|-----------------|
| formations-professionnelles | `Permis` {code, libelle} | 20 codes: A, A1, A2, AM, B, B1, B79, B96, BE, C, C1, C1E, CE, D, D1, D1E, DE, EB, EC, ED |
| offres-emploi | `Permis` {libelle, exigence} | Label-based ("B - Véhicule léger"), no code. Exigence: E (required) / S (desired) |
| offres-emploi | Referential /referentiel/permis | Code/libelle pairs | Lookup table |
| diagnostic-usager | Situation constats | "Permis non valide / suspension de permis" | **Not a data object** — it's a yes/no assessment question |

### L. Formation — training/education

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| formations-professionnelles | `Formation` | anneeFin, description, diplomeObtenu, domaine{code,libelle}, intitule, etranger, lieu, niveau{code,libelle} | User's own training history |
| offres-emploi | `Formation` | codeFormation, domaineLibelle, niveauLibelle, commentaire, exigence (E/S) | Job offer requirement |
| evenements-france-travail | `diplomes` array of strings | Diploma level labels | On event listings |

**Same name `Formation`, different schemas**: user's training record vs. job
requirement. Different fields entirely.

---

## 4. Statistical APIs — shared framework

Three APIs share an **identical** internal schema framework:

- **marche-travail.json** — Labour market indicators (DE counts, offers, hires, tensions)
- **acces-emploi-demandeurs-emploi.json** — Employment access rates
- **sortants-formation-acces-emploi.json** — Training exit outcomes

All three use the same schema set:

```
CritereIndicateurAvecNomenclature / CritereIndicateurSansNomenclature
  → Caracteristique

IndicateurRetour
  → ValeursParPeriode
    → ValeursParCaracteristique

Referential schemas (identical across all 3):
  Activite, TypeActivite, ListeActivite, ListeTypeActivite
  Caracteristique, TypeCaracteristique, ListeCaracteristique, ListeTypeCaracteristique
  Nomenclature, TypeNomenclature, ListeNomenclature, ListeTypeNomenclature
  Periode, TypePeriode, ListePeriode
  Territoire, TypeTerritoire, ListeTerritoire, ListeTypeTerritoire
  DetailIndicateur, CroisementIndicateur, CaracteristiqueIndicateur
  ValeurNomenclatureIndicateur, TypeNomenclatureIndicateur, TypePeriodeIndicateur
  TypeValeur
```

These could share a single schema definition. They are copy-pasted across
the three OpenAPI files.

---

## 5. Naming inconsistencies

### Field name variations for the same data

| Real-world thing | Variations found |
|-----------------|-----------------|
| Code INSEE commune | `codeINSEE`, `codeInseeCommune`, `codeInsee`, `commune`, `communeImplantation`, `communeInsee` |
| Code postal | `codePostal`, `codePostale` (typo in evenements) |
| Identifiant | `id`, `identifiant`, `identifiantCandidature`, `idDiagnostic`, `idOrigine`, `idRCE` |
| Numéro France Travail | `numeroFranceTravail` (most), implicit via jeton (some) |
| Date de mise à jour | `dateMiseAJour`, `datMaj`, `dateModification`, `dateActualisation`, `updated_at`, `lastModifiedDate` |

### Schema name collisions (same name, different structure)

| Name | APIs | Difference |
|------|------|------------|
| `Competence` | rome-4-0-competences, offres-emploi, romeo | Rich polymorphic type vs. flat {code,libelle,exigence} vs. {intitule,identifiant} |
| `Formation` | formations-professionnelles, offres-emploi | User's training history vs. job requirement |
| `Permis` | formations-professionnelles, offres-emploi | {code,libelle} vs. {libelle,exigence} |
| `Salaire` | offres-emploi, metiers-recherches, metiers-recherches-projets-evolution | Three different structures |
| `Adresse` | synthese-pages-employeurs, prestation-partenaire | Completely different field sets |
| `Individu` | gestion-sanctions-rsa, prestation-partenaire | Minimal (1 field) vs. rich (12+ fields) |
| `Commune` | offres-emploi, prestation-partenaire | {code,libelle,codePostal,codeDepartement} vs. different structure |
| `Activite` | marche-travail/stats APIs, prestation-partenaire | Statistical dimension vs. service activity |
| `Objectif` | diagnostic-usager, rome-4-0-competences | Action to overcome a barrier vs. competency framework element |
| `Situation` | diagnostic-usager | Constraint constat — not used elsewhere as a schema name |

### Enum naming patterns

Most APIs use SCREAMING_SNAKE_CASE for enum values:
`EN_COURS`, `NON_ABORDEE`, `POINT_FORT`, `MACRO-SAVOIR-FAIRE`

Exceptions:
- statut-usager uses French words with accents: `"Identifié"`, `"Inscrit"`, `"Cessé"`, `"Radié"`
- statut uses numeric strings: `"0"`, `"1"`
- formations-professionnelles uses short codes for niveaux: `"NV1"`, `"C3A"`, `"AFS"`

### Field naming conventions

Most agent-realm APIs use camelCase: `dateExploration`, `codeRome`, `nomMetier`

Exceptions:
- statut-usager uses m_ prefix Hungarian notation: `m_statut`, `m_date_effet_statut`, `m_duree_inscription_12`
- france-travail-connect uses OIDC snake_case: `family_name`, `given_name`, `updated_at`
- Some metiers-recherches-projets-evolution fields have accent in key: `libellé`

---

## 6. API groupings for documentation

Based on shared concepts and likely user workflows, natural groupings for
generating documentation pages:

### Group A — Dossier usager (Job seeker file)
Tightly coupled APIs that together form the complete picture of a job seeker.
Linked by `jetonUsager` or PE Connect token.

1. **rechercher-usager** — find the person, get token
2. **informations-administratives-usager** — who they are
3. **statut-usager** — their registration status
4. **diagnostic-usager** — their socio-professional assessment (most complex)
5. **conclusions-entretiens** — their interview history
6. **metiers-recherches-projets-evolution** — their career goals
7. **rendez-vous-partenaires** — their appointments

Plus the PE Connect equivalents (simpler, user-initiated):
- france-travail-connect, coordonnees, date-naissance, statut,
  experiences-professionnelles, formations-professionnelles,
  metiers-recherches

### Group B — Offres d'emploi (Job offers)
8. **offres-emploi** — search and read job offers
9. **jcmo-controle-offre** — check offer legality
10. **synthese-pages-employeurs** — employer branding

### Group C — Référentiel ROME (Occupational classification)
11. **rome-4-0-fiches-metiers** — job description sheets
12. **rome-4-0-competences** — skills/competency tree
13. **rome-4-0-contextes-travail** — work situations
14. **romeo** — AI text-to-ROME matching

### Group D — Statistiques (Labour market stats)
15. **marche-travail** — market indicators
16. **acces-emploi-demandeurs-emploi** — employment access rates
17. **sortants-formation-acces-emploi** — training exit outcomes

### Group E — Gestion partenaire (Partner service management)
18. **prestation-partenaire** — outsourced service sessions/candidatures
19. **gestion-sanctions-rsa** — RSA sanctions workflow

### Standalone
20. **referentiel-agences** — agency directory
21. **evenements-france-travail** — employment events/salons
22. **ajout-competence** — add skills to profile
