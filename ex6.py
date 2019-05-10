from math import sqrt
def aut(par1, par2, par3):
    if par1 == 0:
        if par2 < par3:
            return True
        else:
            return False
    else:
        if par2 == 0:
            if par1 < par3:
                return True
            else:
                return False
        else:
            if (sqrt(par1 * par1 + par2 * par2)) < par3:
                return True
            else:
                return False

"!hide"
print(aut(1, 0, 3))
print(aut(1, 2, 3))
print(aut(2, 4, 6))
print(aut(3, 6, 9))
print(aut(1, 0, -1))
"!show"
