# Design — Organisation des productions du plugin CGP

**Date :** 2026-04-03
**Statut :** Approuvé

---

## Contexte

Le plugin CGP produit des documents de natures variées (bilans, lettres, analyses, veilles...). Aujourd'hui ces fichiers ne sont pas organisés — ils atterrissent dans le répertoire courant sans convention de nommage ni arborescence. Ce design définit l'organisation cible et le mécanisme pour l'atteindre.

---

## Arborescence cible

```
~/CGP/
├── _cabinet/                   ← productions non liées à un client
│   ├── veille/                 ← /veille
│   ├── vulgarisation/          ← /vulgariser
│   ├── marketing/              ← /marketing
│   └── prospection/            ← /prospecter
└── <Nom Réel Client>/          ← un dossier par client (nom réel décodé)
    ├── analyses/               ← /analyser
    ├── bilans/                 ← /bilan
    ├── lettres/                ← /rediger
    ├── rendez-vous/            ← /rdv
    └── reporting/              ← /reporting, /dossier
```

### Règles

- `~/CGP/` et `~/CGP/_cabinet/<type>/` sont créés par `/setup`
- Les dossiers `~/CGP/<Client>/` et leurs sous-dossiers sont créés à la volée au premier fichier
- Les dossiers système (`~/.cgp-clients/`, `~/cgp-sessions/`) restent inchangés

### Convention de nommage

- Fichier client : `YYYY-MM-DD_<type>_<NomClient>.docx`
  - ex : `2026-04-03_bilan_Dupont.docx`
- Fichier cabinet : `YYYY-MM-DD_<type>.docx`
  - ex : `2026-04-03_veille.docx`

---

## Sauvegarde des réponses chat

Toutes les commandes (`/veille`, `/analyser`, `/rdv`, `/bilan`, `/rediger`, `/reporting`, `/dossier`, `/marketing`, `/vulgariser`, `/prospecter`) ajoutent en fin de prompt :

> À la fin de ta réponse, propose à l'utilisateur : "Voulez-vous sauvegarder cette réponse ? (oui / non)"
> - Si oui (commande client) : écrire le contenu dans `cgp-<type>-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant
> - Si oui (commande cabinet) : écrire dans `cgp-<type>-<YYYYMMDD>.md` dans le répertoire courant

Le hook `output_router.py` prend le relais dès que le fichier est écrit.

---

## Hook `output_router.py`

Remplace `render_docx.py` (supprimé). Déclenché sur chaque PostToolUse Write/Edit.

### Logique d'exécution (dans l'ordre)

1. **Filtre** — ignore si le fichier écrit n'est pas un `.md`
2. **Charte par défaut** — si `charte_config.json` est absent, le créer avec les paramètres par défaut :
   ```json
   {
     "template_path": null,
     "style_map": {
       "Heading 1": "Heading 1",
       "Heading 2": "Heading 2",
       "Heading 3": "Heading 3",
       "Normal": "Normal",
       "List Bullet": "List Bullet",
       "List Number": "List Number"
     },
     "typography": {
       "body_font": "Calibri",
       "body_size": 11,
       "heading_font": "Calibri",
       "heading_size": 14
     }
   }
   ```
   Quand `template_path` est `null`, `output_router.py` génère le `.docx` sans template (document Word vierge avec styles standards). Log : `[cgp] charte_config.json absent — paramètres par défaut utilisés`
3. **Détecte le type** — depuis le nom du fichier (table de correspondance) :

   | Motif dans le nom | Dossier cible |
   |---|---|
   | `bilan` | `bilans/` |
   | `rediger`, `lettre`, `mission`, `cr` | `lettres/` |
   | `analyser`, `analyse` | `analyses/` |
   | `rdv`, `rendez-vous` | `rendez-vous/` |
   | `reporting`, `dossier`, `rapport` | `reporting/` |
   | `veille` | `_cabinet/veille/` |
   | `vulgariser`, `vulgaris` | `_cabinet/vulgarisation/` |
   | `marketing` | `_cabinet/marketing/` |
   | `prospecter`, `prospect` | `_cabinet/prospection/` |
   | *(non reconnu)* | `_cabinet/divers/` |

4. **Détecte le client** — recherche dans le contenu du `.md` les noms connus du registre RGPD (`~/.cgp-client-registry.json`), correspondance la plus longue en premier. Si aucun match ou type cabinet → `_cabinet/`
5. **Crée le dossier cible** si inexistant
6. **Convertit** — Markdown → `.docx` (avec template si `template_path` non null, sinon document Word vierge avec styles standards)
7. **Nomme et déplace** le `.docx` dans le dossier cible
8. **Supprime** le `.md` source
9. **Log discret** sur stderr : `[cgp] → ~/CGP/Dupont/bilans/2026-04-03_bilan_Dupont.docx`

### Payload attendu (PostToolUse)

```json
{
  "tool_name": "Write",
  "tool_input": { "file_path": "/chemin/vers/cgp-bilan-Dupont-20260403.md" }
}
```

---

## Migrations nécessaires

| Élément | Action |
|---|---|
| `hooks/render_docx.py` | Supprimé — logique absorbée dans `output_router.py` |
| `hooks/hooks.json.example` | `render_docx.py` → `output_router.py` |
| `hooks/hooks.json.windows.example` | Idem |
| `hooks.json` actif (généré) | Mis à jour par `/setup` ou `/charte` |
| `commands/charte.md` Phase 6 | Référence `output_router.py` au lieu de `render_docx.py` |
| `/setup` Phase 6 | Ajoute création de `~/CGP/` et `~/CGP/_cabinet/<type>/` |
| Toutes les commandes concernées | Ajout du bloc "proposition de sauvegarde" en fin de prompt |

---

## Ce qui ne change pas

- `~/.cgp-clients/` — profils pseudonymisés (système)
- `~/cgp-clients-private/` — profils décodés (système)
- `~/cgp-sessions/` — archives de session `/conversation-analyst`
- `hooks/anonymize.py`, `hooks/fiscal_alerts.py`, `hooks/client_store.py` — inchangés
- `hooks.json` reste gitignored et machine-spécifique
