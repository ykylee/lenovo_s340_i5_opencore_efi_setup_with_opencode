# Lenovo IdeaPad S340 OpenCore EFI

Lenovo IdeaPad S340-14IWL (Intel Core i5-8265U) 노트북에 macOS Ventura를 설치하기 위한 OpenCore EFI 설정 프로젝트입니다.

## 하드웨어 스펙

| 항목 | 사양 |
|------|------|
| CPU | Intel Core i5-8265U (Whiskey Lake, 8세대) |
| GPU | Intel UHD Graphics 620 (PCI ID: 8086:3ea0) |
| 메모리 | 8GB DDR4 (Samsung, 4GB x 2) |
| 저장소 | NVMe SSD 256GB (SK Hynix BC501) |
| WiFi | Broadcom BCM4352 802.11ac (사용자 교환) |
| 블루투스 | Broadcom BCM20702A1 |
| 오디오 | Intel Cannon Point-LP HD Audio |
| 카드 리더기 | Realtek RTS522A (PCI ID: 10ec:522a) |
| 터치패드 | Elan (04f3:304b, I2C) |

## 프로젝트 구조

```
opencore/
├── EFI/
│   └── OC/
│       ├── ACPI/          # SSDT 테이블
│       ├── Drivers/       # UEFI 드라이버
│       ├── Kexts/         # 커널 확장
│       ├── Tools/         # UEFI 도구
│       └── config.plist   # OpenCore 설정
├── specs.md               # 하드웨어 상세 스펙
├── config.pllist.md       # config.plist 분석 문서
├── kexts.md              # 커널 확장 상세 문서
├── drivers.md            # UEFI 드라이버 문서
├── setup.md              # 설치 및 튜닝 가이드
├── AGENTS.md             # 에이전트 코딩 지침
├── DOCUMENTATION_KR.md   # 한글 문서화
└── check_korean.py       # 한글 깨짐 검사 스크립트
```

## 생성된 문서

### 하드웨어 문서
- **specs.md**: 수집된 하드웨어 상세 스펙 (PCI ID, USB 디바이스, 입력 장치 등)

### OpenCore 문서
- **config.plist.md**: config.plist 각 섹션 상세 분석 (ACPI, Kernel, UEFI 등)
- **kexts.md**: 커널 확장(Kext) 상세 정보 및 의존성
- **drivers.md**: UEFI 드라이버 목록 및 용도
- **setup.md**: 설치 및 튜닝 가이드 (BIOS 설정, USB 매핑, NVRAM 등)

### 가이드 문서
- **AGENTS.md**: 에이전트를 위한 코딩 지침 및 스타일 가이드
- **DOCUMENTATION_KR.md**: 프로젝트 한글 문서화 요약

## 주요 SSDT

| SSDT | 용도 |
|------|------|
| SSDT-EC.aml | 내장 컨트롤러 수정 |
| SSDT-PLUG.aml | CPU 전원 관리 |
| SSDT-PNLF.aml | 패널 밝기 제어 |
| SSDT-USBX.aml | USB 전원 관리 |
| SSDT-XOSI.aml | Windows 호환성 |

## 권장 Kexts

1. **Lilu.kext** - 패치 엔진
2. **VirtualSMC.kext** - SMC 에뮬레이션
3. **WhateverGreen.kext** - 그래픽 패치
4. **AppleALC.kext** - 오디오
5. **AirportBrcmFixup.kext** - Broadcom WiFi
6. **BlueToolFixup.kext** - 블루투스
7. **VoodooI2C.kext** - I2C 터치패드
8. **VoodooPS2Controller.kext** - 키보드
9. **NVMeFix.kext** - NVMe 최적화
10. **SMCBatteryManager.kext** - 배터리 관리

## 참조 자료

- [Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- [Acidanthera Kexts](https://github.com/acidanthera)
- Lenovo IdeaPad S340 Hackintosh GitHub Samples

## 라이선스

이 프로젝트는 개인 학습 및 연구 목적으로 작성되었습니다. 상용 사용 시 각 kext 및 드라이버의 라이선스를 확인하세요.
