import os
import sys
from PyInstaller.__main__ import run

# if windows
if sys.platform == "win32":
    
    run(
        [
            '--onefile',
            '--paths', '.venv/Lib/site-packages',
            '--name', 'stella-ai',
            '--clean',
            '--add-data', './assets:assets',
            '--optimize', '1',
            '--icon', 'icon.png',
            '--noconsole',
            'main.py'
        ]
    )
    
# or is mac
elif sys.platform == "darwin":
    
    run(
        [
            '--onedir',
            '--paths', '.venv/Lib/site-packages',
            '--name', 'stella-ai',
            '--clean',
            '--add-data', './assets:assets',
            '--optimize', '1',
            '--icon', 'icon.png',
            '--noconsole',
            'main.py'
        ]
    )