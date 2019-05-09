def proc(v: 'array', n:'intero'):
	i=0
	while(i < n):
		b=v[i]
		c=0
		while (b > 1):
			a=1 
			while (b > a):
				a=a*2
			if b < a:
				b=b-a/2
				c=c+a/2
		if i%2 == 0:
			v[i]=c
		else:
			v[i]=c+1
		i=i+1
v = [3.45, 5.67, 8.92, 2.12, 7.33, 8.21, 4.21, 9.03]
proc(v, 8)
print(v)
