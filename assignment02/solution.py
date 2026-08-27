def factorial(n):
    """
    0 이상의 정수 n에 대해 n!을 반환하세요.

    예:
    factorial(0) -> 1
    factorial(5) -> 120
    """
    if n == 0 or n == 1:
        return 1
    return n * factorial(n-1)