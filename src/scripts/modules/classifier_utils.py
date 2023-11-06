import os
import configparser

from typing import Tuple, List
from ultralytics import YOLO
from supervision.draw.color import ColorPalette
from supervision.geometry.dataclasses import Point
from supervision.tools.detections import BoxAnnotator
from yolox.tracker.byte_tracker import BYTETracker

from modules.tracking_utils import TrackingUtils
from modules.bytetracker_args import BYTETrackerArgs
from modules.line_counter import LineCounter, LineCounterAnnotator

config = configparser.ConfigParser()
config.read(os.getcwd() + "/src/config.cfg")
MODEL_NAME = config['MODEL']['name']

LINE_START = Point(0, 400)
LINE_END = Point(1920, 400)
MODEL_PATH = os.getcwd() + "/src/resources/models/best.pt" #.format(MODEL_NAME)

class ClassifierUtils():

    def __init__(self) -> None:
        pass
    
    def get_vehicle_classifier_model(self) -> Tuple[YOLO, List[str], List[str]]:
        model = YOLO(MODEL_PATH)
        model.fuse
        classes = model.model.names
        vehicle_types = [classes[i] for i in range(0, len(classes))]
        return model, classes, vehicle_types

    def get_tracker_tools(self) -> Tuple[BYTETracker, LineCounter, BoxAnnotator, LineCounterAnnotator, TrackingUtils]:
        byte_tracker = BYTETracker(BYTETrackerArgs())
        line_counter = LineCounter(start=LINE_START, end=LINE_END)
        box_annotator = BoxAnnotator(color=ColorPalette(), thickness=4, text_thickness=4, text_scale=1)
        line_annotator = LineCounterAnnotator(thickness=4, text_thickness=4, text_scale=2)
        tracker = TrackingUtils()
        return byte_tracker, line_counter, box_annotator, line_annotator, tracker

