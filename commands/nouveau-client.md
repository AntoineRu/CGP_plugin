---
description: 'Enregistrer un nouveau client dans le système de pseudonymisation RGPD'
argument-hint: '[Prénom Nom]'
---

The user wants to register a new client for RGPD-compliant pseudonymisation.

Client name: $ARGUMENTS

If $ARGUMENTS is empty, ask: "Quel est le nom complet du client ? (Prénom Nom)"

Run this command to register the client and get their pseudonym:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py" register $ARGUMENTS
```

Parse the JSON result and present it clearly in French:

**If status = "registered":**
> ✅ Client enregistré avec succès
> - Vrai nom : [real]
> - Pseudonyme RGPD : **[pseudo]** (mêmes initiales)
>
> À partir de maintenant :
> - Quand vous tapez "[real]" dans un prompt → le hook remplace automatiquement par "[pseudo]" avant que Claude le voie
> - Quand Claude écrit un document → le hook restaure "[real]" dans le fichier final

**If status = "already_registered":**
> ℹ️ Ce client est déjà enregistré
> - Vrai nom : [real]
> - Pseudonyme actif : **[pseudo]**

**If error:**
> ❌ Format invalide. Utiliser : `/nouveau-client Prénom Nom`

After registering, offer to list all registered clients with:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py" list
```
