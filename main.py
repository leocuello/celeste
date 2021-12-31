import csv
import numpy as np
from collections import defaultdict
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from decimal import *

data = np.random.randint(0, 10, size=(100000, 2))
results = defaultdict(list)
geolocator = Nominatim(user_agent="http")


def reference_city(value):
    city = value[0][0]
    state = value[0][3]
    country = "Argentina"
    geo = city + ',' + country
    try:
        loc = geolocator.geocode(geo)
        print(loc)

        if loc is not None:
            return [loc.latitude, loc.longitude]
        else:
            return [0, 0]
    except ValueError as error_message:
        print(error_message)
        return [0, 0]


def distance(reference, point):
    coords_1 = (reference[0], reference[1])
    coords_2 = (point[0], point[1])
    try:
        return geodesic(coords_1, coords_2).km
    except ValueError as error_message:
        print(error_message)
        return 0


def sumColumn(m, column):
    total = 0
    for row in range(len(m)):
        total += Decimal(m[row][column])
    return total


def central_point(value):
    length = len(value)
    sum_x = sumColumn(value, 1)
    sum_y = sumColumn(value, 2)
    return [sum_x / length, sum_y / length]


def open_file():
    with open('files/in.csv') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=';')
        for row in csvReader:
            value = [row[2], row[8], row[9], row[10]]
            results[row[2]].append(value)


def write_file():
    with open('files/out.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        for key, value in list(results.items()):
            total = len(value)
            reference = reference_city(value)
            point = central_point(value)
            dis = distance(reference, point)
            spamwriter.writerow([key, total, reference[0], reference[1], dis])


open_file()
write_file()
