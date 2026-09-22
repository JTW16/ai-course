# 계산기 스펙

## 1. 개요

Windows와 macOS에서 똑같이 실행되는 데스크톱 계산기를 만든다. 책상 위의 일반 계산기처럼 동작한다.

## 2. 기술

- Python 3.10 이상, Flet 1.0 (`python -m pip install "flet[all]"`). 다른 패키지는 쓰지 않는다.
- Flet은 1.0에서 문법이 크게 바뀌었다. 아래 뼈대 코드는 Flet 1.0에서 동작을 확인한 것이다. `main.py`는 이 뼈대를 그대로 가져와 넓혀서 만든다.
- 뼈대에 나온 Flet 문법만 쓴다. 뼈대에 없는 Flet 클래스, 인자, 속성은 쓰지 않는다. 기억하고 있는 Flet 문법은 옛 버전의 것이므로 쓰지 않는다.
- 특히 다음은 Flet 1.0에 없으므로 쓰면 오류가 난다: `ft.app(...)`, `ft.colors`, `ft.alignment.center`, `ft.ElevatedButton`, `Button(text=...)`, `page.window_width`, `ft.UserControl`

```python
import flet as ft


def main(page: ft.Page):
    page.title = "예제"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    display = ft.Text(value="0", size=40, text_align=ft.TextAlign.RIGHT)

    def on_button(e):
        display.value = e.control.data      # 버튼을 만들 때 data에 넣어 둔 값
        page.update()

    def on_key(e: ft.KeyboardEvent):
        display.value = e.key               # "7", "Enter", "Backspace", "Escape" 등
        page.update()

    page.on_keyboard_event = on_key

    def make_button(label, key, bgcolor):
        return ft.Button(content=label, data=key, on_click=on_button, expand=1, height=60,
                         bgcolor=bgcolor, color=ft.Colors.WHITE)

    page.add(
        ft.Container(content=display, alignment=ft.Alignment.CENTER_RIGHT, padding=10, height=90),
        ft.Row(controls=[make_button("7", "7", ft.Colors.GREY_800),
                         make_button("÷", "/", ft.Colors.ORANGE)]),
    )


ft.run(main)
```

## 3. 파일 구성

| 파일 | 내용 |
| --- | --- |
| `calc.py` | 계산 로직. `Calculator` 클래스 하나. flet을 import하지 않는다 |
| `main.py` | 화면. `calc.py`의 `Calculator`를 가져다 쓴다. 계산을 직접 하지 않는다 |
| `test_calc.py` | `calc.py`만 검사하는 테스트. `python test_calc.py`로 실행한다 |
| `README.md` | 설치와 실행 방법 |

## 4. 계산 로직 (`calc.py`)

`Calculator` 클래스는 메소드 `press(key: str)` 하나로 모든 입력을 받고, 속성 `display`(문자열)로 화면에 보일 값을 돌려준다.

`press`가 받는 키: `"0"`~`"9"`, `"."`, `"+"`, `"-"`, `"*"`, `"/"`, `"="`, `"C"`(전체 지움), `"BS"`(한 글자 지움), `"+/-"`(부호 바꿈), `"%"`(현재 값을 100으로 나눔)

규칙

1. 시작할 때와 `C`를 누른 뒤의 `display`는 `"0"`이다.
2. 연산자 우선순위는 없다. 누른 순서대로 바로 계산한다. `2 + 3 * 4 =` 은 `20`이다.
3. 연산자를 연달아 누르면 마지막에 누른 것으로 바뀐다. `5 + - 3 =` 은 `2`이다.
4. 소수점은 한 수에 한 번만 들어간다. 두 번째부터는 무시한다. 맨 처음에 `.`을 누르면 `"0."`이 된다.
5. 앞에 붙는 0은 넣지 않는다. `0 0 7` 은 `"7"`이다.
6. 결과는 소수 10자리에서 반올림하고, 끝의 0과 필요 없는 소수점은 떼어 낸다. `0.1 + 0.2 =` 은 `"0.3"`, `6 / 3 =` 은 `"2"`이다.
7. 0으로 나누면 `display`는 `"0으로 나눌 수 없습니다"`가 된다. 이 상태에서는 `C`만 받고 나머지 키는 무시한다.
8. `=`을 누른 직후에 숫자를 누르면 새 계산을 시작한다. 연산자를 누르면 결과에 이어서 계산한다.
9. `BS`는 입력 중인 수의 마지막 글자를 지운다. 한 글자만 남았을 때 누르면 `"0"`이 된다. 결과가 표시된 상태에서는 아무 일도 하지 않는다.
10. `=`을 연달아 눌러도 같은 연산을 반복하지 않는다. 결과가 그대로 유지된다.
11. 입력하는 수는 소수점과 부호를 빼고 12자리까지만 받는다. 넘는 입력은 무시한다.

## 5. 화면 (`main.py`)

- 창 제목 "계산기", 크기 340 × 520, 크기 조절 불가
- 위쪽에 표시창. 오른쪽 정렬, 글자 크기 40. `display` 값을 그대로 보여 준다
- 아래에 버튼 5줄 × 4칸

| | | | |
| --- | --- | --- | --- |
| C | +/- | % | ÷ |
| 7 | 8 | 9 | × |
| 4 | 5 | 6 | − |
| 1 | 2 | 3 | + |
| 0 | . | ⌫ | = |

- 화면에 보이는 `÷ × − ⌫`는 `press`에 `"/" "*" "-" "BS"`로 넘긴다
- 버튼 색은 아래 세 가지만 쓴다. 다른 색 이름은 쓰지 않는다. 글자색은 전부 `ft.Colors.WHITE`
  - 숫자와 `.` `⌫`: `ft.Colors.GREY_800`
  - 연산자 `÷ × − +`와 `=`: `ft.Colors.ORANGE`
  - `C` `+/-` `%`: `ft.Colors.GREY_600`
- 키보드 입력: 숫자, `.`, `+ - * /`, Enter(=), Backspace(BS), Escape(C)

## 6. 테스트 (`test_calc.py`)

아래 표를 그대로 검사한다. 입력은 공백으로 나눈 키의 순서다. 전부 통과하면 `모든 테스트 통과 (N개)`를 출력하고, 하나라도 틀리면 어떤 입력에서 기대값과 실제값이 무엇이었는지 출력한다.

| 입력 | 기대하는 display |
| --- | --- |
| (아무것도 안 누름) | `0` |
| `1 2 + 3 =` | `15` |
| `2 + 3 * 4 =` | `20` |
| `5 + - 3 =` | `2` |
| `0 . 1 + 0 . 2 =` | `0.3` |
| `6 / 3 =` | `2` |
| `7 / 2 =` | `3.5` |
| `5 / 0 =` | `0으로 나눌 수 없습니다` |
| `5 / 0 = 7` | `0으로 나눌 수 없습니다` |
| `5 / 0 = C` | `0` |
| `1 . . 5` | `1.5` |
| `.` | `0.` |
| `0 0 7` | `7` |
| `1 2 3 BS` | `12` |
| `5 BS` | `0` |
| `9 +/-` | `-9` |
| `5 0 %` | `0.5` |
| `2 + 3 = 4` | `4` |
| `2 + 3 = + 4 =` | `9` |
| `2 + 3 = =` | `5` |

## 7. 완료 전 점검

완료를 보고하기 전에 다음을 차례로 확인한다.

1. 3절의 파일 네 개(`calc.py`, `main.py`, `test_calc.py`, `README.md`)가 전부 있는가
2. `python test_calc.py`가 `모든 테스트 통과 (20개)`를 출력하는가
3. `main.py`에 2절에서 금지한 옛 문법이 없는가. 뼈대에 없는 Flet 문법을 쓰지 않았는가

## 8. 하지 않는 것

괄호, 제곱근, 메모리(M+), 계산 기록, 공학용 기능은 만들지 않는다. 스펙에 없는 기능은 넣지 않는다.