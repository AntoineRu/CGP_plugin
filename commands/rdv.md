---
description: 'Préparer un rendez-vous client (ordre du jour, points clés, objections, questions)'
argument-hint: '[nom du client] [objet du RDV]'
---

Use the cgp-persona skill and the preparer-rdv skill to prepare a complete client meeting document.

Client and meeting context from arguments: $ARGUMENTS

If $ARGUMENTS is empty, ask the user in a single question: the client's name and the main purpose of the meeting (annual review, product presentation, follow-up, succession, etc.).

If the client's profile has been shared earlier in the conversation, use that structured information to personalize the preparation. Otherwise, work with what is provided in $ARGUMENTS.

Generate the full meeting preparation document following the standard format defined in the preparer-rdv skill: agenda, key points to address, anticipated objections with prepared responses, questions to ask the client, documents to gather, and a vigilance note.

Adapt the content to the meeting type (annual review, product recommendation, first meeting with prospect, succession planning, etc.).

Always include the appropriate compliance disclaimer from cgp-persona at the end if financial products or investment advice are involved.

If the input contains identifying personal data (full name + precise financial or personal details), display the RGPD anonymization reminder from cgp-persona before proceeding.
