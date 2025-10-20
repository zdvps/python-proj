#!/usr/bin/env python3
#----------------------
# "---- Autor: Zenio zndv@outlook.com 21977036020
#"---- última atualização: 19/09/2025
# ---- testando o transformer AI no terminal

import argparse
from transformers import pipeline

def main():
    """
    Um script de linha de comando para interagir com um modelo de linguagem.
    """
    parser = argparse.ArgumentParser(description="Interaja com um modelo de linguagem via terminal.")
    parser.add_argument("prompt", type=str, help="O texto inicial para o modelo.")
    args = parser.parse_args()

    # Carregue o modelo, troque 'openai-community/gpt2' por um modelo de sua escolha
    # A primeira vez que você rodar, o modelo será baixado.
    generator = pipeline("text-generation", model="openai-community/gpt2")

    print("Gerando texto...")

    # Gerar o texto
    output = generator(args.prompt, max_length=50, num_return_sequences=1)

    print("\n" + "="*20 + " Resposta " + "="*20)
    print(output[0]['generated_text'])
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
