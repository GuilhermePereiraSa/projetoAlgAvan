import sys

def mdc(a, b):
    if b == 0:
        return a
    return mdc(b, a % b)

def main():
    print("--- GERACAO DE CHAVES ---")
    # Usaremos valores padrao se o usuario der Enter para facilitar o teste
    # Primos maiores para garantir que n > 255 (minimo para 1 byte)
    print("Digite dois primos (ex: 101 103) ou Enter para padrao (104729 104723).")
    
    entrada = input("Primos (p q): ")
    if not entrada.strip():
        p, q = 104729, 104723
        print(f"Usando primos padrao: {p}, {q}")
    else:
        p, q = [int(x) for x in entrada.split()]

    n = p * q
    theta = (p - 1) * (q - 1)
    
    print(f"Modulo n: {n}")
    print(f"Totiente theta: {theta}")

    # Calculo do tamanho do bloco
    # O numero gerado pelo bloco DEVE ser estritamente menor que n.
    # bit_length() - 1 garante margem de seguranca.
    # // 8 converte bits para bytes.
    tamanho_bloco = (n.bit_length() - 1) // 8
    
    print(f"\n[CONFIGURACAO DE BLOCO]")
    print(f"Capacidade de n: {n.bit_length()} bits")
    print(f"Tamanho maximo do bloco seguro: {tamanho_bloco} bytes")
    
    if tamanho_bloco < 1:
        print("Erro: 'n' e muito pequeno para criptografar sequer 1 caractere (byte).")
        print("Use primos maiores (p, q > 16).")
        return

    # Escolha de 'e'
    print(f"\nEscolha 'e' coprimo de {theta}.")
    while True:
        try:
            val = input(f"Sugestao 65537 (ou Enter para 65537): ")
            if not val:
                e = 65537
            else:
                e = int(val)
            
            if mdc(e, theta) == 1:
                break
            print("Erro: 'e' nao e coprimo.")
        except ValueError:
            pass

    # --- CRIPTOGRAFIA ---
    print("\n--- CRIPTOGRAFIA ---")
    print("Digite sua frase longa:")
    msg_str = sys.stdin.readline().strip()
    msg_bytes = msg_str.encode('utf-8')

    cipher_blocks = []

    print(f"\nProcessando {len(msg_bytes)} bytes em blocos de {tamanho_bloco} bytes...")

    # Loop para fatiar a mensagem
    for i in range(0, len(msg_bytes), tamanho_bloco):
        # Pega o pedaco (slice)
        bloco = msg_bytes[i : i + tamanho_bloco]
        
        # Converte pedaco para Inteiro
        m_int = int.from_bytes(bloco, byteorder='big')
        
        # Criptografa: c = m^e mod n
        c = pow(m_int, e, n)
        
        cipher_blocks.append(c)
        print(f" Bloco {i//tamanho_bloco}: '{bloco}' -> int({m_int}) -> Cifrado({c})")

    print(f"\nLista de blocos cifrados: {cipher_blocks}")

    # --- DESCRIPTOGRAFIA ---
    print("\n--- DESCRIPTOGRAFIA ---")
    
    # Calculo da chave privada d
    d = pow(e, -1, theta)
    print(f"Chave Privada d calculada.")

    decrypted_bytes_stream = bytearray()

    for c in cipher_blocks:
        # Decifrar: m = c^d mod n
        m_decifrado = pow(c, d, n)
        
        # Converter de volta para bytes
        # Precisamos saber quantos bytes extrair. Usamos o tamanho_bloco maximo
        # ou calcula-se baseado no tamanho do numero.
        # (m.bit_length() + 7) // 8 calcula o teto de bytes necessarios
        num_bytes_necessarios = (m_decifrado.bit_length() + 7) // 8
        
        part_bytes = m_decifrado.to_bytes(num_bytes_necessarios, byteorder='big')
        
        decrypted_bytes_stream.extend(part_bytes)

    try:
        msg_final = decrypted_bytes_stream.decode('utf-8')
        print(f"\nMensagem remontada: {msg_final}")
    except UnicodeDecodeError:
        print("\nErro: Falha ao decodificar UTF-8. Os blocos podem estar corrompidos ou desalinhados.")
        print(f"Bytes brutos: {decrypted_bytes_stream}")

if __name__ == "__main__":
    main()