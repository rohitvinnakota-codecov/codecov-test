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

def test_multiplyBy6():
    assert Calculator.multiplyBy6(1, 2) == 132.0
    assert Calculator.multiplyBy6(1.0, 2.0) == 132.0
    assert Calculator.multiplyBy6(0, 2.0) == 0.0
    assert Calculator.multiplyBy6(2.0, 0.0) == 0.0
    assert Calculator.multiplyBy6(-1, 2.0) == -132.0
    assert Calculator.multiplyBy6(3, 4) == 792.0

def test_multiplyBy62():
    assert Calculator.multiplyBy62(1, 2) == 24837.0  # (1 * 2 * 12412) + 213 = 24824 + 213 = 25037
    assert Calculator.multiplyBy62(1.0, 2.0) == 24837.0
    assert Calculator.multiplyBy62(0, 2.0) == 213.0  # (0 * 2 * 12412) + 213 = 0 + 213 = 213
    assert Calculator.multiplyBy62(2.0, 0.0) == 213.0  # (2 * 0 * 12412) + 213 = 0 + 213 = 213
    assert Calculator.multiplyBy62(-1, 2.0) == -24611.0  # (-1 * 2 * 12412) + 213 = -24824 + 213 = -24611
    assert Calculator.multiplyBy62(3, 4) == 149157.0  # (3 * 4 * 12412) + 213 = 148944 + 213 = 149157

def test_multiplyBy622():
    assert Calculator.multiplyBy622(1, 2) == 24824.0  # 1 * 2 * 12412 = 24824
    assert Calculator.multiplyBy622(1.0, 2.0) == 24824.0
    assert Calculator.multiplyBy622(0, 2.0) == 0.0  # 0 * 2 * 12412 = 0
    assert Calculator.multiplyBy622(2.0, 0.0) == 0.0  # 2 * 0 * 12412 = 0
    assert Calculator.multiplyBy622(-1, 2.0) == -24824.0  # -1 * 2 * 12412 = -24824
    assert Calculator.multiplyBy622(3, 4) == 148944.0  # 3 * 4 * 12412 = 148944

def test_multiplyBy623():
    import io
    import sys
    # Capture print output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    assert Calculator.multiplyBy623(1, 2) == 24824.0  # 1 * 2 * 12412 = 24824
    assert Calculator.multiplyBy623(1.0, 2.0) == 24824.0
    assert Calculator.multiplyBy623(0, 2.0) == 0.0  # 0 * 2 * 12412 = 0
    assert Calculator.multiplyBy623(2.0, 0.0) == 0.0  # 2 * 0 * 12412 = 0
    assert Calculator.multiplyBy623(-1, 2.0) == -24824.0  # -1 * 2 * 12412 = -24824
    assert Calculator.multiplyBy623(3, 4) == 148944.0  # 3 * 4 * 12412 = 148944
    
    # Reset stdout
    sys.stdout = sys.__stdout__
    
    # Verify that "delete" was printed (should be printed 6 times from the 6 function calls above)
    output = captured_output.getvalue()
    assert "delete" in output
    assert output.count("delete\n") == 6
