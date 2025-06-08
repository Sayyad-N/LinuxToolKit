import os
from PyQt5.QtWidgets import QMessageBox

def check_root_qt(parent=None):
    """للواجهات - يظهر رسالة Qt إذا المستخدم مش Root"""
    if os.getuid() != 0:
        QMessageBox.critical(
            parent,
            "صلاحيات غير كافية",
            "يجب تشغيل البرنامج باستخدام sudo/root."
        )
        exit()

def check_root_cli():
    """للتيرمنال - يطبع رسالة إذا المستخدم مش Root"""
    if os.getuid() != 0:
        print("❌ يجب تشغيل هذا البرنامج باستخدام sudo.")
        exit()
