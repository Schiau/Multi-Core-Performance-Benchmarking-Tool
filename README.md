# Multi-Core Performance Benchmarking Tool

This project is designed to provide users with a versatile multi-core performance benchmarking tool. By leveraging Python's Tkinter library for the graphical interface and subprocess for benchmark execution, this tool allows users to evaluate their system's multi-core capabilities efficiently. 

## Features

1. **Modular Benchmarking:** The tool includes various benchmarks tailored to assess multi-core performance. These benchmarks cover floating-point calculations for Pi, prime number calculation, MergeSort, and thread communication using the Producer-Consumer pattern.

2. **Graphical Interface:** The graphical user interface (GUI) offers an intuitive platform for users to interact with the tool. You can effortlessly select benchmarks, specify the number of threads, and view results within the same interface.

3. **Text and Graphical Results:** Results are presented in both text format and graphical plots. This dual presentation ensures that users can easily interpret performance metrics based on their preferences.

4. **Customizable:** Users have the flexibility to customize benchmark parameters such as the number of threads and specific benchmarks to run. 

## Folder Structure

- **benchmarks:** This directory contains the source code for benchmarks required for performance evaluation.
  
- **gui:** The GUI code resides within this folder, facilitating the interaction between users and the benchmarking tool.

## Usage

To utilize this tool effectively, follow these steps:

1. Clone the repository to your local machine.
   
2. Navigate to the `gui` folder within the cloned repository.
   
3. Execute the `main.py` file to launch the graphical interface.
   
4. Within the GUI, select the desired benchmarks by checking the corresponding checkboxes. You can select multiple benchmarks for simultaneous execution.

5. Specify the number of threads in the provided input field.

6. Initiate the benchmarking process by clicking the "Run" button.

7. Once benchmark execution is complete, you have two additional options for analysis:

   - Typing the command "graphic" in the terminal will generate a graphical plot based on the benchmark results.
   
   - Typing the command "test_multiple" in the terminal will generate multiple sets of results for different numbers of threads, allowing for deeper analysis of multi-threading performance across various configurations.


Feel free to explore and customize the tool according to your requirements and system configurations.
