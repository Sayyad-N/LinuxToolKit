#!/bin/bash

# نجيب اسم المستخدم الحالي
USERNAME=$(whoami)

# مسار التثبيت داخل مجلد المستخدم
TARGET_DIR="/home/$USERNAME/LinuxToolKit"

echo ">>> إنشاء مجلد التطبيق في $TARGET_DIR"
mkdir -p "$TARGET_DIR/core"

echo ">>> نقل start.py إلى $TARGET_DIR"
cp start.py "$TARGET_DIR/"

echo ">>> نقل ملفات core إلى $TARGET_DIR/core"
cp core/package_manager.py "$TARGET_DIR/core/"
cp core/root_checker.py "$TARGET_DIR/core/"
cp core/system_info.py "$TARGET_DIR/core/"
cp core/user_manager.py "$TARGET_DIR/core/"

# إعطاء صلاحيات تشغيل وقراءة
chmod -R u+rwX "$TARGET_DIR"

echo ">>> تثبيت مكتبة PyQt5"
pip install PyQt5
PIP_EXIT_CODE=$?

if [ $PIP_EXIT_CODE -ne 0 ]; then
    echo ">>> خطأ في pip install، جاري تحميل سكربت إصلاح pip وتشغيله..."
    curl -sSL https://raw.githubusercontent.com/Sayyad-N/fix-pip/main/fix_pip_problems.sh -o fix_pip_problems.sh
    chmod +x fix_pip_problems.sh
    ./fix_pip_problems.sh

    echo ">>> محاولة تثبيت PyQt5 مرة أخرى بعد الإصلاح"
    pip install PyQt5 google-genai
fi

echo ">>> إنشاء أمر linux في /usr/local/bin لتشغيل البرنامج بصلاحيات root"

sudo tee /usr/local/bin/linux > /dev/null << EOF
#!/bin/bash
cd "/home/$USERNAME/LinuxToolKit"
sudo python3 start.py
EOF

sudo chmod +x /usr/local/bin/linux

echo "✅ تم التثبيت بنجاح!"
echo "🔐 شغّل أداتك بكتابة: linux (سيطلب كلمة مرور sudo)"

