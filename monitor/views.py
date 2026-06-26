from django.shortcuts import render
import psutil

def get_status_color(value):
    if value < 50:
        return "success"
    
    elif value < 80:
        return "warning"
    
    else:
        return "danger"

def home(request):
    
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    cpu_color = get_status_color(cpu)
    ram_color = get_status_color(ram)
    disk_color = get_status_color(disk)
    
    context = {
        "cpu" : cpu,
        "ram" : ram,
        "disk" : disk,
        "uptime" : "Running",
        "cpu_color" : cpu_color,
        "ram_color"  : ram_color,
        "disk_color" : disk_color
    }
    return render(request, "home.html", context)