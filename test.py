from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QVBoxLayout
import sys

def reassign_button_click(button: QPushButton, new_action):
    """
    Disconnects the current clicked action of the button and reconnects a new one.

    :param button: QPushButton instance to reassign the click action.
    :param new_action: Callable to be connected to the button's clicked signal.
    """
    try:
        # Disconnect all previous connections to the clicked signal
        button.clicked.disconnect()
    except TypeError:
        # This will be raised if there were no connections before
        pass
    
    # Connect the new action
    button.clicked.connect(new_action)

def example_action():
    print("Button clicked and new action executed!")

class ExampleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Button Reassign Example")

        self.button = QPushButton("Click Me", self)
        # self.button.clicked.connect(self.original_action)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def original_action(self):
        print("Original action executed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ExampleWindow()
    window.show()

    # Reassign the button click action to example_action
    reassign_button_click(window.button, example_action)

    sys.exit(app.exec())
