def Ras(a,b):
    Q = [None]
    R = a
    U = b
    N = 0
    while R%U != 0:
        Q.append(R//U)
        P = R
        R = U
        U = P%U
        N += 1
    A = -Q[N]
    B = 1
    for i in range(N,1,-1):
        C = A
        A = A * -Q[i-1]+B
        B = C
    return (U,A,B)
#A * b + B * a = U

#a = int(input())
#b = int(input())
#print(Ras(a,b))
def prost(n):
    a = []
    for i in range(n + 1):
        a.append(i)
    a[1] = 0
    i = 2
    while i <= n:
        if a[i] != 0:
            j = i + i
            while j <= n:
                a[j] = 0
                j = j + i
        i += 1
    a = set(a)
    a.remove(0)
    return a
