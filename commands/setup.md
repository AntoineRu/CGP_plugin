---
description: 'First-run setup: install uv, create venv, configure hooks, verify installation'
argument-hint: ''
---

# /setup — CGP Assistant Initial Configuration

You are the setup assistant for the CGP Assistant plugin. Walk through each phase below in order, using your Bash tool to run commands. Announce each phase clearly and report what you find/do. Stop and ask the user before any destructive action.

**Important:** `$PROJECT_DIR` refers to the current working directory (`pwd`) at the time this command runs — it is the user's Claude Code project root.

---

## Phase 1 — Detect Operating System and Shell Environment

Run:
```bash
uname -s 2>/dev/null || echo "windows"
```

Also check for WSL:
```bash
uname -r 2>/dev/null | grep -i microsoft && echo "WSL" || true
```

Classify the environment as one of:
- **WSL** (Windows Subsystem for Linux) — treat as Linux for paths and commands
- **Linux** (native)
- **macOS**
- **Windows** (Git Bash / PowerShell — paths use backslash, `python` not `python3`)

Announce: "Environment detected: [env]"

---

## Phase 2 — Find or Install uv

Check if uv is available:

```bash
uv --version 2>/dev/null || echo "absent"
```

**If uv is found**, announce: "uv [version] trouvé" and proceed to Phase 3.

**If uv is not found**, display the installation instructions adapted to the detected OS:

> ### uv non trouvé — Installation requise
>
> `uv` est le gestionnaire Python utilisé par ce plugin. Installez-le avant de continuer :
>
> **Linux / macOS / WSL :**
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
>
> **Windows (PowerShell) :**
> ```powershell
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> ```
>
> Après installation, redémarrez votre terminal et relancez `/setup`.

Do not continue to Phase 3.

---

## Phase 3 — Create Virtual Environment

The venv lives inside the project directory at `$PROJECT_DIR/CGP/_config/venv/`.

Determine `$PROJECT_DIR`:
```bash
pwd
```

**Check if venv already exists:**
```bash
PROJECT_DIR="$(pwd)"
"$PROJECT_DIR/CGP/_config/venv/bin/python3" --version 2>/dev/null \
  || "$PROJECT_DIR/CGP/_config/venv/Scripts/python.exe" --version 2>/dev/null \
  || echo "venv absent"
```

- If it exists and works → announce "Environnement virtuel déjà valide — conservé" and skip creation.
- If it exists but is broken → ask the user: "Le venv existant semble corrompu. Le recréer ? (oui/non)" — only delete and recreate if confirmed.
- If absent → create it:

```bash
PROJECT_DIR="$(pwd)"
mkdir -p "$PROJECT_DIR/CGP/_config"
uv venv "$PROJECT_DIR/CGP/_config/venv" --python 3.12
```

Announce: "Environnement virtuel créé dans [path]"

Set `VENV_PYTHON` to:
- Linux/macOS/WSL: `$PROJECT_DIR/CGP/_config/venv/bin/python3`
- Windows: `$PROJECT_DIR/CGP/_config/venv/Scripts/python.exe`

---

## Phase 4 — Install Dependencies

Install from `requirements.txt` using uv:
```bash
uv pip install --python "$VENV_PYTHON" -r "${CLAUDE_PLUGIN_ROOT}/requirements.txt"
```

Count active (non-comment, non-blank) lines in requirements.txt. If zero, announce: "Aucun paquet tiers à installer (le plugin n'utilise que la bibliothèque standard Python)."

---

## Phase 5 — Write `project_config.json`

This file tells all hook scripts where the project data lives. It is machine-specific and gitignored.

```bash
"$VENV_PYTHON" - <<'PYEOF'
import json, os, pathlib, sys

plugin_root = pathlib.Path(os.environ["CLAUDE_PLUGIN_ROOT"])
project_dir = pathlib.Path.cwd()

# Determine venv python path
venv_base = project_dir / "CGP" / "_config" / "venv"
if sys.platform == "win32":
    venv_py = str(venv_base / "Scripts" / "python.exe")
else:
    venv_py = str(venv_base / "bin" / "python3")

config = {
    "project_dir": str(project_dir),
    "venv_python": venv_py,
}

config_path = plugin_root / "hooks" / "project_config.json"
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Écrit : {config_path}")
PYEOF
```

---

## Phase 5b — Generate `hooks/hooks.json`

`hooks.json` is gitignored (machine-specific). Two committed templates exist:
- `hooks/hooks.json.example` — Linux / macOS / WSL
- `hooks/hooks.json.windows.example` — Windows native

The setup selects the correct template and replaces the `__VENV_PYTHON__` placeholder with the actual absolute path.

```bash
"$VENV_PYTHON" - <<'PYEOF'
import os, pathlib, sys, json

plugin_root = pathlib.Path(os.environ["CLAUDE_PLUGIN_ROOT"])
hooks_dir = plugin_root / "hooks"
hooks_path = hooks_dir / "hooks.json"

if hooks_path.exists():
    print("hooks.json already exists — kept as-is")
else:
    # Read project_config to get venv_python
    config = json.loads((hooks_dir / "project_config.json").read_text(encoding="utf-8"))
    venv_py = config["venv_python"]

    example_name = "hooks.json.windows.example" if sys.platform == "win32" else "hooks.json.example"
    example_path = hooks_dir / example_name
    if not example_path.exists():
        print(f"ERROR: {example_name} not found — cannot generate hooks.json")
        raise SystemExit(1)

    content = example_path.read_text(encoding="utf-8")
    content = content.replace("__VENV_PYTHON__", venv_py)
    hooks_path.write_text(content, encoding="utf-8")
    print(f"Generated: {hooks_path} (from {example_name})")
PYEOF
```

Announce: "hooks.json généré avec succès."

---

## Phase 6 — Create Data Directories

```bash
PROJECT_DIR="$(pwd)"

# Config interne
mkdir -p "$PROJECT_DIR/CGP/_config/clients"
chmod 700 "$PROJECT_DIR/CGP/_config/clients" 2>/dev/null || true
mkdir -p "$PROJECT_DIR/CGP/_config/clients-private"
chmod 700 "$PROJECT_DIR/CGP/_config/clients-private" 2>/dev/null || true
mkdir -p "$PROJECT_DIR/CGP/_config/sessions/archive"
mkdir -p "$PROJECT_DIR/CGP/_config/sessions/references"

# Productions
mkdir -p "$PROJECT_DIR/CGP/Production/_cabinet/veille"
mkdir -p "$PROJECT_DIR/CGP/Production/_cabinet/vulgarisation"
mkdir -p "$PROJECT_DIR/CGP/Production/_cabinet/marketing"
mkdir -p "$PROJECT_DIR/CGP/Production/_cabinet/prospection"
mkdir -p "$PROJECT_DIR/CGP/Production/Clients"
```

Explain the directory structure to the user:
- `CGP/_config/` — données internes du plugin (profils clients, registre RGPD, sessions archivées, environnement Python)
- `CGP/Production/_cabinet/` — productions non liées à un client spécifique (veille, marketing, etc.)
- `CGP/Production/Clients/<NomClient>/` — créé automatiquement lors de la première production pour ce client

Check if `CGP/_config/client-registry.json` exists; if not, create an empty one:
```bash
"$VENV_PYTHON" - <<'PYEOF'
import json, pathlib, os

project_dir = pathlib.Path.cwd()
p = project_dir / "CGP" / "_config" / "client-registry.json"
if not p.exists():
    p.write_text(json.dumps({"real_to_pseudo": {}, "pseudo_to_real": {}}, indent=2), encoding="utf-8")
    print("Registre RGPD initialisé : CGP/_config/client-registry.json")
else:
    print("Registre RGPD existant conservé.")
PYEOF
```

---

## Phase 7 — Smoke Tests

Run each hook script and check exit code. Report pass/fail for each.

**fiscal_alerts.py** — temporarily remove the daily-run stamp so it actually executes, then restore it:
```bash
PROJECT_DIR="$(pwd)"
STAMP="$PROJECT_DIR/CGP/_config/last-fiscal-alert"
BACKUP=$(cat "$STAMP" 2>/dev/null || echo "")
rm -f "$STAMP"
echo '{}' | "$VENV_PYTHON" "${CLAUDE_PLUGIN_ROOT}/hooks/fiscal_alerts.py" && echo "PASS" || echo "FAIL"
[ -n "$BACKUP" ] && echo "$BACKUP" > "$STAMP"
```

**anonymize.py — list:**
```bash
"$VENV_PYTHON" "${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py" list && echo "PASS" || echo "FAIL"
```

**anonymize.py — encode (empty registry):**
```bash
echo '{"user_prompt":"test"}' | "$VENV_PYTHON" "${CLAUDE_PLUGIN_ROOT}/hooks/anonymize.py" encode && echo "PASS" || echo "FAIL"
```

**client_store.py — list:**
```bash
"$VENV_PYTHON" "${CLAUDE_PLUGIN_ROOT}/hooks/client_store.py" list && echo "PASS" || echo "FAIL"
```

**output_router.py — filter (fichier non-cgp) :**
```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/not-cgp.md"}}' \
  | "$VENV_PYTHON" "${CLAUDE_PLUGIN_ROOT}/hooks/output_router.py" && echo "PASS" || echo "FAIL"
```
Attendu : PASS sans sortie (fichier non-cgp ignoré silencieusement).

If any test fails, display the error output and advise the user to check that the venv was created correctly and that `requirements.txt` was installed.

---

## Phase 8 — Summary

Print a final summary table:

```
╔══════════════════════════════════════════════════════╗
║         CGP Assistant — Configuration terminée       ║
╠══════════════════════════════════════════════════════╣
║  uv               : [version]                        ║
║  Python           : [version] ([VENV_PYTHON])        ║
║  Venv             : CGP/_config/venv/                ║
║  Profils clients  : CGP/_config/clients/             ║
║  Productions      : CGP/Production/                  ║
║  Registre RGPD    : CGP/_config/client-registry.json ║
║  Tests hooks      : [✓ / ✗ N échec(s)]              ║
╚══════════════════════════════════════════════════════╝
```

Then remind the user of the first commands to use:
> **Prochaines étapes :**
> - Enregistrer un premier client : `/nouveau-client Prénom Nom`
> - Préparer un rendez-vous : `/rdv [client] [objet]`
> - Effectuer une veille réglementaire : `/veille [thème]`
