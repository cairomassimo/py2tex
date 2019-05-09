from math import sqrt
def aut(param1, param2, param3):
    if param1 == 0:
        if param2 < param3:
            return True
        else:
            return False
    else:
        if param2 == 0:
            if param1 < param3:
                return True
            else:
                return False
        else:
            if (sqrt(param1 * param1 + param2 * param2)) < param3:
                return True
            else:
                return False


print(aut(1, 0, 3))
print(aut(1, 2, 3))
print(aut(2, 4, 6))
print(aut(3, 6, 9))
print(aut(1, 0, -1))
