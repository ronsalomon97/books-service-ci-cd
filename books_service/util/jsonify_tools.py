import json
from flask import Response
from bson import ObjectId

def custom_jsonify(data):
    try:
        response_data = json.dumps(data, ensure_ascii=False)
        return Response(response_data, mimetype='application/json; charset=utf-8')
    except Exception as e:
        return Response(json.dumps({"error": "Failed to serialize data to JSON", "details": str(e)}),
                        mimetype='application/json; charset=utf-8'), 500
    
def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data