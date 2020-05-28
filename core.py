import json
import random
import time

from firebase import firebase

FEVER_START = 38.0
FEVER_LIMIT = 10
fever_continue = False
fever_count = 0
firebase = firebase.FirebaseApplication(
    'https://iiotca-temp.firebaseio.com', None)


def read_temperature():
    temperature = random.randrange(33, 40)
    return temperature


def insert_firebase(event):
    time = time_milli()
    data = json.dumps({
        'time': time,
        'event': event
    })
    # firebase.child("events").push(data)
    firebase.post('/events', data)
    print('posted event to fb')


def handle_fever(temperature, fever_continue, fever_count):
    if temperature >= FEVER_START and not fever_continue:
        print("FEVER_START_EVENT")
        insert_firebase("FEVER_START_EVENT")
        fever_continue = True
        nonfever_count = 0
        return

    if fever_continue and nonfever_count == FEVER_LIMIT:
        insert_firebase("FEVER_END_EVENT")
        print("FEVER_END_EVENT")
        fever_continue = False
        nonfever_count = 0
        return

    if fever_continue and temperature < FEVER_START:
        nonfever_count += 1
        print("increased nonfever count: " + nonfever_count)
    if fever_continue and temperature > FEVER_START:
        print("reset nonfever count")
        nonfever_count = 0


def monitor_temperature():
    count = 25
    while count:
        temperature = read_temperature()
        handle_fever(temperature, fever_continue, fever_count)
        count -= 1
        print(temperature)
        print(time.time())
        time.sleep(5)


def time_milli():
    milli = time.time() * 1000
    return milli


def main():
    monitor_temperature()


if __name__ == "__main__":
    main()
