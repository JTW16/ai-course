import json
import os
from datetime import datetime

TODO_FILE = 'todo.json'

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos):
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")

from datetime import datetime

def add_todo(todos):
    """새로운 할 일을 추가합니다 (마감일 포함)."""
    task = input("할 일을 입력하세요: ").strip()
    if not task:
        print("⚠️ 할 일이 비어있습니다. 다시 시도해주세요.")
        return

    deadline_str = input("마감일을 입력하세요 (예: YYYY-MM-DD, 없으면 엔터): ").strip()
    
    deadline = None
    if deadline_str:
        try:
            # 입력된 날짜 형식을 검증하고 datetime 객체로 변환
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("⚠️ 날짜 형식이 잘못되었습니다 (YYYY-MM-DD). 마감일 없이 저장합니다.")
            deadline = None

    todos.append({"task": task, "done": False, "deadline": deadline})
    save_todos(todos)
    print("✅ 할 일이 추가되었습니다.")

def view_todos(todos):
    if not todos:
def save_todos(todos):
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")

def add_todo(todos):
    """새로운 할 일을 추가합니다 (마감일 포함)."""
    task = input("할 일을 입력하세요: ").strip()
    if not task:
        print("⚠️ 할 일이 비어있습니다. 다시 시도해주세요.")
        return

    deadline_str = input("마감일을 입력하세요 (YYYY-MM-DD, 없으면 엔터): ").strip()
    deadline = None
    if deadline_str:
        try:
            # 입력 형식을 검증하고 표준 형식으로 저장
            datetime.strptime(deadline_str, "%Y-%m-%d")
            deadline = deadline_str
        except ValueError:
            print("⚠️ 날짜 형식이 잘못되었습니다 (YYYY-MM-DD). 마감일 없이 저장합니다.")
            deadline = None

    todos.append({"task": task, "done": False, "deadline": deadline})
    save_todos(todos)
    print("✅ 할 일이 추가되었습니다.")

def get_sorted_todos(todos):
    """마감일 순으로 정렬된 할 일 목록을 반환합니다."""
    # 마감일이 없는 경우 '9999-12-31'로 처리하여 가장 뒤로 보냄
    return sorted(
        todos, 
        key=lambda x: x['deadline'] if x['deadline'] else '9999-12-31'
    )

def view_todos(todos):
    """정렬된 할 일 목록을 출력합니다."""
    if not todos:
        print("\n📋 현재 할 일 목록이 비어 있습니다.")
        return False

    sorted_todos = get_sorted_todos(todos)
    print("\n--- 할 일 목록 (마감일 순) ---")
    for i, todo in enumerate(sorted_todos, 1):
        status = "✔" if todo["done"] else " "
        deadline_display = f" | 마감: {todo['deadline']}" if todo['deadline'] else ""
        print(f"{i}. [{status}] {todo['task']}{deadline_display}")
    print("------------------")
    return True

def mark_done(todos):
    """할 일을 완료 상태로 표시합니다."""
    sorted_todos = get_sorted_todos(todos)
    if not view_todos(todos) or not sorted_todos:
        return

    try:
        choice = int(input("완료 처리할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_todos):
            # 정렬된 리스트에서 선택된 항목을 찾아 원본 리스트에서 수정
            target_task = sorted_todos[choice - 1]['task']
            # task 이름이 중복될 수 있으므로 deadline까지 체크하여 정확한 객체 찾기
            for todo in todos:
                if todo['task'] == target_task and todo['deadline'] == sorted_todos[choice-1]['deadline']:
                    todo['done'] = True
                    break
            save_todos(todos)
            print("✅ 완료 표시되었습니다.")
        else:
            print("⚠️ 잘못된 번호입니다.")
    except ValueError:
        print("⚠️ 숫자를 입력해주세요.")

def delete_todo(todos):
    """할 일을 삭제합니다."""
    sorted_todos = get_sorted_todos(todos)
    if not view_todos(todos) or not sorted_todos:
        return

    try:
        choice = int(input("삭제할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_todos):
            target_task = sorted_todos[choice - 1]['task']
            target_deadline = sorted_todos[choice - 1]['deadline']
            
            # 원본 리스트에서 해당 항목 삭제
            for i, todo in enumerate(todos):
                if todo['task'] == target_task and todo['deadline'] == target_deadline:
                    removed = todos.pop(i)
                    save_todos(todos)
                    print(f"🗑️ '{removed['task']}' 항목이 삭제되었습니다.")
                    break
        else:
            print("⚠️ 잘못된 번호입니다.")
    except ValueError:
        print("⚠️ 숫자를 입력해주세요.")

def main():
    """메인 루프를 실행합니다."""
    while True:
        todos = load_todos()
        print("\n--- 📝 TODO 앱 ---")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        print("------------------")
        
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == '1':
            add_todo(todos)
        elif choice == '2':
            view_todos(todos)
        elif choice == '3':
            mark_done(todos)
        elif choice == '4':
            delete_todo(todos)
        elif choice == '5':
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("⚠️ 잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()