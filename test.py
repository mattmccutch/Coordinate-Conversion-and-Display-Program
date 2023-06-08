import re
import json


def coordinates_to_geojson(coordinate_string):
    # Regex pattern to extract latitude, longitude, and their directions
    pattern = r'(\d+(\.\d+)?)\s*([NS]),?\s*(\d+(\.\d+)?)\s*([EW])'
    match = re.match(pattern, coordinate_string, re.IGNORECASE)

    if not match:
        return None

    lat, lat_dir, lon, lon_dir = float(match.group(1)), match.group(
        3), float(match.group(4)), match.group(6)

    if lat_dir.upper() == 'S':
        lat = -lat
    if lon_dir.upper() == 'W':
        lon = -lon

    # Create GeoJSON Point
    geojson = {
        "type": "Point",
        "coordinates": [lon, lat]
    }

    return json.dumps(geojson)


input_string = "45.9 S, 170.5 E"
geojson_str = coordinates_to_geojson(input_string)
print(geojson_str)
