---
name: client-memory
description: This skill should be used when the user invokes /client, asks to "sauvegarder le profil", "charger le profil de [client]", "retrouver les informations de [client]", or wants to persist or retrieve a client profile across sessions. Combines with profil-client to structure profiles before saving, and restores full context when loading.
---

# Client Memory — Mémoire Persistante des Profils Clients

Ce skill gère la persistance des profils clients entre les sessions Claude Code. Par défaut, chaque session démarre vierge : ce skill permet de sauvegarder et recharger le contexte client complet pour éviter de ressaisir les mêmes informations à chaque session.

## Problème résolu

Un CGP travaille sur les mêmes clients session après session. Sans persistance, il faut re-renseigner l'âge, les objectifs, le patrimoine, le profil investisseur, etc. à chaque ouverture de Claude Code. Ce skill élimine cette friction.

## Comment fonctionne la sauvegarde

1. Le skill `profil-client` structure les informations client en un format standardisé (situation personnelle, financière, patrimoniale, objectifs, profil investisseur, fiscalité, notes).
2. Ce profil structuré est sérialisé en JSON.
3. Le script `hooks/client_store.py` écrit le JSON dans `CGP/_config/clients/<pseudo>.json`.
4. Le fichier est keyed par **pseudonyme uniquement** — jamais par nom réel (conformité RGPD).
5. Un champ `_meta` est ajouté automatiquement : `{saved_at, pseudo, real_name}`.

## Comment fonctionne le chargement

1. La commande `/client load [nom]` appelle `client_store.py load [nom]`.
2. Le script résout le nom (réel ou pseudo) via le registre `CGP/_config/client-registry.json`.
3. Le JSON du profil est retourné et injecté dans la session comme contexte `profil-client` actif.
4. Toutes les tâches suivantes (rédaction, analyse, bilan, rendez-vous) bénéficient immédiatement de ce contexte.

## Workflow recommandé en début de session

Dès qu'une session porte sur un client connu :

1. Lancer `/client list` pour voir les profils disponibles.
2. Lancer `/client load [nom du client]` pour restaurer le contexte.
3. Travailler normalement — le profil est actif.
4. En fin de session (ou après mise à jour des informations), lancer `/client save` pour persister les changements.

## Commandes disponibles

| Commande | Action |
|---|---|
| `/client save [nom]` | Sauvegarder le profil du client actif |
| `/client load [nom]` | Charger un profil et l'injecter dans la session |
| `/client list` | Lister tous les profils sauvegardés |
| `/client delete [nom]` | Supprimer un profil (confirmation requise) |

## Conformité RGPD

- Les fichiers sont stockés dans `CGP/_config/clients/` au sein du projet, sur la machine locale du CGP.
- Les noms de fichiers utilisent uniquement le **pseudonyme** (`<pseudo>.json`), jamais le nom réel.
- La correspondance pseudonyme ↔ nom réel est gérée séparément par `hooks/anonymize.py` dans `CGP/_config/client-registry.json`.
- Aucune donnée client n'est transmise à des services externes par ce mécanisme.

## Intégration avec les autres skills

Ce skill s'appuie sur **`profil-client`** pour le format standardisé des données. Lors d'une sauvegarde, charger `profil-client` en premier pour structurer les données avant sérialisation. Lors d'un chargement, utiliser `profil-client` pour interpréter correctement le JSON restauré.

Les données chargées servent de contexte pour :
- **`cgp-persona`** — adapter le registre de communication
- **`/rdv`** — préparer le rendez-vous avec le bon profil
- **`/bilan`** — pré-remplir le bilan patrimonial
- **`/analyser`** — filtrer les produits selon le profil investisseur
- **`/rediger`** — personnaliser les documents clients

## Référence technique

- Script de persistance : `hooks/client_store.py`
- Script d'anonymisation : `hooks/anonymize.py`
- Répertoire de stockage : `CGP/_config/clients/`
- Registre d'anonymisation : `CGP/_config/client-registry.json`
- Format du profil : voir `skills/profil-client/SKILL.md` et `skills/profil-client/assets/template-profil.md`
