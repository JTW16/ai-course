import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    total_amount = None
    people_count = None
    result = None
    items = None

    if request.method == 'POST':
        image_file = request.files.get('receipt_image')
        
        if image_file:
            try:
                image_bytes = image_file.read()
                prompt = "영수증에서 항목 이름과 금액을 추출해서 JSON 형식으로만 답해줘. 형식은 [{'item': '항목명', 'price': 금액}, ...] 와 같아야 해. 다른 설명은 하지 마."
                response_text = ask(prompt, image_bytes=image_bytes)
                items = parse_json(response_text)
                
                if items:
                    total_amount = sum(item.get('price', 0) for item in items)
                else:
                    result = "읽지 못했습니다"
                    items = None
            except Exception as e:
                print(f"Error: {e}")
                result = "읽지 못했습니다"
                items = None
        else:
            try:
                total_amount = int(request.form.get('total_amount', 0))
            except ValueError:
                result = '올바른 숫자를 입력해주세요.'

        people_count_str = request.form.get('people_count', 0)
        try:
            people_count = int(people_count_str)
        except ValueError:
            people_count = 0

        if total_amount is not None and people_count is not None:
            if people_count > 0:
                result = total_amount / people_count
                result = round(result, 2)
            elif total_amount != 0:
                result = '인원수는 0명보다 커야 합니다.'
            elif result is None:
                result = 0
        elif result is None and items is None:
            # 이미 에러 메시지가 setting 되었을 경우 (이미 result에 값이 있음)
            pass

    return render_template('index.html', total_amount=total_amount, people_count=people_count, result=result, items=items)

if __name__ == '__main__':
    app.run(debug=True)
