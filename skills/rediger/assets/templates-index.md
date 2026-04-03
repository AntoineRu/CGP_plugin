# Index des templates — Skill Rédiger

Ce fichier est une aide à la navigation. Les formats complets de chaque type de document sont définis inline dans `skills/rediger/SKILL.md`.

---

## Types de documents disponibles

| # | Type de document       | Usage principal                                                                 |
|---|------------------------|---------------------------------------------------------------------------------|
| 1 | **Lettre de mission**  | Formalise la relation CGP-client ; document réglementaire obligatoire (CIF/AMF) |
| 2 | **Rapport de conseil** | Synthèse formelle d'une recommandation patrimoniale ou d'investissement          |
| 3 | **Compte-rendu de réunion** | Trace écrite d'un rendez-vous client — recommandé après chaque entretien   |
| 4 | **Lettre de suivi client** | Communication périodique après une décision, un événement ou un suivi de portefeuille |
| 5 | **Note de synthèse**   | Synthèse interne ou client sur un produit, une loi ou une stratégie patrimoniale |
| 6 | **Email professionnel**| Communication courante avec clients, notaires, avocats, comptables, partenaires  |

---

## Comment utiliser ce skill

Invoquer `/rediger` en précisant le type de document souhaité et les informations disponibles. Claude identifiera le format approprié, demandera les données manquantes si nécessaire, puis rédigera le document selon le format standard défini dans `SKILL.md`.

**Exemples d'invocation :**
- `/rediger une lettre de mission pour [client] — mission de bilan patrimonial`
- `/rediger un compte-rendu du RDV d'hier avec [client]`
- `/rediger un email pour [notaire] concernant la succession de [client]`

## Ressources associées

- `skills/rediger/SKILL.md` — Formats complets, données requises par type, règles de style
- `skills/rediger/references/formules-politesse.md` — Formules d'ouverture et de clôture selon le contexte
- `skills/cgp-persona/SKILL.md` — Ton professionnel et mentions de conformité obligatoires
