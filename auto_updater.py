import sys
import os
import json
import urllib.request
import tempfile
import zipfile
import subprocess
import logging
from packaging.version import parse as parse_version

# PyInstaller로 빌드된 실행 파일의 경로를 올바르게 찾기 위함
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 로깅 설정 ---
LOG_FILE = os.path.join(APP_DIR, 'updater.log')
logging.basicConfig(level=logging.INFO, 
                    filename=LOG_FILE, 
                    filemode='w', # 새 실행마다 로그 파일 덮어쓰기
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Github 저장소 정보
GH_OWNER = 'dionysus11-source'
GH_REPO = 'stock-analyzer-2025'
# Github Release에 포함된 배포용 압축 파일 이름
RELEASE_ASSET_NAME = 'stock.zip'

def get_current_version():
    """_version.py에서 현재 버전을 읽어옵니다."""
    try:
        from _version import __version__
        logging.info(f"Current version from _version.py: {__version__}")
        return __version__
    except ImportError as e:
        logging.error(f"Could not import __version__: {e}")
        return "0.0.0"

def check_for_updates():
    """
    Github에서 새 릴리즈를 확인합니다.
    업데이트가 있으면 최신 버전 정보를 반환하고, 없으면 None을 반환합니다.
    """
    current_version_str = get_current_version()
    current_version = parse_version(current_version_str)

    api_url = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/releases/latest"
    logging.info(f"Checking for updates at {api_url}")

    try:
        with urllib.request.urlopen(api_url) as response:
            if response.status != 200:
                logging.error(f"Error checking for updates: HTTP {response.status}")
                return None
            
            release_data = json.loads(response.read().decode())
            latest_version_str = release_data['tag_name'].lstrip('v')
            latest_version = parse_version(latest_version_str)

            logging.info(f"Current version: {current_version}, Latest version: {latest_version}")

            if latest_version > current_version:
                logging.info("New version found.")
                for asset in release_data['assets']:
                    if asset['name'] == RELEASE_ASSET_NAME:
                        logging.info(f"Found release asset '{RELEASE_ASSET_NAME}' with download URL.")
                        return {
                            "latest_version": latest_version_str,
                            "download_url": asset['browser_download_url'],
                            "release_notes": release_data['body']
                        }
                logging.error(f"Release asset '{RELEASE_ASSET_NAME}' not found in the latest release.")
                return None

    except Exception as e:
        logging.error(f"An error occurred while checking for updates: {e}", exc_info=True)
        return None
    
    logging.info("Application is up to date.")
    return None

def download_and_install_update(download_url):
    """
    업데이트를 다운로드하고 설치를 준비합니다.
    성공하면 업데이트 스크립트 경로를 반환하고, 실패하면 None을 반환합니다.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        logging.info(f"Created temporary directory: {temp_dir}")
        zip_path = os.path.join(temp_dir, RELEASE_ASSET_NAME)

        logging.info(f"Downloading update from {download_url} to {zip_path}")
        urllib.request.urlretrieve(download_url, zip_path)

        extract_dir = os.path.join(temp_dir, 'extracted')
        os.makedirs(extract_dir, exist_ok=True)
        logging.info(f"Extracting update to {extract_dir}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        update_script_path = create_update_script(extract_dir, temp_dir)
        return update_script_path

    except Exception as e:
        logging.error(f"Failed to download and install update: {e}", exc_info=True)
        return None


def create_update_script(source_dir, temp_dir):
    """업데이트를 수행할 배치 스크립트를 생성합니다."""
    script_path = os.path.join(temp_dir, 'update.bat')
    
    source_path = os.path.normpath(source_dir)
    target_path = os.path.normpath(APP_DIR)
    main_exe_path = os.path.join(target_path, "main.exe")

    script_content = f"""
@echo off
chcp 65001
echo.
echo ==========================================================
echo               Application Updater
echo ==========================================================
echo.
set "XCOPY_LOG_PATH=%~dp0xcopy_log.txt"
echo File copy log will be saved to: 
echo %XCOPY_LOG_PATH%
echo.

echo Waiting for the main application to close...
ping -n 4 127.0.0.1 > nul

echo.
echo Copying new files...
echo    FROM: "{source_path}"
echo    TO:   "{target_path}"
xcopy "{source_path}" "{target_path}" /E /Y /I /C > "%XCOPY_LOG_PATH%" 2>&1

echo.
echo File copy command has been executed.
echo Please check the log file for details.
echo.

echo Verifying copy...
if exist "{main_exe_path}" (
    echo Copy successful. Restarting application...
    start "" "{main_exe_path}"
) else (
    echo ERROR: Main executable not found after copy! Check the log.
)

echo.
echo Update process finished. This window can be closed.
echo.
pause
"""
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    logging.info(f"Update script created at: {script_path}")
    return script_path


def run_updater_and_exit(script_path):
    """업데이트 스크립트를 실행하고 현재 애플리케이션을 종료합니다."""
    logging.info(f"Executing update script: {script_path}")
    # CREATE_NEW_CONSOLE 플래그를 사용하여 새 콘솔 창에서 배치 파일을 실행합니다.
    subprocess.Popen([script_path], creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
    sys.exit(0)
