# 결제 승인 서버 스펙

## 1. 기술
- Python Flask, requests.
- 결제 승인 방법은 토스페이먼츠 MCP로 "결제 승인" 문서를 검색해서 그대로 따른다.

## 2. 파일
| 파일 | 내용 |
| --- | --- |
| `app.py` | Flask 서버. 라우트 세 개 |
| `templates/index.html` | 지금 있는 index.html을 옮긴다. successUrl은 `/success`, failUrl은 `/fail`로 바꾼다 |
| `templates/success.html` | 승인 결과 표시 |
| `templates/fail.html` | 실패 표시 |

## 3. 동작
- `GET /` : index.html
- `GET /success` : 쿼리의 paymentKey, orderId, amount를 받아 서버에서 결제 승인 API를 호출한다. 응답 JSON의 status, orderName, totalAmount, method, approvedAt을 표에 보여 주고, 원본 JSON도 아래에 그대로 보여 준다. 실패하면 HTTP 상태와 code, message를 보여 준다
- `GET /fail` : 쿼리의 code, message를 보여 준다
- 승인 API를 부르기 전에 쿼리의 amount가 1000과 같은지 확인한다. 다르면 승인하지 않고 오류를 보여 준다

## 4. 키
- 시크릿 키는 환경 변수 TOSS_SECRET_KEY에서 읽는다. 없으면 test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6을 기본값으로 쓴다. 시크릿 키를 브라우저로 보내는 코드는 쓰지 않는다

## 5. 하지 않는 것
데이터베이스, 로그인, 취소, 웹훅은 만들지 않는다.