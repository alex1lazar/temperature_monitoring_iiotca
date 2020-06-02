import csv
import json
import random
import time

from firebase import firebase

FEVER_START = 38.0
FEVER_LIMIT = 10
fever_continue = False
nonfever_count = 0
firebase = firebase.FirebaseApplication(
    'https://iiotca-temp.firebaseio.com', None)


def read_temperature():
    temperature = random.randrange(33, 40)
    return temperature


def insert_to_firebase(event):
    time = time_milli()
    data = json.dumps({
        'time': time,
        'event': event
    })
    firebase.post('/events', data)
    print('posted event to fb {}'.format(data))


def insert_to_db(temperature, event):
    time = time_milli()
    with open('db.csv', 'a') as db_file:
        writer = csv.writer(db_file, delimiter=",")
        writer.writerow([time, temperature, event])
        print('wrote to db: {} {} {}'.format(time, temperature, event))


def handle_fever(temperature, fever_continue, nonfever_count):
    event = "NO event"
    # temp bigger than 38 and fever_continue is false?
    if temperature >= FEVER_START and not fever_continue:
        event = "FEVER_START_EVENT"
        insert_to_firebase(event)
        insert_to_db(temperature, event)
        fever_continue = True
        nonfever_count = 0
        return

    # fever_continue is true and nonfever reached max of 10 times
    elif fever_continue and nonfever_count == FEVER_LIMIT:
        event = "FEVER_END_EVENT"
        insert_to_firebase(event)
        insert_to_db(temperature, event)
        fever_continue = False
        nonfever_count = 0
        return

    elif fever_continue and temperature < FEVER_START:
        insert_to_db(temperature, event)
        nonfever_count += 1
    elif fever_continue and temperature > FEVER_START:
        insert_to_db(temperature, event)
        nonfever_count = 0
    else:
        insert_to_db(temperature, event)


def monitor_temperature():
    count = 0
    while count < 3600 * 24:
        temperature = read_temperature()
        handle_fever(temperature, fever_continue, nonfever_count)
        count += 1
        print(temperature)
        print(time.time())
        time.sleep(30)


def time_milli():
    milli = time.time() * 1000
    return milli


def main():
    monitor_temperature()


if __name__ == "__main__":
    main()
