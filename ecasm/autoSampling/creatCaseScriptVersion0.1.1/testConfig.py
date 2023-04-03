#!/usr/bin/python

import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

json_data = load_json("./config.json")

case_path = json_data["casePath"]
sampleTime = json_data['sampleTimes'][0]


print(case_path)
print(sampleTime)

