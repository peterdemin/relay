import time
import logging

from flask import Flask, request


storage = {}
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/<key>/', methods=['POST', 'GET'])
def relay_payload(key):
    try:
        if request.method == 'POST':
            if key in storage:
                file = request.files['file']
                if file.size <= 10240:
                    storage[key] = file.read()
                    return 'ok\n'
                else:
                    return 'too big\n'
            else:
                return 'unwanted\n'
        else:
            if key not in storage:
                storage[key] = None
            for attempt in range(10):
                result = storage[key]
                if result is None:
                    time.sleep(1)
                else:
                    del storage[key]
                    return result
            return ''
    except:
        logger.exception("Request %r failed", key)
