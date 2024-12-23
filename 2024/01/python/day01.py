import unittest
from typing import Iterator, Tuple, List

def process_line(line: str) -> Tuple[int, int]:
    """
    Parses a line and extracts two integers.
    
    Args:
        line: A string from f.readline().
    
    Returns:
        A tuple containing two integers.
    
    Raises:
        ValueError: If the line does not contain exactly two integers.
    """
    stripped_line = line.strip()
    parts = stripped_line.split()
    if len(parts) != 2:
        raise ValueError(f"Invalid line format: '{line}'")
    try:
        return tuple(map(int, parts))
    except ValueError as e:
        raise ValueError(f"Error parsing line: '{line}' - {e}")

def get_data_from_file(file_path: str) -> Tuple[List[int], List[int]]:
    col1, col2 = [], []
    with open(file_path, "r") as f:
        for line in f:
            num1, num2 = process_line(line)
            col1.append(num1)
            col2.append(num2)
    return col1, col2

def calculate_distance(col1: list[int], col2: list[int]) -> int:
    col1.sort()
    col2.sort()
    return sum(abs(a - b) for a, b in zip(col1, col2))





if __name__ == "__main__":
    file_path = "../input"  # Replace with your file path
    try:
        col1, col2 = get_data_from_file(file_path)
        result=calculate_distance(col1,col2)
        print("Result: ", result)
    except ValueError as e:
        print("Error:", e)

