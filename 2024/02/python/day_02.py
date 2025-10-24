import sys
import unittest
from typing import Iterable

Report = Iterable[int]
Reports = Iterable[Report]


def validate(report: Report) -> bool:
    diffs = [b - a for a, b in zip(report, report[1:])]
    ascending = all(d > 0 for d in diffs)
    descending = all(d < 0 for d in diffs)
    small_steps = all(1 <= abs(d) <= 3 for d in diffs)
    return (ascending or descending) and small_steps


def count_safe_reports(reports: Reports) -> int:
    return sum(1 for r in reports if validate(r))


def get_reports(file_path: str) -> Reports:
    with open(file_path) as f:
        yield from ([int(n) for n in line.split()] for line in f)


# -----------------------
# Tests integrados
# -----------------------


class TestValidateFake(unittest.TestCase):
    def test_descending(self):
        self.assertTrue(validate([5, 4, 3]))

    def test_not_descending(self):
        self.assertFalse(validate([3, 4, 2]))


class TestValidateReport(unittest.TestCase):
    def test_cases(self):
        test_data = [
            ([7, 6, 4, 2, 1], True),
            ([1, 2, 7, 8, 9], False),
            ([9, 7, 6, 2, 1], False),
            ([1, 3, 2, 4, 5], False),
            ([8, 6, 4, 4, 1], False),
            ([1, 3, 6, 7, 9], True),
        ]

        for nums, expected in test_data:
            with self.subTest(input=nums, expected=expected):
                got = validate(nums)
                self.assertEqual(
                    got,
                    expected,
                    msg=f"Failed for input: {nums}, expected: {expected} got: {got}",
                )


class TestCountSafeReports(unittest.TestCase):
    def test_count_safe_reports(self):
        test_reports = get_reports("../test")
        expected_count = 2
        result = count_safe_reports(test_reports)
        self.assertEqual(result, expected_count)


if __name__ == "__main__":
    result = unittest.main(exit=False)
    if not result.result.wasSuccessful():
        sys.exit(1)

    # -----------------------
    # Main execution
    reports = get_reports("../input")
    safe_count = count_safe_reports(reports)
    print(f"Number of safe reports: {safe_count}")
