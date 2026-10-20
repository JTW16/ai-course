import unittest
from calculator import calculate_parking_fee

class TestParkingCalculator(unittest.TestCase):
    """
    주차 요금 계산기 로직 검증 테스트 클래스
    """

    # --- 4.1 정상 케이스 (경계값 포함) ---

    def test_free_period_boundary(self):
        # 30분 주차 (예: 09:00 ~ 09:30) -> 요금: 0원
        self.assertEqual(calculate_parking_fee("09:00", "09:30"), 0)
        # 31분 주차 (예: 09:00 ~ 09:31) -> 요금: 500원
        self.assertEqual(calculate_parking_fee("09:00", "09:31"), 500)

    def test_ten_minute_unit_boundary(self):
        # 40분 주차 (예: 09:00 ~ 09:40) -> 요금: 500원
        self.assertEqual(calculate_parking_fee("09:00", "09:40"), 500)
        # 41분 주차 (예: 09:00 ~ 09:41) -> 요금: 1,000원
        self.assertEqual(calculate_parking_fee("09:00", "09:41"), 1000)

    def test_maximum_fee_boundary(self):
        # 10시간 주차 (예: 09:00 ~ 19:00) -> 요금: 20,000원 (계산상 상한선 근처)
        self.assertEqual(calculate_parking_fee("09:00", "19:00"), 20000)
        
        # 입차와 출차가 같은 경우, test_logical_error_time_order의 요구사항에 따라
        # 에러가 발생하는 것을 확인 (테스트 코드 간 충돌 해결)
        with self.assertRaisesRegex(ValueError, "출차 시간은 입차 시간보다 뒤여야 합니다."):
            calculate_parking_fee("09:00", "09:00")

    # --- 4.2 에러 케이스 ---

    def test_empty_input(self):
        # 빈 칸 입력 시 -> "모든 시간을 입력해주세요."
        with self.assertRaisesRegex(ValueError, "모든 시간을 입력해주세요."):
            calculate_parking_fee("", "09:30")
        with self.assertRaisesRegex(ValueError, "모든 시간을 입력해주세요."):
            calculate_parking_fee("09:00", "")

    def test_invalid_format(self):
        # abc:def 입력 시 -> "올바른 시각 형식(HH:MM)을 입력하세요."
        with self.assertRaisesRegex(ValueError, r"올바른 시각 형식\(HH:MM\)을 입력하세요."):
            calculate_parking_fee("abc", "def")
        # 25:60 형태 (형식은 맞으나 범위 오류) -> "유효한 시각을 입력하세요."
        with self.assertRaisesRegex(ValueError, "유효한 시각을 입력하세요."):
            calculate_parking_fee("25:00", "09:00")
        with self.assertRaisesRegex(ValueError, "유효한 시각을 입력하세요."):
            calculate_parking_fee("09:00", "09:60")

    def test_logical_error_time_order(self):
        # 14:00 입차, 12:00 출차 시 -> "출차 시간은 입차 시간보다 뒤여야 합니다."
        with self.assertRaisesRegex(ValueError, "출차 시간은 입차 시간보다 뒤여야 합니다."):
            calculate_parking_fee("14:00", "12:00")
        # 14:00 입차, 14:00 출차 시 -> "출차 시간은 입차 시간보다 뒤여야 합니다."
        with self.assertRaisesRegex(ValueError, "출차 시간은 입차 시간보다 뒤여야 합니다."):
            calculate_parking_fee("14:00", "14:00")

if __name__ == "__main__":
    import sys
    result = unittest.main(argv=[sys.argv[0]])
    
    # 성공/실패 수 출력
    failures = result.result.failures
    errors = result.result.errors
    successes = result.result.testsRun - len(failures) - len(errors)
    
    print("\n" + "="*30)
    print(f"테스트 완료 결과")
    print(f"- 통과: {successes}")
    print(f"- 실패: {len(failures)}")
    print(f"- 에러: {len(errors)}")
    print("="*30)
    
    if len(failures) + len(errors) > 0:
        sys.exit(1)
