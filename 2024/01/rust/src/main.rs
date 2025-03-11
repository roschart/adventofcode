use std::fs;

fn main() {
    println!("Hello, world!");
}


fn calculate_distance(mut col1: Vec<i32>, mut col2: Vec<i32>) -> i32 {
    col1.sort();
    col2.sort();
    col1.iter().zip(col2.iter()).map(|(a, b)| (a - b).abs()).sum()
}

fn get_data_from_file(file_path: &str) -> (Vec<i32>, Vec<i32>) {
    let content = fs::read_to_string(file_path).expect("Failed to read the file");
    let mut col1 = Vec::new();
    let mut col2 = Vec::new();

    for line in content.lines() {
        let nums: Vec<i32> = line
            .split_whitespace()
            .map(|n| n.parse().expect("Invalid number in file"))
            .collect();
        if nums.len() != 2 {
            panic!("Invalid line format");
        }
        col1.push(nums[0]);
        col2.push(nums[1]);
    }

    (col1, col2)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn run_test_case(file_path: &str, expected_result: i32) {
        let (col1, col2) = get_data_from_file(file_path);
        let result = calculate_distance(col1, col2);
        assert_eq!(result, expected_result);
    }

    #[test]
    fn test_example_file() {
        run_test_case("../test", 11);
    }

    #[test]
    fn test_input_file() {
        run_test_case("../input", 2196996);
    }
}
