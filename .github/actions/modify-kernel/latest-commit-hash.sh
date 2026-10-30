# This Bash script defines a function called latest_commit that retrieves the latest commit SHA from a specific branch of a Git repository without cloning it.
#!/usr/bin/env bash

latest_commit() {
    local repo="$1"
    local branch="$2"
    local sha

    echo "Checking $repo ($branch)..." >&2

    sha=$(git ls-remote "$repo" "refs/heads/$branch" | awk '{print $1}')

    if [ -z "$sha" ]; then
        echo "❌ Failed to get commit SHA" >&2
        return 1
    fi

    echo "$sha"
}
