"""UI 컴포넌트를 담당하는 모듈"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from tkcalendar import DateEntry # tkcalendar에서 DateEntry 임포트

class ProgressDialog:
    def __init__(self, parent, title="처리 중..."):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x120")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 화면 중앙에 위치
        self.center_dialog(parent)
        
        self.setup_ui()
        
    def center_dialog(self, parent):
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 150
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 60
        self.dialog.geometry(f"300x120+{x}+{y}")
        
    def setup_ui(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(expand=True, fill='both')
        
        self.status_label = ttk.Label(frame, text="처리 중...")
        self.status_label.pack(pady=(0, 10))
        
        self.progress = ttk.Progressbar(frame, length=250, mode='determinate')
        self.progress.pack(pady=(0, 10))
        
        self.percent_label = ttk.Label(frame, text="0%")
        self.percent_label.pack()
        
    def update(self, value, text=""):
        self.progress['value'] = value
        self.percent_label.config(text=f"{int(value)}%")
        if text:
            self.status_label.config(text=text)
        self.dialog.update()
        
    def close(self):
        self.dialog.destroy()

class MainUI:
    def __init__(self, root, file_handler, data_analyzer, version="N/A"):
        self.root = root
        self.file_handler = file_handler
        self.data_analyzer = data_analyzer
        self.version = version
        self.sort_state = {}  # 정렬 상태 저장
        
        # 드래그 앤 드롭 지연 로딩
        self._tkdnd = None
        self._dnd_enabled = False
        
        self.setup_window()
        self.setup_ui()
        
    def _load_tkdnd(self):
        """tkinterdnd2 지연 로딩"""
        if self._tkdnd is None:
            try:
                import tkinterdnd2 as tkdnd
                self._tkdnd = tkdnd
                print("tkinterdnd2 모듈 로딩 성공")
                return True
            except ImportError:
                print("tkinterdnd2 모듈을 찾을 수 없습니다.")
                return False
        return True
        
    def setup_window(self):
        self.root.title("주식 평가손익 분석기")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="주식 평가손익 분석기", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 파일 선택 영역
        self.setup_file_area(main_frame)
        
        # 결과 표시 영역
        self.setup_result_area(main_frame)
        
        # 상태바 영역
        self.setup_statusbar()
        
        # 그리드 가중치 설정
        self.setup_grid_weights(main_frame)
        
    def setup_file_area(self, parent):
        file_frame = ttk.LabelFrame(parent, text="CSV 파일 선택 및 병합", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # 드래그 앤 드롭 영역
        self.drop_area = tk.Label(file_frame, 
                                 text="CSV 파일을 여기에 드래그하거나\n아래 버튼을 클릭하세요",
                                 bg='#e8e8e8', 
                                 relief='ridge',
                                 bd=2,
                                 height=4,
                                 font=('Arial', 12))
        self.drop_area.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(0, 10)) # columnspan 3 -> 5
        
        # 버튼들
        select_btn = ttk.Button(file_frame, text="파일 선택", command=self.select_file)
        select_btn.grid(row=1, column=0, padx=(0, 10), sticky=tk.EW)
        
        merge_btn = ttk.Button(file_frame, text="CSV 파일 병합", command=self.merge_csv_files)
        merge_btn.grid(row=1, column=1, padx=(0, 10), sticky=tk.EW)

        self.analyze_btn = ttk.Button(file_frame, text="분석 시작", 
                                     command=self.analyze_file, state='disabled')
        self.analyze_btn.grid(row=1, column=2, sticky=tk.EW)
        
        # 날짜 필터 영역
        date_frame = ttk.Frame(file_frame)
        date_frame.grid(row=2, column=0, columnspan=5, pady=(10, 0), sticky=tk.W) # columnspan 3 -> 5

        ttk.Label(date_frame, text="시작일:").grid(row=0, column=0, padx=(0, 5))
        self.start_date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                      foreground='white', borderwidth=2, locale='ko_KR') # DateEntry 사용
        self.start_date_entry.grid(row=0, column=1)
        # ttk.Label(date_frame, text="(YYYY-MM-DD)").grid(row=0, column=2, padx=(2, 20)) # 제거

        ttk.Label(date_frame, text="종료일:").grid(row=0, column=2, padx=(20, 5)) # column 3 -> 2, padx 조정
        self.end_date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, locale='ko_KR') # DateEntry 사용
        self.end_date_entry.grid(row=0, column=3) # column 4 -> 3
        # ttk.Label(date_frame, text="(YYYY-MM-DD)").grid(row=0, column=5) # 제거

        # 현재 파일 표시
        self.file_label = ttk.Label(file_frame, text="선택된 파일: 없음")
        self.file_label.grid(row=3, column=0, columnspan=5, pady=(10, 0)) # columnspan 3 -> 5
        
        # 드래그 앤 드롭 설정 (지연)
        self.root.after(500, self.setup_drag_drop)
        
        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)
        file_frame.columnconfigure(2, weight=1)
        file_frame.columnconfigure(3, weight=1) # 추가
        file_frame.columnconfigure(4, weight=1) # 추가
        
    def setup_result_area(self, parent):
        result_frame = ttk.LabelFrame(parent, text="분석 결과 (헤더를 클릭하여 정렬)", padding="10")
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # 트리뷰 (테이블)
        columns = ('순위', '종목명', '평가손익', '매도 횟수')
        self.tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        # 헤더 설정 및 정렬 이벤트 바인딩
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
        
        # 컬럼 너비 설정
        self.tree.column('순위', width=60, anchor='center')
        self.tree.column('종목명', width=200, anchor='w')
        self.tree.column('평가손익', width=150, anchor='e')
        self.tree.column('매도 횟수', width=100, anchor='center')
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 통계 정보
        self.stats_label = ttk.Label(result_frame, text="")
        self.stats_label.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

    def setup_statusbar(self):
        """상태바 설정"""
        version_label = ttk.Label(self.root, text=f"Version: {self.version}", relief='sunken', anchor='e')
        version_label.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

    def sort_column(self, col):
        """컬럼 헤더를 클릭하여 테이블 정렬"""
        reverse = self.sort_state.get(col, False)
        
        # 데이터 가져오기
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # 데이터 타입에 따른 정렬
        if col in ['평가손익', '매도 횟수', '순위']:
            # 숫자 형식 정리 및 변환
            def safe_float(s):
                try:
                    return float(s.replace('+', '').replace('원', '').replace('$', '').replace(',', ''))
                except (ValueError, AttributeError):
                    return 0
            data.sort(key=lambda x: safe_float(x[0]), reverse=reverse)
        else: # 문자열 정렬
            data.sort(key=lambda x: x[0], reverse=reverse)
            
        # 정렬된 순서대로 아이템 재배치
        for index, (_, item) in enumerate(data):
            self.tree.move(item, '', index)
            
        # 순위 재설정 (정렬 기준이 순위가 아닐 때)
        if col != '순위':
            for index, (_, item) in enumerate(data):
                self.tree.set(item, '순위', index + 1)

        # 다음 정렬 순서 설정
        self.sort_state[col] = not reverse
        # 헤더 텍스트에 정렬 방향 표시
        for c in self.tree['columns']:
            text = c
            if c == col:
                text += ' ▼' if reverse else ' ▲'
            self.tree.heading(c, text=text)

    def setup_grid_weights(self, main_frame):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def setup_drag_drop(self, event=None): # event=None 추가
        """드래그 앤 드롭 설정 (지연 로딩)"""
        if self._load_tkdnd():
            try:
                # tkinterdnd2를 사용한 드래그 앤 드롭 설정
                self.drop_area.drop_target_register(self._tkdnd.DND_FILES)
                self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
                self._dnd_enabled = True
                print("드래그 앤 드롭 기능 활성화됨")
                
                # 성공 시 메시지 업데이트
                current_text = self.drop_area.cget('text')
                if "아래 버튼을" not in current_text:
                    self.drop_area.config(text="CSV 파일을 여기에 드래그하거나\n아래 버튼을 클릭하세요")
                    
            except Exception as e:
                print(f"드래그 앤 드롭 설정 실패: {e}")
                self._dnd_enabled = False
                # 실패 시 안내 메시지 업데이트
                self.drop_area.config(text="파일 선택 버튼을 사용하세요\n(드래그 앤 드롭 불가)")
        else:
            print("tkinterdnd2 로딩 실패 - 드래그 앤 드롭 비활성화")
            self.drop_area.config(text="파일 선택 버튼을 사용하세요\n(드래그 앤 드롭 불가)")
            
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 처리"""
        try:
            files = self.root.tk.splitlist(event.data)
            file_path = self.file_handler.handle_drop(files)
            if file_path:
                self.update_file_display(file_path)
        except Exception as e:
            print(f"드래그 앤 드롭 처리 오류: {e}")
            messagebox.showerror("오류", "파일을 처리할 수 없습니다.")
    
    def merge_csv_files(self):
        """CSV 파일 병합 기능을 file_handler에서 호출"""
        self.file_handler.merge_csv_files(parent=self.root)
            
    def select_file(self):
        """파일 선택"""
        file_path = self.file_handler.select_file(self.root)
        if file_path:
            self.update_file_display(file_path)
            
    def update_file_display(self, file_path):
        """파일 표시 업데이트 및 날짜 필드 자동 채우기"""
        filename = self.file_handler.get_filename(file_path)
        self.file_label.config(text=f"선택된 파일: {filename}")
        self.analyze_btn.config(state='normal')
        self.drop_area.config(text=f"파일 로드됨: {filename}\n분석 버튼을 클릭하세요", 
                             bg='#d4edda')
        
        # 날짜 필드 자동 채우기
        min_date, max_date = self.data_analyzer.get_date_range(file_path)
        
        if min_date and max_date:
            # DateEntry 위젯에 날짜 설정
            # DateEntry의 set_date 메서드는 datetime.date 객체를 기대한다.
            from datetime import datetime
            self.start_date_entry.set_date(datetime.strptime(min_date, '%Y-%m-%d').date())
            self.end_date_entry.set_date(datetime.strptime(max_date, '%Y-%m-%d').date())
        else:
            # 날짜가 없을 경우 필드를 비워두거나 기본값 설정
            self.start_date_entry.set_date(None)
            self.end_date_entry.set_date(None)
                             
    def analyze_file(self):
        """파일 분석 (백그라운드)"""
        if not self.file_handler.current_file:
            messagebox.showerror("오류", "파일을 먼저 선택하세요.")
            return

        # 날짜 값 가져오기 (DateEntry에서 날짜 가져오기)
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d') if self.start_date_entry.get_date() else ""
        end_date = self.end_date_entry.get_date().strftime('%Y-%m-%d') if self.end_date_entry.get_date() else ""
            
        # 진행률 대화상자 표시
        progress_dialog = ProgressDialog(self.root, "파일 분석 중...")
        
        def analyze_worker():
            try:
                # 분석 실행
                results = self.data_analyzer.analyze_csv(
                    self.file_handler.current_file,
                    progress_callback=progress_dialog.update,
                    start_date=start_date,
                    end_date=end_date
                )
                
                # UI 업데이트 (메인 스레드에서)
                self.root.after(0, lambda: self.update_results(results, progress_dialog))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(str(e), progress_dialog))
                
        # 백그라운드에서 분석 실행
        thread = threading.Thread(target=analyze_worker, daemon=True)
        thread.start()
        
    def update_results(self, results, progress_dialog):
        """결과 업데이트"""
        progress_dialog.close()
        
        # 기존 결과 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 새 결과 추가
        for i, (stock_name, profit, sell_count, currency_type) in enumerate(results, 1):
            if currency_type == 'USD':
                profit_str = f"${profit:,.2f}" # 달러는 소수점 둘째 자리까지
                if profit > 0:
                    profit_str = f"+{profit_str}"
            else: # KRW
                profit_str = f"{profit:,.0f}원"
                if profit > 0:
                    profit_str = f"+{profit_str}"
                
            tag = 'profit' if profit >= 0 else 'loss'
            values = (i, stock_name, profit_str, sell_count)
            self.tree.insert('', 'end', values=values, tags=(tag,))
            
        # 색상 태그 설정
        self.tree.tag_configure('profit', foreground='red')
        self.tree.tag_configure('loss', foreground='blue')
        
        # 통계 정보 업데이트
        stats = self.data_analyzer.get_statistics()
        stats_text = f"총 {stats['total_stocks']}개 종목"
        
        # KRW 통계가 있을 경우
        if stats['total_profit_KRW'] != 0 or stats['profit_count_KRW'] != 0 or stats['loss_count_KRW'] != 0:
            stats_text += f" | (KRW) 수익: {stats['profit_count_KRW']}개, 손실: {stats['loss_count_KRW']}개, 총 평가손익: {stats['total_profit_KRW']:,.0f}원"
            
        # USD 통계가 있을 경우
        if stats['total_profit_USD'] != 0 or stats['profit_count_USD'] != 0 or stats['loss_count_USD'] != 0:
            stats_text += f" | (USD) 수익: {stats['profit_count_USD']}개, 손실: {stats['loss_count_USD']}개, 총 평가손익: ${stats['total_profit_USD']:,.2f}"

        self.stats_label.config(text=stats_text)
        
        # 초기 정렬 상태 설정
        self.sort_state = {}
        self.sort_column('평가손익') # 기본으로 평가손익 내림차순 정렬
        self.sort_column('평가손익') # 한번 더 호출하여 내림차순(▲)으로 표시
        
    def handle_error(self, error_msg, progress_dialog):
        """에러 처리"""
        progress_dialog.close()
        messagebox.showerror("오류", f"파일 분석 중 오류가 발생했습니다:\n{error_msg}")

class UpdateProgressDialog:
    def __init__(self, parent, title="업데이트 중..."):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("350x150")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # 화면 중앙에 위치
        self.center_dialog(parent)
        
        self.setup_ui()
        
    def center_dialog(self, parent):
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 175
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 75
        self.dialog.geometry(f"350x150+{x}+{y}")
        
    def setup_ui(self):
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(expand=True, fill='both')
        
        self.status_label = ttk.Label(frame, text="업데이트를 준비하고 있습니다...\n잠시만 기다려 주세요.", justify=tk.CENTER)
        self.status_label.pack(pady=(10, 15))
        
        self.progress = ttk.Progressbar(frame, length=300, mode='indeterminate')
        self.progress.pack()
        self.progress.start(10)
        
    def update_text(self, text):
        self.status_label.config(text=text)
        self.dialog.update()
        
    def close(self):
        self.progress.stop()
        self.dialog.destroy()