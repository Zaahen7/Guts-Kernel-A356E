<div align="center">

# ❄️ GutsKernel for Samsung Galaxy A35 5G ❄️
[![Build Status](https://img.shields.io/github/actions/workflow/status/Zaahen7/Guts-Kernel-A356E/GutsKernel-build.yml?label=Build%20Status&style=for-the-badge&logo=github)](https://github.com/Zaahen7/Guts-Kernel-A356E/actions)
[![GitHub Release](https://img.shields.io/github/v/release/Zaahen7/Guts-Kernel-A356E?label=Latest%20release&style=for-the-badge&color=blue)](https://github.com/Zaahen7/Guts-Kernel-A356E/releases/latest)

</div>

> [!CAUTION]
> **I am not responsible for any bricked devices, hardware damage, data loss, or other issues that may occur while using or flashing this kernel. By choosing to flash this kernel, you acknowledge and accept all associated risks. You are solely responsible for any consequences resulting from its use. Flash at your own risk!**

<div align="center">
<table>
  <tr>
    <th colspan="3">Prebuilt Kernels Info</th>
  </tr>
  <tr>
    <th>Variant</th>
    <th>Root Solution</th>
    <th>Features</th>
  </tr>
  <tr>
    <td>🌸 <strong>Puck</strong></td>
    <td><strong>No root</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, Extended-tmpfs & HM VFS Support</td>
  </tr>
  <tr>
    <td>👹 <strong>Zodd</strong></td>
    <td><strong>KSU + SUSFS</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, Extended-tmpfs & HM VFS Support</td>
  </tr>
  <tr>
    <td>🦅 <strong>Griff</strong></td>
    <td><strong>KSU-Next + SUSFS</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, Extended-tmpfs & HM VFS Support</td>
  </tr>
  <tr>
    <td>❓ <strong>Zoro</strong></td>
    <td><strong>Baka-SU + SUSFS</strong></td>
    <td>Full LTO, Optimization patches, BBG, BBRv3, Net Scheds, Wireguard, Extended-tmpfs & HM VFS Support</td>
  </tr>
</table>
</div>

## ⚙️ Kernel Build Workflow Features
Clone the repository and build your kernel your way using the **GitHub Actions workflow**.
### **🛠️ Available Features**
- **Kernel Variants** — Select which kernel variants to build.
- **One UI Version** — Choose your target One UI version. Currently, only One UI 8.5 is supported.
- **Link-Time Optimization (LTO)** — Choose between Full, Thin, or Default LTO modes.
- **Kernel Optimization Patches** — Enable or disable additional kernel optimization patches.
- **SUSFS Support** — Toggle SUSFS integration. [**Learn more**](https://gitlab.com/simonpunk/susfs4ksu)
- **Baseband-Guard Support (BBG)** — Toggle Baseband-Guard integration. [**Learn more**](https://github.com/vc-teahouse/Baseband-guard)
- **Additional Network Schedulers** — Enable FQ, FQ-CoDel, PIE, FQ-PIE, and CAKE net schedulers.
- **WireGuard Support** — WireGuard remains enabled by default, as it is already enabled on the Galaxy A35 :p
- **BBR & BBRv3 TCP Congestion Control** — Add BBR and BBRv3 support. You still have to set it manually.
- **TMPFS XATTR / POSIX ACL** — Extended TMPFS support for meta modules and [**Mountify**](https://github.com/backslashxx/mountify).
- **Built-in VFS Metamodule Support** — Choose between [**Hybrid-Mount**](https://github.com/Hybrid-Mount/meta-hybrid_mount), [**NoMount**](https://github.com/maxsteeel/nomount) and disabled.

## ⭐ Special thanks!
- **Samsung**, for the base kernel source
- **tiann**, for [**KernelSU**](https://github.com/tiann/KernelSU)
- **rifsxd**, for [**KernelSU-Next**](https://github.com/KernelSU-Next/KernelSU-Next)
- **pershoot**, for [**KernelSU-Next SUSFS fork**](https://github.com/pershoot/KernelSU-Next/tree/dev-susfs)
- **Baka-SU** for [**Baka-SU**](https://github.com/Baka-SU/BakaSU)
- **WildKernels** for [**Kernel Patches**](https://github.com/WildKernels/kernel_patches)
- **simonpunk**, for [**SUSFS**](https://gitlab.com/simonpunk/susfs4ksu)
- **vc-teahouse**, for [**Baseband-guard**](https://github.com/vc-teahouse/Baseband-guard)
- **backslashxx**, for [**Mountify**](https://github.com/backslashxx/mountify)
- **Hybrid-Mount**, for [**Hybrid-Mount**](https://github.com/Hybrid-Mount/meta-hybrid_mount)
- **maxsteeel**, for [**NoMount**](https://github.com/maxsteeel/nomount)

