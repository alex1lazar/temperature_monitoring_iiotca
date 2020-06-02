import csv
import json

import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

results = []


def get_db_data():
    with open('db.csv', 'r') as db_file:
        data = csv.reader(db_file, delimiter=",")
        for row in data:
            if row != []:
                results.append(
                    {'time': row[0], 'temperature': row[1],
                        'event': row[2]}
                )
    return results


@app.route('/all', methods=['GET'])
def all_results():
    return jsonify(results)


@app.route('/temperature', methods=['GET'])
def get_start_end():
    if 'start' and 'end' in request.args:
        start = int(float(request.args.get('start')))
        end = int(float(request.args.get('end')))
    else:
        return 'ERROR! Something wrong with the arguments.'

    data = {'start_date': start, 'end_date': end, 'measurements': []}
    for row in results:
        if int(float(row['time'])) >= start and int(float(row['time'])) <= end:
            data['measurements'].append(
                {'time': row['time'], 'value': row['temperature']})

    return jsonify(data)


@ app.route('/', methods=['GET'])
def home():
    return '''<h1 style="text-align: center">IIOTCA Project</h1>
  <h2> Temperature monitoring</h2>
  <br>
  <h3> For more info about project </h3>
  <p><b><a href="https://github.com/alex1lazar/temperature_monitoring_iiotca">Github Repo</a></b> is a useful place to find code, and further explanations</p>
  <h3> How should a link look like? </h3>
  <p>http://localhost:5051/temperature?start={start_date}&end={end_date}</p>
  <ul>
  <li> start_date represents the start timestamp parameter in milliseconds </li>
  <li> end_date represents the end timestamp parameter in milliseconds </li>
  </ul>
  <br>
  <h3> Simple GET request example </h3>
  <h4> See all data in the db: </h4>
  <p> <a href="http://localhost:5051/all">Check this</a> </p>
  <h4> See data w/ a start and an end </h4>
  <p> http://localhost:5051/temperature?start=start_date&end=end_date by replacing start_date and end_date </p>
  '''


def main():
    get_db_data()
    app.run(port=5051)
