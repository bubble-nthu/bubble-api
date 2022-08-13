from flask import request
import json

class JsonRequestBody:

    @classmethod
    def parse_json_from_request(self, request):
        req_data = json.loads(request.json)
        return req_data

        """content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            return json
        else:
            data = json.loads(request.data)
            return data"""