#hello
class Calculator:

    def add(x, y):
        return x + y

    def subtract(x, y):
        return x - y

    def multiply(x, y):
        return x * y

    def divide(x, y):
        if y == 0:
            return 'Cannot divide by 0'
        return x * 1.0 / y

    def multiplyBy6(x, y):
        return x * y * 66

    def multiplyBy62(x, y):
        return x * y * 12412
