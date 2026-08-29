#!/usr/bin/env python3
"""Prepare audit batches for audit subagents.

Selects words to audit, skips anything already curated by hand, and splits the
result into per-agent batch files.

This pack has never had the candidate heuristics run over it, so there is no
audit_candidates.jsonl and 'rest' -- every word, commonest first -- is the only
source available and the default.
"""
import argparse, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "Data/cache/audit_candidates.jsonl"
TRANSLATIONS = ROOT / "Data/cache/translations_frFR_en.jsonl"
CURATED = ROOT / "Data/CuratedFR.jsonl"
WORKDIR = ROOT / "Data/cache/audit_work"
CONTEXT_CHARS = 220


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reason", default="compound",
                    help="candidate reason to select, or 'any' for every remaining candidate")
    ap.add_argument("--limit", type=int, default=3000, help="how many entries this wave")
    ap.add_argument("--batch-size", type=int, default=150)
    ap.add_argument("--offset", type=int, default=0, help="skip N entries (for later waves)")
    ap.add_argument("--source", choices=("candidates", "rest"), default="rest",
                    help="'rest' audits the words no heuristic ever flagged")
    args = ap.parse_args()

    done = {r["key"] for r in load_jsonl(CURATED)}
    for path in sorted((WORKDIR / "out").glob("*.jsonl")) if (WORKDIR / "out").exists() else []:
        done.update(r["key"] for r in load_jsonl(path))

    if args.source == "rest":
        # Everything the candidate heuristics never looked at -- which here is
        # everything. Sorted by how often the word appears in quest text, so the
        # words a player actually meets are corrected first.
        flagged = {r["key"] for r in load_jsonl(CANDIDATES)}
        rows = [r for r in load_jsonl(TRANSLATIONS)
                if r["key"] not in flagged and r["key"] not in done]
    else:
        rows = [r for r in load_jsonl(CANDIDATES)
                if (args.reason == "any" or args.reason in r.get("reasons", []))
                and r["key"] not in done]
    rows.sort(key=lambda r: -r.get("count", 0))
    rows = rows[args.offset:args.offset + args.limit]

    indir = WORKDIR / "in"
    indir.mkdir(parents=True, exist_ok=True)
    (WORKDIR / "out").mkdir(parents=True, exist_ok=True)

    batches = 0
    for i in range(0, len(rows), args.batch_size):
        chunk = rows[i:i + args.batch_size]
        slim = [{"key": r["key"], "word": r["word"], "current": r["translation"],
                 "count": r.get("count", 0),
                 "context": " ".join(r.get("context", "").split())[:CONTEXT_CHARS]}
                for r in chunk]
        out = indir / f"batch_{batches:02d}.jsonl"
        out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in slim) + "\n", encoding="utf-8")
        batches += 1
    print(f"selected={len(rows)} batches={batches} skipped_already_done={len(done)}")


if __name__ == "__main__":
    main()
