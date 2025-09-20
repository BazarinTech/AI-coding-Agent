import math
import sys

def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return result
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expression = sys.argv[1]
        result = calculate(expression)
        print(f"Result: {result}")
    else:
        print("Please provide an expression as a command-line argument.")