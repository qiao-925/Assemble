#!/usr/bin/env python3
import argparse, os, re, sys, json
from pathlib import Path

def extract_h1_title(md_path: Path) -> str | None:
    try:
        with md_path.open('r', encoding='utf-8') as f:
            for line in f:
                s = line.strip('\n')
                if s.strip().startswith('#'):
                    # Use the whole line (keep leading # and emoji) to match "一样的内容"
                    return s.strip()
    except Exception as e:
        return None
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    base = Path(args.dir)
    if not base.is_dir():
        print(f"ERROR: not a directory: {base}", file=sys.stderr)
        sys.exit(2)

    changes = []
    for p in sorted(base.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() != '.md':
            continue
        if p.name.lower() == 'readme.md':
            continue
        title = extract_h1_title(p)
        if not title:
            continue
        new_name = f"{title}.md"
        if p.name == new_name:
            continue
        # Resolve collisions by appending numeric suffix
        target = base / new_name
        if target.exists() and target.resolve() != p.resolve():
            stem = title
            i = 2
            while True:
                candidate = base / f"{stem} ({i}).md"
                if not candidate.exists():
                    target = candidate
                    break
                i += 1
        changes.append((p.name, target.name))

    # Output mapping in TSV for easier parsing
    for old, new in changes:
        print(f"{old}\t{new}")

    if args.apply and changes:
        for old, new in changes:
            src = base / old
            dst = base / new
            os.rename(src, dst)

if __name__ == '__main__':
    main()
