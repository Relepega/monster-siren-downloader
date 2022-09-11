from rich import box

PANEL_WIDTH = 50
BOX_TYPE = box.ROUNDED # box.ROUNDED: default - box.SIMPLE_HEAD: no borders

color_scheme: dict = {
	# "info": "dim cyan",
	"warning": "magenta",
	# "danger": "bold red",
	"title": "orange_red1",
	"menu.title.text": "indian_red1",
	"menu.title.border": "indian_red1",
	"menu.option.description": "plum1",
	"menu.option.numeration": "royal_blue1 bold", # turquoise2, steel_blue1
	"menu.option.choice.prefix": "pale_violet_red1",
	"menu.option.choice.text": "pale_violet_red1",
	"delimiter": 'light_pink1',
	"status": "bold green",
	"info.main": "bold magenta",
	"info.reply": "light_salmon1",
	"info.number": "cyan1",
	"progress.description": "indian_red1"
}