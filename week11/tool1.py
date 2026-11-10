import json, subprocess, sys
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
tools = [{"type": "function", "function": {
    "name": "run_python",
    "description": "파이썬 코드를 실행하고 출력을 돌려준다.",
    "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}}]

messages = [{"role": "system", "content": "날짜, 시간, 계산은 기억으로 답하지 않고 run_python으로 확인한다."},
            {"role": "user", "content": "오늘 날짜를 YYYYMMDD 꼴로 알려줘."}]
r = client.chat.completions.create(model="gemma4", messages=messages, tools=tools)
m = r.choices[0].message
print("content:", m.content)
print("tool_calls:", m.tool_calls)
if not m.tool_calls:
    sys.exit("도구를 부르지 않았습니다. 다시 실행해 봅니다.")

tc = m.tool_calls[0]
code = json.loads(tc.function.arguments)["code"]
print("--- 모델이 쓴 코드\n" + code)
out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout
print("--- 실행 결과:", out.strip())

messages += [m, {"role": "tool", "tool_call_id": tc.id, "content": out}]
r = client.chat.completions.create(model="gemma4", messages=messages, tools=tools)
print("--- 최종 답:", r.choices[0].message.content)