# AccelApproximer

This is a simple desktop application that estimates the acceleration of a car based on certain parameters such as engine power, car weight, and gear ratio. The application also comes with a graphical user interface (GUI) that makes it easy to use and navigate.
Installation

To use this application, you need to have Python 3.6 or higher installed on your computer. You need to have kivy, kivymd, matplotlib, and the kivygarden matplotlib flower.

Usage

You can use the application with a simpler Tkinter interface which was used for prototyping or a KivyMd interface

Once the application is running, you can enter the values for the different parameters using the sliders provided on the GUI. The application will then estimate the acceleration of the car based on these parameters and display the result in the output box.

Features
The program takes into account
  - starting from a stand still; how agressive the drive start moving
  - finding the optimum upshift point
  - this program simulates only in static friction, therefore if a car breaks traction when accelerating, the program will not simulate that since accurate data about suspension design and tire is needed, which is close to imposible to obtain, instead it limits the maximum possible acceleration to the maximum force pushing on the tire times the friction coefficient
Parameters

The following parameters are used to estimate the acceleration of the car:

    Engine Torque (Nm)
    Car weight (kg)
    Car mass distribution
    Gear ratios
    Final drive ratio
    Idle and Redline RPM
    Wheel diameter (in inches)
    Tire width (in millimeters)
    Tire aspect ratio
    Tire Rolling and Friction Coefficient
    Drag Coefficient
    Frontal Area
    Air density
    Initial and Final Speed (kmh)
    Optional Downforce and weight shifting calculations
    

Output

The application estimates the acceleration of the car in kilometers per hour(kmh). The output is displayed in the output box on the GUI.
Contributing

If you find any issues with this application or would like to contribute to its development, please feel free to submit a pull request or create an issue
