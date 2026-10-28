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
    "#include <linux/vmalloc.h>\n #include <linux/io_uring.h>",
    "#include <linux/io_uring.h>")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "#include <linux/syscall_user_dispatch.h>",
    "#include <linux/syscall_user_dispatch.h>\n #include <linux/task_integrity.h>")

# --- fs/namespace.c ---
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "@@ -32,11 +32,21 @@",
    "@@ -32,10 +32,20 @@")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "#include <linux/fs_context.h>\n #include <linux/shmem_fs.h>\n #include <linux/mnt_idmapping.h>",
    "#ifdef CONFIG_KDP_NS\n #include <linux/kdp.h>\n #endif")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    '#include "internal.h"\n #include <trace/hooks/blk.h>',
    '#include "internal.h"')

edit("50_add_susfs_in_gki-android13-5.15.patch",
"""hlist_for_each_entry_rcu(p, head, mnt_hash)
 \t\tif (&p->mnt_parent->mnt == mnt && p->mnt_mountpoint == dentry)
 \t\t\treturn p;""",
"""hlist_for_each_entry_rcu(p, head, mnt_hash)
 #ifdef CONFIG_KDP_NS
 \t\tif (((struct kdp_mount *)(p->mnt_parent))->mnt == mnt && p->mnt_mountpoint == dentry)""")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "struct super_block *sb = old->mnt.mnt_sb;",
    "#endif")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "struct mnt_namespace *copy_mnt_ns(unsigned long flags, struct mnt_namespace *ns,",
    "/* First pass: copy the tree topology */")
edit("50_add_susfs_in_gki-android13-5.15.patch",
    "\tnew = copy_tree(old, old->mnt.mnt_root, copy_flags);\n\tif (IS_ERR(new)) {\n\t\tnamespace_unlock();",
    " #ifdef CONFIG_KDP_NS\n    new = copy_tree(old, ((struct kdp_mount *)old)->mnt->mnt_root, copy_flags);\n #endif")

