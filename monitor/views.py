from django.shortcuts import render
import psutil
import datetime
import socket
import platform
import getpass

def get_status_color(value):
    if value < 50:
        return "success"
    elif value < 80:
        return "warning"
    else:
        return "danger"

def home(request):
    
    cpu = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=True)
    physical_cores = psutil.cpu_count(logical=False)
    ram = psutil.virtual_memory().percent
    total_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    used_ram = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    aval_ram = round(psutil.virtual_memory().available / (1024 ** 3), 2)
    disk = psutil.disk_usage('/').percent
    total_disk = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
    used_disk = round(psutil.disk_usage('/').used / (1024 ** 3), 2)
    free_disk = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
    boot_time = psutil.boot_time()
    uptime_seconds = datetime.datetime.now().timestamp() - boot_time
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))
    current_time = datetime.datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    net = psutil.net_io_counters()
    bytes_sent = round(net.bytes_sent / (1024 * 1024), 2)
    bytes_received = round(net.bytes_recv / (1024 * 1024), 2)
    os_name = platform.system() + " " + platform.release()
    username = getpass.getuser()
    
    
    cpu_processes = []

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):

        try:

            cpu_processes.append(process.info)

        except:

            pass


    def get_cpu(process):
        return process["cpu_percent"]


    cpu_processes = sorted(
    cpu_processes,
    key=get_cpu,
    reverse=True
    )

    cpu_processes = cpu_processes[:5]
    
    
    ram_processes = []

    for process in psutil.process_iter(['pid', 'name', 'memory_percent']):

        try:

            ram_processes.append(process.info)

        except:

            pass


    def get_memory(process):
        return process["memory_percent"]


    ram_processes = sorted(
    ram_processes,
    key=get_memory,
    reverse=True
    )

    ram_processes = ram_processes[:5]
    
    cpu_color = get_status_color(cpu)
    ram_color = get_status_color(ram)
    disk_color = get_status_color(disk)
        
    if cpu < 80 and ram < 80 and disk < 80:
        system_status = "Healthy"
    
    else:
        system_status = "Warning"
        
    if system_status == 'Healthy':
        system_color = "success"
    else:
        system_color = "danger"
    
    context = {
        "cpu" : cpu,
        "cpu_cores" : cpu_cores,
        "physical_cores" : physical_cores,
        "ram" : ram,
        "total_ram" : total_ram,
        "used_ram" : used_ram,
        "aval_ram" : aval_ram,
        "disk" : disk,
        "total_disk" : total_disk,
        "used_disk" : used_disk,
        "free_disk" : free_disk,
        "uptime" : uptime,
        "current_time" : current_time,
        "hostname" : hostname,
        "ip_address" : ip_address,
        "os_name" : os_name,
        "username" : username,
        "cpu_color" : cpu_color,
        "ram_color" : ram_color,
        "disk_color" : disk_color,
        "system_status" : system_status,
        "system_color" : system_color,
        "bytes_sent" : bytes_sent,
        "bytes_received" : bytes_received,
        "cpu_processes" : cpu_processes,
        "ram_processes" : ram_processes        
    }
    return render(request, "home.html", context)