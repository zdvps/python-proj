#!/usr/bin/env python3

import subprocess
import os
import sys

# Funções para exibir mensagens com cores
def info(mensagem):
    """Exibe uma mensagem informativa em verde."""
    print(f"\033[1;32m[INFO]\033[0m {mensagem}")

def warn(mensagem):
    """Exibe uma mensagem de aviso em amarelo."""
    print(f"\033[1;33m[AVISO]\033[0m {mensagem}")

def error(mensagem):
    """Exibe uma mensagem de erro em vermelho e encerra o script."""
    print(f"\033[1;31m[ERRO]\033[0m {mensagem}", file=sys.stderr)
    sys.exit(1)

def executar_comando_com_log(comando, mensagem_erro="Erro desconhecido."):
    """
    Executa um comando e trata o erro de forma elegante.
    O '&&' do shell é simulado com 'or' ou chamadas separadas.
    """
    try:
        # Usa subprocess.run para executar o comando
        # check=True fará com que o Python levante um erro se o comando falhar
        subprocess.run(comando, shell=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        error(f"{mensagem_erro}\nDetalhes do erro: {e}")

def main():
    """
    Função principal que executa a rotina de manutenção.
    """
    # Verifica se está rodando como root, similar ao `if [[ "$(id -u)" -ne 0 ]]`
    if os.geteuid() != 0:
        error("Este script deve ser executado como root. Use: sudo python3 up.py")

    info("Você está logado como root. Iniciando manutenção...")

    # A lógica de carregar o .bashrc (`source`) é específica do shell.
    # Em Python, os scripts não precisam carregar o ambiente do usuário para rodar comandos `apt`.
    # Apenas exibimos uma mensagem para manter a consistência com o script original.
    user_home = os.path.expanduser("~" + os.getlogin())
    if os.path.exists(f"{user_home}/.bashrc"):
        info(f"O script não precisa carregar o .bashrc, mas o arquivo existe em {user_home}.")
    else:
        warn(f"Arquivo .bashrc não encontrado em {user_home}.")

    # --- INÍCIO DOS COMANDOS DE MANUTENÇÃO ---

    info("Atualizando a lista de pacotes e realizando upgrade completo...")
    executar_comando_com_log("apt update && apt full-upgrade -y", "Falha na atualização dos pacotes.")

    info("Corrigindo pacotes quebrados...")
    executar_comando_com_log("dpkg --configure -a", "Falha na configuração de pacotes.")
    executar_comando_com_log("apt --fix-broken install -y", "Falha ao corrigir pacotes.")

    info("Removendo pacotes desnecessários...")
    executar_comando_com_log("apt autoremove -y", "Falha ao remover pacotes desnecessários.")

    info("Limpando pacotes residuais...")
    executar_comando_com_log("apt autoclean", "Falha ao limpar pacotes residuais.")

    info("Ubuntu atualizado, limpo e seguro!")

if __name__ == "__main__":
    main()
