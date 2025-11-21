import sys
import json

def main():
    print("[BOB] Iniciando processo de descriptografia...")

    # 1. Carregar a Chave Privada
    try:
        with open("privada.json", "r") as f:
            dados_chave = json.load(f)
            n = dados_chave["n"]
            d = dados_chave["d"]
            print(f"[BOB] Chave carregada. Modulo n termina em ...{str(n)[-5:]}")
    except FileNotFoundError:
        print("[ERRO] Arquivo 'privada.json' nao encontrado. Execute alice.py primeiro.")
        return

    # 2. Carregar a Mensagem Cifrada
    cifras = []
    try:
        with open("flag.enc", "r") as f:
            # Le cada linha e converte para int
            for linha in f:
                if linha.strip(): # Ignora linhas vazias
                    cifras.append(int(linha))
        print(f"[BOB] {len(cifras)} blocos criptografados lidos.")
    except FileNotFoundError:
        print("[ERRO] Arquivo 'flag.enc' nao encontrado.")
        return

    # 3. Descriptografar e Remontar
    bytes_recuperados = bytearray()

    print("[BOB] Decifrando blocos...")
    for c in cifras:
        # A magica do RSA: m = c^d mod n
        m = pow(c, d, n)
        
        # Converter int -> bytes
        # Precisamos calcular quantos bytes esse numero representa
        num_bytes = (m.bit_length() + 7) // 8
        
        # Nota: Se o bloco for nulo (byte 0x00), num_bytes seria 0. 
        # Em implementacoes robustas (PKCS), ha padding para evitar isso.
        # Aqui, assumimos que texto normal nao gera bloco 0 absoluto.
        chunk = m.to_bytes(num_bytes, byteorder='big')
        bytes_recuperados.extend(chunk)

    # 4. Resultado Final
    try:
        texto_plano = bytes_recuperados.decode('utf-8')
        print("\n" + "="*30)
        print(f"MENSAGEM SECRETA: {texto_plano}")
        print("="*30 + "\n")
    except UnicodeDecodeError:
        print("[ERRO] Falha na decodificacao. Chave errada ou arquivo corrompido.")
        print(f"Raw bytes: {bytes_recuperados}")

if __name__ == "__main__":
    main()