---
description: 'Préparer un reporting client (lettre de suivi portefeuille, bilan trimestriel, note de performance)'
argument-hint: '[nom du client] [période] [données de performance si disponibles]'
---

Use the reporting skill and the cgp-persona skill. If a client profile is available in the conversation, use profil-client.

Reporting request: $ARGUMENTS

If $ARGUMENTS is empty, ask:
1. Which client and what period to cover?
2. What data is available (portfolio values, performance figures)?
3. What type of document? (lettre de suivi / tableau de bord annuel / note de performance sur un produit)

For simple reporting with provided data, draft directly using the reporting skill formats. For complex multi-product reporting requiring drafting polish, launch the redacteur-cgp agent.

Always include the date of the data, a compliance disclaimer, and a clear next-step proposal.
