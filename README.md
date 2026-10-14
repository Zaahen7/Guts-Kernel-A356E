<div align="center">

# ❄️ GutsKernel — A356E (Galaxy A35 5G, Exynos 1380)
[![Build Status](https://img.shields.io/github/actions/workflow/status/Zaahen7/Guts-Kernel-A356E/GutsKernel-build.yml?label=Build%20Status&style=for-the-badge&logo=github)](https://github.com/Zaahen7/Guts-Kernel-A356E/actions)
[![GitHub Release](https://img.shields.io/github/v/release/Zaahen7/Guts-Kernel-A356E?label=Latest%20release&style=for-the-badge&color=blue)](https://github.com/Zaahen7/Guts-Kernel-A356E/releases/latest)

</div>

<div align="center">
<table>
  <tr>
    <th colspan="3">Prebuilt Kernel Variants</th>
  </tr>
  <tr>
    <th>Variant</th>
    <th>Root Solution</th>
    <th>Features</th>
  </tr>
  <tr>
    <td>🌸 <strong>Puck</strong></td>
    <td><strong>No root</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, HM VFS Support</td>
  </tr>
  <tr>
    <td>🗿 <strong>Zodd</strong></td>
    <td><strong>KSU + SUSFS</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, HM VFS Support</td>
  </tr>
  <tr>
    <td>🥀 <strong>Femto</strong></td>
    <td><strong>KSU-Next + SUSFS</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, HM VFS Support</td>
  </tr>
  <tr>
    <td>❓ <strong>Zoro</strong></td>
    <td><strong>Baka-SU + SUSFS</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, HM VFS Support</td>
  </tr>
</table>
</div>

### Workflow Features
- **Select Kernel Variants to build**
- **Choose One UI Version** - Only One UI 8.5 for now
- **Choose Link-Time Optimization(LTO) Mode** - Full, Thin or Default
- **Toggle Kernel Optimization Patches**
- **Toggle SUSFS** [**(?)**](https://gitlab.com/simonpunk/susfs4ksu)
- **Toggle Baseband-Guard** - [(?)](https://github.com/vc-teahouse/Baseband-guard)
- **Toggle Additional Network Schedulers** - Enables FQ, FQCODEL, PIE, FQPIE & CAKE net schedulers
- **Toggle BBR & BBRv3 TCP Congestion Control Algorithms** - Manual configuration is still required
- **Choose builtin VFS metamodule support** - [**Hybrid-Mount**](https://github.com/Hybrid-Mount/meta-hybrid_mount) or [NoMount](https://github.com/maxsteeel/nomount)

## ⭐ Special thanks!
- **Samsung**, for the base kernel source.
- **tiann**, for [KernelSU](https://github.com/tiann/KernelSU).
- **rifsxd**, for [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next).
- **pershoot**, for [KernelSU-Next SUSFS fork](https://github.com/pershoot/KernelSU-Next/tree/dev-susfs).
- **Baka-SU** for [Baka-SU](https://github.com/Baka-SU/BakaSU).
- **WildKernels** for [Kernel Patches](https://github.com/WildKernels/kernel_patches).
- **simonpunk**, for [SUSFS](https://gitlab.com/simonpunk/susfs4ksu).
- ****

