
# THESIS: Vehicle Classification and Counting System

## Abstract
In the era of smart transportation and traffic management, the need for efficient and accurate vehicle classification and counting systems has become increasingly significant. Previous vehicle classification systems face several challenges. The two main problems encountered by vehicle classification systems. Vehicle blockage, which blocks views of vehicles behind another vehicle, and the fast-moving vehicles, which cause blurred image captures.
The design and development of vehicle classification and counting systems utilizing high definition camera and magnetometer sensors employs advanced computer vision techniques enabling real-time recognition and classification of vehicles. Moreover, magnetometer sensors were employed to detect and track the presence of vehicles in motion. The combination of these technologies allows for precise classification and counting of vehicles, distinguishing between common vehicles in the Philippines such as cars, bicycles, e-bikes, jeepneys, trucks, tricycles, vans, motorcycles, and buses. After a series of experiments using the HMC5883L Magnetometer Sensor, the researcher’s failed to improve the output of the sensor. However, the camera gained a good accuracy using image processing. The dataset was trained using three deep learning algorithms which are YOLOv5, YOLOv7, and YOLOv8. The YOLOv8 was considered as the project’s model with an accuracy of 94.5%. In actual deployment for one-minute intervals, the system consistently achieved classification accuracy ranging from 71% to 100% and counting accuracy of 90.245%.
This study highlights the modularity, scalability, and adaptability, making it suitable for various traffic monitoring applications. This system promises enhanced accuracy in vehicle classification and counting, reduced human intervention, and the potential for real-time traffic analysis


## Authors
-Raymond Cancilao

-Kenneth Toledo: [kenneth.toledo.520](https://www.facebook.com/kenneth.toledo.520)

-Kent Ursolino:
[@Rafiel31](https://github.com/krafiel31)

-Jazley Manguino: 
[Github account](https://www.facebook.com/kenneth.toledo.520)

-_also Leo Magpantay for guiding and helping us_ [@ldmagpantay](https://github.com/ldmagpantay)

---
## Testing and Result

##### __Sample Testing__
![day](https://raw.githubusercontent.com/Chocobot02/Thesis/63067ba386cd0cbe4d774851f9f585220d632851/Screenshot%202023-11-06%20164554.png)
![noght](https://raw.githubusercontent.com/Chocobot02/Thesis/63067ba386cd0cbe4d774851f9f585220d632851/Screenshot%202023-11-06%20164609.png)

##### __Result of Video Inference__
| Object Detection Algorithm | mAP@0.5 conf | mAP@0.7 conf|
| ------- | ------- | -------- |
| YOLOv5 |92.3% |89.7% |
| YOLOv7 |78.54%|53.63% |
| YOLOv8 |94.53%|93.24% |


---
> NOTE: The required dependencies that must be installed in the local or virtual environment are listed in 'requirements.txt'. ByteTrack is also  need to be installed.[Link](https://github.com/ifzhang/ByteTrack)
