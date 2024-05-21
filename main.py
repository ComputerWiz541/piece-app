import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
import subprocess
import cv2
class VideoThread(QThread):
    finished = pyqtSignal()

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.finished.emit()

class Installer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Anovix Installer')
        self.setWindowIcon(QIcon("anovix_logo.png"))
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QGroupBox {
                background-color: #45475a;
                border: 1px solid #313244;
                border-radius: 5px;
                margin-top: 20px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
            QCheckBox {
                background-color: #45475a;
                font: 14px Arial;
            }
            QPushButton {
                background-color: #89b4fa;
                border: 1px solid #313244;
                border-radius: 5px;
                padding: 5px 10px;
                font: bold 14px Arial;
                color: #1e1e2e;
            }
            QPushButton:hover {
                background-color: #a6e3a1;
            }
            QLabel.image-container {
                background-color: rgb(30, 30, 46);
                border-radius: 10px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        options_group = QGroupBox('Select Installation Options:')
        options_layout = QVBoxLayout()
        
        # Web Browser Option
        browser_layout = QHBoxLayout()
        self.browser_checkbox = QCheckBox('Anovix Browser')
        browser_font = QFont('Arial', 24, QFont.Weight.Bold)
        self.browser_checkbox.setFont(browser_font)
        browser_layout.addWidget(self.browser_checkbox)
        browser_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
        browser_image_label = QLabel()
        browser_image_label.setPixmap(QPixmap('browser.png').scaledToWidth(80))
        
        browser_image_container = QLabel()
        browser_image_container.setObjectName("image-container")
        container_layout = QVBoxLayout()
        container_layout.addWidget(browser_image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        browser_image_container.setLayout(container_layout)

        browser_layout.addWidget(browser_image_container)
        options_layout.addLayout(browser_layout)

        # Learning App Option
        learning_layout = QHBoxLayout()
        self.learning_checkbox = QCheckBox('Piece by Piece App')
        self.learning_checkbox.setFont(browser_font)
        learning_layout.addWidget(self.learning_checkbox)
        learning_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
        learning_image_label = QLabel()
        learning_image_label.setPixmap(QPixmap('piece.png').scaledToWidth(80))

        learning_image_container = QLabel()
        learning_image_container.setObjectName("image-container")
        container_layout = QVBoxLayout()
        container_layout.addWidget(learning_image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        learning_image_container.setLayout(container_layout)

        learning_layout.addWidget(learning_image_container)
        options_layout.addLayout(learning_layout)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Install Button
        install_button = QPushButton('Install')
        install_button.clicked.connect(self.install)
        layout.addWidget(install_button)

        self.setLayout(layout)

    def download_file(self, url, local_filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    def run_msi(self, file_path):
        subprocess.run(['msiexec', '/i', file_path])

    def install(self):
        if self.browser_checkbox.isChecked():
            browser_url = 'https://github.com/ComputerWiz541/Anovix-Browser/releases/download/v1/Setup.-.Anovix.Browser.msi'
            browser_file = 'Anovix_Browser.msi'
            print("Downloading Anovix Browser...")
            self.download_file(browser_url, browser_file)
            print("Download complete. Running the installer...")
            self.run_msi(browser_file)
            print("Installation complete.")

        if self.learning_checkbox.isChecked():
            learning_url = 'https://github.com/ComputerWiz541/piece-app/releases/download/v1/Setup.-.Piece.by.Piece.msi'
            learning_file = 'Piece_by_Piece.msi'
            print("Downloading Piece by Piece App...")
            self.download_file(learning_url, learning_file)
            print("Download complete. Running the installer...")
            self.run_msi(learning_file)
            print("Installation complete.")

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Anovix Installer')
        self.setWindowIcon(QIcon("anovix_logo.png"))
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QLabel#green-text {
                color: #a6e3a1;
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel('Welcome to the Anovix Installer')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label.setObjectName("green-text")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # Timer to switch to the installer after a delay
        self.timer = QTimer()
        self.timer.timeout.connect(self.showInstaller)
        self.timer.setSingleShot(True)
        self.timer.start(3000)  # 3 seconds delay

    def showInstaller(self):
        self.installer = Installer()
        self.installer.show()
        self.close()

class NoInternetScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Anovix Installer')
        self.setWindowIcon(QIcon("anovix_logo.png"))
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QLabel#red-text {
                color: #f38ba8;
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel('Please Connect to the Internet')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label.setObjectName("red-text")
        layout.addWidget(self.label)
        self.setLayout(layout)

def check_internet_connection():
    try:
        response = requests.get('http://www.google.com', timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if check_internet_connection():
        welcome_screen = WelcomeScreen()
        welcome_screen.show()
    else:
        no_internet_screen = NoInternetScreen()
        no_internet_screen.show()
    sys.exit(app.exec())
