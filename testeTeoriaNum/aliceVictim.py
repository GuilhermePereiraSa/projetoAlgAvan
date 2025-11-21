import sys
import json

# --- Funcoes Auxiliares ---
def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def get_block_size(n):
    # Retorna quantos bytes cabem em n (com margem de seguranca)
    return (n.bit_length() - 1) // 8

# --- Main ---
def main():
    print("[ALICE] Gerando chaves e criptografando...")
    
    # 1. Parametros (Exemplo com primos medios para teste)
    # Em um CTF real, esses primos seriam gigantes.
    p = 104729
    q = 104723
    
    n = p * q
    theta = (p - 1) * (q - 1)
    e = 65537 # Padrao industrial
    
    # Calculo de d (inverso modular)
    d = pow(e, -1, theta)
    
    print(f"[ALICE] Chaves geradas.")
    print(f" -> n: {n}")
    print(f" -> e: {e}")
    print(f" -> d: {d} (Segredo!)")

    # 2. Salvar a Chave Privada (JSON)
    # Salvamos n e d, pois sao necessarios para descriptografar
    chave_privada = {"n": n, "d": d}
    with open("privada.json", "w") as f:
        json.dump(chave_privada, f)
    print("[ALICE] Arquivo 'privada.json' salvo.")

    # 3. Criptografia
    mensagem = "FLAG{Rsa_Com_B1ocos_Eh_Legal}"
    print(f"[ALICE] Criptografando: {mensagem}")
    
    msg_bytes = mensagem.encode('utf-8')
    block_size = get_block_size(n)
    
    lista_cifrada = []
    
    # Loop de blocos
    for i in range(0, len(msg_bytes), block_size):
        bloco = msg_bytes[i : i + block_size]
        m_int = int.from_bytes(bloco, 'big')
        c = pow(m_int, e, n)
        lista_cifrada.append(c)

    # 4. Salvar o arquivo criptografado
    # Vamos salvar linha por linha para facilitar a leitura
    with open("flag.enc", "w") as f:
        for c in lista_cifrada:
            f.write(str(c) + "\n")
            
    print("[ALICE] Arquivo 'flag.enc' salvo com sucesso.")
    print("--- FIM DA TRANSMISSAO ---\n")

if __name__ == "__main__":
    main()