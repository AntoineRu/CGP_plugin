---
name: rediger
description: This skill should be used when the user invokes /rediger, asks to "rédiger", "écrire", "rédige-moi", "prépare un document", "écris une lettre", "fais un compte-rendu", "rédige un rapport", "prépare une lettre de mission", "rédige une note de synthèse", or needs any client-facing or internal CGP document drafted. Always combine with cgp-persona for professional tone and compliance. Use profil-client if client information is available.
---

# Rédiger — Documents CGP

Ce skill gouverne la rédaction de tous les documents professionnels d'un CGP : lettres, rapports, comptes-rendus, notes de synthèse et propositions commerciales.

## Processus de rédaction

### Étape 1 — Identifier le type de document
Déterminer parmi les types ci-dessous lequel correspond à la demande. Si ambigu, poser une seule question de clarification.

### Étape 2 — Collecter les informations manquantes
Chaque type de document a ses données minimales requises (listées ci-dessous). Si des données critiques manquent, demander en une seule fois avant de rédiger.

### Étape 3 — Rédiger selon le format du type
Utiliser le format standard du type concerné. Adapter le ton et le niveau de détail au destinataire (client vs. usage interne).

### Étape 4 — Vérification conformité
Vérifier que les mentions obligatoires issues de `cgp-persona` sont incluses si le document traite d'investissement ou de conseil.

---

## Types de documents et formats

### 1. Lettre de mission
**Usage :** Formalise la relation CGP-client, obligatoire réglementairement.
**Données requises :** Nom client, nature de la mission, périmètre, durée, rémunération.

```
[Ville], le [date]

[Prénom NOM Client]
[Adresse]

Objet : Lettre de mission — Conseil en gestion de patrimoine

Madame / Monsieur [Nom],

À la suite de notre entretien du [date], j'ai l'honneur de vous soumettre la présente lettre de mission définissant le cadre de notre collaboration.

**1. Nature de la mission**
[Description précise : conseil en investissement, bilan patrimonial, optimisation fiscale, etc.]

**2. Périmètre de la mission**
[Ce qui est inclus et ce qui est exclu explicitement]

**3. Engagements réciproques**
De votre côté : [liste]
De mon côté : [liste]

**4. Durée et renouvellement**
La présente mission est conclue pour une durée de [X] mois / an, renouvelable par tacite reconduction.

**5. Rémunération**
[Mode et montant de rémunération — transparence MIF II]

**6. Confidentialité et données personnelles**
*Conformément au Règlement (UE) 2016/679 (RGPD), les données personnelles collectées dans le cadre de cette mission sont traitées par [Nom du CGP] en qualité de responsable du traitement, sur la base légale de l'exécution du contrat. Vous disposez d'un droit d'accès, de rectification, d'effacement et de portabilité de vos données. Pour exercer ces droits : [email du CGP].*

Je reste à votre disposition pour tout complément d'information.

Veuillez agréer, Madame / Monsieur, l'expression de mes salutations distinguées.

[Prénom NOM du CGP]
[Titre — Statut CIF]
[Coordonnées]

Lu et approuvé :
Signature client : _________________    Date : ___________
```

---

### 2. Rapport de conseil
**Usage :** Synthèse formelle d'une recommandation d'investissement ou patrimoniale.
**Données requises :** Profil client, situation analysée, recommandation(s), justification(s).

```
RAPPORT DE CONSEIL PATRIMONIAL

Client : [Prénom NOM]            Date : [JJ/MM/AAAA]
Conseiller : [Nom CGP]           Référence dossier : [REF]

---

1. RAPPEL DE LA SITUATION

[Résumé de la situation patrimoniale, familiale et fiscale du client en 5-10 lignes]

2. OBJECTIFS IDENTIFIÉS

- Objectif principal : [X]
- Objectif secondaire : [Y]
- Horizon d'investissement : [X ans]
- Profil de risque validé : [Prudent / Équilibré / Dynamique]

3. ANALYSE

[Analyse de la situation actuelle : points forts, points à optimiser, risques identifiés]

4. RECOMMANDATIONS

4.1 [Première recommandation]
Justification : [Pourquoi cette recommandation correspond au profil]
Montant / allocation suggérée : [X €]
Produit(s) concerné(s) : [Nom produit — émetteur]

4.2 [Deuxième recommandation si applicable]
[Même structure]

5. ALTERNATIVES ENVISAGÉES

[Autres options considérées et pourquoi elles ont été écartées ou proposées en complément]

6. POINTS DE VIGILANCE

[Risques, contraintes de liquidité, fiscalité à surveiller]

---

*Ce rapport est établi à titre informatif sur la base des informations communiquées par le client. Il ne constitue pas un conseil en investissement personnalisé au sens de la directive MIF II sans validation des éléments du profil. Les performances passées ne préjugent pas des performances futures.*

Signature CGP : _________________    Date : ___________
```

---

### 3. Compte-rendu de réunion
**Usage :** Trace écrite d'un rendez-vous client — recommandé après chaque RDV.
**Données requises :** Date, participants, points abordés, décisions, prochaines étapes.

```
COMPTE-RENDU DE RÉUNION

Date : [JJ/MM/AAAA]    Heure : [HH:MM]    Durée : [X min]
Lieu / Format : [En personne / Visioconférence / Téléphone]
Présents : [Prénom NOM Client] — [Prénom NOM CGP]
Objet : [Intitulé de la réunion]

---

POINTS ABORDÉS

1. [Premier point]
   → [Résumé de la discussion]

2. [Deuxième point]
   → [Résumé de la discussion]

3. [Troisième point]
   → [Résumé de la discussion]

DÉCISIONS PRISES

- [Décision 1]
- [Décision 2]

POINTS D'ACTION

| Action | Responsable | Délai |
|---|---|---|
| [Action 1] | [CGP / Client] | [Date] |
| [Action 2] | [CGP / Client] | [Date] |

PROCHAIN RENDEZ-VOUS

Date : [À définir / JJ/MM/AAAA]    Objet : [Objet prévu]

---

Document établi par [Prénom NOM CGP] le [date].
*Ce document est confidentiel. Il sera archivé au dossier client conformément aux obligations réglementaires.*
```

---

### 4. Lettre de suivi client
**Usage :** Communication régulière après une décision, un événement de marché ou en suivi de portefeuille.
**Données requises :** Nom client, objet du suivi, informations à communiquer.

```
[Ville], le [date]

[Prénom NOM Client]

Objet : [Suivi de votre portefeuille / Point sur votre investissement en X / etc.]

Madame / Monsieur [Nom],

[Paragraphe d'accroche : contexte ou rappel de la dernière interaction]

[Corps : informations à communiquer, évolution, point de situation]

[Si nécessaire : proposition d'action ou de rendez-vous]

Je reste naturellement disponible pour tout échange sur ces points.

Bien cordialement,

[Prénom NOM du CGP]
[Coordonnées]
```

---

### 5. Note de synthèse
**Usage :** Synthèse interne ou à remettre au client sur un sujet (produit, loi, stratégie).
**Données requises :** Sujet de la note, public cible (interne / client), niveau de détail souhaité.

Structure : Titre — Contexte — Points clés (3-5 max) — Implications pratiques — Sources si pertinentes.

---

### 6. Email professionnel
**Usage :** Communication courante avec clients, notaires, avocats, comptables, partenaires.
**Données requises :** Destinataire, objet, message principal, action attendue.

Ton : direct et professionnel. Corps : 3-5 phrases max. Toujours préciser l'action attendue en fin d'email.

---

## Règles de style transversales

- Toujours utiliser "Madame / Monsieur" dans les courriers (sauf instruction contraire)
- Date en toutes lettres dans les documents formels : "le 15 avril 2025"
- Chiffres en euros : "150 000 €" (avec espace insécable, pas de virgule)
- Sigles écrits en toutes lettres à la première occurrence : "Plan d'Épargne Retraite (PER)"
- Jamais de promesses de rendement dans les documents clients

## Ressources complémentaires

- **`references/formules-politesse.md`** — Formules d'entrée et de sortie selon le contexte
- **`assets/`** — Templates vierges par type de document
