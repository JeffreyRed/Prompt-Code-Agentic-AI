# ✅ REVIEWED BY AGENT 3

# HOW TO RUN
# To run the calculator, save this code in a file named `calculator.py` 
# and execute it using Python 3. The GUI will appear, allowing you to input 
# two numbers and perform addition, subtraction, multiplication, or division.

# DEPENDENCIES
# pip install tk

import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    """A simple calculator application using Tkinter for basic arithmetic operations."""
    
    def __init__(self, master: tk.Tk) -> None:
        """Initialize the calculator interface."""
        self.master = master
        self.master.title("Simple Calculator")

        # Create input fields
        self.input1 = tk.Entry(master)
        self.input1.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.input2 = tk.Entry(master)
        self.input2.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Create buttons for operations
        self.create_buttons()

    def create_buttons(self) -> None:
        """Create buttons for calculator operations."""
        operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
        }

        # Create buttons and add them to the grid
        row = 2
        for op, func in operations.items():
            button = tk.Button(self.master, text=op, command=func)
            button.grid(row=row, column=list(operations.keys()).index(op), padx=5, pady=5)

    def add(self) -> None:
        """Perform addition and display the result."""
        self.calculate(lambda x, y: x + y)

    def subtract(self) -> None:
        """Perform subtraction and display the result."""
        self.calculate(lambda x, y: x - y)

    def multiply(self) -> None:
        """Perform multiplication and display the result."""
        self.calculate(lambda x, y: x * y)

    def divide(self) -> None:
        """Perform division and display the result."""
        self.calculate(lambda x, y: x / y)

    def calculate(self, operation) -> None:
        """Perform the calculation based on the given operation."""
        try:
            num1 = float(self.input1.get())
            num2 = float(self.input2.get())
            result = operation(num1, num2)
            self.display_result(result)
        except ValueError:
            self.show_error("Invalid input! Please enter numeric values.")
        except ZeroDivisionError:
            self.show_error("Error! Division by zero is not allowed.")

    def display_result(self, result: float) -> None:
        """Display the result of the calculation."""
        result_str = f"Result: {result}"
        messagebox.showinfo("Calculation Result", result_str)

    def show_error(self, message: str) -> None:
        """Display an error message."""
        messagebox.showerror("Error", message)


def main() -> None:
    """Run the calculator application."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# This code creates a simple GUI calculator using Tkinter that can perform 
# basic arithmetic operations such as addition, subtraction, multiplication, 
# and division. It handles errors for invalid inputs and division by zero.