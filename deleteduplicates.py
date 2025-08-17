import os
import hashlib
from collections import defaultdict
from send2trash import send2trash  # pip install send2trash

def file_hash(filepath, block_size=65536):
    """Generate an MD5 hash for a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while buf:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicates(folder_path):
    """Return a dictionary of hashes mapping to lists of file paths."""
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                filehash = file_hash(full_path)
                hashes[filehash].append(full_path)
            except (OSError, PermissionError):
                pass
    return {h: files for h, files in hashes.items() if len(files) > 1}

def main():
    folder = input("Enter folder path to scan: ").strip()
    duplicates = find_duplicates(folder)

    if not duplicates:
        print("No duplicates found.")
        return

    print("\nDuplicate files found:")
    for files in duplicates.values():
        for i, f in enumerate(files, start=1):
            print(f"  {i}. {f}")

    choice = input("\nSend duplicates to Recycle Bin/Trash, keeping one copy? (y/n): ").strip().lower()
    if choice == 'y':
        for files in duplicates.values():
            for f in files[1:]:  # keep first file, trash the rest
                try:
                    send2trash(f)
                    print(f"Sent to Recycle Bin: {f}")
                except Exception as e:
                    print(f"Could not send {f} to Recycle Bin: {e}")
        print("\nDuplicate cleanup complete. Files are in the Recycle Bin/Trash.")

if __name__ == "__main__":
    main()
