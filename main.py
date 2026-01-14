"""최적화된 주식 분석기 메인 진입점"""
import tkinter as tk
import time

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
        
        # 메인 앱 실행
        create_main_app()
        
    except Exception as e:
        print(f"메인 함수 오류: {e}")
        import traceback
        traceback.print_exc()
        input("엔터를 눌러 종료...")

if __name__ == "__main__":
    main()