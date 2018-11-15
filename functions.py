import common.logger as log
import common.database as db

db.setUp()

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
    seats = db.read(f'events/dinner/tables/{table_number}')
    if seats is None:
        seats = {}
    seats = {**default_seats, **seats}
    return seats


def updateTableOccupancy(table_number, occupant):
    '''get the occupants of a table'''
    table_number = str(table_number)
    partial_seat_number = str(occupant['seat_number'])
    full_seat_number = table_number + str(occupant['seat_number'])
    log.info(f'Updating occupancy of seat {full_seat_number}')

    email_address = occupant['email_address']

    seats_current_occupant = db.read(f'events/dinner/seats/{full_seat_number}')
    requesting_occupants_seats = db.read(
        f'events/dinner/guests/{email_address}')

    if seats_current_occupant is None \
            and requesting_occupants_seats is None:
        return assignEmptySeat(table_number, email_address, full_seat_number, partial_seat_number, occupant)

    if seats_current_occupant is None \
            and requesting_occupants_seats is not None:
        old_table_number = requesting_occupants_seats['table_number']

        # clear from old seat
        old_seat_number = requesting_occupants_seats['seat_number']
        old_full_seat_number = old_table_number + old_seat_number
        db.delete(f'events/dinner/seats/{old_full_seat_number}')

        # clear from old table
        table = {}
        seat = {}
        seat['taken'] = False
        seat['name'] = None
        table[old_seat_number] = seat
        db.update(f'events/dinner/tables/{old_table_number}', table)

        # finally assign the new seat
        return assignEmptySeat(table_number, email_address, full_seat_number, partial_seat_number, occupant)

    return False, 'Seat already taken'


def assignEmptySeat(table_number, email_address, full_seat_number, partial_seat_number, occupant):
    '''Assigning empty seat to user with no previous seat selection'''
    log.info('Assigning empty seat to user with no previous seat selection')

    del occupant['email_address']
    del occupant['ticket_number']

    table = {}
    occupant['taken'] = True
    table[table_number] = occupant
    db.update(f'events/dinner/tables/{table_number}', table)

    seat = {}
    seat['taken'] = True
    seat['taken_by'] = email_address
    db.update(f'events/dinner/seats/{full_seat_number}', seat)

    guest = {}
    guest['has_seat'] = True
    guest['table_number'] = table_number
    guest['seat_number'] = partial_seat_number
    db.update(f'events/dinner/guests/{email_address}', guest)

    return True, f'You have selected seat {partial_seat_number} from table {table_number}'
