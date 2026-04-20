import os
import hashlib


def get_file_hash(filepath, chunk_size=8192):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_directory(folder):
    size_map = {}

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
                size_map.setdefault(size, []).append(path)
            except Exception:
                continue

    return size_map


def find_duplicates(folder):
    size_map = scan_directory(folder)
    hash_map = {}
    duplicates = []

    for size, files in size_map.items():
        if len(files) < 2:
            continue

        for file in files:
            try:
                file_hash = get_file_hash(file)
                if file_hash in hash_map:
                    duplicates.append((file, hash_map[file_hash]))
                else:
                    hash_map[file_hash] = file
            except Exception:
                continue

    return duplicates


def main():
    folder = input("Enter folder path: ").strip()

    if not os.path.exists(folder):
        print("Invalid path!")
        return

    print("\nScanning...\n")
    duplicates = find_duplicates(folder)

    if not duplicates:
        print("No duplicates found")
        return

    print("Duplicate files:\n")
    for dup, original in duplicates:
        print(f"Duplicate: {dup}")
        print(f"Original : {original}\n")

    choice = input("Delete duplicates? (y/n): ").lower()

    if choice == "y":
        for dup, _ in duplicates:
            try:
                os.remove(dup)
                print(f"Deleted: {dup}")
            except Exception as e:
                print(f"Error deleting {dup}: {e}")


if __name__ == "__main__":
    main()
