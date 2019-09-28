from tornado.websocket import WebSocketHandler

import tornado.ioloop
import tornado.web
import tornado.websocket
from PIL import Image
import io
import json
import base64

_FIELD_TYPE = 'type'
_FIELD_CAUSE = 'cause'
_FIELD_IMAGE_PATH = 'image_path'
_FIELD_IMAGE = 'image'
_FIELD_IMAGE_MODE = 'image_mode'
_FIELD_IMAGE_FORMAT = 'image_format'
_FIELD_IMAGE_HEIGHT = 'image_height'
_FIELD_IMAGE_WIDTH = 'image_width'

_TYPE_ERROR = 'error'
_TYPE_GET_IMAGE = 'get_image'
_TYPE_LOAD_IMAGE = 'load_image'
_TYPE_IMAGE = 'image'

class ImmVisWebSocket(tornado.websocket.WebSocketHandler):
    image_path = None
    original_image = None

    def initialize(self, image_path=None):
        self.load_image(image_path)

    def load_image(self, image_path=None):
        self.image_path = image_path or './example_datasets/cps_df.tif'

        try:
            self.original_image = Image.open(self.image_path)
        except:
            self.original_image = None
            return False
        
        return True

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        try:
            payload = json.loads(message)
        except:
            return self.send_error_message(u'Unexpected request format')

        message_type = payload.get(_FIELD_TYPE)

        if message_type == _TYPE_LOAD_IMAGE:
            image_path = payload.get(_FIELD_IMAGE_PATH)
            if self.load_image(image_path):
                self.send_original_image()
            else:
                self.send_error_message(u'Failed to load image.')

        elif message_type == _TYPE_GET_IMAGE:
            self.send_original_image()

        else:
            self.send_error_message(u'Unknown request type.')

    def send_original_image(self):
        if(self.original_image is not None):
            self.send_image(self.original_image)
        else:
            self.send_error_message(u'Image is not available')

    def send_image(self, image):
        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        image_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        width, height = image.size

        response_message = self.create_response_message(
            {
                _FIELD_TYPE : _TYPE_IMAGE,
                _FIELD_IMAGE_FORMAT : image.format,
                _FIELD_IMAGE_MODE : image.mode,
                _FIELD_IMAGE_WIDTH : width,
                _FIELD_IMAGE_HEIGHT : height,
                _FIELD_IMAGE : image_string
            }
        )

        self.write_message(response_message)

    def send_error_message(self, cause):
        message = self.create_response_message(
            {
                _FIELD_TYPE: _TYPE_ERROR,
                _FIELD_CAUSE: cause
            }
        )
        self.write_message(message)

    def create_response_message(self, data_dict):
        return json.dumps(data_dict)

    def on_close(self):
        print("WebSocket closed")


def create_app(image_path=None):
    return tornado.web.Application([
        (r"/websocket", ImmVisWebSocket, {'image_path': image_path})
    ])


if __name__ == "__main__":
    _PORT = 8888

    app = create_app()
    app.listen(str(_PORT))

    print("Starting server: http://localhost:" + str(_PORT) + "/")

    tornado.ioloop.IOLoop.current().start()
