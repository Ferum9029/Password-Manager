from random import choice
from generation import preferences


def get_symbols():
    symbols = []
    for symbol in preferences.symbols:
        for _ in range(preferences.repeating):
            symbols.append(symbol)
    return symbols


def generate(count):
    symbols = get_symbols()
    output = ''
    for _ in range(count):
        symbol = choice(symbols)
        output += symbol
        symbols.remove(symbol)
    return output
