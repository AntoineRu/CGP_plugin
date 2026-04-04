---
description: 'Analyser un produit financier, comparer des enveloppes, ou évaluer l''adéquation produit/profil client'
argument-hint: '[produit ou situation] [profil client si disponible]'
---

Use the analyser skill and the cgp-persona skill. If a client profile is available in the conversation, use profil-client to personalize the analysis.

Analysis request: $ARGUMENTS

If $ARGUMENTS is empty, ask in a single question what needs to be analyzed: a product comparison (e.g., PEA vs PER), a product summary sheet, a suitability check for a specific client, or a full patrimonial situation diagnosis.

**Routing logic:**

- Simple comparison between 2 products (e.g., "PEA ou AV ?") → answer directly using analyser skill and grilles-comparaison reference
- Product summary sheet (e.g., "fiche PER") → answer directly using analyser skill and produits-financiers reference
- Suitability check with client profile (e.g., "est-ce que le PER convient à Martin ?") → use analyser skill suitability format
- Full patrimonial situation analysis or complex multi-product strategy → launch the analyste-patrimonial agent

Always end with the appropriate compliance disclaimer from cgp-persona if investment products are discussed.

---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-analyser-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/analyses/`.
