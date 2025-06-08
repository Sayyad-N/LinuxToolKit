import sys
import os
from subprocess import run
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
                             QMessageBox, QComboBox)
from PyQt5.QtCore import Qt

try:
    import google.generativeai as genai
    import_good = True
except ImportError:
    import_good = False
import root_checker

API_KEY = "AIzaSyCDXhbDjtMMbKkm0FKGMr3SPAPaQ_aWYBQ"
p = print

pm_commands = {
    "apt": {"install": ["apt", "install", "-y"], "remove": ["apt", "remove", "-y"], "update": ["apt", "update"], "upgrade": ["apt", "upgrade", "-y"], "search": ["apt", "search"], "info": ["apt", "show"]},
    "dnf": {"install": ["dnf", "install", "-y"], "remove": ["dnf", "remove", "-y"], "update": ["dnf", "update"], "upgrade": ["dnf", "upgrade", "-y"], "search": ["dnf", "search"], "info": ["dnf", "info"]},
    "yum": {"install": ["yum", "install", "-y"], "remove": ["yum", "remove", "-y"], "update": ["yum", "update"], "upgrade": ["yum", "upgrade", "-y"], "search": ["yum", "search"]},
    "zypper": {"install": ["zypper", "install", "-y"], "remove": ["zypper", "remove", "-y"], "update": ["zypper", "refresh"], "upgrade": ["zypper", "update", "-y"], "search": ["zypper", "search"]},
    "pacman": {"install": ["pacman", "-S", "--noconfirm"], "remove": ["pacman", "-R", "--noconfirm"], "update": ["pacman", "-Sy"], "upgrade": ["pacman", "-Su", "--noconfirm"], "search": ["pacman", "-Ss"], "info": ["pacman", "-Si"]},
    "apk": {"install": ["apk", "add"], "remove": ["apk", "del"], "update": ["apk", "update"], "upgrade": ["apk", "upgrade"], "search": ["apk", "search"], "info": ["apk", "info"]},
    "snap": {"install": ["snap", "install"], "remove": ["snap", "remove"], "update": ["snap", "refresh"], "search": ["snap", "find"]},
    "flatpak": {"install": ["flatpak", "install", "-y"], "remove": ["flatpak", "uninstall", "-y"], "update": ["flatpak", "update"], "search": ["flatpak", "search"], "info": ["flatpak", "info"]},
    "nix": {"install": ["nix-env", "-iA"], "remove": ["nix-env", "-e"], "update": ["nix-channel", "--update"], "upgrade": ["nix-env", "-u"], "search": ["nix-env", "-qa"]},
    "urpmi": {"install": ["urpmi"], "remove": ["urpme"], "update": ["urpmi.update"], "upgrade": ["urpmi", "upgrade"], "search": ["urpmq"]},
    "rpm": {"install": ["rpm", "-i", "--force", "--nodeps"], "remove": ["rpm", "-e", "--nodeps"], "update": ["rpm", "-U", "--force", "--nodeps"], "query": ["rpm", "-q"]},
    "portage": {"install": ["emerge", "--ask", "--verbose"], "remove": ["emerge", "--unmerge", "--ask", "--verbose"], "update": ["emerge", "--sync"], "upgrade": ["emerge", "--update", "--deep", "--with-bdeps=y", "--newuse", "--ask", "--verbose"], "search": ["eix"]}
}

def detect_package_manager():
    for manager in pm_commands:
        if run(["which", manager], capture_output=True).returncode == 0:
            return manager
    return None

def ai_help(error_message):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(error_message)
        return response.text
    except Exception as ex:
        return f"⚠️ الذكاء الاصطناعي غير متوفر: {ex}"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("أداة إدارة الحزم")
        self.setGeometry(300, 200, 600, 400)
        self.pm = detect_package_manager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.pm_label = QLabel(f"مدير الحزم المكتشف: {self.pm if self.pm else 'غير موجود - اختر يدوياً'}")
        layout.addWidget(self.pm_label)

        self.pm_selector = QComboBox()
        self.pm_selector.addItems(pm_commands.keys())
        if self.pm:
            index = list(pm_commands.keys()).index(self.pm)
            self.pm_selector.setCurrentIndex(index)
        layout.addWidget(self.pm_selector)

        self.pkg_label = QLabel("اسم الحزمة:")
        self.pkg_input = QLineEdit()
        layout.addWidget(self.pkg_label)
        layout.addWidget(self.pkg_input)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        btn_layout = QHBoxLayout()

        self.install_btn = QPushButton("تثبيت")
        self.install_btn.clicked.connect(self.install_package)
        btn_layout.addWidget(self.install_btn)

        self.remove_btn = QPushButton("إزالة")
        self.remove_btn.clicked.connect(self.remove_package)
        btn_layout.addWidget(self.remove_btn)

        self.update_btn = QPushButton("تحديث")
        self.update_btn.clicked.connect(self.update_package)
        btn_layout.addWidget(self.update_btn)

        self.upgrade_btn = QPushButton("ترقية")
        self.upgrade_btn.clicked.connect(self.upgrade_system)
        btn_layout.addWidget(self.upgrade_btn)

        self.search_btn = QPushButton("بحث")
        self.search_btn.clicked.connect(self.search_package)
        btn_layout.addWidget(self.search_btn)

        self.info_btn = QPushButton("عرض معلومات")
        self.info_btn.clicked.connect(self.show_package_info)
        btn_layout.addWidget(self.info_btn)

        self.cleanup_btn = QPushButton("تنظيف النظام")
        self.cleanup_btn.clicked.connect(self.cleanup_system)
        btn_layout.addWidget(self.cleanup_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_pm(self):
        return self.pm_selector.currentText()

    def run_command(self, cmd):
        self.output.append(f"> {' '.join(cmd)}")
        result = run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.output.append(result.stdout)
            return True
        else:
            self.output.append(result.stderr)
            return False

    def install_package(self):
        pm = self.get_pm()
        pkg = self.pkg_input.text().strip()
        if not pkg:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم الحزمة.")
            return
        cmd = pm_commands[pm]["install"] + [pkg]
        if not self.run_command(cmd):
            self.output.append("مساعدة AI:\n" + ai_help(f"فشل تثبيت الحزمة {pkg} باستخدام {pm}."))

    def remove_package(self):
        pm = self.get_pm()
        pkg = self.pkg_input.text().strip()
        if not pkg:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم الحزمة.")
            return
        cmd = pm_commands[pm]["remove"] + [pkg]
        if not self.run_command(cmd):
            self.output.append("مساعدة AI:\n" + ai_help(f"فشل إزالة الحزمة {pkg} باستخدام {pm}."))

    def update_package(self):
        pm = self.get_pm()
        cmd = pm_commands[pm]["update"]
        if not self.run_command(cmd):
            self.output.append("مساعدة AI:\n" + ai_help(f"فشل تحديث النظام باستخدام {pm}."))

    def upgrade_system(self):
        pm = self.get_pm()
        if "upgrade" not in pm_commands[pm]:
            self.output.append("⚠️ هذا المدير لا يدعم الترقية.")
            return
        cmd = pm_commands[pm]["upgrade"]
        if not self.run_command(cmd):
            self.output.append("مساعدة AI:\n" + ai_help(f"فشل ترقية النظام باستخدام {pm}."))

    def search_package(self):
        pm = self.get_pm()
        pkg = self.pkg_input.text().strip()
        if not pkg:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم الحزمة.")
            return
        cmd = pm_commands[pm]["search"] + [pkg]
        if not self.run_command(cmd):
            self.output.append("مساعدة AI:\n" + ai_help(f"فشل البحث عن الحزمة {pkg} باستخدام {pm}."))

    def show_package_info(self):
        pm = self.get_pm()
        pkg = self.pkg_input.text().strip()
        if not pkg:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم الحزمة.")
            return
        if "info" not in pm_commands[pm]:
            self.output.append(f"⚠️ مدير الحزم {pm} لا يدعم عرض معلومات الحزمة.")
            return
        cmd = pm_commands[pm]["info"] + [pkg]
        if not self.run_command(cmd):
            self.output.append("مساعدة AI:\n" + ai_help(f"فشل عرض معلومات الحزمة {pkg} باستخدام {pm}."))

    def cleanup_system(self):
        pm = self.get_pm()
        if pm == "apt":
            cmds = [["apt", "clean"], ["apt", "autoremove", "-y"]]
        elif pm == "dnf":
            cmds = [["dnf", "clean", "all"], ["dnf", "autoremove", "-y"]]
        else:
            self.output.append("⚠️ عملية التنظيف غير مدعومة لهذا المدير.")
            return

        for cmd in cmds:
            if not self.run_command(cmd):
                self.output.append("مساعدة AI:\n" + ai_help(f"فشل تنظيف النظام باستخدام {pm}."))
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    root_checker.check_root_qt(window)
    window.show()
    sys.exit(app.exec())
