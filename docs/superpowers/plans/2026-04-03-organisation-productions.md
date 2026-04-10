# Organisation des Productions — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Organise every document produced by the CGP plugin into `~/CGP/<Client>/<type>/` or `~/CGP/_cabinet/<type>/`, auto-convert to `.docx`, and let every command offer to save its chat response.

**Architecture:** A single PostToolUse hook `output_router.py` replaces `render_docx.py`. It filters on `.md` files whose names match the `cgp-*` convention, resolves client/cabinet routing, converts Markdown→docx, moves the `.docx` to the right folder, and deletes the source `.md`. Every command gains a save-prompt paragraph at the end. `/setup` creates the base directory tree.

**Tech Stack:** Python 3.8+ (stdlib only for routing logic), `python-docx>=1.1` (docx conversion), Claude Code plugin hooks (PostToolUse).

---

## File Map

| Action | File |
|--------|------|
| Create | `hooks/output_router.py` |
| Delete | `hooks/render_docx.py` |
| Modify | `hooks/hooks.json.example` |
| Modify | `hooks/hooks.json.windows.example` |
| Modify | `commands/setup.md` (Phase 6 + Phase 7 smoke test) |
| Modify | `commands/charte.md` (Phase 6 reference) |
| Modify | `commands/veille.md` |
| Modify | `commands/analyser.md` |
| Modify | `commands/rdv.md` |
| Modify | `commands/bilan.md` |
| Modify | `commands/rediger.md` |
| Modify | `commands/reporting.md` |
| Modify | `commands/dossier.md` |
| Modify | `commands/marketing.md` |
| Modify | `commands/vulgariser.md` |
| Modify | `commands/prospecter.md` |

---

## Task 1: Create `output_router.py` — filter, config bootstrap, type detection

**Files:**
- Create: `hooks/output_router.py`
- Test: manual stdin test (see step 4)

- [ ] **Step 1: Write `hooks/output_router.py` with filter + default config creation + type detection**

```python
#!/usr/bin/env python3
"""
PostToolUse hook — output_router.py

Triggered on every Write/Edit. If the written file is a .md matching the
cgp-* convention, converts it to .docx and moves it to ~/CGP/<routing>/,
then deletes the source .md.

Stdin payload: {"tool_name": "Write", "tool_input": {"file_path": "..."}, ...}
Stdout: nothing (passive hook)
"""

import json
import pathlib
import re
import sys

# Files to route must have this prefix
CGP_PREFIX = "cgp-"
TRIGGER_EXTENSIONS = {".md"}

# Maps filename keyword → (subfolder_in_CGP, is_cabinet)
TYPE_MAP = [
    ("bilan",       ("bilans",          False)),
    ("rediger",     ("lettres",         False)),
    ("lettre",      ("lettres",         False)),
    ("mission",     ("lettres",         False)),
    ("-cr-",        ("lettres",         False)),
    ("analyser",    ("analyses",        False)),
    ("analyse",     ("analyses",        False)),
    ("rdv",         ("rendez-vous",     False)),
    ("rendez-vous", ("rendez-vous",     False)),
    ("reporting",   ("reporting",       False)),
    ("dossier",     ("reporting",       False)),
    ("rapport",     ("reporting",       False)),
    ("veille",      ("veille",          True)),
    ("vulgariser",  ("vulgarisation",   True)),
    ("vulgaris",    ("vulgarisation",   True)),
    ("marketing",   ("marketing",       True)),
    ("prospecter",  ("prospection",     True)),
    ("prospect",    ("prospection",     True)),
]

DEFAULT_CONFIG = {
    "template_path": None,
    "style_map": {
        "Heading 1": "Heading 1",
        "Heading 2": "Heading 2",
        "Heading 3": "Heading 3",
        "Normal": "Normal",
        "List Bullet": "List Bullet",
        "List Number": "List Number",
    },
    "typography": {
        "body_font": "Calibri",
        "body_size": 11,
        "heading_font": "Calibri",
        "heading_size": 14,
    },
}


def load_or_create_config() -> dict:
    config_path = pathlib.Path(__file__).parent / "charte_config.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Create default config
    config_path.write_text(
        json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    sys.stderr.write("[cgp] charte_config.json absent — paramètres par défaut utilisés\n")
    return DEFAULT_CONFIG


def detect_type(stem: str) -> tuple[str, bool]:
    """Return (subfolder, is_cabinet). Defaults to ('_cabinet/divers', True)."""
    lower = stem.lower()
    for keyword, result in TYPE_MAP:
        if keyword in lower:
            return result
    return ("divers", True)


def detect_client(md_content: str) -> str | None:
    """Search md_content for known real names from the RGPD registry.
    Returns the real name (for folder naming) or None if not found."""
    registry_path = pathlib.Path.home() / ".cgp-client-registry.json"
    if not registry_path.exists():
        return None
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    real_names = list(registry.get("real_to_pseudo", {}).keys())
    # Longest match first to avoid partial matches
    real_names.sort(key=len, reverse=True)
    for name in real_names:
        if name.lower() in md_content.lower():
            return name
    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    if payload.get("tool_name") not in ("Write", "Edit"):
        return

    file_path = payload.get("tool_input", {}).get("file_path", "")
    md_path = pathlib.Path(file_path)

    if md_path.suffix not in TRIGGER_EXTENSIONS:
        return
    if not md_path.name.startswith(CGP_PREFIX):
        return
    if not md_path.exists():
        return

    config = load_or_create_config()
    md_content = md_path.read_text(encoding="utf-8")

    subfolder, is_cabinet = detect_type(md_path.stem)
    client_name = None if is_cabinet else detect_client(md_content)

    # Routing
    cgp_root = pathlib.Path.home() / "CGP"
    if is_cabinet or client_name is None:
        target_dir = cgp_root / "_cabinet" / subfolder
    else:
        # Sanitise client name for filesystem (keep letters, digits, spaces, hyphens)
        safe_name = re.sub(r"[^\w\s\-]", "", client_name).strip()
        target_dir = cgp_root / safe_name / subfolder

    target_dir.mkdir(parents=True, exist_ok=True)

    # Build output filename: YYYY-MM-DD_<type>_<Client>.docx or YYYY-MM-DD_<type>.docx
    import datetime
    date_str = datetime.date.today().isoformat()
    type_slug = subfolder.replace("-", "").replace("/", "")
    if client_name:
        last_name = client_name.split()[-1]
        out_name = f"{date_str}_{type_slug}_{last_name}.docx"
    else:
        out_name = f"{date_str}_{type_slug}.docx"

    out_path = target_dir / out_name

    # Convert Markdown → docx
    try:
        _md_to_docx(md_path, out_path, config)
    except ImportError:
        sys.stderr.write("[cgp] python-docx manquant — relancer /charte ou /setup\n")
        return
    except Exception as exc:
        sys.stderr.write(f"[cgp] erreur conversion : {exc}\n")
        return

    # Delete source .md
    try:
        md_path.unlink()
    except Exception:
        pass

    sys.stderr.write(f"[cgp] → {out_path}\n")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the file was created**

```bash
ls -lh cgp-assistant/hooks/output_router.py
```

Expected: file exists, ~4-5 KB.

- [ ] **Step 3: Smoke-test filter (non-cgp file → silent exit)**

```bash
VENV_PY=".venv/bin/python3"
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/random.md"}}' \
  | CLAUDE_PLUGIN_ROOT="$(pwd)/cgp-assistant" "$VENV_PY" cgp-assistant/hooks/output_router.py
echo "exit: $?"
```

Expected: no output, exit 0.

- [ ] **Step 4: Smoke-test default config creation**

```bash
VENV_PY=".venv/bin/python3"
# Temporarily hide charte_config.json if it exists
mv cgp-assistant/hooks/charte_config.json /tmp/charte_backup.json 2>/dev/null || true
# Write a test .md file with cgp- prefix
echo "# Test" > /tmp/cgp-bilan-20260403.md
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/cgp-bilan-20260403.md"}}' \
  | CLAUDE_PLUGIN_ROOT="$(pwd)/cgp-assistant" "$VENV_PY" cgp-assistant/hooks/output_router.py 2>&1
```

Expected stderr contains: `[cgp] charte_config.json absent — paramètres par défaut utilisés`
Expected: `cgp-assistant/hooks/charte_config.json` created with `"template_path": null`.

```bash
cat cgp-assistant/hooks/charte_config.json
# Restore
mv /tmp/charte_backup.json cgp-assistant/hooks/charte_config.json 2>/dev/null || true
```

- [ ] **Step 5: Commit**

```bash
git -C cgp-assistant add hooks/output_router.py
git -C cgp-assistant commit -m "feat: add output_router.py — file routing + default charte bootstrap"
```

---

## Task 2: Add `_md_to_docx` conversion logic to `output_router.py`

The `main()` function above calls `_md_to_docx` which doesn't exist yet. Add it now.

**Files:**
- Modify: `hooks/output_router.py` (add `_md_to_docx` before `main()`)

- [ ] **Step 1: Add `_md_to_docx` function to `output_router.py`**

Insert this block immediately before the `def main():` line:

```python
def _apply_inline(para, text: str) -> None:
    """Apply **bold** and *italic* inline markers."""
    parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            para.add_run(part[2:-2]).bold = True
        elif part.startswith("*") and part.endswith("*"):
            para.add_run(part[1:-1]).italic = True
        else:
            para.add_run(part)


def _md_to_docx(md_path: pathlib.Path, out_path: pathlib.Path, config: dict) -> None:
    """Convert a Markdown file to .docx at out_path using config."""
    from docx import Document  # type: ignore

    template_path = config.get("template_path")
    style_map: dict = config.get("style_map", {})

    def style(key: str) -> str:
        return style_map.get(key, key)

    if template_path:
        tp = pathlib.Path(template_path)
        if not tp.exists():
            raise FileNotFoundError(f"Template introuvable : {tp}")
        doc = Document(str(tp))
        # Clear body content, keep styles/headers/footers
        body = doc.element.body
        for child in list(body):
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag in ("p", "tbl"):
                body.remove(child)
    else:
        doc = Document()

    lines = md_path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        stripped = line.rstrip()

        if stripped.startswith("### "):
            doc.add_paragraph(stripped[4:], style=style("Heading 3"))
        elif stripped.startswith("## "):
            doc.add_paragraph(stripped[3:], style=style("Heading 2"))
        elif stripped.startswith("# "):
            doc.add_paragraph(stripped[2:], style=style("Heading 1"))
        elif re.match(r"^[-*] ", stripped):
            doc.add_paragraph(stripped[2:], style=style("List Bullet"))
        elif re.match(r"^\d+\. ", stripped):
            doc.add_paragraph(re.sub(r"^\d+\. ", "", stripped), style=style("List Number"))
        elif re.match(r"^---+$", stripped):
            doc.add_paragraph("", style=style("Normal"))
        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not all(re.match(r"^[-:]+$", c) for c in cells):
                doc.add_paragraph("\t".join(cells), style=style("Normal"))
        elif stripped == "":
            pass
        else:
            para = doc.add_paragraph(style=style("Normal"))
            _apply_inline(para, stripped)

    doc.save(str(out_path))
```

- [ ] **Step 2: Full end-to-end smoke test (cabinet file)**

```bash
VENV_PY=".venv/bin/python3"
# Create a test cabinet veille file
cat > /tmp/cgp-veille-20260403.md << 'EOF'
# Veille réglementaire — Avril 2026

## Nouveautés fiscales

- Acompte IR : échéance 15 juin
- PER : plafond inchangé pour 2026

## Sources consultées

Direction Générale des Finances Publiques, AMF.
EOF

echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/cgp-veille-20260403.md"}}' \
  | CLAUDE_PLUGIN_ROOT="$(pwd)/cgp-assistant" "$VENV_PY" cgp-assistant/hooks/output_router.py 2>&1
```

Expected stderr: `[cgp] → /root/CGP/_cabinet/veille/2026-04-03_veille.docx` (or `~` expanded).
Expected: `/tmp/cgp-veille-20260403.md` deleted. `.docx` exists in `~/CGP/_cabinet/veille/`.

```bash
ls ~/CGP/_cabinet/veille/
# Should show: 2026-04-03_veille.docx
```

- [ ] **Step 3: Full end-to-end smoke test (client file)**

First register a test client:

```bash
VENV_PY=".venv/bin/python3"
"$VENV_PY" cgp-assistant/hooks/anonymize.py register "Marie Durand"
```

Then test routing to client folder:

```bash
cat > /tmp/cgp-bilan-MarieDurand-20260403.md << 'EOF'
# Bilan patrimonial — Marie Durand

## Situation actuelle

Patrimoine net estimé à 450 000 €.
EOF

echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/cgp-bilan-MarieDurand-20260403.md"}}' \
  | CLAUDE_PLUGIN_ROOT="$(pwd)/cgp-assistant" "$VENV_PY" cgp-assistant/hooks/output_router.py 2>&1

ls ~/CGP/
ls ~/CGP/"Marie Durand"/bilans/ 2>/dev/null || ls ~/CGP/Marie\ Durand/bilans/
```

Expected: `2026-04-03_bilans_Durand.docx` in `~/CGP/Marie Durand/bilans/`.

Clean up test client:

```bash
"$VENV_PY" -c "
import json, pathlib
p = pathlib.Path.home() / '.cgp-client-registry.json'
r = json.loads(p.read_text())
pseudo = r['real_to_pseudo'].pop('Marie Durand', None)
if pseudo: r['pseudo_to_real'].pop(pseudo, None)
p.write_text(json.dumps(r, indent=2))
print('cleaned')
"
```

- [ ] **Step 4: Commit**

```bash
git -C cgp-assistant add hooks/output_router.py
git -C cgp-assistant commit -m "feat: add md_to_docx conversion to output_router.py"
```

---

## Task 3: Delete `render_docx.py` and update hook templates

**Files:**
- Delete: `hooks/render_docx.py`
- Modify: `hooks/hooks.json.example`
- Modify: `hooks/hooks.json.windows.example`

- [ ] **Step 1: Delete `render_docx.py`**

```bash
git -C cgp-assistant rm hooks/render_docx.py
```

- [ ] **Step 2: Update `hooks/hooks.json.example`**

Replace the PostToolUse entry. The file currently contains:

```json
"command": "${CLAUDE_PLUGIN_ROOT}/../.venv/bin/python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py\" decode"
```

Replace the entire PostToolUse section so it reads:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/../.venv/bin/python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py\" decode",
        "timeout": 5
      },
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/../.venv/bin/python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/output_router.py\"",
        "timeout": 15
      }
    ]
  }
]
```

- [ ] **Step 3: Update `hooks/hooks.json.windows.example`**

Same change as Step 2 but with `Scripts/python.exe`:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/../.venv/Scripts/python.exe \"${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py\" decode",
        "timeout": 5
      },
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/../.venv/Scripts/python.exe \"${CLAUDE_PLUGIN_ROOT}/hooks/output_router.py\"",
        "timeout": 15
      }
    ]
  }
]
```

- [ ] **Step 4: Verify both example files are valid JSON**

```bash
python3 -c "import json; json.load(open('cgp-assistant/hooks/hooks.json.example')); print('OK linux')"
python3 -c "import json; json.load(open('cgp-assistant/hooks/hooks.json.windows.example')); print('OK windows')"
```

Expected: `OK linux` and `OK windows`.

- [ ] **Step 5: Commit**

```bash
git -C cgp-assistant add hooks/hooks.json.example hooks/hooks.json.windows.example
git -C cgp-assistant commit -m "feat: replace render_docx with output_router in hook templates"
```

---

## Task 4: Update `/setup` — create `~/CGP/` tree in Phase 6

**Files:**
- Modify: `commands/setup.md` (Phase 6 and Phase 7)

- [ ] **Step 1: Add `~/CGP/` directory creation to Phase 6**

In `commands/setup.md`, after the `chmod 700 "$HOME/cgp-clients-private"` block and before the RGPD registry check, insert:

```markdown
Create the CGP productions directory tree:
```bash
mkdir -p "$HOME/CGP/_cabinet/veille"
mkdir -p "$HOME/CGP/_cabinet/vulgarisation"
mkdir -p "$HOME/CGP/_cabinet/marketing"
mkdir -p "$HOME/CGP/_cabinet/prospection"
```

Explain to the user:
- `~/CGP/` — root for all documents produced by the plugin
- `~/CGP/_cabinet/` — productions not linked to a specific client (veille, marketing, etc.)
- `~/CGP/<Client>/` — created automatically when the first document for that client is saved
```

- [ ] **Step 2: Add `output_router.py` smoke test to Phase 7**

In `commands/setup.md`, Phase 7, add after the `client_store.py` test:

```markdown
**output_router.py — filter (non-cgp file):**
```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/not-cgp.md"}}' \
  | "$VENV_PYTHON" "${CLAUDE_PLUGIN_ROOT}/hooks/output_router.py" && echo "PASS" || echo "FAIL"
```
Expected: PASS with no output (non-cgp file correctly ignored).
```

- [ ] **Step 3: Verify the setup.md changes look correct**

```bash
grep -n "CGP/_cabinet" cgp-assistant/commands/setup.md
grep -n "output_router" cgp-assistant/commands/setup.md
```

Expected: both greps return matches.

- [ ] **Step 4: Commit**

```bash
git -C cgp-assistant add commands/setup.md
git -C cgp-assistant commit -m "feat: setup creates ~/CGP/ tree, adds output_router smoke test"
```

---

## Task 5: Update `/charte` Phase 6 — reference `output_router.py`

**Files:**
- Modify: `commands/charte.md`

- [ ] **Step 1: Update Phase 6 of `charte.md`**

In `commands/charte.md` Phase 6, find the string `render_docx.py` and replace all occurrences with `output_router.py`.

Verify:

```bash
grep -n "render_docx\|output_router" cgp-assistant/commands/charte.md
```

Expected: only `output_router.py` appears.

- [ ] **Step 2: Commit**

```bash
git -C cgp-assistant add commands/charte.md
git -C cgp-assistant commit -m "fix: charte.md Phase 6 references output_router.py"
```

---

## Task 6: Add save-prompt to client commands

Add the save-prompt paragraph to `/bilan`, `/rediger`, `/reporting`, `/dossier`, `/analyser`, `/rdv`.

These are **client** commands — the filename includes the client name.

**Files:**
- Modify: `commands/bilan.md`
- Modify: `commands/rediger.md`
- Modify: `commands/reporting.md`
- Modify: `commands/dossier.md`
- Modify: `commands/analyser.md`
- Modify: `commands/rdv.md`

- [ ] **Step 1: Add save-prompt to `bilan.md`**

Append to the end of `commands/bilan.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-bilan-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant
(remplace `<NomClient>` par le nom du client sans espaces, `<YYYYMMDD>` par la date du jour).
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/bilans/`.
```

- [ ] **Step 2: Add save-prompt to `rediger.md`**

Append to the end of `commands/rediger.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-rediger-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/lettres/`.
```

- [ ] **Step 3: Add save-prompt to `reporting.md`**

Append to the end of `commands/reporting.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-reporting-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/reporting/`.
```

- [ ] **Step 4: Add save-prompt to `dossier.md`**

Append to the end of `commands/dossier.md`:

```markdown
---

## Sauvegarde

Le rapport final généré par l'agent `redacteur-cgp` est déjà enregistré sous
`rapport-conseil-<NomClient>-<YYYYMMDD>.md`. Renomme-le en
`cgp-dossier-<NomClient>-<YYYYMMDD>.md` avant de confirmer la fin de la commande,
afin que `output_router.py` le détecte et le range dans `~/CGP/<Client>/reporting/`.
```

- [ ] **Step 5: Add save-prompt to `analyser.md`**

Append to the end of `commands/analyser.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-analyser-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/analyses/`.
```

- [ ] **Step 6: Add save-prompt to `rdv.md`**

Append to the end of `commands/rdv.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-rdv-<NomClient>-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/<Client>/rendez-vous/`.
```

- [ ] **Step 7: Commit**

```bash
git -C cgp-assistant add commands/bilan.md commands/rediger.md commands/reporting.md \
  commands/dossier.md commands/analyser.md commands/rdv.md
git -C cgp-assistant commit -m "feat: add save-prompt to client commands"
```

---

## Task 7: Add save-prompt to cabinet commands

**Files:**
- Modify: `commands/veille.md`
- Modify: `commands/marketing.md`
- Modify: `commands/vulgariser.md`
- Modify: `commands/prospecter.md`

- [ ] **Step 1: Add save-prompt to `veille.md`**

Append to the end of `commands/veille.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-veille-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/_cabinet/veille/`.
```

- [ ] **Step 2: Add save-prompt to `marketing.md`**

Append to the end of `commands/marketing.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-marketing-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/_cabinet/marketing/`.
```

- [ ] **Step 3: Add save-prompt to `vulgariser.md`**

Append to the end of `commands/vulgariser.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-vulgariser-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/_cabinet/vulgarisation/`.
```

- [ ] **Step 4: Add save-prompt to `prospecter.md`**

Append to the end of `commands/prospecter.md`:

```markdown
---

## Sauvegarde

À la fin de ta réponse, propose à l'utilisateur :
> "Voulez-vous sauvegarder cette réponse ? (oui / non)"

Si oui : écris le contenu complet de ta réponse dans un fichier nommé
`cgp-prospecter-<YYYYMMDD>.md` dans le répertoire courant.
Le hook `output_router.py` convertira automatiquement ce fichier en `.docx` et le rangera
dans `~/CGP/_cabinet/prospection/`.
```

- [ ] **Step 5: Commit**

```bash
git -C cgp-assistant add commands/veille.md commands/marketing.md \
  commands/vulgariser.md commands/prospecter.md
git -C cgp-assistant commit -m "feat: add save-prompt to cabinet commands"
```

---

## Task 8: Final integration test

- [ ] **Step 1: Run full setup smoke tests**

```bash
VENV_PY=".venv/bin/python3"
PLUGIN_ROOT="$(pwd)/cgp-assistant"

# fiscal_alerts
rm -f ~/.cgp-last-fiscal-alert
echo '{}' | "$VENV_PY" "$PLUGIN_ROOT/hooks/fiscal_alerts.py" && echo "PASS fiscal_alerts" || echo "FAIL fiscal_alerts"

# anonymize list
"$VENV_PY" "$PLUGIN_ROOT/hooks/anonymize.py" list && echo "PASS anonymize" || echo "FAIL anonymize"

# client_store list
"$VENV_PY" "$PLUGIN_ROOT/hooks/client_store.py" list && echo "PASS client_store" || echo "FAIL client_store"

# output_router filter
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/not-cgp.md"}}' \
  | "$VENV_PY" "$PLUGIN_ROOT/hooks/output_router.py" && echo "PASS output_router filter" || echo "FAIL output_router filter"
```

Expected: all PASS.

- [ ] **Step 2: Verify ~/CGP tree exists**

```bash
ls ~/CGP/_cabinet/
```

Expected: `veille/  vulgarisation/  marketing/  prospection/`

- [ ] **Step 3: Verify no references to `render_docx.py` remain**

```bash
grep -r "render_docx" cgp-assistant/ --include="*.md" --include="*.json" --include="*.py"
```

Expected: no output.

- [ ] **Step 4: Final commit**

```bash
git -C cgp-assistant log --oneline -8
```

Review the commit list — should show all tasks. Tag if desired:

```bash
git -C cgp-assistant tag v0.4-output-router
```
