from flask import Flask, jsonify, request
from flask_cors import CORS
from common import auth, responses
import functions
import common.logger as log
log.setUp()

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:3000',
    'http://localhost:5000',
    'https://pamoja-wallet.firebaseapp.com'
])


def getTableOccupancy(table_number):
    '''Get a tables occupants
    '''
    log.start()
    log.info(f'GET: /table/{table_number}'.center(20, '-'))
    try:
        occupancy = functions.getTableOccupancy(table_number)
        return responses.respondWithData(occupancy)
    except Exception as error:
        log.info('error while trying to retreiving occupancy data')
        log.info('*'.center(20, '-'))
        return responses.respondInternalServerError(error)


@auth.validTicketRequired
def updateTableOccupancy(table_number, name):
    '''Edit table occupancy
    '''
    log.start()
    log.info(f'PUT: /table/{table_number}'.center(20, '-'))
    data_is_valid = validateDataForUpdate(request)
    if data_is_valid:
        try:
            occupant = request.get_json()
            occupant['name'] = name

            succeded, reason = functions.updateTableOccupancy(
                table_number, occupant)

            if succeded:
                return responses.respondOk('successfuly selected seat')
            else:
                return responses.respondBadRequest(reason)
        except Exception as error:
            log.info('error while selecting seat')
            log.info('*'.center(20, '-'))
            return responses.respondInternalServerError(error)
    else:
        log.info('*'.center(20, '-'))
        return responses.respondBadRequest('Invalid data sent')


def validateDataForUpdate(request):
    if request.is_json:
        data = request.get_json()
        if data.get('seat_number') is not None:
            return True
    return False


app.add_url_rule('/table/<table_number>', methods=['GET'],
                 endpoint='update', view_func=getTableOccupancy)
app.add_url_rule('/table/<table_number>', methods=['PUT'],
                 endpoint='table', view_func=updateTableOccupancy)


if __name__ == '__main__':
    # This is used when running locally only. When deployed to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
