import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

# 4. 키 설정
SECRET_KEY = os.environ.get('TOSS_SECRET_KEY', 'test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6')

def get_auth_header():
    # Secret Key 뒤에 ":"를 붙여 Base64로 인코딩
    auth_str = f"{SECRET_KEY}:"
    encoded_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {encoded_auth}"}

# 3. 동작 - GET /
@app.route('/')
def index():
    return render_template('index.html')

# 3. 동작 - GET /success
@app.route('/success')
def success():
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')

    # 19. 금액 검증
    if int(amount) != 1000:
        return f"Invalid amount: {amount}. Expected 1000.", 400

    # 결제 승인 API 호출
    if not payment_key:
        return "Error: paymentKey is missing", 400

    # API URL: https://api.tosspayments.com/v1/payments/{paymentKey}/confirm
    url = f"https://api.tosspayments.com/v1/payments/{payment_key}/confirm"
    payload = {
        "orderId": order_id,
        "amount": amount
    }
    headers = get_auth_header()

    print(f"[DEBUG] Calling API URL: {url}")
    print(f"[DEBUG] Payload: {payload}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"[DEBUG] Response Status: {response.status_code}")
        print(f"[DEBUG] Response Body: {response.text}")
        
        res_data = response.json()

        if response.status_code == 200:
            # 성공 시 res_data를 템플릿으로 전달
            return render_template('success.html', data=res_data)
        else:
            # 실패 시 에러 정보 전달
            return render_template('fail.html', error=res_data), response.status_code
            
    except Exception as e:
        print(f"[DEBUG] Error occurred: {str(e)}")
        return str(e), 500

# 3. 동작 - GET /fail
@app.route('/fail')
def fail():
    code = request.args.get('code')
    message = request.args.get('message')
    return render_template('fail.html', error={'code': code, 'message': message})

if __name__ == '__main__':
    app.run(debug=True, port=5000)