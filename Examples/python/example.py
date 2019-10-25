def function(a: 'integer[]', N: 'integer') -> 'integer':
    palo: 'integer'
    dado: 'integer'
    i: 'integer'
    palo = -1
    dado = -1
    i = -1
    print(dado)
    print("Hello World!")
    while i <= N:
        if a[i] % 2 == 0:
            if a[i] > palo:
                palo = a[i]
        else:
            if a[i] > dado:
                dado = a[i]
        i = i + 1
        
    return palo + dado
