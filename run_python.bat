@echo off
echo ========================================
echo    Stock Portfolio Analyzer (Python Version)
echo ========================================
echo.

REM 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b 1
)

echo Checking Python installation...
python --version

REM 필요한 라이브러리 설치 확인
echo.
echo Checking for required libraries...
python -c "import pandas, tkinterdnd2" 2>nul
if errorlevel 1 (
    echo Installing required libraries...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install libraries.
        pause
        exit /b 1
    )
    echo Library installation complete!
    echo.
) else (
    echo All libraries are already installed.
    echo.
)

REM 프로그램 실행
echo Running the program...
echo.
python main.py

REM 오류 발생 시 대기
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while running the program.
    pause
)