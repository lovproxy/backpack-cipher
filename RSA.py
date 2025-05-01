def bezout(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return (x, y, a)


class RSA:
    def __init__(self):
        self.p = int(input())
        self.q = int(input())
        self.n = self.p*self.q
        self.e = int(input())
        t = bezout(self.e,(self.p-1)*(self.q-1))
        self.d = t[0]%((self.p-1)*(self.q-1))
        print(self.d)

    def ecrypt(self,z):
        return (z**self.e %self.n)

    def decrypt(self,c):
        return(c**self.d %self.n)


r = RSA()
m = int(input())
x = r.ecrypt(m)
print(x)
print(r.decrypt(x))