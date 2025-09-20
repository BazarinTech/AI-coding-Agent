import sympy
from sympy import *

x, y, z = symbols('x y z')

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def differentiate(expression, variable):
    return diff(expression, variable)

def my_integrate(expression, variable):
    return integrate(expression, variable)

def simplify_expression(expression):
    return simplify(expression)

def run_tests():
    test_results = []

    # Test cases for basic arithmetic
    test_results.append(add(5, 3) == 8)
    test_results.append(subtract(10, 4) == 6)
    test_results.append(multiply(2, 6) == 12)
    test_results.append(divide(15, 3) == 5)

    # Test cases for calculus
    test_results.append(str(differentiate(x**2, x)) == '2*x')
    test_results.append(str(my_integrate(x, x)).replace(' + C', '') == 'x**2/2')

    # Test cases for symbolic math
    test_results.append(str(simplify_expression((x+x)*(x+x))) == '4*x**2')

    if all(test_results):
        print("All tests passed!")
    else:
        print("Some tests failed:")
        for i, result in enumerate(test_results):
            if not result:
                print(f"Test case {i+1} failed.")

if __name__ == '__main__':
    run_tests()
