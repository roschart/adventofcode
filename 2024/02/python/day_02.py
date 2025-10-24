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

#  tolerate a single bad level
def validate_with_tolerance(report: Report) -> bool:
    if validate(report):
        return True
    for i in range(len(report)):
        modified_report = report[:i] + report[i+1:]
        if validate(modified_report):
            return True
    return False 


def count_safe_reports(reports: Reports, validator=validate) -> int:
    return sum(1 for r in reports if validator(r))


def get_reports(file_path: str) -> Reports:
    with open(file_path) as f:
        yield from ([int(n) for n in line.split()] for line in f)

def get_repports2(file_path: str) -> Reports:
    yield from ([int(n) for n in line.split()] for line in open(file_path))


# -----------------------
# Tests integrados
# -----------------------


class TestValidateFake(unittest.TestCase):
    def test_descending(self):
        self.assertTrue(validate([5, 4, 3]))

    def test_not_descending(self):
        self.assertFalse(validate([3, 4, 2]))

TEST_DATA=[
            ([7, 6, 4, 2, 1], True, True),
            ([1, 2, 7, 8, 9], False, False),
            ([9, 7, 6, 2, 1], False, False),
            ([1, 3, 2, 4, 5], False, True),
            ([8, 6, 4, 4, 1], False, True),
            ([1, 3, 6, 7, 9], True, True),
        ]
class TestValidateReport(unittest.TestCase):
    def test_cases(self):
        for nums, expected_normal, expected_tolerant in TEST_DATA:
            with self.subTest(fn="validate", report=nums):
                got = validate(nums)
                self.assertEqual(got, expected_normal, msg=f"Failed for input: {nums}, expected: {expected_normal} got: {got}")

            with self.subTest(fn="validate_with_tolerance", report=nums):
                got = validate_with_tolerance(nums)
                self.assertEqual(got, expected_tolerant, msg=f"Failed for input: {nums}, expected: {expected_tolerant} got: {got}")


class TestCountSafeReports(unittest.TestCase):
    def test_count_safe_reports(self):
        test_reports =  list(nums for nums, _, _ in TEST_DATA)
        with self.subTest(fn="validate", report=test_reports):
            expected_count = sum(1 for _, ok, _ in TEST_DATA if ok)
            result = count_safe_reports(test_reports)
            self.assertEqual(result, expected_count)
        with self.subTest(fn="validate_with_tolerance", report=test_reports):
            expected_count = sum(1 for _, _, ok in TEST_DATA if ok)
            result = count_safe_reports(test_reports, validator=validate_with_tolerance)
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
    
    reports = get_reports("../input")
    safe_count_tolerant = count_safe_reports(reports, validator=validate_with_tolerance)
    print(f"Number of safe reports with tolerance: {safe_count_tolerant}")
