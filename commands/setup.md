---
description: 'First-run setup: detect Python, create venv, configure hooks, verify installation'
argument-hint: ''
---

# /setup — CGP Assistant Initial Configuration

You are the setup assistant for the CGP Assistant plugin. Walk through each phase below in order, using your Bash tool to run commands. Announce each phase clearly and report what you find/do. Stop and ask the user before any destructive action.

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

## Phase 2 — Find Python 3.8+

Test candidates in this order, stopping at the first one that returns version ≥ 3.8:

```bash
# Try each of these (adapt for Windows: replace python3 with python/py where needed)
for cmd in python3 python3.13 python3.12 python3.11 python3.10 python3.9 python3.8 python py; do
  if command -v "$cmd" 2>/dev/null; then
    ver=$("$cmd" -c "import sys; v=sys.version_info; print(f'{v.major}.{v.minor}')" 2>/dev/null)
    echo "$cmd -> $ver"
  fi
done
```

On Windows (Git Bash or cmd), also try:
- `py -3` (Python Launcher)
- `%LOCALAPPDATA%\Programs\Python\Python3*\python.exe`
- `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python3.exe`

Also probe conda environments:
```bash
conda env list 2>/dev/null || true
```

**If no Python 3.8+ is found:**
Stop and display this message to the user, tailored to their OS:

> ### Python non trouvé — Installation requise
>
> Aucun Python 3.8+ n'est disponible sur ce système. Veuillez en installer un avant de relancer `/setup` :
>
> **Option A — Miniconda** (recommandée, légère) :
> - Windows : https://docs.conda.io/en/latest/miniconda.html → télécharger `Miniconda3-latest-Windows-x86_64.exe`
> - Linux/WSL : `curl -sL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh | bash`
> - macOS : `brew install miniconda` ou télécharger depuis le site
>
> **Option B — Python.org** :
> - https://www.python.org/downloads/ → cocher "Add Python to PATH" lors de l'installation
>
> Après installation, redémarrez Claude Code et relancez `/setup`.

Do not continue to Phase 3.

**If found**, announce: "Python [version] trouvé : [path]" and store this as `PYTHON_FOUND`.

---

## Phase 3 — Create Virtual Environment

The venv lives **one level above `cgp-assistant/`**, i.e. at the same level as the plugin directory. Determine its path:

- On Linux/macOS/WSL: `VENV_DIR = "${CLAUDE_PLUGIN_ROOT}/../.venv"`
- On Windows (native): `VENV_DIR = parent_of_CLAUDE_PLUGIN_ROOT + "\.venv"`

**Check if venv already exists:**
```bash
"${CLAUDE_PLUGIN_ROOT}/../.venv/bin/python3" --version 2>/dev/null \
  || "${CLAUDE_PLUGIN_ROOT}/../.venv/Scripts/python.exe" --version 2>/dev/null \
  || echo "venv absent"
```

- If it exists and works → announce "Environnement virtuel déjà valide — conservé" and skip creation.
- If it exists but is broken → ask the user: "Le venv existant semble corrompu. Le recréer ? (oui/non)" — only delete and recreate if confirmed.
- If absent → create it:

```bash
"$PYTHON_FOUND" -m venv "${CLAUDE_PLUGIN_ROOT}/../.venv"
```

Announce: "Environnement virtuel créé dans [path]"

Set `VENV_PYTHON` to:
- Linux/macOS/WSL: `${CLAUDE_PLUGIN_ROOT}/../.venv/bin/python3`
- Windows: `${CLAUDE_PLUGIN_ROOT}/../.venv/Scripts/python.exe`

---

## Phase 4 — Install Dependencies

Upgrade pip silently:
```bash
"$VENV_PYTHON" -m pip install --quiet --upgrade pip
```

Install from `requirements.txt`:
```bash
"$VENV_PYTHON" -m pip install --quiet -r "${CLAUDE_PLUGIN_ROOT}/requirements.txt"
```

Count active (non-comment, non-blank) lines in requirements.txt. If zero, announce: "Aucun paquet tiers à installer (le plugin n'utilise que la bibliothèque standard Python)."

---

## Phase 5 — Generate `hooks/hooks.json`

`hooks.json` is gitignored (machine-specific). Two committed templates exist:
- `hooks/hooks.json.example` — Linux / macOS / WSL (`bin/python3`)
- `hooks/hooks.json.windows.example` — Windows native (`Scripts/python.exe`)

The correct template is selected automatically based on the detected platform and copied as-is — no path substitution needed.

```bash
"$VENV_PYTHON" - <<'PYEOF'
import os, pathlib, sys

hooks_dir = pathlib.Path(os.environ["CLAUDE_PLUGIN_ROOT"]) / "hooks"
hooks_path = hooks_dir / "hooks.json"

if hooks_path.exists():
    print("hooks.json already exists — kept as-is")
else:
    example_name = "hooks.json.windows.example" if sys.platform == "win32" else "hooks.json.example"
    example_path = hooks_dir / example_name
    if not example_path.exists():
        print(f"ERROR: {example_name} not found — cannot generate hooks.json")
        raise SystemExit(1)
    hooks_path.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Generated: {hooks_path} (from {example_name})")
PYEOF
```

Announce: "hooks.json généré avec succès."

---

## Phase 6 — Create Data Directories

```bash
mkdir -p "$HOME/.cgp-clients"
chmod 700 "$HOME/.cgp-clients" 2>/dev/null || true   # no-op on Windows

mkdir -p "$HOME/cgp-clients-private"
chmod 700 "$HOME/cgp-clients-private" 2>/dev/null || true
```

Explain the two directories to the user:
- `~/.cgp-clients/` — pseudonymized profiles, used by the AI during sessions
- `~/cgp-clients-private/` — decoded profiles with real names, for your direct consultation

Check if `~/.cgp-client-registry.json` exists; if not, create an empty one:
```bash
"$VENV_PYTHON" - <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".cgp-client-registry.json"
if not p.exists():
    p.write_text(json.dumps({"real_to_pseudo": {}, "pseudo_to_real": {}}, indent=2), encoding="utf-8")
    print("Registre RGPD initialisé : ~/.cgp-client-registry.json")
else:
    print("Registre RGPD existant conservé.")
PYEOF
```

---

## Phase 7 — Smoke Tests

Run each hook script and check exit code. Report pass/fail for each.

**fiscal_alerts.py** — temporarily remove the daily-run stamp so it actually executes, then restore it:
```bash
STAMP="$HOME/.cgp-last-fiscal-alert"
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

If any test fails, display the error output and advise the user to check that the venv was created correctly and that `requirements.txt` was installed.

---

## Phase 8 — Summary

Print a final summary table:

```
╔══════════════════════════════════════════════════════╗
║         CGP Assistant — Configuration terminée       ║
╠══════════════════════════════════════════════════════╣
║  Python          : [version] ([path])                ║
║  Venv            : [VENV_DIR]                        ║
║  Profils clients : ~/.cgp-clients/                   ║
║  Registre RGPD   : ~/.cgp-client-registry.json       ║
║  Tests hooks     : [✓ / ✗ N échec(s)]               ║
╚══════════════════════════════════════════════════════╝
```

Then remind the user of the first commands to use:
> **Prochaines étapes :**
> - Enregistrer un premier client : `/nouveau-client Prénom Nom`
> - Préparer un rendez-vous : `/rdv [client] [objet]`
> - Effectuer une veille réglementaire : `/veille [thème]`
