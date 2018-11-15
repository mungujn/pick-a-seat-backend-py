
from google.cloud import firestore
import common.logger as log

db = None


def setUp():
    '''set up database'''
    global db

    if db is None:
        db = firestore.Client()


def getReference():
    '''get database object'''
    return db


def create(location, data):
    '''create data in the db'''
    nests = location.split('/')
    l = len(nests)

    if l == 2:
        log.info(f'Creating {nests[0]}/{nests[1]}')
        db.collection(nests[0]).document(nests[1]).set(data)
    elif l == 4:
        log.info(f'Creating {nests[0]}/{nests[1]}/{nests[2]}/{nests[3]}')
        db.collection(nests[0]).document(nests[1]).collection(
            nests[2]).document(nests[3]).set(data)


def read(location):
    '''read data in the db. returns None if the data does not exist'''
    nests = location.split('/')
    l = len(nests)

    try:
        if l == 2:
            log.info(f'Reading {nests[0]}/{nests[1]}')
            document = db.collection(nests[0]).document(nests[1]).get()
            return document.to_dict()
        elif l == 4:
            log.info(f'Reading {nests[0]}/{nests[1]}/{nests[2]}/{nests[3]}')
            document = db.collection(nests[0]).document(nests[1]).collection(
                nests[2]).document(nests[3]).get()
            return document.to_dict()
    except Exception as e:
        log.error('Exception while reading data', e)
        return None


def update(location, data):
    '''update data in the db'''
    nests = location.split('/')
    l = len(nests)

    if l == 2:
        log.info(f'Updating {nests[0]}/{nests[1]}')
        db.collection(nests[0]).document(nests[1]).update(data)
    elif l == 4:
        log.info(f'Updating {nests[0]}/{nests[1]}/{nests[2]}/{nests[3]}')
        db.collection(nests[0]).document(nests[1]).collection(
            nests[2]).document(nests[3]).update(data)


def delete(location):
    '''delete data in the db'''
    nests = location.split('/')
    l = len(nests)

    if l == 2:
        log.info(f'Deleting {nests[0]}/{nests[1]}')
        db.collection(nests[0]).document(nests[1]).delete()
    elif l == 4:
        log.info(f'Deleting {nests[0]}/{nests[1]}/{nests[2]}/{nests[3]}')
        db.collection(nests[0]).document(nests[1]).collection(
            nests[2]).document(nests[3]).delete()


def readAll(location):
    '''read all data in a location'''
    nests = location.split('/')
    l = len(nests)

    if l == 1:
        log.info(f'Reading all in {nests[0]}')
        documents = db.collection(nests[0]).get()
        return [document.to_dict() for document in documents]
    elif l == 3:
        log.info(f'Reading all {nests[0]}/{nests[1]}/{nests[2]}')
        documents = db.collection(nests[0]).document(nests[1]).collection(
            nests[2]).get()
        return [document.to_dict() for document in documents]


'''
def query(collection, value_1, value_2):
    # get all documents in collection where value_1 == value_2
    ref = db.collection(collection)
    documents = ref.where(value_1, '==', value_2)

    return [document.to_dict() for document in documents]'''
