from flask import send_file
from getUrl import *
from urlparse import urljoin
import os.path
import urllib2

def get_favicon(source):
	fileLoc = 'static/favicon/'+source+'.ico'
	notFound = False
	if not os.path.isfile(fileLoc):
		domain = 'http://'+source
		urlReturn = getUrl(domain)
		if 'error' not in urlReturn:
			icon = urlReturn['soup'].find("link", type="image/x-icon")
			if icon is None:
				icon = urlReturn['soup'].find("link", rel="shortcut icon")
			if icon is None:
				icon = urlReturn['soup'].find("link", rel="icon")
			if icon is not None:
				icon_link = icon.get('href', '')
				icon_link = urljoin(domain, icon_link)
				icon = urllib2.urlopen(icon_link)
				with open(fileLoc, 'wb') as f:
					f.write(icon.read())
			else:
				notFound = True
		else:
			notFound = True
	if notFound:
		fileLoc = 'static/favicon/noicon.png'

	return send_file(fileLoc, mimetype='image/x-icon')

if __name__ == '__main__':
	print get_favicon('france24.com')