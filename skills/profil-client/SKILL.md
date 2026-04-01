---
name: profil-client
description: This skill should be used when the user provides client information before any task, or when asked to "créer un profil client", "structurer les informations d'un client", "préparer le dossier de [nom]", "renseigner le profil de [nom]", or when client details are mentioned (name, age, family situation, assets, objectives). Always load this skill to structure client context before drafting documents, preparing meetings, or generating analyses for a specific client.
---

# Profil Client — Structuration et Collecte

Ce skill permet de structurer les informations d'un client CGP pour contextualiser toute tâche ultérieure (rédaction de documents, préparation de rendez-vous, analyse patrimoniale, etc.).

## Principe de fonctionnement

À chaque fois que des informations client sont fournies dans la conversation :
1. Extraire et structurer les données dans le format standard ci-dessous
2. Identifier les informations manquantes importantes
3. Utiliser ce profil structuré comme contexte pour toutes les tâches suivantes dans la conversation

## Format Standard du Profil Client

```
## Profil Client — [Prénom NOM]

### Situation personnelle
- Âge : [X ans]
- Situation familiale : [Célibataire / Marié(e) / Pacsé(e) / Divorcé(e) / Veuf(ve)]
- Régime matrimonial : [Communauté légale / Séparation de biens / Participation aux acquêts / N/A]
- Enfants : [Nombre, âges]
- Profession : [Intitulé]
- Statut : [Salarié / TNS / Fonctionnaire / Retraité / Autre]

### Situation financière
- Revenus annuels nets : [X €] (foyer fiscal)
- TMI estimée : [0% / 11% / 30% / 41% / 45%]
- Charges fixes mensuelles : [X €]
- Capacité d'épargne mensuelle : [X €]
- Épargne de précaution disponible : [X €]

### Patrimoine actuel
- Résidence principale : [Propriétaire (valeur estimée X €) / Locataire]
- Immobilier locatif : [Oui (X €) / Non]
- Placements financiers : [PEA X € / AV X € / CTO X € / Livrets X € / PER X €]
- Épargne salariale : [X €]
- Autres actifs : [Entreprise, parts sociales, etc.]
- Dettes / crédits en cours : [X € (type, durée restante)]

### Objectifs patrimoniaux
- Objectif principal : [Retraite / Transmission / Constitution de capital / Défiscalisation / Autre]
- Horizon d'investissement : [Court terme < 3 ans / Moyen terme 3–8 ans / Long terme > 8 ans]
- Objectifs secondaires : [liste]

### Profil investisseur
- Profil déclaré : [Prudent / Équilibré / Dynamique / Offensif]
- Tolérance aux pertes : [X% de perte acceptable]
- Expérience financière : [Débutant / Intermédiaire / Averti]
- Points de sensibilité : [ex. aversion aux marchés actions, préférence immobilier, etc.]

### Situation fiscale
- IFI : [Oui (patrimoine estimé X €) / Non]
- Revenus fonciers : [Oui (X € / an) / Non]
- Dispositifs actifs : [Pinel, Malraux, déficit foncier, etc.]

### Notes et particularités
- [Événements de vie prévus : départ à la retraite dans X ans, héritage attendu, etc.]
- [Contraintes particulières : divorce en cours, problèmes de santé, etc.]
- [Préférences personnelles : investissement responsable (ISR), refus secteurs, etc.]
```

## Règles d'utilisation

### Informations manquantes
Signaler les champs importants manquants, mais ne pas bloquer la tâche :
- **Critique** (TMI, profil investisseur, objectif principal) → mentionner explicitement avant d'avancer
- **Utile** (patrimoine détaillé) → noter "non renseigné", utiliser des hypothèses raisonnables
- **Contextuel** (préférences personnelles) → facultatif, enrichit le conseil

### Hypothèses par défaut si données insuffisantes
Si certaines données sont manquantes et que la tâche doit continuer :
- Mentionner les hypothèses retenues au début du document
- Ex. : *"En l'absence d'information sur la TMI, l'analyse ci-dessous retient une tranche à 30%."*

### Confidentialité
- Ne jamais répéter inutilement les données personnelles dans les documents finaux
- Dans les documents destinés aux clients, utiliser "Madame/Monsieur [Nom]" et non les données brutes

## Intégration avec les autres skills

Le profil structuré sert de contexte pour :
- **`cgp-persona`** → adapter le registre de communication au profil
- **Rédaction de documents** → personnaliser lettres et rapports
- **Préparation de rendez-vous** → cibler les points à aborder
- **Matching produit** → filtrer les produits adaptés au profil
- **Bilan patrimonial** → pré-remplir la trame

## Ressources complémentaires

- **`references/questions-profil.md`** — Questions complètes pour collecter le profil en rendez-vous
- **`assets/template-profil.md`** — Template vierge à remplir pour un nouveau client
