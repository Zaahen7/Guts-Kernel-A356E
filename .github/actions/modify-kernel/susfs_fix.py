import re, sys

PATCH = "50_add_susfs_in_gki-android13-5.15.patch"

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


def C(s=""): return " " + s   # context line
def A(s=""): return "+" + s   # added line

def replace_hunk(src, old_header, lines, first_ctx):
    with open(src, encoding="utf-8") as f:
        kernel = f.read().split("\n")
    if first_ctx not in kernel:
        print(f"[ERROR]  '{first_ctx}' not found in {src}")
        sys.exit(1)
    n = kernel.index(first_ctx) + 1
    old = sum(1 for l in lines if l[0] in " -")
    new = sum(1 for l in lines if l[0] in " +")
    hunk = f"@@ -{n},{old} +{n},{new} @@\n" + "\n".join(lines) + "\n"

    with open(PATCH, encoding="utf-8") as f:
        t = f.read()
    m = re.search(r"^diff --git a/" + re.escape(src) + r" .*?(?=^diff --git |\Z)", t, re.S | re.M)
    if not m:
        print(f"[ERROR]  no section for {src} in patch")
        sys.exit(1)
    sec = m.group(0)
    h = re.search(re.escape(old_header) + r"[^\n]*\n.*?(?=^@@ |\Z)", sec, re.S | re.M)
    if not h:
        print(f"[ERROR]  hunk {old_header} not found in {src}")
        sys.exit(1)
    t = t.replace(sec, sec.replace(h.group(0), hunk, 1), 1)
    with open(PATCH, "w", encoding="utf-8") as f:
        f.write(t)
    print(f"[ok] {src}: hunk rewritten as -{n},{old} +{n},{new}")


# --------- ADJUST SUSFS .PATCH ---------
# --- fs/exec.c ---
edit(PATCH,
    "@@ -65,6 +65,9 @@",
    "@@ -65,7 +65,10 @@")
edit(PATCH,
    "#include <linux/syscall_user_dispatch.h>",
    "#include <linux/syscall_user_dispatch.h>\n #include <linux/task_integrity.h>")

# --- fs/namespace.c ---
replace_hunk("fs/namespace.c", "@@ -32,11 +32,21 @@", [
    C("#ifdef CONFIG_KDP_NS"),
    C("#include <linux/kdp.h>"),
    C("#endif"),
    A("#ifdef CONFIG_KSU_SUSFS"),
    A("#include <linux/susfs_def.h>"),
    A("#endif // #ifdef CONFIG_KSU_SUSFS"),
    C(),
    C('#include "pnode.h"'),
    C('#include "internal.h"'),
    C(),
    A("#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT"),
    A("extern bool susfs_is_current_ksu_domain(void);"),
    A("extern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;"),
    A(),
    A("#define CL_COPY_MNT_NS BIT(25) /* used by copy_mnt_ns() */"),
    A("#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MOUNT"),
    A(),
    C("/* Maximum number of mounts in a mount namespace */"),
    C("unsigned int sysctl_mount_max __read_mostly = 100000;"),
], "#ifdef CONFIG_KDP_NS")

# --- fs/proc/task_mmu.c ---
replace_hunk("fs/proc/task_mmu.c", "@@ -22,6 +22,9 @@", [
    C("#include <linux/shmem_fs.h>"),
    C("#include <linux/uaccess.h>"),
    C("#include <linux/pkeys.h>"),
    A("#if defined(CONFIG_KSU_SUSFS_SUS_KSTAT) || defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)"),
    A("#include <linux/susfs_def.h>"),
    A("#endif // #if defined(CONFIG_KSU_SUSFS_SUS_KSTAT) || defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)"),
    C(),
    C("#include <asm/elf.h>"),
    C("#include <asm/tlb.h>"),
], "#include <linux/shmem_fs.h>")
