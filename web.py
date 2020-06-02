import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


telephone_book = [
    {
        'id': 1,
        'name': 'Alex',
        'phone': '0722431032'
    },
    {
        'id': 2,
        'name': 'Wassup',
        'phone': 'not disclosed'
    },
    {
        'id': 3,
        'name': 'Sabou',
        'phone': '0256425804'
    }
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1 style="text-align: center">IIOTCA Project</h1>
  <h2> Temperature monitoring</h2>
  <br>
  <h3> More info about project </h3>
  <p><b>https://github.com/alex1lazar/temperature_monitoring_iiotca</b></b>
  <p> it is a useful link to find code, and further explanations</p>
  <h3> How should a link look like? </h3>
  <p>http://localhost:5051/temperature?start={start_date}&end={end_date}</p>
  <ul> 
  <li> start_date represents the start timestamp parameter in milliseconds </li>
  <li> end_date represents the end timestamp parameter in milliseconds </li>
  </ul>
  <br>
  <h3> Simple GET request example: </h3>
  <p> http://localhost:5051/temperature?start=1588229930147&end=1588229950147 </p>
  '''


@app.route('/all/books', methods=['GET'])
def api_all():
    return jsonify(telephone_book)


@app.route('/books', methods=["GET"])
def api_something():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR'

    result = []
    for book in telephone_book:
        if book['id'] == id:
            result.append(book)

    return jsonify(result)


app.run(port=5051)
