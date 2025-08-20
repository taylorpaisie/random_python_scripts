#!/usr/bin/env python3
# convert_taxa_names_nopandas.py
# Usage:
#   python convert_taxa_names_nopandas.py input.csv output.csv
#
# Input: CSV with your original names in the FIRST column (header optional)
# Output: CSV with two columns: old_name,new_name

import csv
import re
import sys
from pathlib import Path

ACC_RE = re.compile(r'(GC[FA]_\d+\.\d+)$')  # matches GCF_ or GCA_ plus version

def convert_name(old_name: str) -> str | None:
    """
    Convert 'Genus_species_..._GCF_XXXXXXXXX.Y' to 'Gspecies_GCF_XXXXXXXXX.Y'.
    Returns None if it can't parse what it needs.
    """
    if not old_name:
        return None

    parts = old_name.strip().split('_')
    if len(parts) < 3:
        return None  # need at least Genus, species, and something before accession

    genus = parts[0]
    species = parts[1]

    if not genus or not species:
        return None

    abbrev = f"{genus[0]}{species}"

    m = ACC_RE.search(old_name)
    if not m:
        return None
    acc = m.group(1)

    return f"{abbrev}_{acc}"

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_taxa_names.py input.csv output.csv", file=sys.stderr)
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not in_path.exists():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        sys.exit(2)

    rows_out = []
    warnings = 0

    with in_path.open(newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, start=1):
            if not row:
                continue
            old = row[0].strip()
            if not old:
                continue

            # Heuristic: if this looks like a header, skip it
            if i == 1 and (old.lower() in {"name", "old_name"} or "Leptospira" not in old and "GCF_" not in old and "GCA_" not in old):
                continue

            new = convert_name(old)
            if new is None:
                warnings += 1
                # Still write the old name with an empty new_name, so you can spot issues
                rows_out.append((old, ""))
            else:
                rows_out.append((old, new))

    with out_path.open("w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["old_name", "new_name"])
        writer.writerows(rows_out)

    print(f"✅ Wrote {len(rows_out)} rows to {out_path}")
    if warnings:
        print(f"⚠️ {warnings} name(s) could not be parsed (missing genus/species or accession). They have empty new_name.")

if __name__ == "__main__":
    main()
