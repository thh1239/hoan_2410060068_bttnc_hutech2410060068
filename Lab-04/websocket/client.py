import tornado.ioloop
import tornado.websocket
from tornado import gen

class WebSocketClient:
    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connection = None

    def start(self):
        self.connect()

    def connect(self):
        print("🔄 Đang kết nối WebSocket...")
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",
            callback=self.on_connect,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    def on_connect(self, future):
        try:
            self.connection = future.result()
            print("✅ Kết nối thành công")
        except Exception as e:
            print(f"❌ Kết nối thất bại: {e}")
            print("⏳ Thử lại sau 3 giây...")
            self.io_loop.call_later(3, self.connect)

    def on_message(self, message):
        if message is None:
            print("⚠️ Mất kết nối, đang reconnect...")
            self.connection = None
            self.io_loop.call_later(3, self.connect)
            return

        print(f"📩 Nhận từ server: {message}")

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()

if __name__ == "__main__":
    main()
