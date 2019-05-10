def pp(v: 'array', dim: 'intero', k: 'intero'):
	i=0
	while(i<k):
		v[dim-i-1] = 0
		i=i+1

"!hide"
vet = [None] * 10
"!show"

r"""!tex
	\item[]
	\State{\tt vet[10]}
"""
i=0
while(i<10):
	vet[i] = 25/4
	i=i+1
pp(vet, 10, 5)
print("Lo array dopo pp è: ")
i=0
while(i<10):
	print(vet[i], end=" ")
	i=i+1

