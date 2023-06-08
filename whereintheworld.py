import sys
import re
import geopandas as gpd
import matplotlib.pyplot as plt
import json

# coordinate processing functions


def process_standard_input(coordinate):
    pattern = r"(-?\d{1,3}(?:\.\d+)?)(?:, | )(-?\d{1,3}(?:\.\d+)?)(?: (.+))?"
    match = re.match(pattern, coordinate)

    if not match:
        return None

    lat_value, lon_value, label = match.groups()

    if label is None:
        label = "coordinate"

    return process_geojson(lat_value, lon_value, label)


def process_standard_input_with_compass(coordinate):
    pattern = r"(-?\d+(\.\d+)?)\s*([NS]),?\s*(-?\d+(\.\d+)?)\s*([EW])(?: (.+))?"
    match = re.match(pattern, coordinate)

    if not match:
        return None

    lat_value, lat_dir, lon_value, lon_dir, label = float(match.group(
        1)), match.group(3), float(match.group(4)), match.group(6), match.group(7)

    lat_value = check_lat(lat_value, lat_dir)
    lon_value = check_lon(lon_value, lon_dir)

    if label is None:
        label = ""

    return process_geojson(lat_value, lon_value, label)


def process_standard_input_with_compass_inverted(coordinate):
    pattern = r"(-?\d+(\.\d+)?)\s*([EW]),?\s*(-?\d+(\.\d+)?)\s*([NS])(?: (.+))?"
    match = re.match(pattern, coordinate)

    if not match:
        return None

    lon_value, lon_dir, lat_value, lat_dir, label = float(match.group(
        1)), match.group(3), float(match.group(4)), match.group(6), match.group(7)

    lat_value = check_lat(lat_value, lat_dir)
    lon_value = check_lon(lon_value, lon_dir)

    if label is None:
        label = "coordinate"

    return process_geojson(lat_value, lon_value, label)


def process_standard_input_with_degrees_and_compass(coordinate):
    pattern = r"(\d+(\.\d+)?)°\s*([NS]),?\s*(\d+(\.\d+)?)°\s*([EW])(?: (.+))?"
    match = re.match(pattern, coordinate)

    if not match:
        return None

    lat_value, lat_dir, lon_value, lon_dir, label = float(match.group(1)), match.group(
        3), float(match.group(4)), match.group(6), match.group(7)

    lat_value = check_lat(lat_value, lat_dir)
    lon_value = check_lon(lon_value, lon_dir)

    if label is None:
        label = "coordinate"

    return process_geojson(lat_value, lon_value, label)


def process_dms(coordinate):
    pattern = r'(\d+)[°\s]+(\d+(\.\d+)?)[\'\s]*([NS])\s*,?\s*(\d+)[°\s]+(\d+(\.\d+)?)[\'\s]*([EW])(?: (.+))?'
    match = re.match(pattern, coordinate, re.IGNORECASE)

    if not match:
        return None

    lat_deg, lat_min, lat_dir = match.group(1), match.group(2), match.group(4)
    lon_deg, lon_min, lon_dir, label = match.group(
        5), match.group(6), match.group(8), match.group(9)

    lat_value = dms_to_decimal(lat_deg, lat_min, 0, lat_dir)
    lon_value = dms_to_decimal(lon_deg, lon_min, 0, lon_dir)

    if label is None:
        label = "coordinate"

    return process_geojson(lat_value, lon_value, label)


def process_dms_with_seconds(coordinate):
    pattern = r'(\d+)°\s*(\d+)\'\s*(\d+(\.\d+)?)\"?\s*([NS]),?\s*(\d+)°\s*(\d+)\'\s*(\d+(\.\d+)?)\"?\s*([EW])(?:\s*\((.+)\))?'
    match = re.match(pattern, coordinate, re.IGNORECASE)

    if not match:
        return None

    lat_deg, lat_min, lat_sec, lat_dir = int(match.group(1)), int(
        match.group(2)), float(match.group(3)), match.group(5)
    lon_deg, lon_min, lon_sec, lon_dir, label = int(match.group(6)), int(
        match.group(7)), float(match.group(8)), match.group(10), match.group(11)

    lat_value = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
    lon_value = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

    if label is None:
        label = "coordinate"

    return process_geojson(lat_value, lon_value, label)


# Modify dms_to_decimal to handle seconds as well


def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/3600

    if direction.upper() in ('S', 'W'):
        decimal_degrees = -decimal_degrees

    return decimal_degrees


# Coordinate conversion functions


def check_lat(lat_value, lat_dir):
    return abs(float(lat_value)) * (1 if lat_dir == "N" else -1)


def check_lon(lon_value, lon_dir):
    return abs(float(lon_value)) * (1 if lon_dir == "E" else -1)


def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/3600

    if direction.upper() in ('S', 'W'):
        decimal_degrees = -decimal_degrees

    return decimal_degrees


def process_geojson(lat_value, lon_value, label=""):
    if float(lat_value) >= 90 or float(lat_value) <= -90:
        print("Latitude must be between -90 & 90", file=sys.stderr)
        return None
    if float(lon_value) >= 180 or float(lon_value) <= -180:
        print("Longitude must be between -90 & 90", file=sys.stderr)
        return None
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon_value, lat_value]
        },
        "properties": {
            "name": label
        }
    }
    return geojson


def process_cord(coordinate):
    coordinate = coordinate.strip()

    processing_functions = [
        process_standard_input,
        process_standard_input_with_compass_inverted,
        process_standard_input_with_compass,
        process_standard_input_with_degrees_and_compass,
        process_dms,
        process_dms_with_seconds
    ]

    for function in processing_functions:
        if (geojson := function(coordinate)) is not None:
            return geojson

    return None

# Display function


def display_coordinates():
    df = gpd.read_file('./output.geojson')
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.plot()
    df.plot(ax=plt.gca(), color='red', markersize=50)

    for x, y, label in zip(df.geometry.x, df.geometry.y, df['name']):
        plt.text(x, y, label, fontsize=5)

    plt.show()


def main():

    print("Enter coordinates, then type 'display' to view coordinates on map:")
    feature_collection = {
        "type": "FeatureCollection"
    }
    features = []
    while True:
        try:
            value = input()
        except EOFError:
            break
        print("Checking Input")
        if(value == 'display'):
            break
        else:
            if (geojson := process_cord(value)) != None:
                features.append(geojson)
                print("Coordinate recieved successfully!")
            else:
                print("Unable to process:", value)
    feature_collection["features"] = features
    with open('output.geojson', 'w') as geojson_file:
        json.dump(feature_collection, geojson_file, indent=2)
    display_coordinates()


if __name__ == "__main__":
    main()
