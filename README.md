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
- [RGPD](#rgpd)

---

## Fonctionnalités

| Commande | Description | Gain estimé |
|---|---|---|
| `/rdv` | Prépare un rendez-vous client (ordre du jour, objections, questions) | 1–2h/sem |
| `/rediger` | Rédige tout document CGP (lettre de mission, rapport, compte-rendu…) | 3–6h/sem |
| `/analyser` | Compare des produits financiers et évalue leur adéquation au profil client | 4–7h/sem |
| `/veille` | Synthèse réglementaire et fiscale avec recherche web en temps réel | 2–4h/sem |
| `/bilan` | Génère une trame de bilan patrimonial pré-remplie | 2–4h/sem |
| `/dossier` | Analyse patrimoniale complète + rapport de conseil en une commande | 3–5h/sem |
| `/vulgariser` | Traduit un concept financier en langage simple pour un client | 1–2h/sem |
| `/marketing` | Rédige posts LinkedIn, newsletters, articles de blog | 1–3h/sem |
| `/reporting` | Prépare les lettres de suivi et bilans périodiques clients | 2–3h/sem |
| `/prospecter` | Génère emails de prospection, scripts d'appel, messages LinkedIn | 1–2h/sem |
| `/charte` | Configure le template Word du cabinet — génère `.docx` stylé automatiquement à chaque sauvegarde | — |
| `/client` | Charge ou sauvegarde le profil complet d'un client en mémoire persistante | — |
| `/nouveau-client` | Enregistre un nouveau client avec pseudonymisation RGPD automatique | — |
| `/conversation-analyst` | Archive la session courante : JSON structuré + référence markdown dans `~/cgp-sessions/` | — |

**3 agents spécialisés** travaillent en autonomie sur les tâches complexes :
- `redacteur-cgp` — rédaction longue avec conformité AMF/MIF II automatique
- `analyste-patrimonial` — diagnostic patrimonial complet sur 5 dimensions
- `veilleur-fiscal` — recherche web sur les actualités réglementaires et fiscales

---

## Prérequis

- [Claude Code](https://claude.ai/code) installé et configuré
- Un abonnement Claude actif (Claude.ai Pro ou API)
- Python 3.8+ (détecté et configuré automatiquement par `/setup`)

---

## Installation

### Étape 1 — Enregistrer le repository comme source

```bash
claude plugin marketplace add https://github.com/AntoineRu/CGP_plugin
```

### Étape 2 — Installer le plugin

```bash
claude plugin install cgp-assistant
```

Vérifier l'installation :

```bash
claude plugin list
```

Résultat attendu :
```
❯ cgp-assistant
    Version: 0.1.0
    Scope: user
    Status: ✔ enabled
```

### Étape 3 — Lancer la configuration initiale

Redémarrez Claude Code, puis lancez :

```
/setup
```

Cette commande détecte Python, crée l'environnement virtuel, configure les hooks RGPD et vérifie l'installation. **À faire une seule fois après l'installation ou après un changement d'environnement Python.**

### Étape 4 — Vérifier les commandes

Tapez `/` pour voir apparaître les commandes `/rdv`, `/rediger`, `/analyser`, etc.

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

### `/dossier [client]`
Génère en une seule commande une analyse patrimoniale complète et un rapport de conseil structuré, en combinant les agents `analyste-patrimonial` et `redacteur-cgp`.

```
/dossier Martin Dupont
```

### `/nouveau-client [Prénom Nom]`
Enregistre un nouveau client dans le système de pseudonymisation RGPD. Attribue automatiquement un pseudonyme à initiales identiques. À partir de ce moment, le vrai nom est remplacé par le pseudonyme dans tous les échanges avec Claude.

```
/nouveau-client Martin Dupont
```

### `/client load [Prénom Nom]` · `/client save [Prénom Nom]`
Charge ou sauvegarde le profil complet d'un client (situation familiale, patrimoine, objectifs, notes de session).

Chaque sauvegarde écrit deux fichiers simultanément :
- `~/.cgp-clients/<pseudo>.json` — copie pseudonymisée (utilisée par le système IA)
- `~/cgp-clients-private/<nom_réel>.json` — copie décodée avec les vrais noms, consultable directement

```
/client load Martin Dupont      ← début de session
/client save Martin Dupont      ← fin de session
```

### `/conversation-analyst`
Analyse et archive la session courante en deux fichiers persistants :
- `~/cgp-sessions/archive/<date>_<session_name>.json` — enregistrement structuré (tons, décisions, actions, artefacts produits)
- `~/cgp-sessions/references/<date>_<session_name>_reference.md` — document de référence avec concepts, sources et fils de recherche

Le nom de session est dérivé automatiquement du **vrai nom du client** (résolu depuis le registre RGPD) ou du sujet principal si aucun client n'est impliqué.

> Note : le fichier JSON conserve les pseudonymes (audit) ; le fichier markdown est décodé avec les vrais noms (lecture humaine).

```
/conversation-analyst
```

### `/charte [chemin/vers/template.docx]`
Configure la charte graphique du cabinet à partir d'un template Word. Une fois configuré, chaque commande peut sauvegarder sa réponse en `.docx` (stylé avec votre template) dans `~/CGP/`.

```
/charte /home/user/Cabinet/template.docx
```

### `/setup`
Configuration initiale du plugin. Détecte Python, crée le venv, configure les hooks, initialise le registre RGPD et lance les tests de vérification. Compatible Linux, macOS, WSL et Windows natif.

```
/setup
```

---

## Architecture du plugin

```
cgp-assistant/
├── .claude-plugin/
│   └── plugin.json              # Manifeste du plugin
├── commands/                    # 15 commandes slash
│   ├── setup.md                 # Configuration initiale (à lancer en premier)
│   ├── charte.md                # Configuration charte graphique + template Word
│   ├── rdv.md / rediger.md / analyser.md / veille.md / bilan.md
│   ├── dossier.md               # Analyse patrimoniale complète + rapport
│   ├── vulgariser.md / marketing.md / reporting.md / prospecter.md
│   ├── client.md                # Chargement et sauvegarde profil client
│   ├── nouveau-client.md        # Enregistrement RGPD nouveau client
│   └── conversation-analyst.md  # Archivage de session (JSON + markdown)
├── skills/                      # 13 modules de connaissance
│   ├── cgp-persona/             # Fondation : ton, conformité AMF/CIF, vocabulaire
│   ├── profil-client/           # Fondation : structure et collecte du profil client
│   ├── client-memory/           # Mémoire persistante des profils clients
│   ├── conversation-analyst/    # Analyse et archivage de session dans ~/cgp-sessions/
│   ├── preparer-rdv/            # Logique préparation rendez-vous
│   ├── rediger/                 # Formats et règles de rédaction
│   ├── analyser/                # Comparatifs et grilles d'analyse produits
│   ├── veille/                  # Formats de synthèse réglementaire
│   ├── bilan/                   # Trame bilan patrimonial
│   ├── vulgariser/              # Glossaire et formats pédagogiques
│   ├── marketing/               # Règles AMF et idées de sujets
│   ├── reporting/               # Formats de reporting périodique
│   └── prospecter/              # Scripts et séquences de prospection
├── agents/                      # 3 agents autonomes
│   ├── redacteur-cgp.md         # Rédaction de documents longs
│   ├── analyste-patrimonial.md  # Diagnostic patrimonial complet
│   └── veilleur-fiscal.md       # Veille réglementaire avec recherche web
└── hooks/                       # Traitements automatiques en arrière-plan
    ├── anonymize.py             # Pseudonymisation RGPD (UserPromptSubmit + PostToolUse)
    ├── fiscal_alerts.py         # Alertes échéances fiscales (UserPromptSubmit, 1×/jour)
    ├── client_store.py          # Lecture/écriture profils clients (dual store)
    ├── output_router.py         # Conversion .md → .docx + routage dans ~/CGP/ (PostToolUse)
    ├── hooks.json               # Configuration des événements Claude Code (gitignored)
    ├── hooks.json.example       # Template Linux / macOS / WSL
    └── hooks.json.windows.example  # Template Windows natif
```

---

## Hooks — Traitements automatiques

Quatre scripts s'exécutent silencieusement à chaque session sans intervention de l'utilisateur :

| Hook | Événement | Rôle |
|---|---|---|
| `anonymize.py encode` | Avant chaque prompt | Remplace les vrais noms clients par leurs pseudonymes RGPD |
| `anonymize.py decode` | Après chaque écriture de fichier | Restaure les vrais noms dans les documents produits |
| `fiscal_alerts.py` | Avant le premier prompt de la journée | Rappelle les échéances fiscales imminentes |
| `output_router.py` | Après chaque écriture de fichier `.md` préfixé `cgp-` | Convertit en `.docx` et range dans `~/CGP/<Client>/<type>/` |

**Emplacements de données persistantes :**

| Répertoire | Rôle |
|---|---|
| `~/.cgp-clients/` | Profils pseudonymisés — utilisés par l'IA |
| `~/cgp-clients-private/` | Profils décodés — consultation directe par le CGP |
| `~/.cgp-client-registry.json` | Table de correspondance nom réel ↔ pseudonyme |
| `~/CGP/_cabinet/<type>/` | Productions cabinet (veille, marketing, prospection…) |
| `~/CGP/<Client>/<type>/` | Productions client (bilans, lettres, analyses…) |
| `~/cgp-sessions/` | Archives de session — JSON + markdown |

---

## Mise à jour

```bash
claude plugin update cgp-assistant
```

---

## Avertissement réglementaire

Ce plugin est un **outil d'assistance** pour les professionnels CGP. Il ne se substitue pas au jugement professionnel du conseiller, à sa responsabilité réglementaire (AMF, CIF), ni à la relation de confiance avec le client.

- Les données chiffrées (taux, plafonds, barèmes) doivent être vérifiées sur les sources officielles avant toute utilisation
- Les sorties du plugin ne constituent pas un conseil en investissement personnalisé au sens de la directive MIF II
- La validation finale de toute recommandation appartient au CGP

---

## RGPD

En utilisant ce plugin, vous transmettez des données à Anthropic (sous-traitant). En tant que CGP, vous êtes responsable du traitement au sens du RGPD.

**Règles essentielles :**
- N'entrez jamais de numéro de sécurité sociale, IBAN ou données de santé dans Claude
- Anonymisez les données clients : initiales, âge, ordres de grandeur
- Informez vos clients de l'utilisation d'outils d'IA (clause à intégrer dans le DER)
- Le plugin insère automatiquement les clauses RGPD dans les lettres de mission et comptes-rendus

Voir [RGPD.md](RGPD.md) pour la notice complète et les modèles de clauses.

---

*Licence MIT*
