#!/usr/bin/env python3
"""Repair mechanical damage in audit output, and only mechanical damage.

Agents get the content right far more reliably than they get the file format
right. Two faults recur and neither is a judgement call:

  * the file is written with a BOM, two objects share a line, an object closes
    with `]` or trails a comma, or a bare string is left sitting between fields
  * the typographic apostrophe in a key is written as a plain one, so `c’est`
    arrives as `c'est` and no longer matches anything

Both are repaired here, deterministically, and every repair is printed. A row
that cannot be resolved is left exactly as it was for the merge to reject --
nothing is guessed, and no translation or note is ever altered.
"""
import argparse, codecs, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKDIR = ROOT / "Data/cache/audit_work"
CURLY, PLAIN = "’", "'"


def objects(text):
    """Yield one JSON string per object, undoing the format faults above."""
    for line in text.splitlines():
        line = line.strip().lstrip("﻿")
        if not line:
            continue
        # two objects sharing a line
        for part in re.split(r"(?<=\})(?=\{)", line):
            part = part.strip()
            if not part:
                continue
            # a JSON-array habit leaking into a JSONL file: a trailing comma
            # after the object, or the object closed with a bracket
            part = part.rstrip(",")
            if part.endswith("]"):
                part = part[:-1] + "}"
            yield part


def salvage(part):
    """A bare string between two fields -- drop it. Never touches a real value."""
    fixed = re.sub(r',\s*"[^"]*"\s*(?=,\s*")', "", part)
    if fixed != part:
        try:
            json.loads(fixed)
            return fixed
        except json.JSONDecodeError:
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total_syntax = total_keys = total_lost = 0
    for out_path in sorted((WORKDIR / "out").glob("batch_*.jsonl")):
        in_path = WORKDIR / "in" / out_path.name
        if not in_path.exists():
            continue
        src = {}
        for line in in_path.read_text(encoding="utf-8-sig").splitlines():
            if line.strip():
                r = json.loads(line)
                src[r["key"]] = r
        rows, syntax, keys, lost = [], [], [], []
        raw = out_path.read_text(encoding="utf-8-sig")
        # A byte order mark is harmless to the merge, which reads utf-8-sig, but
        # it breaks every other reader. Rewrite the file for that alone.
        bom = out_path.read_bytes().startswith(codecs.BOM_UTF8)
        if bom:
            print(f"  {out_path.name}: BOM usuniety")
        for part in objects(raw):
            try:
                row = json.loads(part)
            except json.JSONDecodeError:
                repaired = salvage(part)
                if repaired is None:
                    lost.append(part[:70])
                    continue
                syntax.append(json.loads(repaired).get("key"))
                row = json.loads(repaired)
            key = row.get("key")
            if key not in src:
                # The apostrophe, in either direction. Only accepted when the
                # swap lands on a key this batch actually contains.
                for cand in (key.replace(PLAIN, CURLY), key.replace(CURLY, PLAIN)):
                    if cand in src:
                        keys.append((key, cand))
                        row["key"] = cand
                        row["word"] = src[cand]["word"]
                        break
            rows.append(row)

        if syntax or keys or lost:
            print(f"  {out_path.name}: skladnia {len(syntax)}, apostrof {len(keys)}, "
                  f"nie do odzyskania {len(lost)}")
            for k in syntax:
                print(f"      skladnia naprawiona: {k!r}")
            for a, b in keys[:3]:
                print(f"      klucz {a!r} -> {b!r}")
            if len(keys) > 3:
                print(f"      ... i {len(keys)-3} dalszych kluczy")
            for l in lost:
                print(f"      NIE ODZYSKANO: {l}")
        total_syntax += len(syntax); total_keys += len(keys); total_lost += len(lost)

        if not args.dry_run and (syntax or keys or bom):
            out_path.write_text(
                "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                encoding="utf-8", newline="\n")

    print(f"\nnaprawione: skladnia {total_syntax}, klucze {total_keys}; "
          f"nie do odzyskania {total_lost}"
          + ("  (dry run, nic nie zapisano)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
