import flet as ft
from datetime import datetime
from calculator import calculate_parking_fee

class ParkingCalculatorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "주차 요금 계산기"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 500
        self.page.window.height = 700
        self.page.padding = 20

        # 데이터 저장용 리스트: [{'start': str, 'end': str, 'duration': str, 'fee': int, 'id': int}, ...]
        self.history = []
        self.counter = 0

        # UI 컴포넌트 초기화
        self.start_time_input = ft.TextField(
            label="입차 시간 (HH:MM)", 
            hint_text="예: 09:00",
            width=200,
            on_change=self.clear_errors
        )
        self.end_time_input = ft.TextField(
            label="출차 시간 (HH:MM)", 
            hint_text="예: 10:30",
            width=200,
            on_change=self.clear_errors
        )
        self.history_list_view = ft.ListView(
            expand=True, 
            spacing=10, 
            padding=10
        )
        self.total_sum_text = ft.Text("오늘 총 합계: 0원", size=20, weight=ft.FontWeight.BOLD)

        # 페이지 레이아웃 구성
        self.setup_ui()

    def setup_ui(self):
        # 상단 입력 영역
        input_area = ft.Column(
            controls=[
                ft.Row(
                    [self.start_time_input, self.end_time_input],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Button(
                    "계산", 
                    on_click=self.handle_calculate,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # 하단 요약 영역
        summary_area = ft.Column(
            controls=[
                ft.Divider(),
                self.total_sum_text,
                ft.TextButton(
                    "오늘 기록 전체 삭제", 
                    on_click=self.clear_all_history,
                    style=ft.ButtonStyle(color=ft.Colors.RED_400)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        # 전체 레이아웃
        self.page.add(
            ft.Text("🅿️ 주차 요금 계산기", size=28, weight=ft.FontWeight.BOLD),
            input_area,
            ft.Text("주차 기록 목록", size=18, weight=ft.FontWeight.W_500),
            ft.Container(
                content=self.history_list_view,
                expand=True,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=10,
            ),
            summary_area
        )

    def clear_errors(self, e):
        self.start_time_input.error_text = None
        self.end_time_input.error_text = None
        self.page.update()

    def handle_calculate(self, e):
        start_val = self.start_time_input.value.strip()
        end_val = self.end_time_input.value.strip()

        try:
            # 1. 요금 계산 (calculator.py 로직 호출)
            fee = calculate_parking_fee(start_val, end_val)

            # 2. 성공 시 정보 생성
            # 시간 차 계산을 위한 보조 로직 (UI 표시용)
            fmt = "%H:%M"
            dt_start = datetime.strptime(start_val, fmt)
            dt_end = datetime.strptime(end_val, fmt)
            diff = dt_end - dt_start
            
            total_sec = int(diff.total_seconds())
            hours = total_sec // 3600
            minutes = (total_sec % 3600) // 60
            duration_str = f"{hours}시간 {minutes}분"

            # 3. 히스토리 추가
            self.counter += 1
            record = {
                'id': self.counter,
                'start': start_val,
                'end': end_val,
                'duration': duration_str,
                'fee': fee
            }
            self.history.append(record)
            
            # 4. UI 업데이트
            self.add_history_card(record)
            self.update_total_sum()
            
            # 입력창 초기화
            self.start_time_input.value = ""
            self.end_time_input.value = ""
            self.start_time_input.error_text = None
            self.end_time_input.error_text = None
            self.page.update()

        except ValueError as err:
            msg = str(err)
            # 에러 메시지에 따른 필드 피드백
            if msg == "모든 시간을 입력해주세요.":
                self.start_time_input.error_text = msg
                self.end_time_input.error_text = msg
            elif msg == "올바른 시각 형식(HH:MM)을 입력하세요.":
                self.start_time_input.error_text = msg
                self.end_time_input.error_text = msg
            elif msg == "유효한 시각을 입력하세요.":
                self.start_time_input.error_text = msg
                self.end_time_input.error_text = msg
            elif msg == "출차 시간은 입차 시간보다 뒤여야 합니다.":
                self.end_time_input.error_text = msg
            else:
                # 그 외 기타 에러는 SnackBar
                self.page.show_dialog(ft.SnackBar(ft.Text(msg)))
            
            self.page.update()

    def add_history_card(self, record):
        # 삭제 버튼 핸들러를 클로저로 생성하여 특정 ID 참조
        def delete_record(e):
            self.remove_record(record['id'])

        card = ft.Card(
            content=ft.Container(
                padding=15,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"{record['start']} ~ {record['end']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"{record['duration']}", size=12, color=ft.Colors.GREY_700),
                            ],
                            spacing=2
                        ),
                        ft.VerticalDivider(),
                        ft.Text(f"{record['fee']:,}원", size=16, weight=ft.FontWeight.BOLD, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED_400,
                            on_click=delete_record
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        )
        # ID를 카드로 저장하여 나중에 찾기 쉽게 함
        card.data = record['id']
        self.history_list_view.controls.append(card)

    def remove_record(self, record_id):
        # 리스트 데이터 삭제
        self.history = [r for r in self.history if r['id'] != record_id]
        
        # UI 리스트뷰에서 해당 카드 삭제
        for control in self.history_list_view.controls:
            if hasattr(control, 'data') and control.data == record_id:
                self.history_list_view.controls.remove(control)
                break
        
        self.update_total_sum()
        self.page.update()

    def clear_all_history(self, e):
        self.history = []
        self.history_list_view.controls.clear()
        self.update_total_sum()
        self.page.update()

    def update_total_sum(self):
        total = sum(item['fee'] for item in self.history)
        self.total_sum_text.value = f"오늘 총 합계: {total:,}원"

def main(page: ft.Page):
    ParkingCalculatorApp(page)

if __name__ == "__main__":
    ft.run(main)
