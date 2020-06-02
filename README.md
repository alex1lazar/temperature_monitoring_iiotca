# Introduction to Internet of Things and Cloud Architecture Project

The main task of this project is to monitor temperature, asses if a "fever event" started or ended, and insert the events to both a locally stored database file, and to a real time database in Firebase.

## The 3 main components of the project:
- Temperature monitoring
- Fever monitoring
- Temperature data API

### Temperature monitoring

**Entities involved:** core module, database file

Due to the lack of a sensor, I used random library from python in order to generate int numbers from 33 to 41. The logic from core.py is able to query temperature information and stored it into the database.

For the local database I've used a simple .csv file. Temperature was read every 30 seconds for almost a day, and store into the local database.

### Fever monitoring

**Entities involved:** core module, Firebase(Real time Database)
1. If the temperature marks the beginning of a fever sequence then a
“FEVER_START_EVENT” is pushed to Firebase/Firestore
2. All subsequent temperature readings are posted to a Plotly graph.
3. If ten consecutive temperature readings do not present a fever characteristic then a
“FEVER_END_EVENT” is pushed to Firebase/Firestore and the ongoing publishing
to Plotly operation is stopped.

**Only** START and END events were posted to Firebase. Strangely, no sequence of 10 consecutive temperature without fever, after its start, was met. Therefore, no "FEVER_END_EVENT" is present either in database file or Firebase.

### Temperature data API

**Entities involved:** API module and database

The purpose of this feature is to provide comprehensive and digest data related to periods of
temperature monitoring.

In order to create a local server, I used Flask. It runs on port 5051, as asked. It has an introductory first page with helpful information regarding how can one use the API, and the current functionalities.


Resources used for help:

-- https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
-- https://realpython.com/python-csv/
-- https://docs.python.org/3/library/csv.html
-- further advice from colleagues, friends


