# Change: 달력 선택 기능으로 날짜 입력 방식 변경

## Why
현재 날짜를 직접 숫자로 입력하는 방식은 사용자가 불편을 겪고 있으며, 입력 오류의 가능성이 있습니다. 날짜를 달력에서 직접 선택하는 방식으로 변경하면 사용자 경험이 향상되고 오류를 줄일 수 있습니다.

## What Changes
- 날짜 입력 방식을 텍스트 필드에서 달력(데이트 피커) 위젯으로 변경합니다.
- 달력의 기본값은 앱 실행 시 불러온 CSV 데이터의 가장 오래된 날짜와 가장 최신 날짜로 설정됩니다.

## Impact
- Affected specs: `ui-components` (new)
- Affected code: `ui_components.py`, `main.py`
