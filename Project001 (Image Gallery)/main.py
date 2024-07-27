import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QAction, QFileDialog, QMenuBar, QMenu, QSystemTrayIcon, QStyle, QSlider
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QDir

class GalleryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Gallery")
        self.setGeometry(100, 100, 800, 600)
        
        self.images = []
        self.current_index = -1
        self.is_paused = True
        self.timer_interval = 3000  # Default 3 seconds
        
        self.initUI()
        self.setupErrorHandling()
        self.loadImages()

    def initUI(self):
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Image label
        self.image_label = QLabel("No Images Loaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        # Controls
        self.control_layout = QVBoxLayout()
        self.layout.addLayout(self.control_layout)
        
        self.previous_button = QPushButton("Previous", self)
        self.previous_button.clicked.connect(self.showPreviousImage)
        self.control_layout.addWidget(self.previous_button)
        
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.showNextImage)
        self.control_layout.addWidget(self.next_button)
        
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.togglePause)
        self.control_layout.addWidget(self.pause_button)
        
        self.interval_dropdown = QComboBox(self)
        self.interval_dropdown.addItems(["1", "2", "3", "5", "10"])
        self.interval_dropdown.setCurrentIndex(2)  # Default 3 seconds
        self.interval_dropdown.currentIndexChanged.connect(self.changeInterval)
        self.control_layout.addWidget(self.interval_dropdown)
        
        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showNextImage)
        
        # Menu
        self.initMenu()

    def initMenu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.openFolder)
        file_menu.addAction(open_folder_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        file_menu.addAction(about_action)
        
        donate_action = QAction("Donate", self)
        donate_action.triggered.connect(self.openDonatePage)
        file_menu.addAction(donate_action)
        
    def openFolder(self):
        try:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Image Folder")
            if folder_path:
                self.loadImages(folder_path)
        except Exception as e:
            self.showError("Failed to open folder: " + str(e))

    def loadImages(self, folder_path=None):
        try:
            if folder_path is None:
                folder_path = QDir.currentPath()
                
            self.images = []
            image_formats = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"]
            for format in image_formats:
                self.images.extend(QDir(folder_path).entryList([format], QDir.Files))
                
            self.images = [os.path.join(folder_path, image) for image in self.images]
            self.current_index = -1 if not self.images else 0
            if self.images:
                self.showImage()
            else:
                self.image_label.setText("No Images Found")
        except Exception as e:
            self.showError("Failed to load images: " + str(e))

    def showImage(self):
        try:
            if not self.images:
                return
            
            pixmap = QPixmap(self.images[self.current_index])
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        except Exception as e:
            self.showError("Failed to show image: " + str(e))

    def showNextImage(self):
        try:
            if not self.images:
                return
            
            self.current_index = (self.current_index + 1) % len(self.images)
            self.showImage()
        except Exception as e:
            self.showError("Failed to show next image: " + str(e))

    def showPreviousImage(self):
        try:
            if not self.images:
                return
            
            self.current_index = (self.current_index - 1 + len(self.images)) % len(self.images)
            self.showImage()
        except Exception as e:
            self.showError("Failed to show previous image: " + str(e))

    def togglePause(self):
        try:
            if self.is_paused:
                self.timer.start(self.timer_interval)
                self.pause_button.setText("Pause")
            else:
                self.timer.stop()
                self.pause_button.setText("Play")
            self.is_paused = not self.is_paused
        except Exception as e:
            self.showError("Failed to toggle pause: " + str(e))

    def changeInterval(self):
        try:
            self.timer_interval = int(self.interval_dropdown.currentText()) * 1000
            if not self.is_paused:
                self.timer.start(self.timer_interval)
        except Exception as e:
            self.showError("Failed to change interval: " + str(e))

    def showAbout(self):
        self.showMessage("About", "This is a PyQt5 Image Gallery Application.")

    def openDonatePage(self):
        try:
            import webbrowser
            webbrowser.open("https://www.tstp.xyz/donate")
        except Exception as e:
            self.showError("Failed to open donate page: " + str(e))

    def showMessage(self, title, message):
        try:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(title)
            msg_box.setText(message)
            msg_box.exec_()
        except Exception as e:
            self.showError("Failed to show message: " + str(e))

    def showError(self, error_message):
        try:
            print("Error: " + error_message)
        except Exception as e:
            print("Failed to show error: " + str(e))

    def setupErrorHandling(self):
        sys.excepthook = self.handleException

    def handleException(self, exc_type, exc_value, exc_traceback):
        try:
            self.showError(f"An unexpected error occurred: {exc_value}")
        except Exception as e:
            print("Failed to handle exception: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery_app = GalleryApp()
    gallery_app.show()
    sys.exit(app.exec_())
