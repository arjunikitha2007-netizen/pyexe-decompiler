#!/usr/bin/env python3
import os
import sys
import subprocess
import urllib.request

def download_extractor():
    if not os.path.exists("pyinstxtractor.py"):
        print("📥 Downloading pyinstxtractor...")
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py",
            "pyinstxtractor.py"
        )

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "uncompyle6"], capture_output=True)

def decompile_exe(exe_path):
    if not os.path.exists(exe_path):
        print(f"❌ File not found: {exe_path}")
        return
    
    download_extractor()
    install_dependencies()
    
    print(f"🔧 Extracting {exe_path}...")
    subprocess.run([sys.executable, "pyinstxtractor.py", exe_path])
    
    folder = exe_path.replace('.exe', '_extracted')
    if os.path.exists(folder):
        print(f"🔍 Decompiling files in {folder}...")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.pyc'):
                    pyc = os.path.join(root, file)
                    py = pyc.replace('.pyc', '.py')
                    subprocess.run(['uncompyle6', '-o', py, pyc], capture_output=True)
                    print(f"✅ Decompiled: {file}")
        print(f"\n✨ Done! Check {folder} for .py files")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decompile.py file.exe")
        sys.exit(1)
    decompile_exe(sys.argv[1])
