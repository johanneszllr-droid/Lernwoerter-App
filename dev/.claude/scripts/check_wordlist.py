#!/usr/bin/env python3
"""Prüft lernwoerter-blank.json auf typische Fehler.

Aufruf (im Projektordner):
    python3 .claude/scripts/check_wordlist.py            # ganze Liste prüfen
    python3 .claude/scripts/check_wordlist.py Wort1 ...  # nur diese Wörter ausführlich anzeigen

Geprüft wird:
- gültiges JSON, eindeutige IDs (ganze Zahlen)
- keine doppelten Wörter (Artikel wird ignoriert)
- jedes Wort hat Wortart, Emoji und Beispielsatz
- Nomen haben einen Artikel
- das Lernwort (oder sein Plural) steht genau so im Beispielsatz,
  damit die App es ausblenden kann (gleiche Regel wie in der App)
- Groß-/Kleinschreibung des Lernworts stimmt im Satz (z. B. "fett" nicht als "Fett")
"""
import json
import re
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "lernwoerter-blank.json"
ARTIKEL = re.compile(r"^(der|die|das|ein|eine)\s+", re.I)


def lemma(wort: str) -> str:
    return ARTIKEL.sub("", wort.strip())


def found_in_sentence(form_list, satz, ignore_case=True):
    forms = sorted({f for f in form_list if f}, key=len, reverse=True)
    if not forms:
        return False
    pattern = r"(^|[^\w])(?:" + "|".join(map(re.escape, forms)) + r")(?=$|[^\w])"
    return re.search(pattern, satz, re.I if ignore_case else 0) is not None


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    problems = []
    hints = []
    seen_ids, seen_words = {}, {}

    for nr, entry in enumerate(data, 1):
        s = entry.get("stammdaten", {})
        wort = (s.get("wort") or "").strip()
        label = f"Nr. {nr} „{wort}“"

        entry_id = entry.get("id")
        if not isinstance(entry_id, int):
            problems.append(f"{label}: ID ist keine ganze Zahl ({entry_id!r})")
        elif entry_id in seen_ids:
            problems.append(f"{label}: ID {entry_id} doppelt (auch Nr. {seen_ids[entry_id]})")
        seen_ids.setdefault(entry_id, nr)

        key = lemma(wort).lower()
        if key in seen_words:
            problems.append(f"{label}: Wort doppelt (auch Nr. {seen_words[key]})")
        seen_words.setdefault(key, nr)

        satz = (s.get("beispielsatz") or "").strip()
        if not s.get("wortart"):
            problems.append(f"{label}: Wortart fehlt")
        if not s.get("emoji"):
            problems.append(f"{label}: Emoji fehlt")
        elif s.get("emoji") == "📝":
            hints.append(f"{label}: Emoji ist der Platzhalter 📝 (prüfen, ob gewollt)")
        if s.get("wortart") == "Substantiv" and not s.get("artikel"):
            problems.append(f"{label}: Nomen ohne Artikel")
        if not satz:
            problems.append(f"{label}: Beispielsatz fehlt")
            continue
        forms = [lemma(wort), (s.get("plural") or "").strip()]
        if not found_in_sentence(forms, satz):
            problems.append(f"{label}: Wort steht nicht in dieser Form im Satz → „{satz}“")
        elif not found_in_sentence(forms, satz, ignore_case=False):
            # Großschreibung ist erlaubt am Satzanfang und nach . ! ? : (z. B. wörtliche Rede)
            capitalized = [f[:1].upper() + f[1:] for f in forms if f]
            at_start = re.search(r"(^|[.!?:]\s+)(?:" + "|".join(map(re.escape, capitalized)) + r")(?=$|[^\w])", satz)
            if not at_start:
                problems.append(f"{label}: Groß-/Kleinschreibung im Satz weicht ab → „{satz}“")

    wanted = {w.lower() for w in sys.argv[1:]}
    if wanted:
        for nr, entry in enumerate(data, 1):
            s = entry["stammdaten"]
            if lemma(s["wort"]).lower() in wanted or s["wort"].lower() in wanted:
                print(f"Nr. {nr}: " + json.dumps(entry, ensure_ascii=False))

    print(f"{len(data)} Einträge geprüft, {len(problems)} Problem(e).")
    for p in problems:
        print("  - " + p)
    for h in hints:
        print("  (Hinweis) " + h)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
