
import json

from os.path import join, dirname


def status(mockname):
    return read(mockname).get('status')


def headers(mockname):
    return read(mockname).get('headers')


def body(mockname):
    return read(mockname).get('body')


def read(mockname):
    with open(join(dirname(__file__), 'responses', mockname + '.json'), 'r') as f:
        return json.load(f)
