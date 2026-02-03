import mss
from pathlib import Path
from PIL import Image
import questionary as quest
import pywinctl as pwc
import time
import idk
import platform
import os
from datetime import datetime
import subprocess


def check_wayland():
	is_wayland = bool(os.environ.get("WAYLAND_DISPLAY"))
	return is_wayland

def full_screen(mss):
	monitor = mss.monitors[1]
	image = mss.grab(monitor)
	return image

def specific_window(mss,window_titles):
	unfiltered_titles = pwc.getAllTitles()
	window_titles = list(filter(None, unfiltered_titles))

	window_title = quest.select(
	"what would you like to screenshot?",
	choices=window_titles,
	qmark="",
	).ask()
	if not window_title:
		exit(0)

	window = pwc.getWindowsWithTitle(window_title)[0]
	window.activate()
	monitor = {
		"left" : window.left, 
		"top" : window.top, 
		"width" : window.width, 
		"height" : window.height
	}
	time.sleep(0.1)
	image = mss.grab(monitor)
	return image

def selection(mss):
	if check_wayland():
		selection = subprocess.check_output(["slurp"]).decode().strip()
		image = subprocess.run(["grim", "-g", selection]) 
	else:
		result = idk.main()
		if result is None:
			exit(0)

		x1, y1, x2, y2 = result
		width = abs(x2-x1)
		height = abs(y2-y1)

		if width == 0 or height == 0:
			print("no area selected")
			exit(0)

		monitor = {
			"left" : min(x1, x2), 
			"top" : min(y1, y2), 
			"width" : width, 
			"height" : height
		}
		time.sleep(0.1)
		image = mss.grab(monitor)
	return image

def get_time():
	now = datetime.now()
	formatted = now.strftime("screenshot %Y-%m-%d at %H-%M-%S")
	return formatted

def enter_name():
	png_name = input(" enter a name for your image ('.png' will be added): ")
	if not png_name:
		png_name = get_time()
	if not png_name.lower().endswith(".png"):
		png_name += ".png"
	return png_name

try:
	choices = ["full screen", "specific window", "selection"]

	if check_wayland():
		choices.remove("specific window")

	screen_size = quest.select(
		"what would you like to screenshot?",
		choices=choices,
		qmark="",
		instruction="(use arrow keys!)"
		).ask()
	if not screen_size:
		exit(0)

	png_name = enter_name()

	home = Path.home()
	last_saved_dir = home / ".last_save.txt"

	if last_saved_dir.exists():
		last_dir = Path(last_saved_dir.read_text().strip())
		if not last_dir.exists():
			last_dir = home
	else:
		last_dir = home

	save_dir = quest.path(
	   "where would you like to save the file?",
	   default=str(last_dir),
	   only_directories=True,
	   qmark="",
	).ask()

	if not save_dir:
		exit(0)

	last_saved_dir.write_text(str(save_dir))

	with mss.mss() as mss:
		if screen_size == "full screen":
			image = full_screen(mss)

		elif screen_size == "specific window":
			image = specific_window(mss, choices)
		elif screen_size == "selection":
			image = selection(mss)

		final_shot = Image.frombytes(
			"RGB",
			image.size,
			image.rgb
		)

	final_shot.save(Path(save_dir) / png_name)
	print(f"screenshot saved to {Path(save_dir) / png_name}")
	final_shot.show()

except KeyboardInterrupt:
    exit(0)

