from rich import print
import os
from sys import platform

from utilities.rich_settings import color_scheme, PANEL_WIDTH

def clear_console():
	if platform == "linux" or platform == "linux2":
		os.system('clear')
	elif platform == "darwin":
		os.system('clear')
	elif platform == "win32":
		os.system('cls')


def separator():
	for i in range(0, PANEL_WIDTH):
		print(f"[{color_scheme['delimiter']}]─", end='') # U+2500
	print('')