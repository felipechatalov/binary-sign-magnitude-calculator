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

def complement(n: str):

    # numero 1 em binario
    t = decToBin(1)
    
    # inverte todos os bits de n
    y = c_rec(n, _BITS-1)

    # soma o numero 1 com o complemento de n
    return "1" + sum(y, t, 0, _BITS-1)


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
    t = str(int(n1[i]) ^ int(n2[i]) ^ int(co))
    
    # 0 ^ 0 = 0
    # 0 ^ 1 = 1
    # 1 ^ 0 = 1
    # 1 ^ 1 = 0
    if i == 1:
        return t
    
    # o terceiro parametro (carry out) precisa ser 1 se 2 ou mais dos numeros forem 1, caso contrario v recebe 0    
    # 1 1 0 OR 1 0 1 OR 0 1 1 OR 1 1 1
   

    # v = 1 if int(n1[i]) == 1 and int(n2[i]) == 1 and co == 0 or int(n1[i]) == 1 and int(n2[i]) == 0 and co == 1 or int(n1[i]) == 0 and int(n2[i]) == 1 and co == 1 or int(n1[i]) == 1 and int(n2[i]) == 1 and co == 1 else 0
    # por fim retorna a soma de i-1 + a iteracao atual

    return sum(n1, n2, 1 if (int(n1[i]) + int(n2[i]) + int(co)) > 1 else 0, i-1) + t

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
        if abs(binToDec(n1)) > abs(binToDec(n2)):
            # 3 + -2 = pos
            # -3 + 2 = neg            
            return n1[0] + sum(n1, complement(n2), 0, _BITS-1)
        else:
            # 2 + -3 = neg
            # -2 + 3 = pos            
            return n2[0] + sum(n2, complement(n1), 0, _BITS-1)

    # caso contrario soamos os numeros

    # 2 + 3 = pos
    # 3 + 2 = pos
    # -2 + -3 = neg
    # -3 + -2 = neg
    return n1[0] + sum(n1, n2, 0, _BITS-1)



def subOperator(n1, n2):
    # operador de subtracao

    # caso o sinal seja diferente, realizamos a soma dos 2 numeros
    if n1[0] != n2[0]:
        # 2 - -3 = 2 + 3 pos
        # 3 - -2 = 3 + 2 pos
        # -2 - 3 = -2 - 3 neg
        # -3 - 2 = -3 - 2 neg
        return n1[0] + sum(n1, n2, 0, _BITS-1) 

    # caso contrario, colocamos o maior na frente e realizamos a subtracao
    if abs(binToDec(n1)) > abs(binToDec(n2)):
        #  3 -  2 = pos
        # -3 - -2 = -3 + 2 = neg
        return n1[0] + sum(n1, complement(n2), 0, _BITS-1)
    else:
        #  2 -  3 = neg
        # -2 - -3 = -2 + 3 = pos
        return ("1" if n1[0] == "0" else "0") + sum(n2, complement(n1), 0, _BITS-1)



def mulOperator(n1, n2):
    # print(f'max for {_BITS} bits multiplication,  number1 + number2 < {int(2**(_BITS/2))}')
    
    if n1 == "0"*_BITS or n1 == "1" + ("0"*(_BITS-1)) or n2 == "0"*_BITS or n2 == "1" + ("0"*(_BITS-1)):
        return "0"*_BITS
    # max is 255 * 128 (bitshiffting 7 bits to the left) = 32640
    # from 011111111 to 0111111110000000
    if len(remRedudant(n1)) + len(remRedudant(n2)) > _BITS:
        raise ValueError(f"Overflow, multiplicacao de numeros com mais de {_BITS} bits")
    
    hold = decToBin(0)
    # print("h: ", hold)

    for i in range(_BITS):
        if n2[_BITS-1-i] == "1":
            # print(f"sum: {hold} and {bitshift(n1, i, 'left')} len: {len(hold)}")
            # n1 * n2 = pos
            # n1 * -n2 = neg
            # -n1 * n2 = neg
            # -n1 * -n2 = pos
            hold = ("0" if n1[0] == n2[0] else "1") + sum(hold, bitshift(n1, i, "left"), 0, len(hold)-1)

    # print("h2: ", hold)
    # print("h2d: ", binToDec(hold))
    return hold
    # 11
    # 11
    
    #  11
    # 110
    # 1001

def divOperator(n1, n2):
    pass



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
        
        print(f'binary, complement and lenght of n1 {n1} {complement(n1)} {len(n1)}')
        print(f'binary, complement and lenght of n2 {n2} {complement(n2)} {len(n2)}')

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
            pass
        
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
    print(f'binary, complement and lenght of n1 {n1} {complement(n1)} {len(n1)}')
    print(f'binary, complement and lenght of n2 {n2} {complement(n2)} {len(n2)}')

    if op == "+":
        r = sumOperator(n1, n2)
        print(f'r: {r}, {binToDec(r)}')
    elif op == "-":
        r = subOperator(n1, n2)
        print(f'r: {r}, {binToDec(r)}')
    elif op == "*":
        r = mulOperator(n1, n2)
        # print(f'r: {r}, {binToDec(r)}')
        # n1 = bitshift(n1, 1, "left")
        # n2 = bitshift(n2, 1, "right")
        print(f'n1: {n1}, n2: {n2}')

    elif op == "/":
        pass
    
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
        # a = binToDec(divOperator(b1, b2))
        # r = n1 / n2
        print("not implemented")
        return
    print(f'{n1} {op} {n2} = {a}, should be {r} \t{a == r}')







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
        
        n1 = 20
        n2 = 30
        ops = ["+", "-", "*", "/"]
        print(n1, n2)
        for j in range(4):
            print(ops[j])
            for i in range(4):
                test2(n1*(1 if i < 2 else -1), n2*(1 if i%2 == 0 else -1), ops[j])
            
            #-n1 0
            #n1 0
            #0 -n2
            #0 n2
            print("with 0's")
            for i in range(4):
                test2(n1*(1 if i < 2 else 0)*(-1 if i%2 == 0 else 1), n2*(1 if i > 1 else 0)*(-1 if i%2 == 0 else 1), ops[j])
