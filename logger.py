from dbco import *
import time

def log(request):
	if 'localhost' not in request.base_url: # not if we are running locally, only for real requests
		db.api_log.insert_one({'timestamp': int(time.time()), 'path': request.path, 'ip_addr': request.remote_addr})