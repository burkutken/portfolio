---
title: Quadruped Robot Design
short_title: Quadruped Robot
slug: quadruped-robot
summary: A quadruped robot concept combining mechanical design, sensors and control.
subtitle: Design of Quadruped Robot for serviced to search in abandoned building
discipline: Robotics
tags: [Mechatronics]
methods:
- CAD
- Control
- Prototyping
tools:
- SolidWorks CAD
- Fusion 360
- ANSYS Structural
- Finite Element Analysis
- Arduino
role: Mechanical design and control
period: May 2025
status: completed
cover: images/quadruped robot/robodog_assem_2.png
cover_alt: Quadruped Robot
order: 4
featured: false
draft: false
legacy: page2.html
---

## Project Overview

This project focuses on the design and analysis of quadruped robot which capable of autonomous movement for tracking inhuman environments such as abandoned buildings. The robot is engineered using carbon fiber composite materials with the effective manufacturing via vacuum bagging for strength and lightweight performance. It includes MG996R servo motors, advanced sensors such as (IMU, ultrasonic, force etc.) and a microSD-based data logging system. PID control ensures balance, torque management and terrain adaptability. Stress, deformation analysis were conducted using Solidworks and kinematic analysis were conducted using Matlab to verify mechanical and theoretical integrity. The robot adheres to ISO standards and meets budget and operational constraints.

## Challenge

The primary challenge was designing a low-cost, agile quadruped robot for search-and-rescue operations in indoor environments (e.g., collapsed buildings). Existing solutions prioritized expensive components or lacked modularity, limiting scalability. Key hurdles included:

- Balancing high torque for stability with low power consumption

- Achieving accurate terrain detection/mapping with low-cost sensors

- Enabling autonomous navigation within strict size (400×400×400 mm) and budget constraints ($1,000)

- Operating in temperatures from -10°C to 40°C with 1-hour battery life

## Solution

Quadruped robot with optimized mechatronic systems:

- Carbon fiber composites (manufactured via vacuum bagging) for high strength-to-weight ratio.

- Cost-effective Tower Pro MG996R servos (selected via Pugh matrix analysis) for joint movement.

- IMU, force sensors, and ultrasonic sensors for real-time terrain feedback

- Arduino-based PID control for balance, torque management, and adaptability

- 12×Sony VTC6 Li-ion batteries (2s6p) for 1-hour runtime.

- MicroSD data logging and kinematic algorithms (MATLAB) for path planning.

- ISO 12100 (safety), ISO 18243 (batteries), and ISO 2768 (tolerances).

## Engineering Process

After designing the quadruped body, which can be seen below

![Quadruped Robot Design](<images/quadruped robot/robodog_assem_2.png> "Quadruped Robot Design")

Light-weight and durable material was needed. So the best option out there was carbon fiber reinforced polymer (CRFP). Even the body of the quadruped robot is CFRP, it weights and loads on the servo's pins and from force, torque calculation was required and after calculations MG996R servo is selected. So, in ANSYS, static structural is used stress loads on servo pins and the result is as shown

![Servo Pin Stress Analysis](<images/quadruped robot/servo_pin_stress.png> "Servo Pin Stress Analysis")

In the Controller side, I used Arduino Mega as controller and several sensors such as imu for maintaining the robot's stability and ultrasonic sensor for obsticle detection etc. All arduino wiring was done as

![Arduino Wiring](<images/quadruped robot/arduion_wiring2.png> "Arduino Wiring")

## Results

The Quadruped Robot was able to:

- Search in abandoned places

- Map the places and save it on SD Card the is inserted

- Obsticle detection and avoiding to hit them

- Fully automation and long battery life

## Project timeline

| Stage | Period |
| --- | --- |
| Research | Feb 2025 |
| Design | Feb 2025 - March 2025 |
| Simulating | March 2025 - April 2025 |
| Finalizing | May 2025 |
| Presentation | 19 May 2025 |

## Project gallery

![Body Exploded View](<images/quadruped robot/body_assembly_page-0001.png> "Body Exploded View")

![Quadruped Robot Exploded View](<images/quadruped robot/leg_assembly_page-0001.png> "Quadruped Robot Exploded View")

![Leg Exploded View](<images/quadruped robot/leg_page-0001.png> "Leg Exploded View")

![Gripper System](<images/quadruped robot/fbd_leg.png> "Gripper System")
