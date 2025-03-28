#Code Written By SayyadN
#Date 26/3/2025
#Code Written For: To Perform All Linux Related Task
#Version 1.0

#Importing Required Libraries
import subprocess
import os
import google.generativeai as GenAI
from colorama import Fore, Back, Style, init
import platform
import psutil
import ctypes
import sys

#Main Variables
p = print
e = exit
i = input
run = subprocess.run

# Initialize colorama
init(autoreset=True)

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
    }
}

#Main Dictionary For Linux packages or apps (unchanged)
linux_apps = {
    "Development": {
        "Compilers": [
            "gcc", "g++", "clang", "rustc", "go", "swift", "zig", "dmd"
        ],
        "Interpreters": [
            "python3", "nodejs", "ruby", "perl", "php", "lua", "julia", "r-base"
        ],
        "Build Tools": [
            "make", "cmake", "autoconf", "ninja", "bazel", "meson", "autotools"
        ],
        "IDEs": [
            "code", "eclipse", "pycharm-community", "netbeans", "clion",
            "android-studio", "geany", "anjuta", "bluefish", "intellij-idea-community", "atom"
        ],
        "Text Editors": [
            "vim", "nano", "emacs", "gedit", "kate", "neovim", "micro", "lite-xl", "sublime-text"
        ],
        "Version Control": [
            "git", "subversion", "mercurial", "bazaar", "fossil"
        ],
        "Debugging & Profiling": [
            "gdb", "valgrind", "perf", "strace", "ltrace", "rr"
        ],
        "Package Managers": [
            "apt", "snap", "flatpak", "dnf", "pacman", "brew", "cargo", "pip", "paru", "yay"
        ],
        "Containers & Virtualization": [
            "docker.io", "docker-compose", "podman", "virtualbox", "qemu",
            "libvirt-daemon-system", "lxc", "lxd"
        ],
        "Other Tools": [
            "fpm", "pyenv", "rbenv", "nvm"
        ]
    },
    "System Utilities": {
        "Monitoring": [
            "htop", "iotop", "glances", "btop", "conky", "neofetch"
        ],
        "File Managers": [
            "nautilus", "thunar", "pcmanfm", "ranger", "mc", "doublecmd", "dolphin", "nemo"
        ],
        "Terminals": [
            "gnome-terminal", "konsole", "xfce4-terminal", "alacritty",
            "tilix", "kitty", "guake", "xterm"
        ],
        "Process Management": [
            "ps", "kill", "nice", "renice", "pkill", "top"
        ],
        "Compression": [
            "zip", "unzip", "tar", "gzip", "bzip2", "xz-utils", "p7zip-full", "lrzip"
        ],
        "Disk Utilities": [
            "gparted", "parted", "fsck", "e2fsprogs", "testdisk", "smartmontools"
        ],
        "Backup Tools": [
            "rsnapshot", "deja-dup", "timeshift", "borgbackup", "restic", "rsync"
        ],
        "Benchmarking": [
            "phoronix-test-suite", "sysbench", "fio", "hardinfo"
        ],
        "Configuration & Package Frontends": [
            "nala", "synaptic"
        ]
    },
    "Networking": {
        "Web Browsers": [
            "firefox", "chromium", "brave", "vivaldi", "tor-browser", "opera", "icecat"
        ],
        "Download Managers": [
            "wget", "curl", "aria2", "uget", "axel"
        ],
        "File Transfer": [
            "rsync", "scp", "ftp", "filezilla", "lftp", "rclone"
        ],
        "VPN Clients": [
            "openvpn", "wireguard", "protonvpn-cli", "windscribe-cli"
        ],
        "Network Analysis": [
            "nmap", "wireshark", "tcpdump", "netcat", "traceroute", "mtr"
        ],
        "Remote Access": [
            "openssh-client", "openssh-server", "mosh", "remmina", "teamviewer", "anydesk", "nomachine"
        ]
    },
    "Multimedia": {
        "Audio Players": [
            "vlc", "mpv", "rhythmbox", "audacious", "qmmp", "deadbeef", "cmus"
        ],
        "Video Editors": [
            "kdenlive", "shotcut", "openshot", "davinci-resolve", "olive-editor", "pitivi"
        ],
        "Image Editors": [
            "gimp", "inkscape", "krita", "darktable", "blender", "mypaint", "pinta"
        ],
        "Screen Recording": [
            "obs-studio", "kazam", "simple-screen-recorder", "vokoscreen", "recordmydesktop"
        ],
        "Music Production": [
            "lmms", "ardour", "hydrogen", "musE", "qtractor"
        ],
        "Media Servers": [
            "kodi", "plex", "jellyfin", "minidlna"
        ],
        "Media Converters": [
            "ffmpeg", "handbrake", "soundconverter"
        ]
    },
    "Office & Productivity": {
        "Office Suites": [
            "libreoffice", "onlyoffice", "wps-office", "calligra"
        ],
        "Note-Taking": [
            "joplin", "simplenote", "tomboy-ng", "notable", "cherrytree", "obsidian"
        ],
        "PDF Tools": [
            "evince", "okular", "zathura", "pdftk", "mupdf"
        ],
        "Calendar & Email": [
            "thunderbird", "evolution", "mailspring", "geary", "claws-mail"
        ],
        "Mind Mapping": [
            "freemind", "vym", "xmind", "mindomo"
        ],
        "Productivity & Planning": [
            "trello", "gnome-calendar"
        ]
    },
    "Security & Privacy": {
        "Antivirus": [
            "clamav", "chkrootkit", "rkhunter"
        ],
        "Firewalls": [
            "ufw", "iptables", "nftables", "firewalld", "gufw"
        ],
        "Encryption": [
            "gpg", "veracrypt", "cryptsetup", "keepassxc", "openssl"
        ],
        "Privacy Tools": [
            "tor", "bleachbit", "onionshare", "tailscale", "gnome-keyring"
        ],
        "Password Managers": [
            "bitwarden", "keepassxc", "pass", "buttercup"
        ]
    },
    "Gaming & Emulation": {
        "Game Launchers": [
            "steam", "lutris", "heroic-games-launcher", "itch", "legendary"
        ],
        "Emulators": [
            "dolphin-emu", "pcsx2", "retroarch", "dosbox", "ppsspp", "yuzu", "ryujinx"
        ],
        "Game Streaming": [
            "parsec", "moonlight", "sunshine", "stadia"
        ],
        "Gaming Tools": [
            "mangohud", "gamemode", "vkbasalt", "proton-ge-custom"
        ]
    },
    "Cloud & Remote Access": {
        "Cloud Storage": [
            "dropbox", "megasync", "nextcloud-client", "google-drive-ocamlfuse"
        ],
        "Remote Desktop": [
            "remmina", "teamviewer", "anydesk", "nomachine"
        ],
        "SSH & Terminal Access": [
            "openssh-client", "openssh-server", "mosh", "x2go"
        ],
        "File Sync": [
            "rsync", "syncthing"
        ]
    },
    "Science & Engineering": {
        "Math & Data Analysis": [
            "octave", "scilab", "wxmaxima", "sage-math"
        ],
        "Electronic Design": [
            "kicad", "fritzing", "gnucap", "ltspice"
        ],
        "3D Modeling & CAD": [
            "blender", "freecad", "openscad", "salome"
        ],
        "Data Science & Machine Learning": [
            "r-base", "jupyter-notebook", "scipy", "pandas", "tensorflow", "pytorch", "numpy"
        ],
        "Simulation": [
            "gromacs", "lammps", "nwchem"
        ],
        "Plotting & Visualization": [
            "gnuplot", "matplotlib", "plotly", "veusz"
        ]
    },
    "Education": {
        "Learning Platforms": [
            "moodle", "edubuntu", "skolelinux"
        ],
        "Coding Practice": [
            "codewars", "leetcode-cli"
        ],
        "E-Book Readers": [
            "calibre", "foliate", "okular"
        ]
    },
    "Miscellaneous": {
        "E-Book Management": [
            "calibre", "foliate", "koha"
        ],
        "Finance": [
            "gnucash", "kmymoney", "homebank", "firefly-iii"
        ],
        "Backup & Recovery": [
            "timeshift", "rsnapshot", "deja-dup", "borgbackup", "restic"
        ],
        "System Tweakers": [
            "unattended-upgrades", "bleachbit", "stacer"
        ],
        "Tiling Window Managers": [
            "i3", "bspwm", "awesome", "herbstluftwm", "sway"
        ],
        "Multimedia Utilities": [
            "imagemagick", "ffmpeg", "xvidcap", "shutter", "scrot"
        ],
        "Terminal Multiplexers": [
            "tmux", "screen", "byobu"
        ],
        "Application Launchers": [
            "rofi", "dmenu", "synapse", "ulauncher"
        ],
        "Scripting & Automation": [
            "cron", "systemd-timer", "expect"
        ],
        "Communication": [
            "pidgin", "signal", "discord", "telegram", "slack"
        ],
        "Customization": [
            "gnome-tweaks", "unity-tweak-tool", "lxappearance"
        ],
        "Virtualization Management": [
            "virt-manager", "gnome-boxes"
        ]
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
        return os.geteuid() == 0
    except AttributeError:
        # For Windows compatibility
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

# Function to run commands with admin privileges
def run_as_admin(cmd):
    if not is_admin():
        # Automatically re-run the script with admin privileges for Linux/Unix systems
        try:
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        except Exception as ex:
            p(Fore.RED + f"Failed to elevate privileges: {ex}")
            ask_continue("Exiting due to privilege escalation failure.")
            e()
    result = run(["sudo"] + cmd, capture_output=True, text=True)
    return result

# Function For Printing All Linux Apps
def print_linux_apps():
    p(Fore.YELLOW + "Available Linux Applications:")
    for category, subcategories in linux_apps.items():
        p("\n" + "=" * 40)
        p(Fore.CYAN + f"{category.upper()}")
        p("=" * 40)
        for subcat, apps in subcategories.items():
            p(Fore.GREEN + f"\n{subcat}:")
            p(Fore.WHITE + "  " + ", ".join(apps))
    p("\n" + "=" * 40)

# Function to get AI help for package management
def ai_help(error_message):
    try:
        GenAI.configure(api_key="AIzaSyBDh4vnq-5QQvcmmxWbE3iADan2ZWV1DsU")
        model = GenAI.GenerativeModel("gemini-2.0-flash")
        while True:
            response = model.generate_content(error_message)
            p(Fore.GREEN + Back.WHITE + response.text + "\nPowered By SayyadN")
            user_input = i("You can exit by typing 'exit'. Do you need more help? (Y/N): ").lower()
            if user_input in ["exit", "n"]:
                break
            elif user_input == "y":
                error_message = i("Please provide more details about the issue: ")
            else:
                p(Fore.RED + "Invalid input, please try again.")
    except Exception as ex:
        p(Fore.RED + f"AI help is currently unavailable: {ex}")

# Function To Install Package
def install_package():
    package_manager = detect_package_manager()
    package_name = i("Enter Package Name: ").strip()
    p(Fore.BLUE + f"Attempting to install {package_name} using {package_manager}...")
    cmd = pm_commands[package_manager]["install"] + [package_name]
    result = run_as_admin(cmd)
    if result.returncode == 0:
        p(Fore.GREEN + f"{package_name} installed successfully.")
    else:
        error_msg = f"Failed to install {package_name}: {result.stderr}"
        p(Fore.RED + error_msg)
        get_help = i("Do you want to get help from AI? (Y/N): ").lower()
        if get_help == "y":
            ai_help(error_msg)
    ask_continue("Continue after installation attempt?")

# Function To Remove Package
def remove_package():
    package_manager = detect_package_manager()
    package_name = i("Enter Package Name: ").strip()
    p(Fore.BLUE + f"Attempting to remove {package_name} using {package_manager}...")
    cmd = pm_commands[package_manager]["remove"] + [package_name]
    result = run_as_admin(cmd)
    if result.returncode == 0:
        p(Fore.GREEN + f"{package_name} removed successfully.")
    else:
        error_msg = f"Failed to remove {package_name}: {result.stderr}"
        p(Fore.RED + error_msg)
        get_help = i("Do you want to get help from AI? (Y/N): ").lower()
        if get_help == "y":
            ai_help(error_msg)
    ask_continue("Continue after removal attempt?")

# Function To Update Package or Full System
def update():
    package_manager = detect_package_manager()
    p(Fore.BLUE + f"Updating system using {package_manager}...")
    cmd = pm_commands[package_manager]["update"]
    result = run_as_admin(cmd)
    if result.returncode == 0:
        p(Fore.GREEN + "Update completed successfully.")
    else:
        error_msg = f"Error during update: {result.stderr}"
        p(Fore.RED + error_msg)
        get_help = i("Do you want to get help from AI? (Y/N): ").lower()
        if get_help == "y":
            ai_help(error_msg)
    ask_continue("Continue after update attempt?")

# Function To Upgrade Package or Full System
def upgrade():
    package_manager = detect_package_manager()
    p(Fore.BLUE + f"Upgrading system using {package_manager}...")
    cmd = pm_commands[package_manager]["upgrade"]
    result = run_as_admin(cmd)
    if result.returncode == 0:
        p(Fore.GREEN + "Upgrade completed successfully.")
    else:
        error_msg = f"Error during upgrade: {result.stderr}"
        p(Fore.RED + error_msg)
        get_help = i("Do you want to get help from AI? (Y/N): ").lower()
        if get_help == "y":
            ai_help(error_msg)
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

# Function to list installed packages
def list_installed_packages():
    package_manager = detect_package_manager()
    p(Fore.BLUE + f"Listing installed packages using {package_manager}...")
    if package_manager in ["apt", "dnf", "yum", "zypper", "pacman"]:
        cmd = [package_manager, "list", "--installed"]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            p(Fore.GREEN + "Installed Packages:\n" + result.stdout)
        else:
            p(Fore.RED + f"Failed to list installed packages: {result.stderr}")
    else:
        p(Fore.RED + "Listing installed packages is not supported for this package manager.")
    ask_continue("Continue after listing installed packages?")

# Function to clean up unused packages
def cleanup_system():
    package_manager = detect_package_manager()
    p(Fore.BLUE + f"Cleaning up system using {package_manager}...")
    if package_manager in ["apt", "dnf", "yum", "zypper", "pacman"]:
        cmd = [package_manager, "autoremove", "-y"]
        result = run_as_admin(cmd)
        if result.returncode == 0:
            p(Fore.GREEN + "System cleanup completed successfully.")
        else:
            p(Fore.RED + f"Failed to clean up the system: {result.stderr}")
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

# Function to check network connectivity
def check_network_connectivity():
    hostname = "google.com"
    p(Fore.BLUE + f"Checking network connectivity to {hostname}...")
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        p(Fore.GREEN + f"Network connectivity to {hostname} is OK.")
    else:
        p(Fore.RED + f"Network connectivity to {hostname} is down.")
    ask_continue("Continue after checking network connectivity?")

# Function to ask if the user wants to continue
def ask_continue(message="Do you want to continue? (Y/N): "):
    while True:
        choice = i(Fore.YELLOW + message).strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            p(Fore.YELLOW + "Exiting...")
            e()
        else:
            p(Fore.RED + "Invalid input. Please enter 'Y' or 'N'.")

def main_menu():
    while True:
        p("\n" + "=" * 40)
        p(Fore.CYAN + "Welcome to LinuxToolKit by SayyadN")
        p("=" * 40)
        p("1. Install a Package")
        p("2. Remove a Package")
        p("3. Update System")
        p("4. Upgrade System")
        p("5. Search for a Package")
        p("6. View Available Linux Applications")
        p("7. List Installed Packages")
        p("8. Cleanup System")
        p("9. Display System Information")
        p("10. Check Network Connectivity")
        p("11. Exit")
        p("=" * 40)
        
        choice = i("Enter your choice (1-11): ").strip()
        
        if choice == "1":
            install_package()
        elif choice == "2":
            remove_package()
        elif choice == "3":
            update()
        elif choice == "4":
            upgrade()
        elif choice == "5":
            search_package()
        elif choice == "6":
            print_linux_apps()
        elif choice == "7":
            list_installed_packages()
        elif choice == "8":
            cleanup_system()
        elif choice == "9":
            display_system_info()
        elif choice == "10":
            check_network_connectivity()
        elif choice == "11":
            p(Fore.YELLOW + "Thank you for using LinuxToolKit by SayyadN. Goodbye!")
            e()
        else:
            p(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()