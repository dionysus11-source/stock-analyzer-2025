"""데이터 분석 관련 기능을 담당하는 모듈 (지연 로딩)"""

class DataAnalyzer:
    def __init__(self):
        self._pandas = None
        self.results = []
        
    def _load_pandas(self):
        """pandas 지연 로딩"""
        if self._pandas is None:
            import pandas as pd
            self._pandas = pd
        return self._pandas
        
    def _find_columns(self, df):
        """필요한 컬럼 찾기"""
        stock_col, profit_col, trade_type_col, code_col = None, None, None, None
        
        # 종목명 컬럼 찾기
        for col in df.columns:
            if '종목' in str(col) or 'stock' in str(col).lower() or 'name' in str(col).lower():
                stock_col = col
                break
                
        # 평가손익 컬럼 찾기
        for col in df.columns:
            if '평가손익' in str(col) or '손익' in str(col) or 'profit' in str(col).lower():
                profit_col = col
                break
        
        # 매매구분 컬럼 찾기 (선택적)
        for col in df.columns:
            if '매매' in str(col) or '구분' in str(col) or 'type' in str(col).lower():
                trade_type_col = col
                break
                
        # 코드 컬럼 찾기 (필수)
        for col in df.columns:
            if '코드' in str(col) or 'code' in str(col).lower():
                code_col = col
                break
                
        if stock_col is None or profit_col is None or code_col is None:
            available_cols = ", ".join(df.columns.tolist())
            missing_cols = []
            if stock_col is None: missing_cols.append('종목명')
            if profit_col is None: missing_cols.append('평가손익')
            if code_col is None: missing_cols.append('코드')
            raise Exception(f"필요한 컬럼({', '.join(missing_cols)})을 찾을 수 없습니다.\n사용 가능한 컬럼: {available_cols}")
            
        return stock_col, profit_col, trade_type_col, code_col
        
    def _calculate_results(self, df, stock_col, profit_col, trade_type_col, code_col):
        """결과 계산 및 통화 결정"""
        pd = self._pandas
        
        # 데이터 정리
        df[f'{profit_col}_clean'] = df[profit_col].astype(str).str.replace(',', '').str.replace(' ', '').str.strip()
        df[f'{profit_col}_clean'] = pd.to_numeric(df[f'{profit_col}_clean'], errors='coerce').fillna(0)
        
        # 매도 횟수 계산
        if trade_type_col and trade_type_col in df.columns:
            df['sell_count'] = df[trade_type_col].astype(str).apply(lambda x: 1 if '매도' in x else 0)
        else:
            df['sell_count'] = 0
            
        # 통화 결정 함수
        def determine_currency(code):
            if isinstance(code, str) and code.isalpha():
                return 'USD'
            return 'KRW'
            
        df['currency'] = df[code_col].apply(determine_currency)

        # 그룹별 집계 (stock_col과 code_col로 그룹화)
        agg_funcs = {
            f'{profit_col}_clean': 'sum',
            'sell_count': 'sum',
            'currency': 'first' # 그룹 내 통화는 동일하다고 가정
        }
        result_df = df.groupby([stock_col, code_col]).agg(agg_funcs)
        
        # 수익금 기준으로 정렬
        result_df = result_df.sort_values(by=f'{profit_col}_clean', ascending=False)
        
        # 결과 포맷팅: (종목명, 평가손익, 매도 횟수, 통화)
        formatted_results = []
        for (stock, code), row in result_df.iterrows(): # (stock, code)로 이터레이트
            formatted_results.append((stock, row[f'{profit_col}_clean'], int(row['sell_count']), row['currency']))
            
        return formatted_results
        
    def get_statistics(self):
        """통계 정보 반환 (통화별 집계)"""
        if not self.results:
            return {
                'total_stocks': 0,
                'profit_count_KRW': 0,
                'loss_count_KRW': 0,
                'total_profit_KRW': 0,
                'profit_count_USD': 0,
                'loss_count_USD': 0,
                'total_profit_USD': 0
            }
            
        total_stocks = len(self.results)
        profit_count_krw = sum(1 for _, profit, _, currency in self.results if currency == 'KRW' and profit > 0)
        loss_count_krw = sum(1 for _, profit, _, currency in self.results if currency == 'KRW' and profit < 0)
        total_profit_krw = sum(profit for _, profit, _, currency in self.results if currency == 'KRW')

        profit_count_usd = sum(1 for _, profit, _, currency in self.results if currency == 'USD' and profit > 0)
        loss_count_usd = sum(1 for _, profit, _, currency in self.results if currency == 'USD' and profit < 0)
        total_profit_usd = sum(profit for _, profit, _, currency in self.results if currency == 'USD')
        
        return {
            'total_stocks': total_stocks,
            'profit_count_KRW': profit_count_krw,
            'loss_count_KRW': loss_count_krw,
            'total_profit_KRW': total_profit_krw,
            'profit_count_USD': profit_count_usd,
            'loss_count_USD': loss_count_usd,
            'total_profit_USD': total_profit_usd
        }

    def get_date_range(self, file_path):
        """
        CSV 파일에서 '매도' 거래의 최소 및 최대 날짜를 찾아 반환합니다.
        날짜 형식은 YYYY-MM-DD 입니다.
        """
        pd = self._load_pandas()
        
        df = None
        encodings = ['euc-kr', 'cp949', 'utf-8', 'utf-8-sig']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
                
        if df is None:
            # 파일 읽기 실패 시
            return None, None
        
        try:
            # '매매구분'이 '매도'인 경우만 필터링
            if '매매구분' not in df.columns:
                # 오류 대신 (None, None) 반환하여 UI에서 처리하도록
                print("'매매구분' 열을 찾을 수 없습니다. 날짜 범위 추출 불가.")
                return None, None
            df = df[df['매매구분'] == '매도'].copy()

            # '날짜' 열을 datetime 객체로 변환
            if '날짜' not in df.columns:
                print("'날짜' 열을 찾을 수 없습니다. 날짜 범위 추출 불가.")
                return None, None
            df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d', errors='coerce')
            df.dropna(subset=['날짜'], inplace=True) # 파싱 실패한 행 제거

            if df.empty:
                return None, None # 필터링 후 데이터가 없으면

            min_date = df['날짜'].min()
            max_date = df['날짜'].max()

            return min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')

        except Exception as e:
            print(f"날짜 범위 추출 중 오류 발생: {e}")
            return None, None

    def analyze_csv(self, file_path, progress_callback=None, start_date=None, end_date=None):
        """CSV 파일 분석 (날짜 필터링 기능 추가)"""
        pd = self._load_pandas()
        
        if progress_callback:
            progress_callback(10, "파일 읽는 중...")
            
        # CSV 파일 읽기 (여러 인코딩 시도)
        df = None
        encodings = ['euc-kr', 'cp949', 'utf-8', 'utf-8-sig']
        
        for i, encoding in enumerate(encodings):
            try:
                if progress_callback:
                    progress_callback(20 + i * 5, f"인코딩 시도 중... ({encoding})")
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
                
        if df is None:
            raise Exception("파일 인코딩을 인식할 수 없습니다.")
            
        # 날짜 필터링 로직
        if start_date or end_date:
            if progress_callback:
                progress_callback(50, "날짜 필터링 적용 중...")
            
            try:
                # '매매구분' 열 확인
                if '매매구분' not in df.columns:
                    raise Exception("'매매구분' 열을 찾을 수 없습니다.")
                
                # '날짜' 열 확인
                if '날짜' not in df.columns:
                    raise Exception("'날짜' 열을 찾을 수 없습니다.")

                # '매매구분'이 '매도'인 경우만 필터링
                df = df[df['매매구분'] == '매도'].copy()

                # '날짜' 열을 datetime 객체로 변환
                df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d', errors='coerce')
                df.dropna(subset=['날짜'], inplace=True) # 파싱 실패한 행 제거

                # 시작일 필터링
                if start_date:
                    start_date_dt = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
                    if pd.notna(start_date_dt):
                        df = df[df['날짜'] >= start_date_dt]

                # 종료일 필터링
                if end_date:
                    end_date_dt = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')
                    if pd.notna(end_date_dt):
                        df = df[df['날짜'] <= end_date_dt]
            
            except Exception as e:
                raise Exception(f"날짜 필터링 중 오류 발생: {e}")

        if progress_callback:
            progress_callback(60, "데이터 분석 중...")
            
        # 컬럼 찾기 및 분석
        stock_col, profit_col, trade_type_col, code_col = self._find_columns(df)
        
        if progress_callback:
            progress_callback(80, "결과 계산 중...")
            
        # 데이터 정리 및 계산
        results = self._calculate_results(df, stock_col, profit_col, trade_type_col, code_col)
        
        if progress_callback:
            progress_callback(100, "분석 완료!")
            
        self.results = results
        return results