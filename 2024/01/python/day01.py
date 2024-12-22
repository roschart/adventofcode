def process_line(line: str) -> tuple[int, int]:
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

# Example usage:
with open("../input", "r") as f:
    for line in f:
        try:
            result = process_line(line)
            print(result)
        except ValueError as e:
            print(e)
