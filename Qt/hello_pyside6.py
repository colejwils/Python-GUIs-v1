# pip install PySide6
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hello PySide6")

        layout = QVBoxLayout()

        self.label = QLabel("Hello, World!")
        button = QPushButton("Click me!")

        # Connect the button's clicked signal to our method
        button.clicked.connect(self.on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText("Button Pressed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
