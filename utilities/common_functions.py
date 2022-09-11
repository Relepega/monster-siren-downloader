#	this file contains all the logic needed in every site crawler
#	do not add site-specific functions here

import sys
import os
import time
from typing import Union
import httpx
import ujson as json

from rich.progress import (
	Progress,
	MofNCompleteColumn,
	track,
	TextColumn,
	BarColumn,
	TaskProgressColumn,
	TimeElapsedColumn,
	FileSizeColumn,
	DownloadColumn,
	TransferSpeedColumn,
	TimeRemainingColumn
)


# references in case they're needed:
#	https://python.tutorialink.com/how-to-download-pdf-files-with-playwright-python/
#	https://playwright.dev/python/docs/library

_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
}

def get_app_path():
    # https://www.codegrepper.com/code-examples/python/pyinstaller+onefile+current+working+directory
    
	# determine if the application is a frozen `.exe` (e.g. pyinstaller --onefile) 
	if getattr(sys, 'frozen', False):
		return os.path.dirname(sys.executable)
	# or a script file (e.g. `.py` / `.pyw`)
	elif __file__:
		return os.path.join(os.path.dirname(__file__), '..')


def check_path(path):
	# basepath = os.path.dirname(__file__)
	# newpath = f'{basepath}/{append}'
	if not os.path.exists(path):
		os.makedirs(path)
		return False
	else:
		return True


def file_exists(fp):
	if os.path.exists(fp):
		return True
	
	return False


def dump_data(fp, fn, data):
	check_path(fp)
	with open(os.path.join(fp, f"{fn}_{int(time.time())}.json"), 'w') as json_dump_file:
	# with open(os.path.join(fp, fn), 'w') as json_dump_file:
		json.dump(data, json_dump_file, indent=4)

	return True

def sanitize_path(fp):
	path_sanitized = [*fp] # list(fp)
	for i in range(0, len(path_sanitized)):
		if path_sanitized[i] == '\\':
			path_sanitized[i] = '١'
		elif path_sanitized[i] == '*':
			path_sanitized[i] = '⃰'
		elif path_sanitized[i] == '/':
			path_sanitized[i] = '∕'
		elif path_sanitized[i] == '>':
			path_sanitized[i] = '˃'
		elif path_sanitized[i] == '<':
			path_sanitized[i] = '˂'
		elif path_sanitized[i] == ':':
			path_sanitized[i] = '˸'
		elif path_sanitized[i] == '|':
			path_sanitized[i] = '-'
		elif path_sanitized[i] == '"':
			path_sanitized[i] = '\'\''
	
	try:
		while True:
			if path_sanitized[-1] in ['.', ' ']:
				path_sanitized.pop(-1)
			else:
				break
	except:
		pass
	
	path_sanitized = ''.join(path_sanitized)

	return path_sanitized


def words_in_string(word_list, to_test_string):
    return set(word_list).intersection(to_test_string.split())


def download_file(url, absolute_file_path, http_client: httpx.Client, headers = None):
	http_headers = _headers
	r = None

	if not headers == None:
		http_headers = headers

	rich_progressbar = Progress(
		BarColumn(),
		"[progress.percentage]{task.percentage:>3.1f}%",
		"•",
		DownloadColumn(),
		"•",
		TransferSpeedColumn(),
		"•",
		TimeRemainingColumn(),
	)

	try:
		with http_client.stream("GET", url=url, headers=http_headers, timeout=None) as response:
			total = int(response.headers["Content-Length"])

			if file_exists(absolute_file_path):
				file_size = os.stat(absolute_file_path)
				if file_size.st_size == total:
					print("The file has already been downloaded, skipping...")
					return True

			with rich_progressbar:
				task = rich_progressbar.add_task(' ', total=total)
				num_bytes_downloaded = response.num_bytes_downloaded

				with open(absolute_file_path, 'wb') as file:
					for chunk in response.iter_bytes():
						file.write(chunk)
						rich_progressbar.update(task, advance=response.num_bytes_downloaded - num_bytes_downloaded)
						num_bytes_downloaded = response.num_bytes_downloaded

		return True
	except:
		return False


def get_filecount(folder_path):
	totalFiles = 0
	totalDir = 0

	for base, dirs, files in os.walk(folder_path):
		for directories in dirs:
			totalDir += 1
		for Files in files:
			totalFiles += 1

	return [totalFiles, totalDir]
