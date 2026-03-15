#!/bin/bash
# APIs with known page IDs from the catalogue
declare -A apis
apis[84]="offres-emploi"
apis[231]="sortants-formation-acces-emploi"
apis[465]="rechercher-usager"
apis[515]="conclusions-entretiens"
apis[116]="experiences-professionnelles"
apis[452]="metiers-recherches-projets-evolution"
apis[107]="referentiel-agences"
apis[272]="rome-4-0-fiches-metiers"
apis[366]="romeo"
apis[90]="anotea"
apis[233]="marche-travail"
apis[234]="acces-emploi-demandeurs-emploi"
apis[51]="france-travail-connect"
apis[92]="coordonnees"
apis[93]="formations-professionnelles"
apis[115]="metiers-recherches"
apis[103]="evenements-france-travail"
apis[270]="rome-4-0-competences"
apis[271]="rome-4-0-contextes-travail"
apis[279]="jcmo-controle-offre"
apis[135]="statut"
apis[99]="date-naissance"
apis[320]="ajout-competence"
apis[449]="informations-administratives-usager"
apis[466]="statut-usager"
apis[477]="diagnostic-usager"
apis[497]="gestion-sanctions-rsa"
apis[416]="rendez-vous-partenaires"
apis[561]="synthese-pages-employeurs"
apis[260]="prestation-partenaire"
# APIs without swagger metadata but still worth trying
apis[560]="emploi-store"
apis[564]="evenements-emploi-espace-conseiller"
apis[461]="suivi-parcours"
apis[491]="recherche-opportunites-emploi-alternance"
apis[493]="depot-offres-emploi-alternance"
apis[492]="envoi-candidature-alternance"
apis[483]="engagement"
apis[428]="marche-inclusion"
apis[426]="datainclusion"
apis[464]="hub-donnees-agora"
apis[479]="activites-pilotage-partenaires"
apis[482]="academie-france-travail"
apis[502]="tableau-bord-reseau-emploi"
apis[562]="service-geocodage"
apis[462]="semafor"

for id in "${!apis[@]}"; do
  name="${apis[$id]}"
  code=$(curl -s -o "${name}.json" -w "%{http_code}" "https://francetravail.io/api-peio/v2/api/${id}/openapi")
  if [ "$code" = "200" ]; then
    # Check if it's valid JSON
    if python3 -c "import json; json.load(open('${name}.json'))" 2>/dev/null; then
      size=$(wc -c < "${name}.json" | tr -d ' ')
      echo "OK  ${id}  ${name}  ${size}b"
    else
      echo "BADJSON  ${id}  ${name}"
      rm -f "${name}.json"
    fi
  else
    echo "FAIL(${code})  ${id}  ${name}"
    rm -f "${name}.json"
  fi
done
