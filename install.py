import subprocess
import os


subprocess.run(["pip", "install","-r", "GUI/requirements.txt"])

os.system("pyinstaller -w -F --distpath GUI GUI/CT_Analyzer.py")




