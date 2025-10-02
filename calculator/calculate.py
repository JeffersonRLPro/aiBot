def calculate(expression):
    parts = expression.split()
    num1 = int(parts[0])
    operator1 = parts[1]
    num2 = int(parts[2])
    operator2 = parts[3]
    num3 = int(parts[4])

    if operator1 == '+' and operator2 == '*':
        result = num2 * num3
        result = num1 + result
    elif operator1 == '+' and operator2 == '/':
        result = num2 / num3
        result = num1 + result
    elif operator1 == '-' and operator2 == '*':
        result = num2 * num3
        result = num1 - result
    elif operator1 == '-' and operator2 == '/':
        result = num2 / num3
        result = num1 - result
    elif operator2 == '*':
        result = num2 * num3
        if operator1 == '+':
            result = num1 + result
        else:
            result = num1 - result
    else:
        result = num2 / num3
        if operator1 == '+':
            result = num1 + result
        else:
            result = num1 - result

    return result


print(calculate("3 + 7 * 2"))