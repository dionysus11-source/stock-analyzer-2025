# 주식 평가손익 분석기

Magic Split 매매내역을 분석하여 평가손익을 계산하는 도구입니다.

## 🚀 빠른 시작

### 1단계: Magic Split에서 CSV 파일 내보내기
1. **Magic Split** 프로그램 실행
2. **모든 매매내역** 화면으로 이동
3. 매매내역 목록에서 **마우스 오른쪽 클릭**
4. **CSV 저장** 선택하여 파일 저장

### 2단계: 프로그램 실행
1. 이 GitHub 저장소의 Release 페이지에서  ZIP 파일을 다운로드합니다.
https://github.com/dionysus11-source/stock-analyzer-2025/releases


2. **`main.exe`** 파일을 더블클릭하여 실행
   - Python과 필요한 라이브러리가 자동으로 설치됩니다
   - 설치 후 프로그램이 자동으로 시작됩니다

### 3단계: CSV 파일 분석
1. 프로그램이 실행되면 CSV 파일을 **드래그 앤 드롭**
2. 또는 **파일 선택** 버튼으로 Magic Split에서 저장한 CSV 파일 선택
3. 분석 결과 확인

## 🚀 버전 관리

이 애플리케이션의 버전은 `_version.py` 파일에 정의되어 있습니다. 새 릴리스를 준비하거나 버전 정보를 업데이트할 때 다음 지침을 따르세요:

### 버전 업데이트 방법
1. 프로젝트 루트 디렉토리에 있는 `_version.py` 파일을 엽니다.
2. `__version__ = "vX.Y.Z"` 형식으로 되어 있는 문자열을 수정합니다.
   - `X`: **MAJOR** 버전 (하위 호환성을 지원하지 않는 큰 변경사항이 있을 때 증가)
   - `Y`: **MINOR** 버전 (하위 호환성을 유지하면서 새로운 기능을 추가할 때 증가)
   - `Z`: **PATCH** 버전 (버그 수정 등 작은 변경사항이 있을 때 증가)
3. 변경사항을 저장합니다. 애플리케이션을 다시 실행하면 업데이트된 버전이 UI에 표시됩니다.

**예시:**
- `__version__ = "v1.0.0"` (첫 번째 주요 릴리스)
- `__version__ = "v1.0.1"` (버그 수정)
- `__version__ = "v1.1.0"` (새로운 기능 추가)

## 📋 주요 기능

- ✅ **Magic Split CSV 파일 지원**
- ✅ **드래그 앤 드롭** 파일 업로드
- ✅ **평가손익 자동 계산**
- ✅ **종목별 통계** 표시
- ✅ **CSV 파일 합치기**
- ✅ **달러/원 구분 표시**

## 🛠️ 시스템 요구사항

- **Windows 10/11**
- **Python 3.8+** (run_python.bat이 자동 확인)
- **인터넷 연결** (최초 라이브러리 설치 시)

## 📁 파일 구성

```
├── main.py               # 메인 프로그램
├── ui_components.py      # UI 컴포넌트
├── file_handler.py       # 파일 처리
├── data_analyzer.py      # 데이터 분석 엔진
├── requirements.txt      # Python 패키지 목록
├── run_python.bat        # 실행 스크립트 (권장)
├── TradingHistory.csv    # 샘플 데이터
└── README.md            # 이 파일
```

## 🔧 문제 해결

**Python이 설치되지 않은 경우:**
- [Python 공식 사이트](https://python.org)에서 Python 3.8+ 설치

**라이브러리 설치 오류:**
- 관리자 권한으로 `run_python.bat` 실행
- 또는 수동 설치: `pip install -r requirements.txt`

**CSV 파일 인식 오류:**
- Magic Split에서 올바른 형식으로 CSV 저장 확인
- 파일 인코딩이 UTF-8 또는 CP949인지 확인

## 💡 사용 팁

- **샘플 데이터**: `TradingHistory.csv` 파일로 먼저 테스트해보세요
- **성능**: 대용량 파일도 빠르게 처리됩니다
- **호환성**: Magic Split의 모든 버전 CSV 형식 지원
