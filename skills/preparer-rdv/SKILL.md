---
name: preparer-rdv
description: This skill should be used when the user invokes /rdv, asks to "préparer un rendez-vous", "préparer ma réunion avec [client]", "préparer le RDV de [nom]", "que dois-je aborder avec [client]", "ordre du jour pour [client]", or needs to prepare for a client meeting. Always combine with cgp-persona and profil-client skills when client information is available.
---

# Préparer un Rendez-Vous Client

Ce skill génère une préparation complète de rendez-vous CGP : ordre du jour, points clés, objections anticipées, questions à poser et documents à rassembler.

## Processus de préparation

### Étape 1 — Collecter le contexte
Avant de générer quoi que ce soit, identifier :
- **Qui** : nom du client, profil si disponible dans la conversation
- **Quoi** : objet principal du rendez-vous (bilan annuel, présentation produit, suivi, succession, etc.)
- **Quand** : date/heure si précisée (pour ancrer les actualités marchés pertinentes)
- **Où en est le client** : nouvelles depuis le dernier RDV si mentionnées

Si des informations manquent et sont importantes pour la préparation, poser une seule question groupée avant de générer.

### Étape 2 — Générer la préparation

Produire le document de préparation complet en utilisant le format standard ci-dessous.

### Étape 3 — Proposer les documents
En fin de sortie, lister les documents à rassembler avant le rendez-vous.

## Format de sortie standard

```
# Préparation RDV — [Prénom NOM] | [Date]
**Objet :** [Intitulé de la réunion]
**Durée estimée :** [X minutes]

---

## Ordre du jour

1. [Point 1 — durée estimée]
2. [Point 2 — durée estimée]
3. [Point 3 — durée estimée]
4. Points divers / questions du client

---

## Points clés à aborder

### [Thème 1]
- [Sous-point concret]
- [Sous-point concret]
→ **Objectif :** [Ce que le CGP veut accomplir sur ce point]

### [Thème 2]
- [Sous-point concret]
→ **Objectif :** [Ce que le CGP veut accomplir sur ce point]

---

## Objections probables et réponses préparées

| Objection client | Réponse recommandée |
|---|---|
| [Objection 1] | [Réponse concise et professionnelle] |
| [Objection 2] | [Réponse concise et professionnelle] |

---

## Questions à poser au client

- [Question ouverte pour qualifier les besoins]
- [Question sur l'évolution de la situation personnelle]
- [Question sur la satisfaction / feedback]
- [Question sur les projets à venir]

---

## Documents à préparer

- [ ] [Document 1]
- [ ] [Document 2]
- [ ] [Document 3]

---

## Points de vigilance

> [Rappel de conformité si pertinent, point sensible du dossier, ou événement de marché à mentionner]
```

## Adaptation selon le type de rendez-vous

### Bilan annuel / Bilan patrimonial
- Inclure une revue des performances de l'année
- Aborder l'évolution de la situation personnelle (revenus, famille, projets)
- Proposer des ajustements si nécessaire
- Évoquer les actualités fiscales impactantes

### Présentation d'un produit / Recommandation
- Expliquer pourquoi ce produit correspond au profil du client
- Préparer le DIC / DICI à remettre
- Anticiper les questions sur les risques et la liquidité
- Avoir une alternative en cas de refus

### Suivi de portefeuille
- Rappeler les objectifs initiaux
- Comparer les performances réelles aux attentes
- Identifier les écarts et les expliquer
- Proposer des ajustements si l'horizon ou la situation a changé

### Premier rendez-vous (prospect)
- Se concentrer sur l'écoute : poser des questions ouvertes
- Ne pas proposer de solutions dès le premier RDV
- Expliquer le processus et les étapes
- Collecter le maximum d'informations pour le profil

### Succession / Transmission
- Vérifier l'état civil et le régime matrimonial
- Rappeler les abattements disponibles (100k€ tous les 15 ans)
- Évoquer les outils : donation, démembrement, assurance-vie
- Signaler la nécessité d'un notaire pour les actes

## Ressources complémentaires

- **`references/objections-courantes.md`** — Banque d'objections fréquentes et réponses par thème
- **`assets/template-rdv-vierge.md`** — Template de préparation RDV à remplir manuellement
