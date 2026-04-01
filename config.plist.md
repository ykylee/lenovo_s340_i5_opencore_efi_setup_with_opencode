# OpenCore config.plist 상세 분석 문서

## 개요

이 문서는 OpenCore 설정 파일인 `config.plist`의 각 섹션을 상세하게 분석한 것입니다. Lenovo IdeaPad S340 (i5-8265U) 노트북에 macOS Ventura를 설치하기 위한 설정 가이드로 활용됩니다.

---

## 1. ACPI (Advanced Configuration and Power Interface)

ACPI 섹션은 시스템의 전원 관리 및 하드웨어 구성 설정을 담당합니다. 이 섹션은 특히 노트북에서 매우 중요합니다.

### 1.1 Add (ACPI 테이블 추가)

추가할 ACPI 테이블(SSDT) 목록입니다. 각 SSDT는 특정 하드웨어 기능을 활성화하거나 수정합니다.

| SSDT | 설명 | 하드웨어 의존성 | macOS 버전 |
|------|------|----------------|------------|
| SSDT-EC.aml | Embedded Controller 수정 | 필수 (노트북) | 모든 버전 |
| SSDT-HPET.aml | 고정밀 이벤트 타이머 수정 | 권장 | 모든 버전 |
| SSDT-PLUG.aml | CPU 전원 관리 플러그인 | 필수 (Intel) | 10.14+ |
| SSDT-PNLF.aml | 패널 백라이트 제어 | 필수 (노트북) | 모든 버전 |
| SSDT-USBX.aml | USB 전원 관리 | 권장 | 모든 버전 |
| SSDT-XOSI.aml | _OSI → XOSI 이름 변경 | 권장 | 모든 버전 |

#### SSDT-EC.aml
- **용도**: 내장 컨트롤러(EC) 수정
- **필요성**: 노트북 배터리 관리, 백라이트 제어에 필수
- **의존성**: ECEnabler.kext와 함께 사용 권장

#### SSDT-PLUG.aml
- **용도**: CPU 전원 관리 플러그인 활성화
- **하드웨어**: Intel CPU (i5-8265U = Whiskey Lake)
- **macOS**: 10.14 (Mojave) 이상에서 CPU 전원 관리 정상 작동

#### SSDT-PNLF.aml
- **용도**: 패널 밝기 제어 활성화
- **하드웨어**: 내장 디스플레이가 있는 노트북
- **주의**: 이 SSDT가 없으면 디스플레이 밝기 조절 불가

#### SSDT-USBX.aml
- **용도**: USB 컨트롤러 전원 관리 활성화
- **필요**: USBleeproper 작동을 위해 필요

#### SSDT-XOSI.aml
- **용도**: Windows 호환성을 위한 _OSI 메서드 라우팅
- **설정과 함께 사용**: `_OSI to XOSI` 패치 활성화 필요

### 1.2 Delete (ACPI 테이블 삭제)

삭제할 ACPI 테이블입니다. 기본적으로 비활성화되어 있으며, 특정 상황에서만 사용합니다.

| 항목 | 설명 | 사용 상황 |
|------|------|----------|
| CpuPm | CPU power management 테이블 삭제 | CPU 전원 관리 문제가 있을 때 |
| Cpu0Ist | CPU idle states 테이블 삭제 | 절전 모드 문제가 있을 때 |

**주의**: 기본적으로 비활성화되어 있습니다. 문제를 파악한 후 신중하게 사용해야 합니다.

### 1.3 Patch (ACPI 패치)

ACPI 테이블의 메서드를 런타임에 패치합니다.

#### 현재 활성화된 패치

##### _OSI to XOSI
```
Find: X09TSQ== (Base64: _OSI)
Replace: WE9TSQ== (Base64: XOSI)
```
- **용도**: _OSI 메서드를 XOSI로 이름 변경
- **이유**: macOS에서 Windows로 인식되어 특정 드라이버가 로드되도록 함
- **필요 SSDT**: SSDT-XOSI.aml

#### 비활성화된 패치

##### HPET _CRS to XCRS
```
Base: \_SB.PCI0.LPCB.HPET
Find: X0NSUw== (Base64: _CRS)
Replace: WENSUw== (Base64: XCRS)
```
- **용도**: HPET 리소스 기술자를 수정하여 커널 패닉 방지
- **대부분의 시스템에서 비활성화됨**: OpenCore가 자동으로 처리

### 1.4 Quirks (ACPI Quirks)

ACPI 처리 관련 특수 설정입니다.

| Quirks | 기본값 | 설명 | 권장 |
|--------|--------|------|------|
| FadtEnableReset | false | FACD에서 리셋 버튼 활성화 | 노트북에서 일반적으로 false |
| NormalizeHeaders | false | ACPI 헤더 정규화 | false |
| RebaseRegions | false | ACPI 영역 재배치 | false |
| ResetHwSig | false | 하드웨어 시그니처 리셋 | false |
| ResetLogoStatus | true | 로고 상태 리셋 | true (노트북) |
| SyncTableIds | false | 테이블 ID 동기화 | false |

#### ResetLogoStatus
- **설명**: 부트 로고 상태를 리셋
- **권장**: 노트북에서 true로 설정
- **이유**: 수면에서 절전 해제 후 화면 문제 예방

---

## 2. Booter

부트로더 관련 설정입니다. macOS 부팅 과정에서 메모리 매핑과 커널 로딩을 처리합니다.

### 2.1 MmioWhitelist

메모리 매핑 예외 목록입니다. 비어있는 경우 OpenCore가 자동으로 처리합니다.

### 2.2 Patch

부트로더 패치 목록입니다. 일반적으로 비어있습니다.

### 2.3 Quirks

| Quirks | 기본값 | 설명 | 권장 |
|--------|--------|------|------|
| AllowRelocationBlock | false | 재배치 블록 허용 | false |
| AvoidRuntimeDefrag | true | 런타임 조각모음 방지 | **true** |
| DevirtualiseMmio | false | MMIO 가상화 | false |
| DisableSingleUser | false | 단일 사용자 모드 비활성화 | false |
| DisableVariableWrite | false | 변수 쓰기 비활성화 | false |
| DiscardHibernateMap | false | hibernation 맵 폐기 | false |
| EnableSafeModeSlide | true | 세이프 모드 슬라이드 허용 | **true** |
| EnableWriteUnprotector | false | 쓰기 보호 해제 | false |
| FixupAppleEfiImages | false | Apple EFI 이미지 수정 | false |
| ForceBooterSignature | false | 부트로더 서명 강제 | false |
| ForceExitBootServices | false | 부트 서비스 강제 종료 | false |
| ProtectMemoryRegions | false | 메모리 영역 보호 | false |
| ProtectSecureBoot | false | 시큐어 부트 보호 | false |
| ProtectUefiServices | false | UEFI 서비스 보호 | false |
| ProvideCustomSlide | true | 커스텀 슬라이드 제공 | **true** |
| ProvideMaxSlide | 0 | 최대 슬라이드 값 | 0 |
| RebuildAppleMemoryMap | true | Apple 메모리 맵 재구성 | **true** |
| ResizeAppleGpuBars | -1 | GPU BAR 크기 조정 | -1 |
| SetupVirtualMap | false | 가상 맵 설정 | false |
| SignalAppleOS | false | Apple OS 시그널 | false |
| SyncRuntimePermissions | true | 런타임 권한 동기화 | **true** |

#### AvoidRuntimeDefrag
- **용도**:_runtime 중 메모리 조각모음 방지
- **권장**: **true** - macOS에서 필수
- **Intel 8세대 이상**: 항상 true로 설정

#### EnableSafeModeSlide
- **용도**: 세이프 모드에서 메모리 슬라이드 사용 허용
- **권장**: **true**
- **이유**: 부팅 문제 시 세이프 모드에서도 정상 작동하도록 함

#### RebuildAppleMemoryMap
- **용도**: macOS의 메모리 맵 재구성
- **권장**: **true**
- **Intel 8세대 (Whiskey Lake)**: 필수

#### ProvideCustomSlide
- **용도**: 커스텀 slide 값 제공
- **권장**: **true**
- **이유**: 메모리 충돌 방지

#### SyncRuntimePermissions
- **용도**:/runtime 권한 동기화
- **권장**: **true**
- **macOS 11+**: 필수

---

## 3. DeviceProperties

PCI 장치에 속성을 주입하는 섹션입니다. 이 섹션은 하드웨어에 따라 매우 중요합니다.

### 3.1 Add (장치 속성 주입)

| 경로 | 속성 | 설명 | 예시값 |
|------|------|------|--------|
| PciRoot(0x0)/Pci(0x2,0x0) | AAPL,ig-platform-id | 내장 그래픽 ID | 0x3ea00000 |
| PciRoot(0x0)/Pci(0x1f,0x3) | layout-id | 오디오 코덱 ID | 11 |
| PciRoot(0x0)/Pci(0x14,0x3) | built-in | 내장 장치 표시 | &lt;01000000&gt; |

#### 내장 그래픽 (Intel UHD Graphics 620)
- **PCI 경로**: `PciRoot(0x0)/Pci(0x2,0x0)`
- **AAPL,ig-platform-id**: `0x3ea00000` (또는 호환 ID)
- **hw_translated**: `0x3e9b0000` (일부 시스템에서 필요)

#### 오디오 (Realtek ALC)
- **PCI 경로**: `PciRoot(0x0)/Pci(0x1f,0x3)`
- **layout-id**: 테스트 필요 (일반적으로 11, 21, 28 중 하나)
- **주입 예시**:
  ```xml
  <key>PciRoot(0x0)/Pci(0x1f,0x3)</key>
  <dict>
    <key>layout-id</key>
    <integer>11</integer>
  </dict>
  ```

#### WiFi/Bluetooth (Broadcom)
- **PCI 경로**: WiFi 및 Bluetooth 장치 경로
- **built-in**: `&lt;01000000&gt;` (true)
- **주입 예시**:
  ```xml
  <key>PciRoot(0x0)/Pci(0x14,0x3)</key>
  <dict>
    <key>built-in</key>
    <data>AQAAAA==</data>
  </dict>
  ```

### 3.2 Delete (주입된 속성 삭제)

특정 속성을 제거합니다. 일반적으로 비어있습니다.

---

## 4. Kernel

커널 확장(kext) 관리 섹션입니다. macOS의 핵심 드라이버를 로드합니다.

### 4.1 Add (Kext 추가)

추가된 kext 목록입니다. 순서가 매우 중요합니다.

#### Kext 순서 (필수)

1. **Lilu.kext** - 필수 (모든 패치 kext의 기반)
2. **VirtualSMC.kext** - SMC 에뮬레이션
3. **WhateverGreen.kext** - 그래픽 패치
4. **AppleALC.kext** - 오디오
5. **AirportBrcmFixup.kext** - Broadcom WiFi
6. **BlueToolFixup.kext** - 블루투스
7. **VoodooI2C.kext** - I2C 터치패드
8. **VoodooPS2Controller.kext** - PS/2 키보드/마우스
9. **NVMeFix.kext** - NVMe SSD 최적화
10. **SMCBatteryManager.kext** - 배터리 관리
11. **ECEnabler.kext** - EC 활성화

#### 각 kext 설정 필드

| 필드 | 설명 | 예시 |
|------|------|------|
| Arch | 아키텍처 | `Any` (권장) |
| BundlePath | 번들 경로 | `Lilu.kext` |
| Comment | 설명 | `Lilu.kext` |
| Enabled | 활성화 여부 | `true` |
| ExecutablePath | 실행 파일 경로 | `Contents/MacOS/Lilu` |
| MaxKernel | 최대 커널 버전 | `` (무제한) |
| MinKernel | 최소 커널 버전 | `` (무제한) |
| PlistPath | Info.plist 경로 | `Contents/Info.plist` |

### 4.2 Block (차단할 kext)

차단할 kext 목록입니다. 기본적으로 비어있습니다.

### 4.3 Emulate (에뮬레이션)

CPU 에뮬레이션 설정입니다.

### 4.4 Force (강제 로드)

강제로 로드할 kext 목록입니다.

### 4.5 Patch (커널 패치)

커널 패치 목록입니다.

### 4.6 Quirks (커널 Quirks)

| Quirks | 기본값 | 설명 | 권장 |
|--------|--------|------|------|
| AppleCpuPmCfgLock | false | CPU Power Management 잠금 해제 | **true** (Intel 8세대) |
| AppleXcpmCfgLock | false | XCPM 잠금 해제 | **true** (Intel 8세대) |
| PanicNoKextDump | false | kext 덤프 없이 패닉 | **true** |
| PowerTimeoutKernelPanic | false | 전원 타임아웃 패닉 수정 | **true** |
| ProvideCurrentCpuInfo | false | 현재 CPU 정보 제공 | **true** |
| SetApfsTrimTimeout | false | APFS 트림 타임아웃 설정 | false |
| XhciPortLimit | false | USB 포트 수 제한 패치 | **true** (macOS 11.3 이하) |

#### AppleCpuPmCfgLock
- **용도**: MSR 0xE2 (CPU power management) 쓰기 잠금 해제
- **Intel 8세대 (Whiskey Lake)**: 필수 - BIOS에서 CFG Lock 비활성화가 불가능할 경우
- **CFG Lock 비활성화**: BIOS에서 가능하다면 BIOS에서 처리하는 것이 좋음

#### AppleXcpmCfgLock
- **용도**: XCPM (XNU CPU Power Management) 잠금 해제
- **Intel 8세대**: 필수

#### PanicNoKextDump
- **용도**: kext 덤프 없이 커널 패닉 발생
- **권장**: **true** - 로그 분석 용이

#### PowerTimeoutKernelPanic
- **용도**: 전원 상태 변경 타임아웃으로 인한 패닉 수정
- **권장**: **true** - macOS 10.15+

#### ProvideCurrentCpuInfo
- **용도**: 현재 CPU 정보 제공
- **권장**: **true** - 전원 관리 정상 작동에 필요

#### XhciPortLimit
- **용도**: USB 포트 수 15개 제한 우회
- **macOS 11.3 이하**: 필요
- **macOS 11.4+**: Apple이 수정하여 일반적으로 필요 없음

### 4.7 Scheme

커널 로딩 방식 설정입니다.

| 설정 | 설명 | 기본값 |
|------|------|--------|
| KernelCache | 커널 캐시 유형 | `Auto` |
| KernelArch | 커널 아키텍처 | `Auto` |
| KernelSpace | 커널 공간 | `Auto` |

---

## 5. Misc

다양한 부팅 및 보안 설정입니다.

### 5.1 Boot (부팅 설정)

| 설정 | 기본값 | 설명 | 권장 |
|------|--------|------|------|
| HideAuxiliary | false | 보조 파티션 숨기기 | false |
| HideSelf | false | EFI 파티션 숨기기 | false |
| PollAppleHotKeys | false | Apple 단축키 폴링 | false |
| ShowPicker | true | 부트 피커 표시 | **true** |
| PickerMode | `External` | 피커 모드 | `External` |
| PickerAttributes | 0 | 피커 속성 | 0 |
| TakeoffDelay | 0 | 테이크오프 지연 | 0 |
| Timeout | 5 | 타임아웃 (초) | 5 |

#### PickerMode
- **External**: OpenCanopy 사용
- **Builtin**: 기본 피커 사용
- **Apple**: macOS 피커 사용 (권장하지 않음)

### 5.2 Debug (디버그 설정)

| 설정 | 기본값 | 설명 |
|------|--------|------|
| AppleDebug | false | Apple 디버그 로깅 |
| ApplePanic | false | 패닉 로깅 |
| DisableWatchDog | true | 와치독 비활성화 |
| Target | 0 | 디버그 대상 |
| DisplayDelay | 0 | 디버그 지연 |

#### DisableWatchDog
- **권장**: **true** - 부팅 타임아웃으로 인한 문제 예방

### 5.3 Entries (부팅 항목)

사용자 정의 부팅 항목 목록입니다.

### 5.4 Security (보안 설정)

| 설정 | 기본값 | 설명 | 권장 |
|------|--------|------|------|
| AllowSetDefault | true | 기본 부트 항목 설정 허용 | **true** |
| ApECID | 0 | Apple ECID | 0 |
| AuthRestart | false | 인증 재시작 | false |
| BlacklistAppleUpdate | true | Apple 업데이트 차단 | **true** |
| ExposeSecureYAML | true | YAML 표시 | **true** |
| HaltEnabled | false | 정지 모드 | false |
| ScanPolicy | 0 | 스캔 정책 | 0 |
| SecureBootModel | `Default` | 시큐어 부트 모델 | `Default` |
| Vault | `Optional` | 볼트 모드 | `Optional` |

#### Vault
- **Optional**: 서명 검증 비활성화
- **Basic**: 기본 검증
- **Strict**: 완전한 검증 (권장하지 않음)

### 5.5 Tools (도구)

부팅 시 사용할 수 있는 UEFI 도구 목록입니다.

---

## 6. NVRAM

비휘발성 메모리 설정입니다.

### 6.1 Add (추가할 NVRAM 변수)

| 변수 | 값 | 설명 |
|------|-----|------|
| boot-args | `-v keepsyms=1 alcid=11` | 부트 인자 |
| csr-active-config | `00000000` | SIP 상태 |
| prev-lang:kbd | `` | 이전 언어 |
| SystemAudioVolume | `Rg==` | 시스템 볼륨 |
| UIScale | `AQ==` | UI 배율 |

#### boot-args 상세

| 인자 | 설명 |
|------|------|
| `-v` |Verbose 모드 (부팅 과정 표시) |
| `keepsyms=1` | 패닉 시 심볼 유지 |
| `alcid=11` | 오디오 레이아웃 ID |
| `-noDC9` | IceLake 그래픽 문제 해결 |
| `-nodisplaysleepDC6` | 디스플레이 수면 문제 해결 |
| `-cdfwp` | AppleTISocket 활성화 |

#### csr-active-config
- `00000000`: SIP 완전 활성화
- `030E0000`: SIP 부분 비활성화 (권장)
- `FFFFFFFF`: SIP 완전 비활성화

### 6.2 Delete (삭제할 NVRAM 변수)

삭제할 변수 목록입니다.

### 6.3 LegacySchema

레거시 NVRAM 스키마입니다.

### 6.4 WriteFlash
- **값**: `true` - NVRAM 쓰기 허용
- **권장**: **true** (대부분의 노트북)

---

## 7. PlatformInfo

SMBIOS 정보 설정입니다.

### 7.1 Automatic

| 값 | 설명 |
|-----|------|
| `true` | 자동 SMBIOS 생성 |
| `false` | 수동 설정 |

### 7.2 Generic (자동 생성 시)

| 항목 | 설명 | 권장값 |
|------|------|--------|
| MLB | 보드 시리얼 번호 | 자동 생성 |
| ROM | MAC 주소 | 자동 생성 |
| SystemProductName | 시스템 제품명 | `MacBookPro15,4` |
| SystemSerialNumber | 시리얼 번호 | 자동 생성 |
| UpdateSMBIOSMode | SMBIOS 업데이트 모드 | `Create` |

#### 권장 SMBIOS

| CPU 세대 | 권장 SMBIOS |
|----------|-------------|
| Intel 8세대 (Whiskey Lake) | `MacBookPro15,4` |
| Intel 10세대 (IceLake) | `MacBookPro16,2` |
| Intel 11세대 (Tiger Lake) | `MacBookPro18,3` |

### 7.3 DataHub, PlatformNVRAM, SMBIOS

고급 사용자를 위한 상세 설정입니다.

---

## 8. UEFI

UEFI firmware 설정입니다.

### 8.1 APFS

| 설정 | 기본값 | 설명 |
|------|--------|------|
| EnableJumpstart | true | APFS 점프스타트 활성화 |
| HideVerbose | true | Verbose 숨기기 |
| MinDate | `` | 최소 날짜 |
| MinVersion | `` | 최소 버전 |

### 8.2 AppleInput

| 설정 | 기본값 | 설명 |
|------|--------|------|
| KeyInitialDelay | 50 | 키 초기 지연 (ms) |
| KeySubsequentDelay | 5 | 키 후속 지연 (ms) |
| PointerSpeedDim | 0 | 포인터 속도 |

### 8.3 Audio

| 설정 | 기본값 | 설명 |
|------|--------|------|
| AudioSupport | true | 오디오 지원 |
| ConnectDrivers | true | 드라이버 연결 |

### 8.4 Drivers

활성화된 UEFI 드라이버 목록입니다.

### 8.5 Input

입력 장치 설정입니다.

### 8.6 Output

출력 설정입니다.

### 8.7 ProtocolOverrides

프로토콜 오버라이드 설정입니다.

### 8.8 Quirks

| Quirks | 기본값 | 설명 | 권장 |
|--------|--------|------|------|
| RequestBootVarRouting | true | 부트 변수 라우팅 요청 | **true** |

### 8.9 ReservedMemory

예약 메모리 영역입니다.

---

## OpenCore 버전별 호환성

| OpenCore 버전 | 권장 macOS | 주요 변경사항 |
|---------------|------------|---------------|
| 0.6.x | 10.15 - 11.x | 초기 안정 버전 |
| 0.7.x | 10.15 - 12.x | Apple Silicon 지원 추가 |
| 0.8.x | 11 - 13 | 향상된 보안 |
| 0.9.x | 12 - 14 | 최신 macOS 지원 |
| 1.0.x | 13 - 15 | 안정적인 최신 버전 |

### Lenovo IdeaPad S340 (i5-8265U) 권장 버전
- **OpenCore**: 0.9.x 이상
- **macOS**: Ventura (13.x) - Sonoma (14.x)

---

## 문제 해결 참조

### 부팅 문제
1. `-v`로 Verbose 모드 활성화
2. AppleCpuPmCfgLock 및 AppleXcpmCfgLock 활성화
3. RebuildAppleMemoryMap 활성화

### 그래픽 문제
1. WhateverGreen kext 로드 확인
2. AAPL,ig-platform-id 조정
3. AggressiveTextureCompression 확인

### 오디오 문제
1. layout-id 변경 (테스트 필요)
2. AppleALC kext 로드 확인
3. alcid boot-arg 조정

### USB 문제
1. XhciPortLimit 활성화 (11.3 이하)
2. USB 포트 매핑 확인
3. SSDT-USBX.aml 로드 확인

### 배터리 문제
1. SMCBatteryManager kext 로드
2. ECEnabler kext 로드
3. SSDT-EC.aml 로드 확인

### 수면/절전 문제
1. HibernationFixup kext
2. DarkWake 설정 조정
3. ResetLogoStatus 활성화
