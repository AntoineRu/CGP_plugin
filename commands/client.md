---
description: 'Gérer les profils clients persistants — sauvegarder, charger, lister'
argument-hint: '[save|load|list|delete] [nom du client]'
---

# Commande /client — Mémoire persistante des profils clients

Cette commande permet de sauvegarder et recharger les profils clients entre les sessions Claude Code. Les profils sont stockés dans `~/.cgp-clients/` sous forme de fichiers JSON anonymisés (keyed par pseudonyme RGPD).

## Routing par sous-commande

Analyse `$ARGUMENTS` pour déterminer la sous-commande :

---

### `/client save [nom]`

**Objectif** : Persister le profil du client actif dans la conversation.

1. Charge le skill `profil-client` pour extraire et structurer toutes les informations client disponibles dans la conversation en format JSON structuré.
2. Identifie le pseudonyme du client via le registre d'anonymisation :
   ```
   /home/aruna/anaconda3/envs/finance/bin/python3 "${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py" list
   ```
   Cherche la correspondance nom réel ↔ pseudonyme pour le client concerné. Si le client n'est pas encore enregistré, utiliser d'abord :
   ```
   /home/aruna/anaconda3/envs/finance/bin/python3 "${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py" register "Prénom Nom"
   ```
3. Sérialise le profil structuré en JSON (tous les champs du format `profil-client` : situation personnelle, financière, patrimoine, objectifs, profil investisseur, situation fiscale, notes).
4. Sauvegarde via :
   ```
   echo '<json_du_profil>' | /home/aruna/anaconda3/envs/finance/bin/python3 "${CLAUDE_PLUGIN_ROOT}/hooks/client_store.py" save <pseudo>
   ```
5. Confirme à l'utilisateur :
   - "Profil de [nom réel] sauvegardé."
   - Fichier pseudonymisé (copie de travail IA) : `~/.cgp-clients/<pseudo>.json`
   - Fichier privé (noms réels, lisible par vous) : `~/cgp-clients-private/<nom_réel>.json`
   - Si `private_error` est présent dans la réponse JSON, afficher un avertissement : "La copie privée n'a pas pu être écrite : [erreur]"

---

### `/client load [nom]`

**Objectif** : Recharger un profil client sauvegardé et l'injecter dans la session en cours.

1. Exécute :
   ```
   /home/aruna/anaconda3/envs/finance/bin/python3 "${CLAUDE_PLUGIN_ROOT}/hooks/client_store.py" load "[nom]"
   ```
   `[nom]` peut être le nom réel ou le pseudonyme — le script résout automatiquement.
2. Parse le JSON retourné et charge le skill `profil-client` pour injecter les données comme contexte actif de la session.
3. Reconstruit mentalement le profil complet à partir du JSON (situation personnelle, financière, patrimoniale, objectifs, profil investisseur, fiscalité, notes).
4. Confirme : "Profil chargé — [nom réel], [âge] ans, objectif principal : [objectif]. Le contexte client est maintenant actif pour cette session."

---

### `/client list`

**Objectif** : Afficher tous les profils clients sauvegardés.

1. Exécute :
   ```
   /home/aruna/anaconda3/envs/finance/bin/python3 "${CLAUDE_PLUGIN_ROOT}/hooks/client_store.py" list
   ```
2. Affiche un tableau formaté en Markdown :

   | Nom réel | Pseudonyme | Dernière sauvegarde |
   |----------|------------|---------------------|
   | ...      | ...        | ...                 |

   Si aucun profil, afficher : "Aucun profil client sauvegardé. Utilisez `/client save` après avoir travaillé sur un dossier client."

---

### `/client delete [nom]`

**Objectif** : Supprimer définitivement un profil sauvegardé.

1. Demande confirmation à l'utilisateur avant toute suppression :
   "Vous êtes sur le point de supprimer définitivement le profil de [nom]. Cette action est irréversible. Confirmez-vous ? (oui/non)"
2. Si confirmé, résout le pseudonyme si besoin (via `anonymize.py list`), puis exécute :
   ```
   /home/aruna/anaconda3/envs/finance/bin/python3 "${CLAUDE_PLUGIN_ROOT}/hooks/client_store.py" delete "[pseudo]"
   ```
3. Confirme : "Profil de [nom] supprimé."

---

### Sans arguments

Afficher le résumé d'utilisation :

```
/client save [nom]    — Sauvegarder le profil du client actif
/client load [nom]    — Charger un profil client sauvegardé
/client list          — Lister tous les profils sauvegardés
/client delete [nom]  — Supprimer un profil (confirmation requise)
```

---

## Notes techniques

- **Python** : toujours utiliser `/home/aruna/anaconda3/envs/finance/bin/python3`
- **Stockage** : `~/.cgp-clients/<pseudo>.json` — jamais de nom réel dans le nom de fichier
- **Registre anonymisation** : `~/.cgp-client-registry.json` (géré par `anonymize.py`)
- **En cas d'erreur JSON** du script : afficher le message d'erreur retourné et proposer une action corrective
- **Skill requis** : charger `profil-client` lors des opérations save et load pour garantir la cohérence du format
