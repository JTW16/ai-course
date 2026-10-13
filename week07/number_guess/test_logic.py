from logic import parse_guess, judge, Game

def test():
    passed = 0
    failed = 0

    # 표 1: parse_guess와 judge
    tests1 = [
        ("parse_guess", "37", 37),
        ("parse_guess", " 37 ", 37),
        ("parse_guess", "1", 1),
        ("parse_guess", "100", 100),
        ("parse_guess", "05", 5),
        ("parse_guess", "", "숫자를 입력하세요"),
        ("parse_guess", "   ", "숫자를 입력하세요"),
        ("parse_guess", "0", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "101", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "-5", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "+5", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "abc", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "3.5", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "1_0", "1부터 100 사이의 정수를 입력하세요"),
        ("parse_guess", "５０", "1부터 100 사이의 정수를 입력하세요"),
        ("judge", (37, 50), "더 큽니다"),
        ("judge", (63, 50), "더 작습니다"),
        ("judge", (50, 50), "정답"),
    ]

    for name, inp, expected in tests1:
        if name == "parse_guess":
            actual = parse_guess(inp)
        else:
            actual = judge(*inp)
        
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: {name}({inp}) | Expected: {repr(expected)}, Actual: {repr(actual)}")

    # 표 2: Game(answer=50)
    game = Game(answer=50)
    # 0 (만든 직후)
    if (game.result == "" and game.notice == "" and game.attempts == 0 and 
        game.history == [] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(0) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 1 submit("abc")
    game.submit("abc")
    if (game.result == "" and game.notice == "1부터 100 사이의 정수를 입력하세요" and 
        game.attempts == 0 and game.history == [] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(1) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 2 submit("30")
    game.submit("30")
    if (game.result == "더 큽니다" and game.notice == "" and game.attempts == 1 and 
        game.history == ["30 (더 큽니다)"] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(2) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 3 submit("30")
    game.submit("30")
    if (game.result == "더 큽니다" and game.notice == "이미 입력한 숫자입니다" and 
        game.attempts == 1 and game.history == ["30 (더 큽니다)"] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(3) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 4 submit("")
    game.submit("")
    if (game.result == "더 큽니다" and game.notice == "숫자를 입력하세요" and 
        game.attempts == 1 and game.history == ["30 (더 큽니다)"] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(4) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 5 submit(" 70 ")
    game.submit(" 70 ")
    if (game.result == "더 작습니다" and game.notice == "" and game.attempts == 2 and 
        game.history == ["30 (더 큽니다)", "70 (더 작습니다)"] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(5) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 6 submit("50")
    game.submit("50")
    if (game.result == "정답! 3번 만에 맞혔습니다" and game.notice == "" and game.attempts == 3 and 
        game.history == ["30 (더 큽니다)", "70 (더 작습니다)", "50 (정답)"] and game.over == True):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(6) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 7 submit("abc")
    game.submit("abc")
    if (game.result == "정답! 3번 만에 맞혔습니다" and game.notice == "" and game.attempts == 3 and 
        game.history == ["30 (더 큽니다)", "70 (더 작습니다)", "50 (정답)"] and game.over == True):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(7) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 8 submit("10")
    game.submit("10")
    if (game.result == "정답! 3번 만에 맞혔습니다" and game.notice == "" and game.attempts == 3 and 
        game.history == ["30 (더 큽니다)", "70 (더 작습니다)", "50 (정답)"] and game.over == True):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(8) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 9 new_game()
    game.new_game()
    if (game.result == "" and game.notice == "" and game.attempts == 0 and 
        game.history == [] and game.over == False):
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(9) | Result: {game.result}, Notice: {game.notice}, Attempts: {game.attempts}, History: {game.history}, Over: {game.over}")

    # 표 3: 정답
    # Game(answer=50).answer
    if Game(answer=50).answer == 50:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: Game(answer=50).answer | Expected: 50, Actual: {Game(answer=50).answer}")

    # Game()를 1000번 만들어 각각의 answer
    all_answers_ok = True
    for _ in range(1000):
        g = Game()
        if not (1 <= g.answer <= 100):
            all_answers_ok = False
            break
    if all_answers_ok:
        passed += 1
    else:
        failed += 1
        print("FAIL: Game() 1000 times answer range")

    # Game() 하나에 new_game()을 1000번 불러 매번의 answer
    g = Game()
    all_new_answers_ok = True
    for _ in range(1000):
        g.new_game()
        if not (1 <= g.answer <= 100):
            all_new_answers_ok = False
            break
    if all_new_answers_ok:
        passed += 1
    else:
        failed += 1
        print("FAIL: Game().new_game() 1000 times answer range")

    # 표 4: 최고 기록 (5절 추가 기능)
    g = Game(answer=50)

    def check_best(step, attempts, best):
        nonlocal passed, failed
        if g.attempts == attempts and g.best == best:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: best({step}) | Expected: attempts={attempts}, best={best} | "
                  f"Actual: attempts={g.attempts}, best={g.best}")

    # 0 (만든 직후)
    check_best(0, 0, None)

    # 1 submit("30"), submit("70")
    g.submit("30")
    g.submit("70")
    check_best(1, 2, None)

    # 2 submit("50") (정답)
    g.submit("50")
    check_best(2, 3, 3)

    # 3 new_game()
    g.new_game()
    check_best(3, 0, 3)

    # 4 answer = 40, 4번 만에 정답
    g.answer = 40
    for text in ["10", "20", "30", "40"]:
        g.submit(text)
    check_best(4, 4, 3)

    # 5 new_game(), answer = 60, 1번 만에 정답
    g.new_game()
    g.answer = 60
    g.submit("60")
    check_best(5, 1, 1)

    print(f"통과 {passed}개, 실패 {failed}개")

if __name__ == "__main__":
    test()