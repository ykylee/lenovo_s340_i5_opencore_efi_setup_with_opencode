# AGENTS.md - Agent Coding Guidelines for OpenCore EFI Project

## Overview
This document provides guidelines for agentic coding agents operating in this repository, which focuses on setting up EFI for installing macOS Ventura on Lenovo IdeaPad S340 laptops with Intel Core i5-8265U CPU.

## Build/Lint/Test Commands

### EFI Validation Commands
```bash
# Check EFI structure and count essential files
find EFI -type f \( -name "*.efi" -o -name "*.plist" -o -name "*.aml" \) | wc -l

# Validate ACPI tables with detailed output
find EFI/OC/ACPI -name "*.aml" -exec iasl -tc {} \;

# Validate config.plist syntax (requires proper tools)
# Note: Actual validation requires MaciASL or PlistED++/ProperTree
# Example using xmllint (basic validation):
xmllint --noout EFI/OC/config.plist

# Verify kext signatures and dependencies
find EFI/OC/Kexts -name "*.kext" -exec sh -c 'echo "Checking {}"; kextutil -n {} 2>/dev/null || echo "Failed: {}"' \;

# Check for required OpenCore components
test -f EFI/OC/OpenCore.efi && echo "OpenCore.efi found" || echo "OpenCore.efi missing"
test -f EFI/BOOT/BOOTX64.EFI && echo "BOOTX64.EFI found" || echo "BOOTX64.EFI missing"

# Validate Kernel cache (if present)
test -f EFI/OC/KernelCache && echo "KernelCache present" || echo "No KernelCache"

# Check Drivers directory
ls -la EFI/OC/Drivers/*.efi 2>/dev/null | wc -l | xargs echo "UEFI Drivers:"
```

### VM Testing Commands (if using QEMU/KVM)
```bash
# Basic QEMU boot test (limited functionality)
qemu-system-x86_64 \
  -enable-kvm \
  -m 4G \
  -cpu host \
  -drive if=pflash,format=raw,readonly,file=/usr/share/OVMF/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=/usr/share/OVMF/OVMF_VARS.fd \
  -drive format=raw,file=fat:rw:EFI \
  -usb -device usb-kbd -device usb-mouse \
  -netdev user,id=net0 -device e1000,netdev=net0 \
  -vga qxl

# Alternative: Using OpenCore Legacy Patcher for basic validation
# Note: Full macOS boot in VM requires additional setup
```

### Diagnostic Commands
```bash
# Check for common EFI issues in logs
grep -r -i "error\|fail\|panic\|assert" EFI/OC/ 2>/dev/null || echo "No obvious errors found in config"

# Validate ACPI syntax with detailed reporting
find EFI/OC/ACPI -name "*.aml" -exec iasl -tc {} \; 2>&1 | grep -E "(Error|Remark|Warning|Optimal)" || echo "ACPI syntax check completed"

# Check for duplicate kexts by bundle identifier
find EFI/OC/Kexts -name "*.kext" -exec sh -c 'echo "$(defaults read {}/Contents/Info.plist CFBundleIdentifier 2>/dev/null || echo "NO_ID"): {}"' \; | sort | uniq -d

# Validate plist files for basic XML well-formedness
find EFI/OC -name "*.plist" -exec sh -c 'echo "Checking {}"; plutil -lint {} 2>/dev/null || echo "Invalid: {}"' \;

# Check for proper kext installation (executable permissions)
find EFI/OC/Kexts -name "*.kext" -exec test -x {}/Contents/MacOS/* 2>/dev/null \; -print | wc -l | xargs echo "Kexts with executables:"
```

## Code Style Guidelines

### Configuration Files (.plist)
- Use proper XML formatting with consistent indentation (2 spaces)
- Boolean values: `<true/>` or `<false/>` (not strings)
- Integer values: `<integer>...</integer>`
- String values: `<string>...</string>`
- Date values: `<date>YYYY-MM-DDTHH:MM:SSZ</date>`
- Data values: `<data>...</data>` (base64 encoded)
- Array values: `<array>...</array>`
- Dictionary values: `<dict>...</dict>`
- Comments: Use XML comments `<!-- comment -->` for plist files
- Max line length: 120 characters for config.plist
- Trailing spaces: Remove all trailing whitespace
- Empty lines: Use sparingly to separate logical sections

### ACPI/DSDT Patches and SSDTs
- Use descriptive comments explaining purpose
- Group related patches together (power management, USB, audio, etc.)
- Use consistent naming conventions for custom methods (e.g., `RMNE` for _Rename, `PNLF` for Panel Brightness)
- Custom SSDTs: Prefix with `SSDT-` followed by descriptive name (e.g., `SSDT-EC-USBX.aml`)
- Validate all patches with MaciASL before inclusion
- Prefer SSDT-based fixes over DSDT patches when possible
- Follow naming conventions from ACPI specification
- Ensure all referenced AML files exist in the ACPI directory
- Use proper package syntax and data types in ASL code
- Avoid hardcoding memory addresses when possible; use dynamic allocation

### Kext Management
- Only include necessary kexts (avoid bloat)
- Keep kexts updated to latest compatible versions
- Prefer Lilu-based plugins when possible
- Verify kext compatibility with target macOS version (Ventura = 13.x)
- Organize kexts by function: Lilu/plugins, VirtualSMC, audio, networking, input, misc
- Check executable permissions: kext Contents/MacOS/* should be executable
- Avoid modifying kext Info.plist unless absolutely necessary
- Prefer OC-sanitized kexts where available (e.g., from acidanthera/oc-binaries)
- Monitor for kext conflicts (especially with similar functionality)

### Naming Conventions
- ACPI methods: Use descriptive names (e.g., `RMNE` for _Rename, `PNLF` for Panel Brightness)
- Custom SSDTs: Prefix with `SSDT-` followed by descriptive name (e.g., `SSDT-EC-USBX.aml`)
- Kexts: Use official bundle identifiers where applicable
- Config keys: Follow Apple's naming conventions
- UEFI drivers: Use standard OpenCore driver names (OpenRuntime.efi, OpenCanopy.efi, etc.)
- Tools: Use descriptive names for UEFI tools (memtest86, Shell, etc.)
- NVRAM variables: Use standard Apple variable names when possible

### Import Ordering (for config.plist)
Follow this strict order to ensure proper initialization:
1. ACPI (Add, Delete, Patch)
2. Booter
3. DeviceProperties
4. Kernel (Add, Block, Emulate, Force, Patch, Quirks, Scheme)
5. Misc (Boot, Debug, Entries, Security, Tools)
6. NVRAM (Add, Delete, LegacySchema, Overwrite)
7. PlatformInfo
8. UEFI (APFS, Audio, Drivers, Input, Output, Quirks, ReservedMemory)

### Formatting Rules
- Max line length: 120 characters for config.plist
- Indentation: 2 spaces (no tabs)
- Trailing spaces: Remove all trailing whitespace
- Empty lines: Use sparingly to separate logical sections
- Comments: Use XML comments `<!-- comment -->` for plist files
- For ASL/SSDT files: Use 4-space indentation, descriptive comments
- For kext Info.plist: Follow standard Apple plist formatting

### Type Safety
- Use correct data types in plist (don't store numbers as strings)
- Validate all DeviceProperties additions
- Ensure PCI addresses are correctly formatted
- Use proper hexadecimal format for memory addresses
- Check that all required properties are present for each kext
- Validate that kext dependencies are met
- Ensure proper executable paths in kext Info.plist

### Error Handling
- Always validate ACPI patches before committing
- Test kext injection order dependencies
- Verify config.plist with proper tools (PlistED++, ProperTree, MaciASL)
- Maintain bootable backups before making changes
- Document all changes with clear commit messages
- Check build warnings and errors from validation tools
- Test one change at a time to isolate issues
- Keep a working EFI backup before major changes

### Specific to Hackintosh/OpenCore for Lenovo IdeaPad S340
- Prefer SSDT-based fixes over DSDT patches when possible
- Use OC-sanitized kexts where available
- Keep OpenCore firmware updated to latest stable release
- Follow Dortania's OpenCore Install Guide guidelines
- Validate SMBIOS against actual hardware specifications (MacBookPro15,4 or similar for i5-8265U)
- Use proper USB port mapping (SSDT-UIAC or similar)
- Implement proper power management (SSDT-PLUGIN or equivalent)
- For WiFi: Use AirportBrcmFixup.kext for Broadcom cards (as specified by user)
- For Bluetooth: Use BlueToolFixup.kext with IntelBluetoothFirmware.kext or similar
- For audio: Use AppleALC.kext with appropriate layout-id
- For trackpad: Use VoodooI2C.kext and related plugins
- For power management: Use SSDT-PLUG.aml and proper CPU power management kexts

## Additional Guidelines

### Commit Messages
- Use Korean language for commit messages
- Format: `[구역] 설명` (e.g., `[ACPI] SSDT-EC 추가로 배터리 관리 개선`)
- Include specific hardware references when relevant
- Document testing results when applicable
- Reference issue numbers if applicable
- Use conventional prefixes:
  - `[ACPI]`: ACPI tables, SSDTs, DSDT patches
  - `[KEXT]`: Kernel extensions addition/removal/update
  - `[CONFIG]`: config.plist changes
  - `[UEFI]`: UEFI drivers, tools, settings
  - `[DOC]`: Documentation updates
  - `[FIX]`: Bug fixes, issue resolutions
  - `[REF]`: Code refactoring, cleanup
  - `[ADD]`: New feature additions
  - `[RM]`: Removal of components

### Documentation Standards
- All documentation in Korean
- Include hardware specifics (Lenovo IdeaPad S340 variant with i5-8265U)
- Reference specific BIOS versions when relevant
- Link to Dortania guides or other authoritative sources
- Include troubleshooting tips for common issues
- Document known working and non-working features
- Include hardware-specific quirks and solutions
- Maintain a changelog of significant updates

### Safety Practices
- Always maintain a working backup EFI
- Test changes in VM when possible before hardware testing
- Verify compatibility with specific Lenovo IdeaPad S340 sub-model (i5-8265U)
- Check for Windows/Linux dual-boot compatibility requirements
- Monitor temperatures and power management after changes
- Test boot time and performance impacts
- Verify sleep/wake functionality
- Test audio, WiFi, Bluetooth, USB ports
- Test external display output if applicable
- Test boot picker and theme functionality
- Validate NVRAM variable persistence

### Tools Reference
- ProperTree: Plist editing (primary tool for config.plist)
- MaciASL: ACPI/DSDT editing and compilation
- GenSMBIOS: SMBIOS data generation
- Hackintool: USB/Audio/Framebuffer patching and system information
- OpenCore Patcher: For unsupported hardware scenarios
- MountEFI: Helper script for mounting EFI partition
- ocvalidate: OpenCore configuration validator
- iasl: ACPI compiler and disassembler
- plutil: Property list utility
- kextutil: Kernel extension utility
- logs: Console.log utility for debugging

### Version References
- OpenCore: Latest stable release (check https://github.com/acidanthera/OpenCorePkg/releases)
- macOS: Ventura (13.x)
- Lilu: Latest release
- VirtualSMC: Latest release
- WhateverGreen: Latest release
- AppleALC: Latest release
- AirportBrcmFixup: Latest release
- BlueToolFixup: Latest release
- VoodooI2C: Latest release
- VoodooPS2Controller: Latest release
- NVMeFix: Latest release
- RestrictEvents: Latest release
- SMCBatteryManager: Latest release
- ECEnabler: Latest release
- BrightnessKeys: Latest release
- HibernationFixup: Latest release
- NoTouchID: Latest release

### Testing Checklist
Before considering a change complete:
[ ] Config.plist validates without errors
[ ] All referenced ACPI tables exist and compile
[ ] All kexts have proper executable permissions
[ ] No duplicate kext bundle identifiers
[ ] Boot process reaches macOS installer or desktop
[ ] Essential hardware works (keyboard, trackpad, display)
[ ] Audio input/output functions
[ ] WiFi and Bluetooth connect (if applicable)
[ ] USB ports function correctly
[ ] Sleep/wake works properly
[ ] Battery status displays correctly
[ ] No kernel panics during boot or operation
[ ] System information is properly detected
[ ] Services like iCloud, App Store function
[ ] Shutdown and restart work properly