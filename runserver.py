#!/usr/bin/env python3
import numpy as np
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
import json
from os import environ


app = Flask(__name__)
CORS(app)
distances = np.load('day/dist_matrix.npy')
locations = pd.read_csv('locations.csv', encoding="utf-8")
lat = locations['stop_lat']
lng = locations['stop_lng']
name = locations['stop_name']


def get_current_station(current_location):
    current_station = 0
    min_dist = 10**12

    # for station in xrange(locations.shape[0]):
    #     act_dist = np.linalg.norm(locations[station]-current_location)
    #     if act_dist < min_dist:
    #         min_dist = act_dist
    #         current_station = station
    # return current_station

    for station in range(locations.shape[0]):
        act_dist = np.linalg.norm(np.array([lat[station],
                                           lng[station]]) - current_location)
        if act_dist < min_dist:
            min_dist = act_dist
            current_station = station
    return current_station


def get_response_dict(current_station):
    response_array = []

    for station in range(locations.shape[0]):
        if np.isfinite(distances[current_station][station]):
            response_array.append({"lat": lat[station], "lng": lng[station],
                                   "value": distances[current_station][station],
                                   "name": name[station]})
    return {"stations": response_array}


def get_current_location(request):
    lat = float(request.args['lat'])
    lng = float(request.args['lng'])
    return np.array([lat, lng])


@app.route("/accessibility")
def hello():
    current_location = get_current_location(request)
    current_station = get_current_station(current_location)
    return json.dumps(get_response_dict(current_station), ensure_ascii=False)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
