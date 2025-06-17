from .calculator import Calculator


def test_add():
    assert Calculator.add(1, 2) == 3.0
    assert Calculator.add(1.0, 2.0) == 3.0
    assert Calculator.add(0, 2.0) == 2.0
    assert Calculator.add(2.0, 0) == 2.0
    assert Calculator.add(-4, 2.0) == -2.0

def test_subtract():
    assert Calculator.subtract(1, 2) == -1.0
    assert Calculator.subtract(2, 1) == 1.0
    assert Calculator.subtract(1.0, 2.0) == -1.0
    assert Calculator.subtract(0, 2.0) == -2.0
    assert Calculator.subtract(2.0, 0.0) == 2.0
    assert Calculator.subtract(-4, 2.0) == -6.0

def test_multiply():
    assert Calculator.multiply(1, 2) == 2.0
    assert Calculator.multiply(1.0, 2.0) == 2.0
    assert Calculator.multiply(0, 2.0) == 0.0
    assert Calculator.multiply(2.0, 0.0) == 0.0
    assert Calculator.multiply(-4, 2.0) == -8.0

def test_divide():
    # assert Calculator.divide(1, 2) == 0.5
    assert Calculator.divide(1.0, 2.0) == 0.5
    assert Calculator.divide(0, 2.0) == 0
    assert Calculator.divide(-4, 2.0) == -2.0
    # assert Calculator.divide(2.0, 0.0) == 'Cannot divide by 0'

def test_add2():
    # Test that add2 method raises NameError due to undefined variable 'z'
    try:
        Calculator.add2(1, 2)
        assert False, "Expected NameError was not raised"
    except NameError as e:
        assert "name 'z' is not defined" in str(e)
