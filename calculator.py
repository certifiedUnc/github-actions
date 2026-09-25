"""A tiny calculator module used by the GitHub Actions tutorial."""


def add(left: float, right: float) -> float:
    return left + right


def subtract(left: float, right: float) -> float:
    return left - right


def multiply(left: float, right: float) -> float:
    return left * right


def divide(left: float, right: float) -> float:
    if right == 0:
        raise ValueError("Cannot divide by zero")
    return left / right


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)} change")
