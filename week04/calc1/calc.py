def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! 0으로 나눌 수 없습니다."
    return x / y

def calculator():
    print("=== 파이썬 심플 계산기 ===")
    print("사용 가능한 연산: +, -, *, /")
    print("종료하려면 'q'를 입력하세요.")
    print("============================")

    while True:
        # 1. 연산자 입력 받기
        operator = input("\n연산자를 입력하세요 (+, -, *, /) 또는 'q' (종료): ").strip()

        if operator.lower() == 'q':
            print("계산기를 종료합니다. 이용해 주셔서 감사합니다!")
            break

        if operator not in ['+', '-', '*', '/']:
            print("잘못된 연산자입니다. 다시 입력해주세요.")
            continue

        # 2. 숫자 입력 받기
        try:
            num1 = float(input("첫 번째 숫자를 입력하세요: "))
            num2 = float(input("두 번째 숫자를 입력하세요: "))
        except ValueError:
            print("잘못된 입력입니다. 숫자만 입력해 주세요.")
            continue

        # 3. 연산 수행 및 결과 출력
        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)

        print(f"\n[결과] {num1} {operator} {num2} = {result}")
        print("-" * 30)

if __name__ == "__main__":
    calculator()
