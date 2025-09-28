#!/usr/bin/env python3
#----Autor: Zenio Almeida zn-dv@outlook.com 2197700396020
#---- última atualização: 28/09/25
''' Como usar
Atualizar sistema
python3 manutencao.py --atualizar
Limpar sistema
python3 manutencao.py --limpar
Verificar falhas de login
python3 manutencao.py --seguranca
Executar tudo
python3 manutencao.py --tudo '''

import subprocess
import argparse
from datetime import datetime

LOG_FILE = "manutencao.log"

def registrar_log(texto):
    """Salva mensagens em um arquivo de log com timestamp."""
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {texto}\n")

def executar_comando(comando, descricao=None):
    """
    Executa um comando no shell, exibe a saída e registra no log.
    """
    try:
        print(f"\n>>> Executando: {descricao or comando}")
        processo = subprocess.run(
            comando,
            shell=True,
            text=True,
            capture_output=True
        )
        if processo.returncode == 0:
            print(processo.stdout.strip() or "✅ Comando executado com sucesso.")
            registrar_log(f"SUCESSO: {descricao or comando}\n{processo.stdout}")
        else:
            print(f"❌ Erro ao executar: {descricao or comando}")
            print(processo.stderr.strip())
            registrar_log(f"ERRO: {descricao or comando}\n{processo.stderr}")
    except FileNotFoundError:
        print(f"❌ Comando não encontrado: {comando}")
        registrar_log(f"ERRO: comando não encontrado -> {comando}")

def atualizar_sistema():
    executar_comando("sudo apt update", "Atualizando lista de pacotes")
    executar_comando("sudo apt upgrade -y", "Atualizando pacotes")

def limpar_sistema():
    executar_comando("sudo apt autoremove -y", "Removendo pacotes órfãos")
    executar_comando("sudo apt clean", "Limpando cache do APT")

def verificar_falhas_login():
    comando = 'grep "Failed password" /var/log/auth.log'
    print("\n>>> Verificando falhas de login...")
    resultado = subprocess.run(comando, shell=True, text=True, capture_output=True)
    if resultado.stdout:
        print("⚠️ Foram encontradas falhas de login:")
        print(resultado.stdout)
        registrar_log("Falhas de login encontradas:\n" + resultado.stdout)
    else:
        print("Nenhuma falha de login encontrada.")
        registrar_log("Nenhuma falha de login encontrada.")

def main():
    parser = argparse.ArgumentParser(
        description="Script de manutenção para sistemas Ubuntu/Debian"
    )

    parser.add_argument("--atualizar", action="store_true", help="Atualizar o sistema")
    parser.add_argument("--limpar", action="store_true", help="Limpar pacotes e cache")
    parser.add_argument("--seguranca", action="store_true", help="Verificar falhas de login")
    parser.add_argument("--tudo", action="store_true", help="Executar todas as etapas")

    args = parser.parse_args()

    print("\n--- ROTINA DE MANUTENÇÃO ---")

    if args.tudo:
        atualizar_sistema()
        limpar_sistema()
        verificar_falhas_login()
    else:
        if args.atualizar:
            atualizar_sistema()
        if args.limpar:
            limpar_sistema()
        if args.seguranca:
            verificar_falhas_login()

    print("\n--- Rotina concluída. Logs salvos em manutencao.log ---")

if __name__ == "__main__":
    main()


