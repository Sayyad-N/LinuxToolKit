# Code Written By SayyadN
# Based on: https://github.com/kaotickj/LinFo
# Date: 8-6-2025

import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
import sys
import root_checker

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def get_info():
    info = {
    "نظام التشغيل": run_command("lsb_release -sd 2>/dev/null") or run_command("sw_vers -productName 2>/dev/null"),
    "اسم الجهاز": run_command("hostname"),
    "إصدار النواة": run_command("uname -r"),
    "مدة التشغيل": run_command("uptime -p"),
    "عدد الحزم": run_command("dpkg-query -f '${binary:Package}\n' -W 2>/dev/null | wc -l"),
    "بيئة سطح المكتب": run_command("echo $XDG_CURRENT_DESKTOP | tr '[:upper:]' '[:lower:]'"),
    "مدير النوافذ": run_command("echo $XDG_SESSION_TYPE"),
    "الثيم": run_command("gsettings get org.gnome.desktop.interface gtk-theme"),
    "أيقونات الثيم": run_command("gsettings get org.gnome.desktop.interface icon-theme"),
    "دقة الشاشة": run_command("xdpyinfo | awk '/dimensions:/ {print $2}'"),
    "الطرفية": run_command("echo $TERM"),
    "القشرة": run_command("basename $SHELL"),
    "المعالج": run_command("lscpu | awk -F':' '/Model name/ {print $2}' | sed -e 's/^\\s*//'"),
    "بطاقة الرسوميات": run_command("lspci | grep -i 'vga\\|3d' | awk -F': ' '{print $2}'"),
    "الذاكرة العشوائية": run_command("grep MemTotal /proc/meminfo | awk '{print $2/1024/1024 \"GB\"}'") + " (تقريباً)",
    "استخدام القرص": run_command("df -h --total | awk '/total/ {print $2 \" مستخدم, \" $4 \" متاح\"}'"),
    "واجهات الشبكة": run_command("ip -o link show | awk -F': ' '{print $2}' | grep -v 'lo'").split('\n')
    }

    return info


def get_interface_ips(interfaces):
    ip_map = {}
    for interface in interfaces:
        ip = run_command(f"ip -o addr show dev {interface} | awk '$3 == \"inet\" {{print $4}}'")
        ip_map[interface] = ip
    return ip_map


class SystemInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("معلومات النظام ")
        self.setGeometry(200, 200, 600, 600)
        self.layout = QVBoxLayout()

        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)

        self.refresh_btn = QPushButton("🔄 تحديث المعلومات")
        self.refresh_btn.clicked.connect(self.display_info)

        self.layout.addWidget(QLabel("معلومات النظام الكاملة:"))
        self.layout.addWidget(self.info_display)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)
        self.display_info()

    def display_info(self):
        info = get_info()
        interfaces_info = get_interface_ips(info["واجهات الشبكة"])

        lines = []
        for key, value in info.items():
            if key != "Interfaces":
                lines.append(f"{key}:  {value}")
        lines.append("Interfaces:")
        for iface, ip in interfaces_info.items():
            lines.append(f"    {iface}: {ip}")

        self.info_display.setPlainText("\n".join(lines))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemInfoApp()
    root_checker.check_root_qt(window)
    window.show()
    sys.exit(app.exec())
