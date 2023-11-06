import os
import cv2
import numpy as np
import logging
import time
import sys
import configparser
from threading import Thread
from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from modules.classifier_utils import ClassifierUtils
from modules.summary import Summary
from supervision.tools.detections import Detections

from itertools import count
import webbrowser

config = configparser.ConfigParser()
config.read(os.getcwd() + "/src/config.cfg")

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler())

SOURCE = os.getcwd() + "/src/resources/videos/{}".format(config['SOURCE']['video_name'])
# SOURCE = config['SOURCE']['camera_index']

class UI(QMainWindow):
    
    def __init__(self)-> None:
        super().__init__()
        self.initialize_ui()
        # --start-- #     
    def initialize_ui(self):
        self.setWindowTitle("Vehicle Classifier & Counter")
        #self.resize(1200, 800)
        self.setFixedSize(1200, 800)
        self.move_to_center()

        background_image = QLabel(self)
        pixmap = QPixmap(r"C:\Users\Raymond\Documents\VehicleCountandClassificationSystem\src\resources\BGNOLOGO.png")  # Replace with desred bg
        background_image.setPixmap(pixmap)
        background_image.setGeometry(0, 0, pixmap.width(), pixmap.height())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        left_widget = self.create_left_pane()
        right_widget = self.create_right_pane()



        # Create splitter that separates the left and right pane.
        splitter = QSplitter()
        splitter.setHandleWidth(0)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Assemble layouts.
        main_layout = QHBoxLayout()
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Declare worker thread.
        self.worker1 = Worker1(self)
        self.worker1.finished.connect(self.close)
        self.worker1.frame_update.connect(self.setImage)

        # Table update.
        self.worker1.table_update.connect(self.populate_table)

    def move_to_center(self) -> None:
        screens = QApplication.instance().screens()
        for screen in screens:
            geometry = screen.geometry()

        window_size = self.geometry()
        x = (geometry.width() - window_size.width())/2
        y = (geometry.height() - window_size.height())/2
        self.move(x, y)

    def create_left_pane(self):
        # For left pane.
        self.img_label = QLabel(self)
        self.img_label.setText("PRESS START BUTTON")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setFixedSize(800,800)
        self.img_label.setStyleSheet("font-size: 60px; color: white;")
        img_layout = QVBoxLayout()
        img_layout.addWidget(self.img_label)

        left_widget = QWidget()
        left_widget.setLayout(img_layout)

        return left_widget
    
    def create_right_pane(self):
        right_pane = QVBoxLayout()
        adjustor = QLabel(self)
        adjustor.setFixedHeight(200)

        self.status_label = QLabel(self)
        self.status_label.setText("STATUS")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label_font = QFont()
        status_label_font.setPointSize(20)
        self.status_label.setFont(status_label_font)
        self.status_label.setStyleSheet("border: 2px solid; background-color: white; font-weight:bold;")
        self.status_label.setFixedSize(420, 50)

        # Create buttons.
        button_font = QFont()
        button_font.setPointSize(14)
        button_font1 = QFont("Arial", 12)

        self.start_button = QPushButton("START")
        self.start_button.setFont(button_font)
        self.stop_button = QPushButton("STOP")
        self.stop_button.setFont(button_font)
        self.stop_button.setEnabled(False)

        self.magneto_button1 = QPushButton("View HMC883L1")  
        self.magneto_button1.setFont(button_font1)
        self.magneto2_button2 = QPushButton("View HMC883L2")  
        self.magneto2_button2.setFont(button_font1)

        # Style for buttons 
        button_style = """
            QPushButton {
                background-color: #6699FF;
                color: white;
                border: none;
                padding: 7.5px 12px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: white;
                color: #6699FF;
                border: 2px solid #6699FF;
            }
            QPushButton:pressed {
                background-color: #CC00FF;
                color: white;
            }
        """

        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: green;  
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: white;
                color: green;  
                border: 2px solid green;
            }
            QPushButton:pressed {
                background-color: blue;
                color: white;
            }
        """)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: red;  
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: white;
                color: red;
                border: 2px solid red;
            }
            QPushButton:pressed {
                background-color: orange;
                color: white;
            }
        """)
        self.magneto_button1.setStyleSheet(button_style)
        self.magneto2_button2.setStyleSheet(button_style)

        # Connect buttons to functions.
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.magneto_button1.clicked.connect(self.magneto1_web) 
        self.magneto2_button2.clicked.connect(self.magneto2_web)  

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        table_counter = self.create_table()

        additional_buttons_layout = QHBoxLayout()
        additional_buttons_layout.addWidget(self.magneto_button1)
        additional_buttons_layout.addWidget(self.magneto2_button2)

        # Add widgets to the right pane.
        right_pane.addWidget(adjustor)
        right_pane.addWidget(self.status_label)
        right_pane.addLayout(button_layout)
        right_pane.addWidget(table_counter)
        right_pane.addLayout(additional_buttons_layout)

        right_widget = QWidget()
        right_widget.setLayout(right_pane)

        return right_widget



    def create_table(self):
        # Create table.
        self.table_counter = QTableWidget(self)
        self.table_counter.setStyleSheet('''
        QTableWidget {
            background-color: #f0f0f0;
            border: 2px solid #ddd;
        }
        QTableWidget QHeaderView::section {
            background-color: #666;
            color: white;
            font-weight: bold;
        }
        QTableWidget::item {
            padding: 2px;
        }
    ''')
        self.table_counter.setRowCount(9)
        self.table_counter.setColumnCount(3)

        # Table headers.
        columns = ["IN", "OUT", "TOTAL"]
        rows = ["Bike", "Bus", "Car", "E-Bike", "Jeep", "Motorcycle", "Tricycle", "Truck", "Van"]
        self.table_counter.setHorizontalHeaderLabels(columns)
        self.table_counter.setVerticalHeaderLabels(rows)
        self.table_counter.setFixedSize(420,300)
        table_counter_font = QFont()
        table_counter_font.setPixelSize(15)
        self.table_counter.setFont(table_counter_font)
        self.table_counter.setEditTriggers(QTableWidget.NoEditTriggers)

        header = self.table_counter.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)

        return self.table_counter

    @Slot(QImage)
    def setImage(self, image):
        self.img_label.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def start(self):
        self.stop_button.setEnabled(True)
        self.status_label.setText("Detection in progress...")
        self.worker1.start()

    @Slot()
    def stop(self):
        self.status_label.setText("Detection stopped.")
        time.sleep(3)
        self.worker1.status = False
        self.worker1.quit()
        self.worker1.save_to_csv()
        self.worker1.cap.release()

    @Slot()
    def magneto1_web(self):
        webbrowser.open('192.168.87.119')#=======================================================
    @Slot()
    def magneto2_web(self):
        webbrowser.open('192.168.87.165')

    @Slot(list)
    def populate_table(self, data):
        for row, row_data in enumerate(data):
            for  col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_counter.setItem(row, col, item)

class CustomThread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None) -> None:
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return
    
class Worker1(QThread):
    frame_update = Signal(QImage)
    table_update = Signal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.class_ids = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        self.summary = ""
        self.start_time = ""
        self.cap = True
        self.model, self.classes, _ = ClassifierUtils().get_vehicle_classifier_model()
        self.byte_tracker, self.line_counter, self.box_annotator, self.line_annotator, self.tracker = ClassifierUtils().get_tracker_tools()

    def detect_objects(self, frame):
        
        results = self.model(frame)[0] # yolov8
        xyxy = results.boxes.xyxy.cpu().numpy()
        conf = results.boxes.conf.cpu().numpy()
        class_id = results.boxes.cls.cpu().numpy().astype(int)

        detections = Detections(
            xyxy = xyxy,
            confidence = conf,
            class_id = class_id
        )

        mask = np.array([class_id in self.class_ids for class_id in detections.class_id], dtype=bool)
        detections.filter(mask=mask, inplace=True)

        mask = np.array([conf>=0.40 for conf in detections.confidence], dtype=bool)
        detections.filter(mask=mask, inplace=True)

        tracks = self.byte_tracker.update(
            output_results=self.tracker.detections2boxes(detections=detections),
            img_info=frame.shape,
            img_size=frame.shape
        )

        tracker_id = self.tracker.match_detections_with_tracks(detections=detections, tracks=tracks)
        detections.tracker_id = np.array(tracker_id)

        mask = np.array([tracker_id is not None for tracker_id in detections.tracker_id], dtype=bool)
        detections.filter(mask=mask, inplace=True)

        labels = [
            f"{self.classes[class_id]}-{confidence:0.2f}" 
            for _, confidence, class_id, _ in detections 
        ]

        frame = self.box_annotator.annotate(frame=frame, detections=detections, labels=labels)
        self.line_annotator.annotate(frame=frame, line_counter=self.line_counter)

        # Process count data.
        tracker_data = self.line_counter.update(class_names=self.classes, detections=detections)
        summary = Summary().count_vehicle(tracker_data=tracker_data)
        self.summary = summary

        return frame, summary

    def parse_data(self, summary) -> list:
        data_list = []
        for i in summary:
            value = (summary[i]['In'], summary[i]['Out'], summary[i]['Total']) 
            data_list.append(value)
        return data_list
    
    def save_to_csv(self) -> None:
        path = Summary().save_to_csv(self.start_time, self.summary)
        LOGGER.info("CSV file saved to {}".format(path))

    def run(self):
        self.status = True
        self.cap = cv2.VideoCapture(2)
        self.start_time = datetime.today().strftime("%H%M") # Get start time.
        while self.isRunning():
            ret, frame = self.cap.read()
            if ret:
                object_detection_thread = CustomThread(target=self.detect_objects, args=(frame,))
                object_detection_thread.start()
                processed_frame, summary = object_detection_thread.join()

                # Process frame.
                color_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = color_frame.shape
                img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
                scaled_img = img.scaled(1000, 800)

                # Emit signal.
                self.table_update.emit(self.parse_data(summary))
                self.frame_update.emit(scaled_img)

            if self.status == False:
                LOGGER.info("\nExiting video...")
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    app.exec()  