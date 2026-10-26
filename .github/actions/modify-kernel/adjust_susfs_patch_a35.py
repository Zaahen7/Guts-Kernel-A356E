import argparse
import os
from pathlib import Path
import sys


def replace_once(content, old, new, description):
    occurrences = content.count(old)
    if occurrences != 1:
        raise ValueError(
            f"Expected one occurrence of {description}, found {occurrences}."
        )
    return content.replace(old, new, 1)


def prepare_susfs_patch(content):
    content = replace_once(
        content,
        " #include <trace/hooks/blk.h>\n",
        "",
        "the obsolete blk trace include removal",
    )
    content = replace_once(
        content,
        " unsigned int sysctl_mount_max __read_mostly = 100000;\n \n",
        " unsigned int sysctl_mount_max __read_mostly = 100000;\n \n"
        " /* @fs.sec -- c4d165e8cb5ea1cc14cdedb9eab23efd642d4d5f -- */\n",
        "the fs.sec context marker",
    )
    content = replace_once(
        content,
        " new = copy_tree(old, old->mnt.mnt_root, copy_flags);\n"
        " if (IS_ERR(new)) {\n"
        "  namespace_unlock();\n",
        " #ifdef CONFIG_KDP_NS\n"
        " \tnew = copy_tree(old, ((struct kdp_mount *)old)->mnt->mnt_root, copy_flags);\n"
        " #else\n",
        "the CONFIG_KDP_NS namespace context",
    )
    content = replace_once(
        content,
        " #include <trace/hooks/mm.h>\n",
        " +#if defined(CONFIG_KSU_SUSFS_SUS_KSTAT) || defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)\n"
        " +#include <linux/susfs_def.h>\n"
        " +#endif // #if defined(CONFIG_KSU_SUSFS_SUS_KSTAT) || defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)\n",
        "the conditional susfs_def.h include",
    )
    return replace_once(
        content,
        " #include <asm/tlb.h>\n",
        " #include <asm/tlb.h>\n #include <asm/tlbflush.h>\n",
        "the tlbflush.h context",
    )


def prepare_oneui_85_kernel(kernel_dir):
    changes = {
        "fs/exec.c": (
            (
                "#include <linux/binfmts.h>\n#include <linux/utsname.h>\n",
                "#include <linux/binfmts.h>\n"
                "#include <linux/task_integrity.h>\n"
                "#include <linux/utsname.h>\n",
                "the exec.c task_integrity include insertion",
            ),
            (
                "#include <linux/syscall_user_dispatch.h>\n"
                "#include <linux/task_integrity.h>\n",
                "#include <linux/syscall_user_dispatch.h>\n",
                "the exec.c duplicate task_integrity include",
            ),
        ),
        "fs/namespace.c": (
            (
                "#include <linux/security.h>\n",
                "#include <linux/security.h>\n"
                "#include <linux/delay.h>\n"
                "#include <linux/fslog.h>\n"
                "#ifdef CONFIG_KDP_NS\n"
                "#include <linux/kdp.h>\n"
                "#endif\n",
                "the namespace.c KDP and Samsung include insertion",
            ),
            (
                "#include <linux/mnt_idmapping.h>\n"
                "#include <linux/delay.h>\n"
                "#include <linux/fslog.h>\n"
                "#ifdef CONFIG_KDP_NS\n"
                "#include <linux/kdp.h>\n"
                "#endif\n",
                "#include <linux/mnt_idmapping.h>\n",
                "the namespace.c duplicate Samsung includes",
            ),
        ),
        "fs/open.c": (
            (
                "struct file *f = do_filp_open(dfd, tmp, &op);\n\n"
                "#ifdef CONFIG_SECURITY_DEFEX\n",
                "struct file *f = do_filp_open(dfd, tmp, &op);\n"
                "#ifdef CONFIG_SECURITY_DEFEX\n",
                "the open.c extra blank line",
            ),
        ),
        "fs/proc/base.c": (
            (
                "#include <linux/tracehook.h>\n",
                "#include <linux/tracehook.h>\n"
                "#include <linux/task_integrity.h>\n"
                "#include <linux/proca.h>\n",
                "the proc/base.c integrity include insertion",
            ),
            (
                "#include <linux/resctrl.h>\n"
                "#include <linux/task_integrity.h>\n"
                "#include <linux/proca.h>\n"
                "#include <linux/cpufreq_times.h>\n"
                "#include <linux/cn_proc.h>\n",
                "#include <linux/resctrl.h>\n"
                "#include <linux/cn_proc.h>\n"
                "#include <linux/cpufreq_times.h>\n",
                "the proc/base.c reordered includes",
            ),
        ),
    }

    prepared_files = {}
    for relative_path, replacements in changes.items():
        path = kernel_dir / relative_path
        content = path.read_text()
        for old, new, description in replacements:
            content = replace_once(content, old, new, description)
        prepared_files[path] = content

    for path, content in prepared_files.items():
        path.write_text(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kernel_dir", type=Path)
    parser.add_argument("susfs_patch", type=Path)
    args = parser.parse_args()

    kernel_dir = args.kernel_dir.resolve()
    susfs_patch = args.susfs_patch.resolve()
    oneui_version = os.environ.get("ONEUI_VERSION")
    if not oneui_version:
        parser.error("ONEUI_VERSION environment variable is required")

    try:
        if oneui_version == "8.5":
            prepare_oneui_85_kernel(kernel_dir)
        patch_content = prepare_susfs_patch(susfs_patch.read_text())
        susfs_patch.write_text(patch_content)
    except (OSError, ValueError) as error:
        print(f"ERROR: Failed to prepare SUSFS: {error}", file=sys.stderr)
        return 1

    print("Prepared SUSFS patch.")
    if oneui_version == "8.5":
        print("Prepared kernel sources for One UI 8.5.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
