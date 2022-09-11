import httpx

from bs4 import BeautifulSoup

from utilities.common_functions import _headers

def get_html_object(url, mode = 'lxml'):
	response = httpx.get(url, headers = _headers, timeout = None)

	try:
		response.raise_for_status()
		return BeautifulSoup(response.content, mode)
	except httpx.HTTPStatusError as exc:
		print(f'Error response "{str(exc)}"" while requesting {exc.request.url!r}.')
