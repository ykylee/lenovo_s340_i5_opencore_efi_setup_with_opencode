# EFI 현재 상태

## 개요

이 문서는 Lenovo IdeaPad S340 (i5-8265U) OpenCore EFI의 현재 상태를 기록합니다.

---

## 버전 정보

### OpenCore
| 항목 | 버전 | 비고 |
|------|------|------|
| **OpenCore.efi** | 0.6.4 | Big Sur时期 (2020) |
| **BOOTx64.efi** | 0.6.4 | 동일 |

### 지원 macOS
| 버전 | 상태 | 비고 |
|------|------|------|
| macOS 10.15 (Catalina) | ✅ 지원 | |
| macOS 11.x (Big Sur) | ✅ 지원 | 기준 샘플 |
| macOS 12.x (Monterey) | ⚠️ 제한적 | kext 버전 업그레이드 필요 |
| macOS 13.x (Ventura) | ❌ 미지원 | OpenCore 0.9.x 필요 |

---

## 디렉터리 구조

```
EFI/
├── BOOT/
│   └── BOOTx64.efi          ✅ 복사됨 (샘플 기반)
└── OC/
    ├── ACPI/                 ✅ 13개 SSDT
    ├── Bootstrap/            ✅ 복사됨
    ├── Drivers/              ✅ 3개 드라이버
    ├── Kexts/                ✅ 15개 kext
    ├── Resources/            ✅ 부트 피커 리소스
    ├── Tools/                ✅ UEFI 도구
    ├── OpenCore.efi          ✅ 복사됨
    └── config.plist          ✅ 샘플 기반 (수정 필요)
```

---

## ACPI (13개 SSDT)

| 파일 | 용도 | 버전 |
|------|------|------|
| SSDT-AWAC.aml | AWAC 시간 유지 | - |
| SSDT-EC.aml | 내장 컨트롤러 | - |
| SSDT-GPI0.aml | GPIO 컨트롤러 | - |
| SSDT-GPRW.aml | 런웨이크 방지 | - |
| SSDT-HPET.aml | 타이머 수정 | - |
| SSDT-I2C0-SPED.aml | I2C 속도 | - |
| SSDT-PLUG.aml | CPU 전원 관리 | - |
| SSDT-PMC.aml | PMC 수정 | - |
| SSDT-PNLFCFL.aml | 백라이트 제어 (CFL) | - |
| SSDT-PSF13.aml | PSF 수정 | - |
| SSDT-USBX.aml | USB 전원 관리 | - |
| SSDT-XOSI.aml | _OSI → XOSI | - |
| ssdt-rmne.aml | 장치 이름 변경 | - |

---

## UEFI Drivers (3개)

| 파일 | 용도 | 버전 |
|------|------|------|
| OpenCanopy.efi | 그래픽 부트 피커 | - |
| OpenHfsPlus.efi | HFS+ 파일시스템 | - |
| OpenRuntime.efi | 런타임 드라이버 (필수) | - |

---

## Kexts (15개)

| Kext | 버전 | 용도 |
|------|------|------|
| Lilu.kext | 1.5.3 | 패치 엔진 (필수) |
| VirtualSMC.kext | 1.2.3 | SMC 에뮬레이션 (필수) |
| WhateverGreen.kext | 1.4.9 | 그래픽 패치 (필수) |
| AppleALC.kext | 1.6.0 | 오디오 |
| AirportBrcmFixup.kext | 2.1.2 | Broadcom WiFi |
| VoodooI2C.kext | 2.6.5 | I2C 터치패드 |
| VoodooI2CHID.kext | 1.0 | I2C HID |
| VoodooPS2Controller.kext | 2.2.3 | PS/2 키보드/마우스 |
| NVMeFix.kext | 1.0.7 | NVMe 최적화 |
| SMCBatteryManager.kext | 1.2.3 | 배터리 관리 |
| SMCProcessor.kext | 1.2.3 | CPU 센서 |
| BrightnessKeys.kext | - | 밝기 키 |
| NullEthernet.kext | 1.0.6 | 더미 이더넷 |
| Sinetek-rtsx.kext | 2.3 | 카드 리더기 |
| USBPorts.kext | 1.0 | USB 포트 매핑 |

---

## Tools (12개)

| 도구 | 용도 |
|------|------|
| BootKicker.efi | 부트 키커 |
| ChipTune.efi | 칩튜닝 |
| CleanNvram.efi | NVRAM 정리 |
| ControlMsrE2.efi | MSR E2 제어 |
| CsrUtil.efi | SIP 유틸리티 |
| GopStop.efi | GOP 중지 |
| KeyTester.efi | 키 테스트 |
| MmapDump.efi | 메모리 맵 덤프 |
| OpenControl.efi | OpenCore 제어 |
| OpenShell.efi | UEFI 셸 |
| ResetSystem.efi | 시스템 리셋 |
| RtcRw.efi | RTC 읽기/쓰기 |

---

## config.plist 현재 설정 상태

### ACPI 섹션 (샘플 기반 - 수정 필요)
| 항목 | 상태 |
|------|------|
| SSDT-EC.aml | 추가됨 |
| SSDT-HPET.aml | 추가됨 |
| SSDT-PLUG.aml | 추가됨 |
| SSDT-PNLFCFL.aml | 추가됨 |
| SSDT-USBX.aml | 추가됨 |
| SSDT-XOSI.aml | 추가됨 |
| _OSI to XOSI 패치 | 활성화됨 |

### Kernel 섹션 (✅ 설정 완료)
| 항목 | 상태 |
|------|------|
| Lilu.kext | 추가됨 |
| VirtualSMC.kext | 추가됨 |
| WhateverGreen.kext | 추가됨 |
| AppleALC.kext | 추가됨 |
| AirportBrcmFixup.kext | 추가됨 |
| AppleCpuPmCfgLock | ✅ 활성화됨 |
| AppleXcpmCfgLock | ✅ 활성화됨 |
| XhciPortLimit | ✅ 활성화됨 |
| ProvideCurrentCpuInfo | ✅ 활성화됨 |

### DeviceProperties 섹션 (✅ 설정 완료)
| 항목 | 상태 |
|------|------|
| 오디오 layout-id | 11 (ALC257 샘플) |
| 그래픽 model | Intel UHD Graphics 620 수정 |
| WiFi built-in | ✅ Broadcom BCM4352 추가 |

### NVRAM 섹션 (✅ 설정 완료)
| 항목 | 설정값 |
|------|--------|
| boot-args | alcid=11 vsmcgen=1 debug=0x100 darkwake=0 dart=0 keepsyms=1 -v |
| csr-active-config | 0x030E0000 (부분 활성화) |

### PlatformInfo 섹션 (⚠️ 사용자 생성 필요)
| 항목 | 상태 |
|------|------|
| SMBIOS | MacBookPro15,4 (샘플) - GenSMBIOS로 재生成 권장 |

---

## 변경 이력

| 날짜 | 변경사항 | 비고 |
|------|----------|------|
| 2024-04-01 | 초기 EFI 구조 생성 | config.plist 기본 템플릿 작성 |
| 2024-04-01 | 샘플 EFI 기반 복사 | Lenovo-s340-s540-Big-Sur-OpenCore-i5-8265u 기준 |
| | - OpenCore.efi, BOOTx64.efi 복사 (v0.6.4) |
| | - SSDT 13개 복사 |
| | - UEFI 드라이버 3개 복사 |
| | - kext 15개 복사 (버전 기록: Lilu 1.5.3, VirtualSMC 1.2.3 등) |
| | - Tools 12개 복사 |
| | - Resources 복사 |
| | - config.plist 샘플 기반 적용 |
| | - EFI_STATUS.md 버전 정보 추가 |
| 2024-04-01 | config.plist 설정 완료 | |
| | - Kernel Quirks 활성화 (AppleCpuPmCfgLock, AppleXcpmCfgLock, XhciPortLimit, ProvideCurrentCpuInfo) |
| | - DeviceProperties 수정 (WiFi built-in, 그래픽 model) |
| | - NVRAM 설정 확인 완료 |
| | - EFI_STATUS.md 버전 정보 추가 |
