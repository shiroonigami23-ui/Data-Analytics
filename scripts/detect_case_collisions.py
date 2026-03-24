import subprocess
import sys


def main() -> int:
    try:
        output = subprocess.check_output(
            ["git", "ls-files"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        print("Failed to read tracked files:\n", exc.output)
        return 2

    buckets = {}
    for line in output.splitlines():
        key = line.lower()
        buckets.setdefault(key, []).append(line)

    collisions = [paths for paths in buckets.values() if len(paths) > 1]
    if not collisions:
        print("No case-collision entries found.")
        return 0

    print("Case-collision entries detected:")
    for group in collisions:
        for path in group:
            print("  -", path)
        print()

    print(
        "Fix on a case-sensitive filesystem (Linux/WSL) by renaming or removing "
        "duplicate-case paths so only one canonical path remains."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
