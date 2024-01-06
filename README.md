# Parking Interaction System

## Introduction
The Parking Interaction System is an innovative solution combining hardware and software to enhance the interaction with public parking spaces equipped with entrance gates. Our system uses a combination of embedded Google Coral systems, cloud databases, and a user-friendly interface through a Telegram bot. The primary aim is to automate access to parking spaces using computer vision models for car-plate number recognition. For more information you can read [project report](https://drive.google.com/file/d/13EPkbvAllHFcw8iKntHJ6y3KRFjevMNH/view?usp=sharing) or [presentation](https://drive.google.com/file/d/15JpzKiO-78GykuHAe_xsVvMI4-tt5gcC/view?usp=sharing).

## Features
- **Embedded Google Coral System**: Utilizes cutting-edge technology for object detection and character recognition.
- **Cloud Database Integration**: Stores user and parking space data, facilitating information exchange.
- **Telegram Bot Interface**: Provides user registration and real-time notifications about parking space usage.
- **Hardware Integration**: Arduino circuit integration for gate control via radio signals.
- **Two Computational Approaches**: Includes a fully independent Google Coral-based system and a hybrid system with remote server processing for complex models.

## Project Scope
Our solution addresses the inefficiencies in current parking systems by providing a more flexible and efficient way to manage parking spaces. It benefits both parking owners and users by enhancing the capacity and utilization of parking spaces.

## System Architecture
- **Google Coral Dev Board**: Acts as the core computational unit, running machine learning models for character recognition.
- **Cloud Database**: Central repository for storing and managing data about users and parking spaces.
- **Arduino Circuit**: Interfaces with parking gates to control access based on recognized car-plate numbers.
- **Telegram Bot**: Serves as the user interface for registration and notifications.
![Example Image](https://github.com/stequoy/Parking-Interaction-System/blob/main/images/intergration%20approach.png)
![Example Image](https://github.com/stequoy/Parking-Interaction-System/blob/main/images/alternative%20approach.png)

## Inference
- train_... notebooks produce trained tflite models
- compilation and co-compilation files compile the model for Edge TPU compatability
- inference.py provides a basic workflow of the device inference process
