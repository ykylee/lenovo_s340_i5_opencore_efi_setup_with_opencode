# OpenCore EFI 설치 및 튜닝 가이드

## 개요

이 문서는 Lenovo IdeaPad S340 (i5-8265U) 노트북에 OpenCore EFI를 설치하고 튜닝하는 상세한 가이드입니다. 하드웨어 스펙, kexts, 드라이버, 설정 등을 종합적으로 다룹니다.

---

## 1. 시작하기 전 준비사항

### 1.1 필수 도구

| 도구 | 용도 | 비고 |
|------|------|------|
| ProperTree | config.plist 편집 | https://github.com/corpnewt/ProperTree |
| MaciASL | ACPI 테이블 편집/컴파일 | https://github.com/acidanthera/MaciASL |
| GenSMBIOS | SMBIOS 생성 | https://github.com/corpnewt/GenSMBIOS |
| MountEFI | EFI 파티션 마운트 | https://github.com/corpnewt/MountEFI |
| ocvalidate | 설정 검증 | OpenCore 빌드에 포함 |

### 1.2BIOS 설정

Lenovo IdeaPad S340 BIOS에서 다음 설정을 확인/변경합니다:

| 설정 | 권장값 | 설명 |
|------|--------|------|
| Secure Boot | Disabled | 시큐어 부트 비활성화 |
| CSM Support | Disabled | 레거시 부트 비활성화 |
| UEFI Only | Enabled | UEFI만 사용 |
| CFG Lock | Disabled | CPU 전원 관리 잠금 해제 (가능하면) |
| DVMT Pre-Allocated | 64MB or 128MB | 내장 그래픽 메모리 |
| Primary Boot Priority | UEFI | UEFI 부트 우선 |

#### CFG Lock 비활성화 방법
1. BIOS 메뉴 접근 (F2 또는 Fn+F2)
2. Advanced → CPU-Power Management Control
3. CFG Lock → Disabled

만약 BIOS에서 CFG Lock을 비활성화할 수 없다면:
- config.plist에서 `AppleCpuPmCfgLock`과 `AppleXcpmCfgLock`을 `true`로 설정

### 1.3 EFI 파티션 준비

```bash
# Linux에서
sudo mkdir /mnt/efi
sudo mount /dev/nvme0n1p1 /mnt/efi

# macOS에서
sudo mount -t msdos /dev/disk0s1 /Volumes/EFI

# Windows에서
diskpart
list partition
select partition 1
assign letter=Z
```

---

## 2. EFI 디렉터리 구조

OpenCore EFI 구조는 다음과 같이 구성됩니다:

```
EFI/
├── BOOT/
│   └── BOOTX64.EFI          # 부트 로더
└── OC/
    ├── ACPI/
    │   ├── Add/             # 추가할 SSDT
    │   ├── Patch/           # ACPI 패치
    │   └── Delete/          # 삭제할 ACPI 테이블
    ├── Drivers/             # UEFI 드라이버
    ├── Kexts/               # 커널 확장
    ├── Tools/               # UEFI 도구
    ├── Resources/           # 부트 피커 리소스
    ├── OpenCore.efi         # 부트 로더
    ├── config.plist         # 설정 파일
    └── vault.plist          # 볼트 파일 (선택)
```

---

## 3. ACPI 테이블 (SSDT)

### 3.1 필요한 SSDT 목록

Lenovo IdeaPad S340 (i5-8265U)에 필요한 SSDT:

| SSDT | 용도 | 필수/선택 |
|------|------|----------|
| SSDT-EC.aml | 내장 컨트롤러 | **필수** |
| SSDT-PLUG.aml | CPU 전원 관리 | **필수** |
| SSDT-PNLF.aml | 패널 밝기 | **필수** |
| SSDT-USBX.aml | USB 전원 | 권장 |
| SSDT-HPET.aml | 타이머 수정 | 권장 |
| SSDT-XOSI.aml | _OSI 변경 | 권장 |

### 3.2 SSDT 소스 코드

#### SSDT-EC.aml
```asl
DefinitionBlock ("", "DSDT", 2, "LENOVO", "S340    ", 0x00000000)
{
    Scope (\_SB)
    {
        Device (EC)
        {
            Name (_HID, "PNP0C09")
            Name (_UID, 1)
            Method (_STA, 0, NotSerialized)
            {
                If (LEqual (\_SB.PCI0.LPC.ECOK, One))
                {
                    Return (0x0F)
                }
                Else
                {
                    Return (Zero)
                }
            }
            // EC 점유율 영역 (노트북 모델에 따라 다를 수 있음)
        }
    }
}
```

#### SSDT-PLUG.aml
```asl
DefinitionBlock ("", "DSDT", 2, "LENOVO", "S340    ", 0x00000000)
{
    Scope (\_SB)
    {
        Device (CPU0)
        {
            Name (_HID, "ACPI0004")
            Method (_STA, 0, NotSerialized)
            {
                Return (0x0F)
            }
        }
    }
}
```

#### SSDT-PNLF.aml
```asl
DefinitionBlock ("", "DSDT", 2, "LENOVO", "S340    ", 0x00000000)
{
    Scope (\_SB.PCI0)
    {
        Device (PNLF)
        {
            Name (_ADR, Zero)
            Name (_HID, "PNP0C06")
            Name (_UID, 2)
            Method (_STA, 0, NotSerialized)
            {
                Return (0x0B)
            }
        }
    }
}
```

### 3.3 SSDT 컴파일

```bash
# MaciASL 사용 (macOS/Linux)
# File > Compile

# iasl 사용 (명령줄)
iasl -tc SSDT-EC.aml

# 출력 확인
ls -la *.aml
```

---

## 4. USB 매핑

### 4.1 현재 USB 상태 (Linux 기준)

```
Bus 001 (USB 2.0/3.0)
├── Device 002: IMC Networks 웹캠 (13d3:56b2)
├── Device 003: Broadcom 블루투스 (0489:e07a)  
└── Device 004: Logitech Receiver (046d:c548)

Bus 002 (USB 3.1)
└── 빈 포트
```

### 4.2 macOS용 USB 포트 매핑

| 포트 유형 | macOS 이름 | 용도 |
|-----------|-----------|------|
| USB 2.0 | HS01 - HS14 | 저속/전속 장치 |
| USB 3.0 | SS01 - SS08 | 고속 장치 |

#### USB 포트 할당 (IdeaPad S340 14형)

| 물리 포트 | 컨트롤러 | 유형 | macOS 이름 |
|----------|----------|------|------------|
| USB-A (좌측) | xHCI | USB 2.0/3.0 | HS01 |
| USB-A (우측) | xHCI | USB 2.0/3.0 | HS02 |
| USB-C (좌측) | xHCI | USB 3.1 | SS01 |

### 4.3 USBPorts.kext 사용

Hackintool이나 USBMap을 사용하여 커스텀 USB 포트 kext 생성:

```bash
# USBPorts.kext 구조
USBPorts.kext/
├── Contents/
│   ├── Info.plist
│   └── MacOS/
│       └── USBPorts
```

#### Info.plist 예시
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>USBPorts</string>
    <key>CFBundleIdentifier</key>
    <string>com.headsoft.usbports</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>USBPorts</string>
    <key>CFBundlePackageType</key>
    <string>KEXT</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>IOKitPersonalities</key>
    <dict>
        <key>USBPorts</key>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>com.headsoft.usbports</string>
            <key>CFBundleName</key>
            <string>USBPorts</string>
            <key>IOClass</key>
            <string>IOUSBHostDevice</string>
            <key>IOMatchCategory</key>
            <string>IOUSBHostDevice</string>
            <key>IOProviderClass</key>
            <string>IOUSBHostDevice</string>
            <key>IOUserClientClass</key>
            <string>IOUSBHostDeviceUserClient</string>
            <key>IOUserServerClass</key>
            <string>IOUSBHostDeviceUserServer</string>
        </dict>
    </dict>
    <key>OSBundleRequired</key>
    <string>Local-Root</string>
</dict>
</plist>
```

### 4.4 USB 제한 패치

macOS 11.3 이하에서 USB 포트 수 제한 우회:

```xml
<key>Kernel</key>
<dict>
    <key>Quirks</key>
    <dict>
        <key>XhciPortLimit</key>
        <true/>
    </dict>
</dict>
```

---

## 5. PlatformInfo (SMBIOS) 설정

### 5.1 권장 SMBIOS

Intel Core i5-8265U (Whiskey Lake 8세대)에 맞는 SMBIOS:

| SMBIOS | CPU 세대 | 비고 |
|--------|----------|------|
| MacBookPro15,4 | 8세대 | **권장** |
| MacBookPro15,2 | 8세대 | 대안 |

### 5.2 GenSMBIOS 사용

```bash
# GenSMBIOS 실행
python3 GenSMBIOS.py

# 선택:
# 3) Generate SMBIOS
# MacBookPro15,4 선택
# 시리얼 번호 생성
```

### 5.3 PlatformInfo 설정

```xml
<key>PlatformInfo</key>
<dict>
    <key>Automatic</key>
    <true/>
    <key>Generic</key>
    <dict>
        <key>MLB</key>
<string>[생성된 Board Serial]</string>
<key>SystemSerialNumber</key>
<key>ROM</key>
<string>[생성된 MAC 주소]</string>
<key>SystemSerialNumber</key>
<string>[생성된 Serial]</string>
        <key>UpdateSMBIOSMode</key>
        <string>Create</string>
    </dict>
</dict>
```

---

## 6. NVRAM 설정

### 6.1 필수 boot-args

| boot-arg | 설명 | 필수/선택 |
|----------|------|----------|
| `-v` | Verbose 모드 | 초기 설정 시 필수 |
| `keepsyms=1` | 패닉 시 심볼 유지 | 권장 |
| `alcid=11` | 오디오 레이아웃 ID | **필수** (오디오용) |
| `-noDC9` | IceLake 그래픽 패치 | 선택 |
| `-nodisplaysleepDC6` | 디스플레이 절전 패치 | 선택 |

### 6.2 NVRAM 설정 예시

```xml
<key>NVRAM</key>
<dict>
    <key>Add</key>
    <dict>
        <key>boot-args</key>
        <string>-v keepsyms=1 alcid=11</string>
        <key>csr-active-config</key>
        <string>030E0000</string>
        <key>prev-lang:kbd</key>
        <string>ko-KR</string>
    </dict>
    <key>WriteFlash</key>
    <true/>
</dict>
```

### 6.3 SIP (System Integrity Protection)

| 값 | 상태 |
|----|------|
| `00000000` | SIP 완전 활성화 |
| `030E0000` | SIP 부분 활성화 (권장) |
| `FFFFFFFF` | SIP 완전 비활성화 |

권장값 `030E0000`으로 설정하여 다음 기능 활성화:
- NVRAM 쓰기
- 커널 패치
- 일부 kext 로드

---

## 7. 부트 인자 (Boot Arguments) 상세

### 7.1 디버그 인자

| 인자 | 설명 |
|------|------|
| `-v` | Verbose 모드 (부팅 과정 표시) |
| `-x` | 안전 모드 (Safe Boot) |
| `-s` | 단일 사용자 모드 |
| `-f` | kext 캐시 무시 |

### 7.2 그래픽 인자

| 인자 | 설명 |
|------|------|
| `-noDC9` | IceLake 디스플레이 패치 |
| `-nodisplaysleepDC6` | 디스플레이 수면 패치 |
| `-disablegfxoam` | 내장 그래픽 비활성화 |
| `agdpmod=vit9696` | graphics policy 패치 |

### 7.3 오디오 인자

| 인자 | 설명 |
|------|------|
| `alcid=XX` | 오디오 레이아웃 ID (예: 11) |

### 7.4 USB 인자

| 인자 | 설명 |
|------|------|
| `usbfix=1` | USB 전원 관리 패치 |
| `-xhciportlimit` | USB 포트 제한 우회 |

### 7.5 네트워크 인자

| 인자 | 설명 |
|------|------|
| `brcmfx-country=XX` | Broadcom 국가 코드 |
| `fmtx-mac=XX:XX:XX:XX:XX:XX` | MAC 주소 지정 |

### 7.6 CPU 인자

| 인자 | 설명 |
|------|------|
| `-xcpm` | XCPM 전원 관리 사용 |
| `cpus=XX` | CPU 코어 수 제한 |

---

## 8. 문제 해결

### 8.1 부팅 시 검은 화면

**증상**: 부트 피커는 보이지만 macOS 부팅 시 검은 화면

**해결 방법**:
1. `-v` boot-arg로Verbose 모드 활성화
2. WhateverGreen kext 로드 확인
3. AAPL,ig-platform-id 조정:
   - `0x3ea00000` → `0x3e9b0000` 시도
4. AggressiveTextureCompression 비활성화

### 8.2 커널 패닉

**증상**: 커널 패닉 발생

**해결 방법**:
1. `keepsyms=1` boot-arg로 패닉 시 심볼 유지
2. PanicNoKextDump 활성화
3. kext 로드 순서 확인
4. AppleCpuPmCfgLock 활성화 (CFG Lock BIOS 비활성화 불가 시)

### 8.3 오디오 미작동

**증상**: 소리가 나지 않음

**해결 방법**:
1. AppleALC kext 로드 확인
2. layout-id 변경 (11 → 21 → 28)
3. boot-arg에 `alcid=11` 추가
4. Speaker 또는 Headphone 선택 확인

### 8.4 WiFi/Bluetooth 미작동

**증상**: 네트워크 또는 블루투스 불가

**해결 방법**:
1. AirportBrcmFixup kext 로드 확인
2. BlueToolFixup kext 로드 확인
3. `brcmfx-country=US` boot-arg 추가
4. built-in 속성 주입 확인

### 8.5 배터리 미표시

**증상**: 배터리 상태가 표시되지 않음

**해결 방법**:
1. SMCBatteryManager kext 로드 확인
2. ECEnabler kext 로드 확인
3. SSDT-EC.aml 로드 확인
4. EC 접근 권한 확인

### 8.6 터치패드 미작동

**증상**: 터치패드가 응답하지 않음

**해결 방법**:
1. VoodooI2C kext 로드 확인
2. VoodooI2CHID kext 로드 확인
3. I2C 주소 확인 (MSFT0001:02)
4. VoodooInput kext 포함 확인

### 8.7 USB 미작동

**증상**: USB 포트가 작동하지 않음

**해결 방법**:
1. XhciPortLimit 활성화 (macOS 11.3 이하)
2. USBPorts.kext 사용
3. SSDT-USBX.aml 로드 확인
4. USB 포트 매핑 확인

---

## 9. 부팅 체크리스트

### 부팅 전 확인 사항

- [ ] BIOS 설정 완료 (CFG Lock, Secure Boot 등)
- [ ] EFI 파티션 마운트됨
- [ ] OpenCore 파일 구조 올바름
- [ ] config.plist 유효성 검증
- [ ] 모든 kext가 OC/Kexts/에 있음
- [ ] 모든 SSDT가 OC/ACPI/Add/에 있음
- [ ] UEFI 드라이버가 Drivers/에 있음

### 첫 부팅 시

- [ ] `-v` boot-arg로Verbose 모드로 부팅
- [ ] kext 로드 순서 확인
- [ ] 오류 메시지 기록
- [ ] 문제 발생 시 캡처

###macOS 설치 후

- [ ] kext 로드 상태 확인
- [ ] SMBIOS 정보 확인
- [ ] 오디오 테스트
- [ ] WiFi/Bluetooth 테스트
- [ ] 터치패드 테스트
- [ ] USB 테스트
- [ ] 배터리 표시 확인
- [ ] 절전/절전 해제 테스트

---

## 10. 참조 자료

### 공식 문서
- [Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- [Acidanthera Kexts](https://github.com/acidanthera)
- [OpenCore Documentation](https://github.com/acidanthera/OpenCorePkg/docs/)

### 도구
- [ProperTree](https://github.com/corpnewt/ProperTree)
- [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS)
- [MaciASL](https://github.com/acidanthera/MaciASL)
- [Hackintool](https://github.com/benbaker/Hackintool)

### 커뮤니티
- [InsanelyMac Forum](https://www.insanelymac.com/forum/)
- [Reddit r/hackintosh](https://www.reddit.com/r/hackintosh/)

---

## 부록 A: 빠른 참조표

### Lenovo IdeaPad S340 핵심 설정

| 항목 | 설정값 |
|------|--------|
| SMBIOS | MacBookPro15,4 |
| CPU | i5-8265U |
| 내장 그래픽 | UHD Graphics 620 |
| Platform ID | 0x3ea00000 |
| 오디오 | layout-id: 11 |
| WiFi | Broadcom BCM4352 |
| Bluetooth | Broadcom BCM20702A1 |

### kext 로드 순서

```
1. Lilu.kext
2. VirtualSMC.kext
   ├── SMCProcessor.kext
   └── SMCBatteryManager.kext
3. WhateverGreen.kext
4. AppleALC.kext
5. AirportBrcmFixup.kext
6. BlueToolFixup.kext
7. VoodooI2C.kext
   └── VoodooI2CHID.kext
8. VoodooPS2Controller.kext
9. NVMeFix.kext
10. ECEnabler.kext
11. BrightnessKeys.kext
```

### 필수 boot-args

```
-v keepsyms=1 alcid=11
```
