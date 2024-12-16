import math
import random


def generateRandomCode(length=5):
    digits = "0123456789"
    result = ""

    for i in range(length):
        result += digits[math.floor(random.random() * 10)]
    return str(result)
