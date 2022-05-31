from os.path import splitext
from datetime import datetime

def images_filename_generator(instance, filename):
	"""Image uploads custom handler."""

	# return 'images/{year}/{name}{ext}'.format(
	#     year=datetime.today().year,
	#     name=datetime.today().strftime('%m%d%H%M%S%f'),
	#     ext=splitext(filename)[1].lower())

	today = datetime.today()

	return '{year}/{week}/{name}{ext}'.format(
		year=today.year,
		week=today.isocalendar()[1],
		name=today.strftime('%m%d%H%M%S%f'),
		ext=splitext(filename)[1].lower())