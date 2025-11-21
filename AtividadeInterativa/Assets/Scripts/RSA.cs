using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Numerics;
using System.Text;
using System.Collections.Generic;
using System.Linq;

public class RSA : MonoBehaviour
{
    string mensagem;
    int p1, q1, p2, q2;

    // Usamos BigInteger para chaves e cálculos
    BigInteger n1, phi1, e1, d1;
    BigInteger n2, phi2, e2, d2;

    // Texto cifrado/decifrado (cada bloco é um inteiro em string, separado por espaço)
    public string mensagemCifrada1, mensagemDecifrada1;
    public string mensagemCifrada2, mensagemDecifrada2;

    public TMP_InputField mensagemInputField;

    [SerializeField] private TMP_Text criptografado1Text;
    [SerializeField] private TMP_Text descriptografado1Text;
    [SerializeField] private TMP_Text criptografado2Text;
    [SerializeField] private TMP_Text descriptografado2Text;

    [SerializeField] private TMP_Text mensagemMatematica;

    void Start()
    {
        // primes exemplo
        p1 = 61;
        q1 = 53;
        p2 = 47;
        q2 = 71;

        // inicializar chaves como 0
        n1 = phi1 = e1 = d1 = 0;
        n2 = phi2 = e2 = d2 = 0;
    }

    void Update()
    {
        criptografado1Text.text = "Mensagem Cifrada por Um: " + mensagemCifrada2;
        descriptografado1Text.text = "Mensagem Decifrada por Um: " + mensagemDecifrada1;
        criptografado2Text.text = "Mensagem Cifrada por Dois: " + mensagemCifrada1;
        descriptografado2Text.text = "Mensagem Decifrada por Dois: " + mensagemDecifrada2;
    }

    public void AtualizarMensagem()
    {
        mensagem = mensagemInputField.text;
    }

    public void AtualizarMensagemMatematica(int chavePublica, int chavePrivada, int p, int q, int n, string c, string cifrado)
    {
        mensagemMatematica.text = "<color=\"red\">Chave Pública: </color>(" + chavePublica + ", " + n + ")\n" +
                   "<color=\"red\">Chave Privada: </color>(" + chavePrivada + ", " + n + ")\n" +
                   "<color=\"red\">Primos: </color>(p = " + p + ", q = " + q + ")\n" +
                   "<color=\"red\">Primeiro caractere: </color>" + c + "<color=\"red\"> (converte para número)</color> ^ " + chavePublica + " mod " + n + " = " + cifrado + "\n" +
                   "<color=\"red\">Decifrando: </color>" + cifrado + " ^ " + chavePrivada + " mod " + n + " = " + c + "<color=\"red\"> (converte para caractere)</color>";
    }

    public void CalcularPhi1()
    {
        n1 = (BigInteger)p1 * (BigInteger)q1;
        phi1 = (BigInteger)(p1 - 1) * (BigInteger)(q1 - 1);
    }

    public void CalcularPhi2()
    {
        n2 = (BigInteger)p2 * (BigInteger)q2;
        phi2 = (BigInteger)(p2 - 1) * (BigInteger)(q2 - 1);
    }

    public void GerarE1()
    {
        e1 = 3;
        while (phi1 % e1 == 0)
        {
            e1 += 2;
        }
    }

    public void GerarE2()
    {
        e2 = 3;
        while (phi2 % e2 == 0)
        {
            e2 += 2;
        }
    }

    public void GerarD1()
    {
        d1 = 2;
        while ((d1 * e1) % phi1 != 1)
        {
            d1++;
        }
    }

    public void GerarD2()
    {
        d2 = 2;
        while ((d2 * e2) % phi2 != 1)
        {
            d2++;
        }
    }

    // --- Funções de envio/recebimento - mantém sua API original mas agora cifram/decifram toda a mensagem ---

    // "Um" envia mensagem para "Dois" -> cifra usando chave pública de Dois (e2,n2)
    public void UmEnviaMsg()
    {
        CalcularPhi1();
        GerarE1();
        GerarD1();
        // Cifrar1 irá usar (e2,n2) como chave pública do receptor e gravar em mensagemCifrada2
        Cifrar1();
        Debug.Log("Mensagem original: " + mensagem);
        Debug.Log("Mensagem cifrada por Um (destinada a Dois): " + mensagemCifrada2);
        AtualizarMensagemMatematica((int)e2, (int)d2, p2, q2, (int)n2,
            mensagem.Length > 0 ? (mensagem[0]).ToString() : "N/A",
            mensagemCifrada2.Split(' ').Length > 0 ? mensagemCifrada2.Split(' ')[0] : "N/A");
    }

    // "Dois" envia mensagem para "Um" -> cifra usando chave pública de Um (e1,n1)
    public void DoisEnviaMsg()
    {
        CalcularPhi2();
        GerarE2();
        GerarD2();
        // Cifrar2 irá usar (e1,n1) como chave pública do receptor e gravar em mensagemCifrada1
        Cifrar2();
        Debug.Log("Mensagem cifrada por Dois (destinada a Um): " + mensagemCifrada1);
        AtualizarMensagemMatematica((int)e1, (int)d1, p1, q1, (int)n1,
            mensagem.Length > 0 ? (mensagem[0]).ToString() : "N/A",
            mensagemCifrada1.Split(' ').Length > 0 ? mensagemCifrada1.Split(' ')[0] : "N/A");
    }

    // Um recebe (decifra mensagem que foi cifrada para Um -> mensagemCifrada1) usando d1,n1
    public void UmRecebeMsg()
    {
        Decifrar1();
        Debug.Log("Mensagem decifrada por Um: " + mensagemDecifrada1);
    }

    // Dois recebe (decifra mensagem que foi cifrada para Dois -> mensagemCifrada2) usando d2,n2
    public void DoisRecebeMsg()
    {
        Decifrar2();
        Debug.Log("Mensagem decifrada por Dois: " + mensagemDecifrada2);
    }

    // --- Implementação das funções de cifrar e decifrar ---

    // Cifrar1: Um cifra a mensagem para Dois usando (e2, n2) e grava em mensagemCifrada2
    public void Cifrar1()
    {
        if (string.IsNullOrEmpty(mensagem))
        {
            mensagemCifrada2 = "";
            return;
        }

        // garante que a chave pública do receptor exista
        if (n2 == 0)
        {
            CalcularPhi2();
            GerarE2();
            GerarD2(); // opcional, mas gera d2 também
        }

        byte[] bytes = Encoding.UTF8.GetBytes(mensagem);
        List<string> pieces = new List<string>();

        foreach (byte b in bytes)
        {
            BigInteger m = new BigInteger(b); // valor do byte
            BigInteger c = BigInteger.ModPow(m, e2, n2); // c = m^e2 mod n2
            pieces.Add(c.ToString());
        }

        mensagemCifrada2 = string.Join(" ", pieces);
    }

    // Cifrar2: Dois cifra a mensagem para Um usando (e1, n1) e grava em mensagemCifrada1
    public void Cifrar2()
    {
        if (string.IsNullOrEmpty(mensagem))
        {
            mensagemCifrada1 = "";
            return;
        }

        // garante que a chave pública do receptor exista
        if (n1 == 0)
        {
            CalcularPhi1();
            GerarE1();
            GerarD1();
        }

        byte[] bytes = Encoding.UTF8.GetBytes(mensagem);
        List<string> pieces = new List<string>();

        foreach (byte b in bytes)
        {
            BigInteger m = new BigInteger(b);
            BigInteger c = BigInteger.ModPow(m, e1, n1);
            pieces.Add(c.ToString());
        }

        mensagemCifrada1 = string.Join(" ", pieces);
    }

    // Decifrar1: Um decifra mensagemCifrada1 usando d1,n1 (mensagem enviada por Dois)
    public void Decifrar1()
    {
        if (string.IsNullOrEmpty(mensagemCifrada1))
        {
            mensagemDecifrada1 = "";
            return;
        }

        if (d1 == 0 || n1 == 0)
        {
            CalcularPhi1();
            GerarE1();
            GerarD1();
        }

        string[] parts = mensagemCifrada1.Split(' ');
        List<byte> bytes = new List<byte>();

        foreach (string part in parts)
        {
            if (string.IsNullOrWhiteSpace(part)) continue;
            BigInteger c = BigInteger.Parse(part);
            BigInteger m = BigInteger.ModPow(c, d1, n1);
            byte b = (byte)(m); // cada bloco representa 1 byte
            bytes.Add(b);
        }

        mensagemDecifrada1 = Encoding.UTF8.GetString(bytes.ToArray());
    }

    // Decifrar2: Dois decifra mensagemCifrada2 usando d2,n2 (mensagem enviada por Um)
    public void Decifrar2()
    {
        if (string.IsNullOrEmpty(mensagemCifrada2))
        {
            mensagemDecifrada2 = "";
            return;
        }

        if (d2 == 0 || n2 == 0)
        {
            CalcularPhi2();
            GerarE2();
            GerarD2();
        }

        string[] parts = mensagemCifrada2.Split(' ');
        List<byte> bytes = new List<byte>();

        foreach (string part in parts)
        {
            if (string.IsNullOrWhiteSpace(part)) continue;
            BigInteger c = BigInteger.Parse(part);
            BigInteger m = BigInteger.ModPow(c, d2, n2);
            byte b = (byte)(m);
            bytes.Add(b);
        }

        mensagemDecifrada2 = Encoding.UTF8.GetString(bytes.ToArray());
    }
}
