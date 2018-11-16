# Pick a seat backend (Python)

[![Build Status](https://travis-ci.com/mungujn/pick-a-seat-backend-py.svg?branch=master)](https://travis-ci.com/mungujn/pick-a-seat-backend-py)

Backend for a web app for reserving seats. The web apps code is available [here](https://www.github.com/mungujn/pick-a-seat-frontend)

The backend is built around the flask microframework.
Unlike the [Node.js](https://github.com/mungujn/pick-a-seat-backend) backend, here the single exposed endpoint is more 'REST' like.

GET '/table/{table-number}' returns a JSON object with occupancy details of the table specified by table-number

PUT '/table/{table-number}' updates a tables occupancy details.

## Running the project

- Install the requiremnts
- Create a firebase project in case you want to use the code as is. i.e if you want to use the cloud firestore database. Otherwise replace the database logic in the common/database.py file with the logic for whatever persistance store you want to use.
- Test using pytest
