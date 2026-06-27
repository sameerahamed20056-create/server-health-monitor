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
    ram = psutil.virtual_memory().percent
    total_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    disk = psutil.disk_usage('/').percent
    total_disk = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
    boot_time = psutil.boot_time()
    uptime_seconds = datetime.datetime.now().timestamp() - boot_time
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))
    current_time = datetime.datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname) 
    os_name = platform.system() + " " + platform.release()
    username = getpass.getuser()
    
    cpu_color = get_status_color(cpu)
    ram_color = get_status_color(ram)
    disk_color = get_status_color(disk)
    
    context = {
        "cpu" : cpu,
        "cpu_cores" : cpu_cores,
        "ram" : ram,
        "total_ram" : total_ram,
        "disk" : disk,
        "total_disk" : total_disk,
        "uptime" : uptime,
        "current_time" : current_time,
        "hostname" : hostname,
        "ip_address" : ip_address,
        "os_name" : os_name,
        "username" : username,
        "cpu_color" : cpu_color,
        "ram_color"  : ram_color,
        "disk_color" : disk_color,
        
    }
    return render(request, "home.html", context)