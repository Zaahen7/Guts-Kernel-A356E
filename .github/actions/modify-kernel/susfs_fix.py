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


# --------- KERNEL CHANGES ---------
# --- fs/exec.c ---
edit("fs/exec.c",
    "#include <linux/binfmts.h>\n#include <linux/utsname.h>\n",
    "#include <linux/binfmts.h>\n#include <linux/task_integrity.h>\n#include <linux/utsname.h>\n")
edit("fs/exec.c",
    "#include <linux/syscall_user_dispatch.h>\n#include <linux/task_integrity.h>\n",
    "#include <linux/syscall_user_dispatch.h>\n")

# --- fs/namespace.c ---
blk = ("#include <linux/delay.h>\n#include <linux/fslog.h>\n"
       "#ifdef CONFIG_KDP_NS\n#include <linux/kdp.h>\n#endif\n")
edit("fs/namespace.c",
    "#include <linux/security.h>\n#include <linux/cred.h>\n",
    "#include <linux/security.h>\n" + blk + "#include <linux/cred.h>\n")
edit("fs/namespace.c",
    "#include <linux/mnt_idmapping.h>\n" + blk,
    "#include <linux/mnt_idmapping.h>\n")

# --- fs/open.c ---
edit("fs/open.c",
    "struct file *f = do_filp_open(dfd, tmp, &op);\n\n#ifdef CONFIG_SECURITY_DEFEX",
    "struct file *f = do_filp_open(dfd, tmp, &op);\n#ifdef CONFIG_SECURITY_DEFEX")

# --- fs/proc/base.c ---
edit("fs/proc/base.c",
    "#include <linux/resctrl.h>\n#include <linux/task_integrity.h>\n#include <linux/proca.h>\n#include <linux/cpufreq_times.h>\n#include <linux/cn_proc.h>\n",
    "#include <linux/resctrl.h>\n#include <linux/cn_proc.h>\n#include <linux/cpufreq_times.h>\n")
edit("fs/proc/base.c",
    "#include <linux/tracehook.h>\n#include <linux/printk.h>\n",
    "#include <linux/tracehook.h>\n#include <linux/task_integrity.h>\n#include <linux/proca.h>\n#include <linux/printk.h>\n")
