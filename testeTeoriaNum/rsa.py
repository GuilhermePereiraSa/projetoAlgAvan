import sys

# Algoritmo Euclediano
def mdc(a, b):
    if b == 0:
        return a

    return mdc(b, a % b)

def main():
    # Escolha de primos aleatorios grandes, ou, digitados
    # p e q primos, geralmente grandes
    
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


    # Solução de Padding -  OAEP ou PKCS#1 v1.5 - colocar lixo aleatorio
    
    # Conversão bytes <-> int: Usa int.from_bytes() para criptografar e int.to_bytes() para descriptografar.

    print("Digite o valor a ser criptografado")
    # string -> bytes ( .encode('utf-8') ) -> numero inteiro ( ). criptografar este numero
    
    # Quais blocos podemos criptografar? Limitação pelo modulo n, sempre menor
    
    # ou pegar todo o bloco e ir criptografando, mais real

    b = sys.stdin.readline()

    c = pow(b, e, n)

    print(c)

    # parte da descriptografia 


    # chave privada (n, x)
    # tal que x é o inverso de 3 mod (p-1)(q-1)
    x = pow(e, -1, theta)

    d = pow(c, x, n)

    print(d)

if __name__ == "__main__":
    main()