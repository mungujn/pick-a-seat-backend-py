from service import app
import pytest
from flask import json

app.testing = True
client = app.test_client()
skip = pytest.mark.skip(
    reason='private key env variable required for cloud firestore db interaction')

# unskip these after configuring a service account


@skip
def test_getTable():

    r = client.get('/table/1')

    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['1'] == {'name': None, 'taken': False}


# test_getTable()

@skip
def test_updateTable():

    r = client.put('/table/1', json={
        'seat_number': 6,
        'email_address': 'example@gmail.com',
        'ticket_number': '1111111'
    })

    data = json.loads(r.data)
    assert r.status_code == 400
    assert data['message'] == 'Seat already taken'


# test_updateTable()


def test_dummyForBuild():
    pass