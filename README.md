# 02-18-2025_desktop-pet-assistant
imagine a smart sentient cat on your screen...


## Here's the State Machine System

![State Machine System](docs/statediagram.jpeg)

## Building the Project for Your Own Use

I use pyinstaller to build the project. This module is already found in the requirements.txt file for your respective operating system:

*Note*: Using python version `3.11.0`

- MAC: `mac-requirements.txt`
- Windows: `windows-requirements.txt`
- Linux: DNE lol

To build the project, simply run the following command in the terminal:

### Mac Compilation Script

```bash
pyinstaller --onedir main.py --name stella-ai --clean --add-data "./assets:assets" --optimize 1 --icon icon.png --noconsole --paths .venv/Lib/site-packages
```


### Windows Compilation Script

```bash
pyinstaller --onefile --paths .venv/Lib/site-packages --name stella-ai --clean --add-data "./assets:assets" --optimize 1 --icon icon.png --noconsole main.py

```