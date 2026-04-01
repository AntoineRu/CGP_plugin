---
description: 'Générer une trame de bilan patrimonial pré-remplie pour un client'
argument-hint: '[nom du client] ou [informations patrimoniales]'
---

Use the bilan skill and the cgp-persona skill. If a client profile has been shared in the conversation, use profil-client to pre-fill the template.

Client information: $ARGUMENTS

If $ARGUMENTS is empty, ask for the client's name and any available information (age, family situation, assets, income, objectives).

Generate the complete patrimonial assessment template from the bilan skill, pre-filling all fields that are available from the conversation. Mark missing fields as [À compléter]. List all missing critical information at the end.

If the user wants a deep analytical diagnosis (not just the template), suggest launching the analyste-patrimonial agent.
