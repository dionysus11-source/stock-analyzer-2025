"""최적화된 주식 분석기 메인 진입점"""
import tkinter as tk
from tkinter import messagebox
import time
import threading

def create_main_app():
    """메인 애플리케이션 생성 (지연 로딩)"""
    try:
        # 필요한 모듈들을 여기서 임포트 (지연 로딩)
        from ui_components import MainUI
        from file_handler import FileHandler
        from data_analyzer import DataAnalyzer
        from _version import __version__
        
        # tkinterdnd2 호환 루트 생성 시도
        try:
            import tkinterdnd2 as tkdnd
            root = tkdnd.TkinterDnD.Tk()
            print("tkinterdnd2 호환 루트 생성 성공")
        except ImportError:
            # tkinterdnd2가 없으면 일반 Tk 사용
            root = tk.Tk()
            print("일반 Tk 루트 생성 (드래그 앤 드롭 비활성화)")
        
        # 컴포넌트 초기화
        file_handler = FileHandler()
        data_analyzer = DataAnalyzer()
        
        # UI 생성
        app = MainUI(root, file_handler, data_analyzer, __version__)
        
        # 메인 루프 시작
        root.mainloop()
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        input("엔터를 눌러 종료...")

def show_simple_splash():
    """간단한 스플래시 스크린"""
    splash_root = tk.Tk()
    splash_root.title("로딩 중...")
    splash_root.geometry("300x150")
    splash_root.resizable(False, False)
    
    # 화면 중앙에 위치
    splash_root.update_idletasks()
    x = (splash_root.winfo_screenwidth() // 2) - 150
    y = (splash_root.winfo_screenheight() // 2) - 75
    splash_root.geometry(f"300x150+{x}+{y}")
    
    # 스플래시 내용
    splash_root.configure(bg='#2c3e50')
    
    title_label = tk.Label(splash_root, 
                          text="주식 분석기", 
                          font=('Arial', 14, 'bold'),
                          fg='white', bg='#2c3e50')
    title_label.pack(pady=30)
    
    status_label = tk.Label(splash_root,
                           text="로딩 중...",
                           font=('Arial', 10),
                           fg='#ecf0f1', bg='#2c3e50')
    status_label.pack()
    
    # 스플래시 표시
    splash_root.update()
    
    # 잠시 대기 (로딩 시뮬레이션)
    time.sleep(1)
    
    # 스플래시 닫기
    splash_root.destroy()

def main():
    """애플리케이션 진입점"""
    try:
        # 스플래시 스크린 표시
        show_simple_splash()
        
        # --- 업데이트 확인 로직 시작 ---
        hidden_root = tk.Tk()
        hidden_root.withdraw()

        try:
            from auto_updater import check_for_updates, download_and_install_update, run_updater_and_exit
            from ui_components import UpdateProgressDialog

            update_info = check_for_updates()
            
            if update_info:
                release_notes = update_info.get('release_notes', '릴리즈 노트를 불러올 수 없습니다.')
                msg = (
                    f"새로운 버전 ({update_info['latest_version']})이 있습니다. 업데이트 하시겠습니까?\n\n"
                    f"릴리즈 노트:\n{release_notes}"
                )
                
                if messagebox.askyesno("업데이트 확인", msg, parent=hidden_root):
                    progress_dialog = UpdateProgressDialog(hidden_root)
                    
                    def run_update_in_background():
                        """백그라운드에서 업데이트 다운로드 및 준비, UI 업데이트는 메인 스레드에서 예약"""
                        try:
                            # 이 함수는 백그라운드 스레드에서 실행되므로 직접 UI를 업데이트하지 않음
                            # progress_dialog.update_text("업데이트 파일을 다운로드 중입니다...") -> 직접 호출 대신 예약 필요
                            
                            script_path = download_and_install_update(update_info['download_url'])
                            
                            if script_path:
                                # 사용자가 메시지를 볼 수 있도록 잠시 대기
                                time.sleep(1) 
                                # 메인 스레드에서 프로그램 종료 및 업데이터 실행 예약
                                hidden_root.after(0, run_updater_and_exit, script_path)
                            else:
                                # 에러 메시지 표시 및 다이얼로그 닫기를 메인 스레드에서 예약
                                def show_error_and_close():
                                    progress_dialog.close()
                                    messagebox.showerror("업데이트 실패", "업데이트 파일을 다운로드하거나 준비하는 데 실패했습니다.", parent=hidden_root)
                                hidden_root.after(0, show_error_and_close)
                                
                        except Exception as e:
                            # 예외 발생 시 에러 메시지 표시 및 다이얼로그 닫기를 메인 스레드에서 예약
                            def show_exception_and_close(err):
                                progress_dialog.close()
                                messagebox.showerror("업데이트 오류", f"업데이트 중 오류가 발생했습니다: {err}", parent=hidden_root)
                            hidden_root.after(0, show_exception_and_close, e)

                    # 백그라운드에서 업데이트 실행
                    update_thread = threading.Thread(target=run_update_in_background, daemon=True)
                    update_thread.start()
                    
                    # 업데이트 다이얼로그가 떠있는 동안 hidden_root의 메인 루프를 실행
                    hidden_root.mainloop()
                    return # 업데이트가 시작되면 메인 앱을 실행하지 않고 종료

        except Exception as e:
            # Log the error and show a message to the user
            error_msg = f"업데이트 확인 중 오류가 발생했습니다:\n\n{e}\n\n자세한 내용은 updater.log 파일을 확인하세요."
            try:
                # Try to use the logger from the updater module
                from auto_updater import logging
                logging.error("Update check failed in main.py", exc_info=True)
            except ImportError:
                # If updater is not even there, just print
                print("Could not import updater to log error.")
            
            messagebox.showerror("업데이트 확인 오류", error_msg, parent=hidden_root)
        
        finally:
            hidden_root.destroy()
        # --- 업데이트 확인 로직 종료 ---

        # 메인 앱 실행
        create_main_app()
        
    except Exception as e:
        print(f"메인 함수 오류: {e}")
        import traceback
        traceback.print_exc()
        input("엔터를 눌러 종료...")

if __name__ == "__main__":
    main()