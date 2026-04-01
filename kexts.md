# Kernel Extensions (Kexts) 상세 문서

## 개요

이 문서는 Hackintosh에서 사용되는 커널 확장(Kext)의 상세 정보를 정리한 것입니다. 각 kext의 기능, 의존성, 호환성, 설정 방법을 포함합니다.

---

## 필수 Kexts (Intel 8세대 노트북)

### 1. Lilu.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.lilu` |
| **버전** | 1.7.x (최신) |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/Lilu |
| **설명** | macOS 패치를 위한 기반 kext. 다른 kext의 패치 기능을 지원합니다. |

#### 기능
- 다수의 kext와 애플리케이션에 대한 런타임 패치
- 심볼릭 링크 및 프로세스 후킹
- OtherOS 및 비 Apple 하드웨어 지원

#### 의존성
- **없음** - 다른 kext의 기반이 되는 kext

#### 필수 여부
- **필수** - 상당수의 kext가 Lilu에 의존

#### 설정
- MinKernel: `10.13.0` ( Sierra)
- MaxKernel: 제한 없음

#### 호환성
- macOS 10.13 (High Sierra) - macOS 14 (Sonoma)

---

### 2. VirtualSMC.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.virtualsmc` |
| **버전** | 1.3.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/VirtualSMC |
| **설명** | SMC (System Management Controller) 에뮬레이터 |

#### 기능
- 가상의 SMC 장치 생성
- HWMonitor 및 다른 모니터링 도구 지원
- 배터리, 온도, 팬 속도 등 SMC 센서 데이터 제공

#### 의존성
- **Lilu.kext**

#### 필수 여부
- **필수** - 대다수 Hackintosh에 필요

#### 포함 kext
- `SMCProcessor.kext` - CPU 센서
- `SMCSuperIO.kext` - Super I/O 센서
- `SMCBatteryManager.kext` - 배터리 관리

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 3. WhateverGreen.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.whatevergreen` |
| **버전** | 1.6.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/WhateverGreen |
| **설명** | 그래픽 패치 kext - 내장/외장 그래픽 모두 지원 |

#### 기능
- Intel 내장 그래픽 패치
- AMD 외장 그래픽 패치
- 프레임버퍼 패치
- 커널 패닉 방지 패치
- 디스플레이 출력 문제 해결

#### 의존성
- **Lilu.kext**

#### Intel UHD Graphics 620 (i5-8265U) 설정
- **Platform ID**: `0x3ea00000` (또는 `0x3e9b0000`)
- **VRAM**: 2048MB (2GB) 이상 권장

#### 주요 boot-args
```
- disablegfxoam=1      # AMD GPU 비활성화 (외장 GPU 없으면 불필요)
- agdpmod=vit9696     # AppleGraphicsDevicePolicy 패치
- -noDC9              # IceLake 그래픽 문제 해결
- -nodisplaysleepDC6  # 디스플레이 수면 문제 해결
```

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 4. AppleALC.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.applealc` |
| **버전** | 1.9.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/AppleALC |
| **설명** | 비 Apple 오디오 코덱 패치 kext |

#### 기능
- Realtek, Conexant, Cirrus 등의 오디오 코덱 활성화
- 내장 스피커, 마이크, 헤드폰 잭 지원
- 레이아웃 ID를 통한 다양한 구성 지원

#### 의존성
- **Lilu.kext**

#### Lenovo IdeaPad S340 권장 설정
- **layout-id**: 테스트 필요
  - **11**: 가장 일반적인 값
  - **21**: 일부 Lenovo 노트북
  - **28**: 다른 변형
- **boot-arg**: `alcid=11`

#### 설치 방법
1. AppleALC kext 추가
2. boot-args에 `alcid=XX` 추가
3. DeviceProperties에 layout-id 주입

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

## 네트워크 Kexts

### 5. AirportBrcmFixup.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.airportbrcmfixup` |
| **버전** | 2.1.x |
| **개발자** | lvs1974 |
| **저장소** | https://github.com/acidanthera/AirportBrcmFixup |
| **설명** | Broadcom WiFi 카드 패치 kext |

#### 기능
- Broadcom WiFi 카드 지원
- AirPort 기능 활성화
- 국가 코드 설정 지원

#### 의존성
- **Lilu.kext**

#### 호환 카드
- BCM4352 (사용자 카드) ✅
- BCM4360
- BCM4322
- BCM4313

#### 설치 시 주의사항
- `brcmfx-country=XX` boot-arg로 국가 코드 설정 가능
- 기본값: `US`

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 6. BlueToolFixup.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.bluetoolfixup` |
| **버전** | 2.6.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/BlueToolFixup |
| **설명** | 블루투스 패치 kext |

#### 기능
- Broadcom/InteBluetooth 펌웨어 로드
- 블루투스 동작 문제 해결
- BluetoothAutoSwitch kext 대체

#### 의존성
- **Lilu.kext**

#### 호환 블루투스
- Broadcom BCM20702A1 (사용자 블루투스) ✅
- Broadcom BCM20703A1
- Intel Bluetooth

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 7. BCM20702A1 관련 Kexts ( Broadcom 블루투스)

#### BrcmFirmwareData.kext
- **설명**: Broadcom 펌웨어 데이터
- **의존성**: Lilu

#### BrcmPatchRAM3.kext
- **설명**: Broadcom 블루투스 패치
- **의존성**: Lilu, BrcmFirmwareData

---

## 입력 장치 Kexts

### 8. VoodooI2C.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.alexandred.VoodooI2C` |
| **버전** | 2.9.x |
| **개발자** | CoolStar |
| **저장소** | https://github.com/VoodooI2C/VoodooI2C |
| **설명** | I2C 터치패드 드라이버 |

#### 기능
- I2C 터치패드 지원
- 멀티터치 제스처
- Windows Precision Touchpad 에뮬레이션

#### 의존성
- **Lilu.kext**
- **VoodooI2CHID.kext** (필수)

#### Elan Touchpad (사용자 노트북)
- **PCI ID**: `04f3:304b`
- **인터페이스**: I2C
- **I2C 주소**: `MSFT0001:02`

#### 포함 플러그인
- **VoodooI2CHID.kext** - HID 호환성
- **VoodooGPIO.kext** - GPIO 컨트롤러
- **VoodooI2CServices.kext** - I2C 서비스
- **VoodooInput.kext** - 입력 처리

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 9. VoodooPS2Controller.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.voodoo.driver.PS2Controller` |
| **버전** | 1.9.x |
| **개발자** | CoolStar |
| **저장소** | https://github.com/VoodooPS2/VoodooPS2Controller |
| **설명** | PS/2 키보드, 마우스, 트랙패드 드라이버 |

#### 기능
- PS/2 키보드 지원
- PS/2 마우스 지원
- 내장 키보드 백라이트 지원
- Fn 키 지원

#### 의존성
- **없음** (standalone)

#### 포함 플러그인
- **VoodooPS2Keyboard.kext** - 키보드
- **VoodooPS2Mouse.kext** - 마우스
- **VoodooPS2Trackpad.kext** - 트랙패드
- **VoodooInput.kext** - 입력 처리

#### Lenovo 노트북 설정
- `KeyboardLayout` - PS2Map
- `FanSpeedZeroOk` - 팬 속도 0 허용

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

## 저장소 및 전원 Kexts

### 10. NVMeFix.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.nvmefix` |
| **버전** | 1.1.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/NVMeFix |
| **설명** | NVMe SSD 최적화 kext |

#### 기능
- APFS 트림 활성화
- NVMe 전원 관리 개선
- 대용량 NVMe 드라이브 지원

#### 의존성
- **Lilu.kext**

#### Lenovo IdeaPad S340 (SK Hynix BC501)
- **모델**: HFM256GDHTNG-8310A
- **권장**: NVMeFix 활성화

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 11. SMCBatteryManager.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.smcbattery` |
| **버전** | 1.3.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/VirtualSMC |
| **설명** | 배터리 관리 kext |

#### 기능
- 배터리 상태 표시
- 배터리 퍼센트 표시
- 배터리 시간 추정

#### 의존성
- **VirtualSMC.kext**
- **Lilu.kext**
- **ECEnabler.kext** (권장)

#### Lenovo IdeaPad S340 배터리
- **용량**: 36Wh 또는 45Wh
- **셀**: 3셀 또는 4셀

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 12. ECEnabler.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.githubchen.ecenabler` |
| **버전** | 1.0.x |
| **개발자** | chris1111 |
| **저장소** | https://github.com/chris1111/ECEnabler |
| **설명** | Embedded Controller 접근 활성화 |

#### 기능
- EC (Embedded Controller) 메서드 활성화
- 배터리 관리 지원
- 백라이트 제어 지원

#### 의존성
- **Lilu.kext**

#### 필수 여부
- **권장** - 배터리 및 백라이트 작동을 위해 필요

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 13. BrightnessKeys.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.githublvs1974.brightnesskeys` |
| **버전** | 1.0.x |
| **개발자** | lvs1974 |
| **저장소** | https://github.com/lvs1974/BrightnessKeys |
| **설명** | 밝기 키 활성화 kext |

#### 기능
- 화면 밝기 조절 키 활성화
- 키보드 밝기 조절 키 활성화

#### 의존성
- **Lilu.kext**

#### 설정
- MinKernel: `10.14.0`
- MaxKernel: 제한 없음

---

## 추가 유틸리티 Kexts

### 14. RestrictEvents.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.restrictEvents` |
| **버전** | 1.3.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/RestrictEvents |
| **설명** | 불필요한 이벤트 차단 |

#### 기능
- MacBookPro 식별 문제 해결
- 불필요한sysdep pdreq 차단
- iMessage, FaceTime 활성화 도움

#### 의존성
- **Lilu.kext**

#### 설정
- MinKernel: `10.15.0`
- MaxKernel: 제한 없음

---

### 15. HibernationFixup.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.githublvs1974.hibernationfixup` |
| **버전** | 1.4.x |
| **개발자** | lvs1974 |
| **저장소** | https://github.com/lvs1974/HibernationFixup |
| **설명** | 절전/겨울잠 문제 해결 |

#### 기능
- Hibernate (겨울잠) 문제 해결
- DarkWake 지원 개선
- nvram 변수 처리 개선

#### 의존성
- **Lilu.kext**

#### 설정
- MinKernel: `10.14.0`
- MaxKernel: 제한 없음

---

### 16. NullEthernet.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.githubrehabman.nullethernet` |
| **버전** | 1.0.x |
| **개발자** | RehabMan |
| **저장소** | https://github.com/RehabMan/OS-X-NullEthernet |
| **설명** | 더미 이더넷 kext |

#### 기능
- 가상의 이더넷 인터페이스 생성
- HW-MAC 주소 문제 해결
- iCloud/iMessage 활성화 도움

#### 의존성
- **없음**

#### 설정
- MinKernel: `10.10.0`
- MaxKernel: 제한 없음

---

### 17. NoTouchID.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.apple.kpi.notouchid` |
| **버전** | 1.0.x |
| **개발자** | acidanthera |
| **저장소** | https://github.com/acidanthera/NoTouchID |
| **설명** | TouchID 비활성화 (데스크탑용) |

#### 기능
- TouchID 기능 비활성화
- 데스크탑에서 필요 없는 기능 제거

#### 의존성
- **Lilu.kext**

#### 설정
- MinKernel: `10.13.0`
- MaxKernel: 제한 없음

---

### 18. DebugEnhancer.kext

| 항목 | 내용 |
|------|------|
| **번들 ID** | `com.githublvs1974.debugenhancer` |
| **버전** | 1.0.x |
| **개발자** | lvs1974 |
| **저장소** | https://github.com/lvs1974/DebugEnhancer |
| **설명** | 디버그 향상 kext |

#### 기능
- 커널 패닉 시 더 자세한 정보 제공
- 디버그 로깅 개선

#### 의존성
- **Lilu.kext**

#### 설정
- MinKernel: `10.14.0`
- MaxKernel: 제한 없음

---

## Lenovo IdeaPad S340 권장 Kext 구성

### 필수 (Required)
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
   ├── VoodooI2CHID.kext
   └── VoodooInput.kext
8. VoodooPS2Controller.kext
9. NVMeFix.kext
10. ECEnabler.kext
11. BrightnessKeys.kext
```

### 권장 (Recommended)
```
- RestrictEvents.kext
- HibernationFixup.kext
- DebugEnhancer.kext (디버깅 시)
```

### 선택 (Optional)
```
- NullEthernet.kext (iMessage 문제 시)
- NoTouchID.kext (데스크탑 빌드 시)
```

---

## Kext 설치 순서 (중요)

Kext는 특정 순서로 로드해야 합니다. 순서가 잘못되면 부팅이 실패할 수 있습니다.

```
[Lilu.kext]
    ├── [VirtualSMC.kext]
    │       ├── SMCProcessor.kext
    │       ├── SMCSuperIO.kext (필요시)
    │       └── SMCBatteryManager.kext
    ├── [WhateverGreen.kext]
    ├── [AppleALC.kext]
    ├── [AirportBrcmFixup.kext]
    ├── [BlueToolFixup.kext]
    ├── [VoodooI2C.kext]
    │       ├── VoodooI2CHID.kext
    │       ├── VoodooGPIO.kext
    │       ├── VoodooI2CServices.kext
    │       └── VoodooInput.kext
    ├── [VoodooPS2Controller.kext]
    │       ├── VoodooPS2Keyboard.kext
    │       ├── VoodooPS2Mouse.kext (필요시)
    │       ├── VoodooPS2Trackpad.kext (필요시)
    │       └── VoodooInput.kext
    ├── [NVMeFix.kext]
    ├── [ECEnabler.kext]
    ├── [BrightnessKeys.kext]
    ├── [RestrictEvents.kext]
    └── [HibernationFixup.kext]
```

---

## Kext 상태 확인 명령어

```bash
# kext 로드 상태 확인
kextstat | grep -E "(Lilu|VirtualSMC|WhateverGreen|AppleALC)"

# 특정 kext 정보
kextfind -b com.apple.kpi.lilu

# kext 의존성 확인
kextutil -n /Library/Extensions/Lilu.kext
```

---

## 문제 해결

### kext 로드 실패
1. kext 순서 확인
2. Lilu.kext가 가장 먼저 로드되는지 확인
3. kext 권한 확인: `sudo chmod -R 755 /Library/Extensions/XXX.kext`
4. kext 서명 확인: `sudo codesign -dv /Library/Extensions/XXX.kext`

### 패닉 발생
1. `-v` boot-arg로 Verbose 모드 활성화
2. kext 로드 순서 확인
3. MinKernel/MaxKernel 설정 확인
4. kext 호환성 확인

### 특정 기능 미작동
1. kext가 로드되었는지 확인
2. boot-arg 누락 여부 확인
3. DeviceProperties 설정 확인
4. SSDT 필요 여부 확인
