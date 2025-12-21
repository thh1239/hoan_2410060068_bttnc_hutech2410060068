import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def get_key_value(self):
        try:
            return self.ui.txt_key.text().strip()
        except AttributeError:
            return self.ui.txt_key.toPlainText().strip()

    def show_message(self, icon, text):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setText(text)
        msg.exec_()

    def call_api_encrypt(self):
        key = self.get_key_value()
        if not key.isdigit():
            self.show_message(QMessageBox.Warning, "Vui lòng nhập khóa là số và không được để trống!")
            return

        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])
                self.show_message(QMessageBox.Information, "Mã hóa thành công!")
            else:
                self.show_message(QMessageBox.Warning, "Lỗi khi gọi API!")
        except Exception as e:
            self.show_message(QMessageBox.Critical, f"Lỗi kết nối API: {e}")

    def call_api_decrypt(self):
        key = self.get_key_value()
        if not key.isdigit():
            self.show_message(QMessageBox.Warning, "Vui lòng nhập khóa là số và không được để trống!")
            return

        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])
                self.show_message(QMessageBox.Information, "Giải mã thành công!")
            else:
                self.show_message(QMessageBox.Warning, "Lỗi khi gọi API!")
        except Exception as e:
            self.show_message(QMessageBox.Critical, f"Lỗi kết nối API: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())