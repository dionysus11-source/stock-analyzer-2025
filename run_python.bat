@echo off
echo ========================================
echo    주식 평가손익 분석기 (Python 버전)
echo ========================================
echo.

REM 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되지 않았습니다.
    echo Python 3.8 이상을 설치해주세요.
    echo.
    pause
    exit /b 1
)

echo Python 버전 확인 중...
python --version

REM 필요한 라이브러리 설치 확인
echo.
echo 필요한 라이브러리 확인 중...
python -c "import pandas, tkinterdnd2" 2>nul
if errorlevel 1 (
    echo 필요한 라이브러리를 설치합니다...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [오류] 라이브러리 설치에 실패했습니다.
        pause
        exit /b 1
    )
    echo 라이브러리 설치 완료!
    echo.
) else (
    echo 모든 라이브러리가 설치되어 있습니다.
    echo.
)

REM 프로그램 실행
echo 프로그램을 실행합니다...
echo.
python main.py

REM 오류 발생 시 대기
if errorlevel 1 (
    echo.
    echo [오류] 프로그램 실행 중 오류가 발생했습니다.
    pause
)