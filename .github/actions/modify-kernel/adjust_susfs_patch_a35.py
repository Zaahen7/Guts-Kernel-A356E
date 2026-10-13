from pathlib import Path
import sys

patch_file = Path(sys.argv[1])
lines = patch_file.read_text().splitlines(keepends=True)

target = (
    "new = copy_tree(old, old->mnt.mnt_root, copy_flags);",
    "if (IS_ERR(new)) {",
    "namespace_unlock();",
)

matches = []
in_namespace_file = False

for index, line in enumerate(lines):
    if line.startswith("diff --git "):
        in_namespace_file = line.startswith("diff --git a/fs/namespace.c ")

    if not in_namespace_file:
        continue

    if index + len(target) > len(lines):
        continue

    context = lines[index:index + len(target)]

    if all(line.startswith(" ") for line in context):
        normalized = tuple(" ".join(line[1:].split()) for line in context)

        if normalized == target:
            matches.append(index)

if len(matches) != 1:
    print(
        "ERROR: Expected exactly one namespace.c SUSFS context to adapt, "
        f"found {len(matches)} in {patch_file}.",
        file=sys.stderr,
    )
    sys.exit(1)

index = matches[0]

replacement = (
    " #ifdef CONFIG_KDP_NS\n",
    " \tnew = copy_tree(old, ((struct kdp_mount *)old)->mnt->mnt_root, copy_flags);\n",
    " #else\n",
)

lines[index:index + len(target)] = replacement
patch_file.write_text("".join(lines))

print("Adapted exactly one namespace.c SUSFS patch context for CONFIG_KDP_NS.")
