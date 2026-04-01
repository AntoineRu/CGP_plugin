---
name: reporting
description: This skill should be used when the user invokes /reporting, asks to "préparer un reporting client", "lettre de suivi de portefeuille", "bilan trimestriel pour [client]", "rapport de performance", "tableau de bord client", or needs any periodic client reporting document — portfolio review letters, performance summaries, or periodic follow-up communications. Combine with cgp-persona and profil-client. For the actual drafting, the redacteur-cgp agent can be used.
---

# Reporting — Suivi et Communication Périodique Client

Ce skill gouverne la production de documents de reporting périodique : lettres de suivi, bilans de performance, tableaux de bord patrimoniaux.

## Types de reporting

### 1. Lettre de suivi de portefeuille
**Fréquence :** Trimestrielle ou semestrielle.
**Usage :** Informer le client de l'évolution de ses placements, rassurer, maintenir le lien.

**Format :**
```
[Ville], le [date]

[Prénom NOM Client]

Objet : Suivi de votre portefeuille — [Période : T1 2025 / S1 2025 / etc.]

Madame / Monsieur [Nom],

**Contexte de marché**
[2-3 phrases sur le contexte économique et financier de la période — neutre et factuel]

**Évolution de votre portefeuille**
[Tableau ou liste des positions avec valeur de début de période, fin de période, évolution en % et en €]

| Enveloppe       | Valeur début | Valeur fin | Évolution |
|---|---|---|---|
| PEA             | [X €]        | [X €]      | [+/-X%]   |
| Assurance-vie   | [X €]        | [X €]      | [+/-X%]   |
| PER             | [X €]        | [X €]      | [+/-X%]   |
| **TOTAL**       | [X €]        | [X €]      | [+/-X%]   |

**Analyse**
[2-3 phrases : ce qui explique l'évolution, ce qui est conforme aux objectifs, ce qui mérite attention]

**Recommandations / Actions envisagées**
- [Action 1 ou "Aucun arbitrage nécessaire à ce stade"]

**Prochaine étape**
[Proposition de rendez-vous ou de point téléphonique]

Bien cordialement,
[Prénom NOM CGP]
[Coordonnées]

---
*Les performances passées ne préjugent pas des performances futures. Ce document est établi à titre informatif sur la base des informations disponibles à la date de rédaction.*
```

---

### 2. Tableau de bord patrimonial annuel
**Usage :** Bilan complet en fin ou début d'année, base pour les recommandations annuelles.

**Structure :**
1. Synthèse patrimoniale (valeurs globales vs N-1)
2. Performance par enveloppe
3. Répartition actuelle vs cible
4. Actions réalisées dans l'année
5. Recommandations pour l'année à venir

---

### 3. Note de performance sur un investissement
**Usage :** Suivi spécifique d'un produit (SCPI, fonds, PER) suite à une souscription.

**Format court :**
```
**[Produit] — Point de situation au [date]**

Souscription : [X €] le [date]
Valeur actuelle : [X €]
Performance depuis souscription : [+/-X% / [X €]]
Distribution reçue (si SCPI) : [X €]

Observations : [1-2 phrases factuelles]
```

---

## Règles du reporting

- **Factuel et neutre** : présenter les faits sans sur-interpréter les performances
- **Contextualiser** : une baisse de -5% en période de marché à -10% est en réalité une surperformance
- **Jamais de projection** de performance future dans un document de suivi
- **Toujours proposer une action** ou une prochaine étape concrète
- **Données à date** : préciser toujours la date de valorisation des actifs

## Ressources complémentaires

- **`assets/template-reporting-trimestriel.md`** — Template prêt à personnaliser
- **`references/contexte-marche-formules.md`** — Formulations standards pour décrire les contextes de marché sans prendre position
