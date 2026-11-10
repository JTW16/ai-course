import json, os, subprocess, sys
from openai import OpenAI

MODEL, WORK, TASK = sys.argv[1], sys.argv[2], open(sys.argv[3], encoding="utf-8").read()
os.makedirs(WORK, exist_ok=True)
SKILL_DIR = "skills"

if MODEL == "gemma4":
    client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="none")


def frontmatter(path):
    """SKILL.md 맨 위 --- 사이의 key: value 줄을 딕셔너리로 만든다"""
    head = open(path, encoding="utf-8").read().split("---")[1]
    return dict(line.split(":", 1) for line in head.strip().splitlines() if ":" in line)


skills = {}
if os.path.isdir(SKILL_DIR):
    for name in sorted(os.listdir(SKILL_DIR)):
        p = os.path.join(SKILL_DIR, name, "SKILL.md")
        if os.path.exists(p):
            skills[name] = frontmatter(p)["description"].strip()


def run_python(code):
    r = subprocess.run([sys.executable, "-c", code], cwd=WORK, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=60,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return (r.stdout + r.stderr)[-2000:] or "(출력 없음)"


def read_skill(name):
    p = os.path.join(SKILL_DIR, name, "SKILL.md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else f"{name}: 없는 스킬"


tools = [
    {"type": "function", "function": {
        "name": "run_python",
        "description": "파이썬 코드를 실행하고 출력을 돌려준다. python-docx, openpyxl이 설치되어 있다.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "read_skill",
        "description": "스킬의 설명서 SKILL.md 전체를 읽는다.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}}},
]
catalog = "\n".join(f"- {k}: {v}" for k, v in skills.items()) or "(없음)"
system = f"""너는 파일을 만드는 비서다. 코드가 필요하면 run_python으로 실행한다.
사용할 수 있는 스킬:
{catalog}
할 일에 맞는 스킬이 있으면 먼저 read_skill로 설명서를 읽고 그 규칙대로 한다. 맞는 스킬이 없으면 읽지 않는다.
일이 끝나면 만든 파일 이름을 한 줄로 말한다."""

messages = [{"role": "system", "content": system}, {"role": "user", "content": TASK}]
for step in range(8):
    r = client.chat.completions.create(model=MODEL, messages=messages, tools=tools, temperature=0.7)
    m = r.choices[0].message
    messages.append(m)
    if not m.tool_calls:
        print("답:", (m.content or "").strip())
        break
    for tc in m.tool_calls:
        args = json.loads(tc.function.arguments)
        if tc.function.name == "run_python":
            out = run_python(args["code"])
        else:
            out = read_skill(args["name"])
        print(f"[{step}] {tc.function.name} -> {out.strip()[:80]!r}")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": out})