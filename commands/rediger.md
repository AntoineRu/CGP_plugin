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

Deliver the complete document ready to use, followed by a short list of any fields the CGP still needs to fill in before sending.
