from dotenv import load_dotenv
load_dotenv()  # sets gcloud project
from functools import wraps
from flask import request
from common import responses, guests
import common.logger as log
cache = guests.CACHED_AUTH


def validTicketRequired(f):
    '''Middleware for checking that a correct email address and ticket number is being used'''
    log.start()

    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        email_address = None
        ticket_number = None

        if request.is_json:
            data = request.get_json()
            email_address = data.get('email_address')
            ticket_number = data.get('ticket_number')

        if email_address is None or ticket_number is None:
            return responses.respondUnauthorized('No email address or ticket number supplied')
        else:
            guest = cache.get(email_address)

            if guest is None:
                return responses.respondUnauthorized('Incorrect email address')

            if ticket_number != guest['ticket_number']:
                return responses.respondUnauthorized('Incorrect ticket number')

        return f(*args, **kwargs, name=guest['name'])
    return decoratedFunction
