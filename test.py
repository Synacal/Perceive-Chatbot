def count_rows_in_file(file_path):
    """
    Count the number of rows (lines) in a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The number of rows in the file.
    """
    try:
        with open(file_path, "r") as file:
            rows = file.readlines()
            return len(rows)
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


# Example usage:
file_path = "Completed EPO Patent ID List (1).txt"
print(count_rows_in_file(file_path))
