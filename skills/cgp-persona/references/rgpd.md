# RGPD — Référence pour le CGP

## Cadre juridique applicable

Le CGP est soumis au **Règlement (UE) 2016/679 (RGPD)** en tant que responsable du traitement des données personnelles de ses clients. L'utilisation de Claude (Anthropic) introduit une chaîne de sous-traitance à encadrer.

---

## Rôles et responsabilités

| Acteur | Rôle RGPD | Obligations |
|---|---|---|
| Le CGP | Responsable du traitement | Informer les clients, tenir un registre, garantir la sécurité |
| Anthropic (Claude) | Sous-traitant | Traite les données selon les instructions du CGP |
| Le client final | Personne concernée | Droits d'accès, rectification, effacement, portabilité |

**Point de vigilance** : Anthropic est une société américaine. Le transfert de données hors UE est encadré par les Clauses Contractuelles Types (CCT) de la Commission européenne. Vérifier que le contrat avec Anthropic les inclut.

---

## Clause RGPD — Lettre de mission (à insérer systématiquement)

```
PROTECTION DES DONNÉES PERSONNELLES

Les données personnelles vous concernant collectées dans le cadre de la
présente mission sont traitées par [Nom / Raison sociale du CGP],
[Adresse], en qualité de responsable du traitement.

Finalité : exécution de la mission de conseil en gestion de patrimoine.
Base légale : exécution du contrat (art. 6.1.b RGPD).
Durée de conservation : 5 ans après la fin de la relation contractuelle
(délai de prescription civile), 10 ans pour les documents comptables.

Vos droits : accès, rectification, effacement, limitation, portabilité,
opposition — à exercer à [email du CGP] ou [adresse postale].
Vous pouvez également introduire une réclamation auprès de la CNIL
(www.cnil.fr).

Dans le cadre de cette mission, certaines données peuvent être traitées
par des outils d'intelligence artificielle opérés par des sous-traitants
sélectionnés pour leur conformité au RGPD. Aucune donnée n'est cédée
à des tiers à des fins commerciales.
```

---

## Clause de confidentialité — Pied de document (comptes-rendus, notes)

```
Document confidentiel — destiné exclusivement à [Nom du destinataire].
Toute reproduction ou transmission à un tiers est interdite sans accord
préalable du [Nom du CGP]. Données personnelles traitées conformément
au RGPD — droits à exercer auprès de [email].
```

---

## Registre des traitements — Entrée type pour l'activité CGP

Le CGP doit tenir un registre des traitements (art. 30 RGPD). Voici l'entrée type pour l'activité conseil :

| Champ | Valeur |
|---|---|
| Nom du traitement | Conseil en gestion de patrimoine |
| Responsable | [Nom du CGP] |
| Finalité | Analyse patrimoniale, conseil en investissement, suivi client |
| Base légale | Exécution du contrat |
| Catégories de données | Identité, situation familiale, revenus, patrimoine, objectifs |
| Personnes concernées | Clients particuliers et professionnels |
| Destinataires | CGP, sous-traitants IT, dépositaires (avec accord client) |
| Durée de conservation | 5 ans post-contrat (10 ans documents comptables) |
| Transferts hors UE | Oui — outils IA (Anthropic/Claude) — encadrés par CCT |
| Mesures de sécurité | Chiffrement, accès restreint, pseudonymisation recommandée |

---

## Bonnes pratiques — Utilisation de Claude

### Données à ne JAMAIS saisir dans Claude
- Numéro de sécurité sociale
- Numéro fiscal (NIF/SPI)
- Numéro de compte bancaire ou IBAN
- Données de santé
- Données biométriques
- Opinions politiques, religieuses ou philosophiques

### Données à anonymiser avant saisie
- Nom complet → initiales ou prénom seul ("Martin D." ou "client A")
- Adresse exacte → ville et code postal uniquement
- Montants précis → ordres de grandeur ("environ 180 000 €")
- Date de naissance → âge ("52 ans")
- Employeur → secteur d'activité ("cadre dans l'industrie pharmaceutique")

### Exemple de saisie conforme vs non conforme

❌ **Non conforme** :
```
Martin DUPONT, né le 14/03/1972, 14 rue des Lilas 75011 Paris,
NIF 12345678901, revenus nets 2024 : 97 342 €, AV Cardif n°FR123456...
```

✅ **Conforme** :
```
Client M.D., 52 ans, Paris 11e, cadre supérieur, TMI 41%.
Revenus ~97k€. AV ~120k€ chez un assureur français.
```

---

## Information client — Clause à intégrer dans le DER

Le Document d'Entrée en Relation (DER) doit mentionner l'utilisation d'outils d'IA :

```
Dans le cadre de notre mission, nous utilisons des outils d'assistance
numérique, dont des solutions d'intelligence artificielle, pour améliorer
la qualité et la rapidité de nos services (rédaction de documents,
analyse de données patrimoniales). Ces outils sont sélectionnés pour
leur conformité au RGPD. Ils n'ont accès qu'aux données strictement
nécessaires à l'exécution de votre dossier. Aucune décision automatisée
n'est prise sans validation humaine de votre conseiller.
```

---

## Ressources officielles

- CNIL — Guide RGPD pour les professionnels : cnil.fr/fr/professionnels
- CNIL — Registre de traitement simplifié : cnil.fr/fr/registre-de-traitements
- AMF — Données personnelles et conformité : amf-france.org
- Clauses Contractuelles Types CE : eur-lex.europa.eu
