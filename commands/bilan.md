---
description: 'Générer une trame de bilan patrimonial pré-remplie pour un client'
argument-hint: '[nom du client] ou [informations patrimoniales]'
---

Use the bilan skill and the cgp-persona skill. If a client profile has been shared in the conversation, use profil-client to pre-fill the template.

Before processing, check whether the input contains identifying personal data (full name + precise financial figures + address). If so, display the RGPD reminder from cgp-persona before proceeding.

Client information: $ARGUMENTS

If $ARGUMENTS is empty, ask for the client's name and any available information (age, family situation, assets, income, objectives).

Generate the complete patrimonial assessment template from the bilan skill, pre-filling all fields that are available from the conversation. Mark missing fields as [À compléter]. List all missing critical information at the end.

If the user wants a deep analytical diagnosis (not just the template), suggest launching the analyste-patrimonial agent.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-bilan-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant
(remplace `<NomClient>` par le nom du client sans espaces, `<YYYYMMDD>` par la date du jour).
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/bilans/`.
