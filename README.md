# Coordiante Conversion and Display Program
This program accepts various formats of latitude and longitude coordinates, converts them to a standard format, and then displays them on a world map using the GeoPandas and Matplotlib libraries. The coordinates are also stored in a GeoJSON file for further processing.

## Input Formats Supported
The program supports a wide range of formats for coordinates, including:

Decimal degrees: e.g., 40.446, -79.982
Decimal degrees with compass direction: e.g., 40.446 N, 79.982 W
Decimal degrees with inverted order: e.g., 79.982 W, 40.446 N
Decimal degrees with degrees symbol and compass direction: e.g., 40.446° N, 79.982° W
Degrees, minutes and compass direction: e.g., 40° 26.742' N, 79° 58.897' W
Degrees, minutes, seconds and compass direction: e.g., 40° 26' 45\" N, 79° 58' 53\" W

## Installation
To run the program, you will need the following Python libraries:

re
sys
json
matplotlib
geopandas


## Usage
Simply run the Python script and input your coordinates in the console. The program will prompt you to enter your coordinates. You can enter as many coordinates as you want. After entering all your coordinates, type 'display' to view the coordinates on a map.

Please note that the latitude should be between -90 and 90, and longitude should be between -180 and 180. The program will give an error if the input values are outside these ranges.

The coordinates will be displayed as red markers on a world map. The labels will be shown next to the markers.

## Issues
If the input format is not recognizable, you will see a message "Unable to process:" followed by the input line.
Ensure that latitudes are between -90 and 90 and longitudes are between -180 and 180. If not, you will receive an error message.
