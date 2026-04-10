---
description: 'Rédiger un contenu de prospection (email froid, message LinkedIn, script d''appel, séquence de suivi)'
argument-hint: '[type de contenu] [profil du prospect]'
---

Use the prospecter skill and the cgp-persona skill.

Prospecting request: $ARGUMENTS

If $ARGUMENTS is empty, ask:
1. What type of content? (email froid / message LinkedIn / script d'appel / séquence de suivi 3 emails)
2. What prospect profile? (dirigeant TNS / cadre supérieur / proche retraite / autre)
3. Any specific context or connection to personalize the message?

Draft the content following the formats in the prospecter skill. Apply the rule: value before ask — always bring something useful before requesting time. Include one clear CTA only. Apply AMF rules: no promise of gains or tax savings.

For a full 3-email sequence, generate all three messages with timing notes.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-prospecter-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `CGP/Production/_cabinet/prospection/`.
