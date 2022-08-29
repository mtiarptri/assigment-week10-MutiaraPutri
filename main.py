
import time
import requests
import math
import random
from tkinter import Variable
import Adafruit_DHT
import time


TOKEN = "BBFF-Yp2chKv1ah5PiADZyjyArU6Up8g37R"  # Put your TOKEN here
DEVICE_LABEL = "coba"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here


def build_payload(varia_1, varia_2):

    sensor = Adafruit_DHT.DHT11
    pin = 4
    kelembaban, suhu = Adafruit_DHT.read(sensor, pin)

    value_1 = suhu
    value_2 = kelembaban

    payload = {varia_1: value_1,
               varia_2: value_2,
               }

    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(