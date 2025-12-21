import tornado.ioloop
import tornado.websocket

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop

    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("Đang đọc...")
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",
            callback=self.maybe_retry_connection,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    def maybe_retry_connection(self, future) -> None:
        try:
            self.connection = future.encrypted_message()
        except:
            print("Không thể kết nối lại, sẽ thử lại sau 3 giây...")
            self.io_loop.call_later(3, self.connect_and_read)
            return

    def on_message(self, message):
        if message is None:
            print("Đã ngắt kết nối, đang kết nối lại...")
            self.connect_and_read()
            return

        print(f"Nhận thông báo từ máy chủ: {message}")

        self.connection.read_message(callback=self.on_message)

def main():
    io_loop = tornado.ioloop.IOLoop.current()

    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start)

    io_loop.start()

if __name__ == "__main__":
    main()