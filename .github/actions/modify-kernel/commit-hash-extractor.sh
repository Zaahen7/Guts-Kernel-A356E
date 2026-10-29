#!/usr/bin/env bash
# Helpers to pin and record the commits of the repositories used in a build.
# Usage: source "$GITHUB_ACTION_PATH/commit-hash-extractor.sh"

# latest_commit <repo-url> <branch>
# Prints the commit at the tip of <branch> without cloning anything.
latest_commit() {
    local sha
    sha=$(git ls-remote "$1" "refs/heads/$2" | awk -v ref="refs/heads/$2" '$2 == ref {print $1}')
    if [ -z "$sha" ]; then
        echo "::error::Branch '$2' not found in $1" >&2
        return 1
    fi
    echo "$sha"
}

# record_commit <name> <sha>
# Appends "name: sha" to kernel-info.txt (and nowhere else: no env variables).
# The file is $KERNEL_INFO if set, otherwise $GITHUB_WORKSPACE/kernel-info.txt.
record_commit() {
    local info="${KERNEL_INFO:-${GITHUB_WORKSPACE:-.}/kernel-info.txt}"
    echo "$1: $2" >> "$info"
    echo "[commit] $1: $2"
}

# record_linked_repo <name> <path>
# Records the HEAD of the standalone git repo that <path> (e.g. a symlink such
# as drivers/kernelsu) points into. Skips it if <path> is not inside its own
# repo, so the kernel repo's commit is never recorded under the wrong name.
record_linked_repo() {
    local src root kroot
    if [ ! -e "$2" ]; then
        echo "::warning::$1: $2 not found, commit not recorded"
        return 0
    fi
    src=$(readlink -f "$2")
    root=$(git -c safe.directory='*' -C "$src" rev-parse --show-toplevel 2>/dev/null || true)
    kroot=$(git -c safe.directory='*' -C "${KERNEL_DIR:-.}" rev-parse --show-toplevel 2>/dev/null || true)
    if [ -z "$root" ] || [ "$root" = "$kroot" ]; then
        echo "::warning::$1: $2 is not a standalone git repo, commit not recorded"
        return 0
    fi
    record_commit "$1" "$(git -c safe.directory='*' -C "$root" rev-parse HEAD)"
}
