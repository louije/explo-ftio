# France Travail API Schemas — Index & Cross-Reference

44 OpenAPI schemas from francetravail.io, refreshed from the 2026-10-28 sweep
(see `CATALOGUE.md`). 43 are still publicly downloadable; `offres-emploi.json`
is the last public copy (its page has returned `403` since that sweep). This
document indexes every API, lists shared concepts, and flags where the same
real-world thing is modelled differently across schemas.

Counts below are computed from the files (`paths` operations, `components.schemas`).
Families follow the catalogue grouping (`GROUPS` in `build-catalogue.ts`).

---

## 1. API inventory

Auth column = security scheme declared by the schema: **individu** (PE Connect /
France Travail Connect user OAuth), **agent** (agent realm: client credentials or
ProConnect, plus `jetonUsager`), **partenaire** (client credentials only),
**JWT** (`jsonWebToken`), **—** (none declared).

### Dossier usager (agent realm, via jeton usager)

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 1 | rechercher-usager.json | Rechercher usager | 2.1 | 3 | 8 | agent | User lookup → `jetonUsager` (NIR, numéro FT or identité pivot) |
| 2 | informations-administratives-usager.json | Informations administratives usager | 1.2.0 | 1 | 6 | agent | Identity + addresses |
| 3 | statut-usager.json | Statut Usager | 2.0 | 1 | 2 | agent | Registration status (detailed) |
| 4 | diagnostic-usager.json | Diagnostic Usager | 4.0 | 25 | 49 | agent | Socio-professional diagnostic |
| 5 | conclusions-entretiens.json | Conclusions Entretiens | 1.0.0 | 1 | 1 | agent | Interview records |
| 6 | metiers-recherches-projets-evolution.json | Métiers recherchés, projets d'évolution… | 1.0.40 | 2 | 17 | agent | Job search + career / business projects |

### Parcours d'accompagnement (loi plein emploi)

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 7 | orientation-usager-v2.json | Orientation Usager (page 635) | 2.1 | 6 | 16 | agent | Orientation: 4 actor roles, réorientation reasons |
| 8 | orientation-usager.json | Orientation Usager (page 433) | 1.0 | 5 | 14 | agent | Orientation, previous version |
| 9 | contrat-engagement.json | Contrat d'engagement | v1 | 6 | 9 | agent | Mutual commitments, signature |
| 10 | rendez-vous-partenaires.json | Rendez-vous partenaire | 1.0.0 | 4 | 9 | agent | Partner appointments |
| 11 | declaration-demarche.json | Déclaration de démarche | v1 | 4 | 14 | individu | Job-search steps (pourquoi / quoi / comment) |
| 12 | gestion-sanctions-rsa.json | Gestion des sanctions RSA | 1.4 | 4 | 17 | agent | RSA sanctions, remobilisation |

### Connexion & identité (individu realm)

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 13 | france-travail-connect.json | France Travail Connect | 1.0.0 | 1 | 1 | individu | Identity (OIDC userinfo, numéro FT) |
| 14 | coordonnees.json | API Coordonnées | 1.0 | 1 | 1 | individu | Contact info |
| 15 | date-naissance.json | API Date de Naissance | 1.0 | 1 | 1 | individu | Birth date |
| 16 | statut.json | API Statut | 1.0.0 | 1 | 1 | individu | Registration (binary) |
| 17 | pe-connect-indemnisations.json | API Indemnisations | 1.0.0 | 1 | 1 | individu | Benefits (ARE/ASP, minima sociaux) |

### Profil de compétences (individu realm)

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 18 | experiences-professionnelles.json | API Expériences Professionnelles | 1.0 | 1 | 1 | individu | Self-declared career history |
| 19 | experiences-declarees-employeur.json | API Expériences déclarées par l'employeur | 1.0 | 1 | 3 | individu | Employer-declared contracts (SIRET) |
| 20 | competences-professionnelles.json | Compétences professionnelles | 2.0.0 | 3 | 5 | individu | Skills, languages, interests |
| 21 | ajout-competence.json | API Ajout de Compétence | 1.0.0 | 1 | 0 | individu | Write skills to the portfolio |
| 22 | formations-professionnelles.json | API Formations Professionnelles | 1.0 | 2 | 2 | individu | Education |
| 23 | metiers-recherches.json | API Métiers Recherchés | 1.0.0 | 1 | 16 | individu | Job search preferences |

### Offres & recrutement

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 24 | offres-emploi.json | Offres d'emploi | 2 | 18 | 22 | partenaire | Job offers + referentials (schema no longer public) |
| 25 | la-bonne-boite.json | La Bonne Boite | 2.27.3 | 3 | 18 | partenaire | Companies likely to hire |
| 26 | jcmo-controle-offre.json | Je Contrôle Mon Offre - JCMO | 1 | 1 | 4 | JWT | Job offer legality check |
| 27 | synthese-pages-employeurs.json | Synthèse des pages employeur | 1.0.0 | 4 | 25 | partenaire | Employer branding pages |
| 28 | je-recrute-avec-ftpro.json | Je recrute avec FT pro | 1.0 | 1 | 6 | partenaire | Recruitment-need signalling (widget) |

### ROME 4.0

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 29 | rome-4-0-metiers.json | ROME 4.0 - Métiers | 1 | 17 | 20 | partenaire | Job tree, appellations, RIASEC |
| 30 | rome-4-0-fiches-metiers.json | ROME V4.0 - Fiches ROME | 1 | 3 | 12 | partenaire | Job description sheets |
| 31 | rome-4-0-competences.json | ROME 4.0 - Compétences | 1 | 21 | 12 | partenaire | Competency tree |
| 32 | rome-4-0-contextes-travail.json | ROME V4.0 - Situations de travail | 1 | 3 | 2 | partenaire | Work contexts |
| 33 | rome-4-0-substitutions.json | ROME 4.0 - Substitutions d'entités | 1 | 2 | 1 | partenaire | Obsolete code → replacement code |
| 34 | romeo.json | Romeo | 2.0 | 4 | 16 | — | AI text → ROME matching |

### Statistiques (shared framework, see §4)

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 35 | marche-travail.json | Marché du travail | 1.1 | 35 | 35 | partenaire | Job seekers, offers, hires, tensions, salaries |
| 36 | acces-emploi-demandeurs-emploi.json | Accès à l'emploi des demandeurs d'emploi | 1.1 | 28 | 32 | partenaire | Employment access rates (ACC_1, ACC_8) |
| 37 | sortants-formation-acces-emploi.json | Sortants de formation et accès à l'emploi | 1.1 | 28 | 33 | partenaire | Training exit outcomes (ACC_2, DE_3) |
| 38 | informations-territoire.json | Informations sur un territoire | 1.1 | 31 | 32 | partenaire | Territory profile (population, establishments, DYN_1) |

### Gestion partenaire

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 39 | prestation-partenaire.json | Gestion des prestations sous-traitées | 1.0.0 | 20 | 73 | partenaire | Outsourced services |
| 40 | gestion-activites-operationnelles.json | Gestion activités opérationnelles | 2.1 | 7 | 8 | agent | Operational tasks of a structure |

### Référentiels & services

| # | File | API | Version | Endpoints | Schemas | Auth | Domain |
|---|------|-----|---------|-----------|---------|------|--------|
| 41 | referentiel-agences.json | API Référentiel des Agences | 1.0.0 | 2 | 1 | partenaire | Agency directory |
| 42 | cadre-vie-communes.json | API Cadre de vie des communes | 1.0.0 | 1 | 1 | partenaire | Commune amenities |
| 43 | open-formation.json | API Open Formation | 1.0 | 3 | 5 | partenaire | Training info sessions, application slots |
| 44 | evenements-france-travail.json | API Mes évènements emplois | 1.1 | 3 | 5 | partenaire | Employment events |

---

## 2. Authentication patterns

Three realms, plus two exceptions:

### Individu realm (PE Connect / France Travail Connect — user is the job seeker)

The job seeker authenticates via the OAuth2 authorization code flow
(`authentification_individu`). Each API gets an individual access token with
specific scopes. Used by the *Connexion & identité* and *Profil de compétences*
families, and by `declaration-demarche`.

### Agent realm (user is a counsellor)

Since the 2026-10 refresh, every agent-realm schema declares the same two
flows: `authentification_agent` (ProConnect authorization code, the counsellor
logs in) and `authentification_agent-clientCredentials` (system-to-system);
`rendez-vous-partenaires` only declares the first. Before, the scopes were
only described in prose.

To access a specific job seeker's data, the system first calls **Rechercher
usager** with the person's NIR + birth date, numéro France Travail, or — since
v2.1 — *identité pivot* (birth name, first names, sex, birth date and place),
and receives a `jetonUsager`: an encrypted, day-lived token passed as the
`ft-jeton-usager` header to subsequent calls. In client-credentials mode, calls
also carry `pa-nom-agent`, `pa-prenom-agent`, `pa-identifiant-agent` to identify
the counsellor.

Used by the *Dossier usager* family, most of *Parcours d'accompagnement*
(orientation, contrat d'engagement, rendez-vous, sanctions) and
`gestion-activites-operationnelles`. Exception: orientation v2.1's
`GET /nomenclature/motifs-reorientation` takes no jeton.

### Partenaire realm (no user context)

Client credentials alone (`authentification_partenaire`): ROME, statistics,
offers & recruitment, referentials & services, and `prestation-partenaire`.
Essentially public reference data.

### Exceptions

- `jcmo-controle-offre` declares a `jsonWebToken` bearer scheme.
- `romeo` declares no security scheme at all.

---

## 3. Cross-cutting concepts

### A. Usager / Individu — the job seeker

The same person appears across many APIs, but is modelled differently each time.

| API | Schema/Field | Key properties | Notes |
|-----|-------------|----------------|-------|
| france-travail-connect | `UserInfo` | sub (uuid), idIdentiteExterne, referenceExterne, gender, family_name, given_name, email | OIDC-style, English field names; `referenceExterne` = numéro FT (added 2026-10) |
| coordonnees | `Coordonnees` | nom, prenom, email, telephone1/2, adresse1–4, codePostal, codeINSEE | Flat object, French names |
| informations-admin | `UsagerResource` | numeroFranceTravail + nested EtatCivilResource, AdresseResource[], EmailResource[], TelephoneResource[] | Structured, with arrays for multiple addresses |
| informations-admin | `EtatCivilResource` | civilite, nom, prenom, nomCorrespondance, prenomCorrespondance, dateNaissance, nir | Most complete identity |
| date-naissance | `DateDeNaissance` | dateDeNaissance (ISO 8601) | Single field |
| rechercher-usager | `ResultatDTO` | jetonUsager, numeroFranceTravail, topIdentiteCertifiee | Lookup result, not profile |
| rechercher-usager | `ParIdentitePivotDTO` | nomFamilleNaissance, prenoms, sexe (M/F), dateNaissance, codeInseeLieuNaissance, codeInseePaysNaissance, adresseMail | Lookup input (v2.1): birth identity, no identifier |
| gestion-sanctions-rsa | `Individu` | numeroFranceTravail only | Minimal |
| gestion-activites-operationnelles | (field) | numeroFranceTravail | On each activity |
| prestation-partenaire | `Individu` | nom, prenom, numeroFranceTravail, civilite, codeAssedic, codeBNI, idGide, identifiantRCU, telephone, commune, mail | Most fields, includes legacy IDs |

**Type conflicts:**
- `civilite`: string "M"/"Mme"/"Mx" (rendez-vous), "1"/"3" (prestation), English "male"/"female" (FT Connect `gender`), birth sex "M"/"F" (rechercher-usager `sexe`)
- `nom`/`prenom`: appear as separate fields everywhere except `libelleAgent` in conclusions-entretiens (single concatenated string "DUBOIS JEAN"); rechercher-usager's pivot takes all first names in one `prenoms` string
- `email`: single string (most APIs) vs. array of `EmailResource` (infos-admin) vs. nullable confirmed email (FT Connect)
- `telephone`: single string, vs. telephone1/telephone2 (coordonnees), vs. telephone + telephoneMobile (prestation)
- numéro France Travail: `numeroFranceTravail` (most) vs. `referenceExterne` (FT Connect)
- `adresse`: wildly different structures across APIs (see section F below)

### B. Agent / Conseiller — the counsellor

| API | Representation | Properties | Notes |
|-----|---------------|------------|-------|
| diagnostic-usager | `AgentDto` object | nom, prenom, structure, type | Richest model, embedded in every modified entity |
| orientation-usager (v1, v2) | Fields on orientation / decision | agent_creation, agent_decision, agent_derniere_modification; v2 adds referent_parcours | snake_case; v2 names the follow-up actor explicitly |
| conclusions-entretiens | Flat strings | codeAgent, libelleAgent ("DUBOIS JEAN") | No structured object |
| rechercher-usager, contrat-engagement, gestion-activites-operationnelles, orientation | HTTP headers | pa-nom-agent, pa-prenom-agent, pa-identifiant-agent | Not in response at all |
| rendez-vous-partenaires | `Interlocuteur` object | civilite, nom, prenom, organisme, service, email, telephone | Contact-oriented (not agent identity) |
| prestation-partenaire | String matricules | agentCreateur, agentModificateur, agentPrescripteur | Just ID strings, no name |

**Type conflicts:**
- diagnostic-usager models the agent as a structured **object** attached to every data point
- conclusions-entretiens and orientation use **flat fields** on the parent entity
- prestation-partenaire uses **opaque matricule strings** only
- In headers, agent info is always three separate strings — never a structured object

### C. Code ROME / Métier / Appellation — occupational classification

The ROME (Répertoire Opérationnel des Métiers) is the backbone of the
employment ecosystem. It appears in virtually every API, but at different
levels of granularity.

| API | Fields/Schema | Level | Notes |
|-----|--------------|-------|-------|
| rome-4-0-metiers | `Metier`, `Appellation` (romeParent, appellationsProches, appellationsEnvisageables, appellationEsco) | Navigable job tree | Canonical source for codes and labels |
| rome-4-0-fiches-metiers | `FicheMetier` > `Metier` {code, libelle} | Full ROME sheet | Assembled view |
| rome-4-0-competences | `Competence` hierarchy | Skills tree | Cross-referenced to ROME |
| rome-4-0-contextes-travail | `ContexteTravail` {code, libelle, categorie} | Work context categories | Linked to ROME jobs |
| rome-4-0-substitutions | `Substitution` {code, codeSubstitution, typeEntite, obsolete, dateFin} | Code maintenance | typeEntite: APPELLATION, COMPETENCE, CONTEXTE-TRAVAIL, METIER |
| romeo | `AppellationRome` {codeAppellation, libelleAppellation, codeRome, libelleRome} | AI-predicted | Mapping free text → ROME |
| offres-emploi | `romeCode` + `romeLibelle` + `appellationlibelle` | Flat strings on Offre | No separate Rome object |
| offres-emploi | `Referentiel` via /referentiel/metiers, /referentiel/appellations | Code/libelle pairs | Lookup tables |
| la-bonne-boite | `rome` | Search criterion | Companies by ROME + place |
| metiers-recherches-projets-evolution | `rome` {code, libellé} + `appellation` {code, libelle} | Separate objects | Note: `libellé` with accent (typo in schema) |
| metiers-recherches (PE Connect) | `Rome` {code, libelle} + `Appellation` {code, libelle} | Separate objects | Same structure, different schema names |
| diagnostic-usager | `DiagnosticIndividuDto` | codeRome, codeAppellation, nomMetier | Flat fields on diagnostic entity |
| evenements-france-travail | `codesRome` array of strings | Just codes, no labels | On event objects |
| prestation-partenaire | `codeRome` string | Single code | On candidature |
| statistics APIs | `codeTypeActivite` = ROME + `codeActivite` | Statistical dimension | Also NAF, COMP, FORM14… |

**Type conflicts:**
- rome/appellation: sometimes separate objects, sometimes flat strings, sometimes just codes
- `libellé` vs `libelle` (accent typo in metiers-recherches-projets-evolution)
- ROME métier code format is consistent (letter + 4 digits, e.g. "K1302") across all APIs; appellation, compétence and contexte codes are numeric strings, and can be replaced over time (rome-4-0-substitutions)

### D. Compétence — skill/competency

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| rome-4-0-competences | `Competence` base type | code, libelle, type, transitionEcologique, transitionNumerique | Polymorphic: CompetenceDetaillee, MacroSavoirFaire, MacroSavoirEtreProfessionnel, Savoir |
| rome-4-0-competences | `DomaineCompetence` > `Enjeu` > `Objectif` > `MacroCompetence` | Full tree hierarchy | With RIASEC codes, maturité, ESCO mapping |
| rome-4-0-fiches-metiers, rome-4-0-metiers | Same types | Same as above | Copied into each file |
| romeo | `CompetenceRome` | libelleCompetence, codeCompetence, typeCompetence, scorePrediction | AI-predicted match |
| competences-professionnelles | `Competence` | code, libelle, type, niveau, complement… | The user's portfolio (read), with `Langue` and `CentreInteret` |
| ajout-competence | (inline, no schema) | `POST /competences` (renamed from `/competences/enregistrer` in 2026-10) | Writes to portefeuille de compétences |
| offres-emploi | `Competence` | code, libelle, exigence (E/S) | Flat, exigence-oriented — **completely different schema** |
| prestation-partenaire | `Competence` {codeCompetence, identifiantRendezVous, identifiantTechnique}, `DomaineCompetence` {code, libelle} | Skill assessed during a service appointment | Same names as ROME, different content |

**Type conflicts:**
- rome-4-0-competences `Competence` is a rich polymorphic type with inheritance
- offres-emploi `Competence` is a flat {code, libelle, exigence} — **same name, different structure**
- `Competence` is declared in 7 schemas (see §5)
- diagnostic-usager has `BesoinIndividuDto` which is conceptually different (a "need" vs a "skill") but plays a similar role in assessment

### E. Contrat / Type de contrat — employment contract

| API | Schema | Values | Notes |
|-----|--------|--------|-------|
| metiers-recherches-projets-evolution | `typeContrat` | code enum: CDI, CDD, DIN, MIS, SAI, LIB, CCE, FS, E2, PS | Full object with code/libelle/libelleLong |
| metiers-recherches (PE Connect) | `TypeContrat` | Same enum | Same structure |
| offres-emploi | `typeContrat` string + referential | "CDD", "CDI" etc. | Flat string on Offre + /referentiel/typesContrats |
| experiences-declarees-employeur | `Contrat` | natureContrat, dureeContrat + employer SIRET | Contracts declared by employers, not by the user |
| statut-usager | `Contrat` / `m_categ_inscription_code/lib` | "1"–"5" for inscription categories | **Different concept**: registration "contract" and category, not a job contract |
| contrat-engagement | (whole API) | — | **Different concept**: the mutual commitment contract of the loi plein emploi |

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
| la-bonne-boite | (search + results) | citycode (INSEE), latitude, longitude, distance |
| cadre-vie-communes | `Commune` | idinsee, nom, pop, gps [lat, lon]; nearby communes in `proxycom[]` {ncom, cp (integer), distance} |
| metiers-recherches-projets | `lieu` | code, Libelle, type (1=Pays, 2=Continent, 3=Région, 4=Département, 5=Commune) |
| evenements-france-travail | (inline) | ville, codePostal, codeInsee, longitude, latitude |
| orientation-usager (v1, v2) | `Adresse` | snake_case: numero_type_libelle_voie, code_postal, code_commune, libelle_commune |
| open-formation | `Adresse` | adresseLigne1–4, codePostal, codeINSEEcommune |
| synthese-pages-employeurs | `Adresse` | complementAdresse, numeroVoie, extensionNumeroVoie, libelleVoie, codePostal, libelleDistributionPostale |
| prestation-partenaire | `Adresse` | adresseLigne1–4, codeInsee, codePostal, ville, villePostale, identifiantAurore, typeLieu |
| rendez-vous-partenaires | `AdresseRDVU` | adresseLibre (freeform name), libelleAdresse (freeform address) |

**Key observations:**
- No two APIs share the same address schema; `Adresse` alone is declared in 5 schemas with 4 different structures
- Some use structured fields (numéro, voie, code postal), others use line-based (ligne1–4 or adresse1–4)
- GPS coordinates are present in: referentiel-agences (gpsLat/gpsLon), offres-emploi, evenements and la-bonne-boite (latitude/longitude), cadre-vie-communes (`gps` array)
- Code INSEE commune appears as: `codeINSEE`, `codeInseeCommune`, `codeInsee`, `commune`, `communeImplantation`, `communeInsee`, `idinsee`, `codeINSEEcommune`, `code_commune`, `citycode` — same data, 10 different field names

### G. Agence / Structure / Organisme — agency or organisation

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| referentiel-agences | `Agence` | code (Aurore), codeSafir, libelle, type, adresse, horaires, zoneCompetences | Canonical source, very detailed |
| offres-emploi | `Agence` | courriel, telephone | Contact agency of an offer — same name, different content |
| conclusions-entretiens | Flat strings | codeAgence, libelleAgence | Simple |
| diagnostic-usager | `AgentDto.structure` | string | Freeform |
| evenements-france-travail | `safir` (search filter) | 5-digit SAFIR code of the organising agency | Matches referentiel-agences `codeSafir` |
| rendez-vous-partenaires | `Organisme` | code (enum: IND/FT/CD/DCD/ML/CE), idStructure, libelleStructure | Network partner types |
| orientation-usager | `Structure` {code, libelle}; v2 adds `EntiteGeographiqueDto`, `OrganismeDto` | organisme codes FT/CD/ML/CAF/CE/IND | v2 names 4 roles an entity can hold |
| prestation-partenaire | Various | siteGestionnaire, siteRattachement (SAFIR codes) | Legacy naming |

**Organisme.code enum (rendez-vous) maps the employment network:**
- IND = Indépendant
- FT = France Travail
- CD = Conseil Départemental
- DCD = Délégataire du Conseil Départemental
- ML = Mission Locale
- CE = Cap Emploi

Orientation uses the same family of codes plus CAF, without DCD.

### H. Rendez-vous / Entretien — appointments & interviews

| API | Schema | Key properties | Notes |
|-----|--------|----------------|-------|
| rendez-vous-partenaires | `RendezVousPartenaire` | date, modaliteContact (VISIO/TELEPHONE/PHYSIQUE), motif (AUT/ACC/ORI), statut (PRIS/EFFECTUE/MODIFIE/ABSENT/ABSENT_EXC/ANNULE) | CRUD operations; ABSENT_EXC added 2026-10 |
| rendez-vous-partenaires | `RendezVousUsager` | Same + estEnConflit, historiqueEvenementList, dateAnnulation, motifAnnulation | Read-only aggregated view |
| conclusions-entretiens | `ConclusionEntretienPartenaireDetailsDto` | dateEntretien, typeEntretien (21 enum values), codeModaliteContact (8 enum values), commentaire | Read-only history |
| open-formation | `RendezVous` | Information sessions (ICO/RDVI) before a training | Same name, different context |
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
| orientation-usager | `etat` | string enum | BROUILLON, EN_ATTENTE, SAISIE_COMPLETE, OUVERT, CLOTURE, ABANDON — **orientation status** |
| declaration-demarche | `etat` | string enum | AC, RE, AN — **step status** |
| prestation-partenaire | `Candidature.statut` | string enum | TR, AN, AT, SS, EC, EA — **candidature processing status** |

These are entirely different status enums about different things (person
registration, detailed registration lifecycle, diagnostic project state,
orientation, job-search step, and service candidature processing).

### J. Salaire — salary

| API | Schema | Properties | Notes |
|-----|--------|------------|-------|
| offres-emploi | `Salaire` | libelle ("Mensuel de 1923.00 Euros sur 12 mois"), commentaire, complement1, complement2, listeComplements[] | Descriptive, text-oriented |
| metiers-recherches-projets-evolution | `salaire` | libelle (enum: Annuel/Mensuel/Cachet/Horaire/Autre), remuneration (double) | Structured, numeric |
| metiers-recherches (PE Connect) | `Salaire` | remuneration (double), libelle, code | Structured |
| marche-travail | Via statistical indicators (SAL_3) | valeurPrincipaleMontant (double) | Aggregate statistics only |

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
| open-formation | (formation identified by its InterCarif triplet) | Information sessions and application slots | Training offer, not a record or a requirement |
| evenements-france-travail | `diplomes` array of strings | Diploma level labels | On event listings |

**Same name `Formation`, different schemas**: user's training record vs. job
requirement. Different fields entirely.

### M. Entreprise / Établissement — employers

| API | Representation | Notes |
|-----|---------------|-------|
| la-bonne-boite | siret + company data | Companies likely to hire |
| je-recrute-avec-ftpro | `EntrepriseES` {siret} | SIRET only (14 characters) |
| experiences-declarees-employeur | `Entreprise` | Employer of a declared contract |
| offres-emploi | `Entreprise` | Employer of an offer — same name, different content |
| synthese-pages-employeurs | `Etablissement` | Employer branding pages |
| prestation-partenaire | `Etablissement` {siret, raisonSociale, enseigne, numeroRCE…} | Recruiting establishment — same name, different content |
| evenements-france-travail | `intervenants[]` {raisonSociale, siret, urlEntreprise}; `sirets` filter (SIREN and/or SIRET) | Companies taking part in an event (added 2026-10) |

---

## 4. Statistical APIs — shared framework

Four APIs share an **identical** internal schema framework (the "Smart Emploi"
referential):

- **marche-travail.json** — Labour market indicators (DE counts, offers, hires, tensions, salaries)
- **acces-emploi-demandeurs-emploi.json** — Employment access rates
- **sortants-formation-acces-emploi.json** — Training exit outcomes
- **informations-territoire.json** — Territory profile (population, establishments, employees, DYN_1)

All four use the same schema set:

```
CritereIndicateurAvecNomenclature / CritereIndicateurSansNomenclature
  → Caracteristique

IndicateurRetour
  → ValeursParPeriode
    → ValeursParCaracteristique

Referential schemas (identical across all 4):
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
the four OpenAPI files.

**v1.1 changes (2026-10 refresh):**
- `CritereIndicateurAvecNomenclature` gains `profilDemandeur` (e.g. `JEUNES`),
  required by the new per-profile indicators — DE_8 and EMB_8 (marche-travail),
  ACC_8 (acces-emploi) — with the nomenclature `PROF_SPECxCATCAND`.
- `ValeursParPeriode` gains `valeurPrincipaleDecimale` (double).
- marche-travail dropped DYN_1 (still served by informations-territoire) and the
  referentials `indicateurs`, `familles-indicateurs`, `famille-indicateur/{code}`
  and `territoires-communes/{type}`.

---

## 5. Naming inconsistencies

### Field name variations for the same data

| Real-world thing | Variations found |
|-----------------|-----------------|
| Code INSEE commune | `codeINSEE`, `codeInseeCommune`, `codeInsee`, `commune`, `communeImplantation`, `communeInsee`, `idinsee`, `codeINSEEcommune`, `code_commune`, `citycode` |
| Code postal | `codePostal` (most), `code_postal` (orientation), `cp` (cadre-vie-communes, as an integer) |
| Identifiant | `id`, `identifiant`, `identifiantCandidature`, `idDiagnostic`, `idOrigine`, `idRCE`, `idObjetMetier` |
| Numéro France Travail | `numeroFranceTravail` (most), `referenceExterne` (FT Connect), implicit via jeton (some) |
| Date de mise à jour | `dateMiseAJour`, `datMaj`, `dateModification`, `dateActualisation`, `updated_at`, `lastModifiedDate` |

### Schema name collisions (same name, different structure)

Computed across all 44 files (orientation v1/v2 and the four statistics APIs
reuse their own schemas on purpose and are left out).

| Name | APIs | Difference |
|------|------|------------|
| `Competence` | rome-4-0-competences / -fiches-metiers / -metiers, romeo, offres-emploi, competences-professionnelles, prestation-partenaire | Rich polymorphic type vs. flat {code,libelle,exigence} vs. portfolio entry vs. skill assessed in a service appointment |
| `Adresse` | open-formation, orientation-usager (v1, v2), prestation-partenaire, synthese-pages-employeurs | Four different field sets |
| `Commune` | offres-emploi, prestation-partenaire, cadre-vie-communes | {code,libelle,codePostal,codeDepartement} vs. {codeCommune,libelle,libellePostal,codePostal,codeDepartement} vs. amenities record |
| `Contrat` | statut-usager, metiers-recherches, experiences-declarees-employeur | Registration record vs. contract wish vs. declared job contract |
| `Structure` | orientation-usager (v1, v2), contrat-engagement | Agency {code, libelle} vs. the layout of the contract (its `engagements`) |
| `Activite` | statistics APIs, gestion-activites-operationnelles | Statistical dimension vs. operational task |
| `Evenement` | evenements-france-travail, gestion-sanctions-rsa | Employment event vs. sanction lifecycle step |
| `Entreprise` | offres-emploi, experiences-declarees-employeur | Offer employer vs. contract employer |
| `Etablissement` | synthese-pages-employeurs, prestation-partenaire | Employer page establishment vs. recruiting establishment |
| `Agence` | referentiel-agences, offres-emploi | Full agency record vs. offer contact |
| `Offre` | offres-emploi, prestation-partenaire | Full job offer vs. reference to one (idOffre, codeOffreDune) |
| `RendezVous` | open-formation, prestation-partenaire | Information session vs. service appointment |
| `Rome` | metiers-recherches, prestation-partenaire | {code,libelle} vs. {codeRome,libelle} |
| `Langue`, `CentreInteret` | competences-professionnelles, offres-emploi / rome-4-0-metiers | Portfolio entry vs. offer requirement / job metadata |
| `DomaineCompetence` | rome-4-0-competences, prestation-partenaire | Competency tree level vs. flat {code, libelle} |
| `Formation` | formations-professionnelles, offres-emploi | User's training history vs. job requirement |
| `Permis` | formations-professionnelles, offres-emploi | {code,libelle} vs. {libelle,exigence} |
| `Salaire` | offres-emploi, metiers-recherches | Descriptive text vs. structured numeric |
| `Individu` | gestion-sanctions-rsa, prestation-partenaire | Minimal (1 field) vs. rich (12+ fields) |

### Enum naming patterns

Most APIs use SCREAMING_SNAKE_CASE for enum values:
`EN_COURS`, `NON_ABORDEE`, `POINT_FORT`, `MACRO-SAVOIR-FAIRE`

Exceptions:
- statut-usager uses French words with accents: `"Identifié"`, `"Inscrit"`, `"Cessé"`, `"Radié"`
- statut uses numeric strings: `"0"`, `"1"`
- formations-professionnelles uses short codes for niveaux: `"NV1"`, `"C3A"`, `"AFS"`
- gestion-sanctions-rsa uses coded natures: `N23`…`N31` (défauts), `N61`…`N65` (manquements)

### Field naming conventions

Most agent-realm APIs use camelCase: `dateExploration`, `codeRome`, `nomMetier`

Exceptions:
- statut-usager uses m_ prefix Hungarian notation: `m_statut`, `m_date_effet_statut`, `m_duree_inscription_12`
- france-travail-connect uses OIDC snake_case: `family_name`, `given_name`, `updated_at`
- orientation-usager uses snake_case: `etat_decision`, `code_commune`, `motif_reorientation`
- cadre-vie-communes uses short lowercase keys (`cp`, `ncom`, `idinsee`, `pop`) and category names with spaces and accents as keys (`"Services publics"`, `"Éducation"`, `"Santé"`)
- Some metiers-recherches-projets-evolution fields have accent in key: `libellé`

---

## 6. API families

The documentation and the catalogue group the APIs into nine families (source
of truth: `GROUPS` and `GROUP_DEFS` in `build-catalogue.ts`; the order below is
the catalogue order):

1. **Dossier usager** — agent access to a job seeker's file via jeton usager:
   rechercher-usager (entry point), informations-administratives-usager,
   statut-usager, diagnostic-usager, conclusions-entretiens,
   metiers-recherches-projets-evolution.
2. **Parcours d'accompagnement** — the loi plein emploi journey: orientation-usager
   (v1, v2), contrat-engagement, rendez-vous-partenaires, declaration-demarche,
   gestion-sanctions-rsa.
3. **Connexion & identité** — France Travail Connect and the connected user's
   identity, status and benefits: france-travail-connect, coordonnees,
   date-naissance, statut, pe-connect-indemnisations.
4. **Profil de compétences** — the user's portfolio: experiences-professionnelles,
   experiences-declarees-employeur, competences-professionnelles,
   formations-professionnelles, metiers-recherches, ajout-competence.
5. **Offres & recrutement** — offres-emploi, la-bonne-boite, jcmo-controle-offre,
   synthese-pages-employeurs, je-recrute-avec-ftpro.
6. **ROME 4.0** — rome-4-0-metiers, rome-4-0-fiches-metiers, rome-4-0-competences,
   rome-4-0-contextes-travail, rome-4-0-substitutions, romeo.
7. **Statistiques** — marche-travail, acces-emploi-demandeurs-emploi,
   sortants-formation-acces-emploi, informations-territoire.
8. **Gestion partenaire** — prestation-partenaire, gestion-activites-operationnelles.
9. **Référentiels & services** — referentiel-agences, cadre-vie-communes,
   open-formation, evenements-france-travail.
