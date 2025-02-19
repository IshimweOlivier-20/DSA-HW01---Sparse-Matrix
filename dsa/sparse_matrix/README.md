# Sparse Matrix Operations

## Overview
This project implements a Sparse Matrix class in Python that supports basic matrix operations including addition, subtraction, multiplication, and transposition. The implementation is optimized for handling large matrices where most elements are zero.

## Directory Structure
```
dsa/
└── sparse_matrix/
    ├── code/
    │   └── src/
    │       └── sparse_matrix.py       # Main Python script
    ├── sample_inputs/
    │   ├── matrix1.txt                 # Sample input file 1
    │   └── matrix2.txt                 # Sample input file 2
    └── sample_result/
        ├── result_addition.txt          # Sample addition result
        ├── result_subtraction.txt      # Sample subtraction result
        └── result_multiplication.txt    # Sample multiplication result
```

## Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd dsa/sparse_matrix/code/src
   ```

### Usage
Run the main script:
```bash
python sparse_matrix.py
```

The program will:
1. Display a menu of available operations
2. Load sample matrices from the `sample_inputs` directory
3. Perform the selected operation
4. Save the result to the `sample_result` directory

## Available Operations
- **SUM**: Matrix Addition
- **DIFF**: Matrix Subtraction
- **PROD**: Matrix Multiplication

## Sample Input Format
Matrix files should follow this format:
```
rows=3
cols=3
(0, 0, 1)
(1, 1, 2)
(2, 2, 3)
```

## Contributing
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Project Maintainer: [Your Name]  
Email: [Your Email]
