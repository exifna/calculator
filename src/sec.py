

def simpson(a, b, f):
    return ((b - a) / 6) * (f(a) + 4 * f((a + b)/2) + f(b))

def calculate(f, a: int, b: int, step: int = 10_000) -> float:
    dX = abs(b - a) / step
    result = 0

    for n in range(step):
        result += simpson(a + dX * n, a + dX * (n + 1), f)


    return result