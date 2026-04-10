---
description: Veille réglementaire, fiscale ou marché — résumé d'une loi, point sur un sujet, actualités AMF
argument-hint: [sujet ou texte à analyser]
---

Use the veille skill and the cgp-persona skill.

Veille request: $ARGUMENTS

If $ARGUMENTS is empty, ask what topic needs monitoring: a specific law or regulation, a fiscal update (PER, IFI, PFU, assurance-vie…), an AMF regulatory change, a market trend, or the annual loi de finances summary.

**Routing logic:**

- Topic within well-established, stable rules (e.g., "comment fonctionne le PEA") → answer directly from knowledge and cgp-persona references
- Topic requiring current or recent information (recent law, this year's loi de finances, AMF update, current market data) → launch the veilleur-fiscal agent to search and verify via the web

Always indicate the date of the information and its source. Flag clearly if any data needs verification from official sources before being shared with clients.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-veille-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `CGP/Production/_cabinet/veille/`.
