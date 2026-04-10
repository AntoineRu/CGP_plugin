#!/usr/bin/env python3
"""
CGP Client Anonymizer — Claude Code Hook Script

Registry: CGP/_config/client-registry.json (path resolved via config.py)
  { "real_to_pseudo": {"Martin Dupont": "Mathieu Durant"},
    "pseudo_to_real": {"Mathieu Durant": "Martin Dupont"} }

Modes:
  encode   UserPromptSubmit: detect real names → inject systemMessage to use pseudonyms
  decode   PostToolUse Write|Edit: restore real names in written documents
  register <Prénom Nom>: register client, print JSON result
  list     print all registered clients as JSON
"""

import json
import re
import sys
from pathlib import Path

from config import registry_path as _registry_path

# French first names indexed by initial
PRENOMS = {
    "A": ["Adrien", "Alexandre", "Alice", "Amélie", "Antoine", "Audrey"],
    "B": ["Baptiste", "Benjamin", "Brigitte", "Bruno", "Bastien"],
    "C": ["Camille", "Caroline", "Charles", "Christine", "Christophe"],
    "D": ["David", "Denis", "Diane", "Dominique", "Dylan"],
    "E": ["Edouard", "Elise", "Emmanuel", "Eric", "Estelle"],
    "F": ["Fabrice", "Florence", "Francois", "Frederic", "Francoise"],
    "G": ["Gabriel", "Guillaume", "Gilles", "Gaelle", "Gerard"],
    "H": ["Helene", "Henri", "Hugo", "Hubert", "Herve"],
    "I": ["Isabelle", "Ivan", "Ines", "Irene"],
    "J": ["Jacques", "Jean", "Julien", "Julie", "Joelle"],
    "K": ["Karine", "Kevin", "Karl"],
    "L": ["Laurent", "Laure", "Luc", "Lucas", "Lucie", "Lea"],
    "M": ["Marc", "Marie", "Mathieu", "Michel", "Monique", "Maxime"],
    "N": ["Nicolas", "Nathalie", "Noemie", "Norbert"],
    "O": ["Olivier", "Odile", "Oceane", "Oriane"],
    "P": ["Pascal", "Patricia", "Philippe", "Pierre", "Paul", "Pauline"],
    "Q": ["Quentin"],
    "R": ["Raphael", "Rene", "Robert", "Romain", "Rachel"],
    "S": ["Sandrine", "Sebastien", "Sophie", "Stephane", "Sylvie"],
    "T": ["Thomas", "Thierry", "Theodore", "Thibault"],
    "U": ["Ugo", "Ursula", "Ulrich"],
    "V": ["Valerie", "Vincent", "Virginie", "Veronique"],
    "W": ["William", "Wanda", "Walter"],
    "X": ["Xavier"],
    "Y": ["Yannick", "Yves", "Yvette", "Yoann"],
    "Z": ["Zacharie", "Zoe", "Zelie"],
}

NOMS = {
    "A": ["Arnaud", "Aubry", "Aubert", "Allard"],
    "B": ["Barbier", "Bernard", "Blanc", "Bonnet", "Bouchard", "Boyer"],
    "C": ["Carpentier", "Chevalier", "Clement", "Colin", "Cordier"],
    "D": ["David", "Denis", "Dubois", "Dumont", "Dupre", "Durant"],
    "E": ["Etienne", "Evrard"],
    "F": ["Fabre", "Fontaine", "Fournier", "Ferrand", "Fauvet"],
    "G": ["Garnier", "Gautier", "Gerard", "Girard", "Guerin"],
    "H": ["Henry", "Herve", "Hubert", "Hamelin"],
    "I": ["Ibert", "Imbert"],
    "J": ["Jacob", "Joubert", "Journet"],
    "K": ["Klein"],
    "L": ["Lambert", "Lefevre", "Leroy", "Lucas", "Leduc"],
    "M": ["Marchand", "Masson", "Moreau", "Moulin", "Meunier"],
    "N": ["Noel", "Neveu", "Normand"],
    "O": ["Olivier", "Oudin"],
    "P": ["Petit", "Picard", "Perrin", "Pichon", "Poulet"],
    "Q": ["Quantin"],
    "R": ["Renaud", "Richard", "Robert", "Robin", "Roux"],
    "S": ["Simon", "Sorel", "Sabatier", "Simonnet"],
    "T": ["Thomas", "Tissot", "Turpin", "Terrier"],
    "U": ["Urseau"],
    "V": ["Valentin", "Vidal", "Vincent", "Vasseur"],
    "W": ["Weber", "Wolff"],
    "X": ["Xavier"],
    "Y": ["Yvon", "Yver"],
    "Z": ["Zuber", "Zimmermann"],
}

# File extensions where real names should be restored (document types only)
DOCUMENT_EXTENSIONS = {".md", ".txt", ".tex", ".html", ".htm", ".rtf", ".csv"}


# ── Registry ──────────────────────────────────────────────────────────────────

def load_registry() -> dict:
    rp = _registry_path()
    if rp.exists():
        return json.loads(rp.read_text(encoding="utf-8"))
    return {"real_to_pseudo": {}, "pseudo_to_real": {}}


def save_registry(reg: dict):
    rp = _registry_path()
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(
        json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── Pseudonym generation ──────────────────────────────────────────────────────

def generate_pseudonym(first: str, last: str, reg: dict) -> str:
    """Return a pseudonym with same initials not already in use."""
    import random

    fi = first[0].upper() if first else "A"
    li = last[0].upper() if last else "B"
    used = set(reg["real_to_pseudo"].values())

    fn_options = list(PRENOMS.get(fi, ["Alex"]))
    ln_options = list(NOMS.get(li, ["Allard"]))
    random.shuffle(fn_options)
    random.shuffle(ln_options)

    for fn in fn_options:
        for ln in ln_options:
            candidate = f"{fn} {ln}"
            if candidate.lower() != f"{first} {last}".lower() and candidate not in used:
                return candidate

    # Fallback: initials with counter
    base = f"{fi}.{li}."
    n = 1
    while f"{base}{n}" in used:
        n += 1
    return f"{base}{n}"


# ── Name replacement ──────────────────────────────────────────────────────────

def replace_names(text: str, mapping: dict) -> str:
    """Replace all keys with values, longest-match-first, case-insensitive."""
    result = text
    for src, dst in sorted(mapping.items(), key=lambda x: -len(x[0])):
        result = re.sub(
            r"(?<!\w)" + re.escape(src) + r"(?!\w)",
            dst,
            result,
            flags=re.IGNORECASE,
        )
    return result


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_register(name_arg: str):
    """Register a client. Output JSON {status, real, pseudo}."""
    parts = name_arg.strip().split()
    if len(parts) < 2:
        print(json.dumps({"error": "Format requis: Prénom Nom"}, ensure_ascii=False))
        return

    first = parts[0].capitalize()
    last = " ".join(p.capitalize() for p in parts[1:])
    real_key = f"{first} {last}"

    reg = load_registry()
    if real_key in reg["real_to_pseudo"]:
        pseudo = reg["real_to_pseudo"][real_key]
        print(json.dumps({"status": "already_registered", "real": real_key, "pseudo": pseudo}, ensure_ascii=False))
        return

    pseudo = generate_pseudonym(first, last, reg)
    reg["real_to_pseudo"][real_key] = pseudo
    reg["pseudo_to_real"][pseudo] = real_key
    save_registry(reg)
    print(json.dumps({"status": "registered", "real": real_key, "pseudo": pseudo}, ensure_ascii=False))


def cmd_list():
    reg = load_registry()
    clients = [{"real": k, "pseudo": v} for k, v in reg["real_to_pseudo"].items()]
    print(json.dumps({"clients": clients}, ensure_ascii=False))


def cmd_encode():
    """
    UserPromptSubmit hook.
    If the prompt contains registered real names, inject a systemMessage
    telling Claude to use pseudonyms in all outputs.
    """
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    reg = load_registry()
    if not reg["real_to_pseudo"]:
        sys.exit(0)

    user_prompt = data.get("user_prompt", "")
    found = [
        f"'{real}' → '{pseudo}'"
        for real, pseudo in reg["real_to_pseudo"].items()
        if re.search(r"(?<!\w)" + re.escape(real) + r"(?!\w)", user_prompt, re.IGNORECASE)
    ]

    if found:
        system_msg = (
            "RGPD anonymisation active. "
            "Use these pseudonyms in ALL outputs (chat, documents, files): "
            + ", ".join(found)
            + ". Never write the real names in your responses or documents."
        )
        print(json.dumps({"systemMessage": system_msg}, ensure_ascii=False))

    sys.exit(0)


def cmd_decode():
    """
    PostToolUse Write|Edit hook.
    Read the written file and restore real names from pseudonyms.
    Only applies to document file types (.md, .txt, etc.).
    """
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    reg = load_registry()
    if not reg["pseudo_to_real"]:
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    fp = Path(file_path)
    if not fp.exists() or not fp.is_file():
        sys.exit(0)

    # Only process document file types
    if fp.suffix.lower() not in DOCUMENT_EXTENSIONS and fp.suffix != "":
        sys.exit(0)

    try:
        content = fp.read_text(encoding="utf-8")
        restored = replace_names(content, reg["pseudo_to_real"])
        if restored != content:
            fp.write_text(restored, encoding="utf-8")
    except (UnicodeDecodeError, IOError):
        pass

    sys.exit(0)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""

    if mode == "encode":
        cmd_encode()
    elif mode == "decode":
        cmd_decode()
    elif mode == "register" and len(sys.argv) >= 3:
        cmd_register(" ".join(sys.argv[2:]))
    elif mode == "list":
        cmd_list()
    else:
        print(
            "Usage: anonymize.py [encode|decode|register <Prénom Nom>|list]",
            file=sys.stderr,
        )
        sys.exit(1)
