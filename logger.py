from dbco import *
import datetime

def log(request):
	if 'localhost' not in request.base_url: # not if we are running locally, only for real requests
		ip = getRemoteIP(request)
		db.api_log.insert_one({'timestamp': datetime.datetime.now(), 'path': request.path, 'ip_addr': ip})

def getRemoteIP(request):
	if request.headers.getlist("X-Forwarded-For"):
		return request.headers.getlist("X-Forwarded-For")[0]
	else:
		return request.remote_addr
