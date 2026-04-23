from pathlib import Path
import re

MUL_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
INSTRUCTION_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
TEST_FILE = Path(__file__).with_name("test")
INPUT_FILE = Path(__file__).with_name("input")
PART_2_TEST = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def multiply_some_numbers(lines: list[str]) -> int:
    total = 0
    for line in lines:
        for left, right in MUL_PATTERN.findall(line):
            total += int(left) * int(right)
    return total


def main() -> int:
    test_lines = TEST_FILE.read_text(encoding="utf-8").splitlines()
    test_result = multiply_some_numbers(test_lines)
    assert test_result == 161, f"expected 161, got {test_result}"

    input_lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()
    input_result = multiply_some_numbers(input_lines)
    print(input_result)
    return input_result


def multiply_some_numbers_with_state(lines: list[str]) -> int:
    total = 0
    enabled = True
    for line in lines:
        for match in INSTRUCTION_PATTERN.finditer(line):
            instruction = match.group(0)
            if instruction == "do()":
                enabled = True
            elif instruction == "don't()":
                enabled = False
            elif enabled:
                left, right = match.groups()
                total += int(left) * int(right)
    return total


def main_2() -> int:
    test_lines = PART_2_TEST.splitlines()
    test_result = multiply_some_numbers_with_state(test_lines)
    assert test_result == 48, f"expected 48, got {test_result}"

    input_lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()
    input_result = multiply_some_numbers_with_state(input_lines)
    print(input_result)
    return input_result


if __name__ == "__main__":
    main()
    main_2()
