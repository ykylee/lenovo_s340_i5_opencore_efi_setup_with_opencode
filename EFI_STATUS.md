# EFI 현재 상태

## 개요

이 문서는 Lenovo IdeaPad S340 (i5-8265U) OpenCore EFI의 현재 상태를 기록합니다.

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

## 현재 파일 목록

### 부트 파일
- **BOOTx64.efi**: ✅ 존재 (샘플 복사)
- **OpenCore.efi**: ✅ 존재 (샘플 복사)

### ACPI (13개 SSDT)
```
SSDT-AWAC.aml      - AWAC 시간 유지
SSDT-EC.aml        - 내장 컨트롤러
SSDT-GPI0.aml      - GPIO 컨트롤러
SSDT-GPRW.aml      - 런웨이크 방지
SSDT-HPET.aml      - 타이머 수정
SSDT-I2C0-SPED.aml - I2C 속도
SSDT-PLUG.aml      - CPU 전원 관리
SSDT-PMC.aml       - PMC 수정
SSDT-PNLFCFL.aml   - 백라이트 제어 (CFL)
SSDT-PSF13.aml     - PSF 수정
SSDT-USBX.aml      - USB 전원 관리
SSDT-XOSI.aml      - _OSI → XOSI
ssdt-rmne.aml      - 장치 이름 변경
```

### UEFI Drivers (3개)
```
OpenCanopy.efi    - 그래픽 부트 피커
OpenHfsPlus.efi   - HFS+ 파일시스템
OpenRuntime.efi   - 런타임 드라이버 (필수)
```

### Kexts (15개)
```
AirportBrcmFixup.kext  - Broadcom WiFi
AppleALC.kext         - 오디오
BrightnessKeys.kext   - 밝기 키
Lilu.kext            - 패치 엔진 (필수)
NVMeFix.kext         - NVMe 최적화
NullEthernet.kext    - 더미 이더넷
SMCBatteryManager.kext - 배터리 관리
SMCProcessor.kext    - CPU 센서
Sinetek-rtsx.kext    - 카드 리더기
USBPorts.kext        - USB 포트 매핑
VirtualSMC.kext       - SMC 에뮬레이션 (필수)
VoodooI2C.kext       - I2C 터치패드
VoodooI2CHID.kext    - I2C HID
VoodooPS2Controller.kext - PS/2 키보드/마우스
WhateverGreen.kext   - 그래픽 패치 (필수)
```

### Tools
```
BootKicker.efi, ChipTune.efi, CleanNvram.efi, ControlMsrE2.efi, CsrUtil.efi, 
GopStop.efi, KeyTester.efi, MmapDump.efi, OpenControl.efi, OpenShell.efi, 
ResetSystem.efi, RtcRw.efi
```

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

### Kernel 섹션 (샘플 기반 - 수정 필요)
| 항목 | 상태 |
|------|------|
| Lilu.kext | 추가됨 |
| VirtualSMC.kext | 추가됨 |
| WhateverGreen.kext | 추가됨 |
| AppleALC.kext | 추가됨 |
| AirportBrcmFixup.kext | 추가됨 |
| AppleCpuPmCfgLock | 활성화 필요 |
| AppleXcpmCfgLock | 활성화 필요 |
| XhciPortLimit | 활성화 필요 |

### DeviceProperties 섹션
| 항목 | 상태 |
|------|------|
| 오디오 layout-id | 수정 필요 (Realtek ALC257 → 실제 코덱) |
| 그래픽 Platform ID | 수정 필요 |
| WiFi built-in | 수정 필요 |

### NVRAM 섹션
| 항목 | 설정값 |
|------|--------|
| boot-args | 수정 필요 (alcid 확인) |
| csr-active-config | 수정 필요 |

### PlatformInfo 섹션
| 항목 | 상태 |
|------|------|
| SMBIOS | 수정 필요 (사용자 시리얼 생성) |

---

## 변경 이력

| 날짜 | 변경사항 | 비고 |
|------|----------|------|
| 2024-04-01 | 초기 EFI 구조 생성 | config.plist 기본 템플릿 작성 |
| 2024-04-01 | 샘플 EFI 기반 복사 | Lenovo-s340-s540-Big-Sur-OpenCore-i5-8265u 기준 |
| | - OpenCore.efi, BOOTx64.efi 복사 |
| | - SSDT 13개 복사 |
| | - UEFI 드라이버 3개 복사 |
| | - kext 15개 복사 |
| | - Tools 12개 복사 |
| | - Resources 복사 |
| | - config.plist 샘플 기반 적용 |
