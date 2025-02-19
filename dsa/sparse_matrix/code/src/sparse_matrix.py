import os

class SparseMatrix:
    def __init__(self, num_rows, num_cols):
        self.elements = {}
        self.num_rows = num_rows
        self.num_cols = num_cols

    @staticmethod
    def _parse_matrix_file(file_path):
        try:
            with open(file_path.replace("\\", "/"), "r") as file:
                lines = file.readlines()
                return [line.strip() for line in lines if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def from_file(matrix_file_path):
        lines = SparseMatrix._parse_matrix_file(matrix_file_path)
        
        if len(lines) < 2:
            raise ValueError(f"File {matrix_file_path} must contain at least two lines for dimensions.")
        
        try:
            num_rows = int(lines[0].split('=')[1])
            num_cols = int(lines[1].split('=')[1])
        except (IndexError, ValueError):
            raise ValueError(f"Invalid matrix dimensions in {matrix_file_path}.")
        
        matrix = SparseMatrix(num_rows, num_cols)

        for line in lines[2:]:
            if not line.startswith("(") or not line.endswith(")"):
                raise ValueError(f"Invalid format for matrix element: {line}")

            elements = line[1:-1].split(',')
            try:
                row = int(elements[0].strip())
                col = int(elements[1].strip())
                value = int(elements[2].strip())
            except (IndexError, ValueError):
                raise ValueError(f"Invalid matrix element format in file: {line}")
            
            matrix.set_element(row, col, value)
        
        return matrix

    def set_element(self, row, col, value):
        if row >= self.num_rows:
            self.num_rows = row + 1
        if col >= self.num_cols:
            self.num_cols = col + 1
        
        key = f"{row},{col}"
        self.elements[key] = value

    def get_element(self, row, col):
        key = f"{row},{col}"
        return self.elements.get(key, 0)

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError(f"Cannot add matrices of different dimensions.")
        
        result = SparseMatrix(self.num_rows, self.num_cols)
        
        for key, value in self.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(row, col, value)

        for key, value in other.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(row, col, result.get_element(row, col) + value)
        
        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError(f"Cannot subtract matrices of different dimensions.")
        
        result = SparseMatrix(self.num_rows, self.num_cols)
        
        for key, value in other.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(row, col, self.get_element(row, col) - value)
        
        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError(f"Cannot multiply: column count of the first matrix must equal row count of the second.")
        
        result = SparseMatrix(self.num_rows, other.num_cols)

        for key1, value1 in self.elements.items():
            row1, col1 = map(int, key1.split(','))
            for key2, value2 in other.elements.items():
                row2, col2 = map(int, key2.split(','))
                if col1 == row2:
                    result.set_element(row1, col2, result.get_element(row1, col2) + value1 * value2)
        
        return result

    def transpose(self):
        result = SparseMatrix(self.num_cols, self.num_rows)
        for key, value in self.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(col, row, value)
        return result

    def __str__(self):
        result = [f"rows={self.num_rows}", f"cols={self.num_cols}"]
        for key, value in self.elements.items():
            row, col = key.split(',')
            result.append(f"({row}, {col}, {value})")
        return '\n'.join(result)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(str(self))

def get_user_input(prompt):
    return input(prompt)

def do_some_operations():
    try:
        operations = {
            'SUM': ('addition', 'add'),
            'DIFF': ('subtraction', 'subtract'),
            'PROD': ('multiplication', 'multiply')
        }

        print("MATRIX OPERATIONS MENU")
        print("======================")
        print("SUM  - Matrix Addition")
        print("DIFF - Matrix Subtraction")
        print("PROD - Matrix Multiplication")

        choice = get_user_input("Choose operation (SUM, DIFF, PROD): ").upper()

        if choice not in operations:
            raise ValueError("Invalid option.")

        # Get base directory (two levels up from script location)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sample_dir = os.path.join(base_dir, "sample_inputs")
        
        try:
            files = [f for f in os.listdir(sample_dir) if f.endswith('.txt')]
            
            if len(files) < 2:
                raise ValueError("Not enough matrix files found in sample directory")
        except FileNotFoundError:
            print(f"Error: Sample directory not found at {sample_dir}")
            print("Please ensure the directory exists with sample matrix files.")
            return
            
        file1 = os.path.join(sample_dir, files[0])
        file2 = os.path.join(sample_dir, files[1])

        try:
            print(f"Loading first matrix from {file1}...")
            matrix1 = SparseMatrix.from_file(file1)
            print(f"Loaded matrix of size {matrix1.num_rows}x{matrix1.num_cols} successfully")

            print(f"Loading second matrix from {file2}...")
            matrix2 = SparseMatrix.from_file(file2)
            print(f"Loaded matrix of size {matrix2.num_rows}x{matrix2.num_cols} successfully")
        except Exception as e:
            print(f"Error loading matrix files: {str(e)}")
            return

        operation_name, method = operations[choice]
        print(f"Performing {operation_name}...")

        result = getattr(matrix1, method)(matrix2)
        result_dir = os.path.join(base_dir, "sample_result")
        os.makedirs(result_dir, exist_ok=True)
        output_file = os.path.join(result_dir, f"result_{operation_name.lower()}.txt")
        result.save_to_file(output_file)

        print("\nMatrix 1:")
        print(matrix1)
        
        print("\nMatrix 2:")
        print(matrix2)
        
        print(f"\n{operation_name.capitalize()} Result:")
        print(result)
        
        print(f"\nOperation completed successfully. Output saved to {output_file}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    do_some_operations()
