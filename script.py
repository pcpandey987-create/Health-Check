#!/usr/bin/env python3

import shutil
import socket
import psutil

# Define thresholds
CPU_THRESHOLD = 80.0  # Percentage
RAM_THRESHOLD = 80.0  # Percentage
DISK_THRESHOLD = 80.0 # Percentage

def check_cpu():
    """Check current CPU usage percentage."""
    usage = psutil.cpu_percent(interval=1)
    is_healthy = usage < CPU_THRESHOLD
    return is_healthy, f"CPU Usage: {usage}%"

def check_ram():
    """Check available system memory (RAM)."""
    ram = psutil.virtual_memory()
    is_healthy = ram.percent < RAM_THRESHOLD
    return is_healthy, f"RAM Usage: {ram.percent}% (Used: {ram.used // (2**20)} MB / Total: {ram.total // (2**20)} MB)"

def check_disk():
    """Check primary disk drive space utilization."""
    # Using root '/' for Linux/Mac or 'C:\\' for Windows
    disk = shutil.disk_usage("C:\\" if psutil.WINDOWS else "/")
    percent_used = (disk.used / disk.total) * 100
    is_healthy = percent_used < DISK_THRESHOLD
    return is_healthy, f"Disk Usage: {percent_used:.2f}% (Free: {disk.free // (2**30)} GB)"

def check_network():
    """Check internet connectivity by resolving a reliable host."""
    try:
        socket.gethostbyname("www.google.com")
        return True, "Network: Connected"
    except socket.error:
        return False, "Network: No internet connection"

def main():
    print("--- Starting PC Health Check ---\n")

    checks = [check_cpu(), check_ram(), check_disk(), check_network()]
    system_healthy = True

    for is_healthy, message in checks:
        status = "[OK]" if is_healthy else "[WARNING]"
        print(f"{status} {message}")
        if not is_healthy:
            system_healthy = False

    print("\n--------------------------------")
    if system_healthy:
        print("Status: All systems are operating normally!")
    else:
        print("Status: Action required! Some metrics exceed safe thresholds.")

if __name__ == "__main__":
    main()
