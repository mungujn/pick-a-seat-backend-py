import common.logger as log
import common.database as db
db.setUp()

tables = {
    '1': {
        '1': {
            'name': 'Nickson',
            'taken': True
        },
        '6': {
            'name': 'Mungujakisa',
            'taken': True
        }
    }
}

default_seats = {
    '1': {'taken': False},
    '2': {'taken': False},
    '3': {'taken': False},
    '4': {'taken': False},
    '5': {'taken': False},
    '6': {'taken': False},
    '7': {'taken': False},
    '8': {'taken': False},
    '9': {'taken': False},
    '10': {'taken': False},
    '11': {'taken': False}
}


def getTableOccupancy(table_number):
    '''get the occupants of a table'''
    log.info(f'Getting occupants of table {table_number}')
    seats = tables.get(table_number, {})
    seats = {**default_seats, **seats}
    return seats


def updateTableOccupancy(table_number, seat_number):
    '''get the occupants of a table'''
    log.info(f'Updating seat {seat_number} of table {table_number}')
    return True, None
