# CGP Assistant — Plugin Claude Code

Plugin [Claude Code](https://claude.ai/code) conçu pour les **Conseillers en Gestion de Patrimoine (CGP)** français. Il automatise les tâches rédactionnelles et analytiques du quotidien : préparation de rendez-vous, rédaction de documents clients, analyse de produits financiers, veille réglementaire et fiscale.

> **Gain de temps estimé : 19–38 heures par semaine** sur les tâches rédactionnelles et analytiques.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Commandes disponibles](#commandes-disponibles)
- [Architecture du plugin](#architecture-du-plugin)
- [Mise à jour](#mise-à-jour)
- [Avertissement réglementaire](#avertissement-réglementaire)

---

## Fonctionnalités

| Commande | Description | Gain estimé |
|---|---|---|
| `/rdv` | Prépare un rendez-vous client (ordre du jour, objections, questions) | 1–2h/sem |
| `/rediger` | Rédige tout document CGP (lettre de mission, rapport, compte-rendu…) | 3–6h/sem |
| `/analyser` | Compare des produits financiers et évalue leur adéquation au profil client | 4–7h/sem |
| `/veille` | Synthèse réglementaire et fiscale avec recherche web en temps réel | 2–4h/sem |
| `/bilan` | Génère une trame de bilan patrimonial pré-remplie | 2–4h/sem |
| `/vulgariser` | Traduit un concept financier en langage simple pour un client | 1–2h/sem |
| `/marketing` | Rédige posts LinkedIn, newsletters, articles de blog | 1–3h/sem |
| `/reporting` | Prépare les lettres de suivi et bilans périodiques clients | 2–3h/sem |
| `/prospecter` | Génère emails de prospection, scripts d'appel, messages LinkedIn | 1–2h/sem |

**3 agents spécialisés** travaillent en autonomie sur les tâches complexes :
- `redacteur-cgp` — rédaction longue avec conformité AMF/MIF II automatique
- `analyste-patrimonial` — diagnostic patrimonial complet sur 5 dimensions
- `veilleur-fiscal` — recherche web sur les actualités réglementaires et fiscales

---

## Prérequis

- [Claude Code](https://claude.ai/code) installé et configuré
- Un abonnement Claude actif (Claude.ai Pro ou API)

---

## Installation

### Étape 1 — Cloner le repository

```bash
git clone https://github.com/AntoineRu/CGP_plugin.git
cd CGP_plugin
```

### Étape 2 — Créer le marketplace local

Dans le dossier **parent** du repository cloné, créez le fichier `.claude-plugin/marketplace.json` :

```bash
mkdir -p ../.claude-plugin
```

Contenu du fichier `../.claude-plugin/marketplace.json` :

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "cgp-local",
  "description": "Plugin CGP Assistant local",
  "owner": { "name": "Votre nom" },
  "plugins": [
    {
      "name": "cgp-assistant",
      "description": "Assistant IA pour Conseillers en Gestion de Patrimoine",
      "source": "./CGP_plugin",
      "category": "productivity"
    }
  ]
}
```

> **Note :** Le chemin `"./CGP_plugin"` correspond au nom du dossier cloné. Adaptez-le si vous avez cloné dans un dossier différent.

### Étape 3 — Enregistrer le marketplace

Depuis le dossier parent (celui qui contient `.claude-plugin/`) :

```bash
claude plugin marketplace add .
```

Résultat attendu :
```
✔ Successfully added marketplace: cgp-local
```

### Étape 4 — Installer le plugin

```bash
claude plugin install cgp-assistant@cgp-local --scope user
```

Vérifier l'installation :

```bash
claude plugin list
```

Résultat attendu :
```
❯ cgp-assistant@cgp-local
    Version: 0.1.0
    Scope: user
    Status: ✔ enabled
```

### Étape 5 — Vérifier les commandes

Redémarrez Claude Code, puis tapez `/` pour voir apparaître les commandes `/rdv`, `/rediger`, `/analyser`, etc.

---

## Commandes disponibles

### `/rdv [nom du client] [objet du RDV]`
Prépare un rendez-vous client complet : ordre du jour, points clés, objections anticipées, questions à poser, documents à rassembler.

```
/rdv Martin Dupont bilan annuel
/rdv Sophie Bernard présentation PER
/rdv          ← Claude pose les questions nécessaires
```

### `/rediger [type de document] [informations clés]`
Rédige un document professionnel prêt à envoyer.

Types supportés : `lettre de mission` · `rapport de conseil` · `compte-rendu` · `lettre de suivi` · `note de synthèse` · `email`

```
/rediger compte-rendu RDV Dupont du 15/04, décision versement 5000€ PER avant fin année
/rediger lettre de mission Jean Martin conseil investissement 12 mois 2400€/an
```

### `/analyser [produit ou situation]`
Compare des produits ou diagnostique une situation patrimoniale.

```
/analyser PEA ou assurance-vie
/analyser fiche PER
/analyser est-ce que le PER convient à Dupont TMI 41% objectif retraite 15 ans
/analyser situation complète Sophie Martin 45 ans TMI 41% AV 80k€ tout en fonds euros
```

### `/veille [sujet]`
Recherche et synthèse réglementaire et fiscale (avec accès web pour les actualités récentes).

```
/veille loi de finances 2025 mesures patrimoine
/veille évolutions fiscalité assurance-vie
```

### `/bilan [nom du client]`
Génère une trame de bilan patrimonial pré-remplie avec les informations disponibles.

```
/bilan Martin Dupont 52 ans marié 2 enfants revenus 90k€ PEA 40k€ AV 120k€ objectif retraite
```

### `/vulgariser [concept]`
Explique un concept financier en langage simple, adapté au profil du client.

```
/vulgariser PER pour un client de 55 ans novice en finance
/vulgariser démembrement de propriété
```

### `/marketing [type] [sujet]`
Crée du contenu marketing professionnel conforme aux règles AMF.

```
/marketing post LinkedIn optimisation fiscale fin d'année
/marketing newsletter mensuelle actualités taux et marchés
```

### `/reporting [client] [période] [données]`
Prépare les documents de suivi périodique.

```
/reporting Dupont T1 2025 PEA +3% AV -1%
/reporting Bernard bilan annuel 2024
```

### `/prospecter [type] [profil prospect]`
Génère des contenus de prospection personnalisés.

```
/prospecter email froid dirigeant TPE 50 ans
/prospecter script d'appel cadre supérieur proche retraite
/prospecter séquence 3 emails consultant indépendant
```

---

## Architecture du plugin

```
cgp-assistant/
├── .claude-plugin/
│   └── plugin.json              # Manifeste du plugin
├── commands/                    # 9 commandes slash
├── skills/                      # 11 modules de connaissance
│   ├── cgp-persona/             # Fondation : ton, conformité AMF/CIF, vocabulaire
│   ├── profil-client/           # Fondation : structure et collecte du profil client
│   ├── preparer-rdv/            # Logique préparation rendez-vous
│   ├── rediger/                 # Formats et règles de rédaction
│   ├── analyser/                # Comparatifs et grilles d'analyse produits
│   ├── veille/                  # Formats de synthèse réglementaire
│   ├── bilan/                   # Trame bilan patrimonial
│   ├── vulgariser/              # Glossaire et formats pédagogiques
│   ├── marketing/               # Règles AMF et idées de sujets
│   ├── reporting/               # Formats de reporting périodique
│   └── prospecter/              # Scripts et séquences de prospection
└── agents/                      # 3 agents autonomes
    ├── redacteur-cgp.md         # Rédaction de documents longs
    ├── analyste-patrimonial.md  # Diagnostic patrimonial complet
    └── veilleur-fiscal.md       # Veille réglementaire avec recherche web
```

---

## Mise à jour

```bash
cd CGP_plugin
git pull
claude plugin update cgp-assistant@cgp-local
```

---

## Avertissement réglementaire

Ce plugin est un **outil d'assistance** pour les professionnels CGP. Il ne se substitue pas au jugement professionnel du conseiller, à sa responsabilité réglementaire (AMF, CIF), ni à la relation de confiance avec le client.

- Les données chiffrées (taux, plafonds, barèmes) doivent être vérifiées sur les sources officielles avant toute utilisation
- Les sorties du plugin ne constituent pas un conseil en investissement personnalisé au sens de la directive MIF II
- La validation finale de toute recommandation appartient au CGP

---

*Licence MIT*
