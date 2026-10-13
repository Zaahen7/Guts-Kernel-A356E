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
