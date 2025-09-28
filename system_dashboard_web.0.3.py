#!/usr/bin/env python3
# ----------------------
# ---- Autor: Zenio [zndv@outlook.com]
# ---- última atualização: 28/09/25 - 14/05/25
# ----- Dashboard Web com alertas e gráficos em Flask
# ----- Rodar sudo python3 system_dashboard_web.py

from flask import Flask, render_template_string, send_from_directory, url_for
import psutil
import subprocess
import os

app = Flask(__name__)

ALERT_CPU = 80  # Limite de alerta CPU em %
ALERT_RAM = 80  # Limite de alerta RAM em %

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return "Erro"

def get_disk_health():
    lsblk_output = run_cmd("lsblk -d -o NAME,MODEL,SIZE -n | grep -v loop")
    disks = []
    for line in lsblk_output.splitlines():
        parts = line.strip().split(maxsplit=2)
        if len(parts) >= 3:
            disk, model, size = parts
            serial = run_cmd(f"sudo smartctl -i /dev/{disk} | grep 'Serial Number' | awk -F: '{{print $2}}'").strip() or "N/A"
            health = run_cmd(f"sudo smartctl -H /dev/{disk} | grep 'SMART overall-health' || echo 'N/A'").strip()
            temp = run_cmd(f"sudo smartctl -A /dev/{disk} | grep -i Temperature | awk '{{print $10}}' | head -n 1").strip() or "N/A"
            disks.append({
                "disk": disk,
                "model": model,
                "size": size,
                "serial": serial,
                "health": health,
                "temp": temp
            })
    return disks

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

@app.route('/')
def index():
    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    ip = run_cmd("hostname -I")
    conexoes = run_cmd("ss -s")
    disks = get_disk_health()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard do Sistema</title>
        <meta http-equiv="refresh" content="5">
        <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: Arial, sans-serif; background-color: #111; color: #eee; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #444; padding: 8px; text-align: left; }
            th { background-color: #222; }
            h1, h2 { color: #6cf; }
            .alert { color: #ff5555; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Dashboard do Sistema (Web)</h1>
        <h2>Status Geral</h2>
        <table>
            <tr><th>Componente</th><th>Informação</th></tr>
            <tr>
                <td>CPU Uso (%)</td>
                <td {% if cpu > ''' + str(ALERT_CPU) + ''' %}class="alert"{% endif %}>
                    {{ cpu }}%
                    {% if cpu > ''' + str(ALERT_CPU) + ''' %} - ALTO USO DE CPU!{% endif %}
                </td>
            </tr>
            <tr>
                <td>RAM Uso (%)</td>
                <td {% if ram.percent > ''' + str(ALERT_RAM) + ''' %}class="alert"{% endif %}>
                    {{ ram.percent }}% ({{ ram.used // (1024 ** 2) }}MB / {{ ram.total // (1024 ** 2) }}MB)
                    {% if ram.percent > ''' + str(ALERT_RAM) + ''' %} - ALTO USO DE RAM!{% endif %}
                </td>
            </tr>
            <tr><td>Disco Raiz (%)</td><td>{{ disk.percent }}% ({{ disk.used // (1024 ** 3) }}GB / {{ disk.total // (1024 ** 3) }}GB)</td></tr>
            <tr><td>IP Local</td><td>{{ ip }}</td></tr>
        </table>

        <h2>Utilização Histórica</h2>
        <canvas id="cpuChart" width="600" height="200"></canvas>
        <canvas id="ramChart" width="600" height="200" style="margin-top:20px;"></canvas>

        <h2>Discos (SMART)</h2>
        <table>
            <tr><th>Disco</th><th>Modelo</th><th>Tamanho</th><th>Serial</th><th>Saúde</th><th>Temperatura</th></tr>
            {% for d in disks %}
            <tr>
                <td>{{ d.disk }}</td>
                <td>{{ d.model }}</td>
                <td>{{ d.size }}</td>
                <td>{{ d.serial }}</td>
                <td>{{ d.health }}</td>
                <td>{{ d.temp }}</td>
            </tr>
            {% endfor %}
        </table>

        <h2>Conexões Ativas</h2>
        <pre>{{ conexoes }}</pre>

        <script>
            // Carrega histórico do localStorage ou inicializa
            let cpuHistory = JSON.parse(localStorage.getItem('cpuHistory') || '[]');
            let ramHistory = JSON.parse(localStorage.getItem('ramHistory') || '[]');
            const maxDataPoints = 20;

            function updateHistory(value, historyArray) {
                historyArray.push(value);
                if (historyArray.length > maxDataPoints) {
                    historyArray.shift();
                }
                return historyArray;
            }

            cpuHistory = updateHistory({{ cpu }}, cpuHistory);
            ramHistory = updateHistory({{ ram.percent }}, ramHistory);

            localStorage.setItem('cpuHistory', JSON.stringify(cpuHistory));
            localStorage.setItem('ramHistory', JSON.stringify(ramHistory));

            const labels = Array(cpuHistory.length).fill('').map((_, i) => i + 1);

            const ctxCPU = document.getElementById('cpuChart').getContext('2d');
            const cpuChart = new Chart(ctxCPU, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'CPU Uso (%)',
                        data: cpuHistory,
                        borderColor: 'rgba(102, 204, 255, 1)',
                        backgroundColor: 'rgba(102, 204, 255, 0.3)',
                        fill: true,
                    }]
                },
                options: {
                    animation: false,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });

            const ctxRAM = document.getElementById('ramChart').getContext('2d');
            const ramChart = new Chart(ctxRAM, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'RAM Uso (%)',
                        data: ramHistory,
                        borderColor: 'rgba(255, 102, 102, 1)',
                        backgroundColor: 'rgba(255, 102, 102, 0.3)',
                        fill: true,
                    }]
                },
                options: {
                    animation: false,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });
        </script>

    </body>
    </html>
    ''', cpu=cpu_percent,
         ram=ram,
         disk=disk,
         ip=ip,
         conexoes=conexoes,
         disks=disks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
