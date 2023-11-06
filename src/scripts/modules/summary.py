import os
import pandas as pd
from datetime import datetime
from pprint import pprint as pp

BIKE_IN = 0;   BIKE_OUT = 0
BUS_IN = 0;    BUS_OUT = 0
CAR_IN = 0;    CAR_OUT = 0
EBIKE_IN = 0;  EBIKE_OUT = 0
JEEP_IN = 0;   JEEP_OUT = 0
MOTOR_IN = 0;  MOTOR_OUT = 0
TRIKE_IN = 0;  TRIKE_OUT = 0
TRUCK_IN = 0;  TRUCK_OUT = 0
VAN_IN = 0;    VAN_OUT = 0

FILE_PATH = os.getcwd() + "/src/tmp/"
class Summary():

    def __init__(self) -> None:
        pass

    def count_vehicle(self, tracker_data: list) -> dict:
        if tracker_data is not None:
            vehicle_type, direction = tracker_data

            if vehicle_type == "Bicycle":
                if direction == "in":
                    global BIKE_IN
                    BIKE_IN += 1
                else:
                    global BIKE_OUT
                    BIKE_OUT += 1
            if vehicle_type == "Bus":
                if direction == "in":
                    global BUS_IN
                    BUS_IN += 1
                else:
                    global BUS_OUT
                    BUS_OUT += 1
            if vehicle_type == "Car":
                if direction == "in":
                    global CAR_IN
                    CAR_IN += 1
                else:
                    global CAR_OUT
                    CAR_OUT += 1
            if vehicle_type == "E-Bike":
                if direction == "in":
                    global EBIKE_IN
                    EBIKE_IN += 1
                else:
                    global EBIKE_OUT
                    EBIKE_OUT += 1
            if vehicle_type == "Jeepney":
                if direction == "in":
                    global JEEP_IN
                    JEEP_IN += 1
                else:
                    global JEEP_OUT
                    JEEP_OUT += 1
            if vehicle_type == "Motorcycle":
                if direction == "in":
                    global MOTOR_IN
                    MOTOR_IN += 1
                else:
                    global MOTOR_OUT
                    MOTOR_OUT += 1
            if vehicle_type == "Tricycle":
                if direction == "in":
                    global TRIKE_IN
                    TRIKE_IN += 1
                else:
                    global TRIKE_OUT
                    TRIKE_OUT += 1
            if vehicle_type == "Truck":
                if direction == "in":
                    global TRUCK_IN
                    TRUCK_IN += 1
                else:
                    global TRUCK_OUT
                    TRUCK_OUT += 1
            if vehicle_type == "Van":
                if direction == "in":
                    global VAN_IN
                    VAN_IN += 1
                else:
                    global VAN_OUT
                    VAN_OUT += 1
            
        intotal = BIKE_IN + BUS_IN + CAR_IN + EBIKE_IN + JEEP_IN + MOTOR_IN + TRIKE_IN + TRUCK_IN + VAN_IN
        outtotal = BIKE_OUT + BUS_OUT + CAR_OUT + EBIKE_OUT + JEEP_OUT + MOTOR_OUT + TRUCK_OUT + TRIKE_OUT + VAN_OUT 
        overalltotal =  BIKE_IN + BIKE_OUT + BUS_IN + BUS_OUT + CAR_IN + CAR_OUT + EBIKE_IN + EBIKE_OUT + JEEP_IN + JEEP_OUT + MOTOR_IN + MOTOR_OUT + TRIKE_IN + TRIKE_OUT +  TRUCK_IN + TRUCK_OUT +  VAN_IN + VAN_OUT

        summary = {
            "Bicycle": {"In": BIKE_IN, "Out": BIKE_OUT, "Total": BIKE_IN + BIKE_OUT},
            "Bus": {"In": BUS_IN, "Out": BUS_OUT, "Total": BUS_IN + BUS_OUT},
            "Car": {"In": CAR_IN, "Out": CAR_OUT, "Total": CAR_IN + CAR_OUT},
            "E-Bike": {"In": EBIKE_IN, "Out": EBIKE_OUT, "Total": EBIKE_IN + EBIKE_OUT},
            "Jeepney": {"In": JEEP_IN, "Out": JEEP_OUT, "Total": JEEP_IN + JEEP_OUT},                        
            "Motorcycle": {"In": MOTOR_IN, "Out": MOTOR_OUT, "Total": MOTOR_IN + MOTOR_OUT},            
            "Tricycle": {"In": TRIKE_IN, "Out": TRIKE_OUT, "Total": TRIKE_IN + TRIKE_OUT},            
            "Truck": {"In": TRUCK_IN, "Out": TRUCK_OUT, "Total": TRUCK_IN + TRUCK_OUT},            
            "Van": {"In": VAN_IN, "Out": VAN_OUT, "Total": VAN_IN + VAN_OUT}, 
            "Total Count": {"In": intotal, "Out": outtotal, "Total": overalltotal}           
        }
        return summary
    
    def save_to_csv(self, start_time, summary: dict) -> str:
        current_datetime = datetime.now()
        format_curtime = current_datetime.strftime('%m-%d-%y_%H-%M-%S')  # Use underscores instead of spaces and colons
        path = FILE_PATH + "summary-{}.csv".format(format_curtime)
        df = pd.DataFrame.from_dict(data=summary, orient='index')
        df.to_csv(path)
        return path