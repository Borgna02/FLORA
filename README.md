# FLORA: Farming Life-cycle Observation with Real-time Analytics

## Introduction
Our project will monitor data related on both environment and plants that span from weather data such as temperature, humidity, rainfall, solar radiation, light intensity, CO2 level and soil moisture; going over plant’s health data such as ph, concentration of mineral salts, chlorophyll content, leaf temperature, plant stress levels and pest infestations; and lastly to crop yield data such as plant height and canopy density. 

The goal of the system is to streamline agricultural processes and empower farmers with better control over their fields, crops, and the large volumes of data they generate. Also allowing the visualization with a user friendly application showing gauges, graphs or other descriptive diagrams.

The system will analyze the data and alert the farmer in case of hazards concerning plant health like rotting, lack of water or excessive exposure to sunlight.


## Project build and deploy steps
After cloning the repository write in the terminal: 

    cd ./project

To build and run the project execute:

    docker-compose up --build

To delete all the containers execute:

    docker-compose down -v