#!/usr/bin/env python3
#----------------------
# ---- Autor: Zenio zndv@outlook.com 21977036020
# ---- última atualização: 14/05/25
# --- rodar no Shell, para sair do script dê duas vezes ctrl c


from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import subprocess
import psutil
import time

console = Console()

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except:
        return "Erro"


def get_disk_health():
    health_data = {}
    # Lista apenas discos físicos (sem partições), ignora loop e ram disks
    lsblk_output = run_cmd("lsblk -d -o NAME,MODEL,SIZE,STATE,TYPE -n | grep disk")
    for line in lsblk_output.splitlines():
        parts = line.split()
        if len(parts) >= 1:
            disk = parts[0]
            # Realiza diagnóstico de saúde SMART
            smart_info = run_cmd(f"sudo smartctl -H /dev/{disk} || echo 'SMART não disponível para {disk}'")
            health_data[f"{disk} ({' '.join(parts[1:])})"] = smart_info
    return health_data


def get_detailed_disk_health():
    # Coleta lista de todos os discos físicos
    lsblk_output = run_cmd("lsblk -d -o NAME,MODEL,SIZE -n | grep -v loop")
    table = Table(title="Saúde Detalhada dos Discos (SMART)")

    table.add_column("Disco")
    table.add_column("Modelo")
    table.add_column("Tamanho")
    table.add_column("Serial")
    table.add_column("Saúde")
    table.add_column("Temperatura (se disponível)")

    for line in lsblk_output.splitlines():
        parts = line.strip().split(maxsplit=2)
        if len(parts) >= 3:
            disk, model, size = parts
            serial = run_cmd(f"sudo smartctl -i /dev/{disk} | grep 'Serial Number' | awk -F: '{{print $2}}'").strip() or "N/A"
            health = run_cmd(f"sudo smartctl -H /dev/{disk} | grep 'SMART overall-health' || echo 'N/A'").strip()
            temp = run_cmd(f"sudo smartctl -A /dev/{disk} | grep -i Temperature | awk '{{print $10}}' | head -n 1").strip() or "N/A"
            table.add_row(disk, model, size, serial, health, temp)

    return table



def dashboard_panel():
    cpu_percent = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_if_addrs()
    temp = run_cmd("sensors")

    table = Table(title="Dashboard do Sistema")

    table.add_column("Componente", justify="left", style="cyan")
    table.add_column("Informação", style="magenta")

    table.add_row("CPU Uso (%)", f"{cpu_percent}%")
    table.add_row("RAM Uso (%)", f"{mem.percent}% ({mem.used // (1024 ** 2)}MB / {mem.total // (1024 ** 2)}MB)")
    table.add_row("Disco Raiz Uso (%)", f"{disk.percent}% ({disk.used // (1024 ** 3)}GB / {disk.total // (1024 ** 3)}GB)")

    ip_info = run_cmd("hostname -I")
    table.add_row("IP Local", ip_info)

    table.add_row("Conexões Ativas", run_cmd("ss -s"))

    return table, temp, get_disk_health()

def live_dashboard():
    with Live(refresh_per_second=1) as live:
        while True:
            table, temp, _ = dashboard_panel()  # Painel geral (CPU, RAM, Rede, Sensores)
            detailed_table = get_detailed_disk_health()  # Nova tabela de discos detalhada

            layout = Table.grid()
            layout.add_row(table)
            layout.add_row(detailed_table)
            layout.add_row(Panel(f"[bold yellow]Sensores:[/bold yellow]\n{temp}", title="Sensores"))

            live.update(layout)
            time.sleep(3)


if __name__ == "__main__":
    try:
        console.print("[bold green]Iniciando Dashboard do Sistema em Terminal...[/bold green]")
        live_dashboard()
    except KeyboardInterrupt:
        console.print("\n[bold red]Encerrado pelo usuário.[/bold red]")

