import Euclid
import random
import math
import os
class mh:
    def encrypt(self,Name,msg1):
        #msg = input('Введите сообщение: ')
        msg = msg1.encode('utf-8')
        # 1 символ = 8 бит
        #print(msg)
        b = self.cont[Name][-1]
        n = len(b)
        msgbin = ''
        for s in msg:
            q = f"{s:0b}"
            q = (8-len(q))*'0' + q
            #print(s,q)
            msgbin += q
            # q = 8
        e = len(msgbin)%n
        msgbin += (n-e)*'0'
        ch=[]
        for x in range(0,len(msgbin),n):
            msgblock=msgbin[x:x+n]
            s = 0
            for u in range(n):
                if msgblock[u]=='1':
                    s += b[u]
            ch.append(s)
        print(f'Шифровка: {ch}')
        return ch


    def __init__(self):
        self.cont = dict()
        self.numcont = 0
        with open('cont.g',"r") as f:
            h = f.readlines()
            self.numcont = int(h[0])
            I = 1
            while len(h) > I:
                x = h.index('*****\n',I)
                curr_cont = h[I:x:1]
                Name = curr_cont[1][7:]
                Name = Name[:-1]
                if curr_cont[0] == 'FULL\n':
                    b = curr_cont[5][4:]
                    b = b[:-1]
                else:
                    b = curr_cont[2][4:]
                    b = b[:-1]
                I = x + 1
                a = None
                t = None
                m = None
                if curr_cont[0] == 'FULL\n':
                    a = curr_cont[2][4:]
                    a = a[:-1]
                    t = curr_cont[3][4:]
                    t = t[:-1]
                    m = curr_cont[4][4:]
                    m = m[:-1]
                self.cont[Name]=(tuple(int(q) for q in a.split(',')) if not(a is None) else None,\
                                 int(t) if not(t is None) else None,\
                                 int(m) if not(m is None) else None,\
                                 (tuple(int(q) for q in b.split(','))))
        #Считываем с файла данные контактов словарь cont.
        #except IndexError: print('Неправильный формат файла '+cat)



    def add_contact(self,Name,b,flag = False):
        if flag == False:
            self.cont[Name] = (None,None,None,b)
        else:
            self.create_keys(Name = Name)
        self.numcont += 1
        #добавляет контакт в оперативную память


    def save_contacts(self):
        print(self.cont)
        with open('cont.g','w') as file:
            file.writelines([str(self.numcont) + '\n'])
            for Name in self.cont:
                flag = False if self.cont[Name][0] is None else True
                lines = ['FULL\n'if  flag else 'PART\n','Name = '+Name+'\n',\
                    'a = '+','.join(str(x) for x in self.cont[Name][0])+'\n' if flag else None,\
                    't = '+ str(self.cont[Name][1]) + '\n' if flag else None,\
                    'm = ' + str(self.cont[Name][2])+'\n' if flag else None,\
                    'b = '+','.join(str(x) for x in self.cont[Name][3])+'\n','*****' + '\n']
                file.writelines([x for x in lines if not( x is None)])


    def create_keys(self,Name = None):

        n = int(input('Сколько чисел в ключе, не считая первого?: '))
        a = []
        s = 0
        a.append(int(input('Введите первое число ключа: ')))
        s = a[0]
        for i in range(n):
            x = random.randint(s,s+1000)
            s = s + x
            a.append(x)
        m = random.randint(s,s+1000)
        y = random.randint(0,int(math.sqrt(m)))
        p = Euclid.prost(2*m)
        p = list(p.intersection(set(range(m,2*m+1))))
        num = random.randint(0,len(p))
        t = p[num]
        b = [x*t%m for x in a]
        self.cont[Name]=(a,t,m,b)
        print(a,t,m,b,sep = '\n*\n')


    def decrypt(self,ch,Name):
        if Name in self.cont:
            if self.cont[Name][0] is None:
                print('Ошибка,ключ не найден.')
            else:
                e = str()
                p = []
                t1 = Euclid.Ras(self.cont[Name][1],self.cont[Name][2])[2]
                for i in range(len(ch)):
                    o = (ch[i] * t1)%self.cont[Name][2]
                    y = self.razl(self.cont[Name][0],o)
                    e += y
                print(e)
                msg = bytearray()
                for i in range(0,len(e)-(len(e)%8),8):
                    u = bytes([int(e[i:i+8],2)])
                    p.append(u)
                msg = b''.join(p)
                print(msg)
                msg = msg.decode('utf-8')
                return msg

        # O-блок из сверрастущего рюкзака
        #t-множитель,нужно найти t**-1 ,применяя Евклид рас,и домножить на t.
        #self.cont[Name][1] 1-играет роль t,заменем в дальнейшем на t**-1,который найдём.
    def razl(self,a,o):
        e = str()
        for i in range(len(a) - 1, -1, -1):
            if o - a[i] >= 0:
                e = '1' + e
                o -= a[i]
            else:
                e = '0' + e
        return e


    def UpdateCont(self):
        self.cont = dict()
        self.numcont = 0
        with open('cont.g', "r") as f:
            h = f.readlines()
            self.numcont = int(h[0])
            I = 1
            while len(h) > I:
                x = h.index('*****\n', I)
                curr_cont = h[I:x:1]
                Name = curr_cont[1][7:]
                Name = Name[:-1]
                if curr_cont[0] == 'FULL\n':
                    b = curr_cont[5][4:]
                    b = b[:-1]
                else:
                    b = curr_cont[2][4:]
                    b = b[:-1]
                I = x + 1
                a = None
                t = None
                m = None
                if curr_cont[0] == 'FULL\n':
                    a = curr_cont[2][4:]
                    a = a[:-1]
                    t = curr_cont[3][4:]
                    t = t[:-1]
                    m = curr_cont[4][4:]
                    m = m[:-1]
                self.cont[Name] = (tuple(int(q) for q in a.split(',')) if not (a is None) else None, \
                                   int(t) if not (t is None) else None, \
                                   int(m) if not (m is None) else None, \
                                   (tuple(int(q) for q in b.split(','))))


#c = mh()
#c.add_contact('Arteria',[10,12,14,5])
#c.add_contact(input('Как величать вашего друга?'),[10,12,123,13,132],flag = True)
#c.create_keys()
#c.save_contacts()
#d = c.encrypt(input('Для кого зашифровать?: '))
#d = c.encrypt('Artur')
#Все числа байтовой кодировки перевести в двоичную систему,записать в двоичной системе,
#разбить на блоки по 6 штук,добавить нули слева,если чисел не хватит,далее сделать умножение на числа открытого ключв для данного
# контакта,и резултирующий массив передать.
#print(c.decrypt(d),'-Расшифровка')
# оттестировать Create-Keys
# Сделать интерфейс на WX-python
# Сделать цифровую подпись
#оттестировать шифрование для любых контактов взятых из файлов и расшифрование.
# сделать так,чтобы у одного был открытый ключ,а другого закрытый.
