# 숫자 맞히기 스펙

## 1. 기술과 파일 구성

- Python 3.10 이상, Flet 1.0. 다른 패키지는 쓰지 않는다. 파이썬에 들어 있는 모듈(random 등)은 쓸 수 있다.
- `main.py`는 아래 뼈대를 그대로 가져와 넓혀서 만든다. `logic.py`는 처음부터 만든다.
- 뼈대에 나온 Flet 문법만 쓴다. 뼈대에 없는 Flet 클래스, 인자, 속성은 쓰지 않는다. 기억하고 있는 Flet 문법은 옛 버전의 것이므로 쓰지 않는다.
- 특히 다음은 Flet 1.0에 없으므로 쓰면 오류가 난다: `ft.app(...)`, `ft.colors`, `ft.alignment.center`, `ft.ElevatedButton`, `Button(text=...)`, `page.window_width`, `ft.UserControl`, `TextField(error_text=...)`

```python
# main.py
import flet as ft


def main(page: ft.Page):
    page.title = "예제"
    page.window.width = 360
    page.window.height = 440
    page.window.resizable = False

    value = ft.TextField(label="값", value="", width=150)
    unit = ft.Dropdown(label="단위", value="cm", width=120,
                       options=[ft.dropdown.Option("cm"), ft.dropdown.Option("m")])
    upper = ft.Checkbox(label="대문자 포함", value=True)
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    notice = ft.Text(value="", color=ft.Colors.RED)
    items = ft.ListView(expand=True, spacing=4)

    def on_run(e):
        notice.value = ""
        if not value.value.strip():
            notice.value = "값을 입력합니다"
        else:
            result.value = f"{value.value} {unit.value}, 대문자 {upper.value}"
            items.controls.append(ft.Row(controls=[
                ft.Text(value=result.value, expand=True),
                ft.Button(content="삭제", data=len(items.controls), on_click=on_delete),
            ]))
        page.update()

    def on_delete(e):
        items.controls.pop(e.control.data)     # 버튼을 만들 때 data에 넣어 둔 번호
        for i, row in enumerate(items.controls):
            row.controls[1].data = i
        page.update()

    page.add(
        ft.Row(controls=[value, unit]),
        upper,
        ft.Button(content="실행", on_click=on_run, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        result,
        notice,
        items,
    )


ft.run(main)
```

| 파일 | 내용 |
| --- | --- |
| `SPEC.md` | 스펙 |
| `logic.py` | 입력 검사, 판정, 게임 상태(`Game` 클래스). flet을 import하지 않는다 |
| `main.py` | 화면. 검사와 판정은 하지 않고 `logic.py`의 `Game`을 불러 속성을 화면에 옮기기만 한다 |
| `test_logic.py` | `logic.py`만 검사한다. `python test_logic.py`로 실행하면 통과 수와 실패 수를 출력한다 |

## 2. 동작 규칙

### 함수와 메서드

| 이름 | 입력 | 하는 일 / 반환 |
| --- | --- | --- |
| `parse_guess(text)` | 입력창 문자열 | 올바르면 정수를, 아니면 안내 문구(문자열)를 돌려준다 |
| `judge(guess, answer)` | 정수 두 개 | `"더 큽니다"`, `"더 작습니다"`, `"정답"` 중 하나를 돌려준다 |
| `Game.__init__(answer=None)` | 정수 또는 없음 | `answer`를 주면 그 값을 정답으로, 없으면 1~100에서 무작위로 정한다. 나머지 속성은 처음 값으로 둔다 |
| `Game.submit(text)` | 입력창 문자열 | 입력 한 번을 처리하고 속성을 바꾼다. 반환값은 없다 |
| `Game.new_game()` | 없음 | 정답을 1~100에서 무작위로 새로 정하고 `best`를 뺀 나머지 속성을 처음 값으로 되돌린다. 생성자에서 `answer`를 줬더라도 무작위로 정한다 |

### Game 속성

| 이름 | 타입 | 처음 값 | 뜻 |
| --- | --- | --- | --- |
| `answer` | int | 1~100 | 정답 |
| `result` | str | `""` | 판정 글자 |
| `notice` | str | `""` | 빨간 안내 문구 |
| `attempts` | int | `0` | 시도 횟수 |
| `history` | list[str] | `[]` | 기록. 시간순이고 새 기록은 끝에 붙는다 |
| `over` | bool | `False` | 정답을 맞혀 게임이 끝났으면 `True` |
| `best` | int 또는 None | `None` | 최고 기록. 지금까지 맞힌 게임 중 가장 적은 시도 횟수. 맞힌 게임이 없으면 `None`. `new_game()`에서도 지우지 않는다 (5절 추가 기능) |

### 입력 검사 (`parse_guess`)

1. 앞뒤 공백을 지운다.
2. 지운 결과가 빈 문자열이면 `"숫자를 입력하세요"`를 돌려준다.
3. 0~9 숫자로만 이루어지지 않았으면 `"1부터 100 사이의 정수를 입력하세요"`를 돌려준다. `abc`, `3.5`, `-5`, `+5`, `1_0`, 전각 숫자 `５０`이 여기에 해당한다.
4. 정수로 바꾼 값이 1 미만이거나 100 초과이면 `"1부터 100 사이의 정수를 입력하세요"`를 돌려준다.
5. 그 밖에는 정수로 바꾼 값을 돌려준다. `"05"`는 `5`다.

### 판정 (`judge`)

6. `answer`가 `guess`보다 크면 `"더 큽니다"`, 작으면 `"더 작습니다"`, 같으면 `"정답"`을 돌려준다.

### 입력 처리 (`Game.submit`)

아래 규칙은 위에서부터 차례로 보고, 처음 맞는 것 하나만 적용한다.

7. `over`가 `True`이면 아무 속성도 바꾸지 않는다.
8. `parse_guess`가 문구를 돌려주면 `notice`를 그 문구로 바꾼다. `result`, `attempts`, `history`는 그대로다.
9. 이미 `history`에 있는 숫자면 `notice`를 `"이미 입력한 숫자입니다"`로 바꾼다. `result`, `attempts`, `history`는 그대로다.
10. 판정이 `"더 큽니다"` 또는 `"더 작습니다"`이면 `attempts`를 1 늘리고, `result`를 판정으로, `notice`를 `""`로 바꾸고, `history` 끝에 `"숫자 (판정)"`을 붙인다. 숫자는 `parse_guess`가 돌려준 정수다. 예: `"30 (더 큽니다)"`
11. 판정이 `"정답"`이면 `attempts`를 1 늘리고, `result`를 `"정답! N번 만에 맞혔습니다"`(N은 늘린 뒤의 `attempts`)로, `notice`를 `""`로, `over`를 `True`로 바꾸고, `history` 끝에 `"숫자 (정답)"`을 붙인다. `best`가 `None`이거나 `attempts`보다 크면 `best`를 `attempts`로 바꾼다.

## 3. 화면

- 창 제목 `"숫자 맞히기"`, 크기 360 × 480, 크기 조절 불가
- 위에서 아래로 다음 순서로 놓는다.
  1. `Text`: `"1부터 100 사이의 숫자를 맞힙니다."`
  2. `Row`: `TextField`(label `"숫자"`, width 220)와 `Button`(`"확인"`, expand=True, height 44, bgcolor `ft.Colors.BLUE`, color `ft.Colors.WHITE`)
  3. `Text`: 판정 글자. `result`를 보여 준다. size 20, 굵게(`ft.FontWeight.BOLD`)
  4. `Text`: 안내 문구. `notice`를 보여 준다. color `ft.Colors.RED`
  5. `Text`: `"시도 횟수: N"`. N은 `attempts`. 처음에는 `"시도 횟수: 0"`
  6. `Text`: `"최고 기록: N번"`. N은 `best`. `best`가 `None`이면 `"최고 기록: -"` (5절 추가 기능)
  7. `ListView`(expand=True, spacing 4): `history`의 문자열 하나마다 `Text` 하나. 삭제 버튼은 없다
  8. `Row`: `Button`(`"새 게임"`). 인자는 확인 버튼과 같다. `Row` 안에 넣어야 가로로 채워진다(페이지에 바로 넣으면 세로로 늘어난다)
- 확인을 누르거나 입력창에서 엔터를 누르면 → `game.submit(입력창 값)`을 부른다 → 입력창을 비운다 → `game`의 속성을 3~7번 요소에 옮긴다 → `page.update()`
- 새 게임을 누르면 → `game.new_game()`을 부른다 → 입력창을 비운다 → `game`의 속성을 3~7번 요소에 옮긴다 → `page.update()`
- 정답 뒤에도 입력창과 확인 버튼은 그대로 둔다. 눌러도 7번 규칙에 따라 화면이 바뀌지 않는다(입력창만 비워진다).

## 4. 테스트

`python test_logic.py`로 실행하면 통과 수와 실패 수를 출력한다. 아래 표를 그대로 검사한다.

### 표 1: `parse_guess`와 `judge`

| 함수 | 입력 | 기대 결과 |
| --- | --- | --- |
| `parse_guess` | `"37"` | `37` |
| `parse_guess` | `" 37 "` | `37` |
| `parse_guess` | `"1"` | `1` |
| `parse_guess` | `"100"` | `100` |
| `parse_guess` | `"05"` | `5` |
| `parse_guess` | `""` | `"숫자를 입력하세요"` |
| `parse_guess` | `"   "` | `"숫자를 입력하세요"` |
| `parse_guess` | `"0"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"101"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"-5"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"+5"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"abc"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"3.5"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"1_0"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `parse_guess` | `"５０"` | `"1부터 100 사이의 정수를 입력하세요"` |
| `judge` | `37, 50` | `"더 큽니다"` |
| `judge` | `63, 50` | `"더 작습니다"` |
| `judge` | `50, 50` | `"정답"` |

### 표 2: `Game(answer=50)`에 차례로 넣은 뒤의 속성

한 게임 객체에 위에서부터 차례로 넣는다. 각 줄은 그 입력을 처리한 직후의 값이다.

| 순서 | 입력 | result | notice | attempts | history | over |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | (만든 직후) | `""` | `""` | 0 | `[]` | False |
| 1 | `submit("abc")` | `""` | `"1부터 100 사이의 정수를 입력하세요"` | 0 | `[]` | False |
| 2 | `submit("30")` | `"더 큽니다"` | `""` | 1 | `["30 (더 큽니다)"]` | False |
| 3 | `submit("30")` | `"더 큽니다"` | `"이미 입력한 숫자입니다"` | 1 | `["30 (더 큽니다)"]` | False |
| 4 | `submit("")` | `"더 큽니다"` | `"숫자를 입력하세요"` | 1 | `["30 (더 큽니다)"]` | False |
| 5 | `submit(" 70 ")` | `"더 작습니다"` | `""` | 2 | `["30 (더 큽니다)", "70 (더 작습니다)"]` | False |
| 6 | `submit("50")` | `"정답! 3번 만에 맞혔습니다"` | `""` | 3 | `["30 (더 큽니다)", "70 (더 작습니다)", "50 (정답)"]` | True |
| 7 | `submit("abc")` | `"정답! 3번 만에 맞혔습니다"` | `""` | 3 | (6과 같음) | True |
| 8 | `submit("10")` | `"정답! 3번 만에 맞혔습니다"` | `""` | 3 | (6과 같음) | True |
| 9 | `new_game()` | `""` | `""` | 0 | `[]` | False |

### 표 3: 정답

| 검사 | 기대 결과 |
| --- | --- |
| `Game(answer=50).answer` | `50` |
| `Game()`을 1000번 만들어 각각의 `answer` | 전부 1 이상 100 이하의 정수 |
| `Game()` 하나에 `new_game()`을 1000번 불러 매번의 `answer` | 전부 1 이상 100 이하의 정수 |

### 표 4: 최고 기록 (5절 추가 기능)

`Game(answer=50)` 하나로 차례로 진행한다. `new_game()` 뒤의 정답은 무작위이므로, 테스트에서는 `new_game()` 직후 `answer`를 직접 바꾼다.

| 순서 | 진행 | attempts | best |
| --- | --- | --- | --- |
| 0 | (만든 직후) | 0 | `None` |
| 1 | `submit("30")`, `submit("70")` | 2 | `None` |
| 2 | `submit("50")` (정답) | 3 | `3` |
| 3 | `new_game()` | 0 | `3` |
| 4 | `answer = 40`, `submit("10")`, `submit("20")`, `submit("30")`, `submit("40")` (정답) | 4 | `3` |
| 5 | `new_game()`, `answer = 60`, `submit("60")` (정답) | 1 | `1` |

## 5. 추가 기능: 최고 기록

요구사항에 없는 기능으로 최고 기록을 넣는다. 프로그램을 켜 둔 동안 가장 적은 시도 횟수로 맞힌 기록을 시도 횟수 아래에 보여 준다. 더 적은 횟수로 맞히면 바뀌고, 더 많으면 그대로다. 새 게임을 눌러도 지워지지 않는다. 파일에 저장하지 않으므로 프로그램을 끄면 사라진다. 관련 규칙은 2절 `best` 속성과 11번 규칙, 3절 6번 요소, 4절 표 4에 있다.

## 6. 추가 기능: 엔터로 확인

입력창에서 엔터를 누르면 확인 버튼을 누른 것과 똑같이 동작한다. 같은 함수(`on_check`)를 부르므로 동작 규칙은 바뀌지 않는다.

- 확인(버튼이든 엔터든) 뒤에는 포커스를 입력창으로 돌려, 마우스를 쓰지 않고 이어서 숫자를 칠 수 있게 한다.
- 뼈대에 없는 문법이지만 예외로 `TextField`의 `on_submit`과 `focus()` 두 가지만 쓴다. `focus()`는 async 함수라서 `on_check`를 `async def`로 만들고 `await value.focus()`로 부른다. 둘 다 Flet 1.0.0에 있는 것을 확인했다. 이 밖의 뼈대에 없는 문법은 여전히 쓰지 않는다.
- 화면 동작이라 `test_logic.py`로는 검사하지 않고, 실행해서 확인한다.
