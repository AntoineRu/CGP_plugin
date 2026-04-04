---
description: 'Rédiger un contenu marketing CGP (post LinkedIn, newsletter, article, email campagne)'
argument-hint: '[type de contenu] [sujet]'
---

Use the marketing skill and the cgp-persona skill.

Content request: $ARGUMENTS

If $ARGUMENTS is empty, ask:
1. What type of content? (post LinkedIn / newsletter / article de blog / email campagne)
2. What topic or occasion?

Draft the complete content following the format and rules defined in the marketing skill for the requested type. Apply all AMF compliance rules for financial communication — include the mandatory disclaimer if financial products or performance are mentioned.

If the user needs topic ideas, consult references/idees-sujets.md from the marketing skill.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-marketing-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/_cabinet/marketing/`.
