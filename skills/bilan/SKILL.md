---
name: bilan
description: This skill should be used when the user invokes /bilan, asks to "faire un bilan patrimonial", "préparer la trame de bilan pour [client]", "structurer le patrimoine de [client]", "générer un bilan", or needs a patrimonial assessment framework or structured template for a client. Combines with profil-client for personalization. For deep analytical diagnosis, use analyste-patrimonial agent instead.
---

# Bilan Patrimonial — Trame et Structuration

Ce skill génère des trames de bilan patrimonial structurées, pré-remplies avec les informations disponibles dans la conversation. Le diagnostic final reste du ressort du CGP.

## Principe

Le bilan patrimonial est un outil de diagnostic global — il collecte, structure et présente la situation d'un client pour permettre au CGP de formuler ses recommandations. Ce skill génère la trame ; l'agent `analyste-patrimonial` fournit l'analyse approfondie si nécessaire.

## Processus

1. **Extraire** toutes les informations client disponibles dans la conversation
2. **Pré-remplir** la trame avec les données connues, marquer `[À compléter]` pour les champs manquants
3. **Signaler** en fin de document les informations manquantes importantes
4. **Proposer** de lancer `analyste-patrimonial` si une analyse approfondie est souhaitée

## Format standard du bilan patrimonial

```
════════════════════════════════════════════════
BILAN PATRIMONIAL — [Prénom NOM]
Établi par : [Nom CGP]      Date : [JJ/MM/AAAA]
════════════════════════════════════════════════

I. SITUATION PERSONNELLE ET FAMILIALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nom / Prénom       : [Nom Prénom]
Date de naissance  : [JJ/MM/AAAA] ([X] ans)
Situation familiale: [Marié(e) / Pacsé(e) / Célibataire / Divorcé(e)]
Régime matrimonial : [Communauté légale / Séparation de biens / N/A]
Enfants            : [Nombre — Âges]
Profession         : [Intitulé]
Statut             : [Salarié / TNS / Fonctionnaire / Retraité]

II. SITUATION FINANCIÈRE
━━━━━━━━━━━━━━━━━━━━━━━━

Revenus nets annuels (foyer) : [X €]
TMI estimée                  : [X%]
Capacité d'épargne mensuelle : [X €]
Épargne de précaution        : [X €]

III. ACTIF PATRIMONIAL
━━━━━━━━━━━━━━━━━━━━━━

A. Immobilier
┌─────────────────────────────────────────────────────────────┐
│ Bien                  │ Valeur estimée │ Crédit restant │ Net │
├─────────────────────────────────────────────────────────────┤
│ Résidence principale  │ [X €]          │ [X €]          │ [X]│
│ [Bien locatif]        │ [X €]          │ [X €]          │ [X]│
│ TOTAL IMMOBILIER      │ [X €]          │ [X €]          │ [X]│
└─────────────────────────────────────────────────────────────┘

B. Placements financiers
┌──────────────────────────────────────────────┐
│ Enveloppe        │ Valeur    │ Observations  │
├──────────────────────────────────────────────┤
│ PEA              │ [X €]     │               │
│ Assurance-vie    │ [X €]     │               │
│ PER              │ [X €]     │               │
│ CTO              │ [X €]     │               │
│ Livrets          │ [X €]     │               │
│ Épargne salariale│ [X €]     │               │
│ TOTAL FINANCIER  │ [X €]     │               │
└──────────────────────────────────────────────┘

C. Autres actifs
┌──────────────────────────────────────────────┐
│ Actif             │ Valeur   │ Observations  │
├──────────────────────────────────────────────┤
│ Parts sociales    │ [X €]    │               │
│ Autres            │ [X €]    │               │
└──────────────────────────────────────────────┘

TOTAL ACTIF BRUT      : [X €]
TOTAL DETTES          : [X €]
━━━━━━━━━━━━━━━━━━━━━━
PATRIMOINE NET ESTIMÉ : [X €]

IV. PROFIL INVESTISSEUR
━━━━━━━━━━━━━━━━━━━━━━━

Profil déclaré         : [Prudent / Équilibré / Dynamique / Offensif]
Horizon d'investissement: [X ans]
Tolérance aux pertes   : [X% max acceptable]
Expérience financière  : [Débutante / Intermédiaire / Avancée]
Objectif principal     : [Retraite / Transmission / Capital / Défiscalisation]

V. SITUATION FISCALE
━━━━━━━━━━━━━━━━━━━

IFI                    : [Oui / Non]
Revenus fonciers       : [Oui ([X €/an]) / Non]
Dispositifs actifs     : [Pinel / Malraux / Déficit foncier / Aucun]

VI. RÉPARTITION PATRIMONIALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immobilier    : [X%] ([X €])
Financier     : [X%] ([X €])
Autres        : [X%] ([X €])

VII. POINTS D'ATTENTION
━━━━━━━━━━━━━━━━━━━━━━━

- [Point identifié 1]
- [Point identifié 2]

VIII. INFORMATIONS MANQUANTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Information manquante 1]
- [Information manquante 2]

════════════════════════════════════════════════
*Document de travail interne — confidentiel*
*Établi sur la base des informations transmises par le client.*
════════════════════════════════════════════════
```

## Ressources complémentaires

- **`assets/template-bilan-vierge.md`** — Trame vierge à remplir manuellement
- **`profil-client/assets/template-profil.md`** — Template profil complet complémentaire
