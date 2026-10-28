import sys

def edit(path, old, new):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    if new in t and old not in t:
        print(f"[Already applied.] {path}")
        return
    if old not in t:
        print(f"[ERROR]  {path}:\n{old}")
        sys.exit(1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(t.replace(old, new, 1))
    print(f"[ok] {path}")


# --------- ADJUST SUSFS .PATCH ---------
# --- fs/exec.c ---
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "@@ -65,6 +65,9 @@",
    "@@ -65,7 +65,10 @@")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "#include <linux/syscall_user_dispatch.h>\n",
    "#include <linux/syscall_user_dispatch.h>\n #include <linux/task_integrity.h>\n")

# --- fs/namespace.c ---
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "@@ -32,11 +32,21 @@",
    "@@ -32,15 +32,21 @@")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "#include <linux/mnt_idmapping.h>\n",
    """#include <linux/mnt_idmapping.h>\n
    #include <linux/delay.h>\n
    #include <linux/fslog.h>\n
    #ifdef CONFIG_KDP_NS\n
    #include <linux/kdp.h>\n
    #endif\n
    """)
edit("50_add_susfs_in_gki-android13-5.15.patch",
    '#include "internal.h"\n #include <trace/hooks/blk.h>'
    '#include "internal.h"\n')
