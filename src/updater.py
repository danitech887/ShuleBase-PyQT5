import sys, requests, hashlib, os
from PyQt5.QtWidgets import*

class UpdaterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PMS Updater")
        self.setGeometry(300,300,400,200)
        self.main_layout = QVBoxLayout()
        self.version_label = QLabel('Current version: 1.0')
        self.main_layout.addWidget(self.version_label)

        self.progress_bar = QProgressBar()
        self.main_layout.addWidget(self.progress_bar)

        self.update_btn = QPushButton('Check for Updates')
        self.update_btn.clicked.connect(self.check_for_updates)
        self.main_layout.addWidget(self.update_btn)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def check_for_updates(self):
        server_url = "https://example.com/manifest.json"
        try:
            response = requests.get(server_url)
            response.raise_for_status()
            manifest = response.json()
            latest_version = manifest['version']
            download_url = manifest['url']

            if latest_version > '1.0':
                self.download_update(download_url)

            else:
                self.version_label.setText("Your PMS version is up_to_date")
        except Exception as e:
            self.version_label.setText(f"Update check failed: {e}")
    def download_update(self,url):
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length',0))
            downloaded = 0
            with open('update.zip','wb') as file:
                for data in response.iter_content(chunk_size=1024):
                    downloaded += len(data)
                    file.write(data)
                    self.progress_bar.setValue((downloaded / total_size) * 100)
                    self.version_label.setText("New Version of PMS downloaded Installing on progress")
        except Exception as e:
            self.version_label.setText(f'Download failed: {e}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    updater = UpdaterApp()
    updater.show()
    sys.exit(app.exec_())
