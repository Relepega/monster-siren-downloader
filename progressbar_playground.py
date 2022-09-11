import os
import sys
import httpx

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

def downloader1(url, download_file):
	with httpx.stream("GET", url) as response:
		total = int(response.headers["Content-Length"])

		with Progress(TextColumn("{task.description}"), BarColumn(), TaskProgressColumn(), FileSizeColumn(), TimeElapsedColumn()) as rich_progressbar:
			task = rich_progressbar.add_task('Downloading test file...', total=total)
			num_bytes_downloaded = response.num_bytes_downloaded

			for chunk in response.iter_bytes():
				download_file.write(chunk)
				rich_progressbar.update(task, advance=response.num_bytes_downloaded - num_bytes_downloaded)
				num_bytes_downloaded = response.num_bytes_downloaded


def downloader2(url, download_file):
	with httpx.stream("GET", url) as response:
		total = int(response.headers["Content-Length"])

		with Progress(
			TextColumn("{task.description}", justify="right"),
			BarColumn(),
			"[progress.percentage]{task.percentage:>3.1f}%",
			"•",
			DownloadColumn(),
			"•",
			TransferSpeedColumn(),
			"•",
			TimeRemainingColumn(),
		) as rich_progressbar:

			task = rich_progressbar.add_task('Downloading test file...', total=total)
			num_bytes_downloaded = response.num_bytes_downloaded

			for chunk in response.iter_bytes():
				download_file.write(chunk)
				rich_progressbar.update(task, advance=response.num_bytes_downloaded - num_bytes_downloaded)
				num_bytes_downloaded = response.num_bytes_downloaded


def downloader3(url, filepath):
	rich_progressbar = Progress(
		# TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
		TextColumn("{task.description}"),
		# BarColumn(bar_width=None),
		BarColumn(),
		"[progress.percentage]{task.percentage:>3.1f}%",
		"•",
		DownloadColumn(),
		"•",
		TransferSpeedColumn(),
		"•",
		TimeRemainingColumn(),
	)

	with httpx.stream("GET", url) as response:
		total = int(response.headers["Content-Length"])

		with rich_progressbar:
			task = rich_progressbar.add_task('Downloading test file...', total=total)
			num_bytes_downloaded = response.num_bytes_downloaded

			with open(filepath, 'wb') as file:
				for chunk in response.iter_bytes():
					file.write(chunk)
					rich_progressbar.update(task, advance=response.num_bytes_downloaded - num_bytes_downloaded)
					num_bytes_downloaded = response.num_bytes_downloaded


def main():
	filepath = os.path.join(os.path.dirname(__file__), '100mb.bin')
	url = "https://speed.hetzner.de/100MB.bin"
	downloader3(url, filepath)


if __name__ == '__main__':
	main()