from json import detect_encoding
from multiprocessing.sharedctypes import Value
from secrets import token_bytes
import sys

_BITS = 16
_MAX_INT_SIZE = 2 ** (_BITS-1) - 1
print(_MAX_INT_SIZE)

# soma +
# subtracao -
# multi. *
# div. /


def decToBin(n: int):
    # separado em partes caso 1 linha seja confuso

    # coloca o sinal, 0 para positivo e 1 para negativo
    # p1 = ("0" if n > 0 else "1")
    
    # completa o numero com "0" ate o numero desejado de bits
    # p2 = "0" * (_BITS - (len(toBinary(n)))-1)
    
    # transforma um numero inteiro e decimal em binario
    # p3 = toBinary(n)
    
    # apos isso, junta tudo em um string de tamanaho _BITS
    return ("0" if n >= 0 else "1") + ("0" * (_BITS - (len(toBinary(n)))-1)) + toBinary(n)

# funcao recursiva para converter de decimal para binario
def bd_rec(n: str, i: int):
    
    # pega o bit da iteracao atual e ve se esta ativo ou nao
    # p1 = int(n[i])
    
    # se o bit estiver ativo, soma 2**(i-1) ao numero binario, (i-1 ja que o primeiro bit eh de sinal)
    # p2 = (2**(_BITS-i-1))
    
    # caso o sinal seja negativo, multiplica por -1
    # p3 = (-1 if n[0] == "1" else 1)

    # por fim soma este numero com a proxima chamada recursiva com i+=1
    t = int(n[i]) * (2**(_BITS-i-1)) * (-1 if n[0] == "1" else 1)
    # quando chegamos no bit 1, retorna o ultimo numero sem chamada recursiva pois o ultimo bit eh de sinal
    if (i == _BITS-1):
        return t
    return t + bd_rec(n, i+1)

# chamada da funcao recursiva acima, para que n seja necessario passar o 'i' como parametro
def binToDec(n):
    return bd_rec(n, 1)


# parte recursiva da funcao complement
def c_rec(n: str, i: int):
    
    if i == 0:
        return "1" if n[0] == "0" else "0"

    # comecando pelo ultimo bit, de posicao _BITS -1, e indo para a esquerda
    # invertendo todos os bits de 0 para 1 e vice-versa
    return c_rec(n, i-1) + ("1" if n[i] == "0" else "0")


# funcao para transformar um numero inteiro em binario
# ex: 37 -> 10101
def toBinary(n):
    n = abs(int(n))
    hold = ""
    while n > 0:
        # divide o numero por 2 e pega o resto para a string hold
        b = n//2
        hold += str(n%2)
        n = b
    # retorna a string hold invertida
    return hold[::-1]

# faz a soma de 2 numeros binarios, excluindo sinal
def sum(n1: str, n2: str, co: int, i: int) -> str:
    # t recebe a soma de n1 e n2 e o co(carry out da soma anterior)
    # para a soma eh usado 2 portas XOR
    # print(n1, n2)
    t = str(int(n1[i]) ^ int(n2[i]) ^ int(co))
    
    # 0 ^ 0 = 0
    # 0 ^ 1 = 1
    # 1 ^ 0 = 1
    # 1 ^ 1 = 0
    if i == 0:
        return t
    
    # o terceiro parametro (carry out) precisa ser 1 se 2 ou mais dos numeros forem 1, caso contrario v recebe 0    
    # 1 1 0 OR 1 0 1 OR 0 1 1 OR 1 1 1
   

    # v = 1 if int(n1[i]) == 1 and int(n2[i]) == 1 and co == 0 or int(n1[i]) == 1 and int(n2[i]) == 0 and co == 1 or int(n1[i]) == 0 and int(n2[i]) == 1 and co == 1 or int(n1[i]) == 1 and int(n2[i]) == 1 and co == 1 else 0
    # por fim retorna a soma de i-1 + a iteracao atual

    return sum(n1, n2, 1 if (int(n1[i]) + int(n2[i]) + int(co)) > 1 else 0, i-1) + t

def absGreater(n1: str, n2: str):
    i = 1
    while i < _BITS and n1[i] == n2[i] :
        i += 1
    if i == _BITS:
        return False
    if n1[i] == "1":
        return True
    return False
    

def bitshift(n, b, dir):
    if dir == "right":
        return ("0"*b) + n[:-b]
    return n[b:] + ("0"*b)

def remRedudant(n):
    for i in range(_BITS-1):
        if n[i+1] == "1":
            return n[i+1:]

def sumOperator(n1: str, n2: str):
    # operador de soma
    
    # caso o sinal seja diferente, coloque o maior em valor absoluto na frente
    # e fazemos a subtracao
    if (n1[0] != n2[0]):
        if absGreater(n1, n2):
            # 3 + -2 = pos
            # -3 + 2 = neg            
            return n1[0] + sub(n1[1:], n2[1:], 0, _BITS-2)
        else:
            # 2 + -3 = neg
            # -2 + 3 = pos            
            return n2[0] + sub(n2[1:], n1[1:], 0, _BITS-2)

    # caso contrario soamos os numeros

    # 2 + 3 = pos
    # 3 + 2 = pos
    # -2 + -3 = neg
    # -3 + -2 = neg
    return n1[0] + sum(n1[1:], n2[1:], 0, _BITS-2)


def sub(n1, n2, co, i):
    # equacao de subtracao de numeros binarios

    # n1  n2 cin cout/r 
    # 0 - 0 - 0 = 0   0
    # 0 - 0 - 1 = 1   1    
    # 0 - 1 - 0 = 1   1       
    # 0 - 1 - 1 = 1   0     
    # 1 - 0 - 0 = 0   1    
    # 1 - 0 - 1 = 0   0
    # 1 - 1 - 0 = 0   0
    # 1 - 1 - 1 = 1   1  
    
    # r -> n1 ^ n2 ^ cin
    # cout -> n1 - (n2 + cin) < 0

    t = str( (int(n1[i]) ^ int(n2[i]) ) ^ co)
    # print(f'n1: {n1[i]} n2: {n2[i]} co: {co} t: {t}')
    if i == 0:
        return t
    return sub(n1, n2, 1 if (int(n1[i]) - (int(n2[i]) + co)) < 0 else 0, i-1) + t

     

def subOperator(n1, n2):
    # operador de subtracao

    # 0101010101

    # n1 - n2 -> maior abs na frente e subtracao sem sinal, sinal positivo caso nao precise
    # trocar posicoes, se nao, negativo
    # n1 - -n2 -> sum n1 + n2 com sinal positivo sempre
    # -n1 - n2 -> sum n1 + n2 com sinal negativo sempre
    # -n1 - -n2 -> maior na frente e subtracao sem sinal, sinal negativo caso nao precise
    # trocar posicoes, se nao, positivo
    

    if n1[0] != n2[0]:
        # print("sum")
        return n1[0] + sum(n1[1:], n2[1:], 0, _BITS-2)

    # sinais iguais
    if absGreater(n1, n2):
        return n1[0] + sub(n1[1:], n2[1:], 0, _BITS-2)
    else:
        return ("0" if n2[0] == "1" else "1") + sub(n2[1:], n1[1:], 0, _BITS-2)


def mulOperator(n1, n2):
    # print(f'max for {_BITS} bits multiplication,  number1 + number2 < {int(2**(_BITS/2))}')
    
    if n1 == "0"*_BITS or n1 == "1" + ("0"*(_BITS-1)) or n2 == "0"*_BITS or n2 == "1" + ("0"*(_BITS-1)):
        return "0"*_BITS
    # max is 255 * 128 (bitshiffting 7 bits to the left) = 32640
    # from 011111111 to 0111111110000000
    if len(remRedudant(n1)) + len(remRedudant(n2)) > _BITS:
        raise ValueError(f"Overflow, multiplicacao de numeros com mais de {_BITS} bits")
    
    count = _BITS/2
    c = "0"
    a = "00000000"
    q = n1[-8:]
    m = n2[-8:]

    print(f' c  a        q       m')
    print(f'{c} {a} {q} {m}')

    while count != 0:
        # print(f'{c} {a} {q} {m}')
        if q[-1] == "1":
           a = sum("0" + a, "0" + m, 0, len(a))
           c, a = a[0], a[1:]

        full = bitshift(c+a+q, 1, "right")
        c = full[0]
        a = full[1:9]
        q = full[9:]
        count -= 1
        print(c+a+q+m)
        print(f'{c} {a} {q} {m}')
    # print(a+q)
    return ("0" if n1[0] == n2[0] else "1") + (a+q)[1:]

def divOperator(n1, n2):
    # D dividido por V, resultado em Q e resto em R
    # d = n1
    # v = n2

    if n2 == "0"*_BITS or n2 == "1" + ("0"*(_BITS-1)):
        raise ValueError(f"Divisao por zero")
    if n1 == "0"*_BITS or n1 == "1" + ("0"*(_BITS-1)):
        print(f'0 divided by {n2} = 0')
        return "0"*_BITS, "0"*_BITS

    sign = "0" if n1[0] == n2[0] else "1"
    d = "0"+n1[1:]
    v = "0"+n2[1:]

    q = 0; r = d
    # print(f'dividendo: {n1} {binToDec(n1)}  divisor: {n2} {binToDec(n2)}')
    while absGreater(d, v) or d == v:
        d = "0"+sub(d[1:], v[1:], 0, _BITS-2)
        q += 1
        r = d
        print(f'n1: {n1} {binToDec(n1)}  q: {q}  r: {r} {binToDec(r)}')
    # print(f'q: {decToBin(q)} r: {r}')
    return sign + decToBin(q)[1:], n1[0] + r[1:]


def handleInput():
    print("$ digite um numero em base decimal, seguido por uma operacao (+, -, *, /) e outro numero decimal")
    print("$ ex: '2 * 3'")
    usr = input().split(" ")
    if usr[0] == "quit":
        return 0, "quit", 0
    if len(usr) != 3:
        raise ValueError("Invalid input, ex: 2 * 3")
    if usr[1] not in ["+", "-", "*", "/"]:
        raise ValueError("Invalid operator, ex: +, -, *, /")
    try:
        n1, n2 = int(usr[0]), int(usr[2])
    except:
        raise ValueError("Invalid input, values must be integers")
    if n1 > _MAX_INT_SIZE or n2 > _MAX_INT_SIZE:
        raise ValueError('n1 or n2 exceeded max int size for {_BITS} bits')

    return decToBin(n1), usr[1], decToBin(n2)

def main():
    
    
    n1, op, n2 = handleInput()
    print(n1, op, n2)
    while op != "quit":
        
        print(f'binary and lenght of n1 {n1}  {len(n1)}')
        print(f'binary and lenght of n2 {n2}  {len(n2)}')

        if op == "+":
            r = sumOperator(n1, n2)
            print(f'r: {r}, {binToDec(r)}')
        elif op == "-":
            r = subOperator(n1, n2)
            print(f'r: {r}, {binToDec(r)}')
        elif op == "*":
            r = mulOperator(n1, n2)
            print(f'r: {r}, {binToDec(r)}')
        elif op == "/":
            r, re = mulOperator(n1, n2)
            print(f'r: {r}, {binToDec(r)}')
            print(f're: {re}, {binToDec(re)}')
        
        n1, op, n2 = handleInput()
    return 1

def terminal_mode(n1, op, n2):
        
    
    if op not in ["+", "-", "*", "/"]:
        raise ValueError("Invalid operator, ex: +, -, *, /")
    try:
        n1, n2 = int(n1), int(n2)
    except:
        raise ValueError("Invalid input, values must be integers")
    if n1 > _MAX_INT_SIZE or n2 > _MAX_INT_SIZE:
        raise ValueError('n1 or n2 exceeded max int size for {_BITS} bits')

    
    n1 = decToBin(n1)
    n2 = decToBin(n2)
    print(f'binary and lenght of n1 {n1} {len(n1)}')
    print(f'binary and lenght of n2 {n2} {len(n2)}')

    if op == "+":
        r = sumOperator(n1, n2)
        print(f'r: {r}, {binToDec(r)}')
    elif op == "-":
        r = subOperator(n1, n2)
        print(f'r: {r}, {binToDec(r)}')
    elif op == "*":
        r = mulOperator(n1, n2)
    elif op == "/":
        r, re = divOperator(n1, n2)
        print(f'r: {r}, {re}  {binToDec(r), binToDec(re)}')
    return 1

 
def test2(n1, n2, op):
    b1 = decToBin(n1)
    b2 = decToBin(n2)


    a, r = 0, 0
    if op == '+':
        a = binToDec(sumOperator(b1, b2))
        r = n1 + n2
    elif op == '-':
        a = binToDec(subOperator(b1, b2))
        r = n1 - n2
    elif op == '*':
        a = binToDec(mulOperator(b1, b2))
        r = n1 * n2
    elif op == '/':
        if n2 == 0:
            print(f'divisao por 0, nao entrou')
            return
        a, b = divOperator(b1, b2)
        a = binToDec(a)
        r = int(n1 / n2)
    print(f'\t{n1} {op} {n2} = {a}, should be {r}    \t{a == r}')
    if op == '/':
        print(f'\treminder = {binToDec(b)} \t\t')
    return






if __name__ == "__main__":
    if sys.argv[1] == "-t" and len(sys.argv) == 5:
        print("terminal mode")
        terminal_mode(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "-u" and len(sys.argv) == 2:
        print("user mode")
        main()
    elif sys.argv[1] == "-x" and len(sys.argv) == 2:
        print("test mode")
        # n1 = 2413 # "0000100101101101"
        # n2 = 5549 # "0001010110101101" 
        # test(n1, n2)
        
        n1 = 2
        n2 = 3
        ops = ["+", "-", "*", "/"]
        print(n1, n2)
        for j in range(4):
            print(ops[j])

            print('-------------------')
            for i in range(4):
                test2(n1*(1 if i < 2 else -1), n2*(1 if i%2 == 0 else -1), ops[j])
            for i in range(4):
                test2(n2*(1 if i < 2 else -1), n1*(1 if i%2 == 0 else -1), ops[j])
            
            #-n1 0
            #n1 0
            #0 -n2
            #0 n2
            print("with 0's")
            for i in range(4):
                test2(n1*(1 if i < 2 else 0)*(-1 if i%2 == 0 else 1), n2*(1 if i > 1 else 0)*(-1 if i%2 == 0 else 1), ops[j])
            print('-------------------')
