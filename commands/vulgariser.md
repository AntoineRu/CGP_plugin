---
description: 'Expliquer un concept financier ou fiscal en langage simple pour un client non-expert'
argument-hint: '[concept à expliquer] [profil du client si pertinent]'
---

Use the vulgariser skill and the cgp-persona skill.

Concept to explain: $ARGUMENTS

If $ARGUMENTS is empty, ask what concept needs to be explained and for what type of client (age, financial background, context).

Choose the appropriate format from the vulgariser skill based on the use case:
- Quick oral explanation → Format 1 (short explanation with analogy)
- Document to hand to the client → Format 2 (pedagogical sheet)
- FAQ for website or newsletter → Format 3

Adapt the language and analogies to the client's profile if known. Always end with a concrete "what this means for you" implication.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-vulgariser-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/_cabinet/vulgarisation/`.
