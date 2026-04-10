#!/usr/bin/env python3
"""
CGP Client Store — Persistance des profils clients entre sessions

Storage: CGP/_config/clients/<pseudo>.json
Registry: CGP/_config/client-registry.json (géré par anonymize.py)

Paths resolved via config.py → project_config.json (written by /setup).

Modes:
  save <pseudo>     — lit le JSON depuis stdin, sauvegarde dans CGP/_config/clients/<pseudo>.json
  load <nom>        — charge par pseudo ou nom réel (résolution via registre), affiche JSON
  list              — liste tous les profils sauvegardés (JSON array)
  delete <pseudo>   — supprime CGP/_config/clients/<pseudo>.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from config import registry_path as _registry_path
from config import clients_dir as _clients_dir
from config import clients_private_dir as _clients_private_dir


# ── Registry helpers ───────────────────────────────────────────────────────────

def load_registry() -> dict:
    rp = _registry_path()
    if rp.exists():
        try:
            return json.loads(rp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return {"real_to_pseudo": {}, "pseudo_to_real": {}}
    return {"real_to_pseudo": {}, "pseudo_to_real": {}}


def resolve_name(name: str, reg: dict) -> tuple:
    """
    Résout un nom (pseudo ou réel) vers (pseudo, real_name).
    Retourne (None, None) si introuvable.
    """
    # Essai direct comme pseudo
    if name in reg.get("pseudo_to_real", {}):
        return name, reg["pseudo_to_real"][name]

    # Essai direct comme nom réel
    if name in reg.get("real_to_pseudo", {}):
        return reg["real_to_pseudo"][name], name

    # Recherche insensible à la casse
    name_lower = name.lower()
    for pseudo, real in reg.get("pseudo_to_real", {}).items():
        if pseudo.lower() == name_lower or real.lower() == name_lower:
            return pseudo, real

    return None, None


# ── Storage helpers ────────────────────────────────────────────────────────────

def ensure_clients_dir():
    _clients_dir().mkdir(parents=True, exist_ok=True, mode=0o700)
    _clients_private_dir().mkdir(parents=True, exist_ok=True, mode=0o700)


def _safe_filename(name: str) -> str:
    """Sanitize a name for use as a filename."""
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)


def profile_path(pseudo: str) -> Path:
    return _clients_dir() / f"{_safe_filename(pseudo)}.json"


def private_profile_path(real_name: str) -> Path:
    return _clients_private_dir() / f"{_safe_filename(real_name)}.json"


def _encode_profile(profile: dict, reg: dict) -> dict:
    """Return a copy of profile with all real names replaced by pseudonyms."""
    import re

    mapping = reg.get("real_to_pseudo", {})
    if not mapping:
        return profile

    raw = json.dumps(profile, ensure_ascii=False)
    for real, pseudo in sorted(mapping.items(), key=lambda x: -len(x[0])):
        raw = re.sub(
            r"(?<!\w)" + re.escape(real) + r"(?!\w)",
            pseudo,
            raw,
            flags=re.IGNORECASE,
        )
    return json.loads(raw)


def _decode_profile(profile: dict, reg: dict) -> dict:
    """Return a copy of profile with all pseudonyms replaced by real names."""
    import re

    mapping = reg.get("pseudo_to_real", {})
    if not mapping:
        return profile

    # Serialize → replace → deserialize keeps the structure intact
    raw = json.dumps(profile, ensure_ascii=False)
    for pseudo, real in sorted(mapping.items(), key=lambda x: -len(x[0])):
        raw = re.sub(
            r"(?<!\w)" + re.escape(pseudo) + r"(?!\w)",
            real,
            raw,
            flags=re.IGNORECASE,
        )
    return json.loads(raw)


# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_save(pseudo: str):
    """Lit le JSON du profil depuis stdin et le sauvegarde."""
    ensure_clients_dir()

    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "Aucune donnée reçue sur stdin"}, ensure_ascii=False))
        sys.exit(1)

    try:
        profile = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON invalide : {e}"}, ensure_ascii=False))
        sys.exit(1)

    if not isinstance(profile, dict):
        print(json.dumps({"error": "Le profil doit être un objet JSON"}, ensure_ascii=False))
        sys.exit(1)

    reg = load_registry()
    real_name = reg.get("pseudo_to_real", {}).get(pseudo, "")
    saved_at = datetime.now(timezone.utc).isoformat()

    # — Private decoded copy (human-readable, real names) — built before stripping
    private_path = None
    private_error = None
    if real_name:
        try:
            decoded = _decode_profile(profile, reg)
            decoded["_meta"] = {"saved_at": saved_at, "pseudo": pseudo, "real_name": real_name}
            private_path = private_profile_path(real_name)
            private_path.write_text(json.dumps(decoded, ensure_ascii=False, indent=2), encoding="utf-8")
        except (IOError, Exception) as e:
            private_error = str(e)

    # — Pseudonymized copy (AI working copy) — strip all real names, no real_name in _meta —
    pseudo_profile = _encode_profile(profile, reg)
    pseudo_profile["_meta"] = {"saved_at": saved_at, "pseudo": pseudo}

    path = profile_path(pseudo)
    try:
        path.write_text(json.dumps(pseudo_profile, ensure_ascii=False, indent=2), encoding="utf-8")
    except IOError as e:
        print(json.dumps({"error": f"Impossible d'écrire le fichier : {e}"}, ensure_ascii=False))
        sys.exit(1)

    result = {
        "status": "saved",
        "pseudo": pseudo,
        "real_name": real_name,
        "file": str(path),
        "private_file": str(private_path) if private_path else None,
        "saved_at": saved_at,
    }
    if private_error:
        result["private_error"] = private_error
    print(json.dumps(result, ensure_ascii=False))


def cmd_load(name: str):
    """Charge un profil par pseudo ou nom réel, affiche le JSON sur stdout."""
    reg = load_registry()
    pseudo, real_name = resolve_name(name, reg)

    if pseudo is None:
        # Tentative de chargement direct par pseudo même si non enregistré
        path = profile_path(name)
        if path.exists():
            pseudo = name
            real_name = ""
        else:
            print(json.dumps({
                "error": f"Client introuvable : '{name}'. Vérifiez le nom ou le pseudonyme.",
            }, ensure_ascii=False))
            sys.exit(1)
    else:
        path = profile_path(pseudo)

    if not path.exists():
        print(json.dumps({
            "error": f"Aucun profil sauvegardé pour '{name}' (pseudo : {pseudo}). "
                     "Utilisez /client save pour sauvegarder d'abord.",
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"error": f"Impossible de lire le profil : {e}"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(profile, ensure_ascii=False, indent=2))


def cmd_list():
    """Liste tous les profils sauvegardés."""
    ensure_clients_dir()
    reg = load_registry()
    results = []

    for path in sorted(_clients_dir().glob("*.json")):
        try:
            profile = json.loads(path.read_text(encoding="utf-8"))
            meta = profile.get("_meta", {})
            pseudo = meta.get("pseudo", path.stem)
            # Real name is resolved from the registry only — never stored in the pseudonymized file
            real_name = reg.get("pseudo_to_real", {}).get(pseudo, "")
            saved_at = meta.get("saved_at", "")
            results.append({
                "pseudo": pseudo,
                "real_name": real_name,
                "saved_at": saved_at,
                "file": str(path),
            })
        except (json.JSONDecodeError, IOError):
            # Ignorer les fichiers corrompus
            results.append({
                "pseudo": path.stem,
                "real_name": "",
                "saved_at": "",
                "file": str(path),
                "warning": "Fichier illisible",
            })

    print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_delete(pseudo: str):
    """Supprime le profil d'un client."""
    reg = load_registry()

    # Résoudre si c'est un nom réel
    resolved_pseudo, _ = resolve_name(pseudo, reg)
    if resolved_pseudo:
        pseudo = resolved_pseudo

    path = profile_path(pseudo)
    if not path.exists():
        print(json.dumps({
            "error": f"Aucun profil trouvé pour '{pseudo}'.",
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        path.unlink()
    except IOError as e:
        print(json.dumps({"error": f"Impossible de supprimer le fichier : {e}"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({
        "status": "deleted",
        "pseudo": pseudo,
        "file": str(path),
    }, ensure_ascii=False))


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""

    if mode == "save" and len(sys.argv) >= 3:
        cmd_save(sys.argv[2])
    elif mode == "load" and len(sys.argv) >= 3:
        cmd_load(" ".join(sys.argv[2:]))
    elif mode == "list":
        cmd_list()
    elif mode == "delete" and len(sys.argv) >= 3:
        cmd_delete(" ".join(sys.argv[2:]))
    else:
        print(
            "Usage: client_store.py [save <pseudo>|load <nom>|list|delete <pseudo>]\n"
            "  save <pseudo>    — lit le profil JSON depuis stdin, sauvegarde dans CGP/_config/clients/\n"
            "  load <nom>       — charge par pseudo ou nom réel, affiche JSON\n"
            "  list             — liste tous les profils sauvegardés\n"
            "  delete <pseudo>  — supprime le profil",
            file=sys.stderr,
        )
        sys.exit(1)
