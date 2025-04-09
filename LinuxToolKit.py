#Code Written By SayyadN
#Date 09/4/2025
#Code Written For: To Perform All Linux Related Task
#Version 2.0

#Importing Required Libraries
import subprocess
import os
import google.generativeai as GenAI
from colorama import Fore, Back, Style, init
import platform
import psutil
import ctypes
# Removed unused import sys
import random
import string
import socket
import time
import sys


#Main Variables
p = print
e = exit
i = input
run = subprocess.run

# Initialize colorama
init(autoreset=True)

#Function for run it as Admin
def run_as_admin():
    if os.name != 'nt' and os.geteuid() != 0:
        p("This script requires root privileges. Re-launching with sudo...")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)
    else:
        p("Try Again with root privileges.")
        e()

# Dictionary mapping each supported package manager to its command formats
pm_commands = {
    "apt": {
        "install": ["apt", "install", "-y"],
        "remove": ["apt", "remove", "-y"],
        "update": ["apt", "update"],
        "upgrade": ["apt", "upgrade", "-y"],
        "search": ["apt", "search"]
    },
    "dnf": {
        "install": ["dnf", "install", "-y"],
        "remove": ["dnf", "remove", "-y"],
        "update": ["dnf", "update"],
        "upgrade": ["dnf", "upgrade", "-y"],
        "search": ["dnf", "search"]
    },
    "yum": {
        "install": ["yum", "install", "-y"],
        "remove": ["yum", "remove", "-y"],
        "update": ["yum", "update"],
        "upgrade": ["yum", "upgrade", "-y"],
        "search": ["yum", "search"]
    },
    "zypper": {
        "install": ["zypper", "install", "-y"],
        "remove": ["zypper", "remove", "-y"],
        "update": ["zypper", "refresh"],
        "upgrade": ["zypper", "update", "-y"],
        "search": ["zypper", "search"]
    },
    "pacman": {
        "install": ["pacman", "-S", "--noconfirm"],
        "remove": ["pacman", "-R", "--noconfirm"],
        "update": ["pacman", "-Sy"],
        "upgrade": ["pacman", "-Su", "--noconfirm"],
        "search": ["pacman", "-Ss"]
    },
    "apk": {
        "install": ["apk", "add"],
        "remove": ["apk", "del"],
        "update": ["apk", "update"],
        "upgrade": ["apk", "upgrade"],
        "search": ["apk", "search"]
    },
    "snap": {
        "install": ["snap", "install"],
        "remove": ["snap", "remove"],
        "update": ["snap", "refresh"],
        "search": ["snap", "find"]
    },
    "flatpak": {
        "install": ["flatpak", "install", "-y"],
        "remove": ["flatpak", "uninstall", "-y"],
        "update": ["flatpak", "update"],
        "search": ["flatpak", "search"]
    },
    "nix": {
        "install": ["nix-env", "-iA"],
        "remove": ["nix-env", "-e"],
        "update": ["nix-channel", "--update"],
        "upgrade": ["nix-env", "-u"],
        "search": ["nix-env", "-qa"]
    },
    "urpmi": {
        "install": ["urpmi"],
        "remove": ["urpme"],
        "update": ["urpmi.update"],
        "upgrade": ["urpmi", "upgrade"],
        "search": ["urpmq"]
    },
    "rpm": {
        "install": ["rpm", "-i", "--force", "--nodeps"],
        "remove": ["rpm", "-e", "--nodeps"],
        "update": ["rpm", "-U", "--force", "--nodeps"],
        "query": ["rpm", "-q"]
    },
    "portage": {
        "install": ["emerge", "--ask", "--verbose"],
        "remove": ["emerge", "--unmerge", "--ask", "--verbose"],
        "update": ["emerge", "--sync"],
        "upgrade": ["emerge", "--update", "--deep", "--with-bdeps=y", "--newuse", "--ask", "--verbose"],
        "search": ["eix"]
    }
}



# Function to detect the package manager automatically
def detect_package_manager():
    installed_managers = []
    for manager in pm_commands:
        result = run(["which", manager], capture_output=True, text=True)
        if result.returncode == 0:
            installed_managers.append(manager)
    if installed_managers:
        return installed_managers[0]  
    else:
        p(Fore.RED + "No supported package manager found.")
        ask_continue("Exiting due to no package manager found.")
        e()

# Function to check if the script is running with admin privileges
def is_admin():
    try:
        if os.name != 'nt':
            return os.geteuid() == 0
        else:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as ex:
        p(Fore.RED + f"An error occurred: {ex}")
        e()
        return False



# Function to get AI help for package management
def ai_help(error_message):
    try:
        #Ai Configuration
        GenAI.configure(api_key="AIzaSyBDh4vnq-5QQvcmmxWbE3iADan2ZWV1DsU")
        model = GenAI.GenerativeModel("gemini-2.0-flash")
        while True:
            # Get user input for AI assistance
            response = model.generate_content(error_message)
            p(Fore.GREEN + Back.WHITE + Style.BRIGHT + "\n" + "=" * 50)
            p(Fore.GREEN + Back.WHITE + Style.BRIGHT + " AI Assistance Response ".center(50, "="))
            p(Fore.GREEN + Back.WHITE + Style.BRIGHT + response.text)
            p(Fore.GREEN + Back.WHITE + Style.BRIGHT + "\n" + "=" * 50)
            p(Fore.CYAN + Style.BRIGHT + "Powered By SayyadN".center(50))
            user_input = i("You can exit by typing 'exit'. Do you need more help? (Y/N): ").lower()

            # Define user input options
            user_ok = ["yes", "yep", "yeah", "sure", "y"]
            user_no = ["no", "nope", "nah", "n" , "no thanks" , "nope thanks", 'exit']  
            # Check if user input is in the defined options
            if user_input in user_no:
                break
            elif user_input in user_ok:
                error_message = i("Please provide more details about the issue: ")
            else:
                p(Fore.RED + "Invalid input, please try again.")
    except Exception as ex:
        p(Fore.RED + f"AI help is currently unavailable: {ex}")

def install_package():
    package_name = i("Enter Package Name (or type 'exit' to cancel): ").strip()
    if package_name.lower() == "exit":
        p(Fore.YELLOW + "Exiting package installation.")
        return
    # Build a list of available package managers by checking if they exist in the system
    available_managers = []
    for manager in pm_commands:
        result = run(["which", manager], capture_output=True, text=True)
        if result.returncode == 0:
            available_managers.append(manager)

    if not available_managers:
        p(Fore.RED + "No supported package managers found.")
        return

    installed = False
    for manager in available_managers:
        p(Fore.BLUE + f"Attempting to install {package_name} using {manager}...")
        cmd = pm_commands[manager]["install"] + [package_name]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + f"{package_name} installed successfully using {manager}.")
            installed = True
            break  # Package installed successfully; exit the loop.
        else:
            error_msg = f"Failed to install {package_name} using {manager}: {result.stderr}"
            p(Fore.RED + error_msg)

    if not installed:
        p(Fore.RED + f"Failed to install {package_name} using all available package managers.")
        get_help = i("Do you want to get help from AI? (Y/N or type 'exit' to cancel): ").lower()
        if get_help == "exit":
            p(Fore.YELLOW + "Exiting help request.")
            return
        if get_help == "y":
            ai_help(error_msg)

# Function To Remove Package
def remove_package():
    package_name = i("Enter Package Name (or type 'exit' to cancel): ").strip()
    if package_name.lower() == "exit":
        p(Fore.YELLOW + "Exiting package removal.")
        return
    for try_remove in pm_commands.keys():
        p(Fore.BLUE + f"Attempting to remove {package_name} using {try_remove}...")
        cmd = pm_commands[try_remove]["remove"] + [package_name] 
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + f"{package_name} removed successfully.")
            break
        else:
            error_msg = f"Failed to remove {package_name}: {result.stderr}"
            p(Fore.RED + error_msg)
    else:
        p(Fore.RED + f"Failed to remove {package_name} using all available package managers.")
        get_help = i("Do you want to get help from AI? (Y/N or type 'exit' to cancel): ").lower()
        if get_help == "exit":
            p(Fore.YELLOW + "Exiting help request.")
            return
        if get_help == "y":
            ai_help(error_msg)
    ask_continue("Continue after removal attempt?")           

# Function To Update Package or Full System
def update():
    # First ask user if he wants to update a package or full system
    system_exi = ["system", "full", "s" , "f" , "full system" , "full system update" , "fs"]
    package_exi = ["package", "p" , "pkg" , "pckg" , "pckg update" , "package update"]
    update_choice = i("Do you want to update a package or the full system? (P/S or type 'exit' to cancel): ").strip().lower()
    if update_choice == "exit":
        p(Fore.YELLOW + "Exiting update operation.")
        return

    if update_choice in package_exi:
        package_manager = detect_package_manager()
        package_name = i("Enter Package Name (or type 'exit' to cancel): ").strip()
        if package_name.lower() == "exit":
            p(Fore.YELLOW + "Exiting package update.")
            return
        p(Fore.BLUE + f"Updating {package_name} using {package_manager}...")
        cmd = pm_commands[package_manager]["update"] + [package_name]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + f"{package_name} updated successfully.")
        else:
            error_msg = f"Failed to update {package_name}: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N or type 'exit' to cancel): ").lower()
            if get_help == "exit":
                p(Fore.YELLOW + "Exiting help request.")
                return
            if get_help == "y":
                ai_help(error_msg)
    elif update_choice in system_exi:
        package_manager = detect_package_manager()
        p(Fore.BLUE + f"Updating system using {package_manager}...")
        cmd = pm_commands[package_manager]["update"]
        if is_admin():
            result = run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                p(Fore.GREEN + "System update completed successfully.")
            else:
                error_msg = f"Error during update: {result.stderr}"
                p(Fore.RED + error_msg)
                get_help = i("Do you want to get help from AI? (Y/N or type 'exit' to cancel): ").lower()
                if get_help == "exit":
                    p(Fore.YELLOW + "Exiting help request.")
                    return
                if get_help == "y":
                    ai_help(error_msg)
        else:
            p(Fore.RED + "Admin privileges required for system update.")
    else:
        p(Fore.RED + "Invalid input. Please enter 'P' or 'S'.")
        return

    upgrade_choice = i("Do you want to upgrade a package or the full system? (P/S or type 'exit' to cancel): ").strip().lower()
    if upgrade_choice == "exit":
        p(Fore.YELLOW + "Exiting upgrade operation.")
        return

    if upgrade_choice in package_exi:
        package_manager = detect_package_manager()
        package_name = i("Enter Package Name (or type 'exit' to cancel): ").strip()
        if package_name.lower() == "exit":
            p(Fore.YELLOW + "Exiting package upgrade.")
            return
        p(Fore.BLUE + f"Upgrading {package_name} using {package_manager}...")
        cmd = pm_commands[package_manager]["upgrade"] + [package_name]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + f"{package_name} upgraded successfully.")
        else:
            error_msg = f"Failed to upgrade {package_name}: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N or type 'exit' to cancel): ").lower()
            if get_help == "exit":
                p(Fore.YELLOW + "Exiting help request.")
                return
            if get_help == "y":
                ai_help(error_msg)
    elif upgrade_choice in system_exi:
        package_manager = detect_package_manager()
        p(Fore.BLUE + f"Upgrading system using {package_manager}...")
        cmd = pm_commands[package_manager]["upgrade"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + "System upgrade completed successfully.")
        else:
            error_msg = f"Error during upgrade: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N or type 'exit' to cancel): ").lower()
            if get_help == "exit":
                p(Fore.YELLOW + "Exiting help request.")
                return
            if get_help == "y":
                ai_help(error_msg)
    else:
        p(Fore.RED + "Invalid input. Please enter 'P' or 'S'.")
        return
    ask_continue("Continue after upgrade attempt?")

# Function To Search for a Package
def search_package():
    package_manager = detect_package_manager()
    package_name = i("Enter Package Name: ").strip()
    p(Fore.BLUE + f"Searching for {package_name} using {package_manager}...")
    cmd = pm_commands[package_manager]["search"] + [package_name]
    result = run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        p(Fore.GREEN + result.stdout)
    else:
        error_msg = f"Failed to search for {package_name}: {result.stderr}"
        p(Fore.RED + error_msg)
        get_help = i("Do you want to get help from AI? (Y/N): ").lower()
        if get_help == "y":
            ai_help(error_msg)
    ask_continue("Continue after search attempt?")

# Function to clean up unused packages
def cleanup_system():
    package_manager = detect_package_manager()
    p(Fore.BLUE + f"Cleaning up system using {package_manager}...")
    if package_manager in ["apt", "dnf", "yum", "zypper", "pacman"]:
        cmd = [package_manager, "autoremove", "-y"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + "System cleanup completed successfully.")
        else:
            error_msg = f"Failed to clean up the system: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    else:
        p(Fore.RED + "System cleanup is not supported for this package manager.")
    ask_continue("Continue after system cleanup attempt?")

# Function to display system information
def display_system_info():
    p(Fore.YELLOW + "System Information:")
    p(Fore.WHITE + f"  Platform: {platform.system()} {platform.release()}")
    p(Fore.WHITE + f"  Architecture: {platform.machine()}")
    p(Fore.WHITE + f"  Hostname: {platform.node()}")
    p(Fore.WHITE + f"  Python Version: {platform.python_version()}")
    p(Fore.WHITE + f"  CPU Count: {os.cpu_count()}")
    p(Fore.WHITE + f"  Memory (Total): {psutil.virtual_memory().total / (1024 ** 3):.2f} GB")
    p(Fore.WHITE + f"  Disk (Total): {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB")
    ask_continue("Continue after displaying system information?")



# Function for network options
def get_size(bytes):
    """
    Converts bytes to a human-readable format.
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
def network_opions():
    p(Fore.CYAN + "Network Options:")
    p("1. Check Network Connectivity")
    p("2. Display Network Configuration")
    p("3. open network hotspot")
    p("4. Check Network Speed")
    p("5. Check Network Interfaces")
    p("6. Check Network Connections")
    p("7. Check DNS Configuration")
    p("8. Check Firewall Status")
    p("9. Check Network Protocols")
    p("10. Check Network Services")
    p("11. Check Network Statistics")
    p("12. Exit to Main Menu")
    choice = i("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        hostname = "google.com"
        p(Fore.BLUE + f"Checking network connectivity to {hostname}...")
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            p(Fore.GREEN + f"Network connectivity to {hostname} is OK.")
        else:
            p(Fore.RED + f"Network connectivity to {hostname} is down.")
    elif choice == "2":
        p(Fore.BLUE + "Displaying network configuration...")
        cmd = ["ifconfig"] if os.name != 'nt' else ["ipconfig"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to display network configuration: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "3":
        # Generate a random 8-character password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # Generate a random name starting with "wifi-"
        hotspot_name = "wifi-" + ''.join(random.choices(string.ascii_lowercase, k=5))

        p(Fore.BLUE + f"Opening network hotspot with name '{hotspot_name}' and password '{password}'...")
        cmd = ["nmcli", "device", "wifi", "hotspot", "ssid", hotspot_name, "password", password]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + f"Network hotspot '{hotspot_name}' opened successfully with password '{password}'.")
        else:
            error_msg = f"Failed to open network hotspot: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "4":
        p(Fore.BLUE + "Checking network speed...")
        cmd = ["speedtest-cli"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to check network speed: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "5":

        p(Fore.BLUE + "Checking network interfaces...")
        cmd = ["lshw", "-C", "network"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to check network interfaces: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "6":
        try:
            # Attempt to connect to Google's DNS server
            socket.create_connection(('8.8.8.8', 53), timeout=5)
            p(Fore.GREEN + "Network connection is active.")
        except (socket.timeout, socket.error):
            p(Fore.RED + "No network connection.")
    elif choice == "7":
        p(Fore.BLUE + "Checking DNS configuration...")
        cmd = ["cat", "/etc/resolv.conf"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to check DNS configuration: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "8":
        p(Fore.BLUE + "Checking firewall status...")
        cmd = ["ufw", "status"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to check firewall status: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "9":
        p(Fore.BLUE + "Checking network protocols...")
        cmd = ["cat", "/etc/protocols"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to check network protocols: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "10":
        p(Fore.BLUE + "Checking network services...")
        cmd = ["systemctl", "list-units", "--type=service"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + result.stdout)
        else:
            error_msg = f"Failed to check network services: {result.stderr}"
            p(Fore.RED + error_msg)
            get_help = i("Do you want to get help from AI? (Y/N): ").lower()
            if get_help == "y":
                ai_help(error_msg)
    elif choice == "11":
        p(Fore.BLUE + "Checking network statistics...")
        try:
         interval=1
         while True:
             time.sleep(interval)
             net_io = psutil.net_io_counters()
             sent, recv = net_io.bytes_sent - bytes_sent, net_io.bytes_recv - bytes_recv
             print(f"Upload: {get_size(net_io.bytes_sent)} | "
                   f"Download: {get_size(net_io.bytes_recv)} | "
                   f"Upload Speed: {get_size(sent / interval)}/s | "
                   f"Download Speed: {get_size(recv / interval)}/s", end="\r")
             bytes_sent, bytes_recv = net_io.bytes_sent, net_io.bytes_recv
        except KeyboardInterrupt:
         print("\nMonitoring stopped.")
    elif choice == "12":
        p(Fore.YELLOW + "Exiting to Main Menu...")
        return
    else:   
        p(Fore.RED + "Invalid choice. Please try again.")
    ask_continue("Continue after network options?") 


# Function to ask if the user wants to continue
def ask_continue(message="Do you want to continue? (Y/N): "):
    user_ok = ["yes", "yep", "yeah", "sure", "y"]
    user_no = ["no", "nope", "nah", "n" , "no thanks" , "nope thanks", 'exit'] 
    while True:
        choice = i(Fore.YELLOW + message).strip().lower()
        if choice in user_ok:
            p(Fore.GREEN + "Continuing...")
            return True
        elif choice in user_no:
            p(Fore.YELLOW + "Exiting...")
            e()
        else:
            p(Fore.RED + "Invalid input. Please enter 'Y' or 'N'.")


# Normal menu version with banner

def main_menu():
    banner = """
██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
██║     ██║████╗  ██║██║   ██║╚██╗██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝    ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
██║     ██║██║╚██╗██║██║   ██║ ██╔██╗    ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗   ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
                                                                                             
██████╗ ██╗   ██╗    ███████╗ █████╗ ██╗   ██╗██╗   ██╗ █████╗ ██████╗ ███╗   ██╗            
██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔══██╗╚██╗ ██╔╝╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║            
██████╔╝ ╚████╔╝     ███████╗███████║ ╚████╔╝  ╚████╔╝ ███████║██║  ██║██╔██╗ ██║            
██╔══██╗  ╚██╔╝      ╚════██║██╔══██║  ╚██╔╝    ╚██╔╝  ██╔══██║██║  ██║██║╚██╗██║            
██████╔╝   ██║       ███████║██║  ██║   ██║      ██║   ██║  ██║██████╔╝██║ ╚████║            
╚═════╝    ╚═╝       ╚══════╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝            
    """
    
    menu = [
        '1. Install a Package',
        '2. Remove a Package',
        '3. Update & Upgrade System',
        '4. Search for a Package',
        '5. Cleanup System',
        '6. Display System Information',
        '7. Network Options',
        '8. Exit'
    ]
    
    while True:
        print("\n" + banner)
        for item in menu:
            print(item)
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            install_package()
        elif choice == '2':
            remove_package()
        elif choice == '3':
            update()
        elif choice == '4':
            search_package()
        elif choice == '5':
            cleanup_system()
        elif choice == '6':
            display_system_info()
        elif choice == '7':
            network_opions()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    # Check if the script is run as admin
    if not is_admin():
        run_as_admin()
    else:
        # Run the main menu function
        p(Fore.GREEN + "Welcome to Linux Tool Kit!")
        p(Fore.YELLOW + "Please wait while we load the menu...")
        time.sleep(2)  # Simulate loading time
        p(Fore.YELLOW + "Loading completed.")
    main_menu()
