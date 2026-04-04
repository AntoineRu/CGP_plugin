---
description: 'Générer un dossier complet : analyse patrimoniale → rapport de conseil prêt à envoyer'
argument-hint: '[nom du client] [informations patrimoniales disponibles]'
---

## Commande /dossier — Pipeline analyse → rapport de conseil

Cette commande orchestre deux agents spécialisés en séquence : l'`analyste-patrimonial` produit le diagnostic complet, puis le `redacteur-cgp` le transforme en rapport de conseil formel, prêt à remettre au client.

---

### Étape 1 — Vérification du contexte client

Vérifier si un profil client est déjà disponible dans la conversation (chargé via `/client load` ou `profil-client`).

- **Si un profil existe dans la conversation** : l'utiliser comme source principale. Compléter avec $ARGUMENTS si des informations supplémentaires y figurent.
- **Si $ARGUMENTS contient des informations client** : les utiliser comme contexte de départ.
- **Si $ARGUMENTS est vide et aucun profil n'est disponible** : poser une seule question consolidée avant toute action :

  > "Pour générer le dossier complet, j'ai besoin des informations suivantes :
  > - Nom et prénom du client (ou pseudonyme si vous préférez travailler anonymisé)
  > - Âge, situation familiale, nombre d'enfants
  > - Revenus annuels et tranche marginale d'imposition (TMI)
  > - Patrimoine principal (immobilier, financier, épargne — montants approximatifs)
  > - Objectif principal (retraite, transmission, optimisation fiscale, autre)"

**Rappel RGPD :** Si $ARGUMENTS contient le nom réel du client associé à des données financières ou personnelles précises, afficher avant de continuer :

> "Rappel conformité RGPD : ce dossier contient des données à caractère personnel. Assurez-vous que ce client a signé une lettre de mission incluant la clause de traitement des données. Pour travailler de façon anonymisée, vous pouvez remplacer le nom par un pseudonyme ou des initiales."

---

### Étape 2 — Chargement des skills

Charger les skills suivants avant de lancer les agents :

1. `cgp-persona` — cadrage réglementaire (AMF/CIF/MIF II), ton professionnel, mentions de conformité obligatoires
2. `profil-client` — structuration des données client comme contexte partagé pour les deux agents

---

### Étape 3 — Analyse patrimoniale (agent analyste-patrimonial)

Lancer l'agent `analyste-patrimonial` avec l'intégralité du contexte client disponible.

Lui donner les instructions suivantes de façon explicite :

> "Réalise l'analyse patrimoniale complète en 5 dimensions (bilan patrimonial, optimisation fiscale, allocation et risque, succession et transmission, pistes d'action prioritaires) pour ce client. Une fois l'analyse terminée, enregistre-la dans un fichier temporaire `/tmp/cgp-analyse-[TIMESTAMP].md` où [TIMESTAMP] est un identifiant numérique simple basé sur la session courante (format : YYYYMMDDHHMMSS ou un entier incrémental). Retourne ensuite une seule ligne de confirmation indiquant le chemin exact du fichier créé et les 2-3 recommandations prioritaires identifiées."

Attendre la confirmation de l'agent avant de passer à l'étape suivante. Si l'agent ne confirme pas la création du fichier, lui redemander explicitement le chemin du fichier sauvegardé.

---

### Étape 4 — Rapport de conseil (agent redacteur-cgp)

Une fois le fichier d'analyse confirmé, lancer l'agent `redacteur-cgp` avec les instructions suivantes :

> "Lis le fichier d'analyse patrimoniale situé dans `/tmp/` (fichier le plus récent correspondant au pattern `cgp-analyse-*.md`, ou au chemin exact fourni à l'étape précédente). Sur la base de cette analyse, rédige un `Rapport de conseil patrimonial` complet en utilisant le format type 2 (Rapport de conseil) défini dans `skills/rediger/SKILL.md`. Le rapport doit inclure : rappel de la situation, objectifs identifiés, analyse, recommandations détaillées avec justifications, alternatives envisagées, et points de vigilance. Intègre les mentions de conformité obligatoires de `cgp-persona` (avertissement MIF II, absence de garantie de rendement). Enregistre le rapport final dans le répertoire de travail courant sous le nom `rapport-conseil-[NomClient]-[YYYYMMDD].md` (en remplaçant [NomClient] par le nom du client sans espaces ni accents, et [YYYYMMDD] par la date du jour). Retourne le chemin exact du fichier créé."

Le rapport doit impérativement contenir la mention de conformité suivante (non négociable) :

> *Ce rapport est établi à titre informatif sur la base des informations communiquées par le client. Il ne constitue pas un conseil en investissement personnalisé au sens de la directive MIF II sans validation des éléments du profil. Les performances passées ne préjugent pas des performances futures.*

---

### Étape 5 — Confirmation et proposition de suite

Après confirmation de la sauvegarde du rapport par `redacteur-cgp`, afficher le message de clôture suivant :

> "Dossier complet généré : `rapport-conseil-[NomClient]-[date].md`
>
> Que souhaitez-vous faire maintenant ?
>
> **1.** Rédiger une lettre de suivi pour informer [NomClient] que son rapport est prêt (`/rediger lettre de suivi`)
> **2.** Ouvrir et réviser le rapport maintenant
> **3.** Terminer — le dossier est prêt"

Attendre la réponse du CGP avant de continuer.

---

### Étape 6 — Lettre de suivi (si option 1 choisie)

Si le CGP choisit l'option 1, lancer l'agent `redacteur-cgp` avec les instructions suivantes :

> "Rédige une lettre de suivi professionnelle destinée à [NomClient] pour l'informer qu'un rapport de conseil patrimonial a été établi à son attention et est disponible pour discussion lors de leur prochain rendez-vous. La lettre doit : utiliser le ton et le format 'lettre de suivi client' défini dans `skills/rediger/SKILL.md` (type 4), être brève et chaleureuse (3-4 paragraphes maximum), inviter le client à prendre rendez-vous pour en discuter, et inclure une formule de politesse appropriée. Ne pas mentionner le contenu détaillé du rapport dans la lettre."

Si le CGP choisit l'option 2, lire et afficher le contenu du rapport sauvegardé pour révision en direct.

Si le CGP choisit l'option 3, confirmer simplement que le dossier est archivé et disponible dans le répertoire courant.

---

## Sauvegarde

Le rapport final généré par l'agent `redacteur-cgp` est déjà enregistré sous
`rapport-conseil-<NomClient>-<YYYYMMDD>.md`. Renomme-le en
`cgp-dossier-<NomClient>-<YYYYMMDD>.md` avant de confirmer la fin de la commande,
afin que `output_router.py` le détecte et le range dans `~/CGP/<Client>/reporting/`.
