from bson import json_util, ObjectId
import json, datetime
from datetime import datetime

def jsonify(data):
    return JSONEncoder(data).encode(data)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)