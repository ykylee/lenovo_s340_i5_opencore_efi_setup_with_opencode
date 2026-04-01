# OpenCore UEFI Drivers 상세 문서

## 개요

이 문서는 OpenCore에서 사용되는 UEFI 드라이버의 상세 정보를 정리한 것입니다. 각 드라이버의 기능, 용도, 필수 여부 등을 포함합니다.

---

## UEFI 드라이버 기본 정보

### 드라이버 설치 위치
```
EFI/
└── OC/
    └── Drivers/
        └── [드라이버들]
```

### 드라이버 로드 순서
OpenCore는 config.plist의 UEFI > Drivers 섹션에 나열된 순서대로 드라이버를 로드합니다.

---

## 필수 UEFI 드라이버

### 1. OpenRuntime.efi

| 항목 | 내용 |
|------|------|
| **설명** | OpenCore 핵심 런타임 드라이버 |
| **기능** | 부트 서비스, Runtime Services 프로토콜 제공 |
| **필수 여부** | **필수** |
| **OpenCore 버전** | 0.5.9+ |

#### 기능 상세
- Boot Services 프로토콜 로깅
- Runtime Services 프로토콜 활성화
- OpenCore의 핵심 기능 지원
- 메모리 할당 및 관리

#### 의존성
- 없음 (OpenCore의 기반)

#### 권장 설정
- config.plist의 UEFI > Drivers에 첫 번째로 추가

---

### 2. OpenHfsPlus.efi

| 항목 | 내용 |
|------|------|
| **설명** | HFS+ 파일시스템 드라이버 |
| **기능** | HFS+ 볼륨 읽기/쓰기 지원 |
| **필수 여부** | **권장** (macOS Recovery용) |
| **대체품** | HfsPlus.efi (레거시) |

#### 기능 상세
- HFS+ 볼륨 마운트
- macOS Recovery 파티션 지원
- Time Machine 백업 드라이브 지원

#### 권장 사용 시나리오
- macOS Recovery에서 부팅할 때
- HFS+ 형식의 백업 드라이브가 있을 때

---

### 3. HfsPlus.efi

| 항목 | 내용 |
|------|------|
| **설명** | 레거시 HFS+ 드라이버 |
| **기능** | HFS+ 볼륨 읽기 전용 지원 |
| **필수 여부** | **선택** |
| **권장 상황** | OpenHfsPlus.efi가 동작하지 않을 때 |

#### 기능 상세
- 레거시 HFS+ 지원
- 제한된 쓰기 기능

#### 권장 설정
- OpenHfsPlus.efi를 먼저 시도
- 문제가 있을 때 HfsPlus.efi로 대체

---

## 부팅 인터페이스 드라이버

### 4. OpenCanopy.efi

| 항목 | 내용 |
|------|------|
| **설명** | OpenCore 그래픽 부트 피커 |
| **기능** | GUI 기반 부트 선택 화면 |
| **필수 여부** | **선택** (UI 선호 시) |
| **대체품** |Builtin 피커 |

#### 기능 상세
- 그래픽 부트 피커
- 커스텀 테마 지원
- 아이콘 및 이미지 표시
- 마우스/키보드 입력 지원

#### 설정 (config.plist)
```xml
<key>Misc</key>
<dict>
    <key>Boot</key>
    <dict>
        <key>PickerMode</key>
        <string>External</string>
    </dict>
</dict>
```

#### 커스텀 테마
- 위치: `EFI/OC/Resources/`
- 구조:
  ```
  Resources/
  ├── Image/
  │   └── [테마명]/
  ├── Label/
  │   └── [테마명]/
  └── Audio/
      └── [테마명]/
  ```

#### 권장 설정
- Misc > Boot > PickerMode: `External`
- Misc > Boot > PickerAttributes: `0`

---

### 5. OpenLinuxBoot.efi

| 항목 | 내용 |
|------|------|
| **설명** | Linux 부트 드라이버 |
| **기능** | Linux 커널 직접 부팅 |
| **필수 여부** | **선택** (다중 부팅 시) |

#### 기능 상세
- Linux 커널 부팅
- GRUB 대체 가능
- EFI stub 커널 지원

#### 설정 예시
```xml
<key>Misc</key>
<dict>
    <key>Entries</key>
    <array>
        <dict>
            <key>Name</key>
            <string>Ubuntu</string>
            <key>Path</key>
            <string>\EFI\ubuntu\shimx64.efi</string>
        </dict>
    </array>
</dict>
```

---

## 파일시스템 드라이버

### 6. ext4_x64.efi

| 항목 | 내용 |
|------|------|
| **설명** | ext4 파일시스템 드라이버 |
| **기능** | Linux ext4 파티션 읽기/쓰기 |
| **필수 여부** | **선택** (Linux 다중 부팅 시) |

#### 기능 상세
- ext4 볼륨 마운트
- Linux 저장소 접근

---

### 7. NTFS.efi

| 항목 | 내용 |
|------|------|
| **설명** | NTFS 파일시스템 드라이버 |
| **기능** | Windows NTFS 파티션 읽기/쓰기 |
| **필수 여부** | **선택** (Windows 다중 부팅 시) |

#### 기능 상세
- NTFS 읽기/쓰기 (제한적)
- Windows 파티션 접근

---

### 8. ExFatDxe.efi

| 항목 | 내용 |
|------|------|
| **설명** | exFAT 파일시스템 드라이버 |
| **기능** | exFAT 파티션 지원 |
| **필수 여부** | **선택** |

#### 기능 상세
- exFAT 볼륨 마운트
- 대용량 파일 지원

---

## 하드웨어 드라이버

### 9. Rts5227S.efi (또는 유사 카드 리더기 드라이버)

| 항목 | 내용 |
|------|------|
| **설명** | Realtek 카드 리더기 드라이버 |
| **기능** | Realtek RTS522A 카드 리더기 지원 |
| **필수 여부** | **선택** |
| **하드웨어** | Realtek RTS522A (PCI ID: 10ec:522a) |

#### Lenovo IdeaPad S340 카드 리더기
- **모델**: Realtek RTS522A
- **PCI ID**: 10ec:522a
- **지원 카드**: SD, SDHC, SDXC, MMC

#### 기능 상세
- SD 카드 읽기/쓰기
- UHS-I 지원

#### 대안 kext
- RealtekCardReader.kext (커널 레벨)
- RealtekCardReaderFriend.kext

---

### 10. AudioDxe.efi

| 항목 | 내용 |
|------|------|
| **설명** | UEFI 오디오 드라이버 |
| **기능** | 부팅 시 오디오 피드백 |
| **필수 여부** | **선택** |

#### 기능 상세
- 부트 피커 오디오 피드백
- 시스템 시작 효과음

#### 설정 (config.plist)
```xml
<key>UEFI</key>
<dict>
    <key>Audio</key>
    <dict>
        <key>AudioSupport</key>
        <true/>
    </dict>
</dict>
```

---

## 유틸리티 드라이버

### 11. ResetNvramEntry.efi

| 항목 | 내용 |
|------|------|
| **설명** | NVRAM 리셋 도구 |
| **기능** | NVRAM 변수 초기화 |
| **필수 여부** | **선택** |
| **유형** | 도구 (Tool) |

#### 기능 상세
- NVRAM 변수 삭제
- 부팅 문제 해결 시 유용
- 부트 피커에서 접근 가능

#### 사용 방법
1. 부트 피커에서 도구 선택
2. Reset NVRAM 선택

---

### 12. ToggleSipEntry.efi

| 항목 | 내용 |
|------|------|
| **설명** | SIP 토글 도구 |
| **기능** | System Integrity Protection 전환 |
| **필수 여부** | **선택** |
| **유형** | 도구 (Tool) |

#### 기능 상세
- SIP 활성화/비활성화
- csr-active-config 변경

#### 주의
- SIP 비활성화는 보안 위험 수반
- 필요한 경우에만 사용

---

### 13. CrScreenshotDxe.efi

| 항목 | 내용 |
|------|------|
| **설명** | 스크린샷 캡처 드라이버 |
| **기능** | UEFI 환경 스크린샷 저장 |
| **필수 여부** | **선택** |

#### 기능 상세
- F10 키로 스크린샷 캡처
- BMP/PNG 형식 저장

---

### 14. Shell.efi

| 항목 | 내용 |
|------|------|
| **설명** | UEFI Shell |
| **기능** | UEFI 명령줄 환경 |
| **필수 여부** | **선택** |

#### 기능 상세
- 디버깅 및 시스템 정보 확인
- 부팅 문제 해결 도구

---

## Lenovo IdeaPad S340 권장 드라이버 구성

### 필수
```
[ Drivers ]
├── OpenRuntime.efi    (필수)
└── OpenHfsPlus.efi    (권장 - Recovery용)
```

### 부팅 인터페이스 (선택)
```
[ Drivers ]
├── OpenRuntime.efi
├── OpenHfsPlus.efi
└── OpenCanopy.efi     (GUI 피커 사용 시)
```

### 다중 부팅 시
```
[ Drivers ]
├── OpenRuntime.efi
├── OpenHfsPlus.efi
├── OpenCanopy.efi
├── ext4_x64.efi      (Linux 시)
├── NTFS.efi          (Windows 시)
└── ExFatDxe.efi      (exFAT 사용 시)
```

### Lenovo 하드웨어 특화
```
[ Drivers ]
├── OpenRuntime.efi
├── OpenHfsPlus.efi
├── OpenCanopy.efi
└── Rts5227S.efi      (카드 리더기 - 선택)
```

---

## 드라이버 추가 방법

### config.plist 설정

```xml
<key>UEFI</key>
<dict>
    <key>Drivers</key>
    <array>
        <string>OpenRuntime.efi</string>
        <string>OpenHfsPlus.efi</string>
        <string>OpenCanopy.efi</string>
    </array>
</dict>
```

### 드라이버 추가 순서 중요

드라이버는 순서대로 로드됩니다:

1. **OpenRuntime.efi** - 항상 첫 번째
2. **파일시스템 드라이버** - 파일시스템 접근을 위해 먼저 로드
3. **하드웨어 드라이버** - 하드웨어 접근용
4. **UI 드라이버** - 마지막에 로드하여 초기화

---

## 드라이버 버전 호환성

| 드라이버 | OpenCore 0.6.x | OpenCore 0.7.x | OpenCore 0.8.x+ |
|----------|----------------|----------------|-----------------|
| OpenRuntime.efi | ✅ | ✅ | ✅ |
| OpenHfsPlus.efi | ✅ | ✅ | ✅ |
| OpenCanopy.efi | ✅ | ✅ | ✅ |
| ext4_x64.efi | ✅ | ✅ | ✅ |
| NTFS.efi | ✅ | ✅ | ✅ |
| ExFatDxe.efi | ✅ | ✅ | ✅ |

---

## 문제 해결

### 드라이버 로드 실패
1. 드라이버가 EFI/OC/Drivers/에 있는지 확인
2. config.plist에 올바르게 추가되었는지 확인
3. 드라이버 파일 손상 여부 확인

### 부트 피커가 표시되지 않음
1. OpenCanopy.efi 추가 확인
2. Misc > Boot > PickerMode 확인
3. PickerAttributes 확인

### Recovery로 부팅 불가
1. OpenHfsPlus.efi 추가 확인
2. HfsPlus.efi로 대체 시도

### Linux/Windows 부팅 불가
1. 해당 파일시스템 드라이버 추가
2. Entries 설정 확인
3. EFI 파티션 경로 확인

---

## 드라이버 관리 팁

1. **최소화**: 필요한 드라이버만 추가
2. **순서**: 필수 드라이버를 먼저 배치
3. **테스트**: 변경 후 부팅 테스트
4. **백업**: 작업 EFI 백업 유지
5. **로그**: `-v` 모드로 드라이버 로드 확인

---

## 추가 참조

### 공식 문서
- OpenCore 공식 문서: https://dortania.github.io/OpenCore-Install-Guide/
- Acidanthera Drivers: https://github.com/acidanthera/OcBinaryData

### 관련 설정
- config.plist의 UEFI 섹션
- Misc 섹션의 Boot 및 Tools 설정
