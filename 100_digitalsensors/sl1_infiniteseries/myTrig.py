import math

def sin(x, n=20) :
    sin = 0
    for i in range(n):
        iTerm = (((-1)**i)*(x**(2*i+1)))/(math.factorial(2*i+1))
        sin += iTerm
    return sin

def cos(x, n=20) :
    cos = 0
    for i in range(n):
        iTerm = (((-1)**i)*(x**(2*i)))/(math.factorial(2*i))
        cos += iTerm
    return cos

        