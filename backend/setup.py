# setup.py
from setuptools import setup, find_packages

setup(
    name="my_flask_app",           # 套件名稱
    version="0.1.0",               # 版本
    packages=find_packages(),       # 自動尋找 package
    include_package_data=True,     # 包含非 .py 檔案（如 templates、static）
    install_requires=[             # 依賴套件
        "flask>=2.3",
        "flask-cors>=3.0",
        "pillow>=10.0",
        "easyocr>=1.6",
    ],
    python_requires='>=3.10',      # 最低 Python 版本
)