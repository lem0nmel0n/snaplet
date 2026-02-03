# snaplet
a cute little screenshot tool with a cli interface and minimal gui (for selection). developed in python.

## how it's made
made in python 3.13.

the main program runs in the command-line and uses questionary for the prompts. also made a lightweight selection gui using tkinter.

## platforms
- windows 10+ : supported
- linux : supported on x11; the wayland version has a few differences. tested on ubuntu 24.04.
- macos : ...may or may not work. still untested
- other: please don't @ me :)

## how it works :]
1. answer a few cli prompts (using questionary)
2. simple gui in case you select your screenshot
3. screenshot is saved automatically

## requirements
- python 3.x
- dependencies are listed in the requirements.txt

## installation
1. make sure you have python 3.x installed
2. clone or download snaplet
3. navigate to the project folder:
   ```bash
   cd C:\path\to\snaplet
5. install dependencies:
   ```bash
   pip install -r requirements.txt
6. run!
   ```bash
   python main.py

## notes
small learning project. proceed with caution

i was actually pretty proud of this. it was pretty awesome to learn about screenshotting in python.



