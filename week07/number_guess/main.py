# main.py
import flet as ft

from logic import Game


def main(page: ft.Page):
    page.title = "숫자 맞히기"
    page.window.width = 360
    page.window.height = 480
    page.window.resizable = False

    game = Game()

    guide = ft.Text(value="1부터 100 사이의 숫자를 맞힙니다.")
    value = ft.TextField(label="숫자", value="", width=220)
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    notice = ft.Text(value="", color=ft.Colors.RED)
    attempts = ft.Text(value="")
    best = ft.Text(value="")
    items = ft.ListView(expand=True, spacing=4)

    def refresh():
        # 판정과 계산은 하지 않고 game의 속성을 화면에 옮기기만 한다
        result.value = game.result
        notice.value = game.notice
        attempts.value = f"시도 횟수: {game.attempts}"
        best.value = "최고 기록: -" if game.best is None else f"최고 기록: {game.best}번"
        items.controls = [ft.Text(value=entry) for entry in game.history]
        page.update()

    async def on_check(e):
        game.submit(value.value)
        value.value = ""
        refresh()
        await value.focus()        # 엔터 뒤에도 바로 다음 숫자를 칠 수 있게 입력창으로 포커스를 돌린다

    value.on_submit = on_check     # 입력창에서 엔터를 눌러도 확인과 같게 동작 (5절 추가 기능)

    def on_new_game(e):
        game.new_game()
        value.value = ""
        refresh()

    page.add(
        guide,
        ft.Row(controls=[
            value,
            ft.Button(content="확인", on_click=on_check, expand=True, height=44,
                      bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        ]),
        result,
        notice,
        attempts,
        best,
        items,
        # Row 안에 넣어야 expand가 가로 방향으로 적용된다
        ft.Row(controls=[
            ft.Button(content="새 게임", on_click=on_new_game, expand=True, height=44,
                      bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        ]),
    )
    refresh()


ft.run(main)
