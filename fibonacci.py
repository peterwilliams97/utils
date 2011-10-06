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
    calculate Fibonacci numbers to the way I imagine a Python programmer would.
    
"""
import math

# Golden ratio constants
_S = math.sqrt(5.0)
_A = (1.0 + _S)/2.0
_B = (1.0 - _S)/2.0

def fibonacci(n):
    """The way I would expect a Python programmer calculates the nth Fibonacci number, 
        following http://bit.ly/n3netk  This assumes the programmer took an undergraduate 
        math degree and stayed awake during the interesting bits.
    """
    return round((_A ** n - _B ** n)/_S)

def fib2(n):
    """The way a node.js programmer calculates the nth Fibonacci number. 
        See http://bit.ly/q3PeXe
    """
    if n <= 1:
        return n
    return fib2(n-1) + fib2(n-2)

if __name__ == '__main__':
    NUMBER = 100                # Number of Fibonnaci numbers to calculate
    NODE_JS_THRESHOLD = 35      # Number of Fibonnaci numbers before slow method takes too long
    
    for i in range(NUMBER + 1):
        if i == NODE_JS_THRESHOLD:
            print 'Too hard for node.js way. Python way only from now on.'
        f1 = fibonacci(i)
        if i < NODE_JS_THRESHOLD:
            f2 = fib2(i) 
            print '%2d: %5d %5d' % (i, f1, f2)
            assert(f1 == f2)
        else:
            print '%2d: %5d' % (i, f1)
            