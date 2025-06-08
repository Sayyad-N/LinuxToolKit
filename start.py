from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout
import sys
import os
import threading
from core import root_checker

app = QApplication([])
root = QWidget()
root.setWindowTitle("لوحه اداره لينكس -- Linux Tool Kit")
root.setGeometry(200, 200, 400, 200)

layout = QVBoxLayout()

def run_command(command):
    def target():
        os.system(command)
    threading.Thread(target=target).start()

manage_pac = QPushButton("ادارة الحزم")
manage_pac.clicked.connect(lambda: run_command("python3 core/package_manager.py"))

get_system_info = QPushButton("جلب معلومات النظام")
get_system_info.clicked.connect(lambda: run_command("python3 core/system_info.py"))

manage_users = QPushButton("ادارة المستخدمين")
manage_users.clicked.connect(lambda: run_command("python3 core/user_manager.py"))

layout.addWidget(manage_pac)
layout.addWidget(get_system_info)
layout.addWidget(manage_users)

root.setLayout(layout)
root_checker.check_root_qt(root)
root.show()

sys.exit(app.exec_())
