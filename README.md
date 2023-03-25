# AccelApproximer

AccelApproximer is a powerful and user-friendly desktop application that accurately estimates the acceleration of a car based on various parameters such as engine power, car weight, and gear ratio. The application also features a sophisticated graphical user interface (GUI) that makes it easy to use and navigate.

# Installation

To use AccelApproximer, you must have Python 3.6 or higher installed on your computer, along with the following libraries: kivy, kivymd, matplotlib, and the kivygarden matplotlib flower.

# Usage

AccelApproximer comes with two interfaces - a simpler Tkinter interface that was used for prototyping, and a KivyMd interface that offers a more polished user experience. Once the application is running, you can enter the values for different parameters using the sliders provided on the GUI. The application will then estimate the acceleration of the car based on these parameters and display the result in the output box.

# Features

AccelApproximer offers a range of advanced features that enable it to simulate various real-world scenarios. These features include:

    Starting from a standstill: simulates how aggressive the car moves when starting from a stationary position.
    Optimum upshift point: finds the best time to shift gears to maximize acceleration.
    Static friction simulation: the program limits the maximum possible acceleration to the maximum force pushing on the tire times the friction coefficient since accurate data about suspension design and tire is hard to obtain.
    Other optional features: downforce and weight shifting calculations.

# Parameters

AccelApproximer uses the following parameters to estimate the acceleration of a car:

    Engine torque (Nm)
    Car weight (kg)
    Car mass distribution
    Gear ratios
    Final drive ratio
    Idle and redline RPM
    Wheel diameter (in inches)
    Tire width (in millimeters)
    Tire aspect ratio
    Tire rolling and friction coefficient
    Drag coefficient
    Frontal area
    Air density
    Initial and final speed (kmh)

# Output

AccelApproximer estimates the acceleration of the car in kilometers per hour (kmh) and displays the result in the output box on the GUI, as well as specific graphs such as
engine torque and horsepower, acceleration, air resistance, downforce, torque, torque (no opposing forces, such as: drag), gear speeds.

# Contributing

If you encounter any issues while using AccelApproximer or would like to contribute to its development, please feel free to submit a pull request or create an issue.

# Photo Showcase

Here are some photos of the app when it simulates a 2016 mazda miata nd's time from 0-100 km/h.
![python_d57drbX4Zg](https://user-images.githubusercontent.com/99805998/227724960-dc2ecae9-b04a-40d9-bb93-03686a587d5e.png)
![python_SbiWhqGGJ9](https://user-images.githubusercontent.com/99805998/227724966-9f2da7dd-66d4-4083-88cd-6e5519841a33.png)
![python_85BQllGA7y](https://user-images.githubusercontent.com/99805998/227724967-3b32b690-97ec-44d2-b121-c6e166105384.png)
![python_U8eOl4QEu0](https://user-images.githubusercontent.com/99805998/227725193-e5aa0fc5-9320-4e77-9e79-5dbfd6dcafcd.png)
