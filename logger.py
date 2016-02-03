from dbco import *
import time

def log(request):
	print request.headers.getlist("X-Forwarded-For")
	
	if 'localhost' not in request.base_url: # not if we are running locally, only for real requests
		ip = getRemoteIP(request)
		db.api_log.insert_one({'timestamp': int(time.time()), 'path': request.path, 'ip_addr': ip})

def getRemoteIP(request):
	if request.headers.getlist("X-Forwarded-For"):
		return request.headers.getlist("X-Forwarded-For")[0]
	else:
		return request.remote_addr
