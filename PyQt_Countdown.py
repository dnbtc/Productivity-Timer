# A simple GUI productivity timer in Python using PyQt

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QDialog, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont

class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize the main timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)

        # Initialize the default time
        self.resetTime()

        # Set up the main user interface components
        self.label = QLabel(self.time_left.toString("mm:ss.zzz"), self)
        self.label.setFont(QFont("Arial", 60))
        self.label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.startTimer)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stopTimer)

        self.set_time_button = QPushButton('Set Time', self)
        self.set_time_button.clicked.connect(self.setTimeDialog)

        # Add a reset button
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.resetTimer)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.set_time_button)
        layout.addWidget(self.reset_button)  # Add the reset button to the layout

        # Set the initial window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('TC Timer')
        self.label.setText("00:00.00")

    def resetTime(self):
        # Reset the time to 10 minutes
        self.time_left = QTime(0, 10, 0, 0)

    def startTimer(self):
        # Start the timer with a 10-millisecond interval
        self.timer.start(10)

    def stopTimer(self):
        # Stop the timer
        self.timer.stop()

    def updateTime(self):
        # Update the displayed time on each timer tick
        if self.time_left > QTime(0, 0, 0, 0):
            self.time_left = self.time_left.addMSecs(-10)
            self.label.setText(self.time_left.toString("mm:ss.zzz")[0:8])
        else:
            # Stop the timer when it reaches zero and reset to 10 minutes
            self.timer.stop()
            self.label.setText("00:00.00")
            self.resetTime()

    def setTimeDialog(self):
        # Create a dialog to set the countdown time
        dialog = QDialog(self)
        dialog.setWindowTitle('Set Time')

        # Create a time input widget
        time_edit = QTimeEdit(dialog)
        time_edit.setDisplayFormat("mm:ss")
        time_edit.setTime(self.time_left)

        # Create OK and Cancel buttons
        ok_button = QPushButton('OK', dialog)
        ok_button.clicked.connect(lambda: self.setTime(time_edit.time(), dialog))

        cancel_button = QPushButton('Cancel', dialog)
        cancel_button.clicked.connect(dialog.reject)

        # Set up the layout for the dialog
        layout = QHBoxLayout(dialog)
        layout.addWidget(time_edit)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        # Show the dialog
        dialog.exec_()

    def setTime(self, new_time, dialog):
        # Set the new countdown time and update the display
        self.time_left = new_time
        self.label.setText(self.time_left.toString("mm:ss.zzz")[0:8])
        dialog.accept()

    def resetTimer(self):
        # Reset the timer to its initial state
        self.stopTimer()
        self.resetTime()
        self.label.setText(self.time_left.toString("mm:ss.zzz")[0:8])

if __name__ == '__main__':
    # Start the application
    app = QApplication(sys.argv)
    timer = CountdownTimer()
    timer.show()
    sys.exit(app.exec_())
