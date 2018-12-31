
def get_seconds(number):
    if number < 0:
        number = 0

    if 10 <= number < 20:
        return f'{number} секунд'

    digit = number % 10

    if digit == 1:
        return f'{number} секунда'

    if 1 < digit < 5:
        return f'{number} секунды'

    return f'{number} секунд'


