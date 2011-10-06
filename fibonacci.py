from __future__ import division
"""
    http://bit.ly/ooOVLN says
 
        Cutting-edge communities, like Node.js and Ruby, encourage fast-paced innovation 
        (though sometimes at the cost of application breakage). Conservative communities, 
        like Java, favor a more responsible and predictable approach (though sometimes at 
        the expense of being behind the curve). Python has managed to gracefully navigate 
        a middle path between these extremes, giving it a respected reputation even among 
        non-Python programmers. The Python community is an island of calm in the stormy 
        seas of the programming world.
    
    The following code compares how node.js programmers http://bit.ly/q3PeXe are known to 
    calculate Fibonacci numbers to the way I imagine a Python programmer would do so. You 
    may replace "Python programmer" with anyone inclined to think through the underlying 
    math rather than rely on the framework they are using to do all the work. 
"""
import math

# Golden ratio constants
_S = math.sqrt(5.0)
_A = (1.0 + _S)/2.0
_B = (1.0 - _S)/2.0

def _fibonacci_golden(n):
    """The way I would expect a Python programmer to precalculate the low Fibonacci 
        numbers. Follows http://bit.ly/n3netk  Assumes the programmer took an 
        undergraduate math degree and stayed awake during the bits relevant to this 
        calculation. 
        Will only work for n up to which floating point is accurate enough. See 
        _GOLDEN_LIMIT below.
    """
    return int(round((_A ** n - _B ** n)/_S))

# Highest number where floating point accuracy gives correct answer.
# Calculated in _find_breaking_point() below. 
_GOLDEN_LIMIT = 70 

def _find_breaking_point():
    """Find the highest n for which _fibonacci_golden(n) is accurate.
        Used to calculate _GOLDEN_LIMIT
    """
    v2 = 0
    v1 = 1
    for i in range(2, 10**6):
        v0 = _fibonacci_golden(i)
        if v0 != v1 + v2:
            print 'Breaking point at i=%d' % i
            print '   v0=%d' % v0
            print 'v1+v2=%d' % (v1+v2)
            print '   v1=%d' % v1
            print '   v2=%d' % v2
            print ' diff=%g' % ((v0-v1-v2)/v0)
            break
        else:
            assert(_GOLDEN_LIMIT >= i)
        v2 = v1
        v1 = v0  

# _fibonacci_numbers is the cache: _fibonacci_numbers[i] = ith Fibonacci number 
# Precalcuate the numbers for which the golden mean method works
_fibonacci_numbers = [_fibonacci_golden(i) for i in range(_GOLDEN_LIMIT)]

def fibonacci(n):
    """Return the nth Fibonacci number where 0th = 0, 1st = 1 etc
        This is the way I would expect a Python programmer to calculate the nth Fibonacci 
        number with a simple cache and some precalculation.
    """
    # nth Fibonacci number is _fibonacci_numbers[n] so extend _fibonacci_numbers to 
    # length n+1 by the defining recurrence if necessary.
    global _fibonacci_numbers
    for i in range(len(_fibonacci_numbers), n+1):
        _fibonacci_numbers.append(_fibonacci_numbers[-1] + _fibonacci_numbers[-2])
    
    return _fibonacci_numbers[n] 

def fib2(n):
    """The way node.js programmers have been known to calculate the nth Fibonacci number. 
        See http://bit.ly/q3PeXe
    """
    if n <= 1:
        return n
    return fib2(n-1) + fib2(n-2)

if __name__ == '__main__':
    #
    # Some tests for the Fibonacci generators
    #

    MAX_FIBONACCI_DIGITS = 20000

    def test_fibonacci(): 
        """Check that fibonacci() is accurate up to Fibonacci numbers of 
            MAX_FIBONACCI_DIGITS digits"""
        v2 = 0
        v1 = 1
        for i in range(2, 10**6):
            v0 = fibonacci(i)
            if i % 10000 == 0:
                num_digits = len(str(v0))
                print 'n=%6d: %6d digits' % (i, num_digits)
                if num_digits >= MAX_FIBONACCI_DIGITS: 
                    break  
            assert(v0 == v1 + v2)
            v2 = v1
            v1 = v0

    NUMBER = 100                # Number of Fibonnaci numbers to calculate
    NODE_JS_THRESHOLD = 35      # Number of Fibonnaci numbers before slow method takes too long

    def compare_methods():
        """Compare fibonacci() to a Fibonacci number calculator seen in node.js""" 
        for i in range(NUMBER + 1):
            if i == NODE_JS_THRESHOLD:
                print 'Too hard for node.js way. Python way only from now on.'
            f1 = fibonacci(i)
            if i < NODE_JS_THRESHOLD:
                f2 = fib2(i) 
                print '%3d: %8d %8d' % (i, f1, f2)
                assert(f1 == f2)
            else:
                print '%3d: %8d' % (i, f1)

    #  
    # Choose which test to run by un commenting on of the following lines            
    #

    #test_fibonacci()
    compare_methods()