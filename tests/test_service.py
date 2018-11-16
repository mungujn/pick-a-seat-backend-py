from service import app
import pytest
from flask import json

app.testing = True
client = app.test_client()


def test_getTable():

    r = client.get('/table/1')

    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['1'] == {'taken': False}


# test_getTable()


def test_updateTable():

    r = client.put('/table/1', json={
        'seat_number': 6,
        'email_address': 'example@gmail.com',
        'ticket_number': '1111111'
    })

    data = json.loads(r.data)
    print(data)
    assert r.status_code == 200


test_updateTable()
