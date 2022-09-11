import os
import time
import traceback
from datetime import datetime
import httpx
import ujson
from rich import print
from utilities.common_functions import check_path, download_file, file_exists, get_app_path, sanitize_path
from utilities.web_interfaces import get_html_object
from utilities.print import clear_console

def main():
	clear_console()

	httpx_client = httpx.Client()

	print("getting data from website...")
	soup = get_html_object('https://monster-siren.hypergryph.com/music')
	albums = [e['data-album-slider-id'] for e in soup.select('.album___2IOvD')]
	print("Done!")
	print('------------------------')

	APP_PATH = get_app_path()

	download_data: list[dict] = []
	albums_dummy_data: list[dict] = []
	songs_dummy_data: list[dict] = []

	for album in albums:
		print(f'Getting infos for album id "{album}"')
		album_json = httpx_client.get(f'https://monster-siren.hypergryph.com/api/album/{album}/detail', timeout=None).json()
		
		album_folder = os.path.join(APP_PATH, 'Downloads', f"{album_json['data']['cid']} - {album_json['data']['name']}")

		album_cover_fn = f"cover.{album_json['data']['coverUrl'].split('.')[-1]}"
		album_full_banner_fn = f"banner.{album_json['data']['coverDeUrl'].split('.')[-1]}"

		download_data.append({
			'filename': album_cover_fn,
			'filepath': os.path.join(album_folder, sanitize_path(album_cover_fn)),
			'basepath': album_folder,
			'albumname': f"{album_json['data']['cid']} - {album_json['data']['name']}",
			'url': album_json['data']['coverUrl']
		})

		download_data.append({
			'filename': album_full_banner_fn,
			'filepath': os.path.join(album_folder, sanitize_path(album_full_banner_fn)),
			'basepath': album_folder,
			'albumname': f"{album_json['data']['cid']} - {album_json['data']['name']}",
			'url': album_json['data']['coverDeUrl']
		})

		albums_dummy_data.append(album_json)

		for song in album_json['data']['songs']:
			song_id = song['cid']
			print(f'Getting infos for song id  "{album}\{song_id}"')

			song_json = httpx_client.get(f'https://monster-siren.hypergryph.com/api/song/{song_id}', timeout=None).json()

			song_name = song_json['data']['name']
			song_artists = ', '.join(song_json['data']['artists'])

			song_fullname = f"{song_artists} - {song_name} - {song_id}.{song_json['data']['sourceUrl'].split('.')[-1]}"
			song_lyrics_fullname = f'{song_artists} - {song_name} - {song_id}.lrc'

			download_data.append({
				'filename': song_fullname,
				'filepath': os.path.join(album_folder, sanitize_path(song_fullname)),
				'basepath': album_folder,
				'albumname': f"{album_json['data']['cid']} - {album_json['data']['name']}",
				'url': song_json['data']['sourceUrl']
			})

			download_data.append({
				'filename': song_lyrics_fullname,
				'filepath': os.path.join(album_folder, sanitize_path(song_lyrics_fullname)),
				'basepath': album_folder,
				'albumname': f"{album_json['data']['cid']} - {album_json['data']['name']}",
				'url': song_json['data']['lyricUrl']
			})

			songs_dummy_data.append(song_json)

		print('------------------------')

	print('\n')

	time_now = str(datetime.utcnow()).replace(':', '-')

	dump_path = os.path.join(APP_PATH, 'dumps', str(time_now))

	albums_dummy_data_fp = os.path.join(dump_path, f'albums_dummy_data.json')
	songs_dummy_data_fp = os.path.join(dump_path, f'albums_dummy_data.json')
	download_data_fp = os.path.join(dump_path, f'download_data.json')

	check_path(dump_path)

	with open(albums_dummy_data_fp, 'w') as f:
		ujson.dump(albums_dummy_data, f)

	with open(songs_dummy_data_fp, 'w') as f:
		ujson.dump(songs_dummy_data, f)

	with open(download_data_fp, 'w') as f:
		ujson.dump(download_data, f)


	for data in download_data:
		if data['url'] == None:
			continue

		print(f"Now downloading: \"{data['albumname']}\\{data['filename']}\"")

		check_path(data['basepath'])
		# if not file_exists(data['filepath']):
		download_file(
			url=data['url'],
			absolute_file_path=data['filepath'],
			http_client=httpx_client
		)
		# else:
		# 	print("The file has already been downloaded, skipping...")
		print('------------------------')


	httpx_client.close()


if __name__ == '__main__':
	logfile_path = os.path.join(os.path.dirname(__file__), 'Logs')
	logfile_filename = f'{time.time()}.log'
	logfile = os.path.join(logfile_path, logfile_filename)

	try:
		main()
		_ = input('Done! Press enter to continue...')
	except Exception:
		print('An error occurred, check "Logs" folder for more details')
		check_path(logfile_path)
		with open(logfile, 'w+') as f:
			traceback.print_exc(file=f)
		time.sleep(5)