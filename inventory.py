import platform
import socket
import getpass
import shutil
import subprocess
import ctypes
from datetime import datetime


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Not found"


def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)


def get_ram_gb():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory = MEMORYSTATUSEX()
    memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
    return bytes_to_gb(memory.ullTotalPhys)


def get_local_users():
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-LocalUser | Select-Object -ExpandProperty Name"],
            capture_output=True,
            text=True
        )
        users = result.stdout.strip()
        return users if users else "No users found"
    except:
        return "Could not retrieve users"


disk = shutil.disk_usage("C:\\")

report = f"""
Windows System Inventory Report
Generated: {datetime.now()}

Computer Name: {platform.node()}
Current User: {getpass.getuser()}
Operating System: {platform.system()} {platform.release()}
OS Version: {platform.version()}
Processor: {platform.processor()}
Architecture: {platform.machine()}
Total RAM: {get_ram_gb()} GB
Local IP Address: {get_ip()}

Disk C:
Total: {bytes_to_gb(disk.total)} GB
Used: {bytes_to_gb(disk.used)} GB
Free: {bytes_to_gb(disk.free)} GB

Local Users:
{get_local_users()}
"""

print(report)

with open("inventory_report.txt", "w") as file:
    file.write(report)

print("Report saved as inventory_report.txt")