# SayyadN - إدارة شاملة لمستخدمي لينوكس باستخدام PyQt5
# التاريخ: 7-6-2025

import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox,
    QVBoxLayout, QInputDialog
)
import root_checker

# واجهة Qt
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("إدارة المستخدمين - Linux")
window.setGeometry(300, 300, 500, 600)
layout = QVBoxLayout()

# اختصارات
run = subprocess.run

# رسائل
info = lambda msg: QMessageBox.information(window, "معلومة", msg)
error = lambda msg: QMessageBox.critical(window, "خطأ", msg)

# فحص وجود مستخدم
def user_exists(name):
    r = run(["id", name], capture_output=True)
    return r.returncode == 0

# إنشاء مستخدم
def create_user():
    name, ok = QInputDialog.getText(window, "إنشاء مستخدم", "ادخل اسم المستخدم:")
    if ok and name:
        if user_exists(name):
            error("المستخدم موجود بالفعل")
        else:
            r = run(["useradd", name], capture_output=True, text=True)
            info("تم إنشاء المستخدم" if r.returncode == 0 else r.stderr)

# حذف مستخدم
def delete_user():
    name, ok = QInputDialog.getText(window, "حذف مستخدم", "ادخل اسم المستخدم:")
    if ok and name:
        if not user_exists(name):
            error("المستخدم غير موجود")
        else:
            r = run(["userdel", "-r", name], capture_output=True, text=True)
            info("تم حذف المستخدم" if r.returncode == 0 else r.stderr)

# تغيير كلمة مرور
def change_password():
    name, ok = QInputDialog.getText(window, "تغيير كلمة المرور", "ادخل اسم المستخدم:")
    if ok and name:
        if user_exists(name):
            run(["passwd", name])
        else:
            error("المستخدم غير موجود")

# إضافة لمجموعة
def add_to_group():
    name, ok = QInputDialog.getText(window, "إضافة لمجموعة", "ادخل اسم المستخدم:")
    if ok and name and user_exists(name):
        group, g_ok = QInputDialog.getText(window, "اسم المجموعة", "ادخل اسم المجموعة:")
        if g_ok and group:
            r = run(["usermod", "-aG", group, name], capture_output=True, text=True)
            info("تمت الإضافة" if r.returncode == 0 else r.stderr)
        else:
            error("لم يتم إدخال اسم المجموعة")
    else:
        error("المستخدم غير موجود")

# عرض المستخدمين
def list_users():
    users = []
    with open("/etc/passwd") as f:
        for line in f:
            parts = line.split(":")
            if int(parts[2]) >= 1000 and "/home" in parts[5]:
                users.append(parts[0])
    info("\n".join(users))

# قفل الحساب
def lock_user():
    name, ok = QInputDialog.getText(window, "قفل حساب", "ادخل اسم المستخدم:")
    if ok and name and user_exists(name):
        run(["passwd", "-l", name])
        info(f"تم قفل الحساب: {name}")
    else:
        error("المستخدم غير موجود")

# فتح الحساب
def unlock_user():
    name, ok = QInputDialog.getText(window, "فتح حساب", "ادخل اسم المستخدم:")
    if ok and name and user_exists(name):
        run(["passwd", "-u", name])
        info(f"تم فتح الحساب: {name}")
    else:
        error("المستخدم غير موجود")

# فحص صلاحيات المستخدم
def check_groups():
    name, ok = QInputDialog.getText(window, "صلاحيات المستخدم", "ادخل اسم المستخدم:")
    if ok and name and user_exists(name):
        r = run(["groups", name], capture_output=True, text=True)
        info(r.stdout if r.returncode == 0 else r.stderr)
    else:
        error("المستخدم غير موجود")

# تغيير shell أو home
def change_shell_home():
    name, ok = QInputDialog.getText(window, "تعديل مستخدم", "ادخل اسم المستخدم:")
    if not (ok and name and user_exists(name)):
        error("المستخدم غير موجود")
        return
    shell, ok1 = QInputDialog.getText(window, "تعديل الشيل", "ادخل المسار الجديد لـ shell:")
    home, ok2 = QInputDialog.getText(window, "تعديل home", "ادخل المسار الجديد لـ home:")
    if ok1 and shell:
        run(["usermod", "-s", shell, name])
    if ok2 and home:
        run(["usermod", "-d", home, "-m", name])
    info("تم تعديل البيانات")

# الأزرار
buttons = [
    ("✅ إنشاء مستخدم", create_user),
    ("🗑️ حذف مستخدم", delete_user),
    ("🔑 تغيير كلمة مرور", change_password),
    ("➕ إضافة لمجموعة", add_to_group),
    ("📋 عرض المستخدمين", list_users),
    ("🔐 قفل حساب", lock_user),
    ("🔓 فتح حساب", unlock_user),
    ("👁️‍🗨️ عرض صلاحيات", check_groups),
    ("⚙️ تعديل Shell/Home", change_shell_home),
]

for label, func in buttons:
    btn = QPushButton(label)
    btn.setFixedHeight(40)
    btn.clicked.connect(func)
    layout.addWidget(btn)
    
root_checker.check_root_qt(window)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())
