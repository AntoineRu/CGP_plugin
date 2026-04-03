# Notice RGPD — CGP Assistant

## Ce que ce plugin fait avec vos données

CGP Assistant est un plugin pour Claude Code (Anthropic). Lorsque vous l'utilisez, vos saisies — y compris les informations clients que vous entrez dans les commandes — sont transmises aux serveurs d'Anthropic pour traitement.

**Anthropic agit comme sous-traitant.** Vous, le CGP, êtes responsable du traitement au sens du RGPD.

---

## Vos obligations en tant que CGP utilisateur

### 1. Informer vos clients

Vos clients doivent savoir que vous utilisez des outils d'IA pour vous assister. Ajoutez une mention dans votre DER (Document d'Entrée en Relation) — le modèle de clause est disponible dans `skills/cgp-persona/references/rgpd.md`.

### 2. Minimiser les données saisies

N'entrez jamais dans Claude :
- Numéro de sécurité sociale, NIF ou IBAN
- Données de santé
- Combinaison nom complet + adresse + données financières précises

Utilisez des **initiales**, des **âges** (pas de dates de naissance), des **ordres de grandeur** (pas de montants au centime près).

### 3. Inclure les clauses RGPD dans vos documents

Le plugin inclut systématiquement, sur instruction Claude :
- La **clause de protection des données** dans les lettres de mission (incluse dans le modèle de `/rediger lettre de mission` — vérifier sa présence avant envoi)
- Le **pied de confidentialité** dans les comptes-rendus et reportings

Vérifiez que ces clauses sont bien présentes avant envoi et complétez les champs entre crochets (`[email du CGP]`, etc.).

### 4. Tenir votre registre des traitements

Un modèle d'entrée de registre adapté à l'activité CGP est fourni dans `skills/cgp-persona/references/rgpd.md`.

---

## Transferts de données hors UE

Anthropic est une société américaine. Vos données transitent par des serveurs aux États-Unis. Ces transferts sont encadrés par les **Clauses Contractuelles Types (CCT)** de la Commission européenne, incluses dans les conditions d'utilisation d'Anthropic.

Pour vérifier les garanties en vigueur : [privacy.anthropic.com](https://privacy.anthropic.com)

---

## Durée de conservation par Anthropic

Consultez la politique de confidentialité d'Anthropic pour les durées de rétention des conversations. En pratique, Claude ne conserve **aucune mémoire entre les sessions** — chaque conversation repart de zéro.

---

## Contact CNIL

En cas de question sur vos obligations RGPD : [cnil.fr](https://www.cnil.fr) — rubrique "Professionnels".

---

*Ce document est fourni à titre informatif. Il ne constitue pas un avis juridique. Pour une mise en conformité complète, consultez un juriste spécialisé en droit des données.*
