def pp(v: 'array', dim: 'intero', k: 'intero'):
	i=0
	while(i<k):
		v[dim-i-1] = 0
		i=i+1

vet = []
i=0
while(i<10):
	vet.append(25/4)
	i=i+1
pp(vet, 10, 5)
print("Lo array dopo pp è: ")
i=0
while(i<10):
	print(vet[i], end=" ")
	i=i+1

