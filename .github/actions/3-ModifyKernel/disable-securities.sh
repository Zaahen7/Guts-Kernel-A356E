#!/bin/bash
set -euo pipefail

echo "===== DISABLING SAMSUNG SECURITY FEATURES ====="
"$KERNEL_DIR/scripts/config" \
  --file "$A35_DEFCONFIG" \
  --disable CONFIG_UH \  #Samsung Unified Hypervisor
  --disable CONFIG_RKP \  #Real-time Kernel Protection 
  --disable CONFIG_KDP \  #Samsung Kernel Data Protection
  --disable CONFIG_SECURITY_DEFEX \ #Samsung exploit and privilege-escalation protection
  --disable CONFIG_FIVE \ #Samsung process and file integrity protection
  --disable CONFIG_PROCA  #Samsung process and file integrity protection

echo ""
echo "===== SAMSUNG SECURITY CONFIGURATION ====="
grep -E 'CONFIG_(UH|RKP|SECURITY_DEFEX|PROCA|FIVE|KDP)' "$A35_DEFCONFIG" || true
echo "==========================================="
