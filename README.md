# GutsKernel — A356E (Galaxy A35 5G, Exynos 1380)

Custom kernel based on Samsung's One UI 8.5 kernel source (5.15.189),
built for the Galaxy A35 5G (SM-A356E). Focused primarily on battery
efficiency, with KernelSU + SUSFS root support and a runtime tuning
module for values that live outside the kernel image.

## Base
- Kernel: 5.15.189, Samsung One UI 8.5 source
- Device: Samsung Galaxy A35 5G (SM-A356E), Exynos 1380 (s5e8835)
- Toolchain: Clang (AOSP r450784d), Full LTO
- Root: KernelSU (tiann) + SUSFS4KSU

## Kernel patches

### Power management
- Dynamic alarm wakeup timing: replaces a fixed 2s wakeup window with
  the actual time until the next pending alarm
- Avoid redundant s2idle wake attempts: prevents duplicate sync work
  on concurrent wakeup events
- Reduced freeze timeout: 20s → 1s for Android's process freezer
  (a 20s wait on a deadlocked freeze was pure battery waste)
- Silenced non-actionable IRQ affinity and system log spam
  (healthd/logd/dashd), reducing log I/O overhead

### CPU / scheduler
- Disabled CACHE_HOT_BUDDY: this SoC's DSU shares L3 cache across
  cores within a cluster, making the original cache-locality
  restriction unnecessary and limiting to the scheduler
- Optimized CPU scan order in select_idle_capacity (skips re-checking
  a CPU already evaluated by the caller)
- Added a hard 768MHz floor on `scaling_min_freq` requests, on top of
  a runtime-adjustable ceiling (`scaling_min_freq_limit`, exposed via
  sysfs) to stop misbehaving apps/tools from pinning the CPU to an
  unnecessarily high minimum frequency

### Filesystem (F2FS)
- Reduced I/O congestion timeout: 20ms → 6ms
- Increased min fsync blocks: 8 → 20 (fewer forced syncs, better
  write batching)
- Reduced GC urgent sleep time: 500ms → 50ms (aligns with what
  Android's `vold` already tries to configure via IdleMaintenance)

### Memory
- zstd as the default zram compression algorithm (better ratio than
  the stock lzo-rle, worthwhile given typical available RAM on this
  device)
- MGLRU (Multi-Gen LRU) confirmed active — modern page reclaim
  already backported to this GKI base
- PSI (Pressure Stall Information) confirmed active — used by modern
  LMKD for smarter low-memory kill decisions

### Low-level / arch
- 16-byte alignment for `clear_page()`
- 8-byte alignment for `struct file`

### Security
- SELinux hide enabled by default (KernelSU's native anti-detection
  feature, backed by a clean sepolicy snapshot)

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
