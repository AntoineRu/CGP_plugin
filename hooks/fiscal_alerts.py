#!/usr/bin/env python3
"""CGP Fiscal Calendar Alert — UserPromptSubmit hook

Fires once per day (on first prompt of the day) and injects a systemMessage
if any fiscal deadline is within the next 30 days.
"""
import json
import sys
import datetime
from pathlib import Path

LAST_RUN_FILE = Path.home() / ".cgp-last-fiscal-alert"

# (month, day, label, concerned_profiles)
DEADLINES = [
    (1, 15, "Acompte CFE — TNS", "TNS / indépendants"),
    (2, 28, "Déclaration revenus fonciers (option réel)", "Clients avec revenus fonciers"),
    (6, 15, "Acompte IR (hors prélèvement à la source)", "Contribuables concernés"),
    (9, 15, "Deuxième tiers provisionnel IR", "Contribuables concernés"),
    (11, 15, "Paiement CFE", "TNS / indépendants"),
    (11, 30, "Vérification valorisation patrimoine IFI", "Clients assujettis à l'IFI"),
    (12, 31, "Dernière chance : versements PER, donations, arbitrages AV", "Tous les clients"),
]


def already_ran_today() -> bool:
    """Return True if the alert has already been checked today."""
    try:
        content = LAST_RUN_FILE.read_text().strip()
        return content == datetime.date.today().isoformat()
    except (FileNotFoundError, OSError):
        return False


def mark_ran_today():
    """Write today's date to the last-run file."""
    try:
        LAST_RUN_FILE.write_text(datetime.date.today().isoformat())
    except OSError:
        pass  # Non-fatal — worst case we re-check tomorrow


def get_upcoming(today: datetime.date, window_days: int = 30) -> list:
    """Return list of (days_remaining, label, profiles) for deadlines within window_days."""
    upcoming = []
    for month, day, label, profiles in DEADLINES:
        # Try the deadline in the current year first
        try:
            deadline = datetime.date(today.year, month, day)
        except ValueError:
            # Handles edge cases like Feb 29 in non-leap years
            continue

        # If already passed this year, look at next year
        if deadline < today:
            try:
                deadline = datetime.date(today.year + 1, month, day)
            except ValueError:
                continue

        days_remaining = (deadline - today).days
        if 1 <= days_remaining <= window_days:
            upcoming.append((days_remaining, label, profiles))

    upcoming.sort(key=lambda x: x[0])
    return upcoming


def main():
    # Read stdin — may be empty or non-JSON; handle gracefully
    try:
        raw = sys.stdin.read()
        _ = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, Exception):
        pass  # We don't need the hook payload for this script

    if already_ran_today():
        sys.exit(0)

    today = datetime.date.today()
    upcoming = get_upcoming(today)

    if upcoming:
        lines = ["⚠️ Rappels fiscaux à venir (prochains 30 jours) :"]
        for days, label, profiles in upcoming:
            lines.append(f"• {days} jour{'s' if days > 1 else ''} — {label} ({profiles})")
        lines.append("")
        lines.append("Pensez à en parler à vos clients concernés.")
        message = "\n".join(lines)
        print(json.dumps({"systemMessage": message}))

    mark_ran_today()
    sys.exit(0)


if __name__ == "__main__":
    main()
