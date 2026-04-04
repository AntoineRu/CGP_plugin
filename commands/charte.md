---
description: 'Configurer la charte graphique du cabinet à partir d''un template Word (.docx)'
argument-hint: '[chemin/vers/template.docx]'
---

# /charte — Configuration de la charte graphique

Tu es l'assistant de configuration de la charte graphique du cabinet. Tu suis les phases ci-dessous dans l'ordre, en utilisant l'outil Bash pour exécuter les commandes. Annonce chaque phase clairement.

---

## Phase 1 — Identifier le template

Si `$ARGUMENTS` est fourni et se termine par `.docx`, c'est le chemin du template.
Sinon, demander à l'utilisateur :

> "Veuillez indiquer le chemin complet vers votre template Word (.docx) :"

Valider que le fichier existe :
```bash
test -f "$TEMPLATE_PATH" && echo "OK" || echo "INTROUVABLE"
```

Si introuvable, arrêter et afficher :
> "Fichier non trouvé : [chemin]. Vérifiez le chemin et relancez `/charte [chemin]`."

---

## Phase 2 — Installer python-docx

Vérifier si python-docx est disponible dans le venv :
```bash
VENV_PY="${CLAUDE_PLUGIN_ROOT}/../.venv/bin/python3"
[ -f "${CLAUDE_PLUGIN_ROOT}/../.venv/Scripts/python.exe" ] && VENV_PY="${CLAUDE_PLUGIN_ROOT}/../.venv/Scripts/python.exe"
"$VENV_PY" -c "import docx; print('OK')" 2>/dev/null || echo "ABSENT"
```

Si absent, installer :
```bash
"$VENV_PY" -m pip install --quiet "python-docx>=1.1"
```

Confirmer l'installation. Si échec, arrêter avec le message d'erreur.

---

## Phase 3 — Analyser le template

Exécuter ce script pour extraire les styles et métadonnées du template :

```bash
"$VENV_PY" - <<'PYEOF'
import os, json, sys
from docx import Document
from docx.oxml.ns import qn

template_path = os.environ.get("TEMPLATE_PATH", "")
doc = Document(template_path)

# Styles disponibles dans le document
styles = {}
for style in doc.styles:
    if style.font and style.font.name:
        styles[style.name] = {
            "font": style.font.name,
            "size": style.font.size.pt if style.font.size else None,
            "bold": style.font.bold,
        }

# Présence des styles standard (avec fallbacks)
STANDARD = ["Normal", "Heading 1", "Heading 2", "Heading 3",
            "List Bullet", "List Number", "Footer", "Header"]
available = [s.name for s in doc.styles]
style_map = {}
for std in STANDARD:
    if std in available:
        style_map[std] = std
    else:
        # chercher un équivalent partiel
        match = next((s for s in available if std.lower() in s.lower()), None)
        style_map[std] = match or std  # fallback au nom standard

# En-tête et pied de page (texte brut)
header_text = ""
footer_text = ""
for section in doc.sections:
    if section.header:
        header_text = " | ".join(p.text for p in section.header.paragraphs if p.text.strip())
    if section.footer:
        footer_text = " | ".join(p.text for p in section.footer.paragraphs if p.text.strip())

# Police majoritaire (corps du texte)
body_font = styles.get("Normal", {}).get("font", "Calibri")
body_size = styles.get("Normal", {}).get("size", 11)
h1_font   = styles.get("Heading 1", {}).get("font", body_font)
h1_size   = styles.get("Heading 1", {}).get("size", 14)

result = {
    "template_path": template_path,
    "style_map": style_map,
    "typography": {
        "body_font": body_font,
        "body_size": body_size,
        "heading_font": h1_font,
        "heading_size": h1_size,
    },
    "header": header_text,
    "footer": footer_text,
    "available_styles": available[:30],  # cap pour lisibilité
}
print(json.dumps(result, ensure_ascii=False, indent=2))
PYEOF
```

> Remplace `os.environ.get("TEMPLATE_PATH", "")` par le chemin réel en passant `TEMPLATE_PATH="[chemin]"` devant la commande.

Conserver le JSON résultant — il est la source de vérité pour les phases suivantes.

---

## Phase 4 — Générer `hooks/charte_config.json`

Écrire le fichier de configuration (chemin absolu du template, style_map) :

```bash
"$VENV_PY" - <<'PYEOF'
import os, json, pathlib

plugin_root = pathlib.Path(os.environ["CLAUDE_PLUGIN_ROOT"])
config_path = plugin_root / "hooks" / "charte_config.json"

# Insérer ici le JSON produit en Phase 3 (style_map + template_path)
config = {
    "template_path": "REMPLACER_PAR_CHEMIN_ABSOLU",
    "style_map": {},  # remplir depuis Phase 3
}
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Écrit : {config_path}")
PYEOF
```

**En pratique** : générer directement le contenu correct à partir des données de Phase 3, sans placeholder.

---

## Phase 5 — Créer le skill `charte-graphique`

Créer `skills/charte-graphique/SKILL.md` avec les règles extraites en Phase 3 :

```markdown
# Charte Graphique — Cabinet [déduire du header si possible]

## Typographie
- Corps du texte : [body_font] [body_size]pt
- Titres : [heading_font] [heading_size]pt

## Structure des documents
- En-tête : [header extrait]
- Pied de page : [footer extrait]

## Règles de mise en forme
- Utilise les styles Word du template : Titre 1 pour les sections principales,
  Titre 2 pour les sous-sections, Corps de texte pour le contenu courant.
- Conserve les formules de politesse et la signature conformes au ton CGP.
- Inclure systématiquement les mentions AMF/CIF en pied de document.

## Activation du rendu Word
Quand tu produis un document `.md` via l'outil Write, le hook `render_docx.py`
génère automatiquement un `.docx` adjacent en appliquant ce template.
```

Créer le dossier si nécessaire :
```bash
mkdir -p "${CLAUDE_PLUGIN_ROOT}/skills/charte-graphique"
```

---

## Phase 6 — Activer le hook render_docx dans `hooks.json`

Lire le `hooks.json` actif et ajouter l'entrée PostToolUse pour render_docx si elle n'y est pas déjà :

```bash
"$VENV_PY" - <<'PYEOF'
import os, json, pathlib

plugin_root = pathlib.Path(os.environ["CLAUDE_PLUGIN_ROOT"])
hooks_path = plugin_root / "hooks" / "hooks.json"

if not hooks_path.exists():
    print("ERREUR : hooks.json introuvable — relancer /setup d'abord")
    raise SystemExit(1)

config = json.loads(hooks_path.read_text(encoding="utf-8"))

venv_py = str(plugin_root / ".." / ".venv" / "bin" / "python3")
import sys
if sys.platform == "win32":
    venv_py = str(plugin_root / ".." / ".venv" / "Scripts" / "python.exe")

new_hook = {
    "type": "command",
    "command": f"{venv_py} \"{plugin_root}/hooks/render_docx.py\"",
    "timeout": 15
}

post = config["hooks"].setdefault("PostToolUse", [])

# Vérifier si déjà présent
already = any(
    h.get("command", "").endswith("render_docx.py")
    for entry in post
    for h in entry.get("hooks", [])
)

if already:
    print("Hook render_docx déjà présent — rien à faire.")
else:
    post.append({"matcher": "Write|Edit", "hooks": [new_hook]})
    hooks_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Hook render_docx ajouté à hooks.json.")
PYEOF
```

---

## Phase 7 — Résumé

Afficher :

```
╔══════════════════════════════════════════════════════╗
║       CGP Assistant — Charte graphique configurée    ║
╠══════════════════════════════════════════════════════╣
║  Template       : [chemin]                           ║
║  Police corps   : [body_font] [body_size]pt          ║
║  Police titres  : [heading_font] [heading_size]pt    ║
║  En-tête        : [header ou "(vide)"]               ║
║  Pied de page   : [footer ou "(vide)"]               ║
║  Hook Word      : ✓ activé (render_docx.py)          ║
╚══════════════════════════════════════════════════════╝
```

Puis :
> **À retenir :** désormais, chaque document `.md` produit via `/rediger`, `/bilan` ou `/dossier` génère automatiquement un `.docx` adjacent stylé avec votre template.
> Pour reconfigurer avec un nouveau template : relancez `/charte [nouveau_chemin.docx]` — le `charte_config.json` sera mis à jour.
