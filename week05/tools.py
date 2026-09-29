import ollama, json, datetime

def get_time():
    """지금 시각을 돌려준다"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def calc(expression: str):
    """수식 문자열을 계산한다. 예: '17 * 24'"""
    return str(eval(expression, {"__builtins__": {}}))

def read_file(path: str):
    """파일 경로를 받아 그 파일의 내용 전체를 돌려준다. 예: 'chat.py'"""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"오류: {e}"

functions = {"get_time": get_time, "calc": calc, "read_file": read_file}

messages = [{"role": "user", "content": "지금 몇 시야? 그리고 17 곱하기 24는? chat.py 파일의 첫 줄이 뭐야?"}]
for step in range(5):
    r = ollama.chat(model="qwen3:8b", think=False, messages=messages, tools=[get_time, calc, read_file])
    messages.append(r.message)
    if not r.message.tool_calls:                    # 도구 호출이 없으면 최종 답
        print("답:", r.message.content)
        break
    for call in r.message.tool_calls:               # 모델이 요청한 도구를 실제로 실행
        name, args = call.function.name, call.function.arguments
        result = functions[name](**args)
        print(f"  도구 호출: {name}({args}) -> {result}")
        messages.append({"role": "tool", "content": result, "tool_name": name})