# EFI 현재 상태

## 개요

이 문서는 Lenovo IdeaPad S340 (i5-8265U) OpenCore EFI의 현재 상태를 기록합니다.

---

## 디렉터리 구조

```
EFI/
├── BOOT/                    # (미생성 - OpenCore 빌드 시 생성)
│   └── BOOTX64.EFI
└── OC/
    ├── ACPI/
    │   ├── Add/             # SSDT 테이블 (비어있음)
    │   ├── Patch/           # ACPI 패치 (비어있음)
    │   └── Delete/          # ACPI 삭제 (비어있음)
    ├── Drivers/             # UEFI 드라이버 (비어있음)
    ├── Kexts/               # 커널 확장 (비어있음)
    ├── Tools/               # UEFI 도구 (비어있음)
    ├── Resources/            # 부트 피커 리소스 (미생성)
    │   ├── Image/
    │   ├── Label/
    │   └── Audio/
    ├── OpenCore.efi         # (미존재 - 다운로드 필요)
    └── config.plist         # ✅ 존재
```

---

## 현재 파일 목록

### OC/config.plist
- **상태**: ✅ 존재
- **크기**: 5,746 bytes
- **마지막 수정**: 2024-04-01

### ACPI/Add/
```
(비어있음)
```

### Drivers/
```
(비어있음)
```

### Kexts/
```
(비어있음)
```

### Tools/
```
(비어있음)
```

---

## config.plist 현재 설정 상태

### ACPI 섹션
| 항목 | 상태 | 비고 |
|------|------|------|
| SSDT-EC.aml | 추가됨 | Enable |
| SSDT-HPET.aml | 추가됨 | Enable |
| SSDT-PLUG.aml | 추가됨 | Enable |
| SSDT-PNLF.aml | 추가됨 | Enable |
| SSDT-USBX.aml | 추가됨 | Enable |
| SSDT-XOSI.aml | 추가됨 | Enable |
| _OSI to XOSI 패치 | 활성화됨 | |

### Booter 섹션
| Quirks | 상태 |
|--------|------|
| AvoidRuntimeDefrag | true |
| EnableSafeModeSlide | true |
| ProvideCustomSlide | true |
| RebuildAppleMemoryMap | true |
| SyncRuntimePermissions | true |

### Kernel 섹션
| 항목 | 상태 |
|------|------|
| Lilu.kext | 추가됨 |
| VirtualSMC.kext | 추가됨 |
| AppleCpuPmCfgLock | true |
| AppleXcpmCfgLock | true |
| PanicNoKextDump | true |
| PowerTimeoutKernelPanic | true |
| ProvideCurrentCpuInfo | true |
| XhciPortLimit | true |

### DeviceProperties 섹션
| 항목 | 상태 |
|------|------|
| Add | 비어있음 (주입 필요) |

### Misc 섹션
| 항목 | 설정값 |
|------|--------|
| ShowPicker | true |
| PickerMode | External |
| Timeout | 5 |
| DisableWatchDog | true |

### NVRAM 섹션
| 항목 | 설정값 |
|------|--------|
| boot-args | -v keepsyms=1 alcid=11 |
| csr-active-config | 030E0000 |
| WriteFlash | true |

### PlatformInfo 섹션
| 항목 | 상태 |
|------|------|
| Automatic | true |
| SystemProductName | (미설정 - Generic 사용) |

### UEFI 섹션
| Quirks | 상태 |
|--------|------|
| RequestBootVarRouting | true |
| AudioSupport | true |
| ConnectDrivers | true |

---

## 필요한 항목

### SSDT (ACPI/Add/)
- [ ] SSDT-EC.aml
- [ ] SSDT-PLUG.aml
- [ ] SSDT-PNLF.aml
- [ ] SSDT-USBX.aml
- [ ] SSDT-HPET.aml (선택)
- [ ] SSDT-XOSI.aml

### UEFI Drivers (Drivers/)
- [ ] OpenRuntime.efi (필수)
- [ ] OpenHfsPlus.efi (권장)
- [ ] OpenCanopy.efi (선택)

### Kexts (Kexts/)
- [ ] Lilu.kext
- [ ] VirtualSMC.kext
- [ ] WhateverGreen.kext
- [ ] AppleALC.kext
- [ ] AirportBrcmFixup.kext
- [ ] BlueToolFixup.kext
- [ ] VoodooI2C.kext
- [ ] VoodooI2CHID.kext
- [ ] VoodooPS2Controller.kext
- [ ] NVMeFix.kext
- [ ] SMCBatteryManager.kext
- [ ] ECEnabler.kext
- [ ] BrightnessKeys.kext (선택)

### 부트 파일
- [ ] OpenCore.efi
- [ ] BOOTX64.EFI (또는 BOOTx64.efi)

---

## 변경 이력

| 날짜 | 변경사항 | 비고 |
|------|----------|------|
| 2024-04-01 | 초기 EFI 구조 생성 | config.plist基础的 템플릿 작성 |
