import os
import hashlib
from collections import defaultdict

def hash_fasta_sequence_only(file_path):
    """Generate SHA512 checksum of only the sequence content in a FASTA file (ignoring headers)."""
    sha512 = hashlib.sha512()
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(">"):
                continue  # skip header
            seq_line = line.strip()
            sha512.update(seq_line.encode('utf-8'))
    return sha512.hexdigest()

def find_duplicates(folder):
    """Find duplicate FASTA files by sequence content hash."""
    checksum_map = defaultdict(list)
    print(f"Scanning folder: {folder}")

    for root, _, files in os.walk(folder):
        for name in files:
            if name.endswith((".fasta", ".fa", ".fna")):
                file_path = os.path.join(root, name)
                checksum = hash_fasta_sequence_only(file_path)
                checksum_map[checksum].append(file_path)

    duplicates = {cs: paths for cs, paths in checksum_map.items() if len(paths) > 1}
    print(f"Found {len(duplicates)} duplicate sets.")
    return duplicates

if __name__ == "__main__":
    import argparse

    import csv

    parser = argparse.ArgumentParser(description="Detect duplicate genome assemblies ignoring FASTA headers.")
    parser.add_argument("folder", help="Folder containing FASTA files")
    parser.add_argument("--csv", dest="csv_file", default="duplicates.csv", help="Output CSV file for duplicate results (default: duplicates.csv)")
    args = parser.parse_args()

    duplicates = find_duplicates(args.folder)

    # For each duplicate set, take the last sample alphabetically
    last_sample_from_duplicates = []
    if duplicates:
        print("Duplicate sequence-only files detected:")
        for checksum, paths in duplicates.items():
            print(f"\nChecksum: {checksum}")
            for path in paths:
                print(f"  {path}")
            # Get last sample alphabetically
            last_sample = sorted(paths)[-1]
            last_sample_from_duplicates.append(last_sample)
        # Write CSV output
        with open(args.csv_file, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["checksum", "file_path"])
            for checksum, paths in duplicates.items():
                for path in paths:
                    writer.writerow([checksum, path])
        print(f"CSV output written to {args.csv_file}")
    else:
        print("No duplicates found.")
    print(f"Total duplicate sets found: {len(duplicates)}")

    # Write last sample from each duplicate set to text file
    txt_filename = "last_sample_duplicates.txt"
    with open(txt_filename, "w") as txtfile:
        for path in last_sample_from_duplicates:
            txtfile.write(f"{path}\n")
    print(f"Text file listing last sample alphabetically from each duplicate set written to {txt_filename}")
