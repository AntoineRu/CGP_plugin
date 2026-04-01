---
name: analyser
description: This skill should be used when the user invokes /analyser, asks to "comparer", "analyser un produit", "quel produit pour ce client", "PEA ou PER", "SCPI ou assurance-vie", "est-ce que ce produit convient à [client]", "fiche produit", "analyse de suitability", "adéquation produit profil", or needs any financial product comparison, analysis, or suitability assessment. Always combine with cgp-persona for compliance. Use profil-client if client context is available.
---

# Analyser — Produits Financiers et Adéquation

Ce skill gouverne l'analyse de produits financiers : comparatifs, fiches synthèse, et adéquation produit/profil client (suitability MIF II).

## Types d'analyses et processus

### Type 1 — Comparatif entre produits
**Déclencheur :** "PEA ou AV ?", "comparer PER et assurance-vie", "SCPI vs immobilier direct"

**Processus :**
1. Identifier les produits à comparer
2. Si un profil client est disponible, orienter le comparatif vers sa situation
3. Produire un tableau comparatif sur les critères pertinents
4. Conclure avec une recommandation contextuelle

**Critères standards de comparaison :**
- Fiscalité (entrée, en cours, sortie)
- Liquidité et disponibilité des fonds
- Plafond de versement
- Supports d'investissement disponibles
- Avantage successoral
- Adapté à quel profil / horizon

---

### Type 2 — Fiche synthèse d'un produit
**Déclencheur :** "fiche sur le PER", "explique-moi les SCPI", "c'est quoi un PEA-PME"

**Format de sortie :**
```
# [Nom du produit]

**En une phrase :** [Définition simple]

## Points clés
- **Fiscalité :** [Résumé]
- **Plafond :** [Montant]
- **Liquidité :** [Bonne / Limitée / Bloquée jusqu'à X]
- **Supports :** [Types d'actifs accessibles]
- **Succession :** [Traitement]

## Pour qui ?
[Profil d'investisseur idéal en 2-3 critères]

## Points de vigilance
- [Risque ou contrainte 1]
- [Risque ou contrainte 2]

⚠️ *Les données fiscales sont indicatives et basées sur la législation en vigueur à la date de l'analyse. À valider avec les sources officielles.*
```

---

### Type 3 — Analyse d'adéquation (suitability)
**Déclencheur :** "est-ce que [produit] convient à [client]", "quel produit pour [situation]", "matching produit/profil"

**Processus :**
1. Récupérer le profil client depuis la conversation (ou demander les éléments clés)
2. Identifier les contraintes du profil : TMI, horizon, tolérance au risque, liquidité, objectif
3. Évaluer le produit proposé sur chaque contrainte
4. Produire le verdict d'adéquation avec justification

**Format de sortie :**
```
# Analyse d'adéquation — [Produit] pour [Client]

## Profil de référence
- TMI : [X%]
- Horizon : [X ans]
- Profil risque : [Prudent / Équilibré / Dynamique]
- Objectif : [X]
- Liquidité requise : [Oui / Non / Partielle]

## Évaluation

| Critère | Exigence client | Produit | Adéquation |
|---|---|---|---|
| Fiscalité | [Besoin] | [Ce que offre le produit] | ✅ / ⚠️ / ❌ |
| Liquidité | [Besoin] | [Contraintes du produit] | ✅ / ⚠️ / ❌ |
| Horizon | [X ans] | [Horizon recommandé] | ✅ / ⚠️ / ❌ |
| Risque | [Profil] | [Niveau de risque] | ✅ / ⚠️ / ❌ |
| Objectif | [X] | [Adapté ou non] | ✅ / ⚠️ / ❌ |

## Verdict

**[✅ Adéquat / ⚠️ Partiellement adéquat / ❌ Non adapté]**

[Justification en 3-5 lignes : pourquoi ce produit convient ou non, et dans quelles conditions]

## Recommandation CGP

[Ce que le CGP devrait faire : proposer tel montant, combiner avec tel autre produit, ou écarter et proposer une alternative]

---
⚠️ *Cette analyse est réalisée sur la base des informations transmises. La décision finale d'investissement appartient au CGP après validation du profil complet du client (questionnaire MIF II).*
```

---

### Type 4 — Analyse d'une situation patrimoniale
**Déclencheur :** "analyse la situation de [client]", "qu'est-ce qu'on peut optimiser pour [client]", "diagnostic patrimonial rapide"

**Processus :**
1. Récupérer le profil structuré du client
2. Identifier les forces (bonne diversification, enveloppes bien utilisées, etc.)
3. Identifier les axes d'optimisation (fiscalité, liquidité, succession, risque)
4. Proposer 2-3 pistes prioritaires avec justification

Pour ce type d'analyse complexe et longue → déléguer à l'agent `analyste-patrimonial`.

---

## Règles de l'analyse

- **Toujours ancrer dans le profil client** quand il est disponible — une analyse générique a moins de valeur
- **Jamais de recommandation sans mention des risques** correspondants
- **Toujours mentionner la source ou la date** pour les données chiffrées (taux, plafonds)
- Pour les données détaillées sur les produits → consulter **`cgp-persona/references/produits-financiers.md`**

## Ressources complémentaires

- **`references/grilles-comparaison.md`** — Grilles de comparaison pré-remplies pour les paires les plus fréquentes
- **`cgp-persona/references/produits-financiers.md`** — Données de référence sur tous les produits (plafonds, fiscalité, barèmes)
