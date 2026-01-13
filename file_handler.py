"""파일 처리 관련 기능을 담당하는 모듈"""
import os
from tkinter import filedialog, messagebox
import pandas as pd

class FileHandler:
    def __init__(self):
        self.current_file = None
        self.supported_extensions = ['.csv']
        
    def select_file(self, parent=None):
        """파일 선택 대화상자 표시"""
        file_path = filedialog.askopenfilename(
            parent=parent,
            title="CSV 파일 선택",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path and self.validate_file(file_path):
            self.current_file = file_path
            return file_path
        return None
        
    def validate_file(self, file_path):
        """파일 유효성 검사"""
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "파일이 존재하지 않습니다.")
            return False
            
        if not any(file_path.lower().endswith(ext) for ext in self.supported_extensions):
            messagebox.showerror("오류", "CSV 파일만 지원됩니다.")
            return False
            
        return True
        
    def get_filename(self, file_path=None):
        """파일명 반환"""
        path = file_path or self.current_file
        return os.path.basename(path) if path else "없음"
        
    def handle_drop(self, file_paths):
        """드래그 앤 드롭 파일 처리"""
        if not file_paths:
            return None
            
        # 파일 경로 처리 (리스트, 튜플, 문자열 모두 처리)
        if isinstance(file_paths, (list, tuple)):
            file_path = file_paths[0]
        else:
            file_path = file_paths
            
        # 문자열로 변환 및 따옴표 제거
        file_path = str(file_path).strip().strip('"').strip("'")
        
        # 중괄호로 둘러싸인 경우 처리 (Windows 특수 경우)
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        print(f"처리할 파일 경로: {file_path}")
        
        if self.validate_file(file_path):
            self.current_file = file_path
            return file_path
        return None

    def merge_csv_files(self, parent=None):
        """여러 CSV 파일을 병합하고 중복을 제거하여 새 파일로 저장"""
        try:
            file_paths = filedialog.askopenfilenames(
                parent=parent,
                title="병합할 CSV 파일들을 선택하세요",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if len(file_paths) < 2:
                if len(file_paths) > 0: # 0개 또는 1개 선택 시
                    messagebox.showinfo("알림", "병합하려면 2개 이상의 파일을 선택해야 합니다.", parent=parent)
                return

            df_list = []
            for path in file_paths:
                # FileHandler 내의 validate_file을 재사용
                if not self.validate_file(path):
                    # 유효성 검사 실패 메시지는 validate_file 내부에서 처리됨
                    return 

                try:
                    df = pd.read_csv(path, encoding='cp949', engine='python')
                except UnicodeDecodeError:
                    df = pd.read_csv(path, encoding='utf-8', engine='python')
                df_list.append(df)

            if not df_list:
                return

            # 데이터프레임 병합
            merged_df = pd.concat(df_list, ignore_index=True)
            
            # 중복 행 제거 (모든 열이 동일한 경우)
            deduplicated_df = merged_df.drop_duplicates()
            
            # 결과 저장
            output_filename = "merged_data.csv"
            deduplicated_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
            
            messagebox.showinfo(
                "성공",
                f"{len(file_paths)}개의 파일이 성공적으로 병합되었습니다.\n"
                f"총 {len(merged_df)}개 행 -> 중복 제거 후 {len(deduplicated_df)}개 행.\n"
                f"결과가 '{output_filename}'에 저장되었습니다.",
                parent=parent
            )

        except Exception as e:
            messagebox.showerror("병합 오류", f"파일 병합 중 오류가 발생했습니다:\n{e}", parent=parent)