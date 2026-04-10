---
description: 'Rédiger un document CGP (lettre de mission, rapport, compte-rendu, lettre de suivi, email)'
argument-hint: '[type de document] [informations clés]'
---

Use the rediger skill and the cgp-persona skill. If a client profile has been shared in the conversation, also use the profil-client skill to personalize the document.

Document request: $ARGUMENTS

If $ARGUMENTS is empty, ask in a single question:
1. What type of document is needed? (lettre de mission / rapport de conseil / compte-rendu / lettre de suivi / note de synthèse / email)
2. What are the key details? (client name, subject, any specific content to include)

For simple documents (short email, brief follow-up letter): draft directly using the rediger skill formats.

For complex documents (lettre de mission, rapport de conseil, full compte-rendu): launch the redacteur-cgp agent to handle the full drafting with all regulatory elements.

Always verify compliance disclaimers are included if the document involves investment products or advice.

For lettres de mission: always include the RGPD data protection clause from cgp-persona references/rgpd.md.
For comptes-rendus: always append the confidentiality footer from cgp-persona references/rgpd.md.
If the input contains identifying personal data (full name + precise personal or financial details), display the RGPD anonymization reminder from cgp-persona before proceeding.

Deliver the complete document ready to use, followed by a short list of any fields the CGP still needs to fill in before sending.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-rediger-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `CGP/Production/Clients/<Client>/lettres/`.
