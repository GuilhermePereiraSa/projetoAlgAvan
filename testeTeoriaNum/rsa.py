import sys

def crivo(n):
    numeros = [True] * (n+1)
    numeros[0] = numeros[1] = False
    primos = []


    for numero, primo in enumerate(numeros):

        if primo:
            primos.append(numero)

            for i in range(2*numero, n+1, numero):
                numeros[i] = False


    return primos


# Algoritmo RSA das ruas (Matemática Discreta) feito baseado na Teoria dos Números


def mdc(a, b):
    if b == 0:
        return a

    return mdc(b, a % b)

# p e q primos, geralmente grandes
def main():
    # Escolha de primos aleatorios grandes, ou, digitados
    p, q = [int(x) for x in input().split()]

    # n, módulo
    # faz parte tanto da chave pública quanto da chave privada
    n = p*q


    # * calculo do totiente theta(n) = (p-1)(q-1)
    # para calculo posterior do inverso
    theta = (p-1)*(q-1)


    # chave pública (n, e), sendo e o expoente escolhido
    # e = 3 para calculo rápido
    # e deve apenas ser restringido por: ser coprimo de theta(n), isso é, mdc(e, theta(n)) = 1

    while True:
        e = int(input())
        if mdc(e, theta) == 1:
            break
    
        print("Digite um valor válido de e")


    # parte da criptografia
    # C(b), sendo b o bloco escolhido

    print("Digite o valor a ser criptografado")
    # ou pegar todo o bloco e ir criptografando, mais real

    b = sys.stdin.readline()

    c = pow(b, e, n)

    print(c)

    # parte da descriptografia 


    # chave privada (n, x)
    # tal que x é o inverso de 3 mod (p-1)(q-1)
    x = pow(e, -1, theta)

    d = pow(c, d, n)

    print(c)

if __name__ == "__main__":
    main()