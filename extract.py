#!/usr/bin/env python
import csv
import datetime
import json
import random
from argparse import ArgumentParser


def get_date(ts):
    ts = float(ts) / 1000
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


parser = ArgumentParser()
parser.add_argument('filepath', help='The full path to the positions JSON file')
parser.add_argument('size', help='The number of positions to pick, at random')
args = parser.parse_args()

with open(args.filepath) as f:
    data = json.load(f)

positions = []

for r in data['locations']:
    position = {}
    position['longitude'] = r['longitudeE7'] / 10**7
    position['latitude'] = float(r['latitudeE7']) / 10**7
    position['date'] = get_date(r['timestampMs'])
    positions.append(position)


with open('positions.csv', 'w') as csvfile:
    fieldnames = ['latitude', 'longitude', 'date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for p in random.choices(positions, k=int(args.size)):
        writer.writerow(p)
