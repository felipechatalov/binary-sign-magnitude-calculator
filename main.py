import sys

_BITS = 16
_MAX_INT_SIZE = 2 ** (_BITS-1)
print(_MAX_INT_SIZE)

# soma +
# subtracao -
# multi. *
# div. /

def biggerThan(n1, n2):
    return 1 if n1 > n2 else 0

#TODO: rework how the number is transformed to str
def decToBin(n: int):
    return str((0 if n > 0 else 1)) + "0" * (_BITS - (len(bin(n))-1- (0 if n > 0 else 1))) + bin(n)[(2+(0 if n > 0 else 1)):]

def binToDec(n: str, i: int):
    print(n)
    if (i == _BITS-1):
        return int(n[i]) * (2**(_BITS-i-1)) * (-1 if n[0] == 1 else 1)
    return int(n[i]) * (2**(_BITS-i-1)) * (-1 if n[0] == 1 else 1) + binToDec(n, i+1)

def c_rec(n: str, i: int):
    # print(i)
    if i == 0:
        return "1" if n[0] == "0" else "0"

    return c_rec(n, i-1) + ("1" if n[i] == "0" else "0")


def complement(n: str):
    t = decToBin(1)
    y = c_rec(n, _BITS-1)
    print(t)
    print(y)
    return "1" + sum(y, t, 0, _BITS-1)

# faz a soma de 2 numeros binarios, excluindo sinal
def sum(n1: str, n2: str, co: int, i: int) -> str:
    # print(i)
    if i == 1:
        return str(int(n1[1]) ^ int(n2[1]) ^ co)
    

    # print(f'tamanho {len(n1)}, {len(n2)}')
    # print(f'index {i} -> {n1[i]}, {n2[i]}')
    # print(f'xor {int(n1[i]), int(n2[i]), co} {int(n1[i]) ^ int(n2[i]) ^ co}')

    v = 1 if int(n1[i]) == 1 and int(n2[i]) == 1 and co == 0 or int(n1[i]) == 1 and int(n2[i]) == 0 and co == 1 or int(n1[i]) == 0 and int(n2[i]) == 1 and co == 1 or int(n1[i]) == 1 and int(n2[i]) == 1 and co == 1 else 0
    return sum(n1, n2, v, i-1) + str(int(n1[i]) ^ int(n2[i]) ^ co)

def sumOperator(n1: str, n2: str):
    if (n1[0] != n2[0]):
        if biggerThan(abs(binToDec(n1, 1)), abs(binToDec(n2, 1))):
            return subOperator(n1, n2)
        else:
            return subOperator(n2, n1)
    # +n1 + -n2 = n1 - n2 -> sinal == maior entre n1 e n2
    # -n1 + +n2 = n2 - n1 -> sinal == maior entre n1 e n2

    # + & + = + -> 0
    # + & - = bigger
    # - & + = bigger
    # - & - = - -> 1
    
    # 0 + 0 = 0, 0
    # 0 + 1 = 1, 0
    # 1 + 0 = 1, 0
    # 1 + 1 = 0, 1

    #1 if 1 1 0 or 1 0 1 or 0 1 1 else 0
    # 0000100101101101 = 2413 
    # 1001010110101101 = 5549
    # 0001111100011010 = 7962
    return ("1" if n1[0] == "1" and n2[0] == "1" else "0") + sum(n1, n2, 0, _BITS-1)

    


    # -n1 - -n2 = - + + -> + - + subOp
    # -n1 - +n2 = -n1 - +n2 -> -n1 + -n2 sumOp (troca sinal de n2)
    # +n1 - -n2 = +n1 + +n2 -> +n1 + +n2 sumOp (troca sinal de n2)
    # + - + = + - + -> + - + subOp


def subOperator(n1, n2):
    # currently assuming n1 > n2, so the result of the subtracion is always positive       
    # TODO chcek all possible occureciencies to see when to use sub or sum


    if n1[0] != n2[0]:
        return "1" if n1[0] == "1" else "0" + sum(n1, n2, 0, _BITS-1) 

    
    #0101 5
    #     -
    #0010 2
    
    #0101 5
    #1110 2c
    #0011 3
    # 1001010110101101 = 5549
    # 0000100101101101 = 2413 
    # 0000110001000000 = 3136
    n2c = complement(n2)
    print(n2c)
    return "0" if binToDec(n1, 1) > binToDec(n2, 1) else "1" + sum(n1, n2c, 0, _BITS-1)


def multOperator():
    pass

def divOperator():
    pass




def handleInput(n1, n2):
    n1 = int(n1)
    n2 = int(n2)
    
    print(n1, n2)
    print(bin(n2))
    if n1 > _MAX_INT_SIZE or n2 > _MAX_INT_SIZE:
        # print(f'n1 or n2 exceeded max int size for {_BITS} bits')
        raise ValueError('n1 or n2 exceeded max int size for {_BITS} bits')
    
    sign1 = 0 if n1 > 0 else 1
    sign2 = 0 if n2 > 0 else 1

    # s1 = str(sign1)
    # bz1 = "0" * (_BITS - (len(bin(n1))-1-sign1))
    # bnumber1 = bin(n1)[(2+sign1):]
    # res1 = str(sign1) + "0" * (_BITS - (len(bin(n1))-1-sign1)) + bin(n1)[(2+sign1):]

    # s2 = str(sign2)
    # bz2 = "0" * (_BITS - (len(bin(n2))-1-sign2))
    # bnumber2 = bin(n2)[(2+sign2):]
    # res2 = str(sign2) + "0" * (_BITS - (len(bin(n2))-1-sign2)) + bin(n2)[(2+sign2):]

    # print(s1, bz1, bnumber1)
    # print(s2, bz2, bnumber2)

    # print(f"dectobin : \n{decToBin(n1)}")

    return decToBin(n1), decToBin(n2)

def main():
    
    print("$ digite um numero em base decimal, seguido por uma operacao (+, -, *, /) e outro numero decimal")
    print("$ ex: '2 * 3'")
    user = str(input())
    
    while user != "quit":
        n1, op, n2 = user.split(" ")
        bn1, bn2 = handleInput(n1, n2)
        print(bn1)
        print(bn2)
        print(len(bn1), len(bn2))

        if op == "+":
            r = sumOperator(bn1, bn2)
            print(r)
        elif op == "-":
            r = subOperator(bn1, bn2)
            print(r, binToDec(r, 1))
        elif op == "*":
            pass
        elif op == "/":
            pass

        # print(f'resultado: {r1, r2}')
        return 1
        



def terminal_mode(n1, op, n2):
    
    pass









if __name__ == "__main__":
    if sys.argv[1] == "-t" and len(sys.argv) == 4:
        terminal_mode(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "-u" and len(sys.argv) == 2:
        main()


