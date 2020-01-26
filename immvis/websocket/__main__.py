import tornado.ioloop
import tornado.web
import tornado.websocket
from websocket.websocket_server import ImmVisWebSocket
from websocket.message_parser import MessageParser
from websocket.data_store import DataStore
from websocket.message_handler import MessageHandler


def create_app():
    message_parser = MessageParser()
    data_store = DataStore()
    message_handler = MessageHandler(message_parser, data_store)

    return tornado.web.Application([
        (r"/websocket", ImmVisWebSocket, {'message_handler': message_handler})
    ])


if __name__ == "__main__":
    _PORT = 8888

    app = create_app()
    app.listen(str(_PORT))

    print("Starting server: http://localhost:" + str(_PORT) + "/")

    tornado.ioloop.IOLoop.current().start()
