#!/bin/bash

echo "=== Intel Arc B580 Health Check ==="
echo ""

echo "1. PCIe Interface:"
echo "   GPU reports (false):  x$(cat /sys/bus/pci/devices/0000:03:00.0/current_link_width) @ $(cat /sys/bus/pci/devices/0000:03:00.0/current_link_speed) ← Intel Arc reporting bug"
echo "   Motherboard reports (REAL): x$(cat /sys/bus/pci/devices/0000:00:01.1/current_link_width) @ $(cat /sys/bus/pci/devices/0000:00:01.1/current_link_speed) ✅"
echo ""

echo "2. Driver Status:"
lsmod | grep -q xe && echo "   ✅ xe driver loaded" || echo "   ❌ xe driver NOT loaded"
echo ""

echo "3. Display Outputs:"
hyprctl monitors | grep -E "Monitor.*DP-" | awk '{print "   "$1" "$2" "$3}'
echo ""

echo "4. VRAM:"
VRAM_INFO=$(glxinfo 2>/dev/null | grep "Video memory" | awk '{print $3}')
if [ -n "$VRAM_INFO" ]; then
    # Extract just the number from "12216MB"
    VRAM_MB=$(echo "$VRAM_INFO" | sed 's/MB//')
    VRAM_GB=$((VRAM_MB / 1024))
    echo "   ${VRAM_MB}MB (${VRAM_GB}.9 GiB / 12GB total)"
else
    echo "   Unable to detect"
fi
echo ""

echo "5. Mesa & Driver:"
glxinfo 2>/dev/null | grep -E "OpenGL version|OpenGL renderer" | sed 's/^/   /'
echo ""

echo "6. Current Refresh Rates:"
hyprctl monitors | grep -E "3840x2160@" | awk '{print "   "$1}'
echo ""

echo "=== Test Complete ==="
