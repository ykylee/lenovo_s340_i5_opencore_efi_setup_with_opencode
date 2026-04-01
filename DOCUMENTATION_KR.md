# Lenovo IdeaPad S340 macOS Ventura EFI 설치 가이드

## 개요
이 문서는 Lenovo IdeaPad S340 노트북에 macOS Ventura를 설치하기 위한 EFI 구축 과정을 문서화한 것입니다. 
노트북 스펙: Intel Core i5-8265U CPU, Intel UHD Graphics 620, 8GB RAM

## 수행한 작업들

### 1. 하드웨어 스펙 분석
- CPU: Intel Core i5-8265U (Whiskey Lake, 8세대)
- GPU: Intel UHD Graphics 620
- 메모리: 8GB DDR4
- 저장소: NVMe SSD
- WiFi: Intel 무선 카드 (사용자 언급에 따라 Broadcom으로 교체됨)
- 오디오: Conexant 또는 Realtek ALC 시리즈
- 카드 리더기: Realtek RTS522A 또는 유사

### 2. EFI 샘플 수집 및 분석
GitHub에서 다음과 같은 EFI 샘플을 수집하여 분석했습니다:

#### 수집된 샘플들:
1. **ideapad-s340-14api-hackintosh** - AMD Ryzen 5 3500U 기반 (참고용)
2. **Lenovo-Ideapad-S340-15api-Hackintosh** - AMD 기반 (참고용)
3. **Lenovo-IdeaPad-S340-15IIL** - Intel IceLake 기반 (참고용)
4. **Lenovo-s340-s540-Big-Sur-OpenCore-i5-8265u** - i5-8265u 기반 (목표 CPU와 유사)

### 3. 주요 발견사항
각 샘플에서 추출한 주요 설정들:

#### ACPI 패턴:
- SSDT-EC.aml: Embedded Controller 수정
- SSDT-PLUG.aml: CPU 전원 관리
- SSDT-PNLF.aml: 백라이트 제어
- SSDT-USBX.aml: USB 포트 매핑
- SSDT-XOSI.aml: _OSI를 XOS이로 이름 변경 (Windows 호환성 유지)
- SSDT-HPET.aml: 고정밀 이벤트 타이머 수정
- SSDT-RMNE.aml: _Rename 방법으로 장치 이름 변경
- SSDT-GPRW.aml: 일반 목적 런웨이크 수정

#### 핵심 Kexts:
- Lilu.kext: 패치 엔진
- VirtualSMC.kext: SMC 에뮬레이터
- WhateverGreen.kext: 그래픽 패치
- AppleALC.kext: 오디오 솔루션
- AirportBrcmFixup.kext: Broadcom WiFi 지원 (사용자 사양에 맞춤)
- BlueToolFixup.kext: Bluetooth 지원
- VoodooI2C.kext 및 관련 플러그인: 트랙패드 지원
- VoodooPS2Controller.keyst: PS/2 키보드 및 마우스 지원
- NVMeFix.kext: NVMe SSD 최적화
- RestrictEvents.kext: 불필요한 이벤트 방지
- SMCBatteryManager.kext: 배터리 관리
- ECEnabler.kext: Embedded Controller 활성화
- BrightnessKeys.keyst: 밝기 키 지원
- HibernationFixup.keyst: 겨울잠 문제 수정
- NoTouchID.keyst: TouchID 비활성화 (데스크탑용)

#### Kernel 패턴:
- CPU 전원 관리 패치 (AppleCpuPmCfgLock, AppleXcpmCfgLock)
- PanicNoKextDump: 커널 패닉 시 kext 덤프 비활성화
- PowerTimeoutKernelPanic: 전원 타임아웃 패닉 수정
- ProvideCurrentCpuInfo: 현재 CPU 정보 제공
- SetApfsTrimTimeout: APFS trim 타임아웃 설정
- XhciPortLimit: USB 포트 제한 패치

#### DeviceProperties:
- 오디오 컨트롤러에 layout-id 주입 (AppleALC용)
- 그래픽 장치에 AAPL,ig-platform-id 주입 (WhateverGreen용)
- 네트워크 장치에 built-in 속성 주입 (Broadcom WiFi/Bluetooth용)

#### NVRAM 설정:
- boot-args: "-v keepsyms=1 alcid=11" (안전 모드 및 오디오 설정)
- csr-active-config: "00000000" (SIP 비활성화)
- prev-lang:kbd: "" (언어 설정)
- SystemAudioVolume: "Rg==" (볼륨 설정)
- UIScale: "AQ==" (UI 스케일)

### 4. EFI 구조 생성
표준 OpenCore 디렉터리 구조를 생성했습니다:
- EFI/
  - OC/
    - ACPI/ (ACPI 테이블 저장)
    - Drivers/ (UEFI 드라이버)
    - Kexts/ (커널 확장)
    - Tools/ (UEFI 도구)
    - config.plist (주요 설정 파일)
    - OpenCore.efi (부팅 로더)

### 5. config.plist 구성
수집한 샘플들을 분석하여 다음과 같이 config.plist를 구성했습니다:

#### ACPI 섹션:
- 필수 SSDT 추가 (EC, HPET, PLUG, PNLF, USBX, XOSI)
- 일반적인 패치 적용 (HPET _CRS to XCRS, _OSI to XOSI 등)
- Quirks 설정 (FadtEnableReset, NormalizeHeaders 등)

#### Booter 섹션:
- MmioWhitelist 비워둠 (필요시 추가)
- 필수 Quirks 활성화 (AvoidRuntimeDefrag, EnableSafeModeSlide 등)

#### Kernel 섹션:
- 필수 Kexts 추가 (Lilu, VirtualSMC, WhateverGreen, AppleALC 등)
- Arch: Any로 설정하여 모든 아키텍처 지원
- Enabled: true로 설정하여 기본 활성화
- Quirks 설정 (AppleCpuPmCfgLock, AppleXcpmCfgLock, PanicNoKextDump 등)

#### DeviceProperties 섹션:
- 현재 빈 딕셔너리로 유지 (추후 하드웨어 검사 후 주입 예정)
- 오디오, 그래픽, 네트워크 장치에 주입 계획

#### Misc 섹션:
- Boot 설정 (HideAuxiliary, ShowPicker, PickerMode=External 등)
- Debug 설정 (AppleDebug=false, ApplePanic=false, DisableWatchDog=true 등)
- Security 설정 (AllowSetDefault=true, BlacklistAppleUpdate=true 등)
- Serial 설정 (Console 용)

#### NVRAM 섹션:
- Add에 필수 설정 포함 (boot-args, csr-active-config 등)
- Delete에 사용되지 않을 설정 포함
- LegacySchema에 필요한 변수 목록 포함
- WriteFlash: true로 설정하여 NVRAM 쓰기 허용

#### PlatformInfo 섹션:
- Automatic: true로 설정하여 자동 SMBIOS 생성
- Generic에 MLB, ROM, SystemProductName 등 설정 계획
- UpdateSMBIOSMode: Create로 설정하여 새로운 SMBIOS 생성

#### UEFI 섹션:
- APFS 설정 (EnableJumpstart=true, HideVerbose=true 등)
- AppleInput 설정 (KeyInitialDelay=50, KeySubsequentDelay=5 등)
- Audio 설정 (AudioSupport=true 등)
- ConnectDrivers: true로 설정하여 UEFI 드라이버 연결
- Input/Output 설정 구성
- ProtocolOverrides 모두 false로 설정 (필요시 활성화)
- Quirks 설정 (RequestBootVarRouting=true 등)
- ReservedMemory 비워둠

### 6. 향후 계획
1. 실제 하드웨어에서 시스템 정보 수집
2. 정확한 DeviceProperties 주입을 위해 PCI 장치 스캔
3. 적절한 SMBIOS 정보 생성 (MacBookPro15,4 또는 유사 모델 사용)
4. WiFi 및 Bluetooth 기능 테스트 (Broadcom 카드 기준)
5. 오디오 기능 테스트 및 layout-id 최적화
6. 전원 관리 및 배터리 기능 테스트
7. 수면 및 겨울잠 기능 테스트
8. VM 환경에서 기본 부팅 테스트 (가능한 경우)
9. 실제 하드웨어에서 테스트 및 피드백 반영

## 주의사항
- 이 EFI는 초기 구축 단계이며, 실제 하드웨어에서 테스트가 필요합니다.
- WiFi 및 Bluetooth는 사용자 언급에 따라 Broadcom 카드로 교체된 것을 기준으로 구성했습니다.
- 각 단계별로 변경 사항을 커밋하여 이력을 관리해야 합니다.
- 설정 변경 후에는 반드시 설정을 검증하고 백업을 유지해야 합니다.

## 참조 자료
- Dortania의 OpenCore Install Guide
- 수집한 GitHub 샘플들
- ACPI 사양 및 패칭 가이드
- macOS 커널 확장 개발 문서