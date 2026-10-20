from datetime import datetime, timedelta

def calculate_parking_fee(start_time_str: str, end_time_str: str) -> int:
    """
    주차 요금을 계산합니다.
    
    Args:
        start_time_str (str): 입차 시간 (HH:MM)
        end_time_str (str): 출차 시간 (HH:MM)
        
    Returns:
        int: 계산된 주차 요금 (최대 20,000원)
        
    Raises:
        ValueError: 입력 형식이 잘못되었거나 범위를 벗어난 경우
    """
    
    # 1. 빈 입력 검사
    if not start_time_str or not end_time_str:
        raise ValueError("모든 시간을 입력해주세요.")

    # 2. 형식 및 범위 검사
    try:
        # HH:MM 형식을 검사하기 위해 datetime으로 파싱
        start_time = datetime.strptime(start_time_str, "%H:%M")
        end_time = datetime.strptime(end_time_str, "%H:%M")
    except ValueError:
        # 콜론(:)이 없으면 형식 오류, 있으면 값 범위 오류(예: 25:00)로 판단
        if ":" not in start_time_str or ":" not in end_time_str:
            raise ValueError("올바른 시각 형식(HH:MM)을 입력하세요.")
        else:
            raise ValueError("유효한 시각을 입력하세요.")

    # 3. 주차 시간 검증 및 계산
    # 테스트 코드의 요구사항(test_logical_error_time_order)에 따라 
    # 출차 시간이 입차 시간과 같거나 빠르면 에러를 발생시킵니다.
    if end_time <= start_time:
        raise ValueError("출차 시간은 입차 시간보다 뒤여야 합니다.")
    
    # 실제 주차 소요 시간 (분 단위)
    duration = end_time - start_time
    total_minutes = int(duration.total_seconds() // 60)

    # 4. 요금 산정
    # - 최초 30분 무료
    # - 30분 초과 시 10분당 500원 (10분 미만 올림)
    fee = 0
    if total_minutes > 30:
        extra_minutes = total_minutes - 30
        # 올림 처리: (잔여분 + 9) // 10
        units = (extra_minutes + 9) // 10
        fee = units * 500

    # 5. 최대 요금 제한 (20,000원)
    if fee > 20000:
        fee = 20000
        
    return fee
