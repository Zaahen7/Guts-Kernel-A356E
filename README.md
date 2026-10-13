<div align="center">

## GutsKernel — A356E (Galaxy A35 5G, Exynos 1380)
[![Build Status](https://img.shields.io/github/actions/workflow/status/Zaahen7/Guts-Kernel-A356E/GutsKernel-build.yml?label=Build%20Status&style=for-the-badge&logo=github)](https://github.com/Zaahen7/Guts-Kernel-A356E/actions)
[![GitHub Release](https://img.shields.io/github/v/release/Zaahen7/Guts-Kernel-A356E?label=release&style=for-the-badge&color=blue)](https://github.com/Zaahen7/Guts-Kernel-A356E/releases/latest)
</div>

## Prebuilted Kernel Variants
<br>

|  Variant | Root Solution | ✨Features |
|:---|:---|:---|
| 🌸 **Puck / Clean** | No root | BBG|
| 💢 **Zodd / KSU** | KernelSU+SUSFS | BBG |
| 🔐 **KernelSU-Next** | Next-generation kernel-level root solution |
| 🛡️ **SUSFS v2.2.0+** | Advanced root hiding with Magic Mount support (Auto-synced) |
| 🔋 **Battery Optimization** | Modular suite: Wakelock hard-caps, Schedutil tuning, MGLRU, and Log Silencing |
| 🛠️ **Manual Hooks** | `scope_min_manual_hooks_v1.4` for better app compatibility |
| 🖧 **BBRv3** | Next-gen TCP congestion control |
| 🛡️ **BBG** | LSM-based Baseband Guard security |
| 🌐 **TTL Target Support** | Network packet manipulation |
| 🧱 **IP Set Support** | Advanced firewall capabilities |
| 🔄 **NTSync** | Universal NT synchronization primitives for gaming |
| 🛂 **WireGuard** | Fast, modern, and secure kernel-level VPN |
| 🏗️ **HMBIRD SCX** | Scheduler extensions for SM8750 devices |
| ✅ **LTO** | Link Time Optimization (thin/full/none configurable) |
| ⚡️ **TMPFS XATTR** | Extended attributes for Mountify and Meta support |
| 🚀 **Optimization patches** | Memory, I/O, CPU scheduler, network tuning |
| </> **Unicode Bypass Fix** | Prevent path traversal using non-printable Unicode codepoints |
| 🖥️ **Droidspaces Support** | Support for Portable Linux containers |

<br>
- Toolchain: Clang (AOSP r450784d), Full LTO


## What's intentionally NOT changed
Some areas were investigated and left untouched because they were
already well-tuned for this hardware, or because the expected gain
didn't justify the risk:
- **cpuidle residency**: both idle states already reach healthy usage
  ratios; no evidence of a miscalibrated governor
- **I/O scheduler**: Samsung's `ssg` scheduler outperformed
  `mq-deadline` in direct sequential-write benchmarks on this UFS
  controller
- **THP**: already `never` at runtime, correct for constrained RAM
- **GPU frequency governor**: only `highspeed_delay` tuning applied
  (2 cycles instead of 0), filtering short load spikes without
  touching max clock or thermal behavior
- **Undervolt, RCU backporting**: high risk relative to expected
  battery gain, deliberately out of scope

## Runtime tuning module (KernelSU)
Some tunables live in sysfs nodes that reset on every reboot (EMS/EGO
governor parameters, GPU DVFS delay, the custom min-freq ceiling,
swappiness, zram algorithm). These are applied via a KernelSU module
rather than hardcoded in the kernel, so they can be adjusted without
recompiling:
- EGO rate-limit: little cluster 4ms → 16ms, big cluster 4ms → 6ms
- EGO htask_boost: 150 → 100
- GPU highspeed_delay: 0 → 2
- CPU scaling_min_freq_limit: 672000 (little) / 754000 (big)
- vm.swappiness: 100
- zram compression algorithm: forced to zstd if not already active,
  with a free-RAM safety check before switching

Module source: `/module/` — includes `service.sh` (applies tweaks on
boot, after a delay), `apply_tweaks.sh` (the actual tuning logic),
and `action.sh` (on-demand status refresh from the KernelSU manager).

## Pending / candidates for future work
- **Baseband Guard**: LSM-based protection for baseband/boot-chain
  partitions against unauthorized writes — security, not battery,
  but a reasonable addition
- **WireGuard (native kernel module)**: only relevant if using
  WireGuard as a VPN; meaningfully more efficient than userspace
  WireGuard implementations
- **CAKE/PIE qdiscs**: adding as available modules (not as default)
  costs nothing while inactive; useful only for specific bufferbloat
  scenarios, not applied by default here

## Building
See `build.sh`. Produces both an AnyKernel3-flashable zip and an
Odin-flashable tar. Note: this device's kernel dtb is *not* read from
the `boot` partition — it lives in `vendor_boot`. Flashing via
AnyKernel3's `dtb` mechanism (which patches `vendor_boot` correctly)
is the supported path; the Odin tar currently only replaces `boot`
and will not carry dtb changes.

## Credits
- Samsung, for the base kernel source
- tiann, for KernelSU
- simonpunk, for SUSFS4KSU
- Sultan Alsawaf, Park Ju Hyung, Danny Lin, Jesse Chan, Adithya R,
  Panchajanya1999, ztc1997, Hao Jia, Matteo Croce, Colin Ian King,
  Wilco Dijkstra, Arjan van de Ven — authors of the individual
  optimization patches referenced above
