from bson import json_util
import json

def jsonify(data):
	for d in data:
		if '_id' in d:
			print d
			d['_id'] = str(d['_id'])
	return json.dumps(data, default=json_util.default)